"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 79
Generated: 2023-11-14T22:15:11.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_79_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # line: line_79_0
    line_79_0 = lv.line(parent)
    objects["line_79_0"] = line_79_0
    line_79_0.set_pos(607, 38)
    line_79_0_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_79_0.set_points(line_79_0_points, 2)
    line_79_0.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_79_0.set_style_line_width(2, lv.PART.MAIN)

    # table: table_79_1
    table_79_1 = lv.table(parent)
    objects["table_79_1"] = table_79_1
    table_79_1.set_pos(261, 183)
    table_79_1.set_size(120, 81)
    table_79_1.set_column_count(3)
    table_79_1.set_column_width(0, 100)
    table_79_1.set_column_width(1, 100)
    table_79_1.set_column_width(2, 100)
    table_79_1.set_cell_value(0, 0, "Col 1")
    table_79_1.set_cell_value(0, 1, "Col 2")
    table_79_1.set_cell_value(0, 2, "Col 3")
    table_79_1.set_cell_value(1, 0, "A1")
    table_79_1.set_cell_value(1, 1, "B1")
    table_79_1.set_cell_value(1, 2, "C1")
    table_79_1.set_cell_value(2, 0, "A2")
    table_79_1.set_cell_value(2, 1, "B2")
    table_79_1.set_cell_value(2, 2, "C2")
    table_79_1.set_cell_value(3, 0, "A3")
    table_79_1.set_cell_value(3, 1, "B3")
    table_79_1.set_cell_value(3, 2, "C3")
    table_79_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_79_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_79_1.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_79_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # spinbox: spinbox_79_2
    spinbox_79_2 = lv.spinbox(parent)
    objects["spinbox_79_2"] = spinbox_79_2
    spinbox_79_2.set_pos(372, 96)
    spinbox_79_2.set_size(156, 63)
    spinbox_79_2.set_digit_format(4, 0)
    spinbox_79_2.set_range(0, 999)
    spinbox_79_2.set_value(0)
    spinbox_79_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_79_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_79_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # bar: bar_79_3
    bar_79_3 = lv.bar(parent)
    objects["bar_79_3"] = bar_79_3
    bar_79_3.set_pos(427, 33)
    bar_79_3.set_size(87, 47)
    bar_79_3.set_range(0, 100)
    bar_79_3.set_value(50, False)
    bar_79_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_79_3.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)


def random_79_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_79_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_79_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_79_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_79_get_current_page():
    return current_screen

def random_79_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_79_load_page(0)
