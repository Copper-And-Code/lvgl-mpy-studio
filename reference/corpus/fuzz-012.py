"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 12
Generated: 2023-11-14T22:14:04.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_12_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # menu: menu_12_0
    menu_12_0 = lv.obj(parent)
    objects["menu_12_0"] = menu_12_0
    menu_12_0.set_pos(186, 323)
    menu_12_0.set_size(169, 127)
    menu_12_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_12_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_12_0_title = lv.label(menu_12_0)
    menu_12_0_title.set_text("Menu")
    menu_12_0_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_12_0_item_1 = lv.button(menu_12_0)
    menu_12_0_item_1.set_width(lv.pct(100))
    menu_12_0_item_1_label = lv.label(menu_12_0_item_1)
    menu_12_0_item_1_label.set_text("Item 1")
    menu_12_0_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_12_0_item_2 = lv.button(menu_12_0)
    menu_12_0_item_2.set_width(lv.pct(100))
    menu_12_0_item_2_label = lv.label(menu_12_0_item_2)
    menu_12_0_item_2_label.set_text("Item 2")
    menu_12_0_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_12_0_item_3 = lv.button(menu_12_0)
    menu_12_0_item_3.set_width(lv.pct(100))
    menu_12_0_item_3_label = lv.label(menu_12_0_item_3)
    menu_12_0_item_3_label.set_text("Item 3")
    menu_12_0_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_12_0_item_4 = lv.button(menu_12_0)
    menu_12_0_item_4.set_width(lv.pct(100))
    menu_12_0_item_4_label = lv.label(menu_12_0_item_4)
    menu_12_0_item_4_label.set_text("Item 4")
    menu_12_0_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # arc: arc_12_1
    arc_12_1 = lv.arc(parent)
    objects["arc_12_1"] = arc_12_1
    arc_12_1.set_pos(434, 146)
    arc_12_1.set_size(257, 44)
    arc_12_1.set_bg_angles(135, 45)
    arc_12_1.set_range(0, 100)
    arc_12_1.set_value(50)
    arc_12_1.set_style_arc_width(10, lv.PART.MAIN)
    arc_12_1.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_12_1.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_12_1.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_12_1.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # button: button_12_2
    button_12_2 = lv.button(parent)
    objects["button_12_2"] = button_12_2
    button_12_2.set_pos(384, 0)
    button_12_2.set_size(110, 66)
    button_12_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_12_2.set_style_radius(5, lv.PART.MAIN)
    button_12_2_label = lv.label(button_12_2)
    button_12_2_label.set_text("Testo 12:2 \" \\ Città")
    button_12_2_label.center()
    button_12_2_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_12_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # arc: arc_12_3
    arc_12_3 = lv.arc(parent)
    objects["arc_12_3"] = arc_12_3
    arc_12_3.set_pos(480, 110)
    arc_12_3.set_size(93, 92)
    arc_12_3.set_bg_angles(135, 45)
    arc_12_3.set_range(0, 100)
    arc_12_3.set_value(50)
    arc_12_3.set_style_arc_width(10, lv.PART.MAIN)
    arc_12_3.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_12_3.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_12_3.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_12_3.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # roller: roller_12_4
    roller_12_4 = lv.roller(parent)
    objects["roller_12_4"] = roller_12_4
    roller_12_4.set_pos(306, 145)
    roller_12_4.set_size(176, 133)
    roller_12_4.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_12_4.set_visible_row_count(3)
    roller_12_4.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_12_4.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_12_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_12_4.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # table: table_12_5
    table_12_5 = lv.table(parent)
    objects["table_12_5"] = table_12_5
    table_12_5.set_pos(267, 43)
    table_12_5.set_size(163, 143)
    table_12_5.set_column_count(3)
    table_12_5.set_column_width(0, 100)
    table_12_5.set_column_width(1, 100)
    table_12_5.set_column_width(2, 100)
    table_12_5.set_cell_value(0, 0, "Col 1")
    table_12_5.set_cell_value(0, 1, "Col 2")
    table_12_5.set_cell_value(0, 2, "Col 3")
    table_12_5.set_cell_value(1, 0, "A1")
    table_12_5.set_cell_value(1, 1, "B1")
    table_12_5.set_cell_value(1, 2, "C1")
    table_12_5.set_cell_value(2, 0, "A2")
    table_12_5.set_cell_value(2, 1, "B2")
    table_12_5.set_cell_value(2, 2, "C2")
    table_12_5.set_cell_value(3, 0, "A3")
    table_12_5.set_cell_value(3, 1, "B3")
    table_12_5.set_cell_value(3, 2, "C3")
    table_12_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_12_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_12_5.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_12_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # chart: chart_12_6
    chart_12_6 = lv.chart(parent)
    objects["chart_12_6"] = chart_12_6
    chart_12_6.set_pos(143, 223)
    chart_12_6.set_size(117, 65)
    chart_12_6.set_type(lv.chart.TYPE.LINE)
    chart_12_6.set_point_count(10)
    chart_12_6.set_div_line_count(3, 5)
    chart_12_6.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_12_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_12_6_series_1 = chart_12_6.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_12_6.set_next_value(chart_12_6_series_1, 10)
    chart_12_6.set_next_value(chart_12_6_series_1, 20)
    chart_12_6.set_next_value(chart_12_6_series_1, 30)
    chart_12_6.set_next_value(chart_12_6_series_1, 25)
    chart_12_6.set_next_value(chart_12_6_series_1, 40)
    chart_12_6.set_next_value(chart_12_6_series_1, 35)
    chart_12_6.set_next_value(chart_12_6_series_1, 50)

    # spinbox: spinbox_12_7
    spinbox_12_7 = lv.spinbox(parent)
    objects["spinbox_12_7"] = spinbox_12_7
    spinbox_12_7.set_pos(282, 234)
    spinbox_12_7.set_size(36, 34)
    spinbox_12_7.set_digit_format(4, 0)
    spinbox_12_7.set_range(0, 999)
    spinbox_12_7.set_value(0)
    spinbox_12_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_12_7.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_12_7.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_12_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_12_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_12_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_12_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_12_get_current_page():
    return current_screen

def random_12_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_12_load_page(0)
