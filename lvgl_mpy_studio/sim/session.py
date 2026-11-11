"""Simulator driven by a program: the same protocol as the IDE, without Qt or a window."""

import json
from pathlib import Path
import re
import secrets
import socket
import subprocess
import tempfile
import threading
import time

from lvgl_mpy_studio.build.preview import prepare_page
from lvgl_mpy_studio.platform import CREATE_NO_WINDOW, RUNTIME_ENTRY, runtime_environment, runtime_path
from lvgl_mpy_studio.sim.protocol import Decoder, MessageType, encode_key, encode_pointer, encode_quit

START_TIMEOUT = 5
TAP_HOLD = 0.08  # longer than one read period of the indev, or LVGL does not see the touch
QUIT_TIMEOUT = 0.5
TONE_LINE = re.compile(r"\x1bLVSIM_TONE (\d+) (\d+)\r?\n")
PROBE_LINE = re.compile(rb"\x1bLVSIM_PROBE (\d+) (ok|error) (.*?)\r?$")
PARTIAL_LIMIT = 1 << 16  # a line without an end must not grow without limit
CONSOLE_LIMIT = 1 << 20  # an app that prints a lot must not make the memory of the session grow
PROBE_TIMEOUT = 2
ADVANCE_TIMEOUT = 120  # limit in real seconds for a simulated wait: a blocked app does not stop whoever drives it
PROBE_NAME = "lms_probe"  # stepped by main.py after every LVGL turn

# Module added only to the copy of the project that runs in the session: never on the board.
# It reads JSON requests from standard input between two frames and answers on stdout.
# With the simulated clock time advances in fixed steps only when the session asks:
# the game is repeatable and does not wait for real time.
PROBE_MODULE = """import io
import json
import select
import sys

import display_driver
import lvgl as lv

PAGES = {pages!r}
VIRTUAL = {virtual!r}
STEP = {step!r}
MARK = "\\x1bLVSIM_PROBE "
now = 0
_until = 0
_frames = 0
_input = [0, 0, 0, 0, 0]
_open = True
_advance = None
_poll = select.poll()
_poll.register(sys.stdin, select.POLLIN)

if {seed!r} is not None:
    import random
    random.seed({seed!r})

if VIRTUAL:
    import time as _time

    class _Clock:
        # The game code sees simulated time: time.ticks_ms() must agree with LVGL.
        def ticks_ms(self):
            return now

        def ticks_us(self):
            return now * 1000

        def ticks_cpu(self):
            return now * 1000

        def ticks_diff(self, end, start):
            return _time.ticks_diff(end, start)

        def ticks_add(self, ticks, delta):
            return _time.ticks_add(ticks, delta)

        def sleep_ms(self, milliseconds):
            global now
            now += milliseconds

        def sleep_us(self, microseconds):
            global now
            now += microseconds // 1000

        def sleep(self, seconds):
            global now
            now += int(seconds * 1000)

        def time(self):
            return _epoch + now // 1000

        def time_ns(self):
            return (_epoch * 1000 + now) * 1000000

        def localtime(self, seconds=None):
            # Local time in UTC: the time zone of the PC would change the screens from one computer to another.
            return _time.gmtime(self.time() if seconds is None else seconds)

        def gmtime(self, seconds=None):
            return _time.gmtime(self.time() if seconds is None else seconds)

        def __getattr__(self, name):
            return getattr(_time, name)

    _epoch = 1767225600  # 2026-01-01 00:00 UTC, the same for every run: date and time repeat too
    sys.modules["time"] = sys.modules["utime"] = _Clock()
    _real_flush = display_driver._flush
    _real_poll = display_driver.poll

    def _flush(display, area, color):
        global _frames
        last = display.flush_is_last()
        _real_flush(display, area, color)
        if last:
            _frames += 1

    def _poll_input():
        if not _real_poll():
            return False
        display_driver._state = tuple(_input)
        return True

    display_driver._flush = _flush
    display_driver.poll = _poll_input
    def _tick():
        # Time advances before lv.timer_handler(): callbacks see the same instant as LVGL.
        global now
        now += STEP
        return STEP

    display_driver.tick = _tick
    display_driver.wait = lambda milliseconds: None


def page():
    import ui
    return PAGES[ui.current_screen]


def _count(obj):
    total = 0
    for index in range(obj.get_child_count()):
        total += 1 + _count(obj.get_child(index))
    return total


def objects():
    return _count(lv.screen_active())


def _encode(value):
    try:
        return json.dumps(value)
    except Exception:
        return json.dumps(repr(value))


def _answer(number, status, payload):
    print(MARK + str(number) + " " + status + " " + payload)


def _serve(line):
    global _open, _until, _advance
    if not line:
        _open = False
        return
    request = json.loads(line)
    kind = request["kind"]
    if kind == "advance":
        _until = now + request["ms"]
        _advance = request["id"]
        return
    if kind == "input":
        _input[:] = request["state"]
        _answer(request["id"], "ok", "null")
        return
    import app_events
    names = app_events.__dict__
    try:
        if kind == "exec":
            exec(request["source"], names)
            result = None
        else:
            scope = dict(names)
            scope["page"] = page
            scope["objects"] = objects
            result = eval(request["source"], scope)
        _answer(request["id"], "ok", _encode(result))
    except Exception as exc:
        stream = io.StringIO()
        sys.print_exception(exc, stream)
        _answer(request["id"], "error", json.dumps(stream.getvalue()))


def step():
    global now, _advance
    if not VIRTUAL:
        while _open and _poll.poll(0):
            _serve(sys.stdin.readline())
        return
    while _open and now >= _until:
        if _advance is not None:
            _answer(_advance, "ok", json.dumps({{"now": now, "frames": _frames}}))
            _advance = None
        _serve(sys.stdin.readline())
"""
VIRTUAL_STEP_MS = 10


