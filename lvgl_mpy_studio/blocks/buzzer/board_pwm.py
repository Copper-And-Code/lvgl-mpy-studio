# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
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
