"""
Auto-generated LVGL UI Code for MicroPython
Project: One menu
Generated: 2023-11-14T22:13:42.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_menu_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # menu: Menu_w22
    menu_w22 = lv.obj(parent)
    objects["menu_w22"] = menu_w22
    menu_w22.set_pos(86, 74)
    menu_w22.set_size(250, 300)
    menu_w22.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_w22.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_w22_title = lv.label(menu_w22)
    menu_w22_title.set_text("Menu")
    menu_w22_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_w22_item_1 = lv.button(menu_w22)
    menu_w22_item_1.set_width(lv.pct(100))
    menu_w22_item_1_label = lv.label(menu_w22_item_1)
    menu_w22_item_1_label.set_text("Item 1")
    menu_w22_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_w22_item_2 = lv.button(menu_w22)
    menu_w22_item_2.set_width(lv.pct(100))
    menu_w22_item_2_label = lv.label(menu_w22_item_2)
    menu_w22_item_2_label.set_text("Item 2")
    menu_w22_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_w22_item_3 = lv.button(menu_w22)
    menu_w22_item_3.set_width(lv.pct(100))
    menu_w22_item_3_label = lv.label(menu_w22_item_3)
    menu_w22_item_3_label.set_text("Item 3")
    menu_w22_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_w22_item_4 = lv.button(menu_w22)
    menu_w22_item_4.set_width(lv.pct(100))
    menu_w22_item_4_label = lv.label(menu_w22_item_4)
    menu_w22_item_4_label.set_text("Item 4")
    menu_w22_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)


def one_menu_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_menu_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_menu_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_menu_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_menu_get_current_page():
    return current_screen

def one_menu_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_menu_load_page(0)
