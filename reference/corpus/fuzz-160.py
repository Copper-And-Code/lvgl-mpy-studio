"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 160
Generated: 2023-11-14T22:16:32.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_160_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # scale: scale_160_0
    scale_160_0 = lv.scale(parent)
    objects["scale_160_0"] = scale_160_0
    scale_160_0.set_pos(295, 147)
    scale_160_0.set_size(118, 52)
    scale_160_0.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_160_0.set_range(0, 100)
    scale_160_0.set_total_tick_count(51)
    scale_160_0.set_major_tick_every(5)
    scale_160_0.set_style_length(15, lv.PART.INDICATOR)
    scale_160_0.set_style_length(8, lv.PART.ITEMS)
    scale_160_0.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_160_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # tileview: tileview_160_1
    tileview_160_1 = lv.tileview(parent)
    objects["tileview_160_1"] = tileview_160_1
    tileview_160_1.set_pos(55, 202)
    tileview_160_1.set_size(215, 113)
    tileview_160_1.add_tile(0, 0, lv.DIR.ALL)
    tileview_160_1.add_tile(1, 0, lv.DIR.ALL)
    tileview_160_1.add_tile(0, 1, lv.DIR.ALL)
    tileview_160_1.add_tile(1, 1, lv.DIR.ALL)
    tileview_160_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # spinbox: spinbox_160_2
    spinbox_160_2 = lv.spinbox(parent)
    objects["spinbox_160_2"] = spinbox_160_2
    spinbox_160_2.set_pos(562, 181)
    spinbox_160_2.set_size(169, 74)
    spinbox_160_2.set_digit_format(4, 0)
    spinbox_160_2.set_range(0, 999)
    spinbox_160_2.set_value(0)
    spinbox_160_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_160_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_160_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_160_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_160_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_160_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_160_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_160_get_current_page():
    return current_screen

def random_160_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_160_load_page(0)
