"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 93
Generated: 2023-11-14T22:15:25.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_93_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # dropdown: dropdown_93_0
    dropdown_93_0 = lv.dropdown(parent)
    objects["dropdown_93_0"] = dropdown_93_0
    dropdown_93_0.set_pos(554, 162)
    dropdown_93_0.set_size(69, 48)
    dropdown_93_0.set_options("Option 1\nOption 2\nOption 3")
    dropdown_93_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_93_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_93_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # bar: bar_93_1
    bar_93_1 = lv.bar(parent)
    objects["bar_93_1"] = bar_93_1
    bar_93_1.set_pos(427, 203)
    bar_93_1.set_size(253, 66)
    bar_93_1.set_range(0, 100)
    bar_93_1.set_value(50, False)
    bar_93_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_93_1.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # roller: roller_93_2
    roller_93_2 = lv.roller(parent)
    objects["roller_93_2"] = roller_93_2
    roller_93_2.set_pos(13, 84)
    roller_93_2.set_size(24, 67)
    roller_93_2.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_93_2.set_visible_row_count(3)
    roller_93_2.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_93_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_93_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_93_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_93_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_93_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_93_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_93_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_93_get_current_page():
    return current_screen

def random_93_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_93_load_page(0)
