"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 0
Generated: 2023-11-14T22:13:52.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_0_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # dropdown: dropdown_0_0
    dropdown_0_0 = lv.dropdown(parent)
    objects["dropdown_0_0"] = dropdown_0_0
    dropdown_0_0.set_pos(193, 168)
    dropdown_0_0.set_size(152, 13)
    dropdown_0_0.set_options("Option 1\nOption 2\nOption 3")
    dropdown_0_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_0_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_0_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # spinbox: spinbox_0_1
    spinbox_0_1 = lv.spinbox(parent)
    objects["spinbox_0_1"] = spinbox_0_1
    spinbox_0_1.set_pos(689, 72)
    spinbox_0_1.set_size(126, 13)
    spinbox_0_1.set_digit_format(4, 0)
    spinbox_0_1.set_range(0, 999)
    spinbox_0_1.set_value(0)
    spinbox_0_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_0_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_0_1.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # keyboard: keyboard_0_2
    keyboard_0_2 = lv.keyboard(parent)
    objects["keyboard_0_2"] = keyboard_0_2
    keyboard_0_2.set_pos(660, 291)
    keyboard_0_2.set_size(199, 55)


def random_0_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_0_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_0_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_0_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_0_get_current_page():
    return current_screen

def random_0_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_0_load_page(0)
