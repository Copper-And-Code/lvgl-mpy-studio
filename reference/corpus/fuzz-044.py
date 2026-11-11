"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 44
Generated: 2023-11-14T22:14:36.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_44_5_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_44_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # span: span_44_0
    span_44_0 = lv.spangroup(parent)
    objects["span_44_0"] = span_44_0
    span_44_0.set_pos(690, 269)
    span_44_0.set_size(254, 144)
    span_44_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_44_0_span_1 = span_44_0.add_span()
    span_44_0_span_1.set_text("Normal text")
    span_44_0_span_1_style = span_44_0_span_1.get_style()
    span_44_0_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_44_0_span_1_style.set_text_font(lv.font_montserrat_14)
    span_44_0_span_2 = span_44_0.add_span()
    span_44_0_span_2.set_text("Bold text")
    span_44_0_span_2_style = span_44_0_span_2.get_style()
    span_44_0_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_44_0_span_2_style.set_text_font(lv.font_montserrat_16)
    span_44_0_span_3 = span_44_0.add_span()
    span_44_0_span_3.set_text("Small text")
    span_44_0_span_3_style = span_44_0_span_3.get_style()
    span_44_0_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_44_0_span_3_style.set_text_font(lv.font_montserrat_14)
    span_44_0.refresh()

    # list: list_44_1
    list_44_1 = lv.obj(parent)
    objects["list_44_1"] = list_44_1
    list_44_1.set_pos(560, 367)
    list_44_1.set_size(130, 67)
    list_44_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_44_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_44_1_item_1 = lv.button(list_44_1)
    list_44_1_item_1.set_width(lv.pct(100))
    list_44_1_item_1_label = lv.label(list_44_1_item_1)
    list_44_1_item_1_label.set_text("Item 1")
    list_44_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_44_1_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_44_1_item_2 = lv.button(list_44_1)
    list_44_1_item_2.set_width(lv.pct(100))
    list_44_1_item_2_label = lv.label(list_44_1_item_2)
    list_44_1_item_2_label.set_text("Item 2")
    list_44_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_44_1_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_44_1_item_3 = lv.button(list_44_1)
    list_44_1_item_3.set_width(lv.pct(100))
    list_44_1_item_3_label = lv.label(list_44_1_item_3)
    list_44_1_item_3_label.set_text("Item 3")
    list_44_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_44_1_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_44_1_item_4 = lv.button(list_44_1)
    list_44_1_item_4.set_width(lv.pct(100))
    list_44_1_item_4_label = lv.label(list_44_1_item_4)
    list_44_1_item_4_label.set_text("Item 4")
    list_44_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_44_1_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_44_1_item_5 = lv.button(list_44_1)
    list_44_1_item_5.set_width(lv.pct(100))
    list_44_1_item_5_label = lv.label(list_44_1_item_5)
    list_44_1_item_5_label.set_text("Item 5")
    list_44_1_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_44_1_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # label: label_44_2
    label_44_2 = lv.label(parent)
    objects["label_44_2"] = label_44_2
    label_44_2.set_pos(619, 24)
    label_44_2.set_size(58, 97)
    label_44_2.set_text("Testo 44:2 \" \\ Città")
    label_44_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_44_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_44_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # chart: chart_44_3
    chart_44_3 = lv.chart(parent)
    objects["chart_44_3"] = chart_44_3
    chart_44_3.set_pos(340, 82)
    chart_44_3.set_size(177, 62)
    chart_44_3.set_type(lv.chart.TYPE.LINE)
    chart_44_3.set_point_count(10)
    chart_44_3.set_div_line_count(3, 5)
    chart_44_3.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_44_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_44_3_series_1 = chart_44_3.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_44_3.set_next_value(chart_44_3_series_1, 10)
    chart_44_3.set_next_value(chart_44_3_series_1, 20)
    chart_44_3.set_next_value(chart_44_3_series_1, 30)
    chart_44_3.set_next_value(chart_44_3_series_1, 25)
    chart_44_3.set_next_value(chart_44_3_series_1, 40)
    chart_44_3.set_next_value(chart_44_3_series_1, 35)
    chart_44_3.set_next_value(chart_44_3_series_1, 50)

    # msgbox: msgbox_44_4
    msgbox_44_4 = lv.msgbox(parent)
    objects["msgbox_44_4"] = msgbox_44_4
    msgbox_44_4.set_pos(323, 187)
    msgbox_44_4.set_size(183, 80)
    msgbox_44_4_title = msgbox_44_4.add_title("Notice")
    msgbox_44_4_text = msgbox_44_4.add_text("Testo 44:4 \" \\ Città")
    msgbox_44_4_button_1 = msgbox_44_4.add_footer_button("OK")
    msgbox_44_4_button_2 = msgbox_44_4.add_footer_button("Cancel")
    msgbox_44_4_close = msgbox_44_4.add_close_button()
    msgbox_44_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # slider: slider_44_5
    slider_44_5 = lv.slider(parent)
    objects["slider_44_5"] = slider_44_5
    slider_44_5.set_pos(104, 56)
    slider_44_5.set_size(140, 73)
    slider_44_5.set_range(0, 100)
    slider_44_5.set_value(50, False)
    slider_44_5.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_44_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_44_5.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_44_5.add_event_cb(slider_44_5_changed, lv.EVENT.VALUE_CHANGED, None)


def random_44_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_44_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_44_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_44_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_44_get_current_page():
    return current_screen

def random_44_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_44_load_page(0)
