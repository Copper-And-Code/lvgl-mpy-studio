"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 108
Generated: 2023-11-14T22:15:40.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_108_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # calendar: calendar_108_0
    calendar_108_0 = lv.calendar(parent)
    objects["calendar_108_0"] = calendar_108_0
    calendar_108_0.set_pos(494, 244)
    calendar_108_0.set_size(41, 104)
    calendar_108_0.set_today_date(2026, 10, 28)
    calendar_108_0.set_month_shown(2026, 10)
    calendar_108_0_header = calendar_108_0.add_header_arrow()
    calendar_108_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # chart: chart_108_1
    chart_108_1 = lv.chart(parent)
    objects["chart_108_1"] = chart_108_1
    chart_108_1.set_pos(664, 312)
    chart_108_1.set_size(233, 40)
    chart_108_1.set_type(lv.chart.TYPE.LINE)
    chart_108_1.set_point_count(10)
    chart_108_1.set_div_line_count(3, 5)
    chart_108_1.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_108_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_108_1_series_1 = chart_108_1.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_108_1.set_next_value(chart_108_1_series_1, 10)
    chart_108_1.set_next_value(chart_108_1_series_1, 20)
    chart_108_1.set_next_value(chart_108_1_series_1, 30)
    chart_108_1.set_next_value(chart_108_1_series_1, 25)
    chart_108_1.set_next_value(chart_108_1_series_1, 40)
    chart_108_1.set_next_value(chart_108_1_series_1, 35)
    chart_108_1.set_next_value(chart_108_1_series_1, 50)


def random_108_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_108_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_108_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_108_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_108_get_current_page():
    return current_screen

def random_108_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_108_load_page(0)
