"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 179
Generated: 2023-11-14T22:16:51.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_179_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # slider: slider_179_0
    slider_179_0 = lv.slider(parent)
    objects["slider_179_0"] = slider_179_0
    slider_179_0.set_pos(603, 38)
    slider_179_0.set_size(46, 23)
    slider_179_0.set_range(0, 100)
    slider_179_0.set_value(50, False)
    slider_179_0.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_179_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_179_0.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)

    # tabview: tabview_179_1
    tabview_179_1 = lv.tabview(parent)
    objects["tabview_179_1"] = tabview_179_1
    tabview_179_1.set_pos(509, 263)
    tabview_179_1.set_size(65, 35)
    tabview_179_1.set_tab_bar_position(lv.DIR.TOP)
    tabview_179_1.set_tab_bar_size(40)
    tabview_179_1_tab_1 = tabview_179_1.add_tab("Tab 1")
    tabview_179_1_tab_2 = tabview_179_1.add_tab("Tab 2")
    tabview_179_1_tab_3 = tabview_179_1.add_tab("Tab 3")
    tabview_179_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_179_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_179_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_179_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_179_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_179_get_current_page():
    return current_screen

def random_179_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_179_load_page(0)
