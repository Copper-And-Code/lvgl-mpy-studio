"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 26
Generated: 2023-11-14T22:14:18.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_26_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # textarea: textarea_26_0
    textarea_26_0 = lv.textarea(parent)
    objects["textarea_26_0"] = textarea_26_0
    textarea_26_0.set_pos(141, 33)
    textarea_26_0.set_size(24, 29)
    textarea_26_0.set_text("Testo 26:0 \" \\ Città")
    textarea_26_0.set_placeholder_text("Type here")
    textarea_26_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_26_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_26_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # chart: chart_26_1
    chart_26_1 = lv.chart(parent)
    objects["chart_26_1"] = chart_26_1
    chart_26_1.set_pos(593, 248)
    chart_26_1.set_size(199, 36)
    chart_26_1.set_type(lv.chart.TYPE.LINE)
    chart_26_1.set_point_count(10)
    chart_26_1.set_div_line_count(3, 5)
    chart_26_1.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_26_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_26_1_series_1 = chart_26_1.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_26_1.set_next_value(chart_26_1_series_1, 10)
    chart_26_1.set_next_value(chart_26_1_series_1, 20)
    chart_26_1.set_next_value(chart_26_1_series_1, 30)
    chart_26_1.set_next_value(chart_26_1_series_1, 25)
    chart_26_1.set_next_value(chart_26_1_series_1, 40)
    chart_26_1.set_next_value(chart_26_1_series_1, 35)
    chart_26_1.set_next_value(chart_26_1_series_1, 50)


def random_26_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_26_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_26_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_26_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_26_get_current_page():
    return current_screen

def random_26_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_26_load_page(0)
