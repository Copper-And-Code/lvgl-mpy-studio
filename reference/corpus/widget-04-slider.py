"""
Auto-generated LVGL UI Code for MicroPython
Project: One slider
Generated: 2023-11-14T22:13:23.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_slider_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # slider: Slider_w3
    slider_w3 = lv.slider(parent)
    objects["slider_w3"] = slider_w3
    slider_w3.set_pos(29, 36)
    slider_w3.set_size(200, 20)
    slider_w3.set_range(0, 100)
    slider_w3.set_value(50, False)
    slider_w3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_w3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_w3.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)


def one_slider_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_slider_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_slider_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_slider_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_slider_get_current_page():
    return current_screen

def one_slider_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_slider_load_page(0)
