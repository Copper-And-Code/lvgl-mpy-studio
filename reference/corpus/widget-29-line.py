"""
Auto-generated LVGL UI Code for MicroPython
Project: One line
Generated: 2023-11-14T22:13:48.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_line_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # line: Line_w28
    line_w28 = lv.line(parent)
    objects["line_w28"] = line_w28
    line_w28.set_pos(104, 86)
    line_w28_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_w28.set_points(line_w28_points, 2)
    line_w28.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_w28.set_style_line_width(2, lv.PART.MAIN)


def one_line_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_line_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_line_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_line_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_line_get_current_page():
    return current_screen

def one_line_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_line_load_page(0)
