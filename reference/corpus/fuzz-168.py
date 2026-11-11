"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 168
Generated: 2023-11-14T22:16:40.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_168_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # led: led_168_0
    led_168_0 = lv.led(parent)
    objects["led_168_0"] = led_168_0
    led_168_0.set_pos(139, 201)
    led_168_0.set_size(244, 110)
    led_168_0.set_color(lv.color_hex(0xFF0000))
    led_168_0.set_brightness(255)

    # label: label_168_1
    label_168_1 = lv.label(parent)
    objects["label_168_1"] = label_168_1
    label_168_1.set_pos(235, 108)
    label_168_1.set_size(228, 154)
    label_168_1.set_text("Testo 168:1 \" \\ Città")
    label_168_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_168_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_168_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # arc: arc_168_2
    arc_168_2 = lv.arc(parent)
    objects["arc_168_2"] = arc_168_2
    arc_168_2.set_pos(113, 12)
    arc_168_2.set_size(144, 34)
    arc_168_2.set_bg_angles(135, 45)
    arc_168_2.set_range(0, 100)
    arc_168_2.set_value(50)
    arc_168_2.set_style_arc_width(10, lv.PART.MAIN)
    arc_168_2.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_168_2.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_168_2.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_168_2.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)


def random_168_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_168_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_168_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_168_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_168_get_current_page():
    return current_screen

def random_168_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_168_load_page(0)
