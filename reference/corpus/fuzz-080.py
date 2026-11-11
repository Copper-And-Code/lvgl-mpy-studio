"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 80
Generated: 2023-11-14T22:15:12.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def checkbox_80_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_80_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # label: label_80_0
    label_80_0 = lv.label(parent)
    objects["label_80_0"] = label_80_0
    label_80_0.set_pos(182, 301)
    label_80_0.set_size(234, 61)
    label_80_0.set_text("Testo 80:0 \" \\ Città")
    label_80_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_80_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_80_0.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # checkbox: checkbox_80_1
    checkbox_80_1 = lv.checkbox(parent)
    objects["checkbox_80_1"] = checkbox_80_1
    checkbox_80_1.set_pos(548, 200)
    checkbox_80_1.set_text("Testo 80:1 \" \\ Città")
    checkbox_80_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_80_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_80_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_80_1.add_event_cb(checkbox_80_1_changed, lv.EVENT.VALUE_CHANGED, None)

    # menu: menu_80_2
    menu_80_2 = lv.obj(parent)
    objects["menu_80_2"] = menu_80_2
    menu_80_2.set_pos(350, 230)
    menu_80_2.set_size(163, 115)
    menu_80_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_80_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_80_2_title = lv.label(menu_80_2)
    menu_80_2_title.set_text("Menu")
    menu_80_2_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_80_2_item_1 = lv.button(menu_80_2)
    menu_80_2_item_1.set_width(lv.pct(100))
    menu_80_2_item_1_label = lv.label(menu_80_2_item_1)
    menu_80_2_item_1_label.set_text("Item 1")
    menu_80_2_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_80_2_item_2 = lv.button(menu_80_2)
    menu_80_2_item_2.set_width(lv.pct(100))
    menu_80_2_item_2_label = lv.label(menu_80_2_item_2)
    menu_80_2_item_2_label.set_text("Item 2")
    menu_80_2_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_80_2_item_3 = lv.button(menu_80_2)
    menu_80_2_item_3.set_width(lv.pct(100))
    menu_80_2_item_3_label = lv.label(menu_80_2_item_3)
    menu_80_2_item_3_label.set_text("Item 3")
    menu_80_2_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_80_2_item_4 = lv.button(menu_80_2)
    menu_80_2_item_4.set_width(lv.pct(100))
    menu_80_2_item_4_label = lv.label(menu_80_2_item_4)
    menu_80_2_item_4_label.set_text("Item 4")
    menu_80_2_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # label: label_80_3
    label_80_3 = lv.label(parent)
    objects["label_80_3"] = label_80_3
    label_80_3.set_pos(158, 320)
    label_80_3.set_size(258, 71)
    label_80_3.set_text("Testo 80:3 \" \\ Città")
    label_80_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_80_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_80_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)


def random_80_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_80_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_80_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_80_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_80_get_current_page():
    return current_screen

def random_80_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_80_load_page(0)
