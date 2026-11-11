"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 28
Generated: 2023-11-14T22:14:20.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def checkbox_28_3_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_28_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # dropdown: dropdown_28_0
    dropdown_28_0 = lv.dropdown(parent)
    objects["dropdown_28_0"] = dropdown_28_0
    dropdown_28_0.set_pos(494, 67)
    dropdown_28_0.set_size(100, 65)
    dropdown_28_0.set_options("Option 1\nOption 2\nOption 3")
    dropdown_28_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_28_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_28_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # list: list_28_1
    list_28_1 = lv.obj(parent)
    objects["list_28_1"] = list_28_1
    list_28_1.set_pos(4, 137)
    list_28_1.set_size(131, 57)
    list_28_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_28_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_28_1_item_1 = lv.button(list_28_1)
    list_28_1_item_1.set_width(lv.pct(100))
    list_28_1_item_1_label = lv.label(list_28_1_item_1)
    list_28_1_item_1_label.set_text("Item 1")
    list_28_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_28_1_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_28_1_item_2 = lv.button(list_28_1)
    list_28_1_item_2.set_width(lv.pct(100))
    list_28_1_item_2_label = lv.label(list_28_1_item_2)
    list_28_1_item_2_label.set_text("Item 2")
    list_28_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_28_1_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_28_1_item_3 = lv.button(list_28_1)
    list_28_1_item_3.set_width(lv.pct(100))
    list_28_1_item_3_label = lv.label(list_28_1_item_3)
    list_28_1_item_3_label.set_text("Item 3")
    list_28_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_28_1_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_28_1_item_4 = lv.button(list_28_1)
    list_28_1_item_4.set_width(lv.pct(100))
    list_28_1_item_4_label = lv.label(list_28_1_item_4)
    list_28_1_item_4_label.set_text("Item 4")
    list_28_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_28_1_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_28_1_item_5 = lv.button(list_28_1)
    list_28_1_item_5.set_width(lv.pct(100))
    list_28_1_item_5_label = lv.label(list_28_1_item_5)
    list_28_1_item_5_label.set_text("Item 5")
    list_28_1_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_28_1_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # roller: roller_28_2
    roller_28_2 = lv.roller(parent)
    objects["roller_28_2"] = roller_28_2
    roller_28_2.set_pos(233, 282)
    roller_28_2.set_size(109, 148)
    roller_28_2.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_28_2.set_visible_row_count(3)
    roller_28_2.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_28_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_28_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_28_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # checkbox: checkbox_28_3
    checkbox_28_3 = lv.checkbox(parent)
    objects["checkbox_28_3"] = checkbox_28_3
    checkbox_28_3.set_pos(144, 194)
    checkbox_28_3.set_text("Testo 28:3 \" \\ Città")
    checkbox_28_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_28_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_28_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_28_3.add_event_cb(checkbox_28_3_changed, lv.EVENT.VALUE_CHANGED, None)

    # menu: menu_28_4
    menu_28_4 = lv.obj(parent)
    objects["menu_28_4"] = menu_28_4
    menu_28_4.set_pos(498, 18)
    menu_28_4.set_size(67, 139)
    menu_28_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_28_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_28_4_title = lv.label(menu_28_4)
    menu_28_4_title.set_text("Menu")
    menu_28_4_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_28_4_item_1 = lv.button(menu_28_4)
    menu_28_4_item_1.set_width(lv.pct(100))
    menu_28_4_item_1_label = lv.label(menu_28_4_item_1)
    menu_28_4_item_1_label.set_text("Item 1")
    menu_28_4_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_28_4_item_2 = lv.button(menu_28_4)
    menu_28_4_item_2.set_width(lv.pct(100))
    menu_28_4_item_2_label = lv.label(menu_28_4_item_2)
    menu_28_4_item_2_label.set_text("Item 2")
    menu_28_4_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_28_4_item_3 = lv.button(menu_28_4)
    menu_28_4_item_3.set_width(lv.pct(100))
    menu_28_4_item_3_label = lv.label(menu_28_4_item_3)
    menu_28_4_item_3_label.set_text("Item 3")
    menu_28_4_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_28_4_item_4 = lv.button(menu_28_4)
    menu_28_4_item_4.set_width(lv.pct(100))
    menu_28_4_item_4_label = lv.label(menu_28_4_item_4)
    menu_28_4_item_4_label.set_text("Item 4")
    menu_28_4_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)


def random_28_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_28_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_28_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_28_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_28_get_current_page():
    return current_screen

def random_28_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_28_load_page(0)
