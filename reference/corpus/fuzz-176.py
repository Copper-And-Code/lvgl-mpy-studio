"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 176
Generated: 2023-11-14T22:16:48.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_176_3_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_176_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # checkbox: checkbox_176_0
    checkbox_176_0 = lv.checkbox(parent)
    objects["checkbox_176_0"] = checkbox_176_0
    checkbox_176_0.set_pos(469, 55)
    checkbox_176_0.set_text("Testo 176:0 \" \\ Città")
    checkbox_176_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_176_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_176_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # list: list_176_1
    list_176_1 = lv.obj(parent)
    objects["list_176_1"] = list_176_1
    list_176_1.set_pos(50, 93)
    list_176_1.set_size(237, 145)
    list_176_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_176_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_176_1_item_1 = lv.button(list_176_1)
    list_176_1_item_1.set_width(lv.pct(100))
    list_176_1_item_1_label = lv.label(list_176_1_item_1)
    list_176_1_item_1_label.set_text("Item 1")
    list_176_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_176_1_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_176_1_item_2 = lv.button(list_176_1)
    list_176_1_item_2.set_width(lv.pct(100))
    list_176_1_item_2_label = lv.label(list_176_1_item_2)
    list_176_1_item_2_label.set_text("Item 2")
    list_176_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_176_1_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_176_1_item_3 = lv.button(list_176_1)
    list_176_1_item_3.set_width(lv.pct(100))
    list_176_1_item_3_label = lv.label(list_176_1_item_3)
    list_176_1_item_3_label.set_text("Item 3")
    list_176_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_176_1_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_176_1_item_4 = lv.button(list_176_1)
    list_176_1_item_4.set_width(lv.pct(100))
    list_176_1_item_4_label = lv.label(list_176_1_item_4)
    list_176_1_item_4_label.set_text("Item 4")
    list_176_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_176_1_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_176_1_item_5 = lv.button(list_176_1)
    list_176_1_item_5.set_width(lv.pct(100))
    list_176_1_item_5_label = lv.label(list_176_1_item_5)
    list_176_1_item_5_label.set_text("Item 5")
    list_176_1_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_176_1_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_176_2
    buttonmatrix_176_2 = lv.buttonmatrix(parent)
    objects["buttonmatrix_176_2"] = buttonmatrix_176_2
    buttonmatrix_176_2.set_pos(550, 239)
    buttonmatrix_176_2.set_size(262, 106)
    buttonmatrix_176_2_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_176_2.set_map(buttonmatrix_176_2_map)
    buttonmatrix_176_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_176_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_176_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_176_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # button: button_176_3
    button_176_3 = lv.button(parent)
    objects["button_176_3"] = button_176_3
    button_176_3.set_pos(429, 52)
    button_176_3.set_size(206, 91)
    button_176_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_176_3.set_style_radius(5, lv.PART.MAIN)
    button_176_3_label = lv.label(button_176_3)
    button_176_3_label.set_text("Testo 176:3 \" \\ Città")
    button_176_3_label.center()
    button_176_3_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_176_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_176_3.add_event_cb(button_176_3_changed, lv.EVENT.CLICKED, None)

    # menu: menu_176_4
    menu_176_4 = lv.obj(parent)
    objects["menu_176_4"] = menu_176_4
    menu_176_4.set_pos(476, 91)
    menu_176_4.set_size(172, 58)
    menu_176_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_176_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_176_4_title = lv.label(menu_176_4)
    menu_176_4_title.set_text("Menu")
    menu_176_4_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_176_4_item_1 = lv.button(menu_176_4)
    menu_176_4_item_1.set_width(lv.pct(100))
    menu_176_4_item_1_label = lv.label(menu_176_4_item_1)
    menu_176_4_item_1_label.set_text("Item 1")
    menu_176_4_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_176_4_item_2 = lv.button(menu_176_4)
    menu_176_4_item_2.set_width(lv.pct(100))
    menu_176_4_item_2_label = lv.label(menu_176_4_item_2)
    menu_176_4_item_2_label.set_text("Item 2")
    menu_176_4_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_176_4_item_3 = lv.button(menu_176_4)
    menu_176_4_item_3.set_width(lv.pct(100))
    menu_176_4_item_3_label = lv.label(menu_176_4_item_3)
    menu_176_4_item_3_label.set_text("Item 3")
    menu_176_4_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_176_4_item_4 = lv.button(menu_176_4)
    menu_176_4_item_4.set_width(lv.pct(100))
    menu_176_4_item_4_label = lv.label(menu_176_4_item_4)
    menu_176_4_item_4_label.set_text("Item 4")
    menu_176_4_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # scale: scale_176_5
    scale_176_5 = lv.scale(parent)
    objects["scale_176_5"] = scale_176_5
    scale_176_5.set_pos(170, 232)
    scale_176_5.set_size(206, 121)
    scale_176_5.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_176_5.set_range(0, 100)
    scale_176_5.set_total_tick_count(51)
    scale_176_5.set_major_tick_every(5)
    scale_176_5.set_style_length(15, lv.PART.INDICATOR)
    scale_176_5.set_style_length(8, lv.PART.ITEMS)
    scale_176_5.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_176_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # spinner: spinner_176_6
    spinner_176_6 = lv.arc(parent)
    objects["spinner_176_6"] = spinner_176_6
    spinner_176_6.set_pos(186, 330)
    spinner_176_6.set_size(189, 77)
    spinner_176_6.set_bg_angles(0, 360)
    spinner_176_6.set_angles(0, 60)
    spinner_176_6.remove_style(None, lv.PART.KNOB)
    spinner_176_6.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_176_6_anim = lv.anim_t()
    spinner_176_6_anim.init()
    spinner_176_6_anim.set_var(spinner_176_6)
    spinner_176_6_anim.set_values(0, 360)
    spinner_176_6_anim.set_duration(1000)
    spinner_176_6_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_176_6_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_176_6_anim.set_custom_exec_cb(lambda _anim, value: spinner_176_6.set_rotation(value))
    spinner_176_6_anim.start()
    spinner_176_6.set_style_arc_width(8, lv.PART.MAIN)
    spinner_176_6.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_176_6.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # chart: chart_176_7
    chart_176_7 = lv.chart(parent)
    objects["chart_176_7"] = chart_176_7
    chart_176_7.set_pos(482, 177)
    chart_176_7.set_size(47, 56)
    chart_176_7.set_type(lv.chart.TYPE.LINE)
    chart_176_7.set_point_count(10)
    chart_176_7.set_div_line_count(3, 5)
    chart_176_7.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_176_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_176_7_series_1 = chart_176_7.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_176_7.set_next_value(chart_176_7_series_1, 10)
    chart_176_7.set_next_value(chart_176_7_series_1, 20)
    chart_176_7.set_next_value(chart_176_7_series_1, 30)
    chart_176_7.set_next_value(chart_176_7_series_1, 25)
    chart_176_7.set_next_value(chart_176_7_series_1, 40)
    chart_176_7.set_next_value(chart_176_7_series_1, 35)
    chart_176_7.set_next_value(chart_176_7_series_1, 50)


def random_176_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_176_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_176_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_176_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_176_get_current_page():
    return current_screen

def random_176_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_176_load_page(0)
