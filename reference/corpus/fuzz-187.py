"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 187
Generated: 2023-11-14T22:16:59.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_187_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # TODO: handle lv.EVENT.CLICKED
        pass

screens = [None] * 1
current_screen = 0

def random_187_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # chart: chart_187_0
    chart_187_0 = lv.chart(parent)
    objects["chart_187_0"] = chart_187_0
    chart_187_0.set_pos(690, 249)
    chart_187_0.set_size(234, 151)
    chart_187_0.set_type(lv.chart.TYPE.LINE)
    chart_187_0.set_point_count(10)
    chart_187_0.set_div_line_count(3, 5)
    chart_187_0.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_187_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_187_0_series_1 = chart_187_0.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_187_0.set_next_value(chart_187_0_series_1, 10)
    chart_187_0.set_next_value(chart_187_0_series_1, 20)
    chart_187_0.set_next_value(chart_187_0_series_1, 30)
    chart_187_0.set_next_value(chart_187_0_series_1, 25)
    chart_187_0.set_next_value(chart_187_0_series_1, 40)
    chart_187_0.set_next_value(chart_187_0_series_1, 35)
    chart_187_0.set_next_value(chart_187_0_series_1, 50)

    # button: button_187_1
    button_187_1 = lv.button(parent)
    objects["button_187_1"] = button_187_1
    button_187_1.set_pos(369, 368)
    button_187_1.set_size(268, 128)
    button_187_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_187_1.set_style_radius(5, lv.PART.MAIN)
    button_187_1_label = lv.label(button_187_1)
    button_187_1_label.set_text("Testo 187:1 \" \\ Città")
    button_187_1_label.center()
    button_187_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_187_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_187_1.add_event_cb(button_187_1_changed, lv.EVENT.CLICKED, None)

    # button: button_187_2
    button_187_2 = lv.button(parent)
    objects["button_187_2"] = button_187_2
    button_187_2.set_pos(247, 268)
    button_187_2.set_size(95, 82)
    button_187_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_187_2.set_style_radius(5, lv.PART.MAIN)
    button_187_2_label = lv.label(button_187_2)
    button_187_2_label.set_text("Testo 187:2 \" \\ Città")
    button_187_2_label.center()
    button_187_2_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_187_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # msgbox: msgbox_187_3
    msgbox_187_3 = lv.msgbox(parent)
    objects["msgbox_187_3"] = msgbox_187_3
    msgbox_187_3.set_pos(586, 212)
    msgbox_187_3.set_size(229, 55)
    msgbox_187_3_title = msgbox_187_3.add_title("Notice")
    msgbox_187_3_text = msgbox_187_3.add_text("Testo 187:3 \" \\ Città")
    msgbox_187_3_button_1 = msgbox_187_3.add_footer_button("OK")
    msgbox_187_3_button_2 = msgbox_187_3.add_footer_button("Cancel")
    msgbox_187_3_close = msgbox_187_3.add_close_button()
    msgbox_187_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # win: win_187_4
    win_187_4 = lv.obj(parent)
    objects["win_187_4"] = win_187_4
    win_187_4.set_pos(354, 260)
    win_187_4.set_size(87, 16)
    win_187_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_187_4.set_style_pad_all(0, lv.PART.MAIN)
    win_187_4.set_style_pad_row(0, lv.PART.MAIN)
    win_187_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_187_4_header = lv.obj(win_187_4)
    win_187_4_header.set_size(lv.pct(100), 40)
    win_187_4_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_187_4_header.set_style_radius(0, lv.PART.MAIN)
    win_187_4_title = lv.label(win_187_4_header)
    win_187_4_title.set_text("Window Title")
    win_187_4_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_187_4_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_187_4_content = lv.obj(win_187_4)
    win_187_4_content.set_width(lv.pct(100))
    win_187_4_content.set_flex_grow(1)


def random_187_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_187_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_187_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_187_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_187_get_current_page():
    return current_screen

def random_187_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_187_load_page(0)
