"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 186
Generated: 2023-11-14T22:16:58.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_186_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # msgbox: msgbox_186_0
    msgbox_186_0 = lv.msgbox(parent)
    objects["msgbox_186_0"] = msgbox_186_0
    msgbox_186_0.set_pos(549, 45)
    msgbox_186_0.set_size(246, 43)
    msgbox_186_0_title = msgbox_186_0.add_title("Notice")
    msgbox_186_0_text = msgbox_186_0.add_text("Testo 186:0 \" \\ Città")
    msgbox_186_0_button_1 = msgbox_186_0.add_footer_button("OK")
    msgbox_186_0_button_2 = msgbox_186_0.add_footer_button("Cancel")
    msgbox_186_0_close = msgbox_186_0.add_close_button()
    msgbox_186_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # checkbox: checkbox_186_1
    checkbox_186_1 = lv.checkbox(parent)
    objects["checkbox_186_1"] = checkbox_186_1
    checkbox_186_1.set_pos(18, 72)
    checkbox_186_1.set_text("Testo 186:1 \" \\ Città")
    checkbox_186_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_186_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_186_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # led: led_186_2
    led_186_2 = lv.led(parent)
    objects["led_186_2"] = led_186_2
    led_186_2.set_pos(365, 364)
    led_186_2.set_size(229, 42)
    led_186_2.set_color(lv.color_hex(0xFF0000))
    led_186_2.set_brightness(255)

    # keyboard: keyboard_186_3
    keyboard_186_3 = lv.keyboard(parent)
    objects["keyboard_186_3"] = keyboard_186_3
    keyboard_186_3.set_pos(503, 183)
    keyboard_186_3.set_size(124, 107)

    # list: list_186_4
    list_186_4 = lv.obj(parent)
    objects["list_186_4"] = list_186_4
    list_186_4.set_pos(629, 395)
    list_186_4.set_size(46, 29)
    list_186_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_186_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_186_4_item_1 = lv.button(list_186_4)
    list_186_4_item_1.set_width(lv.pct(100))
    list_186_4_item_1_label = lv.label(list_186_4_item_1)
    list_186_4_item_1_label.set_text("Item 1")
    list_186_4_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_186_4_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_186_4_item_2 = lv.button(list_186_4)
    list_186_4_item_2.set_width(lv.pct(100))
    list_186_4_item_2_label = lv.label(list_186_4_item_2)
    list_186_4_item_2_label.set_text("Item 2")
    list_186_4_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_186_4_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_186_4_item_3 = lv.button(list_186_4)
    list_186_4_item_3.set_width(lv.pct(100))
    list_186_4_item_3_label = lv.label(list_186_4_item_3)
    list_186_4_item_3_label.set_text("Item 3")
    list_186_4_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_186_4_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_186_4_item_4 = lv.button(list_186_4)
    list_186_4_item_4.set_width(lv.pct(100))
    list_186_4_item_4_label = lv.label(list_186_4_item_4)
    list_186_4_item_4_label.set_text("Item 4")
    list_186_4_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_186_4_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_186_4_item_5 = lv.button(list_186_4)
    list_186_4_item_5.set_width(lv.pct(100))
    list_186_4_item_5_label = lv.label(list_186_4_item_5)
    list_186_4_item_5_label.set_text("Item 5")
    list_186_4_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_186_4_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # msgbox: msgbox_186_5
    msgbox_186_5 = lv.msgbox(parent)
    objects["msgbox_186_5"] = msgbox_186_5
    msgbox_186_5.set_pos(671, 140)
    msgbox_186_5.set_size(133, 30)
    msgbox_186_5_title = msgbox_186_5.add_title("Notice")
    msgbox_186_5_text = msgbox_186_5.add_text("Testo 186:5 \" \\ Città")
    msgbox_186_5_button_1 = msgbox_186_5.add_footer_button("OK")
    msgbox_186_5_button_2 = msgbox_186_5.add_footer_button("Cancel")
    msgbox_186_5_close = msgbox_186_5.add_close_button()
    msgbox_186_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # button: button_186_6
    button_186_6 = lv.button(parent)
    objects["button_186_6"] = button_186_6
    button_186_6.set_pos(7, 184)
    button_186_6.set_size(77, 67)
    button_186_6.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_186_6.set_style_radius(5, lv.PART.MAIN)
    button_186_6_label = lv.label(button_186_6)
    button_186_6_label.set_text("Testo 186:6 \" \\ Città")
    button_186_6_label.center()
    button_186_6_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_186_6_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # span: span_186_7
    span_186_7 = lv.spangroup(parent)
    objects["span_186_7"] = span_186_7
    span_186_7.set_pos(662, 327)
    span_186_7.set_size(151, 90)
    span_186_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_186_7_span_1 = span_186_7.add_span()
    span_186_7_span_1.set_text("Normal text")
    span_186_7_span_1_style = span_186_7_span_1.get_style()
    span_186_7_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_186_7_span_1_style.set_text_font(lv.font_montserrat_14)
    span_186_7_span_2 = span_186_7.add_span()
    span_186_7_span_2.set_text("Bold text")
    span_186_7_span_2_style = span_186_7_span_2.get_style()
    span_186_7_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_186_7_span_2_style.set_text_font(lv.font_montserrat_16)
    span_186_7_span_3 = span_186_7.add_span()
    span_186_7_span_3.set_text("Small text")
    span_186_7_span_3_style = span_186_7_span_3.get_style()
    span_186_7_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_186_7_span_3_style.set_text_font(lv.font_montserrat_14)
    span_186_7.refresh()


def random_186_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_186_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_186_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_186_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_186_get_current_page():
    return current_screen

def random_186_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_186_load_page(0)
