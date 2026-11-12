# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
# In the simulator there is no pin: the state is kept and each change is printed.


class Block:
    def __init__(self, name="", pin=None, active_low=False, initial=False):
        self._name = name
        self._state = bool(initial)

    def set(self, value):
        value = bool(value)
        if value != self._state:
            self._state = value
            print(self._name + ": " + ("on" if value else "off"))

    def on(self):
        self.set(True)

    def off(self):
        self.set(False)

    def toggle(self):
        self.set(not self._state)

    def value(self):
        return self._state
