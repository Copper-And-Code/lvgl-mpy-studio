"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 155
Generated: 2023-11-14T22:16:27.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_155_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # textarea: textarea_155_0
    textarea_155_0 = lv.textarea(parent)
    objects["textarea_155_0"] = textarea_155_0
    textarea_155_0.set_pos(371, 313)
    textarea_155_0.set_size(101, 74)
    textarea_155_0.set_text("Testo 155:0 \" \\ Città")
    textarea_155_0.set_placeholder_text("Type here")
    textarea_155_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_155_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_155_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # imagebutton: imagebutton_155_1
    imagebutton_155_1 = lv.imagebutton(parent)
    objects["imagebutton_155_1"] = imagebutton_155_1
    imagebutton_155_1.set_pos(177, 43)
    imagebutton_155_1.set_size(86, 67)
    imagebutton_155_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_155_1.set_style_radius(5, lv.PART.MAIN)
    imagebutton_155_1_label = lv.label(imagebutton_155_1)
    imagebutton_155_1_label.set_text("Testo 155:1 \" \\ Città")
    imagebutton_155_1_label.center()
    imagebutton_155_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_155_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # led: led_155_2
    led_155_2 = lv.led(parent)
    objects["led_155_2"] = led_155_2
    led_155_2.set_pos(175, 110)
    led_155_2.set_size(263, 20)
    led_155_2.set_color(lv.color_hex(0xFF0000))
    led_155_2.set_brightness(255)


def random_155_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_155_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_155_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_155_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_155_get_current_page():
    return current_screen

def random_155_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_155_load_page(0)
