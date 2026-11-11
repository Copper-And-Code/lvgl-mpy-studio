"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 88
Generated: 2023-11-14T22:15:20.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_88_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # bar: bar_88_0
    bar_88_0 = lv.bar(parent)
    objects["bar_88_0"] = bar_88_0
    bar_88_0.set_pos(654, 97)
    bar_88_0.set_size(242, 145)
    bar_88_0.set_range(0, 100)
    bar_88_0.set_value(50, False)
    bar_88_0.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_88_0.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # spinner: spinner_88_1
    spinner_88_1 = lv.arc(parent)
    objects["spinner_88_1"] = spinner_88_1
    spinner_88_1.set_pos(188, 284)
    spinner_88_1.set_size(119, 26)
    spinner_88_1.set_bg_angles(0, 360)
    spinner_88_1.set_angles(0, 60)
    spinner_88_1.remove_style(None, lv.PART.KNOB)
    spinner_88_1.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_88_1_anim = lv.anim_t()
    spinner_88_1_anim.init()
    spinner_88_1_anim.set_var(spinner_88_1)
    spinner_88_1_anim.set_values(0, 360)
    spinner_88_1_anim.set_duration(1000)
    spinner_88_1_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_88_1_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_88_1_anim.set_custom_exec_cb(lambda _anim, value: spinner_88_1.set_rotation(value))
    spinner_88_1_anim.start()
    spinner_88_1.set_style_arc_width(8, lv.PART.MAIN)
    spinner_88_1.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_88_1.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # chart: chart_88_2
    chart_88_2 = lv.chart(parent)
    objects["chart_88_2"] = chart_88_2
    chart_88_2.set_pos(172, 380)
    chart_88_2.set_size(59, 74)
    chart_88_2.set_type(lv.chart.TYPE.LINE)
    chart_88_2.set_point_count(10)
    chart_88_2.set_div_line_count(3, 5)
    chart_88_2.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_88_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_88_2_series_1 = chart_88_2.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_88_2.set_next_value(chart_88_2_series_1, 10)
    chart_88_2.set_next_value(chart_88_2_series_1, 20)
    chart_88_2.set_next_value(chart_88_2_series_1, 30)
    chart_88_2.set_next_value(chart_88_2_series_1, 25)
    chart_88_2.set_next_value(chart_88_2_series_1, 40)
    chart_88_2.set_next_value(chart_88_2_series_1, 35)
    chart_88_2.set_next_value(chart_88_2_series_1, 50)

    # menu: menu_88_3
    menu_88_3 = lv.obj(parent)
    objects["menu_88_3"] = menu_88_3
    menu_88_3.set_pos(681, 165)
    menu_88_3.set_size(190, 144)
    menu_88_3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_88_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_88_3_title = lv.label(menu_88_3)
    menu_88_3_title.set_text("Menu")
    menu_88_3_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_88_3_item_1 = lv.button(menu_88_3)
    menu_88_3_item_1.set_width(lv.pct(100))
    menu_88_3_item_1_label = lv.label(menu_88_3_item_1)
    menu_88_3_item_1_label.set_text("Item 1")
    menu_88_3_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_88_3_item_2 = lv.button(menu_88_3)
    menu_88_3_item_2.set_width(lv.pct(100))
    menu_88_3_item_2_label = lv.label(menu_88_3_item_2)
    menu_88_3_item_2_label.set_text("Item 2")
    menu_88_3_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_88_3_item_3 = lv.button(menu_88_3)
    menu_88_3_item_3.set_width(lv.pct(100))
    menu_88_3_item_3_label = lv.label(menu_88_3_item_3)
    menu_88_3_item_3_label.set_text("Item 3")
    menu_88_3_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_88_3_item_4 = lv.button(menu_88_3)
    menu_88_3_item_4.set_width(lv.pct(100))
    menu_88_3_item_4_label = lv.label(menu_88_3_item_4)
    menu_88_3_item_4_label.set_text("Item 4")
    menu_88_3_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)


def random_88_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_88_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_88_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_88_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_88_get_current_page():
    return current_screen

def random_88_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_88_load_page(0)
