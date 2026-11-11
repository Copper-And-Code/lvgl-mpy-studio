"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 141
Generated: 2023-11-14T22:16:13.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_141_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # list: list_141_0
    list_141_0 = lv.obj(parent)
    objects["list_141_0"] = list_141_0
    list_141_0.set_pos(435, 254)
    list_141_0.set_size(58, 45)
    list_141_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_141_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_141_0_item_1 = lv.button(list_141_0)
    list_141_0_item_1.set_width(lv.pct(100))
    list_141_0_item_1_label = lv.label(list_141_0_item_1)
    list_141_0_item_1_label.set_text("Item 1")
    list_141_0_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_141_0_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_141_0_item_2 = lv.button(list_141_0)
    list_141_0_item_2.set_width(lv.pct(100))
    list_141_0_item_2_label = lv.label(list_141_0_item_2)
    list_141_0_item_2_label.set_text("Item 2")
    list_141_0_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_141_0_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_141_0_item_3 = lv.button(list_141_0)
    list_141_0_item_3.set_width(lv.pct(100))
    list_141_0_item_3_label = lv.label(list_141_0_item_3)
    list_141_0_item_3_label.set_text("Item 3")
    list_141_0_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_141_0_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_141_0_item_4 = lv.button(list_141_0)
    list_141_0_item_4.set_width(lv.pct(100))
    list_141_0_item_4_label = lv.label(list_141_0_item_4)
    list_141_0_item_4_label.set_text("Item 4")
    list_141_0_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_141_0_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_141_0_item_5 = lv.button(list_141_0)
    list_141_0_item_5.set_width(lv.pct(100))
    list_141_0_item_5_label = lv.label(list_141_0_item_5)
    list_141_0_item_5_label.set_text("Item 5")
    list_141_0_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_141_0_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_141_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_141_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_141_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_141_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_141_get_current_page():
    return current_screen

def random_141_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_141_load_page(0)
