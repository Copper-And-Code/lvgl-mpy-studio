"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 195
Generated: 2023-11-14T22:17:07.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_195_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # line: line_195_0
    line_195_0 = lv.line(parent)
    objects["line_195_0"] = line_195_0
    line_195_0.set_pos(411, 279)
    line_195_0_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_195_0.set_points(line_195_0_points, 2)
    line_195_0.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_195_0.set_style_line_width(2, lv.PART.MAIN)

    # imagebutton: imagebutton_195_1
    imagebutton_195_1 = lv.imagebutton(parent)
    objects["imagebutton_195_1"] = imagebutton_195_1
    imagebutton_195_1.set_pos(19, 169)
    imagebutton_195_1.set_size(23, 136)
    imagebutton_195_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_195_1.set_style_radius(5, lv.PART.MAIN)
    imagebutton_195_1_label = lv.label(imagebutton_195_1)
    imagebutton_195_1_label.set_text("Testo 195:1 \" \\ Città")
    imagebutton_195_1_label.center()
    imagebutton_195_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_195_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # table: table_195_2
    table_195_2 = lv.table(parent)
    objects["table_195_2"] = table_195_2
    table_195_2.set_pos(237, 365)
    table_195_2.set_size(113, 108)
    table_195_2.set_column_count(3)
    table_195_2.set_column_width(0, 100)
    table_195_2.set_column_width(1, 100)
    table_195_2.set_column_width(2, 100)
    table_195_2.set_cell_value(0, 0, "Col 1")
    table_195_2.set_cell_value(0, 1, "Col 2")
    table_195_2.set_cell_value(0, 2, "Col 3")
    table_195_2.set_cell_value(1, 0, "A1")
    table_195_2.set_cell_value(1, 1, "B1")
    table_195_2.set_cell_value(1, 2, "C1")
    table_195_2.set_cell_value(2, 0, "A2")
    table_195_2.set_cell_value(2, 1, "B2")
    table_195_2.set_cell_value(2, 2, "C2")
    table_195_2.set_cell_value(3, 0, "A3")
    table_195_2.set_cell_value(3, 1, "B3")
    table_195_2.set_cell_value(3, 2, "C3")
    table_195_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_195_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_195_2.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_195_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # panel: panel_195_3
    panel_195_3 = lv.obj(parent)
    objects["panel_195_3"] = panel_195_3
    panel_195_3.set_pos(152, 378)
    panel_195_3.set_size(54, 152)
    panel_195_3.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_195_3.set_style_border_width(2, lv.PART.MAIN)
    panel_195_3.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_195_3.set_style_radius(5, lv.PART.MAIN)
    panel_195_3.set_style_pad_all(0, lv.PART.MAIN)
    panel_195_3.set_style_pad_gap(0, lv.PART.MAIN)


def random_195_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_195_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_195_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_195_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_195_get_current_page():
    return current_screen

def random_195_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_195_load_page(0)
