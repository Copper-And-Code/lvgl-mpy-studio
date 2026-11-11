"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 53
Generated: 2023-11-14T22:14:45.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_53_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # chart: chart_53_0
    chart_53_0 = lv.chart(parent)
    objects["chart_53_0"] = chart_53_0
    chart_53_0.set_pos(639, 248)
    chart_53_0.set_size(239, 151)
    chart_53_0.set_type(lv.chart.TYPE.LINE)
    chart_53_0.set_point_count(10)
    chart_53_0.set_div_line_count(3, 5)
    chart_53_0.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_53_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_53_0_series_1 = chart_53_0.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_53_0.set_next_value(chart_53_0_series_1, 10)
    chart_53_0.set_next_value(chart_53_0_series_1, 20)
    chart_53_0.set_next_value(chart_53_0_series_1, 30)
    chart_53_0.set_next_value(chart_53_0_series_1, 25)
    chart_53_0.set_next_value(chart_53_0_series_1, 40)
    chart_53_0.set_next_value(chart_53_0_series_1, 35)
    chart_53_0.set_next_value(chart_53_0_series_1, 50)

    # win: win_53_1
    win_53_1 = lv.obj(parent)
    objects["win_53_1"] = win_53_1
    win_53_1.set_pos(614, 101)
    win_53_1.set_size(103, 15)
    win_53_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_53_1.set_style_pad_all(0, lv.PART.MAIN)
    win_53_1.set_style_pad_row(0, lv.PART.MAIN)
    win_53_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_53_1_header = lv.obj(win_53_1)
    win_53_1_header.set_size(lv.pct(100), 40)
    win_53_1_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_53_1_header.set_style_radius(0, lv.PART.MAIN)
    win_53_1_title = lv.label(win_53_1_header)
    win_53_1_title.set_text("Window Title")
    win_53_1_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_53_1_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_53_1_content = lv.obj(win_53_1)
    win_53_1_content.set_width(lv.pct(100))
    win_53_1_content.set_flex_grow(1)

    # calendar: calendar_53_2
    calendar_53_2 = lv.calendar(parent)
    objects["calendar_53_2"] = calendar_53_2
    calendar_53_2.set_pos(152, 169)
    calendar_53_2.set_size(230, 65)
    calendar_53_2.set_today_date(2026, 10, 28)
    calendar_53_2.set_month_shown(2026, 10)
    calendar_53_2_header = calendar_53_2.add_header_arrow()
    calendar_53_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # list: list_53_3
    list_53_3 = lv.obj(parent)
    objects["list_53_3"] = list_53_3
    list_53_3.set_pos(50, 108)
    list_53_3.set_size(232, 64)
    list_53_3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_53_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_53_3_item_1 = lv.button(list_53_3)
    list_53_3_item_1.set_width(lv.pct(100))
    list_53_3_item_1_label = lv.label(list_53_3_item_1)
    list_53_3_item_1_label.set_text("Item 1")
    list_53_3_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_53_3_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_53_3_item_2 = lv.button(list_53_3)
    list_53_3_item_2.set_width(lv.pct(100))
    list_53_3_item_2_label = lv.label(list_53_3_item_2)
    list_53_3_item_2_label.set_text("Item 2")
    list_53_3_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_53_3_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_53_3_item_3 = lv.button(list_53_3)
    list_53_3_item_3.set_width(lv.pct(100))
    list_53_3_item_3_label = lv.label(list_53_3_item_3)
    list_53_3_item_3_label.set_text("Item 3")
    list_53_3_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_53_3_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_53_3_item_4 = lv.button(list_53_3)
    list_53_3_item_4.set_width(lv.pct(100))
    list_53_3_item_4_label = lv.label(list_53_3_item_4)
    list_53_3_item_4_label.set_text("Item 4")
    list_53_3_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_53_3_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_53_3_item_5 = lv.button(list_53_3)
    list_53_3_item_5.set_width(lv.pct(100))
    list_53_3_item_5_label = lv.label(list_53_3_item_5)
    list_53_3_item_5_label.set_text("Item 5")
    list_53_3_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_53_3_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # spinbox: spinbox_53_4
    spinbox_53_4 = lv.spinbox(parent)
    objects["spinbox_53_4"] = spinbox_53_4
    spinbox_53_4.set_pos(242, 130)
    spinbox_53_4.set_size(221, 44)
    spinbox_53_4.set_digit_format(4, 0)
    spinbox_53_4.set_range(0, 999)
    spinbox_53_4.set_value(0)
    spinbox_53_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_53_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_53_4.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # led: led_53_5
    led_53_5 = lv.led(parent)
    objects["led_53_5"] = led_53_5
    led_53_5.set_pos(192, 220)
    led_53_5.set_size(150, 112)
    led_53_5.set_color(lv.color_hex(0xFF0000))
    led_53_5.set_brightness(255)

    # line: line_53_6
    line_53_6 = lv.line(parent)
    objects["line_53_6"] = line_53_6
    line_53_6.set_pos(482, 43)
    line_53_6_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_53_6.set_points(line_53_6_points, 2)
    line_53_6.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_53_6.set_style_line_width(2, lv.PART.MAIN)


def random_53_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_53_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_53_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_53_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_53_get_current_page():
    return current_screen

def random_53_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_53_load_page(0)
