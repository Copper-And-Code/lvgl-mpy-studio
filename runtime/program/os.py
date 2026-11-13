# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
"""The os module of the unix port, with what a board has and the unix port lacks.

This is how MicroPython documents extending a built-in module: with sys.path empty,
`from os import *` reaches the built-in one.
"""
import sys

_path = sys.path
sys.path = ()
try:
    from os import *  # noqa: F403
finally:
    sys.path = _path
del _path

import io  # noqa: E402
from collections import namedtuple  # noqa: E402

_uname = namedtuple("uname_result", ("sysname", "nodename", "release", "version", "machine"))
_dupterm = dupterm  # noqa: F405


def uname():
    board = getenv("LMS_BOARD") or "board"  # noqa: F405
    release = ".".join(str(part) for part in sys.implementation.version[:3])
    return _uname("simulator", "simulator", release, "v" + release + " LVGL MPY Studio simulator", board + " (simulator)")


class _Cooked(io.IOBase):
    """A board sends CR LF where a program prints LF; the unix port sends LF alone."""

    def __init__(self, stream):
        self.stream = stream
        self._carriage = False

    def write(self, data):
        out = bytearray()
        for byte in data:
            if byte == 10 and not self._carriage:
                out.append(13)
            out.append(byte)
            self._carriage = byte == 13
        self.stream.write(bytes(out))
        return len(data)

    def readinto(self, buffer):
        return self.stream.readinto(buffer)

    def ioctl(self, request, argument):
        return self.stream.ioctl(request, argument) if hasattr(self.stream, "ioctl") else 0


def dupterm(stream, index=0):
    previous = _dupterm(_Cooked(stream) if stream is not None else None, index)
    return previous.stream if isinstance(previous, _Cooked) else previous
