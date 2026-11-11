"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 129
Generated: 2023-11-14T22:16:01.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_129_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # arc: arc_129_0
    arc_129_0 = lv.arc(parent)
    objects["arc_129_0"] = arc_129_0
    arc_129_0.set_pos(93, 255)
    arc_129_0.set_size(96, 151)
    arc_129_0.set_bg_angles(135, 45)
    arc_129_0.set_range(0, 100)
    arc_129_0.set_value(50)
    arc_129_0.set_style_arc_width(10, lv.PART.MAIN)
    arc_129_0.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_129_0.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_129_0.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_129_0.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # switch: switch_129_1
    switch_129_1 = lv.switch(parent)
    objects["switch_129_1"] = switch_129_1
    switch_129_1.set_pos(481, 312)
    switch_129_1.set_size(231, 75)
    switch_129_1.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_129_1.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_129_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # switch: switch_129_2
    switch_129_2 = lv.switch(parent)
    objects["switch_129_2"] = switch_129_2
    switch_129_2.set_pos(166, 103)
    switch_129_2.set_size(136, 102)
    switch_129_2.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_129_2.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_129_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # spinbox: spinbox_129_3
    spinbox_129_3 = lv.spinbox(parent)
    objects["spinbox_129_3"] = spinbox_129_3
    spinbox_129_3.set_pos(308, 294)
    spinbox_129_3.set_size(261, 134)
    spinbox_129_3.set_digit_format(4, 0)
    spinbox_129_3.set_range(0, 999)
    spinbox_129_3.set_value(0)
    spinbox_129_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_129_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_129_3.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # label: label_129_4
    label_129_4 = lv.label(parent)
    objects["label_129_4"] = label_129_4
    label_129_4.set_pos(86, 49)
    label_129_4.set_size(35, 123)
    label_129_4.set_text("Testo 129:4 \" \\ Città")
    label_129_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_129_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_129_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)


def random_129_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_129_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_129_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_129_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_129_get_current_page():
    return current_screen

def random_129_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_129_load_page(0)
