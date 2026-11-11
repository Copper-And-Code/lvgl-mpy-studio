"""
Auto-generated LVGL UI Code for MicroPython
Project: One image
Generated: 2023-11-14T22:13:38.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_image_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # image: Image_w18
    image_w18 = lv.image(parent)
    objects["image_w18"] = image_w18
    image_w18.set_pos(74, 66)
    image_w18.set_size(100, 100)


def one_image_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_image_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_image_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_image_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_image_get_current_page():
    return current_screen

def one_image_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_image_load_page(0)
