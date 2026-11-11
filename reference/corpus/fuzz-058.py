"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 58
Generated: 2023-11-14T22:14:50.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_58_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # msgbox: msgbox_58_0
    msgbox_58_0 = lv.msgbox(parent)
    objects["msgbox_58_0"] = msgbox_58_0
    msgbox_58_0.set_pos(634, 40)
    msgbox_58_0.set_size(236, 120)
    msgbox_58_0_title = msgbox_58_0.add_title("Notice")
    msgbox_58_0_text = msgbox_58_0.add_text("Testo 58:0 \" \\ Città")
    msgbox_58_0_button_1 = msgbox_58_0.add_footer_button("OK")
    msgbox_58_0_button_2 = msgbox_58_0.add_footer_button("Cancel")
    msgbox_58_0_close = msgbox_58_0.add_close_button()
    msgbox_58_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # table: table_58_1
    table_58_1 = lv.table(parent)
    objects["table_58_1"] = table_58_1
    table_58_1.set_pos(699, 32)
    table_58_1.set_size(92, 104)
    table_58_1.set_column_count(3)
    table_58_1.set_column_width(0, 100)
    table_58_1.set_column_width(1, 100)
    table_58_1.set_column_width(2, 100)
    table_58_1.set_cell_value(0, 0, "Col 1")
    table_58_1.set_cell_value(0, 1, "Col 2")
    table_58_1.set_cell_value(0, 2, "Col 3")
    table_58_1.set_cell_value(1, 0, "A1")
    table_58_1.set_cell_value(1, 1, "B1")
    table_58_1.set_cell_value(1, 2, "C1")
    table_58_1.set_cell_value(2, 0, "A2")
    table_58_1.set_cell_value(2, 1, "B2")
    table_58_1.set_cell_value(2, 2, "C2")
    table_58_1.set_cell_value(3, 0, "A3")
    table_58_1.set_cell_value(3, 1, "B3")
    table_58_1.set_cell_value(3, 2, "C3")
    table_58_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_58_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_58_1.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_58_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # scale: scale_58_2
    scale_58_2 = lv.scale(parent)
    objects["scale_58_2"] = scale_58_2
    scale_58_2.set_pos(60, 34)
    scale_58_2.set_size(233, 50)
    scale_58_2.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_58_2.set_range(0, 100)
    scale_58_2.set_total_tick_count(51)
    scale_58_2.set_major_tick_every(5)
    scale_58_2.set_style_length(15, lv.PART.INDICATOR)
    scale_58_2.set_style_length(8, lv.PART.ITEMS)
    scale_58_2.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_58_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # win: win_58_3
    win_58_3 = lv.obj(parent)
    objects["win_58_3"] = win_58_3
    win_58_3.set_pos(236, 287)
    win_58_3.set_size(75, 150)
    win_58_3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_58_3.set_style_pad_all(0, lv.PART.MAIN)
    win_58_3.set_style_pad_row(0, lv.PART.MAIN)
    win_58_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_58_3_header = lv.obj(win_58_3)
    win_58_3_header.set_size(lv.pct(100), 40)
    win_58_3_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_58_3_header.set_style_radius(0, lv.PART.MAIN)
    win_58_3_title = lv.label(win_58_3_header)
    win_58_3_title.set_text("Window Title")
    win_58_3_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_58_3_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_58_3_content = lv.obj(win_58_3)
    win_58_3_content.set_width(lv.pct(100))
    win_58_3_content.set_flex_grow(1)

    # table: table_58_4
    table_58_4 = lv.table(parent)
    objects["table_58_4"] = table_58_4
    table_58_4.set_pos(513, 194)
    table_58_4.set_size(179, 22)
    table_58_4.set_column_count(3)
    table_58_4.set_column_width(0, 100)
    table_58_4.set_column_width(1, 100)
    table_58_4.set_column_width(2, 100)
    table_58_4.set_cell_value(0, 0, "Col 1")
    table_58_4.set_cell_value(0, 1, "Col 2")
    table_58_4.set_cell_value(0, 2, "Col 3")
    table_58_4.set_cell_value(1, 0, "A1")
    table_58_4.set_cell_value(1, 1, "B1")
    table_58_4.set_cell_value(1, 2, "C1")
    table_58_4.set_cell_value(2, 0, "A2")
    table_58_4.set_cell_value(2, 1, "B2")
    table_58_4.set_cell_value(2, 2, "C2")
    table_58_4.set_cell_value(3, 0, "A3")
    table_58_4.set_cell_value(3, 1, "B3")
    table_58_4.set_cell_value(3, 2, "C3")
    table_58_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_58_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_58_4.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_58_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # win: win_58_5
    win_58_5 = lv.obj(parent)
    objects["win_58_5"] = win_58_5
    win_58_5.set_pos(409, 39)
    win_58_5.set_size(229, 157)
    win_58_5.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_58_5.set_style_pad_all(0, lv.PART.MAIN)
    win_58_5.set_style_pad_row(0, lv.PART.MAIN)
    win_58_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_58_5_header = lv.obj(win_58_5)
    win_58_5_header.set_size(lv.pct(100), 40)
    win_58_5_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_58_5_header.set_style_radius(0, lv.PART.MAIN)
    win_58_5_title = lv.label(win_58_5_header)
    win_58_5_title.set_text("Window Title")
    win_58_5_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_58_5_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_58_5_content = lv.obj(win_58_5)
    win_58_5_content.set_width(lv.pct(100))
    win_58_5_content.set_flex_grow(1)

    # menu: menu_58_6
    menu_58_6 = lv.obj(parent)
    objects["menu_58_6"] = menu_58_6
    menu_58_6.set_pos(162, 319)
    menu_58_6.set_size(247, 24)
    menu_58_6.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_58_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_58_6_title = lv.label(menu_58_6)
    menu_58_6_title.set_text("Menu")
    menu_58_6_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_58_6_item_1 = lv.button(menu_58_6)
    menu_58_6_item_1.set_width(lv.pct(100))
    menu_58_6_item_1_label = lv.label(menu_58_6_item_1)
    menu_58_6_item_1_label.set_text("Item 1")
    menu_58_6_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_58_6_item_2 = lv.button(menu_58_6)
    menu_58_6_item_2.set_width(lv.pct(100))
    menu_58_6_item_2_label = lv.label(menu_58_6_item_2)
    menu_58_6_item_2_label.set_text("Item 2")
    menu_58_6_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_58_6_item_3 = lv.button(menu_58_6)
    menu_58_6_item_3.set_width(lv.pct(100))
    menu_58_6_item_3_label = lv.label(menu_58_6_item_3)
    menu_58_6_item_3_label.set_text("Item 3")
    menu_58_6_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_58_6_item_4 = lv.button(menu_58_6)
    menu_58_6_item_4.set_width(lv.pct(100))
    menu_58_6_item_4_label = lv.label(menu_58_6_item_4)
    menu_58_6_item_4_label.set_text("Item 4")
    menu_58_6_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # span: span_58_7
    span_58_7 = lv.spangroup(parent)
    objects["span_58_7"] = span_58_7
    span_58_7.set_pos(264, 263)
    span_58_7.set_size(106, 25)
    span_58_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_58_7_span_1 = span_58_7.add_span()
    span_58_7_span_1.set_text("Normal text")
    span_58_7_span_1_style = span_58_7_span_1.get_style()
    span_58_7_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_58_7_span_1_style.set_text_font(lv.font_montserrat_14)
    span_58_7_span_2 = span_58_7.add_span()
    span_58_7_span_2.set_text("Bold text")
    span_58_7_span_2_style = span_58_7_span_2.get_style()
    span_58_7_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_58_7_span_2_style.set_text_font(lv.font_montserrat_16)
    span_58_7_span_3 = span_58_7.add_span()
    span_58_7_span_3.set_text("Small text")
    span_58_7_span_3_style = span_58_7_span_3.get_style()
    span_58_7_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_58_7_span_3_style.set_text_font(lv.font_montserrat_14)
    span_58_7.refresh()


def random_58_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_58_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_58_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_58_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_58_get_current_page():
    return current_screen

def random_58_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_58_load_page(0)
