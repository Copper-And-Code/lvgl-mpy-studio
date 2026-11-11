"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 43
Generated: 2023-11-14T22:14:35.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_43_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # menu: menu_43_0
    menu_43_0 = lv.obj(parent)
    objects["menu_43_0"] = menu_43_0
    menu_43_0.set_pos(0, 314)
    menu_43_0.set_size(251, 12)
    menu_43_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_43_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_43_0_title = lv.label(menu_43_0)
    menu_43_0_title.set_text("Menu")
    menu_43_0_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_43_0_item_1 = lv.button(menu_43_0)
    menu_43_0_item_1.set_width(lv.pct(100))
    menu_43_0_item_1_label = lv.label(menu_43_0_item_1)
    menu_43_0_item_1_label.set_text("Item 1")
    menu_43_0_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_43_0_item_2 = lv.button(menu_43_0)
    menu_43_0_item_2.set_width(lv.pct(100))
    menu_43_0_item_2_label = lv.label(menu_43_0_item_2)
    menu_43_0_item_2_label.set_text("Item 2")
    menu_43_0_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_43_0_item_3 = lv.button(menu_43_0)
    menu_43_0_item_3.set_width(lv.pct(100))
    menu_43_0_item_3_label = lv.label(menu_43_0_item_3)
    menu_43_0_item_3_label.set_text("Item 3")
    menu_43_0_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_43_0_item_4 = lv.button(menu_43_0)
    menu_43_0_item_4.set_width(lv.pct(100))
    menu_43_0_item_4_label = lv.label(menu_43_0_item_4)
    menu_43_0_item_4_label.set_text("Item 4")
    menu_43_0_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # list: list_43_1
    list_43_1 = lv.obj(parent)
    objects["list_43_1"] = list_43_1
    list_43_1.set_pos(627, 316)
    list_43_1.set_size(96, 19)
    list_43_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_43_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_43_1_item_1 = lv.button(list_43_1)
    list_43_1_item_1.set_width(lv.pct(100))
    list_43_1_item_1_label = lv.label(list_43_1_item_1)
    list_43_1_item_1_label.set_text("Item 1")
    list_43_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_43_1_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_43_1_item_2 = lv.button(list_43_1)
    list_43_1_item_2.set_width(lv.pct(100))
    list_43_1_item_2_label = lv.label(list_43_1_item_2)
    list_43_1_item_2_label.set_text("Item 2")
    list_43_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_43_1_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_43_1_item_3 = lv.button(list_43_1)
    list_43_1_item_3.set_width(lv.pct(100))
    list_43_1_item_3_label = lv.label(list_43_1_item_3)
    list_43_1_item_3_label.set_text("Item 3")
    list_43_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_43_1_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_43_1_item_4 = lv.button(list_43_1)
    list_43_1_item_4.set_width(lv.pct(100))
    list_43_1_item_4_label = lv.label(list_43_1_item_4)
    list_43_1_item_4_label.set_text("Item 4")
    list_43_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_43_1_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_43_1_item_5 = lv.button(list_43_1)
    list_43_1_item_5.set_width(lv.pct(100))
    list_43_1_item_5_label = lv.label(list_43_1_item_5)
    list_43_1_item_5_label.set_text("Item 5")
    list_43_1_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_43_1_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_43_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_43_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_43_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_43_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_43_get_current_page():
    return current_screen

def random_43_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_43_load_page(0)
