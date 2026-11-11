"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 140
Generated: 2023-11-14T22:16:12.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_140_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tileview: tileview_140_0
    tileview_140_0 = lv.tileview(parent)
    objects["tileview_140_0"] = tileview_140_0
    tileview_140_0.set_pos(637, 141)
    tileview_140_0.set_size(59, 155)
    tileview_140_0.add_tile(0, 0, lv.DIR.ALL)
    tileview_140_0.add_tile(1, 0, lv.DIR.ALL)
    tileview_140_0.add_tile(0, 1, lv.DIR.ALL)
    tileview_140_0.add_tile(1, 1, lv.DIR.ALL)
    tileview_140_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # dropdown: dropdown_140_1
    dropdown_140_1 = lv.dropdown(parent)
    objects["dropdown_140_1"] = dropdown_140_1
    dropdown_140_1.set_pos(64, 332)
    dropdown_140_1.set_size(154, 22)
    dropdown_140_1.set_options("Option 1\nOption 2\nOption 3")
    dropdown_140_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_140_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_140_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # tabview: tabview_140_2
    tabview_140_2 = lv.tabview(parent)
    objects["tabview_140_2"] = tabview_140_2
    tabview_140_2.set_pos(223, 114)
    tabview_140_2.set_size(41, 20)
    tabview_140_2.set_tab_bar_position(lv.DIR.TOP)
    tabview_140_2.set_tab_bar_size(40)
    tabview_140_2_tab_1 = tabview_140_2.add_tab("Tab 1")
    tabview_140_2_tab_2 = tabview_140_2.add_tab("Tab 2")
    tabview_140_2_tab_3 = tabview_140_2.add_tab("Tab 3")
    tabview_140_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # bar: bar_140_3
    bar_140_3 = lv.bar(parent)
    objects["bar_140_3"] = bar_140_3
    bar_140_3.set_pos(29, 364)
    bar_140_3.set_size(120, 40)
    bar_140_3.set_range(0, 100)
    bar_140_3.set_value(50, False)
    bar_140_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_140_3.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)


def random_140_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_140_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_140_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_140_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_140_get_current_page():
    return current_screen

def random_140_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_140_load_page(0)
