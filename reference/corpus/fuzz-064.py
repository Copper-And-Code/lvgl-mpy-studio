"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 64
Generated: 2023-11-14T22:14:56.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_64_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # span: span_64_0
    span_64_0 = lv.spangroup(parent)
    objects["span_64_0"] = span_64_0
    span_64_0.set_pos(308, 174)
    span_64_0.set_size(234, 17)
    span_64_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_64_0_span_1 = span_64_0.add_span()
    span_64_0_span_1.set_text("Normal text")
    span_64_0_span_1_style = span_64_0_span_1.get_style()
    span_64_0_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_64_0_span_1_style.set_text_font(lv.font_montserrat_14)
    span_64_0_span_2 = span_64_0.add_span()
    span_64_0_span_2.set_text("Bold text")
    span_64_0_span_2_style = span_64_0_span_2.get_style()
    span_64_0_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_64_0_span_2_style.set_text_font(lv.font_montserrat_16)
    span_64_0_span_3 = span_64_0.add_span()
    span_64_0_span_3.set_text("Small text")
    span_64_0_span_3_style = span_64_0_span_3.get_style()
    span_64_0_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_64_0_span_3_style.set_text_font(lv.font_montserrat_14)
    span_64_0.refresh()

    # chart: chart_64_1
    chart_64_1 = lv.chart(parent)
    objects["chart_64_1"] = chart_64_1
    chart_64_1.set_pos(523, 133)
    chart_64_1.set_size(109, 122)
    chart_64_1.set_type(lv.chart.TYPE.LINE)
    chart_64_1.set_point_count(10)
    chart_64_1.set_div_line_count(3, 5)
    chart_64_1.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_64_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_64_1_series_1 = chart_64_1.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_64_1.set_next_value(chart_64_1_series_1, 10)
    chart_64_1.set_next_value(chart_64_1_series_1, 20)
    chart_64_1.set_next_value(chart_64_1_series_1, 30)
    chart_64_1.set_next_value(chart_64_1_series_1, 25)
    chart_64_1.set_next_value(chart_64_1_series_1, 40)
    chart_64_1.set_next_value(chart_64_1_series_1, 35)
    chart_64_1.set_next_value(chart_64_1_series_1, 50)

    # line: line_64_2
    line_64_2 = lv.line(parent)
    objects["line_64_2"] = line_64_2
    line_64_2.set_pos(425, 52)
    line_64_2_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_64_2.set_points(line_64_2_points, 2)
    line_64_2.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_64_2.set_style_line_width(2, lv.PART.MAIN)

    # led: led_64_3
    led_64_3 = lv.led(parent)
    objects["led_64_3"] = led_64_3
    led_64_3.set_pos(129, 395)
    led_64_3.set_size(160, 73)
    led_64_3.set_color(lv.color_hex(0xFF0000))
    led_64_3.set_brightness(255)

    # label: label_64_4
    label_64_4 = lv.label(parent)
    objects["label_64_4"] = label_64_4
    label_64_4.set_pos(550, 181)
    label_64_4.set_size(91, 45)
    label_64_4.set_text("Testo 64:4 \" \\ Città")
    label_64_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_64_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_64_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # spinner: spinner_64_5
    spinner_64_5 = lv.arc(parent)
    objects["spinner_64_5"] = spinner_64_5
    spinner_64_5.set_pos(572, 391)
    spinner_64_5.set_size(147, 112)
    spinner_64_5.set_bg_angles(0, 360)
    spinner_64_5.set_angles(0, 60)
    spinner_64_5.remove_style(None, lv.PART.KNOB)
    spinner_64_5.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_64_5_anim = lv.anim_t()
    spinner_64_5_anim.init()
    spinner_64_5_anim.set_var(spinner_64_5)
    spinner_64_5_anim.set_values(0, 360)
    spinner_64_5_anim.set_duration(1000)
    spinner_64_5_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_64_5_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_64_5_anim.set_custom_exec_cb(lambda _anim, value: spinner_64_5.set_rotation(value))
    spinner_64_5_anim.start()
    spinner_64_5.set_style_arc_width(8, lv.PART.MAIN)
    spinner_64_5.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_64_5.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_64_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_64_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_64_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_64_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_64_get_current_page():
    return current_screen

def random_64_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_64_load_page(0)
