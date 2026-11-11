"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 172
Generated: 2023-11-14T22:16:44.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_172_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tabview: tabview_172_0
    tabview_172_0 = lv.tabview(parent)
    objects["tabview_172_0"] = tabview_172_0
    tabview_172_0.set_pos(298, 56)
    tabview_172_0.set_size(228, 14)
    tabview_172_0.set_tab_bar_position(lv.DIR.TOP)
    tabview_172_0.set_tab_bar_size(40)
    tabview_172_0_tab_1 = tabview_172_0.add_tab("Tab 1")
    tabview_172_0_tab_2 = tabview_172_0.add_tab("Tab 2")
    tabview_172_0_tab_3 = tabview_172_0.add_tab("Tab 3")
    tabview_172_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # textarea: textarea_172_1
    textarea_172_1 = lv.textarea(parent)
    objects["textarea_172_1"] = textarea_172_1
    textarea_172_1.set_pos(66, 48)
    textarea_172_1.set_size(39, 17)
    textarea_172_1.set_text("Testo 172:1 \" \\ Città")
    textarea_172_1.set_placeholder_text("Type here")
    textarea_172_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_172_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_172_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # slider: slider_172_2
    slider_172_2 = lv.slider(parent)
    objects["slider_172_2"] = slider_172_2
    slider_172_2.set_pos(437, 23)
    slider_172_2.set_size(114, 86)
    slider_172_2.set_range(0, 100)
    slider_172_2.set_value(50, False)
    slider_172_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_172_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_172_2.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)

    # scale: scale_172_3
    scale_172_3 = lv.scale(parent)
    objects["scale_172_3"] = scale_172_3
    scale_172_3.set_pos(282, 350)
    scale_172_3.set_size(158, 91)
    scale_172_3.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_172_3.set_range(0, 100)
    scale_172_3.set_total_tick_count(51)
    scale_172_3.set_major_tick_every(5)
    scale_172_3.set_style_length(15, lv.PART.INDICATOR)
    scale_172_3.set_style_length(8, lv.PART.ITEMS)
    scale_172_3.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_172_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)


def random_172_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_172_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_172_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_172_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_172_get_current_page():
    return current_screen

def random_172_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_172_load_page(0)
