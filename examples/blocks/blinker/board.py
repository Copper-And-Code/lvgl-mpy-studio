# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
# An LVGL timer does the blinking: it runs where LVGL runs, so a handler may touch the screen.
import lvgl as lv
from machine import Pin


class Block:
    def __init__(self, name="", pin=None, period=500, running=True, on_blinked=None):
        if pin is None:
            raise ValueError(name + ": set the Pin property")
        self._pin = Pin(pin, Pin.OUT, value=0)
        self._on = False
        self._handler = on_blinked
        self._timer = lv.timer_create(self._tick, max(1, int(period) // 2), None)
        if not running:
            self._timer.pause()
        self._running = bool(running)

    def _tick(self, timer):
        self._on = not self._on
        self._pin.value(int(self._on))
        if self._on and self._handler is not None:
            self._handler(self)

    def start(self):
        self._running = True
        self._timer.resume()

    def stop(self):
        self._running = False
        self._timer.pause()
        self._on = False
        self._pin.value(0)

    def set_period(self, ms):
        self._timer.set_period(max(1, int(ms) // 2))

    def is_running(self):
        return self._running
