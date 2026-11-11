"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 90
Generated: 2023-11-14T22:15:22.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_90_3_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_90_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: win_90_0
    win_90_0 = lv.obj(parent)
    objects["win_90_0"] = win_90_0
    win_90_0.set_pos(206, 330)
    win_90_0.set_size(94, 85)
    win_90_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_90_0.set_style_pad_all(0, lv.PART.MAIN)
    win_90_0.set_style_pad_row(0, lv.PART.MAIN)
    win_90_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_90_0_header = lv.obj(win_90_0)
    win_90_0_header.set_size(lv.pct(100), 40)
    win_90_0_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_90_0_header.set_style_radius(0, lv.PART.MAIN)
    win_90_0_title = lv.label(win_90_0_header)
    win_90_0_title.set_text("Window Title")
    win_90_0_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_90_0_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_90_0_content = lv.obj(win_90_0)
    win_90_0_content.set_width(lv.pct(100))
    win_90_0_content.set_flex_grow(1)

    # arc: arc_90_1
    arc_90_1 = lv.arc(parent)
    objects["arc_90_1"] = arc_90_1
    arc_90_1.set_pos(618, 398)
    arc_90_1.set_size(215, 129)
    arc_90_1.set_bg_angles(135, 45)
    arc_90_1.set_range(0, 100)
    arc_90_1.set_value(50)
    arc_90_1.set_style_arc_width(10, lv.PART.MAIN)
    arc_90_1.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_90_1.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_90_1.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_90_1.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # image: image_90_2
    image_90_2 = lv.image(parent)
    objects["image_90_2"] = image_90_2
    image_90_2.set_pos(388, 255)
    image_90_2.set_size(66, 74)

    # slider: slider_90_3
    slider_90_3 = lv.slider(parent)
    objects["slider_90_3"] = slider_90_3
    slider_90_3.set_pos(2, 323)
    slider_90_3.set_size(223, 146)
    slider_90_3.set_range(0, 100)
    slider_90_3.set_value(50, False)
    slider_90_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_90_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_90_3.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_90_3.add_event_cb(slider_90_3_changed, lv.EVENT.VALUE_CHANGED, None)

    # chart: chart_90_4
    chart_90_4 = lv.chart(parent)
    objects["chart_90_4"] = chart_90_4
    chart_90_4.set_pos(149, 40)
    chart_90_4.set_size(159, 49)
    chart_90_4.set_type(lv.chart.TYPE.LINE)
    chart_90_4.set_point_count(10)
    chart_90_4.set_div_line_count(3, 5)
    chart_90_4.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_90_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_90_4_series_1 = chart_90_4.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_90_4.set_next_value(chart_90_4_series_1, 10)
    chart_90_4.set_next_value(chart_90_4_series_1, 20)
    chart_90_4.set_next_value(chart_90_4_series_1, 30)
    chart_90_4.set_next_value(chart_90_4_series_1, 25)
    chart_90_4.set_next_value(chart_90_4_series_1, 40)
    chart_90_4.set_next_value(chart_90_4_series_1, 35)
    chart_90_4.set_next_value(chart_90_4_series_1, 50)

    # msgbox: msgbox_90_5
    msgbox_90_5 = lv.msgbox(parent)
    objects["msgbox_90_5"] = msgbox_90_5
    msgbox_90_5.set_pos(70, 51)
    msgbox_90_5.set_size(165, 54)
    msgbox_90_5_title = msgbox_90_5.add_title("Notice")
    msgbox_90_5_text = msgbox_90_5.add_text("Testo 90:5 \" \\ Città")
    msgbox_90_5_button_1 = msgbox_90_5.add_footer_button("OK")
    msgbox_90_5_button_2 = msgbox_90_5.add_footer_button("Cancel")
    msgbox_90_5_close = msgbox_90_5.add_close_button()
    msgbox_90_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_90_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_90_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_90_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_90_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_90_get_current_page():
    return current_screen

def random_90_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_90_load_page(0)
