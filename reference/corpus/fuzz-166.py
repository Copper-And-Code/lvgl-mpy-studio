"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 166
Generated: 2023-11-14T22:16:38.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_166_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # label: label_166_0
    label_166_0 = lv.label(parent)
    objects["label_166_0"] = label_166_0
    label_166_0.set_pos(158, 284)
    label_166_0.set_size(31, 150)
    label_166_0.set_text("Testo 166:0 \" \\ Città")
    label_166_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_166_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_166_0.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # menu: menu_166_1
    menu_166_1 = lv.obj(parent)
    objects["menu_166_1"] = menu_166_1
    menu_166_1.set_pos(276, 238)
    menu_166_1.set_size(158, 108)
    menu_166_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_166_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_166_1_title = lv.label(menu_166_1)
    menu_166_1_title.set_text("Menu")
    menu_166_1_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_166_1_item_1 = lv.button(menu_166_1)
    menu_166_1_item_1.set_width(lv.pct(100))
    menu_166_1_item_1_label = lv.label(menu_166_1_item_1)
    menu_166_1_item_1_label.set_text("Item 1")
    menu_166_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_166_1_item_2 = lv.button(menu_166_1)
    menu_166_1_item_2.set_width(lv.pct(100))
    menu_166_1_item_2_label = lv.label(menu_166_1_item_2)
    menu_166_1_item_2_label.set_text("Item 2")
    menu_166_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_166_1_item_3 = lv.button(menu_166_1)
    menu_166_1_item_3.set_width(lv.pct(100))
    menu_166_1_item_3_label = lv.label(menu_166_1_item_3)
    menu_166_1_item_3_label.set_text("Item 3")
    menu_166_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_166_1_item_4 = lv.button(menu_166_1)
    menu_166_1_item_4.set_width(lv.pct(100))
    menu_166_1_item_4_label = lv.label(menu_166_1_item_4)
    menu_166_1_item_4_label.set_text("Item 4")
    menu_166_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # table: table_166_2
    table_166_2 = lv.table(parent)
    objects["table_166_2"] = table_166_2
    table_166_2.set_pos(156, 128)
    table_166_2.set_size(184, 108)
    table_166_2.set_column_count(3)
    table_166_2.set_column_width(0, 100)
    table_166_2.set_column_width(1, 100)
    table_166_2.set_column_width(2, 100)
    table_166_2.set_cell_value(0, 0, "Col 1")
    table_166_2.set_cell_value(0, 1, "Col 2")
    table_166_2.set_cell_value(0, 2, "Col 3")
    table_166_2.set_cell_value(1, 0, "A1")
    table_166_2.set_cell_value(1, 1, "B1")
    table_166_2.set_cell_value(1, 2, "C1")
    table_166_2.set_cell_value(2, 0, "A2")
    table_166_2.set_cell_value(2, 1, "B2")
    table_166_2.set_cell_value(2, 2, "C2")
    table_166_2.set_cell_value(3, 0, "A3")
    table_166_2.set_cell_value(3, 1, "B3")
    table_166_2.set_cell_value(3, 2, "C3")
    table_166_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_166_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_166_2.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_166_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # slider: slider_166_3
    slider_166_3 = lv.slider(parent)
    objects["slider_166_3"] = slider_166_3
    slider_166_3.set_pos(596, 166)
    slider_166_3.set_size(129, 106)
    slider_166_3.set_range(0, 100)
    slider_166_3.set_value(50, False)
    slider_166_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_166_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_166_3.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)

    # switch: switch_166_4
    switch_166_4 = lv.switch(parent)
    objects["switch_166_4"] = switch_166_4
    switch_166_4.set_pos(604, 250)
    switch_166_4.set_size(265, 18)
    switch_166_4.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_166_4.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_166_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)


def random_166_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_166_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_166_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_166_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_166_get_current_page():
    return current_screen

def random_166_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_166_load_page(0)
