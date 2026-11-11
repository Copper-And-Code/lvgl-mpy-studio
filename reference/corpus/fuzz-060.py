"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 60
Generated: 2023-11-14T22:14:52.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_60_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # imagebutton: imagebutton_60_0
    imagebutton_60_0 = lv.imagebutton(parent)
    objects["imagebutton_60_0"] = imagebutton_60_0
    imagebutton_60_0.set_pos(679, 124)
    imagebutton_60_0.set_size(84, 118)
    imagebutton_60_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_60_0.set_style_radius(5, lv.PART.MAIN)
    imagebutton_60_0_label = lv.label(imagebutton_60_0)
    imagebutton_60_0_label.set_text("Testo 60:0 \" \\ Città")
    imagebutton_60_0_label.center()
    imagebutton_60_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_60_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_60_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_60_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_60_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_60_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_60_get_current_page():
    return current_screen

def random_60_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_60_load_page(0)
