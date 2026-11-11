"""
Auto-generated LVGL UI Code for MicroPython
Project: One checkbox
Generated: 2023-11-14T22:13:25.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_checkbox_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # checkbox: Checkbox_w5
    checkbox_w5 = lv.checkbox(parent)
    objects["checkbox_w5"] = checkbox_w5
    checkbox_w5.set_pos(35, 40)
    checkbox_w5.set_text("Checkbox")
    checkbox_w5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_w5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_w5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)


def one_checkbox_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_checkbox_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_checkbox_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_checkbox_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_checkbox_get_current_page():
    return current_screen

def one_checkbox_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_checkbox_load_page(0)
