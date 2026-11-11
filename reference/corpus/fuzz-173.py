"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 173
Generated: 2023-11-14T22:16:45.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_173_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # scale: scale_173_0
    scale_173_0 = lv.scale(parent)
    objects["scale_173_0"] = scale_173_0
    scale_173_0.set_pos(693, 183)
    scale_173_0.set_size(72, 48)
    scale_173_0.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_173_0.set_range(0, 100)
    scale_173_0.set_total_tick_count(51)
    scale_173_0.set_major_tick_every(5)
    scale_173_0.set_style_length(15, lv.PART.INDICATOR)
    scale_173_0.set_style_length(8, lv.PART.ITEMS)
    scale_173_0.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_173_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # arc: arc_173_1
    arc_173_1 = lv.arc(parent)
    objects["arc_173_1"] = arc_173_1
    arc_173_1.set_pos(379, 327)
    arc_173_1.set_size(262, 17)
    arc_173_1.set_bg_angles(135, 45)
    arc_173_1.set_range(0, 100)
    arc_173_1.set_value(50)
    arc_173_1.set_style_arc_width(10, lv.PART.MAIN)
    arc_173_1.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_173_1.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_173_1.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_173_1.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)


def random_173_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_173_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_173_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_173_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_173_get_current_page():
    return current_screen

def random_173_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_173_load_page(0)
