/* SPDX-License-Identifier: MIT */
/* Copyright (c) 2026 Nunzio Raciti */
#define _POSIX_C_SOURCE 200809L
#include "lvsim_time.h"

#include <time.h>
#ifdef __EMSCRIPTEN__
#include <emscripten.h>
#endif

uint32_t lvsim_time_ms(void) {
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now);
    return (uint32_t)((uint64_t)now.tv_sec * 1000 + (uint64_t)now.tv_nsec / 1000000);
}

void lvsim_sleep_ms(uint32_t milliseconds) {
    #ifdef __EMSCRIPTEN__
    // In the browser a real wait would block the page: ASYNCIFY gives control back to the browser.
    emscripten_sleep(milliseconds);
    return;
    #endif
    struct timespec pause = {milliseconds / 1000, (long)(milliseconds % 1000) * 1000000};
    nanosleep(&pause, 0);
}

void lvsim_time_open(void) {
}

void lvsim_time_close(void) {
}
