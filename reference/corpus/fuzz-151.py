"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 151
Generated: 2023-11-14T22:16:23.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_151_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # keyboard: keyboard_151_0
    keyboard_151_0 = lv.keyboard(parent)
    objects["keyboard_151_0"] = keyboard_151_0
    keyboard_151_0.set_pos(599, 358)
    keyboard_151_0.set_size(143, 97)

    # table: table_151_1
    table_151_1 = lv.table(parent)
    objects["table_151_1"] = table_151_1
    table_151_1.set_pos(489, 45)
    table_151_1.set_size(248, 85)
    table_151_1.set_column_count(3)
    table_151_1.set_column_width(0, 100)
    table_151_1.set_column_width(1, 100)
    table_151_1.set_column_width(2, 100)
    table_151_1.set_cell_value(0, 0, "Col 1")
    table_151_1.set_cell_value(0, 1, "Col 2")
    table_151_1.set_cell_value(0, 2, "Col 3")
    table_151_1.set_cell_value(1, 0, "A1")
    table_151_1.set_cell_value(1, 1, "B1")
    table_151_1.set_cell_value(1, 2, "C1")
    table_151_1.set_cell_value(2, 0, "A2")
    table_151_1.set_cell_value(2, 1, "B2")
    table_151_1.set_cell_value(2, 2, "C2")
    table_151_1.set_cell_value(3, 0, "A3")
    table_151_1.set_cell_value(3, 1, "B3")
    table_151_1.set_cell_value(3, 2, "C3")
    table_151_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_151_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_151_1.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_151_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # roller: roller_151_2
    roller_151_2 = lv.roller(parent)
    objects["roller_151_2"] = roller_151_2
    roller_151_2.set_pos(398, 70)
    roller_151_2.set_size(255, 89)
    roller_151_2.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_151_2.set_visible_row_count(3)
    roller_151_2.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_151_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_151_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_151_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # label: label_151_3
    label_151_3 = lv.label(parent)
    objects["label_151_3"] = label_151_3
    label_151_3.set_pos(690, 109)
    label_151_3.set_size(22, 74)
    label_151_3.set_text("Testo 151:3 \" \\ Città")
    label_151_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_151_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_151_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # chart: chart_151_4
    chart_151_4 = lv.chart(parent)
    objects["chart_151_4"] = chart_151_4
    chart_151_4.set_pos(286, 157)
    chart_151_4.set_size(245, 62)
    chart_151_4.set_type(lv.chart.TYPE.LINE)
    chart_151_4.set_point_count(10)
    chart_151_4.set_div_line_count(3, 5)
    chart_151_4.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_151_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_151_4_series_1 = chart_151_4.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_151_4.set_next_value(chart_151_4_series_1, 10)
    chart_151_4.set_next_value(chart_151_4_series_1, 20)
    chart_151_4.set_next_value(chart_151_4_series_1, 30)
    chart_151_4.set_next_value(chart_151_4_series_1, 25)
    chart_151_4.set_next_value(chart_151_4_series_1, 40)
    chart_151_4.set_next_value(chart_151_4_series_1, 35)
    chart_151_4.set_next_value(chart_151_4_series_1, 50)

    # keyboard: keyboard_151_5
    keyboard_151_5 = lv.keyboard(parent)
    objects["keyboard_151_5"] = keyboard_151_5
    keyboard_151_5.set_pos(122, 138)
    keyboard_151_5.set_size(248, 122)

    # menu: menu_151_6
    menu_151_6 = lv.obj(parent)
    objects["menu_151_6"] = menu_151_6
    menu_151_6.set_pos(508, 136)
    menu_151_6.set_size(140, 128)
    menu_151_6.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_151_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_151_6_title = lv.label(menu_151_6)
    menu_151_6_title.set_text("Menu")
    menu_151_6_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_151_6_item_1 = lv.button(menu_151_6)
    menu_151_6_item_1.set_width(lv.pct(100))
    menu_151_6_item_1_label = lv.label(menu_151_6_item_1)
    menu_151_6_item_1_label.set_text("Item 1")
    menu_151_6_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_151_6_item_2 = lv.button(menu_151_6)
    menu_151_6_item_2.set_width(lv.pct(100))
    menu_151_6_item_2_label = lv.label(menu_151_6_item_2)
    menu_151_6_item_2_label.set_text("Item 2")
    menu_151_6_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_151_6_item_3 = lv.button(menu_151_6)
    menu_151_6_item_3.set_width(lv.pct(100))
    menu_151_6_item_3_label = lv.label(menu_151_6_item_3)
    menu_151_6_item_3_label.set_text("Item 3")
    menu_151_6_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_151_6_item_4 = lv.button(menu_151_6)
    menu_151_6_item_4.set_width(lv.pct(100))
    menu_151_6_item_4_label = lv.label(menu_151_6_item_4)
    menu_151_6_item_4_label.set_text("Item 4")
    menu_151_6_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # led: led_151_7
    led_151_7 = lv.led(parent)
    objects["led_151_7"] = led_151_7
    led_151_7.set_pos(676, 263)
    led_151_7.set_size(22, 66)
    led_151_7.set_color(lv.color_hex(0xFF0000))
    led_151_7.set_brightness(255)


def random_151_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_151_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_151_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_151_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_151_get_current_page():
    return current_screen

def random_151_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_151_load_page(0)