class SimulationError(RuntimeError):
    pass


class Session:
    """Run the project; use it with `with`.

    clock="virtual": time advances in fixed steps only with wait(), so the game is repeatable
    and faster than real time. clock="real": the game runs as in the IDE panel.
    """

    def __init__(self, project, page_index=0, design_only=False, clock="virtual", seed=None):
        if clock not in ("virtual", "real"):
            raise ValueError(f"unknown clock {clock!r}")
        self.project = project
        self.page_index = page_index
        self.design_only = design_only
        self.virtual = clock == "virtual"
        self.seed = seed
        self._now = 0
        self._started = time.monotonic()
        self._input = [0, 0, 0, 0, 0]
        self.width = self.height = 0
        self.frames = 0
        self._redraw = self._new_redraw()
        self._pending = (0, 0)
        self._pixels = None
        self._shown = None
        self._changed = threading.Condition()
        self._closed = False
        self._error = None
        self._output = bytearray()
        self._partial = b""
        self._answers = {}
        self._requests = 0
        self._broken = False

    def __enter__(self):
        if not runtime_path().exists():
            raise SimulationError("runtime not built")
        self._temporary = tempfile.TemporaryDirectory(prefix="lvgl-mpy-studio-session-")
        try:
            self._start(Path(self._temporary.name))
        except BaseException:
            self.__exit__(None, None, None)
            raise
        return self

    def __exit__(self, *_details):
        process = getattr(self, "_process", None)
        connection = getattr(self, "_connection", None)
        if process and process.stdin:
            try:
                process.stdin.close()  # with the simulated clock the app is stopped waiting for commands
            except OSError:
                pass
        if connection:
            try:
                connection.sendall(encode_quit())
            except OSError:
                pass
        if process:
            try:
                process.wait(QUIT_TIMEOUT)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        if connection:
            connection.close()
        for thread in (getattr(self, "_reader", None), getattr(self, "_printer", None)):
            if thread:
                thread.join()
        self.console_text = self._read_console()
        self._temporary.cleanup()

    def _start(self, directory):
        prepare_page(self.project, self.page_index, directory, self.design_only, expose_all=True, loop_module=PROBE_NAME)
        self._add_probe(directory)
        token = secrets.token_bytes(16)
        with socket.create_server(("127.0.0.1", 0)) as server:
            server.settimeout(START_TIMEOUT)
            environment = runtime_environment(LVSIM_CONNECT=f"127.0.0.1:{server.getsockname()[1]}", LVSIM_TOKEN=token.hex())
            self._process = subprocess.Popen([str(runtime_path()), *RUNTIME_ENTRY], cwd=directory, env=environment, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=CREATE_NO_WINDOW)
            self._printer = threading.Thread(target=self._read_output, daemon=True)
            self._printer.start()
            try:
                self._connection, _address = server.accept()
            except TimeoutError as exc:
                raise SimulationError(f"The simulator did not start: {self._read_console()[-500:]}") from exc
        self._connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._token = token
        self._reader = threading.Thread(target=self._read, daemon=True)
        self._reader.start()
        with self._changed:
            self._changed.wait_for(lambda: self._shown is not None or self._closed, START_TIMEOUT)
            if self._error:
                raise SimulationError(self._error)
            if self._shown is None:
                raise SimulationError(f"The simulator drew no frame: {self._read_console()[-500:]}")

    def _read(self):
        decoder = Decoder()
        authenticated = False
        try:
            while data := self._connection.recv(1 << 16):
                for kind, message in decoder.feed(data):
                    if kind == MessageType.HELLO:
                        if authenticated or message["token"] != self._token:
                            raise ValueError("invalid HELLO")
                        authenticated = True
                        self.width, self.height = message["width"], message["height"]
                        self._pixels = bytearray(self.width * self.height * 2)
                    elif not authenticated:
                        raise ValueError("HELLO must come first")
                    elif kind == MessageType.RECT:
                        self._blit(message)
                    elif kind == MessageType.PRESENT:
                        with self._changed:
                            self._shown = bytes(self._pixels)
                            self.frames += 1
                            self._count_frame()
                            self._changed.notify_all()
        except ValueError as exc:
            self._error = str(exc)
        except OSError:
            pass
        with self._changed:
            self._closed = True
            self._changed.notify_all()

    def now(self):
        """Milliseconds since the start: simulated with the virtual clock, real otherwise."""
        return self._now if self.virtual else int((time.monotonic() - self._started) * 1000)

    def _new_redraw(self):
        return {"started": self.now(), "frames": 0, "pixels": 0, "rects": 0, "peak": 0}

    def _count_frame(self):
        pixels, rects = self._pending
        self._pending = (0, 0)
        if pixels:
            self._redraw["frames"] += 1
            self._redraw["pixels"] += pixels
            self._redraw["rects"] += rects
            self._redraw["peak"] = max(self._redraw["peak"], pixels)

    def reset_redraw(self):
        """Reset the measures: start-up redraws the whole screen and says nothing about the game."""
        with self._changed:
            self._redraw = self._new_redraw()
            self._pending = (0, 0)  # the current frame started before the reset

    def redraw(self):
        """How much the app redraws. On the board it can differ: an indication, not a measure."""
        with self._changed:
            data = dict(self._redraw)
        screen = self.width * self.height or 1
        frames = data["frames"] or 1
        seconds = max((self.now() - data["started"]) / 1000, 0.001)
        return {
            "seconds": round(seconds, 2), "framesDrawn": data["frames"], "framesPerSecond": round(data["frames"] / seconds, 1),
            "averagePixelsPerFrame": data["pixels"] // frames, "peakPixelsPerFrame": data["peak"],
            "averageScreenShare": round(data["pixels"] / frames / screen, 3), "peakScreenShare": round(data["peak"] / screen, 3),
            "pixelsPerSecond": round(data["pixels"] / seconds), "rectsPerFrame": round(data["rects"] / frames, 1),
        }

    def _blit(self, rect):
        x, y, width, height = rect["x"], rect["y"], rect["width"], rect["height"]
        self._pending = (self._pending[0] + width * height, self._pending[1] + 1)
        pixels = rect["pixels"]
        for row in range(height):
            target = y + row
            left = max(x, 0)
            right = min(x + width, self.width)
            if 0 <= target < self.height and left < right:
                start = (target * self.width + left) * 2
                source = (row * width + left - x) * 2
                self._pixels[start:start + (right - left) * 2] = pixels[source:source + (right - left) * 2]

    def _send(self, data):
        try:
            self._connection.sendall(data)
        except OSError:
            pass  # the console tells the outcome: the app may already have exited

    @property
    def running(self):
        return not self._closed and not self._broken and self._process.poll() is None

    @property
    def exit_code(self):
        return self._process.poll()

    def wait(self, seconds):
        """Let time pass; ends earlier if the app closes."""
        if self.virtual:
            milliseconds = round(seconds * 1000)
            if milliseconds <= 0:
                return
            answer = self._request({"kind": "advance", "ms": milliseconds}, min(PROBE_TIMEOUT + milliseconds / 100, ADVANCE_TIMEOUT))
            if answer and answer[0] == "ok":
                self._now = answer[1]["now"]
                with self._changed:  # pixels travel on the socket: wait for all of them
                    self._changed.wait_for(lambda: self.frames >= answer[1]["frames"] or self._closed, PROBE_TIMEOUT)
            return
        deadline = time.monotonic() + seconds
        with self._changed:
            while not self._closed and (left := deadline - time.monotonic()) > 0:
                self._changed.wait(left)

    def _pointer(self, x, y, pressed):
        if self.virtual:
            self._input[:3] = [x, y, int(pressed)]
            self._request({"kind": "input", "state": self._input})
        else:
            self._send(encode_pointer(x, y, pressed))

    def press(self, x, y):
        self._pointer(x, y, True)

    def move(self, x, y):
        self._pointer(x, y, True)

    def release(self, x, y):
        self._pointer(x, y, False)

    def tap(self, x, y):
        self.press(x, y)
        self.wait(TAP_HOLD)
        self.release(x, y)
        self.wait(TAP_HOLD)

    def drag(self, x, y, to_x, to_y, seconds):
        steps = max(2, round(seconds / 0.03))
        self.press(x, y)
        self.wait(TAP_HOLD)
        for step in range(1, steps + 1):
            self.move(x + (to_x - x) * step // steps, y + (to_y - y) * step // steps)
            self.wait(seconds / steps)
        self.wait(TAP_HOLD)
        self.release(to_x, to_y)
        self.wait(TAP_HOLD)

    def _key(self, code, pressed):
        if self.virtual:
            self._input[3:] = [code, int(pressed)]
            self._request({"kind": "input", "state": self._input})
        else:
            self._send(encode_key(code, pressed))

    def key(self, code):
        self._key(code, True)
        self.wait(TAP_HOLD)
        self._key(code, False)
        self.wait(TAP_HOLD)

    def frame(self):
        """Last complete frame, in RGB565."""
        with self._changed:
            return self._shown

    def _add_probe(self, directory):
        pages = [page.name for page in self.project.pages]
        source = PROBE_MODULE.format(pages=pages, virtual=self.virtual, step=VIRTUAL_STEP_MS, seed=self.seed)
        (directory / f"{PROBE_NAME}.py").write_text(source, encoding="utf-8", newline="\n")

    def _read_output(self):
        stream = self._process.stdout
        while data := stream.read1(1 << 16) if hasattr(stream, "read1") else stream.read(1 << 16):
            *lines, self._partial = (self._partial + data).split(b"\n")  # complete lines only
            with self._changed:
                if len(self._partial) > PARTIAL_LIMIT:
                    self._output += self._partial
                    self._partial = b""
                for line in lines:
                    match = PROBE_LINE.search(line)  # the app may have printed without a newline
                    if match:
                        try:
                            answer = json.loads(match.group(3))
                        except ValueError:
                            match = None  # the app printed something that looks like an answer: it is its own output
                    if match:
                        self._answers[int(match.group(1))] = (match.group(2).decode(), answer)
                        line = line[:match.start()]
                        if not line:
                            continue
                    self._output += line + b"\n"
                if len(self._output) > CONSOLE_LIMIT:
                    del self._output[:len(self._output) - CONSOLE_LIMIT]
                self._changed.notify_all()
        with self._changed:
            self._output += self._partial

    def _request(self, request, timeout=PROBE_TIMEOUT):
        """Send a request to the module in the app; None if it does not answer."""
        if self._broken:
            return None
        with self._changed:
            self._requests += 1
            number = self._requests
        try:
            self._process.stdin.write((json.dumps({**request, "id": number}) + "\n").encode())
            self._process.stdin.flush()
        except (OSError, ValueError):
            return None
        with self._changed:
            self._changed.wait_for(lambda: number in self._answers or self._closed, timeout)
            answer = self._answers.pop(number, None)
        if answer is None:
            # The app no longer reads: more requests would fill the pipe and block the session.
            self._broken = True
        return answer

    def probe(self, kind, source, timeout=PROBE_TIMEOUT):
        """Evaluate an expression ("eval") or run code ("exec") inside the app, between two frames.

        Return (True, value) or (False, traceback or reason).
        """
        answer = self._request({"kind": kind, "source": source}, timeout)
        if answer is None:
            return False, "the app did not answer: it is not running or its loop is blocked"
        status, value = answer
        return status == "ok", value

    def _read_console(self):
        with self._changed:
            return self._output.decode("utf-8", "replace")


def split_tones(text):
    """Split the tones of the simulated buzzer from the text: [{"hz", "ms"}, …]."""
    tones = [{"hz": int(hz), "ms": int(ms)} for hz, ms in TONE_LINE.findall(text)]
    return TONE_LINE.sub("", text), tones
