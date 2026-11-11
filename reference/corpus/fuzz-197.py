"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 197
Generated: 2023-11-14T22:17:09.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_197_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tileview: tileview_197_0
    tileview_197_0 = lv.tileview(parent)
    objects["tileview_197_0"] = tileview_197_0
    tileview_197_0.set_pos(6, 109)
    tileview_197_0.set_size(105, 124)
    tileview_197_0.add_tile(0, 0, lv.DIR.ALL)
    tileview_197_0.add_tile(1, 0, lv.DIR.ALL)
    tileview_197_0.add_tile(0, 1, lv.DIR.ALL)
    tileview_197_0.add_tile(1, 1, lv.DIR.ALL)
    tileview_197_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # bar: bar_197_1
    bar_197_1 = lv.bar(parent)
    objects["bar_197_1"] = bar_197_1
    bar_197_1.set_pos(114, 156)
    bar_197_1.set_size(238, 103)
    bar_197_1.set_range(0, 100)
    bar_197_1.set_value(50, False)
    bar_197_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_197_1.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)


def random_197_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_197_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_197_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_197_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_197_get_current_page():
    return current_screen

def random_197_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_197_load_page(0)
