"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 147
Generated: 2023-11-14T22:16:19.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_147_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # led: led_147_0
    led_147_0 = lv.led(parent)
    objects["led_147_0"] = led_147_0
    led_147_0.set_pos(688, 195)
    led_147_0.set_size(127, 15)
    led_147_0.set_color(lv.color_hex(0xFF0000))
    led_147_0.set_brightness(255)

    # imagebutton: imagebutton_147_1
    imagebutton_147_1 = lv.imagebutton(parent)
    objects["imagebutton_147_1"] = imagebutton_147_1
    imagebutton_147_1.set_pos(337, 106)
    imagebutton_147_1.set_size(182, 127)
    imagebutton_147_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_147_1.set_style_radius(5, lv.PART.MAIN)
    imagebutton_147_1_label = lv.label(imagebutton_147_1)
    imagebutton_147_1_label.set_text("Testo 147:1 \" \\ Città")
    imagebutton_147_1_label.center()
    imagebutton_147_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_147_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # keyboard: keyboard_147_2
    keyboard_147_2 = lv.keyboard(parent)
    objects["keyboard_147_2"] = keyboard_147_2
    keyboard_147_2.set_pos(23, 223)
    keyboard_147_2.set_size(200, 23)

    # roller: roller_147_3
    roller_147_3 = lv.roller(parent)
    objects["roller_147_3"] = roller_147_3
    roller_147_3.set_pos(506, 368)
    roller_147_3.set_size(267, 50)
    roller_147_3.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_147_3.set_visible_row_count(3)
    roller_147_3.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_147_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_147_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_147_3.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_147_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_147_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_147_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_147_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_147_get_current_page():
    return current_screen

def random_147_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_147_load_page(0)
