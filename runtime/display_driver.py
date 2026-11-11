# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
import os
import time
import lvgl as lv
import lvsim

_getenv = getattr(os, "getenv", lambda name: None)  # MicroPython for the browser has no os.getenv

_width = 0
_height = 0
_buffer = None
_display = None
_pointer = None
_state = (0, 0, 0, 0, 0)
_started = lvsim.ticks_ms()


def _flush(display, area, _color_p):
    x1, y1 = area.x1, area.y1
    w, h = area.get_width(), area.get_height()
    stride = _width * 2
    offset = (y1 * _width + x1) * 2
    lvsim.blit(x1, y1, w, h, memoryview(_buffer)[offset:], stride)
    if display.flush_is_last():
        lvsim.present()
    display.flush_ready()


def _read(_indev, data):
    data.point.x = _state[0]
    data.point.y = _state[1]
    data.state = lv.INDEV_STATE.PRESSED if _state[2] else lv.INDEV_STATE.RELEASED


def init(width, height, title="LVGL MPY Studio"):
    global _width, _height, _buffer, _display, _pointer
    _width, _height = width, height
    lvsim.open(width, height, title)
    lv.init()
    _buffer = bytearray(width * height * 2)
    _display = lv.display_create(width, height)
    _display.set_color_format(lv.COLOR_FORMAT.RGB565)
    _display.set_buffers(_buffer, None, len(_buffer), lv.DISPLAY_RENDER_MODE.DIRECT)
    _display.set_flush_cb(_flush)
    _pointer = lv.indev_create()
    _pointer.set_type(lv.INDEV_TYPE.POINTER)
    _pointer.set_display(_display)
    _pointer.set_read_cb(_read)
    return _display


def poll():
    global _state
    state = lvsim.poll()
    if state is None:
        return False
    _state = state
    return True


def tick():
    global _started
    override = _getenv("LVSIM_TICK_MS")
    if override is not None:
        return int(override)
    now = lvsim.ticks_ms()
    elapsed = time.ticks_diff(now, _started)
    _started = now
    return elapsed


def wait(milliseconds):
    lvsim.wait(milliseconds)


def idle_ms():
    return 5


def close():
    lvsim.close()
