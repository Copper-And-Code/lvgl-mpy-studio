"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 149
Generated: 2023-11-14T22:16:21.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_149_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # dropdown: dropdown_149_0
    dropdown_149_0 = lv.dropdown(parent)
    objects["dropdown_149_0"] = dropdown_149_0
    dropdown_149_0.set_pos(284, 21)
    dropdown_149_0.set_size(211, 128)
    dropdown_149_0.set_options("Option 1\nOption 2\nOption 3")
    dropdown_149_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_149_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_149_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # roller: roller_149_1
    roller_149_1 = lv.roller(parent)
    objects["roller_149_1"] = roller_149_1
    roller_149_1.set_pos(508, 149)
    roller_149_1.set_size(94, 59)
    roller_149_1.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_149_1.set_visible_row_count(3)
    roller_149_1.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_149_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_149_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_149_1.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # roller: roller_149_2
    roller_149_2 = lv.roller(parent)
    objects["roller_149_2"] = roller_149_2
    roller_149_2.set_pos(487, 20)
    roller_149_2.set_size(256, 27)
    roller_149_2.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_149_2.set_visible_row_count(3)
    roller_149_2.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_149_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_149_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_149_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # led: led_149_3
    led_149_3 = lv.led(parent)
    objects["led_149_3"] = led_149_3
    led_149_3.set_pos(392, 281)
    led_149_3.set_size(215, 150)
    led_149_3.set_color(lv.color_hex(0xFF0000))
    led_149_3.set_brightness(255)

    # list: list_149_4
    list_149_4 = lv.obj(parent)
    objects["list_149_4"] = list_149_4
    list_149_4.set_pos(124, 9)
    list_149_4.set_size(142, 108)
    list_149_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_149_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_149_4_item_1 = lv.button(list_149_4)
    list_149_4_item_1.set_width(lv.pct(100))
    list_149_4_item_1_label = lv.label(list_149_4_item_1)
    list_149_4_item_1_label.set_text("Item 1")
    list_149_4_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_149_4_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_149_4_item_2 = lv.button(list_149_4)
    list_149_4_item_2.set_width(lv.pct(100))
    list_149_4_item_2_label = lv.label(list_149_4_item_2)
    list_149_4_item_2_label.set_text("Item 2")
    list_149_4_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_149_4_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_149_4_item_3 = lv.button(list_149_4)
    list_149_4_item_3.set_width(lv.pct(100))
    list_149_4_item_3_label = lv.label(list_149_4_item_3)
    list_149_4_item_3_label.set_text("Item 3")
    list_149_4_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_149_4_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_149_4_item_4 = lv.button(list_149_4)
    list_149_4_item_4.set_width(lv.pct(100))
    list_149_4_item_4_label = lv.label(list_149_4_item_4)
    list_149_4_item_4_label.set_text("Item 4")
    list_149_4_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_149_4_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_149_4_item_5 = lv.button(list_149_4)
    list_149_4_item_5.set_width(lv.pct(100))
    list_149_4_item_5_label = lv.label(list_149_4_item_5)
    list_149_4_item_5_label.set_text("Item 5")
    list_149_4_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_149_4_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_149_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_149_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_149_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_149_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_149_get_current_page():
    return current_screen

def random_149_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_149_load_page(0)
