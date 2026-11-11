"""
Auto-generated LVGL UI Code for MicroPython
Project: One calendar
Generated: 2023-11-14T22:13:47.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_calendar_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # calendar: Calendar_w27
    calendar_w27 = lv.calendar(parent)
    objects["calendar_w27"] = calendar_w27
    calendar_w27.set_pos(101, 84)
    calendar_w27.set_size(230, 230)
    calendar_w27.set_today_date(2026, 10, 28)
    calendar_w27.set_month_shown(2026, 10)
    calendar_w27_header = calendar_w27.add_header_arrow()
    calendar_w27.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def one_calendar_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_calendar_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_calendar_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_calendar_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_calendar_get_current_page():
    return current_screen

def one_calendar_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_calendar_load_page(0)
