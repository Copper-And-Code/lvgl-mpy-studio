"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 97
Generated: 2023-11-14T22:15:29.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_97_0_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # handled by app
        pass

def textarea_97_4_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_97_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # button: button_97_0
    button_97_0 = lv.button(parent)
    objects["button_97_0"] = button_97_0
    button_97_0.set_pos(547, 337)
    button_97_0.set_size(267, 114)
    button_97_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_97_0.set_style_radius(5, lv.PART.MAIN)
    button_97_0_label = lv.label(button_97_0)
    button_97_0_label.set_text("Testo 97:0 \" \\ Città")
    button_97_0_label.center()
    button_97_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_97_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_97_0.add_event_cb(button_97_0_changed, lv.EVENT.CLICKED, None)

    # switch: switch_97_1
    switch_97_1 = lv.switch(parent)
    objects["switch_97_1"] = switch_97_1
    switch_97_1.set_pos(1, 78)
    switch_97_1.set_size(129, 103)
    switch_97_1.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_97_1.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_97_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # menu: menu_97_2
    menu_97_2 = lv.obj(parent)
    objects["menu_97_2"] = menu_97_2
    menu_97_2.set_pos(287, 145)
    menu_97_2.set_size(64, 88)
    menu_97_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_97_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_97_2_title = lv.label(menu_97_2)
    menu_97_2_title.set_text("Menu")
    menu_97_2_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_97_2_item_1 = lv.button(menu_97_2)
    menu_97_2_item_1.set_width(lv.pct(100))
    menu_97_2_item_1_label = lv.label(menu_97_2_item_1)
    menu_97_2_item_1_label.set_text("Item 1")
    menu_97_2_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_97_2_item_2 = lv.button(menu_97_2)
    menu_97_2_item_2.set_width(lv.pct(100))
    menu_97_2_item_2_label = lv.label(menu_97_2_item_2)
    menu_97_2_item_2_label.set_text("Item 2")
    menu_97_2_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_97_2_item_3 = lv.button(menu_97_2)
    menu_97_2_item_3.set_width(lv.pct(100))
    menu_97_2_item_3_label = lv.label(menu_97_2_item_3)
    menu_97_2_item_3_label.set_text("Item 3")
    menu_97_2_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_97_2_item_4 = lv.button(menu_97_2)
    menu_97_2_item_4.set_width(lv.pct(100))
    menu_97_2_item_4_label = lv.label(menu_97_2_item_4)
    menu_97_2_item_4_label.set_text("Item 4")
    menu_97_2_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # tileview: tileview_97_3
    tileview_97_3 = lv.tileview(parent)
    objects["tileview_97_3"] = tileview_97_3
    tileview_97_3.set_pos(233, 112)
    tileview_97_3.set_size(166, 86)
    tileview_97_3.add_tile(0, 0, lv.DIR.ALL)
    tileview_97_3.add_tile(1, 0, lv.DIR.ALL)
    tileview_97_3.add_tile(0, 1, lv.DIR.ALL)
    tileview_97_3.add_tile(1, 1, lv.DIR.ALL)
    tileview_97_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # textarea: textarea_97_4
    textarea_97_4 = lv.textarea(parent)
    objects["textarea_97_4"] = textarea_97_4
    textarea_97_4.set_pos(170, 70)
    textarea_97_4.set_size(181, 70)
    textarea_97_4.set_text("Testo 97:4 \" \\ Città")
    textarea_97_4.set_placeholder_text("Type here")
    textarea_97_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_97_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_97_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    textarea_97_4.add_event_cb(textarea_97_4_changed, lv.EVENT.VALUE_CHANGED, None)

    # spinbox: spinbox_97_5
    spinbox_97_5 = lv.spinbox(parent)
    objects["spinbox_97_5"] = spinbox_97_5
    spinbox_97_5.set_pos(454, 299)
    spinbox_97_5.set_size(266, 37)
    spinbox_97_5.set_digit_format(4, 0)
    spinbox_97_5.set_range(0, 999)
    spinbox_97_5.set_value(0)
    spinbox_97_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_97_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_97_5.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_97_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_97_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_97_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_97_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_97_get_current_page():
    return current_screen

def random_97_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_97_load_page(0)
