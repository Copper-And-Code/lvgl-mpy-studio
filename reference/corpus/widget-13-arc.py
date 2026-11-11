"""
Auto-generated LVGL UI Code for MicroPython
Project: One arc
Generated: 2023-11-14T22:13:32.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_arc_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # arc: Arc_w12
    arc_w12 = lv.arc(parent)
    objects["arc_w12"] = arc_w12
    arc_w12.set_pos(56, 54)
    arc_w12.set_size(100, 100)
    arc_w12.set_bg_angles(135, 45)
    arc_w12.set_range(0, 100)
    arc_w12.set_value(50)
    arc_w12.set_style_arc_width(10, lv.PART.MAIN)
    arc_w12.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_w12.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_w12.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_w12.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)


def one_arc_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_arc_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_arc_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_arc_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_arc_get_current_page():
    return current_screen

def one_arc_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_arc_load_page(0)
