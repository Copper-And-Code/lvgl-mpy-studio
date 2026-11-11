"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 174
Generated: 2023-11-14T22:16:46.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_174_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # button: button_174_0
    button_174_0 = lv.button(parent)
    objects["button_174_0"] = button_174_0
    button_174_0.set_pos(484, 114)
    button_174_0.set_size(264, 34)
    button_174_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_174_0.set_style_radius(5, lv.PART.MAIN)
    button_174_0_label = lv.label(button_174_0)
    button_174_0_label.set_text("Testo 174:0 \" \\ Città")
    button_174_0_label.center()
    button_174_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_174_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # switch: switch_174_1
    switch_174_1 = lv.switch(parent)
    objects["switch_174_1"] = switch_174_1
    switch_174_1.set_pos(499, 247)
    switch_174_1.set_size(236, 108)
    switch_174_1.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_174_1.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_174_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)


def random_174_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_174_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_174_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_174_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_174_get_current_page():
    return current_screen

def random_174_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_174_load_page(0)
