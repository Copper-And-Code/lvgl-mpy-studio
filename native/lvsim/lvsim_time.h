/* SPDX-License-Identifier: MIT */
/* Copyright (c) 2026 Nunzio Raciti */
#ifndef LVSIM_TIME_H
#define LVSIM_TIME_H

#include <stdint.h>

uint32_t lvsim_time_ms(void);
void lvsim_sleep_ms(uint32_t milliseconds);
void lvsim_time_open(void);
void lvsim_time_close(void);

#endif
