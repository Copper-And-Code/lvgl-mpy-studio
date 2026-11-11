"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 33
Generated: 2023-11-14T22:14:25.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_33_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # keyboard: keyboard_33_0
    keyboard_33_0 = lv.keyboard(parent)
    objects["keyboard_33_0"] = keyboard_33_0
    keyboard_33_0.set_pos(571, 114)
    keyboard_33_0.set_size(96, 76)

    # chart: chart_33_1
    chart_33_1 = lv.chart(parent)
    objects["chart_33_1"] = chart_33_1
    chart_33_1.set_pos(691, 50)
    chart_33_1.set_size(213, 123)
    chart_33_1.set_type(lv.chart.TYPE.LINE)
    chart_33_1.set_point_count(10)
    chart_33_1.set_div_line_count(3, 5)
    chart_33_1.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_33_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_33_1_series_1 = chart_33_1.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_33_1.set_next_value(chart_33_1_series_1, 10)
    chart_33_1.set_next_value(chart_33_1_series_1, 20)
    chart_33_1.set_next_value(chart_33_1_series_1, 30)
    chart_33_1.set_next_value(chart_33_1_series_1, 25)
    chart_33_1.set_next_value(chart_33_1_series_1, 40)
    chart_33_1.set_next_value(chart_33_1_series_1, 35)
    chart_33_1.set_next_value(chart_33_1_series_1, 50)

    # menu: menu_33_2
    menu_33_2 = lv.obj(parent)
    objects["menu_33_2"] = menu_33_2
    menu_33_2.set_pos(222, 325)
    menu_33_2.set_size(169, 38)
    menu_33_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_33_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_33_2_title = lv.label(menu_33_2)
    menu_33_2_title.set_text("Menu")
    menu_33_2_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_33_2_item_1 = lv.button(menu_33_2)
    menu_33_2_item_1.set_width(lv.pct(100))
    menu_33_2_item_1_label = lv.label(menu_33_2_item_1)
    menu_33_2_item_1_label.set_text("Item 1")
    menu_33_2_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_33_2_item_2 = lv.button(menu_33_2)
    menu_33_2_item_2.set_width(lv.pct(100))
    menu_33_2_item_2_label = lv.label(menu_33_2_item_2)
    menu_33_2_item_2_label.set_text("Item 2")
    menu_33_2_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_33_2_item_3 = lv.button(menu_33_2)
    menu_33_2_item_3.set_width(lv.pct(100))
    menu_33_2_item_3_label = lv.label(menu_33_2_item_3)
    menu_33_2_item_3_label.set_text("Item 3")
    menu_33_2_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_33_2_item_4 = lv.button(menu_33_2)
    menu_33_2_item_4.set_width(lv.pct(100))
    menu_33_2_item_4_label = lv.label(menu_33_2_item_4)
    menu_33_2_item_4_label.set_text("Item 4")
    menu_33_2_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # arc: arc_33_3
    arc_33_3 = lv.arc(parent)
    objects["arc_33_3"] = arc_33_3
    arc_33_3.set_pos(370, 345)
    arc_33_3.set_size(30, 156)
    arc_33_3.set_bg_angles(135, 45)
    arc_33_3.set_range(0, 100)
    arc_33_3.set_value(50)
    arc_33_3.set_style_arc_width(10, lv.PART.MAIN)
    arc_33_3.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_33_3.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_33_3.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_33_3.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # span: span_33_4
    span_33_4 = lv.spangroup(parent)
    objects["span_33_4"] = span_33_4
    span_33_4.set_pos(235, 345)
    span_33_4.set_size(36, 146)
    span_33_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_33_4_span_1 = span_33_4.add_span()
    span_33_4_span_1.set_text("Normal text")
    span_33_4_span_1_style = span_33_4_span_1.get_style()
    span_33_4_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_33_4_span_1_style.set_text_font(lv.font_montserrat_14)
    span_33_4_span_2 = span_33_4.add_span()
    span_33_4_span_2.set_text("Bold text")
    span_33_4_span_2_style = span_33_4_span_2.get_style()
    span_33_4_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_33_4_span_2_style.set_text_font(lv.font_montserrat_16)
    span_33_4_span_3 = span_33_4.add_span()
    span_33_4_span_3.set_text("Small text")
    span_33_4_span_3_style = span_33_4_span_3.get_style()
    span_33_4_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_33_4_span_3_style.set_text_font(lv.font_montserrat_14)
    span_33_4.refresh()

    # arc: arc_33_5
    arc_33_5 = lv.arc(parent)
    objects["arc_33_5"] = arc_33_5
    arc_33_5.set_pos(242, 185)
    arc_33_5.set_size(27, 22)
    arc_33_5.set_bg_angles(135, 45)
    arc_33_5.set_range(0, 100)
    arc_33_5.set_value(50)
    arc_33_5.set_style_arc_width(10, lv.PART.MAIN)
    arc_33_5.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_33_5.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_33_5.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_33_5.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # chart: chart_33_6
    chart_33_6 = lv.chart(parent)
    objects["chart_33_6"] = chart_33_6
    chart_33_6.set_pos(565, 115)
    chart_33_6.set_size(46, 120)
    chart_33_6.set_type(lv.chart.TYPE.LINE)
    chart_33_6.set_point_count(10)
    chart_33_6.set_div_line_count(3, 5)
    chart_33_6.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_33_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_33_6_series_1 = chart_33_6.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_33_6.set_next_value(chart_33_6_series_1, 10)
    chart_33_6.set_next_value(chart_33_6_series_1, 20)
    chart_33_6.set_next_value(chart_33_6_series_1, 30)
    chart_33_6.set_next_value(chart_33_6_series_1, 25)
    chart_33_6.set_next_value(chart_33_6_series_1, 40)
    chart_33_6.set_next_value(chart_33_6_series_1, 35)
    chart_33_6.set_next_value(chart_33_6_series_1, 50)

    # scale: scale_33_7
    scale_33_7 = lv.scale(parent)
    objects["scale_33_7"] = scale_33_7
    scale_33_7.set_pos(356, 112)
    scale_33_7.set_size(163, 14)
    scale_33_7.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_33_7.set_range(0, 100)
    scale_33_7.set_total_tick_count(51)
    scale_33_7.set_major_tick_every(5)
    scale_33_7.set_style_length(15, lv.PART.INDICATOR)
    scale_33_7.set_style_length(8, lv.PART.ITEMS)
    scale_33_7.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_33_7.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)


def random_33_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_33_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_33_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_33_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_33_get_current_page():
    return current_screen

def random_33_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_33_load_page(0)
