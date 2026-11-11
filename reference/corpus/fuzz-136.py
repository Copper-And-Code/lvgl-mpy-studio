"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 136
Generated: 2023-11-14T22:16:08.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_136_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinner: spinner_136_0
    spinner_136_0 = lv.arc(parent)
    objects["spinner_136_0"] = spinner_136_0
    spinner_136_0.set_pos(305, 194)
    spinner_136_0.set_size(124, 102)
    spinner_136_0.set_bg_angles(0, 360)
    spinner_136_0.set_angles(0, 60)
    spinner_136_0.remove_style(None, lv.PART.KNOB)
    spinner_136_0.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_136_0_anim = lv.anim_t()
    spinner_136_0_anim.init()
    spinner_136_0_anim.set_var(spinner_136_0)
    spinner_136_0_anim.set_values(0, 360)
    spinner_136_0_anim.set_duration(1000)
    spinner_136_0_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_136_0_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_136_0_anim.set_custom_exec_cb(lambda _anim, value: spinner_136_0.set_rotation(value))
    spinner_136_0_anim.start()
    spinner_136_0.set_style_arc_width(8, lv.PART.MAIN)
    spinner_136_0.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_136_0.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_136_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_136_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_136_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_136_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_136_get_current_page():
    return current_screen

def random_136_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_136_load_page(0)
