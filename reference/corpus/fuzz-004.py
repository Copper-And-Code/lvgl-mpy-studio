"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 4
Generated: 2023-11-14T22:13:56.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_4_7_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_4_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinbox: spinbox_4_0
    spinbox_4_0 = lv.spinbox(parent)
    objects["spinbox_4_0"] = spinbox_4_0
    spinbox_4_0.set_pos(255, 57)
    spinbox_4_0.set_size(161, 91)
    spinbox_4_0.set_digit_format(4, 0)
    spinbox_4_0.set_range(0, 999)
    spinbox_4_0.set_value(0)
    spinbox_4_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_4_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_4_0.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # list: list_4_1
    list_4_1 = lv.obj(parent)
    objects["list_4_1"] = list_4_1
    list_4_1.set_pos(667, 306)
    list_4_1.set_size(193, 47)
    list_4_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_4_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_4_1_item_1 = lv.button(list_4_1)
    list_4_1_item_1.set_width(lv.pct(100))
    list_4_1_item_1_label = lv.label(list_4_1_item_1)
    list_4_1_item_1_label.set_text("Item 1")
    list_4_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_4_1_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_4_1_item_2 = lv.button(list_4_1)
    list_4_1_item_2.set_width(lv.pct(100))
    list_4_1_item_2_label = lv.label(list_4_1_item_2)
    list_4_1_item_2_label.set_text("Item 2")
    list_4_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_4_1_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_4_1_item_3 = lv.button(list_4_1)
    list_4_1_item_3.set_width(lv.pct(100))
    list_4_1_item_3_label = lv.label(list_4_1_item_3)
    list_4_1_item_3_label.set_text("Item 3")
    list_4_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_4_1_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_4_1_item_4 = lv.button(list_4_1)
    list_4_1_item_4.set_width(lv.pct(100))
    list_4_1_item_4_label = lv.label(list_4_1_item_4)
    list_4_1_item_4_label.set_text("Item 4")
    list_4_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_4_1_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_4_1_item_5 = lv.button(list_4_1)
    list_4_1_item_5.set_width(lv.pct(100))
    list_4_1_item_5_label = lv.label(list_4_1_item_5)
    list_4_1_item_5_label.set_text("Item 5")
    list_4_1_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_4_1_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # win: win_4_2
    win_4_2 = lv.obj(parent)
    objects["win_4_2"] = win_4_2
    win_4_2.set_pos(511, 81)
    win_4_2.set_size(147, 40)
    win_4_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_4_2.set_style_pad_all(0, lv.PART.MAIN)
    win_4_2.set_style_pad_row(0, lv.PART.MAIN)
    win_4_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_4_2_header = lv.obj(win_4_2)
    win_4_2_header.set_size(lv.pct(100), 40)
    win_4_2_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_4_2_header.set_style_radius(0, lv.PART.MAIN)
    win_4_2_title = lv.label(win_4_2_header)
    win_4_2_title.set_text("Window Title")
    win_4_2_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_4_2_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_4_2_content = lv.obj(win_4_2)
    win_4_2_content.set_width(lv.pct(100))
    win_4_2_content.set_flex_grow(1)

    # msgbox: msgbox_4_3
    msgbox_4_3 = lv.msgbox(parent)
    objects["msgbox_4_3"] = msgbox_4_3
    msgbox_4_3.set_pos(435, 79)
    msgbox_4_3.set_size(251, 130)
    msgbox_4_3_title = msgbox_4_3.add_title("Notice")
    msgbox_4_3_text = msgbox_4_3.add_text("Testo 4:3 \" \\ Città")
    msgbox_4_3_button_1 = msgbox_4_3.add_footer_button("OK")
    msgbox_4_3_button_2 = msgbox_4_3.add_footer_button("Cancel")
    msgbox_4_3_close = msgbox_4_3.add_close_button()
    msgbox_4_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # calendar: calendar_4_4
    calendar_4_4 = lv.calendar(parent)
    objects["calendar_4_4"] = calendar_4_4
    calendar_4_4.set_pos(373, 373)
    calendar_4_4.set_size(49, 20)
    calendar_4_4.set_today_date(2026, 10, 28)
    calendar_4_4.set_month_shown(2026, 10)
    calendar_4_4_header = calendar_4_4.add_header_arrow()
    calendar_4_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_4_5
    buttonmatrix_4_5 = lv.buttonmatrix(parent)
    objects["buttonmatrix_4_5"] = buttonmatrix_4_5
    buttonmatrix_4_5.set_pos(678, 372)
    buttonmatrix_4_5.set_size(95, 15)
    buttonmatrix_4_5_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_4_5.set_map(buttonmatrix_4_5_map)
    buttonmatrix_4_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_4_5.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_4_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_4_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # chart: chart_4_6
    chart_4_6 = lv.chart(parent)
    objects["chart_4_6"] = chart_4_6
    chart_4_6.set_pos(667, 315)
    chart_4_6.set_size(122, 68)
    chart_4_6.set_type(lv.chart.TYPE.LINE)
    chart_4_6.set_point_count(10)
    chart_4_6.set_div_line_count(3, 5)
    chart_4_6.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_4_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_4_6_series_1 = chart_4_6.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_4_6.set_next_value(chart_4_6_series_1, 10)
    chart_4_6.set_next_value(chart_4_6_series_1, 20)
    chart_4_6.set_next_value(chart_4_6_series_1, 30)
    chart_4_6.set_next_value(chart_4_6_series_1, 25)
    chart_4_6.set_next_value(chart_4_6_series_1, 40)
    chart_4_6.set_next_value(chart_4_6_series_1, 35)
    chart_4_6.set_next_value(chart_4_6_series_1, 50)

    # slider: slider_4_7
    slider_4_7 = lv.slider(parent)
    objects["slider_4_7"] = slider_4_7
    slider_4_7.set_pos(503, 123)
    slider_4_7.set_size(185, 148)
    slider_4_7.set_range(0, 100)
    slider_4_7.set_value(50, False)
    slider_4_7.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_4_7.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_4_7.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_4_7.add_event_cb(slider_4_7_changed, lv.EVENT.VALUE_CHANGED, None)


def random_4_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_4_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_4_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_4_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_4_get_current_page():
    return current_screen

def random_4_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_4_load_page(0)
