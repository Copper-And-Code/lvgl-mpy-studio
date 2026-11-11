"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 199
Generated: 2023-11-14T22:17:11.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_199_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tileview: tileview_199_0
    tileview_199_0 = lv.tileview(parent)
    objects["tileview_199_0"] = tileview_199_0
    tileview_199_0.set_pos(421, 346)
    tileview_199_0.set_size(86, 60)
    tileview_199_0.add_tile(0, 0, lv.DIR.ALL)
    tileview_199_0.add_tile(1, 0, lv.DIR.ALL)
    tileview_199_0.add_tile(0, 1, lv.DIR.ALL)
    tileview_199_0.add_tile(1, 1, lv.DIR.ALL)
    tileview_199_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # checkbox: checkbox_199_1
    checkbox_199_1 = lv.checkbox(parent)
    objects["checkbox_199_1"] = checkbox_199_1
    checkbox_199_1.set_pos(523, 375)
    checkbox_199_1.set_text("Testo 199:1 \" \\ Città")
    checkbox_199_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_199_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_199_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # keyboard: keyboard_199_2
    keyboard_199_2 = lv.keyboard(parent)
    objects["keyboard_199_2"] = keyboard_199_2
    keyboard_199_2.set_pos(273, 253)
    keyboard_199_2.set_size(133, 141)


def random_199_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_199_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_199_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_199_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_199_get_current_page():
    return current_screen

def random_199_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_199_load_page(0)
