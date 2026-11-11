"""
Auto-generated LVGL UI Code for MicroPython
Project: One roller
Generated: 2023-11-14T22:13:28.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_roller_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # roller: Roller_w8
    roller_w8 = lv.roller(parent)
    objects["roller_w8"] = roller_w8
    roller_w8.set_pos(44, 46)
    roller_w8.set_size(100, 150)
    roller_w8.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_w8.set_visible_row_count(3)
    roller_w8.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_w8.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_w8.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_w8.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def one_roller_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_roller_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_roller_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_roller_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_roller_get_current_page():
    return current_screen

def one_roller_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_roller_load_page(0)
