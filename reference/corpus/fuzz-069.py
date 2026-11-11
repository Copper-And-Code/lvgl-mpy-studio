"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 69
Generated: 2023-11-14T22:15:01.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_69_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # checkbox: checkbox_69_0
    checkbox_69_0 = lv.checkbox(parent)
    objects["checkbox_69_0"] = checkbox_69_0
    checkbox_69_0.set_pos(56, 100)
    checkbox_69_0.set_text("Testo 69:0 \" \\ Città")
    checkbox_69_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_69_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_69_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # panel: panel_69_1
    panel_69_1 = lv.obj(parent)
    objects["panel_69_1"] = panel_69_1
    panel_69_1.set_pos(528, 97)
    panel_69_1.set_size(266, 114)
    panel_69_1.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_69_1.set_style_border_width(2, lv.PART.MAIN)
    panel_69_1.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_69_1.set_style_radius(5, lv.PART.MAIN)
    panel_69_1.set_style_pad_all(0, lv.PART.MAIN)
    panel_69_1.set_style_pad_gap(0, lv.PART.MAIN)

    # bar: bar_69_2
    bar_69_2 = lv.bar(parent)
    objects["bar_69_2"] = bar_69_2
    bar_69_2.set_pos(246, 385)
    bar_69_2.set_size(138, 43)
    bar_69_2.set_range(0, 100)
    bar_69_2.set_value(50, False)
    bar_69_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_69_2.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # buttonmatrix: buttonmatrix_69_3
    buttonmatrix_69_3 = lv.buttonmatrix(parent)
    objects["buttonmatrix_69_3"] = buttonmatrix_69_3
    buttonmatrix_69_3.set_pos(15, 178)
    buttonmatrix_69_3.set_size(205, 115)
    buttonmatrix_69_3_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_69_3.set_map(buttonmatrix_69_3_map)
    buttonmatrix_69_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_69_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_69_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_69_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_69_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_69_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_69_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_69_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_69_get_current_page():
    return current_screen

def random_69_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_69_load_page(0)
