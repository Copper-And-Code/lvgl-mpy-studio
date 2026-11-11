"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 106
Generated: 2023-11-14T22:15:38.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_106_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # calendar: calendar_106_0
    calendar_106_0 = lv.calendar(parent)
    objects["calendar_106_0"] = calendar_106_0
    calendar_106_0.set_pos(355, 197)
    calendar_106_0.set_size(35, 110)
    calendar_106_0.set_today_date(2026, 10, 28)
    calendar_106_0.set_month_shown(2026, 10)
    calendar_106_0_header = calendar_106_0.add_header_arrow()
    calendar_106_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # table: table_106_1
    table_106_1 = lv.table(parent)
    objects["table_106_1"] = table_106_1
    table_106_1.set_pos(317, 143)
    table_106_1.set_size(126, 49)
    table_106_1.set_column_count(3)
    table_106_1.set_column_width(0, 100)
    table_106_1.set_column_width(1, 100)
    table_106_1.set_column_width(2, 100)
    table_106_1.set_cell_value(0, 0, "Col 1")
    table_106_1.set_cell_value(0, 1, "Col 2")
    table_106_1.set_cell_value(0, 2, "Col 3")
    table_106_1.set_cell_value(1, 0, "A1")
    table_106_1.set_cell_value(1, 1, "B1")
    table_106_1.set_cell_value(1, 2, "C1")
    table_106_1.set_cell_value(2, 0, "A2")
    table_106_1.set_cell_value(2, 1, "B2")
    table_106_1.set_cell_value(2, 2, "C2")
    table_106_1.set_cell_value(3, 0, "A3")
    table_106_1.set_cell_value(3, 1, "B3")
    table_106_1.set_cell_value(3, 2, "C3")
    table_106_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_106_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_106_1.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_106_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # line: line_106_2
    line_106_2 = lv.line(parent)
    objects["line_106_2"] = line_106_2
    line_106_2.set_pos(438, 93)
    line_106_2_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_106_2.set_points(line_106_2_points, 2)
    line_106_2.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_106_2.set_style_line_width(2, lv.PART.MAIN)

    # scale: scale_106_3
    scale_106_3 = lv.scale(parent)
    objects["scale_106_3"] = scale_106_3
    scale_106_3.set_pos(595, 373)
    scale_106_3.set_size(97, 79)
    scale_106_3.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_106_3.set_range(0, 100)
    scale_106_3.set_total_tick_count(51)
    scale_106_3.set_major_tick_every(5)
    scale_106_3.set_style_length(15, lv.PART.INDICATOR)
    scale_106_3.set_style_length(8, lv.PART.ITEMS)
    scale_106_3.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_106_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # span: span_106_4
    span_106_4 = lv.spangroup(parent)
    objects["span_106_4"] = span_106_4
    span_106_4.set_pos(96, 267)
    span_106_4.set_size(74, 131)
    span_106_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_106_4_span_1 = span_106_4.add_span()
    span_106_4_span_1.set_text("Normal text")
    span_106_4_span_1_style = span_106_4_span_1.get_style()
    span_106_4_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_106_4_span_1_style.set_text_font(lv.font_montserrat_14)
    span_106_4_span_2 = span_106_4.add_span()
    span_106_4_span_2.set_text("Bold text")
    span_106_4_span_2_style = span_106_4_span_2.get_style()
    span_106_4_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_106_4_span_2_style.set_text_font(lv.font_montserrat_16)
    span_106_4_span_3 = span_106_4.add_span()
    span_106_4_span_3.set_text("Small text")
    span_106_4_span_3_style = span_106_4_span_3.get_style()
    span_106_4_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_106_4_span_3_style.set_text_font(lv.font_montserrat_14)
    span_106_4.refresh()

    # chart: chart_106_5
    chart_106_5 = lv.chart(parent)
    objects["chart_106_5"] = chart_106_5
    chart_106_5.set_pos(462, 177)
    chart_106_5.set_size(121, 51)
    chart_106_5.set_type(lv.chart.TYPE.LINE)
    chart_106_5.set_point_count(10)
    chart_106_5.set_div_line_count(3, 5)
    chart_106_5.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_106_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_106_5_series_1 = chart_106_5.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_106_5.set_next_value(chart_106_5_series_1, 10)
    chart_106_5.set_next_value(chart_106_5_series_1, 20)
    chart_106_5.set_next_value(chart_106_5_series_1, 30)
    chart_106_5.set_next_value(chart_106_5_series_1, 25)
    chart_106_5.set_next_value(chart_106_5_series_1, 40)
    chart_106_5.set_next_value(chart_106_5_series_1, 35)
    chart_106_5.set_next_value(chart_106_5_series_1, 50)

    # switch: switch_106_6
    switch_106_6 = lv.switch(parent)
    objects["switch_106_6"] = switch_106_6
    switch_106_6.set_pos(219, 191)
    switch_106_6.set_size(246, 109)
    switch_106_6.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_106_6.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_106_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)


def random_106_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_106_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_106_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_106_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_106_get_current_page():
    return current_screen

def random_106_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_106_load_page(0)
