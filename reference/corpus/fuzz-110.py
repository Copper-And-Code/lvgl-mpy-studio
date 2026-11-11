"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 110
Generated: 2023-11-14T22:15:42.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_110_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # switch: switch_110_0
    switch_110_0 = lv.switch(parent)
    objects["switch_110_0"] = switch_110_0
    switch_110_0.set_pos(210, 144)
    switch_110_0.set_size(247, 105)
    switch_110_0.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_110_0.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_110_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # table: table_110_1
    table_110_1 = lv.table(parent)
    objects["table_110_1"] = table_110_1
    table_110_1.set_pos(572, 91)
    table_110_1.set_size(189, 139)
    table_110_1.set_column_count(3)
    table_110_1.set_column_width(0, 100)
    table_110_1.set_column_width(1, 100)
    table_110_1.set_column_width(2, 100)
    table_110_1.set_cell_value(0, 0, "Col 1")
    table_110_1.set_cell_value(0, 1, "Col 2")
    table_110_1.set_cell_value(0, 2, "Col 3")
    table_110_1.set_cell_value(1, 0, "A1")
    table_110_1.set_cell_value(1, 1, "B1")
    table_110_1.set_cell_value(1, 2, "C1")
    table_110_1.set_cell_value(2, 0, "A2")
    table_110_1.set_cell_value(2, 1, "B2")
    table_110_1.set_cell_value(2, 2, "C2")
    table_110_1.set_cell_value(3, 0, "A3")
    table_110_1.set_cell_value(3, 1, "B3")
    table_110_1.set_cell_value(3, 2, "C3")
    table_110_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_110_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_110_1.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_110_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # label: label_110_2
    label_110_2 = lv.label(parent)
    objects["label_110_2"] = label_110_2
    label_110_2.set_pos(516, 397)
    label_110_2.set_size(67, 134)
    label_110_2.set_text("Testo 110:2 \" \\ Città")
    label_110_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_110_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_110_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # win: win_110_3
    win_110_3 = lv.obj(parent)
    objects["win_110_3"] = win_110_3
    win_110_3.set_pos(130, 339)
    win_110_3.set_size(55, 152)
    win_110_3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_110_3.set_style_pad_all(0, lv.PART.MAIN)
    win_110_3.set_style_pad_row(0, lv.PART.MAIN)
    win_110_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_110_3_header = lv.obj(win_110_3)
    win_110_3_header.set_size(lv.pct(100), 40)
    win_110_3_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_110_3_header.set_style_radius(0, lv.PART.MAIN)
    win_110_3_title = lv.label(win_110_3_header)
    win_110_3_title.set_text("Window Title")
    win_110_3_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_110_3_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_110_3_content = lv.obj(win_110_3)
    win_110_3_content.set_width(lv.pct(100))
    win_110_3_content.set_flex_grow(1)

    # checkbox: checkbox_110_4
    checkbox_110_4 = lv.checkbox(parent)
    objects["checkbox_110_4"] = checkbox_110_4
    checkbox_110_4.set_pos(65, 256)
    checkbox_110_4.set_text("Testo 110:4 \" \\ Città")
    checkbox_110_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_110_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_110_4.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # label: label_110_5
    label_110_5 = lv.label(parent)
    objects["label_110_5"] = label_110_5
    label_110_5.set_pos(65, 105)
    label_110_5.set_size(158, 33)
    label_110_5.set_text("Testo 110:5 \" \\ Città")
    label_110_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_110_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_110_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)


def random_110_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_110_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_110_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_110_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_110_get_current_page():
    return current_screen

def random_110_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_110_load_page(0)
