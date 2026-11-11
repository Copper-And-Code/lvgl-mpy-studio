"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 21
Generated: 2023-11-14T22:14:13.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_21_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # chart: chart_21_0
    chart_21_0 = lv.chart(parent)
    objects["chart_21_0"] = chart_21_0
    chart_21_0.set_pos(264, 350)
    chart_21_0.set_size(249, 123)
    chart_21_0.set_type(lv.chart.TYPE.LINE)
    chart_21_0.set_point_count(10)
    chart_21_0.set_div_line_count(3, 5)
    chart_21_0.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_21_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_21_0_series_1 = chart_21_0.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_21_0.set_next_value(chart_21_0_series_1, 10)
    chart_21_0.set_next_value(chart_21_0_series_1, 20)
    chart_21_0.set_next_value(chart_21_0_series_1, 30)
    chart_21_0.set_next_value(chart_21_0_series_1, 25)
    chart_21_0.set_next_value(chart_21_0_series_1, 40)
    chart_21_0.set_next_value(chart_21_0_series_1, 35)
    chart_21_0.set_next_value(chart_21_0_series_1, 50)

    # scale: scale_21_1
    scale_21_1 = lv.scale(parent)
    objects["scale_21_1"] = scale_21_1
    scale_21_1.set_pos(82, 37)
    scale_21_1.set_size(152, 115)
    scale_21_1.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_21_1.set_range(0, 100)
    scale_21_1.set_total_tick_count(51)
    scale_21_1.set_major_tick_every(5)
    scale_21_1.set_style_length(15, lv.PART.INDICATOR)
    scale_21_1.set_style_length(8, lv.PART.ITEMS)
    scale_21_1.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_21_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)


def random_21_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_21_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_21_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_21_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_21_get_current_page():
    return current_screen

def random_21_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_21_load_page(0)
