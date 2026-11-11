"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 57
Generated: 2023-11-14T22:14:49.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_57_2_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_57_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinbox: spinbox_57_0
    spinbox_57_0 = lv.spinbox(parent)
    objects["spinbox_57_0"] = spinbox_57_0
    spinbox_57_0.set_pos(53, 321)
    spinbox_57_0.set_size(24, 95)
    spinbox_57_0.set_digit_format(4, 0)
    spinbox_57_0.set_range(0, 999)
    spinbox_57_0.set_value(0)
    spinbox_57_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_57_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_57_0.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # imagebutton: imagebutton_57_1
    imagebutton_57_1 = lv.imagebutton(parent)
    objects["imagebutton_57_1"] = imagebutton_57_1
    imagebutton_57_1.set_pos(275, 87)
    imagebutton_57_1.set_size(37, 99)
    imagebutton_57_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_57_1.set_style_radius(5, lv.PART.MAIN)
    imagebutton_57_1_label = lv.label(imagebutton_57_1)
    imagebutton_57_1_label.set_text("Testo 57:1 \" \\ Città")
    imagebutton_57_1_label.center()
    imagebutton_57_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_57_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # button: button_57_2
    button_57_2 = lv.button(parent)
    objects["button_57_2"] = button_57_2
    button_57_2.set_pos(115, 381)
    button_57_2.set_size(252, 32)
    button_57_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_57_2.set_style_radius(5, lv.PART.MAIN)
    button_57_2_label = lv.label(button_57_2)
    button_57_2_label.set_text("Testo 57:2 \" \\ Città")
    button_57_2_label.center()
    button_57_2_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_57_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_57_2.add_event_cb(button_57_2_changed, lv.EVENT.CLICKED, None)

    # chart: chart_57_3
    chart_57_3 = lv.chart(parent)
    objects["chart_57_3"] = chart_57_3
    chart_57_3.set_pos(514, 60)
    chart_57_3.set_size(52, 126)
    chart_57_3.set_type(lv.chart.TYPE.LINE)
    chart_57_3.set_point_count(10)
    chart_57_3.set_div_line_count(3, 5)
    chart_57_3.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_57_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_57_3_series_1 = chart_57_3.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_57_3.set_next_value(chart_57_3_series_1, 10)
    chart_57_3.set_next_value(chart_57_3_series_1, 20)
    chart_57_3.set_next_value(chart_57_3_series_1, 30)
    chart_57_3.set_next_value(chart_57_3_series_1, 25)
    chart_57_3.set_next_value(chart_57_3_series_1, 40)
    chart_57_3.set_next_value(chart_57_3_series_1, 35)
    chart_57_3.set_next_value(chart_57_3_series_1, 50)

    # line: line_57_4
    line_57_4 = lv.line(parent)
    objects["line_57_4"] = line_57_4
    line_57_4.set_pos(506, 28)
    line_57_4_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_57_4.set_points(line_57_4_points, 2)
    line_57_4.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_57_4.set_style_line_width(2, lv.PART.MAIN)

    # span: span_57_5
    span_57_5 = lv.spangroup(parent)
    objects["span_57_5"] = span_57_5
    span_57_5.set_pos(651, 108)
    span_57_5.set_size(180, 15)
    span_57_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_57_5_span_1 = span_57_5.add_span()
    span_57_5_span_1.set_text("Normal text")
    span_57_5_span_1_style = span_57_5_span_1.get_style()
    span_57_5_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_57_5_span_1_style.set_text_font(lv.font_montserrat_14)
    span_57_5_span_2 = span_57_5.add_span()
    span_57_5_span_2.set_text("Bold text")
    span_57_5_span_2_style = span_57_5_span_2.get_style()
    span_57_5_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_57_5_span_2_style.set_text_font(lv.font_montserrat_16)
    span_57_5_span_3 = span_57_5.add_span()
    span_57_5_span_3.set_text("Small text")
    span_57_5_span_3_style = span_57_5_span_3.get_style()
    span_57_5_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_57_5_span_3_style.set_text_font(lv.font_montserrat_14)
    span_57_5.refresh()

    # led: led_57_6
    led_57_6 = lv.led(parent)
    objects["led_57_6"] = led_57_6
    led_57_6.set_pos(598, 1)
    led_57_6.set_size(91, 157)
    led_57_6.set_color(lv.color_hex(0xFF0000))
    led_57_6.set_brightness(255)

    # msgbox: msgbox_57_7
    msgbox_57_7 = lv.msgbox(parent)
    objects["msgbox_57_7"] = msgbox_57_7
    msgbox_57_7.set_pos(560, 96)
    msgbox_57_7.set_size(163, 152)
    msgbox_57_7_title = msgbox_57_7.add_title("Notice")
    msgbox_57_7_text = msgbox_57_7.add_text("Testo 57:7 \" \\ Città")
    msgbox_57_7_button_1 = msgbox_57_7.add_footer_button("OK")
    msgbox_57_7_button_2 = msgbox_57_7.add_footer_button("Cancel")
    msgbox_57_7_close = msgbox_57_7.add_close_button()
    msgbox_57_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_57_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_57_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_57_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_57_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_57_get_current_page():
    return current_screen

def random_57_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_57_load_page(0)
