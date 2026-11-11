"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 137
Generated: 2023-11-14T22:16:09.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_137_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # span: span_137_0
    span_137_0 = lv.spangroup(parent)
    objects["span_137_0"] = span_137_0
    span_137_0.set_pos(202, 49)
    span_137_0.set_size(192, 82)
    span_137_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_137_0_span_1 = span_137_0.add_span()
    span_137_0_span_1.set_text("Normal text")
    span_137_0_span_1_style = span_137_0_span_1.get_style()
    span_137_0_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_137_0_span_1_style.set_text_font(lv.font_montserrat_14)
    span_137_0_span_2 = span_137_0.add_span()
    span_137_0_span_2.set_text("Bold text")
    span_137_0_span_2_style = span_137_0_span_2.get_style()
    span_137_0_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_137_0_span_2_style.set_text_font(lv.font_montserrat_16)
    span_137_0_span_3 = span_137_0.add_span()
    span_137_0_span_3.set_text("Small text")
    span_137_0_span_3_style = span_137_0_span_3.get_style()
    span_137_0_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_137_0_span_3_style.set_text_font(lv.font_montserrat_14)
    span_137_0.refresh()

    # bar: bar_137_1
    bar_137_1 = lv.bar(parent)
    objects["bar_137_1"] = bar_137_1
    bar_137_1.set_pos(591, 284)
    bar_137_1.set_size(175, 129)
    bar_137_1.set_range(0, 100)
    bar_137_1.set_value(50, False)
    bar_137_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_137_1.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)


def random_137_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_137_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_137_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_137_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_137_get_current_page():
    return current_screen

def random_137_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_137_load_page(0)
