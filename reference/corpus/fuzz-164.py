"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 164
Generated: 2023-11-14T22:16:36.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def checkbox_164_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_164_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # menu: menu_164_0
    menu_164_0 = lv.obj(parent)
    objects["menu_164_0"] = menu_164_0
    menu_164_0.set_pos(201, 102)
    menu_164_0.set_size(114, 143)
    menu_164_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_164_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_164_0_title = lv.label(menu_164_0)
    menu_164_0_title.set_text("Menu")
    menu_164_0_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_164_0_item_1 = lv.button(menu_164_0)
    menu_164_0_item_1.set_width(lv.pct(100))
    menu_164_0_item_1_label = lv.label(menu_164_0_item_1)
    menu_164_0_item_1_label.set_text("Item 1")
    menu_164_0_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_164_0_item_2 = lv.button(menu_164_0)
    menu_164_0_item_2.set_width(lv.pct(100))
    menu_164_0_item_2_label = lv.label(menu_164_0_item_2)
    menu_164_0_item_2_label.set_text("Item 2")
    menu_164_0_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_164_0_item_3 = lv.button(menu_164_0)
    menu_164_0_item_3.set_width(lv.pct(100))
    menu_164_0_item_3_label = lv.label(menu_164_0_item_3)
    menu_164_0_item_3_label.set_text("Item 3")
    menu_164_0_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_164_0_item_4 = lv.button(menu_164_0)
    menu_164_0_item_4.set_width(lv.pct(100))
    menu_164_0_item_4_label = lv.label(menu_164_0_item_4)
    menu_164_0_item_4_label.set_text("Item 4")
    menu_164_0_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # checkbox: checkbox_164_1
    checkbox_164_1 = lv.checkbox(parent)
    objects["checkbox_164_1"] = checkbox_164_1
    checkbox_164_1.set_pos(235, 100)
    checkbox_164_1.set_text("Testo 164:1 \" \\ Città")
    checkbox_164_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_164_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_164_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_164_1.add_event_cb(checkbox_164_1_changed, lv.EVENT.VALUE_CHANGED, None)

    # bar: bar_164_2
    bar_164_2 = lv.bar(parent)
    objects["bar_164_2"] = bar_164_2
    bar_164_2.set_pos(540, 25)
    bar_164_2.set_size(149, 66)
    bar_164_2.set_range(0, 100)
    bar_164_2.set_value(50, False)
    bar_164_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_164_2.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # spinbox: spinbox_164_3
    spinbox_164_3 = lv.spinbox(parent)
    objects["spinbox_164_3"] = spinbox_164_3
    spinbox_164_3.set_pos(405, 21)
    spinbox_164_3.set_size(64, 55)
    spinbox_164_3.set_digit_format(4, 0)
    spinbox_164_3.set_range(0, 999)
    spinbox_164_3.set_value(0)
    spinbox_164_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_164_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_164_3.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # win: win_164_4
    win_164_4 = lv.obj(parent)
    objects["win_164_4"] = win_164_4
    win_164_4.set_pos(372, 382)
    win_164_4.set_size(238, 71)
    win_164_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_164_4.set_style_pad_all(0, lv.PART.MAIN)
    win_164_4.set_style_pad_row(0, lv.PART.MAIN)
    win_164_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_164_4_header = lv.obj(win_164_4)
    win_164_4_header.set_size(lv.pct(100), 40)
    win_164_4_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_164_4_header.set_style_radius(0, lv.PART.MAIN)
    win_164_4_title = lv.label(win_164_4_header)
    win_164_4_title.set_text("Window Title")
    win_164_4_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_164_4_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_164_4_content = lv.obj(win_164_4)
    win_164_4_content.set_width(lv.pct(100))
    win_164_4_content.set_flex_grow(1)


def random_164_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_164_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_164_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_164_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_164_get_current_page():
    return current_screen

def random_164_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_164_load_page(0)
