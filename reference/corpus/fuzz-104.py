"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 104
Generated: 2023-11-14T22:15:36.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_104_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # switch: switch_104_0
    switch_104_0 = lv.switch(parent)
    objects["switch_104_0"] = switch_104_0
    switch_104_0.set_pos(678, 15)
    switch_104_0.set_size(104, 136)
    switch_104_0.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_104_0.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_104_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # panel: panel_104_1
    panel_104_1 = lv.obj(parent)
    objects["panel_104_1"] = panel_104_1
    panel_104_1.set_pos(625, 339)
    panel_104_1.set_size(206, 145)
    panel_104_1.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_104_1.set_style_border_width(2, lv.PART.MAIN)
    panel_104_1.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_104_1.set_style_radius(5, lv.PART.MAIN)
    panel_104_1.set_style_pad_all(0, lv.PART.MAIN)
    panel_104_1.set_style_pad_gap(0, lv.PART.MAIN)

    # tileview: tileview_104_2
    tileview_104_2 = lv.tileview(parent)
    objects["tileview_104_2"] = tileview_104_2
    tileview_104_2.set_pos(490, 102)
    tileview_104_2.set_size(26, 25)
    tileview_104_2.add_tile(0, 0, lv.DIR.ALL)
    tileview_104_2.add_tile(1, 0, lv.DIR.ALL)
    tileview_104_2.add_tile(0, 1, lv.DIR.ALL)
    tileview_104_2.add_tile(1, 1, lv.DIR.ALL)
    tileview_104_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # chart: chart_104_3
    chart_104_3 = lv.chart(parent)
    objects["chart_104_3"] = chart_104_3
    chart_104_3.set_pos(90, 2)
    chart_104_3.set_size(109, 20)
    chart_104_3.set_type(lv.chart.TYPE.LINE)
    chart_104_3.set_point_count(10)
    chart_104_3.set_div_line_count(3, 5)
    chart_104_3.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_104_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_104_3_series_1 = chart_104_3.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_104_3.set_next_value(chart_104_3_series_1, 10)
    chart_104_3.set_next_value(chart_104_3_series_1, 20)
    chart_104_3.set_next_value(chart_104_3_series_1, 30)
    chart_104_3.set_next_value(chart_104_3_series_1, 25)
    chart_104_3.set_next_value(chart_104_3_series_1, 40)
    chart_104_3.set_next_value(chart_104_3_series_1, 35)
    chart_104_3.set_next_value(chart_104_3_series_1, 50)

    # led: led_104_4
    led_104_4 = lv.led(parent)
    objects["led_104_4"] = led_104_4
    led_104_4.set_pos(435, 16)
    led_104_4.set_size(214, 64)
    led_104_4.set_color(lv.color_hex(0xFF0000))
    led_104_4.set_brightness(255)

    # menu: menu_104_5
    menu_104_5 = lv.obj(parent)
    objects["menu_104_5"] = menu_104_5
    menu_104_5.set_pos(596, 13)
    menu_104_5.set_size(112, 76)
    menu_104_5.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_104_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_104_5_title = lv.label(menu_104_5)
    menu_104_5_title.set_text("Menu")
    menu_104_5_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_104_5_item_1 = lv.button(menu_104_5)
    menu_104_5_item_1.set_width(lv.pct(100))
    menu_104_5_item_1_label = lv.label(menu_104_5_item_1)
    menu_104_5_item_1_label.set_text("Item 1")
    menu_104_5_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_104_5_item_2 = lv.button(menu_104_5)
    menu_104_5_item_2.set_width(lv.pct(100))
    menu_104_5_item_2_label = lv.label(menu_104_5_item_2)
    menu_104_5_item_2_label.set_text("Item 2")
    menu_104_5_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_104_5_item_3 = lv.button(menu_104_5)
    menu_104_5_item_3.set_width(lv.pct(100))
    menu_104_5_item_3_label = lv.label(menu_104_5_item_3)
    menu_104_5_item_3_label.set_text("Item 3")
    menu_104_5_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_104_5_item_4 = lv.button(menu_104_5)
    menu_104_5_item_4.set_width(lv.pct(100))
    menu_104_5_item_4_label = lv.label(menu_104_5_item_4)
    menu_104_5_item_4_label.set_text("Item 4")
    menu_104_5_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)


def random_104_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_104_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_104_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_104_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_104_get_current_page():
    return current_screen

def random_104_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_104_load_page(0)
