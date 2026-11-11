"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 66
Generated: 2023-11-14T22:14:58.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_66_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # label: label_66_0
    label_66_0 = lv.label(parent)
    objects["label_66_0"] = label_66_0
    label_66_0.set_pos(560, 372)
    label_66_0.set_size(221, 46)
    label_66_0.set_text("Testo 66:0 \" \\ Città")
    label_66_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_66_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_66_0.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # arc: arc_66_1
    arc_66_1 = lv.arc(parent)
    objects["arc_66_1"] = arc_66_1
    arc_66_1.set_pos(271, 329)
    arc_66_1.set_size(249, 87)
    arc_66_1.set_bg_angles(135, 45)
    arc_66_1.set_range(0, 100)
    arc_66_1.set_value(50)
    arc_66_1.set_style_arc_width(10, lv.PART.MAIN)
    arc_66_1.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_66_1.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_66_1.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_66_1.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # dropdown: dropdown_66_2
    dropdown_66_2 = lv.dropdown(parent)
    objects["dropdown_66_2"] = dropdown_66_2
    dropdown_66_2.set_pos(453, 136)
    dropdown_66_2.set_size(89, 56)
    dropdown_66_2.set_options("Option 1\nOption 2\nOption 3")
    dropdown_66_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_66_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_66_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # roller: roller_66_3
    roller_66_3 = lv.roller(parent)
    objects["roller_66_3"] = roller_66_3
    roller_66_3.set_pos(690, 319)
    roller_66_3.set_size(207, 62)
    roller_66_3.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_66_3.set_visible_row_count(3)
    roller_66_3.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_66_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_66_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_66_3.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_66_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_66_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_66_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_66_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_66_get_current_page():
    return current_screen

def random_66_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_66_load_page(0)
