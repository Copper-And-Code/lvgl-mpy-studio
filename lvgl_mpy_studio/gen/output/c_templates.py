# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
"""C templates included in built projects."""

MAIN_TEMPLATE = r'''#ifndef _WIN32
#define _POSIX_C_SOURCE 200809L
#endif
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#include <io.h>
#include <wchar.h>
#include <windows.h>
#endif
#include "lvgl.h"
#include "ui.h"
#include "lvsim_io.h"
#include "lvsim_time.h"

#define DISPLAY_WIDTH @WIDTH@
#define DISPLAY_HEIGHT @HEIGHT@
static uint8_t framebuffer[DISPLAY_WIDTH * DISPLAY_HEIGHT * 2];
static lv_display_t * display;
static lvsim_input_t input;

static void flush_cb(lv_display_t * disp, const lv_area_t * area, uint8_t * pixels)
{
    LV_UNUSED(pixels);
    int width = lv_area_get_width(area);
    int height = lv_area_get_height(area);
    lvsim_blit(area->x1, area->y1, width, height, framebuffer + (area->y1 * DISPLAY_WIDTH + area->x1) * 2, DISPLAY_WIDTH * 2);
    if (lv_display_flush_is_last(disp)) lvsim_present();
    lv_display_flush_ready(disp);
}

static void read_cb(lv_indev_t * indev, lv_indev_data_t * data)
{
    LV_UNUSED(indev);
    data->point.x = input.x;
    data->point.y = input.y;
    data->state = input.pressed ? LV_INDEV_STATE_PRESSED : LV_INDEV_STATE_RELEASED;
}

static void set_environment(const char * name, const char * value, int overwrite)
{
#ifdef _WIN32
    if (overwrite || getenv(name) == NULL) _putenv_s(name, value);
#else
    setenv(name, value, overwrite);
#endif
}

static void prepare_process(void)
{
#ifdef _WIN32
    wchar_t path[32768];
    DWORD length = GetModuleFileNameW(NULL, path, sizeof(path) / sizeof(path[0]));
    if (length == 0 || length >= sizeof(path) / sizeof(path[0])) return;
    wchar_t * separator = wcsrchr(path, L'\\');
    if (separator != NULL) {
        *separator = L'\0';
        SetCurrentDirectoryW(path);
        *separator = L'\\';
    }
    wchar_t * extension = wcsrchr(path, L'.');
    if (extension == NULL) return;
    wcscpy(extension, L".log");
    if (_wfreopen(path, L"w", stdout) != NULL) {
        _dup2(_fileno(stdout), _fileno(stderr));
        setvbuf(stdout, NULL, _IOLBF, 0);
    }
#endif
}

int main(int argc, char ** argv)
{
    prepare_process();
    if (argc == 2 && strcmp(argv[1], "--selftest") == 0) {
        set_environment("LVSIM_HEADLESS", "1", 1);
        set_environment("LVSIM_FRAMES", "1", 0);
        set_environment("LVSIM_DUMP", "selftest.raw", 0);
    } else if (argc != 1) {
        return 2;
    }
    const char * tick_override = getenv("LVSIM_TICK_MS");
    lv_init();
    if (lvsim_open(DISPLAY_WIDTH, DISPLAY_HEIGHT, 16, @TITLE@) != 0) return 1;
    display = lv_display_create(DISPLAY_WIDTH, DISPLAY_HEIGHT);
    lv_display_set_color_format(display, LV_COLOR_FORMAT_RGB565);
    lv_display_set_buffers(display, framebuffer, NULL, sizeof(framebuffer), LV_DISPLAY_RENDER_MODE_DIRECT);
    lv_display_set_flush_cb(display, flush_cb);
    lv_indev_t * pointer = lv_indev_create();
    lv_indev_set_type(pointer, LV_INDEV_TYPE_POINTER);
    lv_indev_set_display(pointer, display);
    lv_indev_set_read_cb(pointer, read_cb);
    ui_create();
    uint32_t previous = lvsim_time_ms();
    while (lvsim_poll(&input)) {
        uint32_t now = lvsim_time_ms();
        lv_tick_inc(tick_override ? (uint32_t)strtoul(tick_override, NULL, 10) : now - previous);
        previous = now;
        lv_timer_handler();
        lvsim_wait(5);
    }
    lvsim_close();
    return 0;
}
'''


MAKEFILE_TEMPLATE = r'''CC ?= gcc
AR ?= ar
LVGL_DIR ?= @LVGL_DIR@
CONF_DIR ?= @CONF_DIR@
LVSIM_DIR ?= @LVSIM_DIR@
CACHE_DIR ?= @CACHE_DIR@
SDL2_DIR ?= @SDL2_DIR@
CFLAGS ?= -O2
CFLAGS += -std=c11 -Wall -Wextra -Werror -DLV_CPYTHON_BUILD -DLV_CONF_INCLUDE_SIMPLE -I"$(CONF_DIR)" -I"$(LVGL_DIR)" -I"$(LVSIM_DIR)"

ifeq ($(OS),Windows_NT)
APP := app.exe
CFLAGS += -DSDL_MAIN_HANDLED -I"$(SDL2_DIR)/include" -I"$(SDL2_DIR)/include/SDL2"
LDLIBS += -L"$(SDL2_DIR)/lib" -lSDL2 -lws2_32 -lwinmm -lm
APP_SOURCES := ui.c ui_events.c main.c $(LVSIM_DIR)/lvsim_io.c $(LVSIM_DIR)/lvsim_net_win32.c $(LVSIM_DIR)/lvsim_time_win32.c
else
APP := app
CFLAGS += $(shell pkg-config --cflags sdl2)
LDLIBS += $(shell pkg-config --libs sdl2) -lm
LVGL_SOURCES := $(shell find "$(LVGL_DIR)/src" -name '*.c' -not -path '*/drivers/*' -not -name 'lv_gltf_view_shader.c')
LVGL_OBJECTS := $(patsubst $(LVGL_DIR)/src/%.c,$(CACHE_DIR)/%.o,$(LVGL_SOURCES))
APP_SOURCES := ui.c ui_events.c main.c $(LVSIM_DIR)/lvsim_io.c $(LVSIM_DIR)/lvsim_net_posix.c $(LVSIM_DIR)/lvsim_time_posix.c
endif

.PHONY: all clean
all: $(APP)

$(APP): $(APP_SOURCES) ui.h ui_events.h $(CACHE_DIR)/liblvgl.a
	$(CC) $(CFLAGS) -o $@ $(APP_SOURCES) $(CACHE_DIR)/liblvgl.a $(LDLIBS)

ifeq ($(OS),Windows_NT)
$(CACHE_DIR)/liblvgl.a:
	@printf 'Libreria LVGL Windows mancante: %s\n' "$@" >&2
	@exit 1
else
$(CACHE_DIR)/liblvgl.a: $(LVGL_OBJECTS)
	$(AR) rcs $@ $^

$(CACHE_DIR)/%.o: $(LVGL_DIR)/src/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@
endif

clean:
	rm -f app app.exe
'''
