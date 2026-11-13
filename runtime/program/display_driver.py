# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
"""The display of a program without pages in the simulator, with the contract of a board's driver.

As on a board, importing it starts the display and LVGL, and start() serves LVGL in the
background: a thread of lvsim schedules _service every PERIOD_MS, which runs in the main thread
between two bytecodes, also while the program waits for a key. WIDTH, HEIGHT, BUFFERS and indev
are those of mpy-lvgl-boards; _task, _timer and _arm() are there too, because ansiterm.py of the
same repository replaces _task with its own.
"""
import os
import time

import lvgl as lv
import lvsim

PERIOD_MS = 5
WIDTH = int(os.getenv("LVSIM_WIDTH") or 800)
HEIGHT = int(os.getenv("LVSIM_HEIGHT") or 480)
BUFFERS = 1

_state = (0, 0, 0, 0, 0)
_buffer = bytearray(WIDTH * HEIGHT * 2)
_timer = None
_busy = False
_last = lvsim.ticks_ms()


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
    stop()
    print("display_driver: stopped by Ctrl-C (display_driver.start() resumes)")


def _task(_):
    """What a period does after the tick; a program may replace it, as ansiterm.py does."""
    try:
        lv.timer_handler()
    except KeyboardInterrupt:
        _interrupted()


def _service(_):
    global _busy, _last, _state
    if _busy:
        return
    _busy = True
    try:
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


def start():
    global _timer
    if _timer is None:
        _timer = PERIOD_MS
        lvsim.service(_service, PERIOD_MS)


def stop():
    global _timer
    if _timer is not None:
        _timer = None
        lvsim.service(None, 0)


def backlight(percent=None):
    """The simulator has no backlight: it is always full."""
    return 100 if percent is None else None


start()
