"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 86
Generated: 2023-11-14T22:15:18.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_86_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # button: button_86_0
    button_86_0 = lv.button(parent)
    objects["button_86_0"] = button_86_0
    button_86_0.set_pos(642, 204)
    button_86_0.set_size(220, 102)
    button_86_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_86_0.set_style_radius(5, lv.PART.MAIN)
    button_86_0_label = lv.label(button_86_0)
    button_86_0_label.set_text("Testo 86:0 \" \\ Città")
    button_86_0_label.center()
    button_86_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_86_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # tabview: tabview_86_1
    tabview_86_1 = lv.tabview(parent)
    objects["tabview_86_1"] = tabview_86_1
    tabview_86_1.set_pos(610, 135)
    tabview_86_1.set_size(178, 157)
    tabview_86_1.set_tab_bar_position(lv.DIR.TOP)
    tabview_86_1.set_tab_bar_size(40)
    tabview_86_1_tab_1 = tabview_86_1.add_tab("Tab 1")
    tabview_86_1_tab_2 = tabview_86_1.add_tab("Tab 2")
    tabview_86_1_tab_3 = tabview_86_1.add_tab("Tab 3")
    tabview_86_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # msgbox: msgbox_86_2
    msgbox_86_2 = lv.msgbox(parent)
    objects["msgbox_86_2"] = msgbox_86_2
    msgbox_86_2.set_pos(133, 1)
    msgbox_86_2.set_size(222, 97)
    msgbox_86_2_title = msgbox_86_2.add_title("Notice")
    msgbox_86_2_text = msgbox_86_2.add_text("Testo 86:2 \" \\ Città")
    msgbox_86_2_button_1 = msgbox_86_2.add_footer_button("OK")
    msgbox_86_2_button_2 = msgbox_86_2.add_footer_button("Cancel")
    msgbox_86_2_close = msgbox_86_2.add_close_button()
    msgbox_86_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # table: table_86_3
    table_86_3 = lv.table(parent)
    objects["table_86_3"] = table_86_3
    table_86_3.set_pos(121, 91)
    table_86_3.set_size(253, 93)
    table_86_3.set_column_count(3)
    table_86_3.set_column_width(0, 100)
    table_86_3.set_column_width(1, 100)
    table_86_3.set_column_width(2, 100)
    table_86_3.set_cell_value(0, 0, "Col 1")
    table_86_3.set_cell_value(0, 1, "Col 2")
    table_86_3.set_cell_value(0, 2, "Col 3")
    table_86_3.set_cell_value(1, 0, "A1")
    table_86_3.set_cell_value(1, 1, "B1")
    table_86_3.set_cell_value(1, 2, "C1")
    table_86_3.set_cell_value(2, 0, "A2")
    table_86_3.set_cell_value(2, 1, "B2")
    table_86_3.set_cell_value(2, 2, "C2")
    table_86_3.set_cell_value(3, 0, "A3")
    table_86_3.set_cell_value(3, 1, "B3")
    table_86_3.set_cell_value(3, 2, "C3")
    table_86_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_86_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_86_3.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_86_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # table: table_86_4
    table_86_4 = lv.table(parent)
    objects["table_86_4"] = table_86_4
    table_86_4.set_pos(401, 255)
    table_86_4.set_size(174, 118)
    table_86_4.set_column_count(3)
    table_86_4.set_column_width(0, 100)
    table_86_4.set_column_width(1, 100)
    table_86_4.set_column_width(2, 100)
    table_86_4.set_cell_value(0, 0, "Col 1")
    table_86_4.set_cell_value(0, 1, "Col 2")
    table_86_4.set_cell_value(0, 2, "Col 3")
    table_86_4.set_cell_value(1, 0, "A1")
    table_86_4.set_cell_value(1, 1, "B1")
    table_86_4.set_cell_value(1, 2, "C1")
    table_86_4.set_cell_value(2, 0, "A2")
    table_86_4.set_cell_value(2, 1, "B2")
    table_86_4.set_cell_value(2, 2, "C2")
    table_86_4.set_cell_value(3, 0, "A3")
    table_86_4.set_cell_value(3, 1, "B3")
    table_86_4.set_cell_value(3, 2, "C3")
    table_86_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_86_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_86_4.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_86_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # menu: menu_86_5
    menu_86_5 = lv.obj(parent)
    objects["menu_86_5"] = menu_86_5
    menu_86_5.set_pos(144, 214)
    menu_86_5.set_size(162, 92)
    menu_86_5.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_86_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_86_5_title = lv.label(menu_86_5)
    menu_86_5_title.set_text("Menu")
    menu_86_5_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_86_5_item_1 = lv.button(menu_86_5)
    menu_86_5_item_1.set_width(lv.pct(100))
    menu_86_5_item_1_label = lv.label(menu_86_5_item_1)
    menu_86_5_item_1_label.set_text("Item 1")
    menu_86_5_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_86_5_item_2 = lv.button(menu_86_5)
    menu_86_5_item_2.set_width(lv.pct(100))
    menu_86_5_item_2_label = lv.label(menu_86_5_item_2)
    menu_86_5_item_2_label.set_text("Item 2")
    menu_86_5_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_86_5_item_3 = lv.button(menu_86_5)
    menu_86_5_item_3.set_width(lv.pct(100))
    menu_86_5_item_3_label = lv.label(menu_86_5_item_3)
    menu_86_5_item_3_label.set_text("Item 3")
    menu_86_5_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_86_5_item_4 = lv.button(menu_86_5)
    menu_86_5_item_4.set_width(lv.pct(100))
    menu_86_5_item_4_label = lv.label(menu_86_5_item_4)
    menu_86_5_item_4_label.set_text("Item 4")
    menu_86_5_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # scale: scale_86_6
    scale_86_6 = lv.scale(parent)
    objects["scale_86_6"] = scale_86_6
    scale_86_6.set_pos(95, 161)
    scale_86_6.set_size(75, 80)
    scale_86_6.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_86_6.set_range(0, 100)
    scale_86_6.set_total_tick_count(51)
    scale_86_6.set_major_tick_every(5)
    scale_86_6.set_style_length(15, lv.PART.INDICATOR)
    scale_86_6.set_style_length(8, lv.PART.ITEMS)
    scale_86_6.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_86_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)


def random_86_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_86_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_86_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_86_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_86_get_current_page():
    return current_screen

def random_86_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_86_load_page(0)
