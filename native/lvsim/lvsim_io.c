/* SPDX-License-Identifier: MIT */
/* Copyright (c) 2026 Nunzio Raciti */
#include "lvsim_io.h"
#include "lvsim_net.h"
#include "lvsim_time.h"

#include <SDL.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MSG_HELLO 1
#define MSG_RECT 2
#define MSG_PRESENT 3
#define MSG_POINTER 4
#define MSG_KEY 5
#define MSG_WHEEL 6
#define MSG_QUIT 7
#define MSG_STOP 8
#define MAX_FRAME_LIMIT 1000000

typedef enum { BACKEND_SDL, BACKEND_IDE, BACKEND_HEADLESS } backend_t;

static struct {
    backend_t backend;
    int width, height, opened, closed, frame_count, frame_limit, stop_requested, time_opened;
    lvsim_socket_t fd;
    uint16_t *frame;
    const char *dump_path;
    lvsim_input_t input;
    uint8_t rx[8192];
    size_t rx_len;
    SDL_Window *window;
    SDL_Renderer *renderer;
    SDL_Texture *texture;
} state;

static void put16(uint8_t *p, uint16_t value) {
    p[0] = (uint8_t)value;
    p[1] = (uint8_t)(value >> 8);
}

static void put32(uint8_t *p, uint32_t value) {
    p[0] = (uint8_t)value;
    p[1] = (uint8_t)(value >> 8);
    p[2] = (uint8_t)(value >> 16);
    p[3] = (uint8_t)(value >> 24);
}

static uint16_t get16(const uint8_t *p) {
    return (uint16_t)(p[0] | ((uint16_t)p[1] << 8));
}

