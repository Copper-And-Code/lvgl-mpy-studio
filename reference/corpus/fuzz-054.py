"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 54
Generated: 2023-11-14T22:14:46.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_54_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: win_54_0
    win_54_0 = lv.obj(parent)
    objects["win_54_0"] = win_54_0
    win_54_0.set_pos(417, 362)
    win_54_0.set_size(149, 91)
    win_54_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_54_0.set_style_pad_all(0, lv.PART.MAIN)
    win_54_0.set_style_pad_row(0, lv.PART.MAIN)
    win_54_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_54_0_header = lv.obj(win_54_0)
    win_54_0_header.set_size(lv.pct(100), 40)
    win_54_0_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_54_0_header.set_style_radius(0, lv.PART.MAIN)
    win_54_0_title = lv.label(win_54_0_header)
    win_54_0_title.set_text("Window Title")
    win_54_0_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_54_0_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_54_0_content = lv.obj(win_54_0)
    win_54_0_content.set_width(lv.pct(100))
    win_54_0_content.set_flex_grow(1)

    # led: led_54_1
    led_54_1 = lv.led(parent)
    objects["led_54_1"] = led_54_1
    led_54_1.set_pos(589, 6)
    led_54_1.set_size(194, 79)
    led_54_1.set_color(lv.color_hex(0xFF0000))
    led_54_1.set_brightness(255)

    # switch: switch_54_2
    switch_54_2 = lv.switch(parent)
    objects["switch_54_2"] = switch_54_2
    switch_54_2.set_pos(331, 157)
    switch_54_2.set_size(141, 55)
    switch_54_2.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_54_2.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_54_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # chart: chart_54_3
    chart_54_3 = lv.chart(parent)
    objects["chart_54_3"] = chart_54_3
    chart_54_3.set_pos(242, 76)
    chart_54_3.set_size(57, 70)
    chart_54_3.set_type(lv.chart.TYPE.LINE)
    chart_54_3.set_point_count(10)
    chart_54_3.set_div_line_count(3, 5)
    chart_54_3.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_54_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_54_3_series_1 = chart_54_3.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_54_3.set_next_value(chart_54_3_series_1, 10)
    chart_54_3.set_next_value(chart_54_3_series_1, 20)
    chart_54_3.set_next_value(chart_54_3_series_1, 30)
    chart_54_3.set_next_value(chart_54_3_series_1, 25)
    chart_54_3.set_next_value(chart_54_3_series_1, 40)
    chart_54_3.set_next_value(chart_54_3_series_1, 35)
    chart_54_3.set_next_value(chart_54_3_series_1, 50)

    # calendar: calendar_54_4
    calendar_54_4 = lv.calendar(parent)
    objects["calendar_54_4"] = calendar_54_4
    calendar_54_4.set_pos(69, 319)
    calendar_54_4.set_size(38, 126)
    calendar_54_4.set_today_date(2026, 10, 28)
    calendar_54_4.set_month_shown(2026, 10)
    calendar_54_4_header = calendar_54_4.add_header_arrow()
    calendar_54_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # image: image_54_5
    image_54_5 = lv.image(parent)
    objects["image_54_5"] = image_54_5
    image_54_5.set_pos(301, 180)
    image_54_5.set_size(238, 61)

    # led: led_54_6
    led_54_6 = lv.led(parent)
    objects["led_54_6"] = led_54_6
    led_54_6.set_pos(409, 131)
    led_54_6.set_size(142, 61)
    led_54_6.set_color(lv.color_hex(0xFF0000))
    led_54_6.set_brightness(255)


def random_54_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_54_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_54_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_54_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_54_get_current_page():
    return current_screen

def random_54_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_54_load_page(0)
