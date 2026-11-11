"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 89
Generated: 2023-11-14T22:15:21.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def textarea_89_2_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_89_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # panel: panel_89_0
    panel_89_0 = lv.obj(parent)
    objects["panel_89_0"] = panel_89_0
    panel_89_0.set_pos(17, 233)
    panel_89_0.set_size(250, 74)
    panel_89_0.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_89_0.set_style_border_width(2, lv.PART.MAIN)
    panel_89_0.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_89_0.set_style_radius(5, lv.PART.MAIN)
    panel_89_0.set_style_pad_all(0, lv.PART.MAIN)
    panel_89_0.set_style_pad_gap(0, lv.PART.MAIN)

    # checkbox: checkbox_89_1
    checkbox_89_1 = lv.checkbox(parent)
    objects["checkbox_89_1"] = checkbox_89_1
    checkbox_89_1.set_pos(520, 254)
    checkbox_89_1.set_text("Testo 89:1 \" \\ Città")
    checkbox_89_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_89_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_89_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # textarea: textarea_89_2
    textarea_89_2 = lv.textarea(parent)
    objects["textarea_89_2"] = textarea_89_2
    textarea_89_2.set_pos(260, 45)
    textarea_89_2.set_size(186, 158)
    textarea_89_2.set_text("Testo 89:2 \" \\ Città")
    textarea_89_2.set_placeholder_text("Type here")
    textarea_89_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_89_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_89_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    textarea_89_2.add_event_cb(textarea_89_2_changed, lv.EVENT.VALUE_CHANGED, None)

    # keyboard: keyboard_89_3
    keyboard_89_3 = lv.keyboard(parent)
    objects["keyboard_89_3"] = keyboard_89_3
    keyboard_89_3.set_pos(500, 139)
    keyboard_89_3.set_size(151, 119)

    # keyboard: keyboard_89_4
    keyboard_89_4 = lv.keyboard(parent)
    objects["keyboard_89_4"] = keyboard_89_4
    keyboard_89_4.set_pos(296, 243)
    keyboard_89_4.set_size(137, 102)

    # textarea: textarea_89_5
    textarea_89_5 = lv.textarea(parent)
    objects["textarea_89_5"] = textarea_89_5
    textarea_89_5.set_pos(269, 200)
    textarea_89_5.set_size(121, 141)
    textarea_89_5.set_text("Testo 89:5 \" \\ Città")
    textarea_89_5.set_placeholder_text("Type here")
    textarea_89_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_89_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_89_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # list: list_89_6
    list_89_6 = lv.obj(parent)
    objects["list_89_6"] = list_89_6
    list_89_6.set_pos(607, 363)
    list_89_6.set_size(167, 62)
    list_89_6.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_89_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_89_6_item_1 = lv.button(list_89_6)
    list_89_6_item_1.set_width(lv.pct(100))
    list_89_6_item_1_label = lv.label(list_89_6_item_1)
    list_89_6_item_1_label.set_text("Item 1")
    list_89_6_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_89_6_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_89_6_item_2 = lv.button(list_89_6)
    list_89_6_item_2.set_width(lv.pct(100))
    list_89_6_item_2_label = lv.label(list_89_6_item_2)
    list_89_6_item_2_label.set_text("Item 2")
    list_89_6_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_89_6_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_89_6_item_3 = lv.button(list_89_6)
    list_89_6_item_3.set_width(lv.pct(100))
    list_89_6_item_3_label = lv.label(list_89_6_item_3)
    list_89_6_item_3_label.set_text("Item 3")
    list_89_6_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_89_6_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_89_6_item_4 = lv.button(list_89_6)
    list_89_6_item_4.set_width(lv.pct(100))
    list_89_6_item_4_label = lv.label(list_89_6_item_4)
    list_89_6_item_4_label.set_text("Item 4")
    list_89_6_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_89_6_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_89_6_item_5 = lv.button(list_89_6)
    list_89_6_item_5.set_width(lv.pct(100))
    list_89_6_item_5_label = lv.label(list_89_6_item_5)
    list_89_6_item_5_label.set_text("Item 5")
    list_89_6_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_89_6_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_89_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_89_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_89_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_89_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_89_get_current_page():
    return current_screen

def random_89_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_89_load_page(0)
