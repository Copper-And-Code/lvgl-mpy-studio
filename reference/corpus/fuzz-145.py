"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 145
Generated: 2023-11-14T22:16:17.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_145_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # switch: switch_145_0
    switch_145_0 = lv.switch(parent)
    objects["switch_145_0"] = switch_145_0
    switch_145_0.set_pos(655, 139)
    switch_145_0.set_size(191, 106)
    switch_145_0.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_145_0.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_145_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # scale: scale_145_1
    scale_145_1 = lv.scale(parent)
    objects["scale_145_1"] = scale_145_1
    scale_145_1.set_pos(44, 18)
    scale_145_1.set_size(259, 44)
    scale_145_1.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_145_1.set_range(0, 100)
    scale_145_1.set_total_tick_count(51)
    scale_145_1.set_major_tick_every(5)
    scale_145_1.set_style_length(15, lv.PART.INDICATOR)
    scale_145_1.set_style_length(8, lv.PART.ITEMS)
    scale_145_1.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_145_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # tileview: tileview_145_2
    tileview_145_2 = lv.tileview(parent)
    objects["tileview_145_2"] = tileview_145_2
    tileview_145_2.set_pos(78, 315)
    tileview_145_2.set_size(37, 124)
    tileview_145_2.add_tile(0, 0, lv.DIR.ALL)
    tileview_145_2.add_tile(1, 0, lv.DIR.ALL)
    tileview_145_2.add_tile(0, 1, lv.DIR.ALL)
    tileview_145_2.add_tile(1, 1, lv.DIR.ALL)
    tileview_145_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_145_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_145_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_145_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_145_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_145_get_current_page():
    return current_screen

def random_145_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_145_load_page(0)
