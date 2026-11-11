"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 47
Generated: 2023-11-14T22:14:39.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def textarea_47_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_47_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # textarea: textarea_47_0
    textarea_47_0 = lv.textarea(parent)
    objects["textarea_47_0"] = textarea_47_0
    textarea_47_0.set_pos(235, 333)
    textarea_47_0.set_size(53, 107)
    textarea_47_0.set_text("Testo 47:0 \" \\ Città")
    textarea_47_0.set_placeholder_text("Type here")
    textarea_47_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_47_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_47_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # textarea: textarea_47_1
    textarea_47_1 = lv.textarea(parent)
    objects["textarea_47_1"] = textarea_47_1
    textarea_47_1.set_pos(166, 167)
    textarea_47_1.set_size(78, 105)
    textarea_47_1.set_text("Testo 47:1 \" \\ Città")
    textarea_47_1.set_placeholder_text("Type here")
    textarea_47_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_47_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_47_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    textarea_47_1.add_event_cb(textarea_47_1_changed, lv.EVENT.VALUE_CHANGED, None)

    # list: list_47_2
    list_47_2 = lv.obj(parent)
    objects["list_47_2"] = list_47_2
    list_47_2.set_pos(511, 259)
    list_47_2.set_size(150, 19)
    list_47_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_47_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_47_2_item_1 = lv.button(list_47_2)
    list_47_2_item_1.set_width(lv.pct(100))
    list_47_2_item_1_label = lv.label(list_47_2_item_1)
    list_47_2_item_1_label.set_text("Item 1")
    list_47_2_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_47_2_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_47_2_item_2 = lv.button(list_47_2)
    list_47_2_item_2.set_width(lv.pct(100))
    list_47_2_item_2_label = lv.label(list_47_2_item_2)
    list_47_2_item_2_label.set_text("Item 2")
    list_47_2_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_47_2_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_47_2_item_3 = lv.button(list_47_2)
    list_47_2_item_3.set_width(lv.pct(100))
    list_47_2_item_3_label = lv.label(list_47_2_item_3)
    list_47_2_item_3_label.set_text("Item 3")
    list_47_2_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_47_2_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_47_2_item_4 = lv.button(list_47_2)
    list_47_2_item_4.set_width(lv.pct(100))
    list_47_2_item_4_label = lv.label(list_47_2_item_4)
    list_47_2_item_4_label.set_text("Item 4")
    list_47_2_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_47_2_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_47_2_item_5 = lv.button(list_47_2)
    list_47_2_item_5.set_width(lv.pct(100))
    list_47_2_item_5_label = lv.label(list_47_2_item_5)
    list_47_2_item_5_label.set_text("Item 5")
    list_47_2_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_47_2_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_47_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_47_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_47_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_47_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_47_get_current_page():
    return current_screen

def random_47_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_47_load_page(0)
