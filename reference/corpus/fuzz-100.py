"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 100
Generated: 2023-11-14T22:15:32.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_100_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinner: spinner_100_0
    spinner_100_0 = lv.arc(parent)
    objects["spinner_100_0"] = spinner_100_0
    spinner_100_0.set_pos(68, 68)
    spinner_100_0.set_size(132, 106)
    spinner_100_0.set_bg_angles(0, 360)
    spinner_100_0.set_angles(0, 60)
    spinner_100_0.remove_style(None, lv.PART.KNOB)
    spinner_100_0.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_100_0_anim = lv.anim_t()
    spinner_100_0_anim.init()
    spinner_100_0_anim.set_var(spinner_100_0)
    spinner_100_0_anim.set_values(0, 360)
    spinner_100_0_anim.set_duration(1000)
    spinner_100_0_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_100_0_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_100_0_anim.set_custom_exec_cb(lambda _anim, value: spinner_100_0.set_rotation(value))
    spinner_100_0_anim.start()
    spinner_100_0.set_style_arc_width(8, lv.PART.MAIN)
    spinner_100_0.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_100_0.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # chart: chart_100_1
    chart_100_1 = lv.chart(parent)
    objects["chart_100_1"] = chart_100_1
    chart_100_1.set_pos(687, 327)
    chart_100_1.set_size(114, 87)
    chart_100_1.set_type(lv.chart.TYPE.LINE)
    chart_100_1.set_point_count(10)
    chart_100_1.set_div_line_count(3, 5)
    chart_100_1.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_100_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_100_1_series_1 = chart_100_1.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_100_1.set_next_value(chart_100_1_series_1, 10)
    chart_100_1.set_next_value(chart_100_1_series_1, 20)
    chart_100_1.set_next_value(chart_100_1_series_1, 30)
    chart_100_1.set_next_value(chart_100_1_series_1, 25)
    chart_100_1.set_next_value(chart_100_1_series_1, 40)
    chart_100_1.set_next_value(chart_100_1_series_1, 35)
    chart_100_1.set_next_value(chart_100_1_series_1, 50)

    # list: list_100_2
    list_100_2 = lv.obj(parent)
    objects["list_100_2"] = list_100_2
    list_100_2.set_pos(149, 77)
    list_100_2.set_size(130, 11)
    list_100_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_100_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_100_2_item_1 = lv.button(list_100_2)
    list_100_2_item_1.set_width(lv.pct(100))
    list_100_2_item_1_label = lv.label(list_100_2_item_1)
    list_100_2_item_1_label.set_text("Item 1")
    list_100_2_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_100_2_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_100_2_item_2 = lv.button(list_100_2)
    list_100_2_item_2.set_width(lv.pct(100))
    list_100_2_item_2_label = lv.label(list_100_2_item_2)
    list_100_2_item_2_label.set_text("Item 2")
    list_100_2_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_100_2_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_100_2_item_3 = lv.button(list_100_2)
    list_100_2_item_3.set_width(lv.pct(100))
    list_100_2_item_3_label = lv.label(list_100_2_item_3)
    list_100_2_item_3_label.set_text("Item 3")
    list_100_2_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_100_2_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_100_2_item_4 = lv.button(list_100_2)
    list_100_2_item_4.set_width(lv.pct(100))
    list_100_2_item_4_label = lv.label(list_100_2_item_4)
    list_100_2_item_4_label.set_text("Item 4")
    list_100_2_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_100_2_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_100_2_item_5 = lv.button(list_100_2)
    list_100_2_item_5.set_width(lv.pct(100))
    list_100_2_item_5_label = lv.label(list_100_2_item_5)
    list_100_2_item_5_label.set_text("Item 5")
    list_100_2_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_100_2_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # slider: slider_100_3
    slider_100_3 = lv.slider(parent)
    objects["slider_100_3"] = slider_100_3
    slider_100_3.set_pos(53, 292)
    slider_100_3.set_size(58, 77)
    slider_100_3.set_range(0, 100)
    slider_100_3.set_value(50, False)
    slider_100_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_100_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_100_3.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)

    # buttonmatrix: buttonmatrix_100_4
    buttonmatrix_100_4 = lv.buttonmatrix(parent)
    objects["buttonmatrix_100_4"] = buttonmatrix_100_4
    buttonmatrix_100_4.set_pos(245, 155)
    buttonmatrix_100_4.set_size(102, 156)
    buttonmatrix_100_4_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_100_4.set_map(buttonmatrix_100_4_map)
    buttonmatrix_100_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_100_4.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_100_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_100_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # tabview: tabview_100_5
    tabview_100_5 = lv.tabview(parent)
    objects["tabview_100_5"] = tabview_100_5
    tabview_100_5.set_pos(33, 183)
    tabview_100_5.set_size(241, 132)
    tabview_100_5.set_tab_bar_position(lv.DIR.TOP)
    tabview_100_5.set_tab_bar_size(40)
    tabview_100_5_tab_1 = tabview_100_5.add_tab("Tab 1")
    tabview_100_5_tab_2 = tabview_100_5.add_tab("Tab 2")
    tabview_100_5_tab_3 = tabview_100_5.add_tab("Tab 3")
    tabview_100_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # roller: roller_100_6
    roller_100_6 = lv.roller(parent)
    objects["roller_100_6"] = roller_100_6
    roller_100_6.set_pos(74, 305)
    roller_100_6.set_size(54, 75)
    roller_100_6.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_100_6.set_visible_row_count(3)
    roller_100_6.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_100_6.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_100_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_100_6.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_100_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_100_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_100_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_100_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_100_get_current_page():
    return current_screen

def random_100_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_100_load_page(0)
