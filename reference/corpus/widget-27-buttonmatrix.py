"""
Auto-generated LVGL UI Code for MicroPython
Project: One buttonmatrix
Generated: 2023-11-14T22:13:46.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_buttonmatrix_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # buttonmatrix: Button Matrix_w26
    button_matrix_w26 = lv.buttonmatrix(parent)
    objects["button_matrix_w26"] = button_matrix_w26
    button_matrix_w26.set_pos(98, 82)
    button_matrix_w26.set_size(250, 120)
    button_matrix_w26_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    button_matrix_w26.set_map(button_matrix_w26_map)
    button_matrix_w26.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_matrix_w26.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    button_matrix_w26.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    button_matrix_w26.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def one_buttonmatrix_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_buttonmatrix_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_buttonmatrix_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_buttonmatrix_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_buttonmatrix_get_current_page():
    return current_screen

def one_buttonmatrix_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_buttonmatrix_load_page(0)
