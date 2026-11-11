"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 46
Generated: 2023-11-14T22:14:38.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_46_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinbox: spinbox_46_0
    spinbox_46_0 = lv.spinbox(parent)
    objects["spinbox_46_0"] = spinbox_46_0
    spinbox_46_0.set_pos(425, 4)
    spinbox_46_0.set_size(145, 87)
    spinbox_46_0.set_digit_format(4, 0)
    spinbox_46_0.set_range(0, 999)
    spinbox_46_0.set_value(0)
    spinbox_46_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_46_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_46_0.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # led: led_46_1
    led_46_1 = lv.led(parent)
    objects["led_46_1"] = led_46_1
    led_46_1.set_pos(652, 84)
    led_46_1.set_size(64, 62)
    led_46_1.set_color(lv.color_hex(0xFF0000))
    led_46_1.set_brightness(255)

    # keyboard: keyboard_46_2
    keyboard_46_2 = lv.keyboard(parent)
    objects["keyboard_46_2"] = keyboard_46_2
    keyboard_46_2.set_pos(462, 127)
    keyboard_46_2.set_size(231, 97)


def random_46_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_46_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_46_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_46_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_46_get_current_page():
    return current_screen

def random_46_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_46_load_page(0)
