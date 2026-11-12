# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
import audio


def tone(freq):
    if freq <= 0:
        off()
    else:
        audio.tone(int(freq))


def off():
    audio.finish()


def beep(freq, ms=40):
    audio.beep(int(freq), ms)
