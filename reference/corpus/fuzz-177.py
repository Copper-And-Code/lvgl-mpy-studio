"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 177
Generated: 2023-11-14T22:16:49.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_177_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # image: image_177_0
    image_177_0 = lv.image(parent)
    objects["image_177_0"] = image_177_0
    image_177_0.set_pos(350, 159)
    image_177_0.set_size(94, 103)

    # tileview: tileview_177_1
    tileview_177_1 = lv.tileview(parent)
    objects["tileview_177_1"] = tileview_177_1
    tileview_177_1.set_pos(133, 332)
    tileview_177_1.set_size(244, 85)
    tileview_177_1.add_tile(0, 0, lv.DIR.ALL)
    tileview_177_1.add_tile(1, 0, lv.DIR.ALL)
    tileview_177_1.add_tile(0, 1, lv.DIR.ALL)
    tileview_177_1.add_tile(1, 1, lv.DIR.ALL)
    tileview_177_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # button: button_177_2
    button_177_2 = lv.button(parent)
    objects["button_177_2"] = button_177_2
    button_177_2.set_pos(363, 345)
    button_177_2.set_size(103, 66)
    button_177_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_177_2.set_style_radius(5, lv.PART.MAIN)
    button_177_2_label = lv.label(button_177_2)
    button_177_2_label.set_text("Testo 177:2 \" \\ Città")
    button_177_2_label.center()
    button_177_2_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_177_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_177_3
    buttonmatrix_177_3 = lv.buttonmatrix(parent)
    objects["buttonmatrix_177_3"] = buttonmatrix_177_3
    buttonmatrix_177_3.set_pos(240, 88)
    buttonmatrix_177_3.set_size(176, 149)
    buttonmatrix_177_3_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_177_3.set_map(buttonmatrix_177_3_map)
    buttonmatrix_177_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_177_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_177_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_177_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # roller: roller_177_4
    roller_177_4 = lv.roller(parent)
    objects["roller_177_4"] = roller_177_4
    roller_177_4.set_pos(657, 9)
    roller_177_4.set_size(35, 50)
    roller_177_4.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_177_4.set_visible_row_count(3)
    roller_177_4.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_177_4.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_177_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_177_4.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # menu: menu_177_5
    menu_177_5 = lv.obj(parent)
    objects["menu_177_5"] = menu_177_5
    menu_177_5.set_pos(635, 203)
    menu_177_5.set_size(48, 154)
    menu_177_5.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_177_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_177_5_title = lv.label(menu_177_5)
    menu_177_5_title.set_text("Menu")
    menu_177_5_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_177_5_item_1 = lv.button(menu_177_5)
    menu_177_5_item_1.set_width(lv.pct(100))
    menu_177_5_item_1_label = lv.label(menu_177_5_item_1)
    menu_177_5_item_1_label.set_text("Item 1")
    menu_177_5_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_177_5_item_2 = lv.button(menu_177_5)
    menu_177_5_item_2.set_width(lv.pct(100))
    menu_177_5_item_2_label = lv.label(menu_177_5_item_2)
    menu_177_5_item_2_label.set_text("Item 2")
    menu_177_5_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_177_5_item_3 = lv.button(menu_177_5)
    menu_177_5_item_3.set_width(lv.pct(100))
    menu_177_5_item_3_label = lv.label(menu_177_5_item_3)
    menu_177_5_item_3_label.set_text("Item 3")
    menu_177_5_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_177_5_item_4 = lv.button(menu_177_5)
    menu_177_5_item_4.set_width(lv.pct(100))
    menu_177_5_item_4_label = lv.label(menu_177_5_item_4)
    menu_177_5_item_4_label.set_text("Item 4")
    menu_177_5_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # panel: panel_177_6
    panel_177_6 = lv.obj(parent)
    objects["panel_177_6"] = panel_177_6
    panel_177_6.set_pos(481, 217)
    panel_177_6.set_size(200, 143)
    panel_177_6.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_177_6.set_style_border_width(2, lv.PART.MAIN)
    panel_177_6.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_177_6.set_style_radius(5, lv.PART.MAIN)
    panel_177_6.set_style_pad_all(0, lv.PART.MAIN)
    panel_177_6.set_style_pad_gap(0, lv.PART.MAIN)


def random_177_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_177_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_177_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_177_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_177_get_current_page():
    return current_screen

def random_177_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_177_load_page(0)
