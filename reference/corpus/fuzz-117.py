"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 117
Generated: 2023-11-14T22:15:49.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_117_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # buttonmatrix: buttonmatrix_117_0
    buttonmatrix_117_0 = lv.buttonmatrix(parent)
    objects["buttonmatrix_117_0"] = buttonmatrix_117_0
    buttonmatrix_117_0.set_pos(269, 398)
    buttonmatrix_117_0.set_size(31, 142)
    buttonmatrix_117_0_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_117_0.set_map(buttonmatrix_117_0_map)
    buttonmatrix_117_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_117_0.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_117_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_117_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # spinner: spinner_117_1
    spinner_117_1 = lv.arc(parent)
    objects["spinner_117_1"] = spinner_117_1
    spinner_117_1.set_pos(423, 12)
    spinner_117_1.set_size(156, 13)
    spinner_117_1.set_bg_angles(0, 360)
    spinner_117_1.set_angles(0, 60)
    spinner_117_1.remove_style(None, lv.PART.KNOB)
    spinner_117_1.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_117_1_anim = lv.anim_t()
    spinner_117_1_anim.init()
    spinner_117_1_anim.set_var(spinner_117_1)
    spinner_117_1_anim.set_values(0, 360)
    spinner_117_1_anim.set_duration(1000)
    spinner_117_1_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_117_1_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_117_1_anim.set_custom_exec_cb(lambda _anim, value: spinner_117_1.set_rotation(value))
    spinner_117_1_anim.start()
    spinner_117_1.set_style_arc_width(8, lv.PART.MAIN)
    spinner_117_1.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_117_1.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # tileview: tileview_117_2
    tileview_117_2 = lv.tileview(parent)
    objects["tileview_117_2"] = tileview_117_2
    tileview_117_2.set_pos(320, 346)
    tileview_117_2.set_size(158, 122)
    tileview_117_2.add_tile(0, 0, lv.DIR.ALL)
    tileview_117_2.add_tile(1, 0, lv.DIR.ALL)
    tileview_117_2.add_tile(0, 1, lv.DIR.ALL)
    tileview_117_2.add_tile(1, 1, lv.DIR.ALL)
    tileview_117_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # roller: roller_117_3
    roller_117_3 = lv.roller(parent)
    objects["roller_117_3"] = roller_117_3
    roller_117_3.set_pos(653, 299)
    roller_117_3.set_size(62, 137)
    roller_117_3.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_117_3.set_visible_row_count(3)
    roller_117_3.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_117_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_117_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_117_3.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # calendar: calendar_117_4
    calendar_117_4 = lv.calendar(parent)
    objects["calendar_117_4"] = calendar_117_4
    calendar_117_4.set_pos(644, 57)
    calendar_117_4.set_size(38, 130)
    calendar_117_4.set_today_date(2026, 10, 28)
    calendar_117_4.set_month_shown(2026, 10)
    calendar_117_4_header = calendar_117_4.add_header_arrow()
    calendar_117_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # span: span_117_5
    span_117_5 = lv.spangroup(parent)
    objects["span_117_5"] = span_117_5
    span_117_5.set_pos(304, 277)
    span_117_5.set_size(134, 47)
    span_117_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_117_5_span_1 = span_117_5.add_span()
    span_117_5_span_1.set_text("Normal text")
    span_117_5_span_1_style = span_117_5_span_1.get_style()
    span_117_5_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_117_5_span_1_style.set_text_font(lv.font_montserrat_14)
    span_117_5_span_2 = span_117_5.add_span()
    span_117_5_span_2.set_text("Bold text")
    span_117_5_span_2_style = span_117_5_span_2.get_style()
    span_117_5_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_117_5_span_2_style.set_text_font(lv.font_montserrat_16)
    span_117_5_span_3 = span_117_5.add_span()
    span_117_5_span_3.set_text("Small text")
    span_117_5_span_3_style = span_117_5_span_3.get_style()
    span_117_5_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_117_5_span_3_style.set_text_font(lv.font_montserrat_14)
    span_117_5.refresh()

    # chart: chart_117_6
    chart_117_6 = lv.chart(parent)
    objects["chart_117_6"] = chart_117_6
    chart_117_6.set_pos(550, 111)
    chart_117_6.set_size(46, 41)
    chart_117_6.set_type(lv.chart.TYPE.LINE)
    chart_117_6.set_point_count(10)
    chart_117_6.set_div_line_count(3, 5)
    chart_117_6.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_117_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_117_6_series_1 = chart_117_6.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_117_6.set_next_value(chart_117_6_series_1, 10)
    chart_117_6.set_next_value(chart_117_6_series_1, 20)
    chart_117_6.set_next_value(chart_117_6_series_1, 30)
    chart_117_6.set_next_value(chart_117_6_series_1, 25)
    chart_117_6.set_next_value(chart_117_6_series_1, 40)
    chart_117_6.set_next_value(chart_117_6_series_1, 35)
    chart_117_6.set_next_value(chart_117_6_series_1, 50)


def random_117_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_117_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_117_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_117_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_117_get_current_page():
    return current_screen

def random_117_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_117_load_page(0)
