"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 61
Generated: 2023-11-14T22:14:53.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_61_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # list: list_61_0
    list_61_0 = lv.obj(parent)
    objects["list_61_0"] = list_61_0
    list_61_0.set_pos(261, 42)
    list_61_0.set_size(134, 127)
    list_61_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_61_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_61_0_item_1 = lv.button(list_61_0)
    list_61_0_item_1.set_width(lv.pct(100))
    list_61_0_item_1_label = lv.label(list_61_0_item_1)
    list_61_0_item_1_label.set_text("Item 1")
    list_61_0_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_61_0_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_61_0_item_2 = lv.button(list_61_0)
    list_61_0_item_2.set_width(lv.pct(100))
    list_61_0_item_2_label = lv.label(list_61_0_item_2)
    list_61_0_item_2_label.set_text("Item 2")
    list_61_0_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_61_0_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_61_0_item_3 = lv.button(list_61_0)
    list_61_0_item_3.set_width(lv.pct(100))
    list_61_0_item_3_label = lv.label(list_61_0_item_3)
    list_61_0_item_3_label.set_text("Item 3")
    list_61_0_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_61_0_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_61_0_item_4 = lv.button(list_61_0)
    list_61_0_item_4.set_width(lv.pct(100))
    list_61_0_item_4_label = lv.label(list_61_0_item_4)
    list_61_0_item_4_label.set_text("Item 4")
    list_61_0_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_61_0_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_61_0_item_5 = lv.button(list_61_0)
    list_61_0_item_5.set_width(lv.pct(100))
    list_61_0_item_5_label = lv.label(list_61_0_item_5)
    list_61_0_item_5_label.set_text("Item 5")
    list_61_0_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_61_0_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # scale: scale_61_1
    scale_61_1 = lv.scale(parent)
    objects["scale_61_1"] = scale_61_1
    scale_61_1.set_pos(376, 124)
    scale_61_1.set_size(204, 80)
    scale_61_1.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_61_1.set_range(0, 100)
    scale_61_1.set_total_tick_count(51)
    scale_61_1.set_major_tick_every(5)
    scale_61_1.set_style_length(15, lv.PART.INDICATOR)
    scale_61_1.set_style_length(8, lv.PART.ITEMS)
    scale_61_1.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_61_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # scale: scale_61_2
    scale_61_2 = lv.scale(parent)
    objects["scale_61_2"] = scale_61_2
    scale_61_2.set_pos(508, 365)
    scale_61_2.set_size(171, 73)
    scale_61_2.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_61_2.set_range(0, 100)
    scale_61_2.set_total_tick_count(51)
    scale_61_2.set_major_tick_every(5)
    scale_61_2.set_style_length(15, lv.PART.INDICATOR)
    scale_61_2.set_style_length(8, lv.PART.ITEMS)
    scale_61_2.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_61_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # tabview: tabview_61_3
    tabview_61_3 = lv.tabview(parent)
    objects["tabview_61_3"] = tabview_61_3
    tabview_61_3.set_pos(11, 242)
    tabview_61_3.set_size(74, 84)
    tabview_61_3.set_tab_bar_position(lv.DIR.TOP)
    tabview_61_3.set_tab_bar_size(40)
    tabview_61_3_tab_1 = tabview_61_3.add_tab("Tab 1")
    tabview_61_3_tab_2 = tabview_61_3.add_tab("Tab 2")
    tabview_61_3_tab_3 = tabview_61_3.add_tab("Tab 3")
    tabview_61_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_61_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_61_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_61_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_61_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_61_get_current_page():
    return current_screen

def random_61_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_61_load_page(0)
