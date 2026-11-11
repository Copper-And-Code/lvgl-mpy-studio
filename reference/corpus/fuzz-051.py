"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 51
Generated: 2023-11-14T22:14:43.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def textarea_51_5_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_51_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # chart: chart_51_0
    chart_51_0 = lv.chart(parent)
    objects["chart_51_0"] = chart_51_0
    chart_51_0.set_pos(477, 5)
    chart_51_0.set_size(141, 16)
    chart_51_0.set_type(lv.chart.TYPE.LINE)
    chart_51_0.set_point_count(10)
    chart_51_0.set_div_line_count(3, 5)
    chart_51_0.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_51_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_51_0_series_1 = chart_51_0.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_51_0.set_next_value(chart_51_0_series_1, 10)
    chart_51_0.set_next_value(chart_51_0_series_1, 20)
    chart_51_0.set_next_value(chart_51_0_series_1, 30)
    chart_51_0.set_next_value(chart_51_0_series_1, 25)
    chart_51_0.set_next_value(chart_51_0_series_1, 40)
    chart_51_0.set_next_value(chart_51_0_series_1, 35)
    chart_51_0.set_next_value(chart_51_0_series_1, 50)

    # imagebutton: imagebutton_51_1
    imagebutton_51_1 = lv.imagebutton(parent)
    objects["imagebutton_51_1"] = imagebutton_51_1
    imagebutton_51_1.set_pos(318, 342)
    imagebutton_51_1.set_size(128, 127)
    imagebutton_51_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_51_1.set_style_radius(5, lv.PART.MAIN)
    imagebutton_51_1_label = lv.label(imagebutton_51_1)
    imagebutton_51_1_label.set_text("Testo 51:1 \" \\ Città")
    imagebutton_51_1_label.center()
    imagebutton_51_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_51_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # menu: menu_51_2
    menu_51_2 = lv.obj(parent)
    objects["menu_51_2"] = menu_51_2
    menu_51_2.set_pos(24, 374)
    menu_51_2.set_size(205, 151)
    menu_51_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_51_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_51_2_title = lv.label(menu_51_2)
    menu_51_2_title.set_text("Menu")
    menu_51_2_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_51_2_item_1 = lv.button(menu_51_2)
    menu_51_2_item_1.set_width(lv.pct(100))
    menu_51_2_item_1_label = lv.label(menu_51_2_item_1)
    menu_51_2_item_1_label.set_text("Item 1")
    menu_51_2_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_51_2_item_2 = lv.button(menu_51_2)
    menu_51_2_item_2.set_width(lv.pct(100))
    menu_51_2_item_2_label = lv.label(menu_51_2_item_2)
    menu_51_2_item_2_label.set_text("Item 2")
    menu_51_2_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_51_2_item_3 = lv.button(menu_51_2)
    menu_51_2_item_3.set_width(lv.pct(100))
    menu_51_2_item_3_label = lv.label(menu_51_2_item_3)
    menu_51_2_item_3_label.set_text("Item 3")
    menu_51_2_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_51_2_item_4 = lv.button(menu_51_2)
    menu_51_2_item_4.set_width(lv.pct(100))
    menu_51_2_item_4_label = lv.label(menu_51_2_item_4)
    menu_51_2_item_4_label.set_text("Item 4")
    menu_51_2_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # calendar: calendar_51_3
    calendar_51_3 = lv.calendar(parent)
    objects["calendar_51_3"] = calendar_51_3
    calendar_51_3.set_pos(181, 188)
    calendar_51_3.set_size(207, 27)
    calendar_51_3.set_today_date(2026, 10, 28)
    calendar_51_3.set_month_shown(2026, 10)
    calendar_51_3_header = calendar_51_3.add_header_arrow()
    calendar_51_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # msgbox: msgbox_51_4
    msgbox_51_4 = lv.msgbox(parent)
    objects["msgbox_51_4"] = msgbox_51_4
    msgbox_51_4.set_pos(421, 130)
    msgbox_51_4.set_size(108, 104)
    msgbox_51_4_title = msgbox_51_4.add_title("Notice")
    msgbox_51_4_text = msgbox_51_4.add_text("Testo 51:4 \" \\ Città")
    msgbox_51_4_button_1 = msgbox_51_4.add_footer_button("OK")
    msgbox_51_4_button_2 = msgbox_51_4.add_footer_button("Cancel")
    msgbox_51_4_close = msgbox_51_4.add_close_button()
    msgbox_51_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # textarea: textarea_51_5
    textarea_51_5 = lv.textarea(parent)
    objects["textarea_51_5"] = textarea_51_5
    textarea_51_5.set_pos(16, 92)
    textarea_51_5.set_size(184, 129)
    textarea_51_5.set_text("Testo 51:5 \" \\ Città")
    textarea_51_5.set_placeholder_text("Type here")
    textarea_51_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_51_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_51_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    textarea_51_5.add_event_cb(textarea_51_5_changed, lv.EVENT.VALUE_CHANGED, None)

    # textarea: textarea_51_6
    textarea_51_6 = lv.textarea(parent)
    objects["textarea_51_6"] = textarea_51_6
    textarea_51_6.set_pos(488, 85)
    textarea_51_6.set_size(158, 31)
    textarea_51_6.set_text("Testo 51:6 \" \\ Città")
    textarea_51_6.set_placeholder_text("Type here")
    textarea_51_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_51_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_51_6.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_51_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_51_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_51_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_51_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_51_get_current_page():
    return current_screen

def random_51_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_51_load_page(0)
