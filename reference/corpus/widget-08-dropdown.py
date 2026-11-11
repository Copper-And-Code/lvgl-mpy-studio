"""
Auto-generated LVGL UI Code for MicroPython
Project: One dropdown
Generated: 2023-11-14T22:13:27.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_dropdown_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # dropdown: Dropdown_w7
    dropdown_w7 = lv.dropdown(parent)
    objects["dropdown_w7"] = dropdown_w7
    dropdown_w7.set_pos(41, 44)
    dropdown_w7.set_size(150, 40)
    dropdown_w7.set_options("Option 1\nOption 2\nOption 3")
    dropdown_w7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_w7.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_w7.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def one_dropdown_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_dropdown_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_dropdown_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_dropdown_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_dropdown_get_current_page():
    return current_screen

def one_dropdown_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_dropdown_load_page(0)
