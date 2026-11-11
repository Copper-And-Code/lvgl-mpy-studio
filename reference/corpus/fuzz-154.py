"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 154
Generated: 2023-11-14T22:16:26.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def checkbox_154_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_154_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # span: span_154_0
    span_154_0 = lv.spangroup(parent)
    objects["span_154_0"] = span_154_0
    span_154_0.set_pos(152, 241)
    span_154_0.set_size(221, 55)
    span_154_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_154_0_span_1 = span_154_0.add_span()
    span_154_0_span_1.set_text("Normal text")
    span_154_0_span_1_style = span_154_0_span_1.get_style()
    span_154_0_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_154_0_span_1_style.set_text_font(lv.font_montserrat_14)
    span_154_0_span_2 = span_154_0.add_span()
    span_154_0_span_2.set_text("Bold text")
    span_154_0_span_2_style = span_154_0_span_2.get_style()
    span_154_0_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_154_0_span_2_style.set_text_font(lv.font_montserrat_16)
    span_154_0_span_3 = span_154_0.add_span()
    span_154_0_span_3.set_text("Small text")
    span_154_0_span_3_style = span_154_0_span_3.get_style()
    span_154_0_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_154_0_span_3_style.set_text_font(lv.font_montserrat_14)
    span_154_0.refresh()

    # checkbox: checkbox_154_1
    checkbox_154_1 = lv.checkbox(parent)
    objects["checkbox_154_1"] = checkbox_154_1
    checkbox_154_1.set_pos(127, 257)
    checkbox_154_1.set_text("Testo 154:1 \" \\ Città")
    checkbox_154_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_154_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_154_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_154_1.add_event_cb(checkbox_154_1_changed, lv.EVENT.VALUE_CHANGED, None)

    # bar: bar_154_2
    bar_154_2 = lv.bar(parent)
    objects["bar_154_2"] = bar_154_2
    bar_154_2.set_pos(625, 75)
    bar_154_2.set_size(76, 57)
    bar_154_2.set_range(0, 100)
    bar_154_2.set_value(50, False)
    bar_154_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_154_2.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # bar: bar_154_3
    bar_154_3 = lv.bar(parent)
    objects["bar_154_3"] = bar_154_3
    bar_154_3.set_pos(320, 97)
    bar_154_3.set_size(157, 28)
    bar_154_3.set_range(0, 100)
    bar_154_3.set_value(50, False)
    bar_154_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_154_3.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # arc: arc_154_4
    arc_154_4 = lv.arc(parent)
    objects["arc_154_4"] = arc_154_4
    arc_154_4.set_pos(3, 115)
    arc_154_4.set_size(101, 25)
    arc_154_4.set_bg_angles(135, 45)
    arc_154_4.set_range(0, 100)
    arc_154_4.set_value(50)
    arc_154_4.set_style_arc_width(10, lv.PART.MAIN)
    arc_154_4.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_154_4.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_154_4.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_154_4.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # msgbox: msgbox_154_5
    msgbox_154_5 = lv.msgbox(parent)
    objects["msgbox_154_5"] = msgbox_154_5
    msgbox_154_5.set_pos(406, 295)
    msgbox_154_5.set_size(173, 45)
    msgbox_154_5_title = msgbox_154_5.add_title("Notice")
    msgbox_154_5_text = msgbox_154_5.add_text("Testo 154:5 \" \\ Città")
    msgbox_154_5_button_1 = msgbox_154_5.add_footer_button("OK")
    msgbox_154_5_button_2 = msgbox_154_5.add_footer_button("Cancel")
    msgbox_154_5_close = msgbox_154_5.add_close_button()
    msgbox_154_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # tabview: tabview_154_6
    tabview_154_6 = lv.tabview(parent)
    objects["tabview_154_6"] = tabview_154_6
    tabview_154_6.set_pos(676, 222)
    tabview_154_6.set_size(212, 87)
    tabview_154_6.set_tab_bar_position(lv.DIR.TOP)
    tabview_154_6.set_tab_bar_size(40)
    tabview_154_6_tab_1 = tabview_154_6.add_tab("Tab 1")
    tabview_154_6_tab_2 = tabview_154_6.add_tab("Tab 2")
    tabview_154_6_tab_3 = tabview_154_6.add_tab("Tab 3")
    tabview_154_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # led: led_154_7
    led_154_7 = lv.led(parent)
    objects["led_154_7"] = led_154_7
    led_154_7.set_pos(252, 112)
    led_154_7.set_size(54, 142)
    led_154_7.set_color(lv.color_hex(0xFF0000))
    led_154_7.set_brightness(255)


def random_154_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_154_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_154_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_154_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_154_get_current_page():
    return current_screen

def random_154_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_154_load_page(0)
