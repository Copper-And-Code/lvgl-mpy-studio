# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
"""Starts a program without pages in the browser as a board would.

The browser has no threads, no serial port and no native code, so what a board gives through
interrupts happens here while the program waits: reading a key, sleeping or polling serves LVGL
and lets the browser run (lvsim.wait, with Asyncify). The program gets, through sys.modules,
modules that do this: sys with a stdin fed by the page and a stdout that also reaches os.dupterm,
time, select, micropython and machine. A program that computes for long without waiting keeps
the screen still, and the page too.

The page writes lms_board.py (WIDTH, HEIGHT, BOARD, ENTRY) and the program's files in /flash,
then runs `import lms_web_boot`.
"""
import builtins
from collections import namedtuple
import io
import os
import select as _select
import sys as _sys
import time as _time
import micropython as _micropython

try:
    import machine as _machine
except ImportError:  # MicroPython in the browser has none
    _machine = None

import js
import lms_board
import display_driver
from lms_sandbox import SandboxVfs

PERIOD_MS = 5
_print = builtins.print
_state = {"keys": "", "interrupt": 3, "dupterm": None, "carriage": False}


def _serve(milliseconds=PERIOD_MS):
    display_driver.serve(milliseconds)


def _take():
    """The keys the page collected; a Ctrl-C stops the program while kbd_intr allows it, as on a board."""
    more = js.lmsTake()
    if not more:
        return
    if _state["interrupt"] == 3 and "\x03" in more:
        _state["keys"] += more.split("\x03", 1)[0]
        raise KeyboardInterrupt
    _state["keys"] += more


def _mirror(text):
    """What the program prints goes to os.dupterm too, with CR LF as on a board."""
    stream = _state["dupterm"]
    if stream is None or not text:
        return
    out = bytearray()
    for byte in text.encode():
        if byte == 10 and not _state["carriage"]:
            out.append(13)
        out.append(byte)
        _state["carriage"] = byte == 13
    stream.write(bytes(out))


class _Stdin(io.IOBase):
    def read(self, size=1):
        while len(_state["keys"]) < size:
            _take()
            if len(_state["keys"]) >= size:
                break
            _serve()
        keys = _state["keys"]
        _state["keys"] = keys[size:]
        return keys[:size]

    def readline(self):
        line = ""
        while not line.endswith(("\r", "\n")):
            line += self.read(1)
        return line

    def readinto(self, buffer):
        data = self.read(1).encode()
        buffer[: len(data)] = data
        return len(data)


class _Stdout(io.IOBase):
    def write(self, text):
        if isinstance(text, (bytes, bytearray)):
            text = bytes(text).decode()
        _sys.stdout.write(text)
        _mirror(text)
        return len(text)


def _write(text):
    _sys.stdout.write(text)
    _mirror(text)


def _web_print(*values, sep=" ", end="\n", file=None):
    if file is not None and not isinstance(file, _Stdout):
        _print(*values, sep=sep, end=end, file=file)
        return
    _write(sep.join(str(value) for value in values) + end)


class _Module:
    """A module of the board: its own names first, the rest from the real module."""

    def __init__(self, real, **names):
        self._real = real
        for name, value in names.items():
            setattr(self, name, value)

    def __getattr__(self, name):
        return getattr(self._real, name)


def _print_exception(exc, file=None):
    buffer = io.StringIO()
    _sys.print_exception(exc, buffer)
    _web_print(buffer.getvalue(), end="", file=file)


def _sleep_ms(milliseconds):
    """Keys typed meanwhile wait for the next read; a Ctrl-C stops the sleep."""
    end = _time.ticks_add(_time.ticks_ms(), int(milliseconds))
    while True:
        _take()
        left = _time.ticks_diff(end, _time.ticks_ms())
        if left <= 0:
            return
        _serve(min(PERIOD_MS, left))


def _kbd_intr(character):
    _state["interrupt"] = character


class _Poll:
    def register(self, _stream, _mask=None):
        pass

    def unregister(self, _stream):
        pass

    def modify(self, _stream, _mask):
        pass

    def poll(self, timeout=-1):
        start = _time.ticks_ms()
        while True:
            _take()
            if _state["keys"]:
                return [(_stdin, _select.POLLIN)]
            if timeout >= 0 and _time.ticks_diff(_time.ticks_ms(), start) >= timeout:
                return []
            _serve()

    def ipoll(self, timeout=-1, _flags=0):
        return iter(self.poll(timeout))


def _reset():
    _write("\r\nmachine.reset(): the page starts again\r\n")
    js.location.reload()
    raise SystemExit


def _dupterm(stream, index=0):
    previous, _state["dupterm"] = _state["dupterm"], stream
    return previous


_Uname = namedtuple("uname_result", ("sysname", "nodename", "release", "version", "machine"))


def _uname():
    board = getattr(lms_board, "BOARD", "board")
    release = ".".join(str(part) for part in _sys.implementation.version[:3])
    return _Uname("browser", "browser", release, "v" + release + " LVGL MPY Studio in the browser", board + " (browser)")


_stdin, _stdout = _Stdin(), _Stdout()
_sys.modules["sys"] = _Module(_sys, stdin=_stdin, stdout=_stdout, print_exception=_print_exception)
_sys.modules["time"] = _Module(_time, sleep=lambda seconds: _sleep_ms(seconds * 1000), sleep_ms=_sleep_ms, sleep_us=lambda us: _sleep_ms(us // 1000) if us >= 1000 else None)
_sys.modules["select"] = _Module(_select, poll=_Poll)
_sys.modules["micropython"] = _Module(_micropython, kbd_intr=_kbd_intr)
_sys.modules["machine"] = _Module(_machine, reset=_reset, soft_reset=_reset, reset_cause=lambda: 1)
_sys.modules["os"] = _Module(os, dupterm=_dupterm, uname=_uname)
builtins.print = _web_print

os.umount("/")
os.mount(SandboxVfs("/flash"), "/")
os.chdir("/")
_sys.path[:] = ["", "/lib"]


def _read_line(prompt):
    _write(prompt)
    line = ""
    while True:
        key = _stdin.read(1)
        if key in ("\r", "\n"):
            _write("\r\n")
            return line
        if key in ("\x7f", "\x08"):
            if line:
                line = line[:-1]
                _write("\b \b")
        elif key == "\x1b":
            _stdin.read(2)  # an arrow or another sequence: not edited here
        elif key == "\x04" and not line:
            raise EOFError
        elif key >= " ":
            line += key
            _write(key)


def _repl():
    _write("\r\nThe program ended. MicroPython REPL in the browser; machine.reset() starts it again.\r\n")
    scope = {"__name__": "__main__"}
    while True:
        try:
            line = _read_line(">>> ")
        except KeyboardInterrupt:
            _write("\r\n")
            continue
        except EOFError:
            continue
        if not line.strip():
            continue
        try:
            exec(compile(line, "<stdin>", "single"), scope)
        except KeyboardInterrupt:
            _write("KeyboardInterrupt\r\n")
        except Exception as exc:  # noqa: BLE001  a REPL shows every error and goes on
            _print_exception(exc)


def _run():
    entry = lms_board.ENTRY
    with open(entry) as source:
        text = source.read()
    exec(compile(text, entry, "exec"), {"__name__": "__main__", "__file__": "/" + entry})


try:
    _run()
except KeyboardInterrupt:
    _write("\r\nKeyboardInterrupt\r\n")
except SystemExit:
    pass
except Exception as exc:  # noqa: BLE001  the traceback is what a board would print
    _print_exception(exc)
_repl()
