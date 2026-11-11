"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 126
Generated: 2023-11-14T22:15:58.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_126_4_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_126_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # calendar: calendar_126_0
    calendar_126_0 = lv.calendar(parent)
    objects["calendar_126_0"] = calendar_126_0
    calendar_126_0.set_pos(296, 356)
    calendar_126_0.set_size(182, 38)
    calendar_126_0.set_today_date(2026, 10, 28)
    calendar_126_0.set_month_shown(2026, 10)
    calendar_126_0_header = calendar_126_0.add_header_arrow()
    calendar_126_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # chart: chart_126_1
    chart_126_1 = lv.chart(parent)
    objects["chart_126_1"] = chart_126_1
    chart_126_1.set_pos(555, 396)
    chart_126_1.set_size(144, 99)
    chart_126_1.set_type(lv.chart.TYPE.LINE)
    chart_126_1.set_point_count(10)
    chart_126_1.set_div_line_count(3, 5)
    chart_126_1.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_126_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_126_1_series_1 = chart_126_1.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_126_1.set_next_value(chart_126_1_series_1, 10)
    chart_126_1.set_next_value(chart_126_1_series_1, 20)
    chart_126_1.set_next_value(chart_126_1_series_1, 30)
    chart_126_1.set_next_value(chart_126_1_series_1, 25)
    chart_126_1.set_next_value(chart_126_1_series_1, 40)
    chart_126_1.set_next_value(chart_126_1_series_1, 35)
    chart_126_1.set_next_value(chart_126_1_series_1, 50)

    # calendar: calendar_126_2
    calendar_126_2 = lv.calendar(parent)
    objects["calendar_126_2"] = calendar_126_2
    calendar_126_2.set_pos(254, 26)
    calendar_126_2.set_size(253, 135)
    calendar_126_2.set_today_date(2026, 10, 28)
    calendar_126_2.set_month_shown(2026, 10)
    calendar_126_2_header = calendar_126_2.add_header_arrow()
    calendar_126_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # line: line_126_3
    line_126_3 = lv.line(parent)
    objects["line_126_3"] = line_126_3
    line_126_3.set_pos(575, 55)
    line_126_3_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_126_3.set_points(line_126_3_points, 2)
    line_126_3.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_126_3.set_style_line_width(2, lv.PART.MAIN)

    # slider: slider_126_4
    slider_126_4 = lv.slider(parent)
    objects["slider_126_4"] = slider_126_4
    slider_126_4.set_pos(228, 255)
    slider_126_4.set_size(260, 144)
    slider_126_4.set_range(0, 100)
    slider_126_4.set_value(50, False)
    slider_126_4.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_126_4.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_126_4.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_126_4.add_event_cb(slider_126_4_changed, lv.EVENT.VALUE_CHANGED, None)

    # spinbox: spinbox_126_5
    spinbox_126_5 = lv.spinbox(parent)
    objects["spinbox_126_5"] = spinbox_126_5
    spinbox_126_5.set_pos(124, 267)
    spinbox_126_5.set_size(263, 68)
    spinbox_126_5.set_digit_format(4, 0)
    spinbox_126_5.set_range(0, 999)
    spinbox_126_5.set_value(0)
    spinbox_126_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_126_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_126_5.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_126_6
    buttonmatrix_126_6 = lv.buttonmatrix(parent)
    objects["buttonmatrix_126_6"] = buttonmatrix_126_6
    buttonmatrix_126_6.set_pos(148, 336)
    buttonmatrix_126_6.set_size(231, 65)
    buttonmatrix_126_6_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_126_6.set_map(buttonmatrix_126_6_map)
    buttonmatrix_126_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_126_6.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_126_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_126_6.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_126_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_126_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_126_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_126_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_126_get_current_page():
    return current_screen

def random_126_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_126_load_page(0)
