# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
# In the simulator there is no pin: the input changes only with simulate().


class Block:
    def __init__(self, name="", pin=None, pull="up", active_low=True, debounce=30, on_changed=None, on_pressed=None, on_released=None):
        self._handlers = (on_changed, on_pressed, on_released)
        self._state = False

    def value(self):
        return self._state

    def simulate(self, value):
        value = bool(value)
        if value == self._state:
            return
        self._state = value
        for handler in (self._handlers[0], self._handlers[1 if value else 2]):
            if handler is not None:
                handler(self)
