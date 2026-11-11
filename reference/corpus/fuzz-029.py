"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 29
Generated: 2023-11-14T22:14:21.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_29_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tabview: tabview_29_0
    tabview_29_0 = lv.tabview(parent)
    objects["tabview_29_0"] = tabview_29_0
    tabview_29_0.set_pos(217, 345)
    tabview_29_0.set_size(33, 158)
    tabview_29_0.set_tab_bar_position(lv.DIR.TOP)
    tabview_29_0.set_tab_bar_size(40)
    tabview_29_0_tab_1 = tabview_29_0.add_tab("Tab 1")
    tabview_29_0_tab_2 = tabview_29_0.add_tab("Tab 2")
    tabview_29_0_tab_3 = tabview_29_0.add_tab("Tab 3")
    tabview_29_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # tabview: tabview_29_1
    tabview_29_1 = lv.tabview(parent)
    objects["tabview_29_1"] = tabview_29_1
    tabview_29_1.set_pos(620, 336)
    tabview_29_1.set_size(142, 14)
    tabview_29_1.set_tab_bar_position(lv.DIR.TOP)
    tabview_29_1.set_tab_bar_size(40)
    tabview_29_1_tab_1 = tabview_29_1.add_tab("Tab 1")
    tabview_29_1_tab_2 = tabview_29_1.add_tab("Tab 2")
    tabview_29_1_tab_3 = tabview_29_1.add_tab("Tab 3")
    tabview_29_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # chart: chart_29_2
    chart_29_2 = lv.chart(parent)
    objects["chart_29_2"] = chart_29_2
    chart_29_2.set_pos(359, 5)
    chart_29_2.set_size(83, 132)
    chart_29_2.set_type(lv.chart.TYPE.LINE)
    chart_29_2.set_point_count(10)
    chart_29_2.set_div_line_count(3, 5)
    chart_29_2.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_29_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_29_2_series_1 = chart_29_2.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_29_2.set_next_value(chart_29_2_series_1, 10)
    chart_29_2.set_next_value(chart_29_2_series_1, 20)
    chart_29_2.set_next_value(chart_29_2_series_1, 30)
    chart_29_2.set_next_value(chart_29_2_series_1, 25)
    chart_29_2.set_next_value(chart_29_2_series_1, 40)
    chart_29_2.set_next_value(chart_29_2_series_1, 35)
    chart_29_2.set_next_value(chart_29_2_series_1, 50)

    # win: win_29_3
    win_29_3 = lv.obj(parent)
    objects["win_29_3"] = win_29_3
    win_29_3.set_pos(313, 188)
    win_29_3.set_size(76, 72)
    win_29_3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_29_3.set_style_pad_all(0, lv.PART.MAIN)
    win_29_3.set_style_pad_row(0, lv.PART.MAIN)
    win_29_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_29_3_header = lv.obj(win_29_3)
    win_29_3_header.set_size(lv.pct(100), 40)
    win_29_3_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_29_3_header.set_style_radius(0, lv.PART.MAIN)
    win_29_3_title = lv.label(win_29_3_header)
    win_29_3_title.set_text("Window Title")
    win_29_3_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_29_3_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_29_3_content = lv.obj(win_29_3)
    win_29_3_content.set_width(lv.pct(100))
    win_29_3_content.set_flex_grow(1)

    # table: table_29_4
    table_29_4 = lv.table(parent)
    objects["table_29_4"] = table_29_4
    table_29_4.set_pos(432, 184)
    table_29_4.set_size(240, 140)
    table_29_4.set_column_count(3)
    table_29_4.set_column_width(0, 100)
    table_29_4.set_column_width(1, 100)
    table_29_4.set_column_width(2, 100)
    table_29_4.set_cell_value(0, 0, "Col 1")
    table_29_4.set_cell_value(0, 1, "Col 2")
    table_29_4.set_cell_value(0, 2, "Col 3")
    table_29_4.set_cell_value(1, 0, "A1")
    table_29_4.set_cell_value(1, 1, "B1")
    table_29_4.set_cell_value(1, 2, "C1")
    table_29_4.set_cell_value(2, 0, "A2")
    table_29_4.set_cell_value(2, 1, "B2")
    table_29_4.set_cell_value(2, 2, "C2")
    table_29_4.set_cell_value(3, 0, "A3")
    table_29_4.set_cell_value(3, 1, "B3")
    table_29_4.set_cell_value(3, 2, "C3")
    table_29_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_29_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_29_4.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_29_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # line: line_29_5
    line_29_5 = lv.line(parent)
    objects["line_29_5"] = line_29_5
    line_29_5.set_pos(457, 133)
    line_29_5_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_29_5.set_points(line_29_5_points, 2)
    line_29_5.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_29_5.set_style_line_width(2, lv.PART.MAIN)


def random_29_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_29_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_29_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_29_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_29_get_current_page():
    return current_screen

def random_29_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_29_load_page(0)
