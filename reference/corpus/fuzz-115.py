"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 115
Generated: 2023-11-14T22:15:47.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_115_2_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_115_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # table: table_115_0
    table_115_0 = lv.table(parent)
    objects["table_115_0"] = table_115_0
    table_115_0.set_pos(264, 227)
    table_115_0.set_size(250, 120)
    table_115_0.set_column_count(3)
    table_115_0.set_column_width(0, 100)
    table_115_0.set_column_width(1, 100)
    table_115_0.set_column_width(2, 100)
    table_115_0.set_cell_value(0, 0, "Col 1")
    table_115_0.set_cell_value(0, 1, "Col 2")
    table_115_0.set_cell_value(0, 2, "Col 3")
    table_115_0.set_cell_value(1, 0, "A1")
    table_115_0.set_cell_value(1, 1, "B1")
    table_115_0.set_cell_value(1, 2, "C1")
    table_115_0.set_cell_value(2, 0, "A2")
    table_115_0.set_cell_value(2, 1, "B2")
    table_115_0.set_cell_value(2, 2, "C2")
    table_115_0.set_cell_value(3, 0, "A3")
    table_115_0.set_cell_value(3, 1, "B3")
    table_115_0.set_cell_value(3, 2, "C3")
    table_115_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_115_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_115_0.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_115_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # chart: chart_115_1
    chart_115_1 = lv.chart(parent)
    objects["chart_115_1"] = chart_115_1
    chart_115_1.set_pos(669, 56)
    chart_115_1.set_size(173, 151)
    chart_115_1.set_type(lv.chart.TYPE.LINE)
    chart_115_1.set_point_count(10)
    chart_115_1.set_div_line_count(3, 5)
    chart_115_1.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_115_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_115_1_series_1 = chart_115_1.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_115_1.set_next_value(chart_115_1_series_1, 10)
    chart_115_1.set_next_value(chart_115_1_series_1, 20)
    chart_115_1.set_next_value(chart_115_1_series_1, 30)
    chart_115_1.set_next_value(chart_115_1_series_1, 25)
    chart_115_1.set_next_value(chart_115_1_series_1, 40)
    chart_115_1.set_next_value(chart_115_1_series_1, 35)
    chart_115_1.set_next_value(chart_115_1_series_1, 50)

    # slider: slider_115_2
    slider_115_2 = lv.slider(parent)
    objects["slider_115_2"] = slider_115_2
    slider_115_2.set_pos(164, 138)
    slider_115_2.set_size(197, 79)
    slider_115_2.set_range(0, 100)
    slider_115_2.set_value(50, False)
    slider_115_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_115_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_115_2.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_115_2.add_event_cb(slider_115_2_changed, lv.EVENT.VALUE_CHANGED, None)

    # button: button_115_3
    button_115_3 = lv.button(parent)
    objects["button_115_3"] = button_115_3
    button_115_3.set_pos(409, 261)
    button_115_3.set_size(39, 65)
    button_115_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_115_3.set_style_radius(5, lv.PART.MAIN)
    button_115_3_label = lv.label(button_115_3)
    button_115_3_label.set_text("Testo 115:3 \" \\ Città")
    button_115_3_label.center()
    button_115_3_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_115_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_115_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_115_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_115_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_115_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_115_get_current_page():
    return current_screen

def random_115_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_115_load_page(0)
