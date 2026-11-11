"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 65
Generated: 2023-11-14T22:14:57.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_65_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: win_65_0
    win_65_0 = lv.obj(parent)
    objects["win_65_0"] = win_65_0
    win_65_0.set_pos(155, 336)
    win_65_0.set_size(164, 109)
    win_65_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_65_0.set_style_pad_all(0, lv.PART.MAIN)
    win_65_0.set_style_pad_row(0, lv.PART.MAIN)
    win_65_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_65_0_header = lv.obj(win_65_0)
    win_65_0_header.set_size(lv.pct(100), 40)
    win_65_0_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_65_0_header.set_style_radius(0, lv.PART.MAIN)
    win_65_0_title = lv.label(win_65_0_header)
    win_65_0_title.set_text("Window Title")
    win_65_0_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_65_0_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_65_0_content = lv.obj(win_65_0)
    win_65_0_content.set_width(lv.pct(100))
    win_65_0_content.set_flex_grow(1)

    # menu: menu_65_1
    menu_65_1 = lv.obj(parent)
    objects["menu_65_1"] = menu_65_1
    menu_65_1.set_pos(235, 356)
    menu_65_1.set_size(71, 89)
    menu_65_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_65_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_65_1_title = lv.label(menu_65_1)
    menu_65_1_title.set_text("Menu")
    menu_65_1_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_65_1_item_1 = lv.button(menu_65_1)
    menu_65_1_item_1.set_width(lv.pct(100))
    menu_65_1_item_1_label = lv.label(menu_65_1_item_1)
    menu_65_1_item_1_label.set_text("Item 1")
    menu_65_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_65_1_item_2 = lv.button(menu_65_1)
    menu_65_1_item_2.set_width(lv.pct(100))
    menu_65_1_item_2_label = lv.label(menu_65_1_item_2)
    menu_65_1_item_2_label.set_text("Item 2")
    menu_65_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_65_1_item_3 = lv.button(menu_65_1)
    menu_65_1_item_3.set_width(lv.pct(100))
    menu_65_1_item_3_label = lv.label(menu_65_1_item_3)
    menu_65_1_item_3_label.set_text("Item 3")
    menu_65_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_65_1_item_4 = lv.button(menu_65_1)
    menu_65_1_item_4.set_width(lv.pct(100))
    menu_65_1_item_4_label = lv.label(menu_65_1_item_4)
    menu_65_1_item_4_label.set_text("Item 4")
    menu_65_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # arc: arc_65_2
    arc_65_2 = lv.arc(parent)
    objects["arc_65_2"] = arc_65_2
    arc_65_2.set_pos(594, 192)
    arc_65_2.set_size(114, 132)
    arc_65_2.set_bg_angles(135, 45)
    arc_65_2.set_range(0, 100)
    arc_65_2.set_value(50)
    arc_65_2.set_style_arc_width(10, lv.PART.MAIN)
    arc_65_2.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_65_2.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_65_2.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_65_2.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # msgbox: msgbox_65_3
    msgbox_65_3 = lv.msgbox(parent)
    objects["msgbox_65_3"] = msgbox_65_3
    msgbox_65_3.set_pos(616, 76)
    msgbox_65_3.set_size(34, 74)
    msgbox_65_3_title = msgbox_65_3.add_title("Notice")
    msgbox_65_3_text = msgbox_65_3.add_text("Testo 65:3 \" \\ Città")
    msgbox_65_3_button_1 = msgbox_65_3.add_footer_button("OK")
    msgbox_65_3_button_2 = msgbox_65_3.add_footer_button("Cancel")
    msgbox_65_3_close = msgbox_65_3.add_close_button()
    msgbox_65_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_65_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_65_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_65_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_65_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_65_get_current_page():
    return current_screen

def random_65_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_65_load_page(0)
