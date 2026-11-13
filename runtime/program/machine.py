# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
"""The machine module of the unix port, with what a program without pages expects of a board."""
import sys

_path = sys.path
sys.path = ()
try:
    from machine import *  # noqa: F403
finally:
    sys.path = _path
del _path

RESET_EXIT_CODE = 75  # the IDE starts the simulator again when it ends with this code


def reset():
    """The IDE starts the program again, with the files of its flash as they are."""
    print("\r\nmachine.reset(): the simulator starts again")
    raise SystemExit(RESET_EXIT_CODE)  # not an Exception: a program's `except Exception` lets it through


def soft_reset():
    reset()


def reset_cause():
    return 1  # PWRON_RESET
