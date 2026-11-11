"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 139
Generated: 2023-11-14T22:16:11.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_139_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # buttonmatrix: buttonmatrix_139_0
    buttonmatrix_139_0 = lv.buttonmatrix(parent)
    objects["buttonmatrix_139_0"] = buttonmatrix_139_0
    buttonmatrix_139_0.set_pos(136, 223)
    buttonmatrix_139_0.set_size(58, 150)
    buttonmatrix_139_0_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_139_0.set_map(buttonmatrix_139_0_map)
    buttonmatrix_139_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_139_0.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_139_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_139_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # textarea: textarea_139_1
    textarea_139_1 = lv.textarea(parent)
    objects["textarea_139_1"] = textarea_139_1
    textarea_139_1.set_pos(166, 213)
    textarea_139_1.set_size(144, 69)
    textarea_139_1.set_text("Testo 139:1 \" \\ Città")
    textarea_139_1.set_placeholder_text("Type here")
    textarea_139_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_139_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_139_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # chart: chart_139_2
    chart_139_2 = lv.chart(parent)
    objects["chart_139_2"] = chart_139_2
    chart_139_2.set_pos(155, 32)
    chart_139_2.set_size(250, 56)
    chart_139_2.set_type(lv.chart.TYPE.LINE)
    chart_139_2.set_point_count(10)
    chart_139_2.set_div_line_count(3, 5)
    chart_139_2.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_139_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_139_2_series_1 = chart_139_2.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_139_2.set_next_value(chart_139_2_series_1, 10)
    chart_139_2.set_next_value(chart_139_2_series_1, 20)
    chart_139_2.set_next_value(chart_139_2_series_1, 30)
    chart_139_2.set_next_value(chart_139_2_series_1, 25)
    chart_139_2.set_next_value(chart_139_2_series_1, 40)
    chart_139_2.set_next_value(chart_139_2_series_1, 35)
    chart_139_2.set_next_value(chart_139_2_series_1, 50)

    # button: button_139_3
    button_139_3 = lv.button(parent)
    objects["button_139_3"] = button_139_3
    button_139_3.set_pos(248, 340)
    button_139_3.set_size(111, 85)
    button_139_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_139_3.set_style_radius(5, lv.PART.MAIN)
    button_139_3_label = lv.label(button_139_3)
    button_139_3_label.set_text("Testo 139:3 \" \\ Città")
    button_139_3_label.center()
    button_139_3_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_139_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # roller: roller_139_4
    roller_139_4 = lv.roller(parent)
    objects["roller_139_4"] = roller_139_4
    roller_139_4.set_pos(369, 80)
    roller_139_4.set_size(117, 82)
    roller_139_4.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_139_4.set_visible_row_count(3)
    roller_139_4.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_139_4.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_139_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_139_4.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_139_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_139_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_139_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_139_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_139_get_current_page():
    return current_screen

def random_139_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_139_load_page(0)
