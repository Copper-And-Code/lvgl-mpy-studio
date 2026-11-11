"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 146
Generated: 2023-11-14T22:16:18.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_146_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # textarea: textarea_146_0
    textarea_146_0 = lv.textarea(parent)
    objects["textarea_146_0"] = textarea_146_0
    textarea_146_0.set_pos(172, 112)
    textarea_146_0.set_size(111, 159)
    textarea_146_0.set_text("Testo 146:0 \" \\ Città")
    textarea_146_0.set_placeholder_text("Type here")
    textarea_146_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_146_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_146_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # chart: chart_146_1
    chart_146_1 = lv.chart(parent)
    objects["chart_146_1"] = chart_146_1
    chart_146_1.set_pos(450, 239)
    chart_146_1.set_size(97, 51)
    chart_146_1.set_type(lv.chart.TYPE.LINE)
    chart_146_1.set_point_count(10)
    chart_146_1.set_div_line_count(3, 5)
    chart_146_1.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_146_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_146_1_series_1 = chart_146_1.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_146_1.set_next_value(chart_146_1_series_1, 10)
    chart_146_1.set_next_value(chart_146_1_series_1, 20)
    chart_146_1.set_next_value(chart_146_1_series_1, 30)
    chart_146_1.set_next_value(chart_146_1_series_1, 25)
    chart_146_1.set_next_value(chart_146_1_series_1, 40)
    chart_146_1.set_next_value(chart_146_1_series_1, 35)
    chart_146_1.set_next_value(chart_146_1_series_1, 50)

    # led: led_146_2
    led_146_2 = lv.led(parent)
    objects["led_146_2"] = led_146_2
    led_146_2.set_pos(623, 287)
    led_146_2.set_size(259, 67)
    led_146_2.set_color(lv.color_hex(0xFF0000))
    led_146_2.set_brightness(255)

    # image: image_146_3
    image_146_3 = lv.image(parent)
    objects["image_146_3"] = image_146_3
    image_146_3.set_pos(485, 196)
    image_146_3.set_size(145, 13)

    # panel: panel_146_4
    panel_146_4 = lv.obj(parent)
    objects["panel_146_4"] = panel_146_4
    panel_146_4.set_pos(490, 180)
    panel_146_4.set_size(104, 157)
    panel_146_4.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_146_4.set_style_border_width(2, lv.PART.MAIN)
    panel_146_4.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_146_4.set_style_radius(5, lv.PART.MAIN)
    panel_146_4.set_style_pad_all(0, lv.PART.MAIN)
    panel_146_4.set_style_pad_gap(0, lv.PART.MAIN)

    # panel: panel_146_5
    panel_146_5 = lv.obj(parent)
    objects["panel_146_5"] = panel_146_5
    panel_146_5.set_pos(13, 358)
    panel_146_5.set_size(269, 86)
    panel_146_5.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_146_5.set_style_border_width(2, lv.PART.MAIN)
    panel_146_5.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_146_5.set_style_radius(5, lv.PART.MAIN)
    panel_146_5.set_style_pad_all(0, lv.PART.MAIN)
    panel_146_5.set_style_pad_gap(0, lv.PART.MAIN)

    # textarea: textarea_146_6
    textarea_146_6 = lv.textarea(parent)
    objects["textarea_146_6"] = textarea_146_6
    textarea_146_6.set_pos(121, 109)
    textarea_146_6.set_size(237, 118)
    textarea_146_6.set_text("Testo 146:6 \" \\ Città")
    textarea_146_6.set_placeholder_text("Type here")
    textarea_146_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_146_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_146_6.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_146_7
    buttonmatrix_146_7 = lv.buttonmatrix(parent)
    objects["buttonmatrix_146_7"] = buttonmatrix_146_7
    buttonmatrix_146_7.set_pos(186, 328)
    buttonmatrix_146_7.set_size(198, 31)
    buttonmatrix_146_7_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_146_7.set_map(buttonmatrix_146_7_map)
    buttonmatrix_146_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_146_7.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_146_7.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_146_7.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_146_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_146_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_146_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_146_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_146_get_current_page():
    return current_screen

def random_146_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_146_load_page(0)
