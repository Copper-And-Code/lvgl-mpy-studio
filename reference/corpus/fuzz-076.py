"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 76
Generated: 2023-11-14T22:15:08.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_76_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tileview: tileview_76_0
    tileview_76_0 = lv.tileview(parent)
    objects["tileview_76_0"] = tileview_76_0
    tileview_76_0.set_pos(658, 159)
    tileview_76_0.set_size(57, 31)
    tileview_76_0.add_tile(0, 0, lv.DIR.ALL)
    tileview_76_0.add_tile(1, 0, lv.DIR.ALL)
    tileview_76_0.add_tile(0, 1, lv.DIR.ALL)
    tileview_76_0.add_tile(1, 1, lv.DIR.ALL)
    tileview_76_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # win: win_76_1
    win_76_1 = lv.obj(parent)
    objects["win_76_1"] = win_76_1
    win_76_1.set_pos(484, 329)
    win_76_1.set_size(258, 124)
    win_76_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_76_1.set_style_pad_all(0, lv.PART.MAIN)
    win_76_1.set_style_pad_row(0, lv.PART.MAIN)
    win_76_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_76_1_header = lv.obj(win_76_1)
    win_76_1_header.set_size(lv.pct(100), 40)
    win_76_1_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_76_1_header.set_style_radius(0, lv.PART.MAIN)
    win_76_1_title = lv.label(win_76_1_header)
    win_76_1_title.set_text("Window Title")
    win_76_1_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_76_1_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_76_1_content = lv.obj(win_76_1)
    win_76_1_content.set_width(lv.pct(100))
    win_76_1_content.set_flex_grow(1)

    # calendar: calendar_76_2
    calendar_76_2 = lv.calendar(parent)
    objects["calendar_76_2"] = calendar_76_2
    calendar_76_2.set_pos(473, 13)
    calendar_76_2.set_size(158, 21)
    calendar_76_2.set_today_date(2026, 10, 28)
    calendar_76_2.set_month_shown(2026, 10)
    calendar_76_2_header = calendar_76_2.add_header_arrow()
    calendar_76_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_76_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_76_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_76_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_76_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_76_get_current_page():
    return current_screen

def random_76_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_76_load_page(0)
