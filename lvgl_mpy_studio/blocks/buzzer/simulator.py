# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
import os
import sys

# In the browser the page plays the markers with Web Audio.
_active = sys.platform == "webassembly" or getattr(os, "getenv", lambda name: None)("LVSIM_CONNECT") is not None


def tone(freq):
    if _active:
        print("\x1bLVSIM_TONE %d 0" % freq)


def beep(freq, ms=40):
    if _active:
        print("\x1bLVSIM_TONE %d %d" % (freq, ms))


def off():
    if _active:
        print("\x1bLVSIM_TONE 0 0")
