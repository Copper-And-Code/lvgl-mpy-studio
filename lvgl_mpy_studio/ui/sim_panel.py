import re
import secrets
import time
from pathlib import Path

from PySide6.QtCore import QProcess, QProcessEnvironment, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QImage, QPainter
from PySide6.QtNetwork import QHostAddress, QTcpServer, QTcpSocket
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QSplitter, QVBoxLayout, QWidget

from lvgl_mpy_studio.build.program import RESET_EXIT_CODE
from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.platform import RUNTIME_ENTRY, runtime_environment, runtime_path
from lvgl_mpy_studio.ui.sim_audio import TonePlayer
from lvgl_mpy_studio.ui.terminal import TerminalView, key_bytes
from lvgl_mpy_studio.ui.theme import canvas_color
from lvgl_mpy_studio.sim.protocol import Decoder, MessageType, encode_key, encode_pointer, encode_quit, encode_stop, encode_wheel


TONE_LINE = re.compile(r"\x1bLVSIM_TONE (\d+) (\d+)\r?\n")
TONE_PREFIX = "\x1b"


class SimScreen(QWidget):
    pointer = Signal(int, int, bool)
    key = Signal(int, bool)
    wheel = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QImage(800, 480, QImage.Format_RGB16)
        self.image.fill(Qt.black)
        self.scale = 1
        self.physical_pixels = False
        self.setMinimumSize(240, 144)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)
        self._pressed = False

    def set_image(self, image):
        self.image = image
        self.update()

    def toggle_zoom(self):
        self.scale = 2 if self.scale == 1 else 1
        self.update()

    def set_physical_pixels(self, enabled):
        self.physical_pixels = bool(enabled)
        self.update()

    def _target(self):
        if self.image.isNull():
            return QRectF()
        ratio = self.devicePixelRatioF() if self.physical_pixels else 1.0
        width, height = self.image.width() * self.scale / ratio, self.image.height() * self.scale / ratio
        factor = min(self.width() / width, self.height() / height)
        if self.physical_pixels:
            factor = min(factor, 1.0)
        width, height = width * factor, height * factor
        return QRectF((self.width() - width) / 2, (self.height() - height) / 2, width, height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), canvas_color())
        if not self.image.isNull():
            painter.setRenderHint(QPainter.SmoothPixmapTransform, False)
            painter.drawImage(self._target(), self.image)

    def _coordinates(self, position):
        target = self._target()
        if not target.contains(position):
            return None
        return (int((position.x() - target.x()) * self.image.width() / target.width()), int((position.y() - target.y()) * self.image.height() / target.height()))

    def mousePressEvent(self, event):
        self.setFocus()
        self._pressed = event.button() == Qt.LeftButton
        point = self._coordinates(event.position())
        if point:
            self.pointer.emit(point[0], point[1], self._pressed)

    def mouseMoveEvent(self, event):
        point = self._coordinates(event.position())
        if point:
            self.pointer.emit(point[0], point[1], self._pressed)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = False
        point = self._coordinates(event.position())
        if point:
            self.pointer.emit(point[0], point[1], self._pressed)

    typed = Signal(bytes)  # a program without pages reads the keys as its serial port

    def keyPressEvent(self, event):
        self.key.emit(event.key(), True)
        data = key_bytes(event.key(), event.modifiers(), event.text())
        if data:
            self.typed.emit(data)

    def keyReleaseEvent(self, event):
        self.key.emit(event.key(), False)

    def wheelEvent(self, event):
        self.wheel.emit(event.angleDelta().y())


