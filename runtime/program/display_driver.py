# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
"""The display of a program without pages in the simulator, with contract 1 of a board's driver.

The names an application may rely on are those of docs/display-driver.md in mpy-lvgl-boards:
CONTRACT, WIDTH, HEIGHT, BUFFERS, PERIOD_MS, indev, start(), stop(), running() and backlight().
As on a board, importing it starts the display and LVGL, and LVGL is served in the background. In
the simulator a thread of lvsim schedules _service every PERIOD_MS, which runs in the main thread
between two bytecodes, also while the program waits for a key. In the browser there are no
threads: lms_web_boot.py calls serve() while the program waits for a key or sleeps.

A Ctrl-C reaches the program and the screen goes on. Here, as on the STM32H743, a pending Ctrl-C
is not raised inside the service: it waits for the program. Should one land in the service all
the same, it is handed on as the boards do, and LVGL waits HOLD_MS before being served again.
_task, _timer and _arm() are the names ansiterm.py used before contract 1: deprecated, they stay
for this version.
"""
import os
import time

import micropython
import lvgl as lv
import lvsim

CONTRACT = 1
PERIOD_MS = 5
HOLD_MS = 30
try:
    from lms_board import HEIGHT, WIDTH  # the browser, where the page writes it: there is no os.getenv
except ImportError:
    WIDTH = int(os.getenv("LVSIM_WIDTH") or 800)
    HEIGHT = int(os.getenv("LVSIM_HEIGHT") or 480)
BUFFERS = 1

_state = (0, 0, 0, 0, 0)
_buffer = bytearray(WIDTH * HEIGHT * 2)
_timer = None
_busy = False
_last = lvsim.ticks_ms()
_hold = None  # until when LVGL waits after a Ctrl-C


def _flush(display, area, _color_p):
    x1, y1 = area.x1, area.y1
    offset = (y1 * WIDTH + x1) * 2
    lvsim.blit(x1, y1, area.get_width(), area.get_height(), memoryview(_buffer)[offset:], WIDTH * 2)
    if display.flush_is_last():
        lvsim.present()
    display.flush_ready()


def _read(_indev, data):
    data.point.x = _state[0]
    data.point.y = _state[1]
    data.state = lv.INDEV_STATE.PRESSED if _state[2] else lv.INDEV_STATE.RELEASED


lvsim.open(WIDTH, HEIGHT, "LVGL MPY Studio")
lv.init()
display = lv.display_create(WIDTH, HEIGHT)
display.set_color_format(lv.COLOR_FORMAT.RGB565)
display.set_buffers(_buffer, None, len(_buffer), lv.DISPLAY_RENDER_MODE.DIRECT)
display.set_flush_cb(_flush)
indev = lv.indev_create()
indev.set_type(lv.INDEV_TYPE.POINTER)
indev.set_display(display)
indev.set_read_cb(_read)


def _interrupted():
    """A Ctrl-C landed in the service: it goes back to the program, and LVGL waits a little."""
    global _hold
    _hold = time.ticks_add(lvsim.ticks_ms(), HOLD_MS)
    try:
        micropython.schedule(micropython.kbd_intr, None)
    except (ValueError, RuntimeError):
        pass  # a runtime without MICROPY_SCHEDULER_STATIC_NODES, or a full queue


def _task(_):
    """What a period does after the tick; deprecated: ansiterm.py replaced it before contract 1."""
    try:
        lv.timer_handler()
    except KeyboardInterrupt:
        _interrupted()


def _service(_):
    global _busy, _last, _state, _hold
    if _busy:
        return
    _busy = True
    try:
        if _hold is not None:
            if time.ticks_diff(_hold, lvsim.ticks_ms()) > 0:
                return
            _hold = None
        state = lvsim.poll()
        if state is None:  # the IDE closed the simulator
            stop()
            raise SystemExit
        _state = state
        now = lvsim.ticks_ms()
        lv.tick_inc(time.ticks_diff(now, _last))
        _last = now
        _task(None)
    finally:
        _busy = False


def _arm():
    """The board's timer may be one shot; this one is periodic, so there is nothing to arm."""


BACKGROUND = hasattr(lvsim, "service")  # the simulator; the browser serves LVGL from the waits


def start():
    """Resumes the background service; while LVGL is served it does nothing."""
    global _timer
    if _timer is None:
        _timer = PERIOD_MS
        if BACKGROUND:
            lvsim.service(_service, PERIOD_MS)


def stop():
    """Suspends the background service; the screen keeps the last image."""
    global _timer
    if _timer is not None:
        _timer = None
        if BACKGROUND:
            lvsim.service(None, 0)


def running():
    """True while LVGL is served in the background, also during the pause after a Ctrl-C."""
    return _timer is not None


def serve(milliseconds=PERIOD_MS):
    """One period, then the browser runs for a while: the board's timer, where there is none."""
    if _timer is not None:
        _service(None)
    lvsim.wait(milliseconds)


def backlight(percent=None):
    """The simulator has no backlight: it is always full."""
    return 100 if percent is None else None


start()
