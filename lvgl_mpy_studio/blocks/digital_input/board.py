# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
# The pin is read by an LVGL timer, not by an interrupt: handlers run where touching LVGL is safe.
import lvgl as lv
from machine import Pin

PERIOD_MS = 10


class Block:
    def __init__(self, name="", pin=None, pull="up", active_low=True, debounce=30, on_changed=None, on_pressed=None, on_released=None):
        if pin is None:
            raise ValueError(name + ": set the Pin property")
        mode = {"up": Pin.PULL_UP, "down": Pin.PULL_DOWN}.get(pull)
        self._pin = Pin(pin, Pin.IN) if mode is None else Pin(pin, Pin.IN, mode)
        self._active_low = bool(active_low)
        self._handlers = (on_changed, on_pressed, on_released)
        self._needed = max(1, int(debounce) // PERIOD_MS)
        self._count = 0
        self._state = self._read()
        self._timer = lv.timer_create(self._poll, PERIOD_MS, None)

    def _read(self):
        return bool(self._pin.value()) != self._active_low

    def _poll(self, timer):
        now = self._read()
        if now == self._state:
            self._count = 0
            return
        self._count += 1
        if self._count >= self._needed:
            self._apply(now)

    def _apply(self, state):
        self._count = 0
        self._state = state
        for handler in (self._handlers[0], self._handlers[1 if state else 2]):
            if handler is not None:
                handler(self)

    def value(self):
        return self._state

    def simulate(self, value):
        if bool(value) != self._state:
            self._apply(bool(value))
