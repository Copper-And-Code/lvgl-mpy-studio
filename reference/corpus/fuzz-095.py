"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 95
Generated: 2023-11-14T22:15:27.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_95_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # span: span_95_0
    span_95_0 = lv.spangroup(parent)
    objects["span_95_0"] = span_95_0
    span_95_0.set_pos(195, 324)
    span_95_0.set_size(226, 118)
    span_95_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_95_0_span_1 = span_95_0.add_span()
    span_95_0_span_1.set_text("Normal text")
    span_95_0_span_1_style = span_95_0_span_1.get_style()
    span_95_0_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_95_0_span_1_style.set_text_font(lv.font_montserrat_14)
    span_95_0_span_2 = span_95_0.add_span()
    span_95_0_span_2.set_text("Bold text")
    span_95_0_span_2_style = span_95_0_span_2.get_style()
    span_95_0_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_95_0_span_2_style.set_text_font(lv.font_montserrat_16)
    span_95_0_span_3 = span_95_0.add_span()
    span_95_0_span_3.set_text("Small text")
    span_95_0_span_3_style = span_95_0_span_3.get_style()
    span_95_0_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_95_0_span_3_style.set_text_font(lv.font_montserrat_14)
    span_95_0.refresh()

    # switch: switch_95_1
    switch_95_1 = lv.switch(parent)
    objects["switch_95_1"] = switch_95_1
    switch_95_1.set_pos(141, 29)
    switch_95_1.set_size(195, 123)
    switch_95_1.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_95_1.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_95_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # led: led_95_2
    led_95_2 = lv.led(parent)
    objects["led_95_2"] = led_95_2
    led_95_2.set_pos(276, 25)
    led_95_2.set_size(101, 63)
    led_95_2.set_color(lv.color_hex(0xFF0000))
    led_95_2.set_brightness(255)

    # keyboard: keyboard_95_3
    keyboard_95_3 = lv.keyboard(parent)
    objects["keyboard_95_3"] = keyboard_95_3
    keyboard_95_3.set_pos(658, 342)
    keyboard_95_3.set_size(65, 79)


def random_95_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_95_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_95_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_95_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_95_get_current_page():
    return current_screen

def random_95_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_95_load_page(0)
