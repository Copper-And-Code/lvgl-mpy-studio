"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 107
Generated: 2023-11-14T22:15:39.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_107_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # arc: arc_107_0
    arc_107_0 = lv.arc(parent)
    objects["arc_107_0"] = arc_107_0
    arc_107_0.set_pos(104, 331)
    arc_107_0.set_size(267, 65)
    arc_107_0.set_bg_angles(135, 45)
    arc_107_0.set_range(0, 100)
    arc_107_0.set_value(50)
    arc_107_0.set_style_arc_width(10, lv.PART.MAIN)
    arc_107_0.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_107_0.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_107_0.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_107_0.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # slider: slider_107_1
    slider_107_1 = lv.slider(parent)
    objects["slider_107_1"] = slider_107_1
    slider_107_1.set_pos(400, 318)
    slider_107_1.set_size(101, 136)
    slider_107_1.set_range(0, 100)
    slider_107_1.set_value(50, False)
    slider_107_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_107_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_107_1.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)


def random_107_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_107_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_107_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_107_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_107_get_current_page():
    return current_screen

def random_107_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_107_load_page(0)
