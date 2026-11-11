"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 121
Generated: 2023-11-14T22:15:53.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_121_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # image: image_121_0
    image_121_0 = lv.image(parent)
    objects["image_121_0"] = image_121_0
    image_121_0.set_pos(383, 228)
    image_121_0.set_size(117, 152)

    # image: image_121_1
    image_121_1 = lv.image(parent)
    objects["image_121_1"] = image_121_1
    image_121_1.set_pos(55, 127)
    image_121_1.set_size(110, 145)

    # scale: scale_121_2
    scale_121_2 = lv.scale(parent)
    objects["scale_121_2"] = scale_121_2
    scale_121_2.set_pos(514, 128)
    scale_121_2.set_size(236, 48)
    scale_121_2.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_121_2.set_range(0, 100)
    scale_121_2.set_total_tick_count(51)
    scale_121_2.set_major_tick_every(5)
    scale_121_2.set_style_length(15, lv.PART.INDICATOR)
    scale_121_2.set_style_length(8, lv.PART.ITEMS)
    scale_121_2.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_121_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)


def random_121_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_121_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_121_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_121_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_121_get_current_page():
    return current_screen

def random_121_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_121_load_page(0)
