/* SPDX-License-Identifier: MIT */
/* Copyright (c) 2026 Nunzio Raciti */
#ifndef LVSIM_IO_H
#define LVSIM_IO_H

#include <stdint.h>

typedef struct { int16_t x, y; uint8_t pressed; uint32_t key; uint8_t key_pressed; } lvsim_input_t;

int lvsim_open(int width, int height, int color_format, const char *title);
void lvsim_blit(int x, int y, int w, int h, const void *pixels, int stride_bytes);
void lvsim_present(void);
int lvsim_poll(lvsim_input_t *in);
int lvsim_wait(int timeout_ms);
int lvsim_stop_requested(void);
void lvsim_close(void);

#endif
