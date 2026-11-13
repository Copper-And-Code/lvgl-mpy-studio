/* SPDX-License-Identifier: MIT */
/* Copyright (c) 2026 Nunzio Raciti */
#include "lvsim_io.h"
#include "lvsim_time.h"
#include "py/runtime.h"
#include <string.h>

static mp_obj_t lvsim_open_py(mp_obj_t width_obj, mp_obj_t height_obj, mp_obj_t title_obj) {
    int width = mp_obj_get_int(width_obj);
    int height = mp_obj_get_int(height_obj);
    const char *title = mp_obj_str_get_str(title_obj);
    if (lvsim_open(width, height, 16, title) != 0) {
        mp_raise_msg(&mp_type_RuntimeError, MP_ERROR_TEXT("lvsim.open failed"));
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(lvsim_open_py_obj, lvsim_open_py);

static mp_obj_t lvsim_blit_py(size_t argc, const mp_obj_t *args) {
    int x = mp_obj_get_int(args[0]);
    int y = mp_obj_get_int(args[1]);
    int w = mp_obj_get_int(args[2]);
    int h = mp_obj_get_int(args[3]);
    int stride = mp_obj_get_int(args[5]);
    mp_buffer_info_t buffer;
    mp_get_buffer_raise(args[4], &buffer, MP_BUFFER_READ);
    if (w <= 0 || h <= 0 || stride < w * 2 || buffer.len < (size_t)((h - 1) * stride + w * 2)) {
        mp_raise_ValueError(MP_ERROR_TEXT("invalid framebuffer slice"));
    }
    lvsim_blit(x, y, w, h, buffer.buf, stride);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(lvsim_blit_py_obj, 6, 6, lvsim_blit_py);

static mp_obj_t lvsim_present_py(void) {
    lvsim_present();
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_0(lvsim_present_py_obj, lvsim_present_py);

static void schedule_stop(void) {
    if (lvsim_stop_requested()) mp_sched_keyboard_interrupt();
}

static mp_obj_t lvsim_poll_py(void) {
    lvsim_input_t input;
    int running = lvsim_poll(&input);
    schedule_stop();
    if (!running) return mp_const_none;
    mp_obj_t values[5] = {
        mp_obj_new_int(input.x), mp_obj_new_int(input.y), mp_obj_new_int(input.pressed),
        mp_obj_new_int_from_uint(input.key), mp_obj_new_int(input.key_pressed),
    };
    return mp_obj_new_tuple(5, values);
}
static MP_DEFINE_CONST_FUN_OBJ_0(lvsim_poll_py_obj, lvsim_poll_py);

static mp_obj_t lvsim_wait_py(mp_obj_t milliseconds_obj) {
    int running = lvsim_wait(mp_obj_get_int(milliseconds_obj));
    schedule_stop();
    return mp_obj_new_bool(running);
}
static MP_DEFINE_CONST_FUN_OBJ_1(lvsim_wait_py_obj, lvsim_wait_py);

static mp_obj_t lvsim_ticks_ms_py(void) {
    return mp_obj_new_int_from_uint(lvsim_time_ms());
}
static MP_DEFINE_CONST_FUN_OBJ_0(lvsim_ticks_ms_py_obj, lvsim_ticks_ms_py);

static mp_obj_t lvsim_close_py(void) {
    lvsim_close();
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_0(lvsim_close_py_obj, lvsim_close_py);

// ---- Programs without pages: the board's timer and serial port ----
//
// On a board a hardware timer schedules the LVGL task, which runs in the main thread
// between two bytecodes, also while the program waits for a key: the wait is in the
// interrupt-driven REPL. Here a thread schedules it, and a signal makes a blocking read of
// the main thread return EINTR, so that MicroPython runs what is scheduled and reads again.
// Keys come through a pipe that this module puts in place of standard input, so that a
// Ctrl-C becomes a KeyboardInterrupt only while the program lets it, as on a board.
#if defined(__unix__) && !defined(__EMSCRIPTEN__)
#include <errno.h>
#include <pthread.h>
#include <signal.h>
#include <time.h>
#include <unistd.h>

MP_REGISTER_ROOT_POINTER(mp_obj_t lvsim_service_callback);

static pthread_t service_main;
static volatile int service_period_ms;
static volatile int service_on;
static volatile int service_pending;
static int service_started;
static int keys_started;

static void service_wake(int signum) {
    (void)signum;  // nothing to do: the signal only interrupts a blocking call
}

static mp_obj_t service_run(mp_obj_t arg) {
    service_pending = 0;
    mp_obj_t callback = MP_STATE_VM(lvsim_service_callback);
    if (callback != MP_OBJ_NULL && callback != mp_const_none) {
        mp_call_function_1(callback, arg);
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(service_run_obj, service_run);

static void *service_loop(void *unused) {
    (void)unused;
    for (;;) {
        int period = service_period_ms > 0 ? service_period_ms : 5;
        struct timespec delay = { period / 1000, (long)(period % 1000) * 1000000L };
        while (nanosleep(&delay, &delay) == -1 && errno == EINTR) {
        }
        if (!service_on || service_pending) {
            continue;  // one task at a time, as the board's driver
        }
        service_pending = 1;
        if (mp_sched_schedule(MP_OBJ_FROM_PTR(&service_run_obj), mp_const_none)) {
            pthread_kill(service_main, SIGUSR1);
        } else {
            service_pending = 0;  // the queue is full: the next period catches up
        }
    }
    return NULL;
}

static void service_signal(void) {
    struct sigaction action;
    memset(&action, 0, sizeof(action));
    action.sa_handler = service_wake;  // without SA_RESTART: a blocking read returns EINTR
    sigemptyset(&action.sa_mask);
    sigaction(SIGUSR1, &action, NULL);
}

// service(callback, period_ms): calls callback every period from the main thread; None stops.
static mp_obj_t lvsim_service_py(mp_obj_t callback, mp_obj_t period_obj) {
    if (callback == mp_const_none) {
        service_on = 0;
        MP_STATE_VM(lvsim_service_callback) = mp_const_none;
        return mp_const_none;
    }
    service_period_ms = mp_obj_get_int(period_obj);
    MP_STATE_VM(lvsim_service_callback) = callback;
    service_main = pthread_self();
    service_on = 1;
    if (!service_started) {
        service_signal();
        pthread_t thread;
        if (pthread_create(&thread, NULL, service_loop, NULL) != 0) {
            service_on = 0;
            mp_raise_OSError(errno);
        }
        pthread_detach(thread);
        service_started = 1;
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(lvsim_service_py_obj, lvsim_service_py);

static int keys_source = -1;
static int keys_sink = -1;

static int interrupt_enabled(void) {
    // micropython.kbd_intr(3) installs the SIGINT handler of the unix port, kbd_intr(-1) removes it.
    struct sigaction current;
    if (sigaction(SIGINT, NULL, &current) != 0) {
        return 0;
    }
    return current.sa_handler != SIG_DFL && current.sa_handler != SIG_IGN;
}

static int write_all(int fd, const unsigned char *data, size_t size) {
    while (size > 0) {
        ssize_t written = write(fd, data, size);
        if (written < 0) {
            if (errno == EINTR) continue;
            return -1;
        }
        data += written;
        size -= (size_t)written;
    }
    return 0;
}

static void *keys_loop(void *unused) {
    (void)unused;
    unsigned char buffer[256];
    for (;;) {
        ssize_t count = read(keys_source, buffer, sizeof(buffer));
        if (count < 0 && errno == EINTR) continue;
        if (count <= 0) break;
        size_t start = 0;
        for (size_t index = 0; index < (size_t)count; ++index) {
            if (buffer[index] == 3 && interrupt_enabled()) {
                if (write_all(keys_sink, buffer + start, index - start) != 0) goto done;
                start = index + 1;
                mp_sched_keyboard_interrupt();
                pthread_kill(service_main, SIGUSR1);
            }
        }
        if (write_all(keys_sink, buffer + start, (size_t)count - start) != 0) break;
    }
done:
    close(keys_sink);  // the program reads the end of its input
    return NULL;
}

// keys(): standard input as a board's serial port: Ctrl-C interrupts only while kbd_intr allows it.
static mp_obj_t lvsim_keys_py(void) {
    if (keys_started) {
        return mp_const_none;
    }
    int pipe_fds[2];
    if (pipe(pipe_fds) != 0) {
        mp_raise_OSError(errno);
    }
    keys_source = dup(STDIN_FILENO);
    if (keys_source < 0 || dup2(pipe_fds[0], STDIN_FILENO) < 0) {
        int error = errno;
        close(pipe_fds[0]);
        close(pipe_fds[1]);
        mp_raise_OSError(error);
    }
    close(pipe_fds[0]);
    keys_sink = pipe_fds[1];
    service_main = pthread_self();
    service_signal();
    pthread_t thread;
    if (pthread_create(&thread, NULL, keys_loop, NULL) != 0) {
        mp_raise_OSError(errno);
    }
    pthread_detach(thread);
    keys_started = 1;
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_0(lvsim_keys_py_obj, lvsim_keys_py);
#endif

static const mp_rom_map_elem_t lvsim_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_lvsim) },
    { MP_ROM_QSTR(MP_QSTR_open), MP_ROM_PTR(&lvsim_open_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_blit), MP_ROM_PTR(&lvsim_blit_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_present), MP_ROM_PTR(&lvsim_present_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_poll), MP_ROM_PTR(&lvsim_poll_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_wait), MP_ROM_PTR(&lvsim_wait_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&lvsim_ticks_ms_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_close), MP_ROM_PTR(&lvsim_close_py_obj) },
    #if defined(__unix__) && !defined(__EMSCRIPTEN__)
    { MP_ROM_QSTR(MP_QSTR_service), MP_ROM_PTR(&lvsim_service_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_keys), MP_ROM_PTR(&lvsim_keys_py_obj) },
    #endif
};
static MP_DEFINE_CONST_DICT(lvsim_globals, lvsim_globals_table);

const mp_obj_module_t lvsim_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&lvsim_globals,
};
MP_REGISTER_MODULE(MP_QSTR_lvsim, lvsim_user_cmodule);
