"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 183
Generated: 2023-11-14T22:16:55.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_183_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # switch: switch_183_0
    switch_183_0 = lv.switch(parent)
    objects["switch_183_0"] = switch_183_0
    switch_183_0.set_pos(214, 49)
    switch_183_0.set_size(181, 79)
    switch_183_0.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_183_0.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_183_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # slider: slider_183_1
    slider_183_1 = lv.slider(parent)
    objects["slider_183_1"] = slider_183_1
    slider_183_1.set_pos(86, 391)
    slider_183_1.set_size(62, 77)
    slider_183_1.set_range(0, 100)
    slider_183_1.set_value(50, False)
    slider_183_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_183_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_183_1.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)


def random_183_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_183_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_183_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_183_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_183_get_current_page():
    return current_screen

def random_183_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_183_load_page(0)
