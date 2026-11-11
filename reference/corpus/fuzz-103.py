"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 103
Generated: 2023-11-14T22:15:35.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_103_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # bar: bar_103_0
    bar_103_0 = lv.bar(parent)
    objects["bar_103_0"] = bar_103_0
    bar_103_0.set_pos(51, 277)
    bar_103_0.set_size(131, 10)
    bar_103_0.set_range(0, 100)
    bar_103_0.set_value(50, False)
    bar_103_0.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_103_0.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # win: win_103_1
    win_103_1 = lv.obj(parent)
    objects["win_103_1"] = win_103_1
    win_103_1.set_pos(366, 366)
    win_103_1.set_size(152, 15)
    win_103_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_103_1.set_style_pad_all(0, lv.PART.MAIN)
    win_103_1.set_style_pad_row(0, lv.PART.MAIN)
    win_103_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_103_1_header = lv.obj(win_103_1)
    win_103_1_header.set_size(lv.pct(100), 40)
    win_103_1_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_103_1_header.set_style_radius(0, lv.PART.MAIN)
    win_103_1_title = lv.label(win_103_1_header)
    win_103_1_title.set_text("Window Title")
    win_103_1_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_103_1_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_103_1_content = lv.obj(win_103_1)
    win_103_1_content.set_width(lv.pct(100))
    win_103_1_content.set_flex_grow(1)


def random_103_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_103_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_103_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_103_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_103_get_current_page():
    return current_screen

def random_103_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_103_load_page(0)
