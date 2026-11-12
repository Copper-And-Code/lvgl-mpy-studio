import time

from PySide6.QtCore import Qt, QThread, QTimer, Signal
from PySide6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QProgressBar, QPushButton, QVBoxLayout, QWidget

from lvgl_mpy_studio.core.i18n import tr


class DeviceWorker(QThread):
    succeeded = Signal(object)
    failed = Signal(object)
    progress = Signal(int, int, str, int)

    def __init__(self, operation, parent=None):
        super().__init__(parent)
        self.operation = operation

    def run(self):
        try:
            self.succeeded.emit(self.operation())
        except Exception as exc:
            self.failed.emit(exc)


def duration(seconds):
    seconds = max(0, round(seconds))
    return f"{seconds // 60}:{seconds % 60:02}" if seconds >= 60 else tr("{seconds} s", seconds=seconds)


class UploadProgress(QDialog):
    """Shows how far the upload to the board is, and lets the user cancel it.

    It appears only when the upload takes longer than DELAY_MS. Boards reached through mpremote
    report nothing while a file is written, so between two reports the bar moves at the speed
    measured so far, and stops just before the end of the file. Until something is measured the
    speed is `rate`: the one of the last upload to that board, or a cautious guess."""

    cancelRequested = Signal()
    DELAY_MS = 800
    TICK_MS = 200
    FIRST_RATE = 4000  # bytes per second: slower than the boards measured, so the bar never runs ahead

    def __init__(self, parent=None, clock=time.monotonic, rate=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Uploading to the board"))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setModal(True)
        self.setMinimumWidth(420)
        self._clock = clock
        self._started = clock()
        self._sent = self._total = self._size = self._file_start = 0
        self._reported = self._first = None
        self.rate = float(rate or self.FIRST_RATE)  # bytes per second
        self._name = ""
        self._cancelling = False
        self.file_label = QLabel(tr("Preparing…"))
        self.bar = QProgressBar()
        self.bar.setRange(0, 0)  # busy until the first report
        self.detail_label = QLabel()
        self.cancel_button = QPushButton(tr("Cancel"))
        self.cancel_button.clicked.connect(self.reject)
        layout = QVBoxLayout(self)
        layout.addWidget(self.file_label)
        layout.addWidget(self.bar)
        row = QHBoxLayout()
        row.addWidget(self.detail_label, 1)
        row.addWidget(self.cancel_button)
        layout.addLayout(row)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(self.TICK_MS)
        self._show_timer = QTimer(self)
        self._show_timer.setSingleShot(True)
        self._show_timer.timeout.connect(self.show)
        self._show_timer.start(self.DELAY_MS)

    def report(self, sent, total, name, size):
        now = self._clock()
        if self._first is None:
            self._first = now  # what comes before is preparation, not writing
        elif sent > 0 and now > self._first:
            self.rate = sent / (now - self._first)
        if name != self._name:
            self._name, self._file_start = name, sent
        self._sent, self._total, self._size, self._reported = sent, total, size, now
        self._refresh()

    def shown_bytes(self):
        """The bytes the bar shows: those reported, plus the estimate for the file being written."""
        if not self._total:
            return 0
        limit = self._file_start + self._size * 0.95
        estimate = self._sent + self.rate * (self._clock() - self._reported)
        return int(max(self._sent, min(limit, estimate)))

    def _refresh(self):
        elapsed = self._clock() - self._started
        if self._cancelling:
            self.detail_label.setText(tr("Cancelling after the current command…"))
            return
        if not self._total:
            self.detail_label.setText(tr("Elapsed {time}", time=duration(elapsed)))
            return
        shown = self.shown_bytes()
        self.bar.setRange(0, 1000)
        self.bar.setValue(shown * 1000 // self._total)
        if self._name:
            self.file_label.setText(tr("Writing {name}", name=self._name))
        text = tr("{sent} of {total} kB", sent=f"{shown / 1024:.0f}", total=f"{self._total / 1024:.0f}") + " · " + tr("Elapsed {time}", time=duration(elapsed))
        left = (self._total - shown) / self.rate
        if left >= 1:
            text += " · " + tr("about {time} left", time=duration(left))
        self.detail_label.setText(text)

    def reject(self):
        """Cancel and Esc ask to stop: the window stays until the board answers."""
        if not self._cancelling:
            self._cancelling = True
            self.cancel_button.setEnabled(False)
            self._refresh()
            self.cancelRequested.emit()

    def finish(self):
        self._timer.stop()
        self._show_timer.stop()
        self.hide()
        self.deleteLater()


class DeviceConsole(QWidget):
    commandRequested = Signal(str)
    interruptRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumBlockCount(10000)
        layout.addWidget(self.output, 1)
        row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText(tr("MicroPython REPL command"))
        self.send = QPushButton(tr("Send"))
        self.interrupt = QPushButton(tr("Cancel operation"))
        self.interrupt.setEnabled(False)
        row.addWidget(self.input, 1)
        row.addWidget(self.send)
        row.addWidget(self.interrupt)
        layout.addLayout(row)
        self.send.clicked.connect(self.submit)
        self.input.returnPressed.connect(self.submit)
        self.interrupt.clicked.connect(self.interruptRequested)
        self.set_ready(False)

    def set_ready(self, ready):
        self.input.setEnabled(ready)
        self.send.setEnabled(ready)

    def set_busy(self, busy):
        self.interrupt.setEnabled(busy)

    def submit(self):
        source = self.input.text()
        if source.strip():
            self.input.clear()
            self.commandRequested.emit(source)

    def append(self, text):
        if text:
            self.output.insertPlainText(str(text))
            scrollbar = self.output.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())


class SelectDeviceDialog(QDialog):
    def __init__(self, ports, current=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Select Device"))
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(tr("Explicitly select the port; the board profile is configured in the project.")))
        form = QFormLayout()
        self.port = QComboBox()
        self.port.setEditable(True)
        for device in ports:
            label = f"{device['port']} — {device['description']} ({device['usb']})"
            self.port.addItem(label, device["port"])
        if current:
            index = self.port.findData(current)
            if index >= 0:
                self.port.setCurrentIndex(index)
            else:
                self.port.setEditText(current)
        elif not ports:
            self.port.setEditText("")
        form.addRow(tr("Port"), self.port)
        layout.addLayout(form)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.button(QDialogButtonBox.Ok).setText(tr("Select"))
        self.buttons.button(QDialogButtonBox.Cancel).setText(tr("Cancel"))
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def selected_port(self):
        return self.port.currentData() if self.port.currentIndex() >= 0 and self.port.currentText() == self.port.itemText(self.port.currentIndex()) else self.port.currentText().strip()