static uint32_t get32(const uint8_t *p) {
    return (uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}

static int send_all(const void *data, size_t size) {
    if (lvsim_net_send(state.fd, data, size) < 0) {
        state.closed = 1;
        return -1;
    }
    return 0;
}

static void send_header(uint8_t type, uint32_t length) {
    uint8_t header[5] = {type, 0, 0, 0, 0};
    put32(header + 1, length);
    send_all(header, sizeof(header));
}

static int parse_endpoint(const char *endpoint, uint16_t *port) {
    if (!endpoint || strncmp(endpoint, "127.0.0.1:", 10) != 0) return 0;
    char *end;
    unsigned long value = strtoul(endpoint + 10, &end, 10);
    if (!value || value > 65535 || *end) return 0;
    *port = (uint16_t)value;
    return 1;
}

static int hex_digit(char value) {
    if (value >= '0' && value <= '9') return value - '0';
    if (value >= 'a' && value <= 'f') return value - 'a' + 10;
    if (value >= 'A' && value <= 'F') return value - 'A' + 10;
    return -1;
}

static void consume_message(uint8_t type, const uint8_t *payload, uint32_t length) {
    if (type == MSG_QUIT) {
        state.closed = 1;
    } else if (type == MSG_STOP) {
        state.stop_requested = 1;
    } else if (type == MSG_POINTER && length >= 5) {
        state.input.x = (int16_t)get16(payload);
        state.input.y = (int16_t)get16(payload + 2);
        state.input.pressed = payload[4] != 0;
    } else if (type == MSG_KEY && length >= 5) {
        state.input.key = get32(payload);
        state.input.key_pressed = payload[4] != 0;
    }
}

static void poll_socket(void) {
    for (;;) {
        int count = lvsim_net_recv(state.fd, state.rx + state.rx_len, sizeof(state.rx) - state.rx_len);
        if (count > 0) {
            state.rx_len += (size_t)count;
            size_t offset = 0;
            while (state.rx_len - offset >= 5) {
                uint32_t length = get32(state.rx + offset + 1);
                if (length > sizeof(state.rx) - 5) {
                    state.closed = 1;
                    return;
                }
                if (state.rx_len - offset < 5 + length) break;
                consume_message(state.rx[offset], state.rx + offset + 5, length);
                offset += 5 + length;
            }
            memmove(state.rx, state.rx + offset, state.rx_len - offset);
            state.rx_len -= offset;
            if (state.rx_len == sizeof(state.rx)) {
                state.closed = 1;
                return;
            }
            continue;
        }
        if (count == 0 || count == LVSIM_NET_ERROR) state.closed = 1;
        return;
    }
}

static void map_pointer(int *x, int *y) {
    int window_w, window_h;
    SDL_GetWindowSize(state.window, &window_w, &window_h);
    if (window_w > 0 && window_h > 0) {
        *x = *x * state.width / window_w;
        *y = *y * state.height / window_h;
    }
}

static void poll_sdl(void) {
    SDL_Event event;
    while (SDL_PollEvent(&event)) {
        if (event.type == SDL_QUIT) state.closed = 1;
        if (event.type == SDL_MOUSEMOTION || event.type == SDL_MOUSEBUTTONDOWN || event.type == SDL_MOUSEBUTTONUP) {
            int x, y;
            SDL_GetMouseState(&x, &y);
            map_pointer(&x, &y);
            state.input.x = (int16_t)x;
            state.input.y = (int16_t)y;
            if (event.type == SDL_MOUSEBUTTONDOWN) state.input.pressed = 1;
            if (event.type == SDL_MOUSEBUTTONUP) state.input.pressed = 0;
        }
        if (event.type == SDL_KEYDOWN || event.type == SDL_KEYUP) {
            state.input.key = (uint32_t)event.key.keysym.sym;
            state.input.key_pressed = event.type == SDL_KEYDOWN;
        }
    }
}

int lvsim_open(int width, int height, int color_format, const char *title) {
    memset(&state, 0, sizeof(state));
    state.fd = LVSIM_INVALID_SOCKET;
    state.width = width;
    state.height = height;
    state.frame_limit = 0;
    const char *frames = getenv("LVSIM_FRAMES");
    if (frames) state.frame_limit = atoi(frames);
    if (state.frame_limit < 0 || state.frame_limit > MAX_FRAME_LIMIT) return -1;
    if (width <= 0 || height <= 0 || color_format != 16) return -1;

    const char *endpoint = getenv("LVSIM_CONNECT");
    const char *headless = getenv("LVSIM_HEADLESS");
    if (endpoint && *endpoint) {
        uint16_t port;
        const char *token = getenv("LVSIM_TOKEN");
        if (!parse_endpoint(endpoint, &port) || !token || strlen(token) != 32) return -1;
        state.backend = BACKEND_IDE;
        state.fd = lvsim_net_connect("127.0.0.1", port);
        if (state.fd == LVSIM_INVALID_SOCKET) return -1;
        uint8_t payload[22];
        put16(payload, (uint16_t)width);
        put16(payload + 2, (uint16_t)height);
        payload[4] = 1;
        payload[5] = 2;
        for (int index = 0; index < 16; index++) {
            int high = hex_digit(token[index * 2]);
            int low = hex_digit(token[index * 2 + 1]);
            if (high < 0 || low < 0) {
                lvsim_net_close(state.fd);
                state.fd = LVSIM_INVALID_SOCKET;
                return -1;
            }
            payload[6 + index] = (uint8_t)((high << 4) | low);
        }
        send_header(MSG_HELLO, sizeof(payload));
        if (send_all(payload, sizeof(payload)) < 0) return -1;
    } else if (headless && strcmp(headless, "1") == 0) {
        state.backend = BACKEND_HEADLESS;
        state.frame = calloc((size_t)width * height, sizeof(uint16_t));
        if (!state.frame) return -1;
        state.dump_path = getenv("LVSIM_DUMP");
    } else {
        state.backend = BACKEND_SDL;
        if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS) != 0) return -1;
        int scale = getenv("LVSIM_SCALE") ? atoi(getenv("LVSIM_SCALE")) : 1;
        if (scale < 1) scale = 1;
        state.window = SDL_CreateWindow(title ? title : "LVGL", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width * scale, height * scale, 0);
        if (!state.window) return -1;
        #ifdef __EMSCRIPTEN__
        // In the browser the wait between frames already sets the pace: there is no vertical sync here.
        state.renderer = SDL_CreateRenderer(state.window, -1, SDL_RENDERER_ACCELERATED);
        #else
        state.renderer = SDL_CreateRenderer(state.window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
        #endif
        if (!state.renderer) state.renderer = SDL_CreateRenderer(state.window, -1, SDL_RENDERER_SOFTWARE);
        if (!state.renderer) return -1;
        SDL_RenderSetLogicalSize(state.renderer, width, height);
        state.texture = SDL_CreateTexture(state.renderer, SDL_PIXELFORMAT_RGB565, SDL_TEXTUREACCESS_STREAMING, width, height);
        if (!state.texture) return -1;
    }
    state.opened = 1;
    lvsim_time_open();
    state.time_opened = 1;
    return 0;
}

