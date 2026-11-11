"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 14
Generated: 2023-11-14T22:14:06.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_14_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # chart: chart_14_0
    chart_14_0 = lv.chart(parent)
    objects["chart_14_0"] = chart_14_0
    chart_14_0.set_pos(138, 48)
    chart_14_0.set_size(201, 82)
    chart_14_0.set_type(lv.chart.TYPE.LINE)
    chart_14_0.set_point_count(10)
    chart_14_0.set_div_line_count(3, 5)
    chart_14_0.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_14_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_14_0_series_1 = chart_14_0.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_14_0.set_next_value(chart_14_0_series_1, 10)
    chart_14_0.set_next_value(chart_14_0_series_1, 20)
    chart_14_0.set_next_value(chart_14_0_series_1, 30)
    chart_14_0.set_next_value(chart_14_0_series_1, 25)
    chart_14_0.set_next_value(chart_14_0_series_1, 40)
    chart_14_0.set_next_value(chart_14_0_series_1, 35)
    chart_14_0.set_next_value(chart_14_0_series_1, 50)

    # menu: menu_14_1
    menu_14_1 = lv.obj(parent)
    objects["menu_14_1"] = menu_14_1
    menu_14_1.set_pos(412, 357)
    menu_14_1.set_size(138, 39)
    menu_14_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_14_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_14_1_title = lv.label(menu_14_1)
    menu_14_1_title.set_text("Menu")
    menu_14_1_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_14_1_item_1 = lv.button(menu_14_1)
    menu_14_1_item_1.set_width(lv.pct(100))
    menu_14_1_item_1_label = lv.label(menu_14_1_item_1)
    menu_14_1_item_1_label.set_text("Item 1")
    menu_14_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_14_1_item_2 = lv.button(menu_14_1)
    menu_14_1_item_2.set_width(lv.pct(100))
    menu_14_1_item_2_label = lv.label(menu_14_1_item_2)
    menu_14_1_item_2_label.set_text("Item 2")
    menu_14_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_14_1_item_3 = lv.button(menu_14_1)
    menu_14_1_item_3.set_width(lv.pct(100))
    menu_14_1_item_3_label = lv.label(menu_14_1_item_3)
    menu_14_1_item_3_label.set_text("Item 3")
    menu_14_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_14_1_item_4 = lv.button(menu_14_1)
    menu_14_1_item_4.set_width(lv.pct(100))
    menu_14_1_item_4_label = lv.label(menu_14_1_item_4)
    menu_14_1_item_4_label.set_text("Item 4")
    menu_14_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # switch: switch_14_2
    switch_14_2 = lv.switch(parent)
    objects["switch_14_2"] = switch_14_2
    switch_14_2.set_pos(467, 34)
    switch_14_2.set_size(103, 27)
    switch_14_2.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_14_2.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_14_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)


def random_14_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_14_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_14_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_14_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_14_get_current_page():
    return current_screen

def random_14_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_14_load_page(0)
