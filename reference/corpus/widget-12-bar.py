"""
Auto-generated LVGL UI Code for MicroPython
Project: One bar
Generated: 2023-11-14T22:13:31.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_bar_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # bar: Progress Bar_w11
    progress_bar_w11 = lv.bar(parent)
    objects["progress_bar_w11"] = progress_bar_w11
    progress_bar_w11.set_pos(53, 52)
    progress_bar_w11.set_size(200, 20)
    progress_bar_w11.set_range(0, 100)
    progress_bar_w11.set_value(50, False)
    progress_bar_w11.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    progress_bar_w11.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)


def one_bar_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_bar_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_bar_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_bar_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_bar_get_current_page():
    return current_screen

def one_bar_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_bar_load_page(0)
