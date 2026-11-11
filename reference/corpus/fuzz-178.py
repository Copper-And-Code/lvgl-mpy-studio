"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 178
Generated: 2023-11-14T22:16:50.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_178_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # led: led_178_0
    led_178_0 = lv.led(parent)
    objects["led_178_0"] = led_178_0
    led_178_0.set_pos(523, 307)
    led_178_0.set_size(232, 37)
    led_178_0.set_color(lv.color_hex(0xFF0000))
    led_178_0.set_brightness(255)

    # line: line_178_1
    line_178_1 = lv.line(parent)
    objects["line_178_1"] = line_178_1
    line_178_1.set_pos(101, 192)
    line_178_1_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_178_1.set_points(line_178_1_points, 2)
    line_178_1.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_178_1.set_style_line_width(2, lv.PART.MAIN)

    # arc: arc_178_2
    arc_178_2 = lv.arc(parent)
    objects["arc_178_2"] = arc_178_2
    arc_178_2.set_pos(496, 292)
    arc_178_2.set_size(84, 106)
    arc_178_2.set_bg_angles(135, 45)
    arc_178_2.set_range(0, 100)
    arc_178_2.set_value(50)
    arc_178_2.set_style_arc_width(10, lv.PART.MAIN)
    arc_178_2.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_178_2.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_178_2.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_178_2.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)


def random_178_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_178_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_178_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_178_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_178_get_current_page():
    return current_screen

def random_178_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_178_load_page(0)
