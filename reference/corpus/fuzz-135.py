"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 135
Generated: 2023-11-14T22:16:07.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_135_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tileview: tileview_135_0
    tileview_135_0 = lv.tileview(parent)
    objects["tileview_135_0"] = tileview_135_0
    tileview_135_0.set_pos(561, 115)
    tileview_135_0.set_size(150, 119)
    tileview_135_0.add_tile(0, 0, lv.DIR.ALL)
    tileview_135_0.add_tile(1, 0, lv.DIR.ALL)
    tileview_135_0.add_tile(0, 1, lv.DIR.ALL)
    tileview_135_0.add_tile(1, 1, lv.DIR.ALL)
    tileview_135_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # chart: chart_135_1
    chart_135_1 = lv.chart(parent)
    objects["chart_135_1"] = chart_135_1
    chart_135_1.set_pos(513, 308)
    chart_135_1.set_size(90, 152)
    chart_135_1.set_type(lv.chart.TYPE.LINE)
    chart_135_1.set_point_count(10)
    chart_135_1.set_div_line_count(3, 5)
    chart_135_1.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_135_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_135_1_series_1 = chart_135_1.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_135_1.set_next_value(chart_135_1_series_1, 10)
    chart_135_1.set_next_value(chart_135_1_series_1, 20)
    chart_135_1.set_next_value(chart_135_1_series_1, 30)
    chart_135_1.set_next_value(chart_135_1_series_1, 25)
    chart_135_1.set_next_value(chart_135_1_series_1, 40)
    chart_135_1.set_next_value(chart_135_1_series_1, 35)
    chart_135_1.set_next_value(chart_135_1_series_1, 50)

    # list: list_135_2
    list_135_2 = lv.obj(parent)
    objects["list_135_2"] = list_135_2
    list_135_2.set_pos(350, 222)
    list_135_2.set_size(217, 26)
    list_135_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_135_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_135_2_item_1 = lv.button(list_135_2)
    list_135_2_item_1.set_width(lv.pct(100))
    list_135_2_item_1_label = lv.label(list_135_2_item_1)
    list_135_2_item_1_label.set_text("Item 1")
    list_135_2_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_135_2_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_135_2_item_2 = lv.button(list_135_2)
    list_135_2_item_2.set_width(lv.pct(100))
    list_135_2_item_2_label = lv.label(list_135_2_item_2)
    list_135_2_item_2_label.set_text("Item 2")
    list_135_2_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_135_2_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_135_2_item_3 = lv.button(list_135_2)
    list_135_2_item_3.set_width(lv.pct(100))
    list_135_2_item_3_label = lv.label(list_135_2_item_3)
    list_135_2_item_3_label.set_text("Item 3")
    list_135_2_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_135_2_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_135_2_item_4 = lv.button(list_135_2)
    list_135_2_item_4.set_width(lv.pct(100))
    list_135_2_item_4_label = lv.label(list_135_2_item_4)
    list_135_2_item_4_label.set_text("Item 4")
    list_135_2_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_135_2_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_135_2_item_5 = lv.button(list_135_2)
    list_135_2_item_5.set_width(lv.pct(100))
    list_135_2_item_5_label = lv.label(list_135_2_item_5)
    list_135_2_item_5_label.set_text("Item 5")
    list_135_2_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_135_2_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # line: line_135_3
    line_135_3 = lv.line(parent)
    objects["line_135_3"] = line_135_3
    line_135_3.set_pos(348, 319)
    line_135_3_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_135_3.set_points(line_135_3_points, 2)
    line_135_3.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_135_3.set_style_line_width(2, lv.PART.MAIN)

    # tabview: tabview_135_4
    tabview_135_4 = lv.tabview(parent)
    objects["tabview_135_4"] = tabview_135_4
    tabview_135_4.set_pos(588, 72)
    tabview_135_4.set_size(117, 75)
    tabview_135_4.set_tab_bar_position(lv.DIR.TOP)
    tabview_135_4.set_tab_bar_size(40)
    tabview_135_4_tab_1 = tabview_135_4.add_tab("Tab 1")
    tabview_135_4_tab_2 = tabview_135_4.add_tab("Tab 2")
    tabview_135_4_tab_3 = tabview_135_4.add_tab("Tab 3")
    tabview_135_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # slider: slider_135_5
    slider_135_5 = lv.slider(parent)
    objects["slider_135_5"] = slider_135_5
    slider_135_5.set_pos(235, 66)
    slider_135_5.set_size(45, 54)
    slider_135_5.set_range(0, 100)
    slider_135_5.set_value(50, False)
    slider_135_5.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_135_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_135_5.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)


def random_135_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_135_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_135_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_135_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_135_get_current_page():
    return current_screen

def random_135_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_135_load_page(0)
