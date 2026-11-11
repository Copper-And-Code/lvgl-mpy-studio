"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 189
Generated: 2023-11-14T22:17:01.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_189_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # line: line_189_0
    line_189_0 = lv.line(parent)
    objects["line_189_0"] = line_189_0
    line_189_0.set_pos(502, 107)
    line_189_0_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_189_0.set_points(line_189_0_points, 2)
    line_189_0.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_189_0.set_style_line_width(2, lv.PART.MAIN)

    # chart: chart_189_1
    chart_189_1 = lv.chart(parent)
    objects["chart_189_1"] = chart_189_1
    chart_189_1.set_pos(691, 316)
    chart_189_1.set_size(79, 119)
    chart_189_1.set_type(lv.chart.TYPE.LINE)
    chart_189_1.set_point_count(10)
    chart_189_1.set_div_line_count(3, 5)
    chart_189_1.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_189_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_189_1_series_1 = chart_189_1.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_189_1.set_next_value(chart_189_1_series_1, 10)
    chart_189_1.set_next_value(chart_189_1_series_1, 20)
    chart_189_1.set_next_value(chart_189_1_series_1, 30)
    chart_189_1.set_next_value(chart_189_1_series_1, 25)
    chart_189_1.set_next_value(chart_189_1_series_1, 40)
    chart_189_1.set_next_value(chart_189_1_series_1, 35)
    chart_189_1.set_next_value(chart_189_1_series_1, 50)

    # span: span_189_2
    span_189_2 = lv.spangroup(parent)
    objects["span_189_2"] = span_189_2
    span_189_2.set_pos(289, 314)
    span_189_2.set_size(58, 71)
    span_189_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_189_2_span_1 = span_189_2.add_span()
    span_189_2_span_1.set_text("Normal text")
    span_189_2_span_1_style = span_189_2_span_1.get_style()
    span_189_2_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_189_2_span_1_style.set_text_font(lv.font_montserrat_14)
    span_189_2_span_2 = span_189_2.add_span()
    span_189_2_span_2.set_text("Bold text")
    span_189_2_span_2_style = span_189_2_span_2.get_style()
    span_189_2_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_189_2_span_2_style.set_text_font(lv.font_montserrat_16)
    span_189_2_span_3 = span_189_2.add_span()
    span_189_2_span_3.set_text("Small text")
    span_189_2_span_3_style = span_189_2_span_3.get_style()
    span_189_2_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_189_2_span_3_style.set_text_font(lv.font_montserrat_14)
    span_189_2.refresh()

    # panel: panel_189_3
    panel_189_3 = lv.obj(parent)
    objects["panel_189_3"] = panel_189_3
    panel_189_3.set_pos(274, 322)
    panel_189_3.set_size(109, 25)
    panel_189_3.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_189_3.set_style_border_width(2, lv.PART.MAIN)
    panel_189_3.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_189_3.set_style_radius(5, lv.PART.MAIN)
    panel_189_3.set_style_pad_all(0, lv.PART.MAIN)
    panel_189_3.set_style_pad_gap(0, lv.PART.MAIN)

    # calendar: calendar_189_4
    calendar_189_4 = lv.calendar(parent)
    objects["calendar_189_4"] = calendar_189_4
    calendar_189_4.set_pos(134, 41)
    calendar_189_4.set_size(223, 18)
    calendar_189_4.set_today_date(2026, 10, 28)
    calendar_189_4.set_month_shown(2026, 10)
    calendar_189_4_header = calendar_189_4.add_header_arrow()
    calendar_189_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # roller: roller_189_5
    roller_189_5 = lv.roller(parent)
    objects["roller_189_5"] = roller_189_5
    roller_189_5.set_pos(44, 370)
    roller_189_5.set_size(250, 34)
    roller_189_5.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_189_5.set_visible_row_count(3)
    roller_189_5.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_189_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_189_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_189_5.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_189_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_189_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_189_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_189_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_189_get_current_page():
    return current_screen

def random_189_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_189_load_page(0)
