"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 32
Generated: 2023-11-14T22:14:24.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_32_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_32_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # led: led_32_0
    led_32_0 = lv.led(parent)
    objects["led_32_0"] = led_32_0
    led_32_0.set_pos(666, 179)
    led_32_0.set_size(161, 159)
    led_32_0.set_color(lv.color_hex(0xFF0000))
    led_32_0.set_brightness(255)

    # slider: slider_32_1
    slider_32_1 = lv.slider(parent)
    objects["slider_32_1"] = slider_32_1
    slider_32_1.set_pos(153, 284)
    slider_32_1.set_size(256, 132)
    slider_32_1.set_range(0, 100)
    slider_32_1.set_value(50, False)
    slider_32_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_32_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_32_1.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_32_1.add_event_cb(slider_32_1_changed, lv.EVENT.VALUE_CHANGED, None)


def random_32_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_32_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_32_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_32_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_32_get_current_page():
    return current_screen

def random_32_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_32_load_page(0)
