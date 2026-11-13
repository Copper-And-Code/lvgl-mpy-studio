# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
"""Starts a program without pages in the simulator as a board would.

The IDE runs this from a folder of its own, with os.py, machine.py and display_driver.py next to
it. Once they are imported, the program's flash (LMS_FLASH) becomes the root filesystem, standard
input becomes the board's serial port, and the program (LMS_ENTRY, a file of the flash, or
LMS_CODE, a line of code) runs as __main__. When it ends, a REPL takes the keys, as on a board.
"""
import os  # the extended os of this folder: imported before the root changes, it stays in sys.modules
import sys

import machine  # noqa: F401  (the extended machine, for the same reason)
import micropython
import display_driver  # noqa: F401  (starts the display and LVGL, as on a board)
import lvsim
from lms_sandbox import SandboxVfs

lvsim.keys()
os.umount("/")
os.mount(SandboxVfs(os.getenv("LMS_FLASH")), "/")
os.chdir("/")
sys.path[:] = ["", "/lib"]
micropython.kbd_intr(3)


def run_program():
    entry, code = os.getenv("LMS_ENTRY"), os.getenv("LMS_CODE")
    if code:
        exec(code, {"__name__": "__main__"})
    elif entry:
        with open(entry) as source:
            text = source.read()
        exec(compile(text, entry, "exec"), {"__name__": "__main__", "__file__": entry})


def repl():
    print("\r\nThe program ended. MicroPython REPL of the simulator; machine.reset() starts it again.")
    scope = {"__name__": "__main__"}
    while True:
        try:
            line = input(">>> ")
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            return
        if not line.strip():
            continue
        try:
            exec(compile(line, "<stdin>", "single"), scope)  # "single" prints each expression, as the REPL of a board
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
        except Exception as exc:  # noqa: BLE001  a REPL shows every error and goes on
            sys.print_exception(exc)


try:
    run_program()
except KeyboardInterrupt:
    print("\r\nKeyboardInterrupt")
except Exception as exc:  # noqa: BLE001  the traceback is what a board would print
    sys.print_exception(exc)
repl()
