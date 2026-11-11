"""
Auto-generated LVGL UI Code for MicroPython
Project: One win
Generated: 2023-11-14T22:13:43.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_win_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: Window_w23
    window_w23 = lv.obj(parent)
    objects["window_w23"] = window_w23
    window_w23.set_pos(89, 76)
    window_w23.set_size(300, 250)
    window_w23.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    window_w23.set_style_pad_all(0, lv.PART.MAIN)
    window_w23.set_style_pad_row(0, lv.PART.MAIN)
    window_w23.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    window_w23_header = lv.obj(window_w23)
    window_w23_header.set_size(lv.pct(100), 40)
    window_w23_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    window_w23_header.set_style_radius(0, lv.PART.MAIN)
    window_w23_title = lv.label(window_w23_header)
    window_w23_title.set_text("Window Title")
    window_w23_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    window_w23_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    window_w23_content = lv.obj(window_w23)
    window_w23_content.set_width(lv.pct(100))
    window_w23_content.set_flex_grow(1)


def one_win_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_win_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_win_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_win_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_win_get_current_page():
    return current_screen

def one_win_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_win_load_page(0)
