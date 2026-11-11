"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 125
Generated: 2023-11-14T22:15:57.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def checkbox_125_2_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_125_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # chart: chart_125_0
    chart_125_0 = lv.chart(parent)
    objects["chart_125_0"] = chart_125_0
    chart_125_0.set_pos(97, 65)
    chart_125_0.set_size(92, 26)
    chart_125_0.set_type(lv.chart.TYPE.LINE)
    chart_125_0.set_point_count(10)
    chart_125_0.set_div_line_count(3, 5)
    chart_125_0.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_125_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_125_0_series_1 = chart_125_0.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_125_0.set_next_value(chart_125_0_series_1, 10)
    chart_125_0.set_next_value(chart_125_0_series_1, 20)
    chart_125_0.set_next_value(chart_125_0_series_1, 30)
    chart_125_0.set_next_value(chart_125_0_series_1, 25)
    chart_125_0.set_next_value(chart_125_0_series_1, 40)
    chart_125_0.set_next_value(chart_125_0_series_1, 35)
    chart_125_0.set_next_value(chart_125_0_series_1, 50)

    # bar: bar_125_1
    bar_125_1 = lv.bar(parent)
    objects["bar_125_1"] = bar_125_1
    bar_125_1.set_pos(4, 217)
    bar_125_1.set_size(142, 65)
    bar_125_1.set_range(0, 100)
    bar_125_1.set_value(50, False)
    bar_125_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_125_1.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # checkbox: checkbox_125_2
    checkbox_125_2 = lv.checkbox(parent)
    objects["checkbox_125_2"] = checkbox_125_2
    checkbox_125_2.set_pos(535, 131)
    checkbox_125_2.set_text("Testo 125:2 \" \\ Città")
    checkbox_125_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_125_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_125_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_125_2.add_event_cb(checkbox_125_2_changed, lv.EVENT.VALUE_CHANGED, None)

    # checkbox: checkbox_125_3
    checkbox_125_3 = lv.checkbox(parent)
    objects["checkbox_125_3"] = checkbox_125_3
    checkbox_125_3.set_pos(215, 345)
    checkbox_125_3.set_text("Testo 125:3 \" \\ Città")
    checkbox_125_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_125_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_125_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # led: led_125_4
    led_125_4 = lv.led(parent)
    objects["led_125_4"] = led_125_4
    led_125_4.set_pos(582, 130)
    led_125_4.set_size(52, 99)
    led_125_4.set_color(lv.color_hex(0xFF0000))
    led_125_4.set_brightness(255)


def random_125_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_125_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_125_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_125_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_125_get_current_page():
    return current_screen

def random_125_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_125_load_page(0)
