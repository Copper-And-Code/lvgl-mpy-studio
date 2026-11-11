"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 38
Generated: 2023-11-14T22:14:30.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_38_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # menu: menu_38_0
    menu_38_0 = lv.obj(parent)
    objects["menu_38_0"] = menu_38_0
    menu_38_0.set_pos(153, 216)
    menu_38_0.set_size(180, 39)
    menu_38_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_38_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_38_0_title = lv.label(menu_38_0)
    menu_38_0_title.set_text("Menu")
    menu_38_0_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_38_0_item_1 = lv.button(menu_38_0)
    menu_38_0_item_1.set_width(lv.pct(100))
    menu_38_0_item_1_label = lv.label(menu_38_0_item_1)
    menu_38_0_item_1_label.set_text("Item 1")
    menu_38_0_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_38_0_item_2 = lv.button(menu_38_0)
    menu_38_0_item_2.set_width(lv.pct(100))
    menu_38_0_item_2_label = lv.label(menu_38_0_item_2)
    menu_38_0_item_2_label.set_text("Item 2")
    menu_38_0_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_38_0_item_3 = lv.button(menu_38_0)
    menu_38_0_item_3.set_width(lv.pct(100))
    menu_38_0_item_3_label = lv.label(menu_38_0_item_3)
    menu_38_0_item_3_label.set_text("Item 3")
    menu_38_0_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_38_0_item_4 = lv.button(menu_38_0)
    menu_38_0_item_4.set_width(lv.pct(100))
    menu_38_0_item_4_label = lv.label(menu_38_0_item_4)
    menu_38_0_item_4_label.set_text("Item 4")
    menu_38_0_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)


def random_38_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_38_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_38_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_38_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_38_get_current_page():
    return current_screen

def random_38_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_38_load_page(0)
