/* SPDX-License-Identifier: MIT */
/* Copyright (c) 2026 Nunzio Raciti */
#include "lvsim_time.h"

#include <windows.h>
#include <timeapi.h>

uint32_t lvsim_time_ms(void) {
    static LARGE_INTEGER frequency;
    LARGE_INTEGER now;
    if (!frequency.QuadPart) QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&now);
    return (uint32_t)((now.QuadPart * 1000) / frequency.QuadPart);
}

void lvsim_sleep_ms(uint32_t milliseconds) {
    SleepEx(milliseconds, TRUE);
}

void lvsim_time_open(void) {
    timeBeginPeriod(1);
}

void lvsim_time_close(void) {
    timeEndPeriod(1);
}
