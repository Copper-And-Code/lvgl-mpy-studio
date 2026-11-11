"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 144
Generated: 2023-11-14T22:16:16.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_144_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # table: table_144_0
    table_144_0 = lv.table(parent)
    objects["table_144_0"] = table_144_0
    table_144_0.set_pos(310, 183)
    table_144_0.set_size(87, 75)
    table_144_0.set_column_count(3)
    table_144_0.set_column_width(0, 100)
    table_144_0.set_column_width(1, 100)
    table_144_0.set_column_width(2, 100)
    table_144_0.set_cell_value(0, 0, "Col 1")
    table_144_0.set_cell_value(0, 1, "Col 2")
    table_144_0.set_cell_value(0, 2, "Col 3")
    table_144_0.set_cell_value(1, 0, "A1")
    table_144_0.set_cell_value(1, 1, "B1")
    table_144_0.set_cell_value(1, 2, "C1")
    table_144_0.set_cell_value(2, 0, "A2")
    table_144_0.set_cell_value(2, 1, "B2")
    table_144_0.set_cell_value(2, 2, "C2")
    table_144_0.set_cell_value(3, 0, "A3")
    table_144_0.set_cell_value(3, 1, "B3")
    table_144_0.set_cell_value(3, 2, "C3")
    table_144_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_144_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_144_0.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_144_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # roller: roller_144_1
    roller_144_1 = lv.roller(parent)
    objects["roller_144_1"] = roller_144_1
    roller_144_1.set_pos(56, 377)
    roller_144_1.set_size(244, 135)
    roller_144_1.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_144_1.set_visible_row_count(3)
    roller_144_1.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_144_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_144_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_144_1.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_144_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_144_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_144_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_144_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_144_get_current_page():
    return current_screen

def random_144_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_144_load_page(0)
