/* SPDX-License-Identifier: MIT */
/* Copyright (c) 2026 Nunzio Raciti */
#include "lvsim_io.h"
#include "lvsim_time.h"
#include "py/runtime.h"

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

static const mp_rom_map_elem_t lvsim_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_lvsim) },
    { MP_ROM_QSTR(MP_QSTR_open), MP_ROM_PTR(&lvsim_open_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_blit), MP_ROM_PTR(&lvsim_blit_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_present), MP_ROM_PTR(&lvsim_present_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_poll), MP_ROM_PTR(&lvsim_poll_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_wait), MP_ROM_PTR(&lvsim_wait_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&lvsim_ticks_ms_py_obj) },
    { MP_ROM_QSTR(MP_QSTR_close), MP_ROM_PTR(&lvsim_close_py_obj) },
};
static MP_DEFINE_CONST_DICT(lvsim_globals, lvsim_globals_table);

const mp_obj_module_t lvsim_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&lvsim_globals,
};
MP_REGISTER_MODULE(MP_QSTR_lvsim, lvsim_user_cmodule);
