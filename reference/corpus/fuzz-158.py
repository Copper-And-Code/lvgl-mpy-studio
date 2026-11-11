"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 158
Generated: 2023-11-14T22:16:30.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_158_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tileview: tileview_158_0
    tileview_158_0 = lv.tileview(parent)
    objects["tileview_158_0"] = tileview_158_0
    tileview_158_0.set_pos(526, 326)
    tileview_158_0.set_size(115, 137)
    tileview_158_0.add_tile(0, 0, lv.DIR.ALL)
    tileview_158_0.add_tile(1, 0, lv.DIR.ALL)
    tileview_158_0.add_tile(0, 1, lv.DIR.ALL)
    tileview_158_0.add_tile(1, 1, lv.DIR.ALL)
    tileview_158_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # calendar: calendar_158_1
    calendar_158_1 = lv.calendar(parent)
    objects["calendar_158_1"] = calendar_158_1
    calendar_158_1.set_pos(309, 89)
    calendar_158_1.set_size(72, 32)
    calendar_158_1.set_today_date(2026, 10, 28)
    calendar_158_1.set_month_shown(2026, 10)
    calendar_158_1_header = calendar_158_1.add_header_arrow()
    calendar_158_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # spinbox: spinbox_158_2
    spinbox_158_2 = lv.spinbox(parent)
    objects["spinbox_158_2"] = spinbox_158_2
    spinbox_158_2.set_pos(162, 381)
    spinbox_158_2.set_size(119, 89)
    spinbox_158_2.set_digit_format(4, 0)
    spinbox_158_2.set_range(0, 999)
    spinbox_158_2.set_value(0)
    spinbox_158_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_158_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_158_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_158_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_158_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_158_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_158_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_158_get_current_page():
    return current_screen

def random_158_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_158_load_page(0)