class SimPanel(QWidget):
    frameReady = Signal()
    output = Signal(str, bool)
    started = Signal()
    stopped = Signal(int)
    error = Signal(str)
    tone = Signal(int, int)
    resetRequested = Signal()  # a program called machine.reset()

    def __init__(self, document=None, runtime=None, parent=None):
        super().__init__(parent)
        self.document = document
        self.runtime = Path(runtime) if runtime else runtime_path()
        self.process = QProcess(self)
        self.server = QTcpServer(self)
        self.socket = None
        self._token = None
        self._authenticated = False
        self.decoder = Decoder()
        self.framebuffer = QImage(800, 480, QImage.Format_RGB16)
        self.framebuffer.fill(Qt.black)
        self._hello_timer = QTimer(self)
        self._hello_timer.setSingleShot(True)
        self._hello_timer.timeout.connect(self._hello_timeout)
        self._quit_timer = QTimer(self)
        self._quit_timer.setSingleShot(True)
        self._quit_timer.timeout.connect(self._quit)
        self._kill_timer = QTimer(self)
        self._kill_timer.setSingleShot(True)
        self._kill_timer.timeout.connect(self._kill)
        self._frames = 0
        self._fps_started = 0.0
        self.fps = 0.0
        self.started_at = 0.0
        self.first_frame_ms = None
        self._stdout_tail = ""
        self.tone_player = TonePlayer(self)
        self.tone.connect(self.tone_player.play)
        self.screen = SimScreen()
        self.status = QLabel(tr("Simulator stopped"))
        self.physical_pixels = QCheckBox(tr("1:1 physical pixels"))
        self.physical_pixels.toggled.connect(self.screen.set_physical_pixels)
        status_row = QHBoxLayout()
        status_row.addWidget(self.status, 1)
        status_row.addWidget(self.physical_pixels)
        self.terminal = TerminalView()  # the serial port of a program without pages
        self.terminal.typed.connect(self.write_keys)
        self.terminal.setVisible(False)
        self.program = False
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.screen)
        splitter.addWidget(self.terminal)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        layout = QVBoxLayout(self)
        layout.addWidget(splitter, 1)
        layout.addLayout(status_row)
        self.server.newConnection.connect(self._accept_connection)
        self.process.readyReadStandardOutput.connect(self._stdout)
        self.process.readyReadStandardError.connect(self._stderr)
        self.process.finished.connect(self._finished)
        self.process.errorOccurred.connect(self._process_error)
        self.screen.pointer.connect(self.send_pointer)
        self.screen.key.connect(self.send_key)
        self.screen.typed.connect(self.write_keys)
        self.screen.wheel.connect(self.send_wheel)

    @property
    def running(self):
        return self.process.state() != QProcess.NotRunning

    def start(self, build_dir, arguments=None, environment=None):
        """Start the app generated in build_dir; with arguments, a program without pages (build/program.py)."""
        if self.running:
            raise RuntimeError(tr("The simulator is already running"))
        executable = self.runtime
        if not executable.exists():
            raise FileNotFoundError(tr("Executable not found: {path}", path=executable))
        self.stop_server()
        self._token = secrets.token_bytes(16)
        self._authenticated = False
        if not self.server.listen(QHostAddress.LocalHost, 0):
            raise RuntimeError(self.server.errorString())
        self.decoder = Decoder()
        self._frames = 0
        self._fps_started = time.monotonic()
        self.first_frame_ms = None
        env = QProcessEnvironment()
        settings = {**(environment or {}), "LVSIM_CONNECT": f"127.0.0.1:{self.server.serverPort()}", "LVSIM_TOKEN": self._token.hex()}
        for name, value in runtime_environment(**settings).items():
            env.insert(name, value)
        self.process.setProcessEnvironment(env)
        self.process.setWorkingDirectory(str(build_dir))
        self.process.setProgram(str(executable.resolve()))
        self.process.setArguments(arguments or RUNTIME_ENTRY)
        self.program = arguments is not None
        self.terminal.setVisible(self.program)
        self.terminal.input_enabled = self.program
        self.started_at = time.monotonic()
        self.status.setText(tr("Starting {target} simulator…", target="MicroPython"))
        if self.document and not self.program:  # a program is not the open project: that stays editable
            self.document.read_only = True
        self.process.start()
        if self.running:  # if the start already failed, _process_error released everything
            self.started.emit()

    def _accept_connection(self):
        if self.socket:
            self.server.nextPendingConnection().disconnectFromHost()
            return
        self.socket = self.server.nextPendingConnection()
        self.socket.readyRead.connect(self._read_socket)
        self.socket.disconnected.connect(self._socket_closed)
        self._hello_timer.start(2000)
        self._read_socket()

    def _hello_timeout(self):
        if self.socket and not self._authenticated:
            self.error.emit(tr("Simulator protocol: {error}", error=tr("HELLO not received within 2 seconds")))
            self.stop()

    def _socket_closed(self):
        socket = self.socket
        self.socket = None
        self._authenticated = False
        self._hello_timer.stop()
        if socket:
            socket.deleteLater()

    def _read_socket(self):
        if not self.socket:
            return
        data = bytes(self.socket.readAll())
        if not data:
            return
        try:
            messages = self.decoder.feed(data)
            for kind, payload in messages:
                self._message(kind, payload)
        except (ValueError, TypeError) as exc:
            self.error.emit(tr("Simulator protocol: {error}", error=exc))
            self.stop()

    def _message(self, kind, payload):
        if not self._authenticated and kind != MessageType.HELLO:
            raise ValueError(tr("Expected authenticated HELLO"))
        if kind == MessageType.HELLO:
            if self._authenticated or not secrets.compare_digest(payload["token"], self._token):
                raise ValueError(tr("Invalid simulator token"))
            if payload["version"] != 2:
                raise ValueError(tr("Unsupported protocol version"))
            if payload["format"] != 1:
                raise ValueError(tr("Unsupported color format"))
            self._authenticated = True
            self._hello_timer.stop()
            self.framebuffer = QImage(payload["width"], payload["height"], QImage.Format_RGB16)
            self.framebuffer.fill(Qt.black)
            self.screen.set_image(self.framebuffer)
            self.status.setText(f"{payload['width']}×{payload['height']} RGB565")
        elif kind == MessageType.RECT:
            rect = QImage(payload["pixels"], payload["width"], payload["height"], payload["width"] * 2, QImage.Format_RGB16).copy()
            painter = QPainter(self.framebuffer)
            painter.drawImage(payload["x"], payload["y"], rect)
            painter.end()
        elif kind == MessageType.PRESENT:
            self.screen.set_image(self.framebuffer)
            self._frames += 1
            if self.first_frame_ms is None:
                self.first_frame_ms = (time.monotonic() - self.started_at) * 1000
            elapsed = time.monotonic() - self._fps_started
            if elapsed >= 1:
                self.fps = self._frames / elapsed
                self._frames = 0
                self._fps_started = time.monotonic()
                self.status.setText(f"{self.framebuffer.width()}×{self.framebuffer.height()} · {self.fps:.0f} fps")
            self.frameReady.emit()

    def _send(self, data):
        if self.socket and self.socket.state() == QTcpSocket.ConnectedState:
            self.socket.write(data)
            self.socket.flush()

    def send_pointer(self, x, y, pressed):
        self._send(encode_pointer(x, y, pressed))

    def send_key(self, code, pressed):
        if not self.program:  # a program reads keys from its serial port, not from LVGL
            self._send(encode_key(code, pressed))

    def write_keys(self, data):
        if self.program and self.running:
            self.process.write(data)

    def send_wheel(self, delta):
        self._send(encode_wheel(delta))

    def _stdout(self):
        text = self._stdout_tail + bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="replace")
        if not self.program:
            text = text.replace("\r\n", "\n")
        self._stdout_tail = ""
        for match in TONE_LINE.finditer(text):
            self.tone.emit(int(match.group(1)), int(match.group(2)))
        text = TONE_LINE.sub("", text)
        partial = text.rfind(TONE_PREFIX)
        if partial >= 0:
            text, self._stdout_tail = text[:partial], text[partial:]
        if text and self.program:
            self.terminal.feed_serial(text)
        elif text:
            self.output.emit(text, False)

    def _stderr(self):
        text = bytes(self.process.readAllStandardError()).decode("utf-8", errors="replace")
        if self.program:
            self.terminal.feed_serial(text)
        else:
            self.output.emit(text.replace("\r\n", "\n"), True)

    def _process_error(self, error):
        self.error.emit(self.process.errorString())
        if error == QProcess.ProcessError.FailedToStart:  # finished does not arrive: it is unlocked here
            if self.document:
                self.document.read_only = False
            self.status.setText(tr("Simulator not started"))
            self.stop_server()
            self.stopped.emit(-1)

    def _finished(self, code, status):
        self._quit_timer.stop()
        self._kill_timer.stop()
        self.tone_player.stop()
        if self.document:
            self.document.read_only = False
        self.status.setText(tr("Simulator finished ({code})", code=code))
        self.terminal.input_enabled = False
        self.stop_server()
        self.stopped.emit(code)
        if self.program and code == RESET_EXIT_CODE:
            self.resetRequested.emit()

    def stop(self):
        if not self.running:
            self.stop_server()
            if self.document:
                self.document.read_only = False
            return
        self._send(encode_stop())
        self.status.setText(tr("Stopping simulator…"))
        self._quit_timer.start(500)
        self._kill_timer.start(2000)

    def _quit(self):
        if self.running:
            self._send(encode_quit())

    def _kill(self):
        if self.running:
            self.process.kill()

    def stop_server(self):
        socket = self.socket
        self.socket = None
        self._token = None
        self._authenticated = False
        self._hello_timer.stop()
        if socket:
            socket.disconnect(self)
            socket.disconnectFromHost()
            socket.deleteLater()
        self.server.close()

    def shutdown(self):
        self.stop()
        if self.running:
            self.process.waitForFinished(2500)
