"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 70
Generated: 2023-11-14T22:15:02.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_70_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # line: line_70_0
    line_70_0 = lv.line(parent)
    objects["line_70_0"] = line_70_0
    line_70_0.set_pos(462, 306)
    line_70_0_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_70_0.set_points(line_70_0_points, 2)
    line_70_0.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_70_0.set_style_line_width(2, lv.PART.MAIN)

    # scale: scale_70_1
    scale_70_1 = lv.scale(parent)
    objects["scale_70_1"] = scale_70_1
    scale_70_1.set_pos(455, 131)
    scale_70_1.set_size(175, 143)
    scale_70_1.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_70_1.set_range(0, 100)
    scale_70_1.set_total_tick_count(51)
    scale_70_1.set_major_tick_every(5)
    scale_70_1.set_style_length(15, lv.PART.INDICATOR)
    scale_70_1.set_style_length(8, lv.PART.ITEMS)
    scale_70_1.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_70_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)


def random_70_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_70_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_70_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_70_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_70_get_current_page():
    return current_screen

def random_70_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_70_load_page(0)
