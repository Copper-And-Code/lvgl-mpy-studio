"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 6
Generated: 2023-11-14T22:13:58.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_6_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # imagebutton: imagebutton_6_0
    imagebutton_6_0 = lv.imagebutton(parent)
    objects["imagebutton_6_0"] = imagebutton_6_0
    imagebutton_6_0.set_pos(518, 134)
    imagebutton_6_0.set_size(243, 64)
    imagebutton_6_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_6_0.set_style_radius(5, lv.PART.MAIN)
    imagebutton_6_0_label = lv.label(imagebutton_6_0)
    imagebutton_6_0_label.set_text("Testo 6:0 \" \\ Città")
    imagebutton_6_0_label.center()
    imagebutton_6_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_6_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # table: table_6_1
    table_6_1 = lv.table(parent)
    objects["table_6_1"] = table_6_1
    table_6_1.set_pos(161, 96)
    table_6_1.set_size(64, 60)
    table_6_1.set_column_count(3)
    table_6_1.set_column_width(0, 100)
    table_6_1.set_column_width(1, 100)
    table_6_1.set_column_width(2, 100)
    table_6_1.set_cell_value(0, 0, "Col 1")
    table_6_1.set_cell_value(0, 1, "Col 2")
    table_6_1.set_cell_value(0, 2, "Col 3")
    table_6_1.set_cell_value(1, 0, "A1")
    table_6_1.set_cell_value(1, 1, "B1")
    table_6_1.set_cell_value(1, 2, "C1")
    table_6_1.set_cell_value(2, 0, "A2")
    table_6_1.set_cell_value(2, 1, "B2")
    table_6_1.set_cell_value(2, 2, "C2")
    table_6_1.set_cell_value(3, 0, "A3")
    table_6_1.set_cell_value(3, 1, "B3")
    table_6_1.set_cell_value(3, 2, "C3")
    table_6_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_6_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_6_1.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_6_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # calendar: calendar_6_2
    calendar_6_2 = lv.calendar(parent)
    objects["calendar_6_2"] = calendar_6_2
    calendar_6_2.set_pos(475, 91)
    calendar_6_2.set_size(46, 51)
    calendar_6_2.set_today_date(2026, 10, 28)
    calendar_6_2.set_month_shown(2026, 10)
    calendar_6_2_header = calendar_6_2.add_header_arrow()
    calendar_6_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # scale: scale_6_3
    scale_6_3 = lv.scale(parent)
    objects["scale_6_3"] = scale_6_3
    scale_6_3.set_pos(640, 237)
    scale_6_3.set_size(202, 81)
    scale_6_3.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_6_3.set_range(0, 100)
    scale_6_3.set_total_tick_count(51)
    scale_6_3.set_major_tick_every(5)
    scale_6_3.set_style_length(15, lv.PART.INDICATOR)
    scale_6_3.set_style_length(8, lv.PART.ITEMS)
    scale_6_3.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_6_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # switch: switch_6_4
    switch_6_4 = lv.switch(parent)
    objects["switch_6_4"] = switch_6_4
    switch_6_4.set_pos(644, 87)
    switch_6_4.set_size(70, 119)
    switch_6_4.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_6_4.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_6_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # keyboard: keyboard_6_5
    keyboard_6_5 = lv.keyboard(parent)
    objects["keyboard_6_5"] = keyboard_6_5
    keyboard_6_5.set_pos(282, 258)
    keyboard_6_5.set_size(212, 139)

    # tileview: tileview_6_6
    tileview_6_6 = lv.tileview(parent)
    objects["tileview_6_6"] = tileview_6_6
    tileview_6_6.set_pos(169, 87)
    tileview_6_6.set_size(46, 154)
    tileview_6_6.add_tile(0, 0, lv.DIR.ALL)
    tileview_6_6.add_tile(1, 0, lv.DIR.ALL)
    tileview_6_6.add_tile(0, 1, lv.DIR.ALL)
    tileview_6_6.add_tile(1, 1, lv.DIR.ALL)
    tileview_6_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_6_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_6_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_6_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_6_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_6_get_current_page():
    return current_screen

def random_6_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_6_load_page(0)
