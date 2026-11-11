"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 132
Generated: 2023-11-14T22:16:04.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_132_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # bar: bar_132_0
    bar_132_0 = lv.bar(parent)
    objects["bar_132_0"] = bar_132_0
    bar_132_0.set_pos(527, 355)
    bar_132_0.set_size(98, 78)
    bar_132_0.set_range(0, 100)
    bar_132_0.set_value(50, False)
    bar_132_0.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_132_0.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # panel: panel_132_1
    panel_132_1 = lv.obj(parent)
    objects["panel_132_1"] = panel_132_1
    panel_132_1.set_pos(634, 246)
    panel_132_1.set_size(87, 11)
    panel_132_1.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_132_1.set_style_border_width(2, lv.PART.MAIN)
    panel_132_1.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_132_1.set_style_radius(5, lv.PART.MAIN)
    panel_132_1.set_style_pad_all(0, lv.PART.MAIN)
    panel_132_1.set_style_pad_gap(0, lv.PART.MAIN)


def random_132_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_132_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_132_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_132_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_132_get_current_page():
    return current_screen

def random_132_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_132_load_page(0)
