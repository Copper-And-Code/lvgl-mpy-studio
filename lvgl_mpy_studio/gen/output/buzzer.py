# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
"""Buzzer modules copied into projects."""

NOTICE = "# SPDX-License-Identifier: MIT\n# Copyright (c) 2026 Nunzio Raciti\n"

# In the simulator the sound comes from the PC: the IDE reads these markers from stdout.
SIMULATOR_BUZZER = '''import os
import sys

# In the browser the page plays the markers with Web Audio.
_active = sys.platform == "webassembly" or getattr(os, "getenv", lambda name: None)("LVSIM_CONNECT") is not None


def tone(freq):
    if _active:
        print("\\x1bLVSIM_TONE %d 0" % freq)


def beep(freq, ms=40):
    if _active:
        print("\\x1bLVSIM_TONE %d %d" % (freq, ms))


def off():
    if _active:
        print("\\x1bLVSIM_TONE 0 0")
'''

SILENT_BUZZER = '''def tone(freq):
    pass


def beep(freq, ms=40):
    pass


def off():
    pass
'''

PWM_BUZZER = '''PIN = {pin}
_pwm = None
_timer = None


def tone(freq):
    global _pwm
    if freq <= 0:
        off()
        return
    if _pwm is None:
        from machine import PWM, Pin

        _pwm = PWM(Pin(PIN), freq=int(freq), duty_u16=0)
    _pwm.freq(int(freq))
    _pwm.duty_u16(32768)


def off():
    if _pwm is not None:
        _pwm.duty_u16(0)


def _stop(timer):
    off()
    timer.pause()


def beep(freq, ms=40):
    global _timer
    import lvgl as lv

    tone(freq)
    if _timer is None:
        _timer = lv.timer_create(_stop, ms, None)
    else:
        _timer.set_period(ms)
        _timer.reset()
        _timer.resume()
'''

AUDIO_BUZZER = '''import audio


def tone(freq):
    if freq <= 0:
        off()
    else:
        audio.tone(int(freq))


def off():
    audio.finish()


def beep(freq, ms=40):
    audio.beep(int(freq), ms)
'''
