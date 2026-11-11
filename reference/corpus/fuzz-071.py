"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 71
Generated: 2023-11-14T22:15:03.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_71_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # bar: bar_71_0
    bar_71_0 = lv.bar(parent)
    objects["bar_71_0"] = bar_71_0
    bar_71_0.set_pos(162, 340)
    bar_71_0.set_size(116, 45)
    bar_71_0.set_range(0, 100)
    bar_71_0.set_value(50, False)
    bar_71_0.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_71_0.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # chart: chart_71_1
    chart_71_1 = lv.chart(parent)
    objects["chart_71_1"] = chart_71_1
    chart_71_1.set_pos(654, 264)
    chart_71_1.set_size(260, 25)
    chart_71_1.set_type(lv.chart.TYPE.LINE)
    chart_71_1.set_point_count(10)
    chart_71_1.set_div_line_count(3, 5)
    chart_71_1.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_71_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_71_1_series_1 = chart_71_1.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_71_1.set_next_value(chart_71_1_series_1, 10)
    chart_71_1.set_next_value(chart_71_1_series_1, 20)
    chart_71_1.set_next_value(chart_71_1_series_1, 30)
    chart_71_1.set_next_value(chart_71_1_series_1, 25)
    chart_71_1.set_next_value(chart_71_1_series_1, 40)
    chart_71_1.set_next_value(chart_71_1_series_1, 35)
    chart_71_1.set_next_value(chart_71_1_series_1, 50)

    # menu: menu_71_2
    menu_71_2 = lv.obj(parent)
    objects["menu_71_2"] = menu_71_2
    menu_71_2.set_pos(164, 110)
    menu_71_2.set_size(180, 13)
    menu_71_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_71_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_71_2_title = lv.label(menu_71_2)
    menu_71_2_title.set_text("Menu")
    menu_71_2_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_71_2_item_1 = lv.button(menu_71_2)
    menu_71_2_item_1.set_width(lv.pct(100))
    menu_71_2_item_1_label = lv.label(menu_71_2_item_1)
    menu_71_2_item_1_label.set_text("Item 1")
    menu_71_2_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_71_2_item_2 = lv.button(menu_71_2)
    menu_71_2_item_2.set_width(lv.pct(100))
    menu_71_2_item_2_label = lv.label(menu_71_2_item_2)
    menu_71_2_item_2_label.set_text("Item 2")
    menu_71_2_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_71_2_item_3 = lv.button(menu_71_2)
    menu_71_2_item_3.set_width(lv.pct(100))
    menu_71_2_item_3_label = lv.label(menu_71_2_item_3)
    menu_71_2_item_3_label.set_text("Item 3")
    menu_71_2_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_71_2_item_4 = lv.button(menu_71_2)
    menu_71_2_item_4.set_width(lv.pct(100))
    menu_71_2_item_4_label = lv.label(menu_71_2_item_4)
    menu_71_2_item_4_label.set_text("Item 4")
    menu_71_2_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # imagebutton: imagebutton_71_3
    imagebutton_71_3 = lv.imagebutton(parent)
    objects["imagebutton_71_3"] = imagebutton_71_3
    imagebutton_71_3.set_pos(313, 178)
    imagebutton_71_3.set_size(223, 12)
    imagebutton_71_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_71_3.set_style_radius(5, lv.PART.MAIN)
    imagebutton_71_3_label = lv.label(imagebutton_71_3)
    imagebutton_71_3_label.set_text("Testo 71:3 \" \\ Città")
    imagebutton_71_3_label.center()
    imagebutton_71_3_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_71_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # switch: switch_71_4
    switch_71_4 = lv.switch(parent)
    objects["switch_71_4"] = switch_71_4
    switch_71_4.set_pos(68, 176)
    switch_71_4.set_size(266, 73)
    switch_71_4.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_71_4.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_71_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # spinbox: spinbox_71_5
    spinbox_71_5 = lv.spinbox(parent)
    objects["spinbox_71_5"] = spinbox_71_5
    spinbox_71_5.set_pos(54, 389)
    spinbox_71_5.set_size(253, 24)
    spinbox_71_5.set_digit_format(4, 0)
    spinbox_71_5.set_range(0, 999)
    spinbox_71_5.set_value(0)
    spinbox_71_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_71_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_71_5.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # checkbox: checkbox_71_6
    checkbox_71_6 = lv.checkbox(parent)
    objects["checkbox_71_6"] = checkbox_71_6
    checkbox_71_6.set_pos(469, 315)
    checkbox_71_6.set_text("Testo 71:6 \" \\ Città")
    checkbox_71_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_71_6.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_71_6.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # dropdown: dropdown_71_7
    dropdown_71_7 = lv.dropdown(parent)
    objects["dropdown_71_7"] = dropdown_71_7
    dropdown_71_7.set_pos(154, 148)
    dropdown_71_7.set_size(148, 159)
    dropdown_71_7.set_options("Option 1\nOption 2\nOption 3")
    dropdown_71_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_71_7.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_71_7.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_71_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_71_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_71_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_71_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_71_get_current_page():
    return current_screen

def random_71_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_71_load_page(0)
