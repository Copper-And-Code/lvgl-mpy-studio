"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 23
Generated: 2023-11-14T22:14:15.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_23_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tileview: tileview_23_0
    tileview_23_0 = lv.tileview(parent)
    objects["tileview_23_0"] = tileview_23_0
    tileview_23_0.set_pos(612, 309)
    tileview_23_0.set_size(130, 57)
    tileview_23_0.add_tile(0, 0, lv.DIR.ALL)
    tileview_23_0.add_tile(1, 0, lv.DIR.ALL)
    tileview_23_0.add_tile(0, 1, lv.DIR.ALL)
    tileview_23_0.add_tile(1, 1, lv.DIR.ALL)
    tileview_23_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # line: line_23_1
    line_23_1 = lv.line(parent)
    objects["line_23_1"] = line_23_1
    line_23_1.set_pos(431, 287)
    line_23_1_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_23_1.set_points(line_23_1_points, 2)
    line_23_1.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_23_1.set_style_line_width(2, lv.PART.MAIN)

    # roller: roller_23_2
    roller_23_2 = lv.roller(parent)
    objects["roller_23_2"] = roller_23_2
    roller_23_2.set_pos(641, 29)
    roller_23_2.set_size(116, 60)
    roller_23_2.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_23_2.set_visible_row_count(3)
    roller_23_2.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_23_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_23_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_23_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # dropdown: dropdown_23_3
    dropdown_23_3 = lv.dropdown(parent)
    objects["dropdown_23_3"] = dropdown_23_3
    dropdown_23_3.set_pos(234, 365)
    dropdown_23_3.set_size(95, 141)
    dropdown_23_3.set_options("Option 1\nOption 2\nOption 3")
    dropdown_23_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_23_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_23_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # list: list_23_4
    list_23_4 = lv.obj(parent)
    objects["list_23_4"] = list_23_4
    list_23_4.set_pos(452, 294)
    list_23_4.set_size(139, 133)
    list_23_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_23_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_23_4_item_1 = lv.button(list_23_4)
    list_23_4_item_1.set_width(lv.pct(100))
    list_23_4_item_1_label = lv.label(list_23_4_item_1)
    list_23_4_item_1_label.set_text("Item 1")
    list_23_4_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_23_4_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_23_4_item_2 = lv.button(list_23_4)
    list_23_4_item_2.set_width(lv.pct(100))
    list_23_4_item_2_label = lv.label(list_23_4_item_2)
    list_23_4_item_2_label.set_text("Item 2")
    list_23_4_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_23_4_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_23_4_item_3 = lv.button(list_23_4)
    list_23_4_item_3.set_width(lv.pct(100))
    list_23_4_item_3_label = lv.label(list_23_4_item_3)
    list_23_4_item_3_label.set_text("Item 3")
    list_23_4_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_23_4_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_23_4_item_4 = lv.button(list_23_4)
    list_23_4_item_4.set_width(lv.pct(100))
    list_23_4_item_4_label = lv.label(list_23_4_item_4)
    list_23_4_item_4_label.set_text("Item 4")
    list_23_4_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_23_4_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_23_4_item_5 = lv.button(list_23_4)
    list_23_4_item_5.set_width(lv.pct(100))
    list_23_4_item_5_label = lv.label(list_23_4_item_5)
    list_23_4_item_5_label.set_text("Item 5")
    list_23_4_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_23_4_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # scale: scale_23_5
    scale_23_5 = lv.scale(parent)
    objects["scale_23_5"] = scale_23_5
    scale_23_5.set_pos(233, 337)
    scale_23_5.set_size(28, 124)
    scale_23_5.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_23_5.set_range(0, 100)
    scale_23_5.set_total_tick_count(51)
    scale_23_5.set_major_tick_every(5)
    scale_23_5.set_style_length(15, lv.PART.INDICATOR)
    scale_23_5.set_style_length(8, lv.PART.ITEMS)
    scale_23_5.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_23_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # line: line_23_6
    line_23_6 = lv.line(parent)
    objects["line_23_6"] = line_23_6
    line_23_6.set_pos(217, 81)
    line_23_6_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_23_6.set_points(line_23_6_points, 2)
    line_23_6.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_23_6.set_style_line_width(2, lv.PART.MAIN)

    # tileview: tileview_23_7
    tileview_23_7 = lv.tileview(parent)
    objects["tileview_23_7"] = tileview_23_7
    tileview_23_7.set_pos(61, 150)
    tileview_23_7.set_size(190, 88)
    tileview_23_7.add_tile(0, 0, lv.DIR.ALL)
    tileview_23_7.add_tile(1, 0, lv.DIR.ALL)
    tileview_23_7.add_tile(0, 1, lv.DIR.ALL)
    tileview_23_7.add_tile(1, 1, lv.DIR.ALL)
    tileview_23_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_23_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_23_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_23_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_23_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_23_get_current_page():
    return current_screen

def random_23_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_23_load_page(0)
