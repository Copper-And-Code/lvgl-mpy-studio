"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 92
Generated: 2023-11-14T22:15:24.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_92_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tabview: tabview_92_0
    tabview_92_0 = lv.tabview(parent)
    objects["tabview_92_0"] = tabview_92_0
    tabview_92_0.set_pos(131, 385)
    tabview_92_0.set_size(41, 62)
    tabview_92_0.set_tab_bar_position(lv.DIR.TOP)
    tabview_92_0.set_tab_bar_size(40)
    tabview_92_0_tab_1 = tabview_92_0.add_tab("Tab 1")
    tabview_92_0_tab_2 = tabview_92_0.add_tab("Tab 2")
    tabview_92_0_tab_3 = tabview_92_0.add_tab("Tab 3")
    tabview_92_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # arc: arc_92_1
    arc_92_1 = lv.arc(parent)
    objects["arc_92_1"] = arc_92_1
    arc_92_1.set_pos(590, 245)
    arc_92_1.set_size(202, 131)
    arc_92_1.set_bg_angles(135, 45)
    arc_92_1.set_range(0, 100)
    arc_92_1.set_value(50)
    arc_92_1.set_style_arc_width(10, lv.PART.MAIN)
    arc_92_1.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_92_1.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_92_1.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_92_1.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)


def random_92_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_92_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_92_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_92_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_92_get_current_page():
    return current_screen

def random_92_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_92_load_page(0)
