"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 56
Generated: 2023-11-14T22:14:48.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_56_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # calendar: calendar_56_0
    calendar_56_0 = lv.calendar(parent)
    objects["calendar_56_0"] = calendar_56_0
    calendar_56_0.set_pos(378, 147)
    calendar_56_0.set_size(210, 145)
    calendar_56_0.set_today_date(2026, 10, 28)
    calendar_56_0.set_month_shown(2026, 10)
    calendar_56_0_header = calendar_56_0.add_header_arrow()
    calendar_56_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # scale: scale_56_1
    scale_56_1 = lv.scale(parent)
    objects["scale_56_1"] = scale_56_1
    scale_56_1.set_pos(511, 138)
    scale_56_1.set_size(35, 137)
    scale_56_1.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_56_1.set_range(0, 100)
    scale_56_1.set_total_tick_count(51)
    scale_56_1.set_major_tick_every(5)
    scale_56_1.set_style_length(15, lv.PART.INDICATOR)
    scale_56_1.set_style_length(8, lv.PART.ITEMS)
    scale_56_1.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_56_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # tabview: tabview_56_2
    tabview_56_2 = lv.tabview(parent)
    objects["tabview_56_2"] = tabview_56_2
    tabview_56_2.set_pos(130, 309)
    tabview_56_2.set_size(48, 111)
    tabview_56_2.set_tab_bar_position(lv.DIR.TOP)
    tabview_56_2.set_tab_bar_size(40)
    tabview_56_2_tab_1 = tabview_56_2.add_tab("Tab 1")
    tabview_56_2_tab_2 = tabview_56_2.add_tab("Tab 2")
    tabview_56_2_tab_3 = tabview_56_2.add_tab("Tab 3")
    tabview_56_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_56_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_56_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_56_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_56_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_56_get_current_page():
    return current_screen

def random_56_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_56_load_page(0)
