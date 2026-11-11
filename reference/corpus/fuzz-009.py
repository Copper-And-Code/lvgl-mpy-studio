"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 9
Generated: 2023-11-14T22:14:01.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_9_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # roller: roller_9_0
    roller_9_0 = lv.roller(parent)
    objects["roller_9_0"] = roller_9_0
    roller_9_0.set_pos(392, 90)
    roller_9_0.set_size(91, 155)
    roller_9_0.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_9_0.set_visible_row_count(3)
    roller_9_0.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_9_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_9_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_9_0.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_9_1
    buttonmatrix_9_1 = lv.buttonmatrix(parent)
    objects["buttonmatrix_9_1"] = buttonmatrix_9_1
    buttonmatrix_9_1.set_pos(408, 13)
    buttonmatrix_9_1.set_size(95, 114)
    buttonmatrix_9_1_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_9_1.set_map(buttonmatrix_9_1_map)
    buttonmatrix_9_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_9_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_9_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_9_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_9_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_9_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_9_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_9_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_9_get_current_page():
    return current_screen

def random_9_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_9_load_page(0)
