"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 10
Generated: 2023-11-14T22:14:02.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_10_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # roller: roller_10_0
    roller_10_0 = lv.roller(parent)
    objects["roller_10_0"] = roller_10_0
    roller_10_0.set_pos(379, 238)
    roller_10_0.set_size(67, 107)
    roller_10_0.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_10_0.set_visible_row_count(3)
    roller_10_0.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_10_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_10_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_10_0.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # win: win_10_1
    win_10_1 = lv.obj(parent)
    objects["win_10_1"] = win_10_1
    win_10_1.set_pos(411, 398)
    win_10_1.set_size(202, 77)
    win_10_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_10_1.set_style_pad_all(0, lv.PART.MAIN)
    win_10_1.set_style_pad_row(0, lv.PART.MAIN)
    win_10_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_10_1_header = lv.obj(win_10_1)
    win_10_1_header.set_size(lv.pct(100), 40)
    win_10_1_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_10_1_header.set_style_radius(0, lv.PART.MAIN)
    win_10_1_title = lv.label(win_10_1_header)
    win_10_1_title.set_text("Window Title")
    win_10_1_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_10_1_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_10_1_content = lv.obj(win_10_1)
    win_10_1_content.set_width(lv.pct(100))
    win_10_1_content.set_flex_grow(1)

    # image: image_10_2
    image_10_2 = lv.image(parent)
    objects["image_10_2"] = image_10_2
    image_10_2.set_pos(516, 128)
    image_10_2.set_size(244, 137)

    # bar: bar_10_3
    bar_10_3 = lv.bar(parent)
    objects["bar_10_3"] = bar_10_3
    bar_10_3.set_pos(61, 329)
    bar_10_3.set_size(107, 36)
    bar_10_3.set_range(0, 100)
    bar_10_3.set_value(50, False)
    bar_10_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_10_3.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # menu: menu_10_4
    menu_10_4 = lv.obj(parent)
    objects["menu_10_4"] = menu_10_4
    menu_10_4.set_pos(175, 304)
    menu_10_4.set_size(251, 147)
    menu_10_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_10_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_10_4_title = lv.label(menu_10_4)
    menu_10_4_title.set_text("Menu")
    menu_10_4_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_10_4_item_1 = lv.button(menu_10_4)
    menu_10_4_item_1.set_width(lv.pct(100))
    menu_10_4_item_1_label = lv.label(menu_10_4_item_1)
    menu_10_4_item_1_label.set_text("Item 1")
    menu_10_4_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_10_4_item_2 = lv.button(menu_10_4)
    menu_10_4_item_2.set_width(lv.pct(100))
    menu_10_4_item_2_label = lv.label(menu_10_4_item_2)
    menu_10_4_item_2_label.set_text("Item 2")
    menu_10_4_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_10_4_item_3 = lv.button(menu_10_4)
    menu_10_4_item_3.set_width(lv.pct(100))
    menu_10_4_item_3_label = lv.label(menu_10_4_item_3)
    menu_10_4_item_3_label.set_text("Item 3")
    menu_10_4_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_10_4_item_4 = lv.button(menu_10_4)
    menu_10_4_item_4.set_width(lv.pct(100))
    menu_10_4_item_4_label = lv.label(menu_10_4_item_4)
    menu_10_4_item_4_label.set_text("Item 4")
    menu_10_4_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # switch: switch_10_5
    switch_10_5 = lv.switch(parent)
    objects["switch_10_5"] = switch_10_5
    switch_10_5.set_pos(526, 325)
    switch_10_5.set_size(71, 73)
    switch_10_5.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_10_5.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_10_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # switch: switch_10_6
    switch_10_6 = lv.switch(parent)
    objects["switch_10_6"] = switch_10_6
    switch_10_6.set_pos(343, 0)
    switch_10_6.set_size(123, 88)
    switch_10_6.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_10_6.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_10_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)


def random_10_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_10_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_10_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_10_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_10_get_current_page():
    return current_screen

def random_10_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_10_load_page(0)
