"""
Auto-generated LVGL UI Code for MicroPython
Project: One scale
Generated: 2023-11-14T22:13:37.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_scale_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # scale: Scale_w17
    scale_w17 = lv.scale(parent)
    objects["scale_w17"] = scale_w17
    scale_w17.set_pos(71, 64)
    scale_w17.set_size(200, 60)
    scale_w17.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_w17.set_range(0, 100)
    scale_w17.set_total_tick_count(51)
    scale_w17.set_major_tick_every(5)
    scale_w17.set_style_length(15, lv.PART.INDICATOR)
    scale_w17.set_style_length(8, lv.PART.ITEMS)
    scale_w17.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_w17.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)


def one_scale_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_scale_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_scale_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_scale_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_scale_get_current_page():
    return current_screen

def one_scale_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_scale_load_page(0)
