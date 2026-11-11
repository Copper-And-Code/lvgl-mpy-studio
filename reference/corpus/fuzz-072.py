"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 72
Generated: 2023-11-14T22:15:04.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def textarea_72_4_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_72_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # menu: menu_72_0
    menu_72_0 = lv.obj(parent)
    objects["menu_72_0"] = menu_72_0
    menu_72_0.set_pos(686, 37)
    menu_72_0.set_size(181, 103)
    menu_72_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_72_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_72_0_title = lv.label(menu_72_0)
    menu_72_0_title.set_text("Menu")
    menu_72_0_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_72_0_item_1 = lv.button(menu_72_0)
    menu_72_0_item_1.set_width(lv.pct(100))
    menu_72_0_item_1_label = lv.label(menu_72_0_item_1)
    menu_72_0_item_1_label.set_text("Item 1")
    menu_72_0_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_72_0_item_2 = lv.button(menu_72_0)
    menu_72_0_item_2.set_width(lv.pct(100))
    menu_72_0_item_2_label = lv.label(menu_72_0_item_2)
    menu_72_0_item_2_label.set_text("Item 2")
    menu_72_0_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_72_0_item_3 = lv.button(menu_72_0)
    menu_72_0_item_3.set_width(lv.pct(100))
    menu_72_0_item_3_label = lv.label(menu_72_0_item_3)
    menu_72_0_item_3_label.set_text("Item 3")
    menu_72_0_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_72_0_item_4 = lv.button(menu_72_0)
    menu_72_0_item_4.set_width(lv.pct(100))
    menu_72_0_item_4_label = lv.label(menu_72_0_item_4)
    menu_72_0_item_4_label.set_text("Item 4")
    menu_72_0_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # win: win_72_1
    win_72_1 = lv.obj(parent)
    objects["win_72_1"] = win_72_1
    win_72_1.set_pos(418, 286)
    win_72_1.set_size(140, 131)
    win_72_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_72_1.set_style_pad_all(0, lv.PART.MAIN)
    win_72_1.set_style_pad_row(0, lv.PART.MAIN)
    win_72_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_72_1_header = lv.obj(win_72_1)
    win_72_1_header.set_size(lv.pct(100), 40)
    win_72_1_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_72_1_header.set_style_radius(0, lv.PART.MAIN)
    win_72_1_title = lv.label(win_72_1_header)
    win_72_1_title.set_text("Window Title")
    win_72_1_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_72_1_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_72_1_content = lv.obj(win_72_1)
    win_72_1_content.set_width(lv.pct(100))
    win_72_1_content.set_flex_grow(1)

    # image: image_72_2
    image_72_2 = lv.image(parent)
    objects["image_72_2"] = image_72_2
    image_72_2.set_pos(331, 21)
    image_72_2.set_size(100, 20)

    # table: table_72_3
    table_72_3 = lv.table(parent)
    objects["table_72_3"] = table_72_3
    table_72_3.set_pos(459, 68)
    table_72_3.set_size(149, 24)
    table_72_3.set_column_count(3)
    table_72_3.set_column_width(0, 100)
    table_72_3.set_column_width(1, 100)
    table_72_3.set_column_width(2, 100)
    table_72_3.set_cell_value(0, 0, "Col 1")
    table_72_3.set_cell_value(0, 1, "Col 2")
    table_72_3.set_cell_value(0, 2, "Col 3")
    table_72_3.set_cell_value(1, 0, "A1")
    table_72_3.set_cell_value(1, 1, "B1")
    table_72_3.set_cell_value(1, 2, "C1")
    table_72_3.set_cell_value(2, 0, "A2")
    table_72_3.set_cell_value(2, 1, "B2")
    table_72_3.set_cell_value(2, 2, "C2")
    table_72_3.set_cell_value(3, 0, "A3")
    table_72_3.set_cell_value(3, 1, "B3")
    table_72_3.set_cell_value(3, 2, "C3")
    table_72_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_72_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_72_3.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_72_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # textarea: textarea_72_4
    textarea_72_4 = lv.textarea(parent)
    objects["textarea_72_4"] = textarea_72_4
    textarea_72_4.set_pos(188, 399)
    textarea_72_4.set_size(224, 103)
    textarea_72_4.set_text("Testo 72:4 \" \\ Città")
    textarea_72_4.set_placeholder_text("Type here")
    textarea_72_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_72_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_72_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    textarea_72_4.add_event_cb(textarea_72_4_changed, lv.EVENT.VALUE_CHANGED, None)

    # imagebutton: imagebutton_72_5
    imagebutton_72_5 = lv.imagebutton(parent)
    objects["imagebutton_72_5"] = imagebutton_72_5
    imagebutton_72_5.set_pos(536, 129)
    imagebutton_72_5.set_size(163, 35)
    imagebutton_72_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_72_5.set_style_radius(5, lv.PART.MAIN)
    imagebutton_72_5_label = lv.label(imagebutton_72_5)
    imagebutton_72_5_label.set_text("Testo 72:5 \" \\ Città")
    imagebutton_72_5_label.center()
    imagebutton_72_5_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_72_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # switch: switch_72_6
    switch_72_6 = lv.switch(parent)
    objects["switch_72_6"] = switch_72_6
    switch_72_6.set_pos(580, 105)
    switch_72_6.set_size(139, 24)
    switch_72_6.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_72_6.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_72_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)


def random_72_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_72_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_72_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_72_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_72_get_current_page():
    return current_screen

def random_72_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_72_load_page(0)
