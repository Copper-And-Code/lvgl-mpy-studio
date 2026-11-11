"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 73
Generated: 2023-11-14T22:15:05.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_73_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # keyboard: keyboard_73_0
    keyboard_73_0 = lv.keyboard(parent)
    objects["keyboard_73_0"] = keyboard_73_0
    keyboard_73_0.set_pos(401, 41)
    keyboard_73_0.set_size(48, 99)

    # win: win_73_1
    win_73_1 = lv.obj(parent)
    objects["win_73_1"] = win_73_1
    win_73_1.set_pos(383, 345)
    win_73_1.set_size(111, 122)
    win_73_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_73_1.set_style_pad_all(0, lv.PART.MAIN)
    win_73_1.set_style_pad_row(0, lv.PART.MAIN)
    win_73_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_73_1_header = lv.obj(win_73_1)
    win_73_1_header.set_size(lv.pct(100), 40)
    win_73_1_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_73_1_header.set_style_radius(0, lv.PART.MAIN)
    win_73_1_title = lv.label(win_73_1_header)
    win_73_1_title.set_text("Window Title")
    win_73_1_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_73_1_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_73_1_content = lv.obj(win_73_1)
    win_73_1_content.set_width(lv.pct(100))
    win_73_1_content.set_flex_grow(1)

    # span: span_73_2
    span_73_2 = lv.spangroup(parent)
    objects["span_73_2"] = span_73_2
    span_73_2.set_pos(122, 390)
    span_73_2.set_size(47, 106)
    span_73_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_73_2_span_1 = span_73_2.add_span()
    span_73_2_span_1.set_text("Normal text")
    span_73_2_span_1_style = span_73_2_span_1.get_style()
    span_73_2_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_73_2_span_1_style.set_text_font(lv.font_montserrat_14)
    span_73_2_span_2 = span_73_2.add_span()
    span_73_2_span_2.set_text("Bold text")
    span_73_2_span_2_style = span_73_2_span_2.get_style()
    span_73_2_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_73_2_span_2_style.set_text_font(lv.font_montserrat_16)
    span_73_2_span_3 = span_73_2.add_span()
    span_73_2_span_3.set_text("Small text")
    span_73_2_span_3_style = span_73_2_span_3.get_style()
    span_73_2_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_73_2_span_3_style.set_text_font(lv.font_montserrat_14)
    span_73_2.refresh()

    # list: list_73_3
    list_73_3 = lv.obj(parent)
    objects["list_73_3"] = list_73_3
    list_73_3.set_pos(393, 225)
    list_73_3.set_size(54, 75)
    list_73_3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_73_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_73_3_item_1 = lv.button(list_73_3)
    list_73_3_item_1.set_width(lv.pct(100))
    list_73_3_item_1_label = lv.label(list_73_3_item_1)
    list_73_3_item_1_label.set_text("Item 1")
    list_73_3_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_73_3_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_73_3_item_2 = lv.button(list_73_3)
    list_73_3_item_2.set_width(lv.pct(100))
    list_73_3_item_2_label = lv.label(list_73_3_item_2)
    list_73_3_item_2_label.set_text("Item 2")
    list_73_3_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_73_3_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_73_3_item_3 = lv.button(list_73_3)
    list_73_3_item_3.set_width(lv.pct(100))
    list_73_3_item_3_label = lv.label(list_73_3_item_3)
    list_73_3_item_3_label.set_text("Item 3")
    list_73_3_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_73_3_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_73_3_item_4 = lv.button(list_73_3)
    list_73_3_item_4.set_width(lv.pct(100))
    list_73_3_item_4_label = lv.label(list_73_3_item_4)
    list_73_3_item_4_label.set_text("Item 4")
    list_73_3_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_73_3_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_73_3_item_5 = lv.button(list_73_3)
    list_73_3_item_5.set_width(lv.pct(100))
    list_73_3_item_5_label = lv.label(list_73_3_item_5)
    list_73_3_item_5_label.set_text("Item 5")
    list_73_3_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_73_3_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # keyboard: keyboard_73_4
    keyboard_73_4 = lv.keyboard(parent)
    objects["keyboard_73_4"] = keyboard_73_4
    keyboard_73_4.set_pos(146, 6)
    keyboard_73_4.set_size(83, 84)


def random_73_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_73_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_73_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_73_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_73_get_current_page():
    return current_screen

def random_73_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_73_load_page(0)
