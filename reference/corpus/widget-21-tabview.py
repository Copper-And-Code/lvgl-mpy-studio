"""
Auto-generated LVGL UI Code for MicroPython
Project: One tabview
Generated: 2023-11-14T22:13:40.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_tabview_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tabview: Tab View_w20
    tab_view_w20 = lv.tabview(parent)
    objects["tab_view_w20"] = tab_view_w20
    tab_view_w20.set_pos(80, 70)
    tab_view_w20.set_size(300, 250)
    tab_view_w20.set_tab_bar_position(lv.DIR.TOP)
    tab_view_w20.set_tab_bar_size(40)
    tab_view_w20_tab_1 = tab_view_w20.add_tab("Tab 1")
    tab_view_w20_tab_2 = tab_view_w20.add_tab("Tab 2")
    tab_view_w20_tab_3 = tab_view_w20.add_tab("Tab 3")
    tab_view_w20.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def one_tabview_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_tabview_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_tabview_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_tabview_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_tabview_get_current_page():
    return current_screen

def one_tabview_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_tabview_load_page(0)
