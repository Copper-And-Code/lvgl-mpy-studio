"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 101
Generated: 2023-11-14T22:15:33.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_101_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # chart: chart_101_0
    chart_101_0 = lv.chart(parent)
    objects["chart_101_0"] = chart_101_0
    chart_101_0.set_pos(442, 323)
    chart_101_0.set_size(246, 54)
    chart_101_0.set_type(lv.chart.TYPE.LINE)
    chart_101_0.set_point_count(10)
    chart_101_0.set_div_line_count(3, 5)
    chart_101_0.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_101_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_101_0_series_1 = chart_101_0.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_101_0.set_next_value(chart_101_0_series_1, 10)
    chart_101_0.set_next_value(chart_101_0_series_1, 20)
    chart_101_0.set_next_value(chart_101_0_series_1, 30)
    chart_101_0.set_next_value(chart_101_0_series_1, 25)
    chart_101_0.set_next_value(chart_101_0_series_1, 40)
    chart_101_0.set_next_value(chart_101_0_series_1, 35)
    chart_101_0.set_next_value(chart_101_0_series_1, 50)

    # led: led_101_1
    led_101_1 = lv.led(parent)
    objects["led_101_1"] = led_101_1
    led_101_1.set_pos(656, 149)
    led_101_1.set_size(98, 153)
    led_101_1.set_color(lv.color_hex(0xFF0000))
    led_101_1.set_brightness(255)

    # switch: switch_101_2
    switch_101_2 = lv.switch(parent)
    objects["switch_101_2"] = switch_101_2
    switch_101_2.set_pos(640, 168)
    switch_101_2.set_size(107, 34)
    switch_101_2.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_101_2.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_101_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)


def random_101_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_101_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_101_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_101_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_101_get_current_page():
    return current_screen

def random_101_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_101_load_page(0)
