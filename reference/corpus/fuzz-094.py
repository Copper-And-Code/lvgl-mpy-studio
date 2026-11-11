"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 94
Generated: 2023-11-14T22:15:26.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_94_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # span: span_94_0
    span_94_0 = lv.spangroup(parent)
    objects["span_94_0"] = span_94_0
    span_94_0.set_pos(67, 376)
    span_94_0.set_size(112, 51)
    span_94_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_94_0_span_1 = span_94_0.add_span()
    span_94_0_span_1.set_text("Normal text")
    span_94_0_span_1_style = span_94_0_span_1.get_style()
    span_94_0_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_94_0_span_1_style.set_text_font(lv.font_montserrat_14)
    span_94_0_span_2 = span_94_0.add_span()
    span_94_0_span_2.set_text("Bold text")
    span_94_0_span_2_style = span_94_0_span_2.get_style()
    span_94_0_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_94_0_span_2_style.set_text_font(lv.font_montserrat_16)
    span_94_0_span_3 = span_94_0.add_span()
    span_94_0_span_3.set_text("Small text")
    span_94_0_span_3_style = span_94_0_span_3.get_style()
    span_94_0_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_94_0_span_3_style.set_text_font(lv.font_montserrat_14)
    span_94_0.refresh()

    # win: win_94_1
    win_94_1 = lv.obj(parent)
    objects["win_94_1"] = win_94_1
    win_94_1.set_pos(471, 361)
    win_94_1.set_size(135, 38)
    win_94_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_94_1.set_style_pad_all(0, lv.PART.MAIN)
    win_94_1.set_style_pad_row(0, lv.PART.MAIN)
    win_94_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_94_1_header = lv.obj(win_94_1)
    win_94_1_header.set_size(lv.pct(100), 40)
    win_94_1_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_94_1_header.set_style_radius(0, lv.PART.MAIN)
    win_94_1_title = lv.label(win_94_1_header)
    win_94_1_title.set_text("Window Title")
    win_94_1_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_94_1_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_94_1_content = lv.obj(win_94_1)
    win_94_1_content.set_width(lv.pct(100))
    win_94_1_content.set_flex_grow(1)

    # spinbox: spinbox_94_2
    spinbox_94_2 = lv.spinbox(parent)
    objects["spinbox_94_2"] = spinbox_94_2
    spinbox_94_2.set_pos(140, 335)
    spinbox_94_2.set_size(86, 59)
    spinbox_94_2.set_digit_format(4, 0)
    spinbox_94_2.set_range(0, 999)
    spinbox_94_2.set_value(0)
    spinbox_94_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_94_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_94_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # led: led_94_3
    led_94_3 = lv.led(parent)
    objects["led_94_3"] = led_94_3
    led_94_3.set_pos(323, 159)
    led_94_3.set_size(30, 45)
    led_94_3.set_color(lv.color_hex(0xFF0000))
    led_94_3.set_brightness(255)

    # label: label_94_4
    label_94_4 = lv.label(parent)
    objects["label_94_4"] = label_94_4
    label_94_4.set_pos(651, 327)
    label_94_4.set_size(212, 34)
    label_94_4.set_text("Testo 94:4 \" \\ Città")
    label_94_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_94_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_94_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # spinbox: spinbox_94_5
    spinbox_94_5 = lv.spinbox(parent)
    objects["spinbox_94_5"] = spinbox_94_5
    spinbox_94_5.set_pos(49, 153)
    spinbox_94_5.set_size(96, 132)
    spinbox_94_5.set_digit_format(4, 0)
    spinbox_94_5.set_range(0, 999)
    spinbox_94_5.set_value(0)
    spinbox_94_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_94_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_94_5.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_94_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_94_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_94_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_94_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_94_get_current_page():
    return current_screen

def random_94_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_94_load_page(0)
