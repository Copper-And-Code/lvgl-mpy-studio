# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
from machine import Pin


class Block:
    def __init__(self, name="", pin=None, active_low=False, initial=False):
        if pin is None:
            raise ValueError(name + ": set the Pin property")
        self._active_low = bool(active_low)
        self._state = bool(initial)
        self._pin = Pin(pin, Pin.OUT, value=self._level())

    def _level(self):
        return int(self._state != self._active_low)

    def set(self, value):
        self._state = bool(value)
        self._pin.value(self._level())

    def on(self):
        self.set(True)

    def off(self):
        self.set(False)

    def toggle(self):
        self.set(not self._state)

    def value(self):
        return self._state