void lvsim_blit(int x, int y, int w, int h, const void *pixels, int stride_bytes) {
    if (!state.opened || state.closed || !pixels || w <= 0 || h <= 0) return;
    const uint8_t *bytes = pixels;
    if (state.backend == BACKEND_IDE) {
        uint8_t rect[8];
        put16(rect, (uint16_t)(int16_t)x);
        put16(rect + 2, (uint16_t)(int16_t)y);
        put16(rect + 4, (uint16_t)(int16_t)w);
        put16(rect + 6, (uint16_t)(int16_t)h);
        send_header(MSG_RECT, 8 + (uint32_t)(w * h * 2));
        send_all(rect, sizeof(rect));
        for (int row = 0; row < h && !state.closed; row++) send_all(bytes + row * stride_bytes, (size_t)w * 2);
    } else if (state.backend == BACKEND_SDL) {
        SDL_Rect rect = {x, y, w, h};
        SDL_UpdateTexture(state.texture, &rect, bytes, stride_bytes);
    } else {
        for (int row = 0; row < h; row++) {
            int dy = y + row;
            if (dy < 0 || dy >= state.height) continue;
            int sx = x < 0 ? -x : 0;
            int dx = x < 0 ? 0 : x;
            int count = w - sx;
            if (dx + count > state.width) count = state.width - dx;
            if (count > 0) memcpy(state.frame + dy * state.width + dx, bytes + row * stride_bytes + sx * 2, (size_t)count * 2);
        }
    }
}

void lvsim_present(void) {
    if (!state.opened || state.closed) return;
    state.frame_count++;
    if (state.backend == BACKEND_IDE) {
        send_header(MSG_PRESENT, 0);
    } else if (state.backend == BACKEND_SDL) {
        SDL_RenderClear(state.renderer);
        SDL_RenderCopy(state.renderer, state.texture, NULL, NULL);
        SDL_RenderPresent(state.renderer);
    } else if (state.dump_path && *state.dump_path) {
        FILE *file = fopen(state.dump_path, "wb");
        if (file) {
            fwrite(state.frame, sizeof(uint16_t), (size_t)state.width * state.height, file);
            fclose(file);
        }
    }
}

int lvsim_poll(lvsim_input_t *in) {
    if (!state.opened || state.closed) return 0;
    if (state.frame_limit && state.frame_count >= state.frame_limit) return 0;
    if (state.backend == BACKEND_IDE) poll_socket();
    if (state.backend == BACKEND_SDL) poll_sdl();
    if (in) *in = state.input;
    return !state.closed;
}

int lvsim_wait(int timeout_ms) {
    if (!state.opened || state.closed) return 0;
    if (state.frame_limit && state.frame_count >= state.frame_limit) return 0;
    if (state.backend == BACKEND_IDE) {
        int ready = lvsim_net_wait(state.fd, timeout_ms);
        if (ready < 0) state.closed = 1;
        if (ready > 0) poll_socket();
    } else {
        if (state.backend == BACKEND_SDL) poll_sdl();
        lvsim_sleep_ms((uint32_t)timeout_ms);
    }
    return !state.closed;
}

int lvsim_stop_requested(void) {
    int requested = state.stop_requested;
    state.stop_requested = 0;
    return requested;
}

void lvsim_close(void) {
    if (state.texture) SDL_DestroyTexture(state.texture);
    if (state.renderer) SDL_DestroyRenderer(state.renderer);
    if (state.window) SDL_DestroyWindow(state.window);
    if (state.backend == BACKEND_SDL && state.opened) SDL_QuitSubSystem(SDL_INIT_VIDEO | SDL_INIT_EVENTS);
    if (state.fd != LVSIM_INVALID_SOCKET) lvsim_net_close(state.fd);
    if (state.time_opened) lvsim_time_close();
    free(state.frame);
    memset(&state, 0, sizeof(state));
    state.fd = LVSIM_INVALID_SOCKET;
}
