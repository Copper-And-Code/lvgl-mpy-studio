"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 131
Generated: 2023-11-14T22:16:03.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_131_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # table: table_131_0
    table_131_0 = lv.table(parent)
    objects["table_131_0"] = table_131_0
    table_131_0.set_pos(522, 18)
    table_131_0.set_size(181, 18)
    table_131_0.set_column_count(3)
    table_131_0.set_column_width(0, 100)
    table_131_0.set_column_width(1, 100)
    table_131_0.set_column_width(2, 100)
    table_131_0.set_cell_value(0, 0, "Col 1")
    table_131_0.set_cell_value(0, 1, "Col 2")
    table_131_0.set_cell_value(0, 2, "Col 3")
    table_131_0.set_cell_value(1, 0, "A1")
    table_131_0.set_cell_value(1, 1, "B1")
    table_131_0.set_cell_value(1, 2, "C1")
    table_131_0.set_cell_value(2, 0, "A2")
    table_131_0.set_cell_value(2, 1, "B2")
    table_131_0.set_cell_value(2, 2, "C2")
    table_131_0.set_cell_value(3, 0, "A3")
    table_131_0.set_cell_value(3, 1, "B3")
    table_131_0.set_cell_value(3, 2, "C3")
    table_131_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_131_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_131_0.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_131_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # table: table_131_1
    table_131_1 = lv.table(parent)
    objects["table_131_1"] = table_131_1
    table_131_1.set_pos(217, 45)
    table_131_1.set_size(162, 119)
    table_131_1.set_column_count(3)
    table_131_1.set_column_width(0, 100)
    table_131_1.set_column_width(1, 100)
    table_131_1.set_column_width(2, 100)
    table_131_1.set_cell_value(0, 0, "Col 1")
    table_131_1.set_cell_value(0, 1, "Col 2")
    table_131_1.set_cell_value(0, 2, "Col 3")
    table_131_1.set_cell_value(1, 0, "A1")
    table_131_1.set_cell_value(1, 1, "B1")
    table_131_1.set_cell_value(1, 2, "C1")
    table_131_1.set_cell_value(2, 0, "A2")
    table_131_1.set_cell_value(2, 1, "B2")
    table_131_1.set_cell_value(2, 2, "C2")
    table_131_1.set_cell_value(3, 0, "A3")
    table_131_1.set_cell_value(3, 1, "B3")
    table_131_1.set_cell_value(3, 2, "C3")
    table_131_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_131_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_131_1.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_131_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # table: table_131_2
    table_131_2 = lv.table(parent)
    objects["table_131_2"] = table_131_2
    table_131_2.set_pos(12, 366)
    table_131_2.set_size(262, 144)
    table_131_2.set_column_count(3)
    table_131_2.set_column_width(0, 100)
    table_131_2.set_column_width(1, 100)
    table_131_2.set_column_width(2, 100)
    table_131_2.set_cell_value(0, 0, "Col 1")
    table_131_2.set_cell_value(0, 1, "Col 2")
    table_131_2.set_cell_value(0, 2, "Col 3")
    table_131_2.set_cell_value(1, 0, "A1")
    table_131_2.set_cell_value(1, 1, "B1")
    table_131_2.set_cell_value(1, 2, "C1")
    table_131_2.set_cell_value(2, 0, "A2")
    table_131_2.set_cell_value(2, 1, "B2")
    table_131_2.set_cell_value(2, 2, "C2")
    table_131_2.set_cell_value(3, 0, "A3")
    table_131_2.set_cell_value(3, 1, "B3")
    table_131_2.set_cell_value(3, 2, "C3")
    table_131_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_131_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_131_2.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_131_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # image: image_131_3
    image_131_3 = lv.image(parent)
    objects["image_131_3"] = image_131_3
    image_131_3.set_pos(38, 326)
    image_131_3.set_size(262, 71)

    # span: span_131_4
    span_131_4 = lv.spangroup(parent)
    objects["span_131_4"] = span_131_4
    span_131_4.set_pos(304, 161)
    span_131_4.set_size(112, 10)
    span_131_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_131_4_span_1 = span_131_4.add_span()
    span_131_4_span_1.set_text("Normal text")
    span_131_4_span_1_style = span_131_4_span_1.get_style()
    span_131_4_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_131_4_span_1_style.set_text_font(lv.font_montserrat_14)
    span_131_4_span_2 = span_131_4.add_span()
    span_131_4_span_2.set_text("Bold text")
    span_131_4_span_2_style = span_131_4_span_2.get_style()
    span_131_4_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_131_4_span_2_style.set_text_font(lv.font_montserrat_16)
    span_131_4_span_3 = span_131_4.add_span()
    span_131_4_span_3.set_text("Small text")
    span_131_4_span_3_style = span_131_4_span_3.get_style()
    span_131_4_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_131_4_span_3_style.set_text_font(lv.font_montserrat_14)
    span_131_4.refresh()

    # bar: bar_131_5
    bar_131_5 = lv.bar(parent)
    objects["bar_131_5"] = bar_131_5
    bar_131_5.set_pos(216, 61)
    bar_131_5.set_size(154, 58)
    bar_131_5.set_range(0, 100)
    bar_131_5.set_value(50, False)
    bar_131_5.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_131_5.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # tabview: tabview_131_6
    tabview_131_6 = lv.tabview(parent)
    objects["tabview_131_6"] = tabview_131_6
    tabview_131_6.set_pos(595, 284)
    tabview_131_6.set_size(260, 62)
    tabview_131_6.set_tab_bar_position(lv.DIR.TOP)
    tabview_131_6.set_tab_bar_size(40)
    tabview_131_6_tab_1 = tabview_131_6.add_tab("Tab 1")
    tabview_131_6_tab_2 = tabview_131_6.add_tab("Tab 2")
    tabview_131_6_tab_3 = tabview_131_6.add_tab("Tab 3")
    tabview_131_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_131_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_131_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_131_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_131_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_131_get_current_page():
    return current_screen

def random_131_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_131_load_page(0)
