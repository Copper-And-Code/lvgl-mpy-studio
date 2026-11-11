"""
Auto-generated LVGL UI Code for MicroPython
Project: One chart
Generated: 2023-11-14T22:13:35.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_chart_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # chart: Chart_w15
    chart_w15 = lv.chart(parent)
    objects["chart_w15"] = chart_w15
    chart_w15.set_pos(65, 60)
    chart_w15.set_size(250, 150)
    chart_w15.set_type(lv.chart.TYPE.LINE)
    chart_w15.set_point_count(10)
    chart_w15.set_div_line_count(3, 5)
    chart_w15.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_w15.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_w15_series_1 = chart_w15.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_w15.set_next_value(chart_w15_series_1, 10)
    chart_w15.set_next_value(chart_w15_series_1, 20)
    chart_w15.set_next_value(chart_w15_series_1, 30)
    chart_w15.set_next_value(chart_w15_series_1, 25)
    chart_w15.set_next_value(chart_w15_series_1, 40)
    chart_w15.set_next_value(chart_w15_series_1, 35)
    chart_w15.set_next_value(chart_w15_series_1, 50)


def one_chart_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_chart_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_chart_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_chart_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_chart_get_current_page():
    return current_screen

def one_chart_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_chart_load_page(0)
