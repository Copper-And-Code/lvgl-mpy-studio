"""
Auto-generated LVGL UI Code for MicroPython
Project: One spinner
Generated: 2023-11-14T22:13:33.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_spinner_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinner: Spinner_w13
    spinner_w13 = lv.arc(parent)
    objects["spinner_w13"] = spinner_w13
    spinner_w13.set_pos(59, 56)
    spinner_w13.set_size(50, 50)
    spinner_w13.set_bg_angles(0, 360)
    spinner_w13.set_angles(0, 60)
    spinner_w13.remove_style(None, lv.PART.KNOB)
    spinner_w13.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_w13_anim = lv.anim_t()
    spinner_w13_anim.init()
    spinner_w13_anim.set_var(spinner_w13)
    spinner_w13_anim.set_values(0, 360)
    spinner_w13_anim.set_duration(1000)
    spinner_w13_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_w13_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_w13_anim.set_custom_exec_cb(lambda _anim, value: spinner_w13.set_rotation(value))
    spinner_w13_anim.start()
    spinner_w13.set_style_arc_width(8, lv.PART.MAIN)
    spinner_w13.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_w13.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def one_spinner_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_spinner_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_spinner_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_spinner_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_spinner_get_current_page():
    return current_screen

def one_spinner_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_spinner_load_page(0)
