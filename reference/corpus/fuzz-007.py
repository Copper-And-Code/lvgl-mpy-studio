"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 7
Generated: 2023-11-14T22:13:59.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_7_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # span: span_7_0
    span_7_0 = lv.spangroup(parent)
    objects["span_7_0"] = span_7_0
    span_7_0.set_pos(98, 205)
    span_7_0.set_size(144, 37)
    span_7_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_7_0_span_1 = span_7_0.add_span()
    span_7_0_span_1.set_text("Normal text")
    span_7_0_span_1_style = span_7_0_span_1.get_style()
    span_7_0_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_7_0_span_1_style.set_text_font(lv.font_montserrat_14)
    span_7_0_span_2 = span_7_0.add_span()
    span_7_0_span_2.set_text("Bold text")
    span_7_0_span_2_style = span_7_0_span_2.get_style()
    span_7_0_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_7_0_span_2_style.set_text_font(lv.font_montserrat_16)
    span_7_0_span_3 = span_7_0.add_span()
    span_7_0_span_3.set_text("Small text")
    span_7_0_span_3_style = span_7_0_span_3.get_style()
    span_7_0_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_7_0_span_3_style.set_text_font(lv.font_montserrat_14)
    span_7_0.refresh()

    # label: label_7_1
    label_7_1 = lv.label(parent)
    objects["label_7_1"] = label_7_1
    label_7_1.set_pos(258, 135)
    label_7_1.set_size(168, 19)
    label_7_1.set_text("Testo 7:1 \" \\ Città")
    label_7_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_7_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_7_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # table: table_7_2
    table_7_2 = lv.table(parent)
    objects["table_7_2"] = table_7_2
    table_7_2.set_pos(271, 63)
    table_7_2.set_size(42, 107)
    table_7_2.set_column_count(3)
    table_7_2.set_column_width(0, 100)
    table_7_2.set_column_width(1, 100)
    table_7_2.set_column_width(2, 100)
    table_7_2.set_cell_value(0, 0, "Col 1")
    table_7_2.set_cell_value(0, 1, "Col 2")
    table_7_2.set_cell_value(0, 2, "Col 3")
    table_7_2.set_cell_value(1, 0, "A1")
    table_7_2.set_cell_value(1, 1, "B1")
    table_7_2.set_cell_value(1, 2, "C1")
    table_7_2.set_cell_value(2, 0, "A2")
    table_7_2.set_cell_value(2, 1, "B2")
    table_7_2.set_cell_value(2, 2, "C2")
    table_7_2.set_cell_value(3, 0, "A3")
    table_7_2.set_cell_value(3, 1, "B3")
    table_7_2.set_cell_value(3, 2, "C3")
    table_7_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_7_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_7_2.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_7_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # slider: slider_7_3
    slider_7_3 = lv.slider(parent)
    objects["slider_7_3"] = slider_7_3
    slider_7_3.set_pos(163, 258)
    slider_7_3.set_size(159, 58)
    slider_7_3.set_range(0, 100)
    slider_7_3.set_value(50, False)
    slider_7_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_7_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_7_3.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)


def random_7_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_7_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_7_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_7_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_7_get_current_page():
    return current_screen

def random_7_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_7_load_page(0)
