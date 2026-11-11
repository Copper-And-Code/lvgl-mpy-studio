"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 35
Generated: 2023-11-14T22:14:27.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_35_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # calendar: calendar_35_0
    calendar_35_0 = lv.calendar(parent)
    objects["calendar_35_0"] = calendar_35_0
    calendar_35_0.set_pos(271, 27)
    calendar_35_0.set_size(24, 54)
    calendar_35_0.set_today_date(2026, 10, 28)
    calendar_35_0.set_month_shown(2026, 10)
    calendar_35_0_header = calendar_35_0.add_header_arrow()
    calendar_35_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_35_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_35_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_35_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_35_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_35_get_current_page():
    return current_screen

def random_35_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_35_load_page(0)
