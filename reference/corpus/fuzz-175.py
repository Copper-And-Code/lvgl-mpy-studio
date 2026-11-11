"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 175
Generated: 2023-11-14T22:16:47.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_175_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: win_175_0
    win_175_0 = lv.obj(parent)
    objects["win_175_0"] = win_175_0
    win_175_0.set_pos(307, 85)
    win_175_0.set_size(136, 69)
    win_175_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_175_0.set_style_pad_all(0, lv.PART.MAIN)
    win_175_0.set_style_pad_row(0, lv.PART.MAIN)
    win_175_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_175_0_header = lv.obj(win_175_0)
    win_175_0_header.set_size(lv.pct(100), 40)
    win_175_0_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_175_0_header.set_style_radius(0, lv.PART.MAIN)
    win_175_0_title = lv.label(win_175_0_header)
    win_175_0_title.set_text("Window Title")
    win_175_0_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_175_0_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_175_0_content = lv.obj(win_175_0)
    win_175_0_content.set_width(lv.pct(100))
    win_175_0_content.set_flex_grow(1)

    # tabview: tabview_175_1
    tabview_175_1 = lv.tabview(parent)
    objects["tabview_175_1"] = tabview_175_1
    tabview_175_1.set_pos(636, 218)
    tabview_175_1.set_size(188, 94)
    tabview_175_1.set_tab_bar_position(lv.DIR.TOP)
    tabview_175_1.set_tab_bar_size(40)
    tabview_175_1_tab_1 = tabview_175_1.add_tab("Tab 1")
    tabview_175_1_tab_2 = tabview_175_1.add_tab("Tab 2")
    tabview_175_1_tab_3 = tabview_175_1.add_tab("Tab 3")
    tabview_175_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # list: list_175_2
    list_175_2 = lv.obj(parent)
    objects["list_175_2"] = list_175_2
    list_175_2.set_pos(664, 4)
    list_175_2.set_size(101, 133)
    list_175_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_175_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_175_2_item_1 = lv.button(list_175_2)
    list_175_2_item_1.set_width(lv.pct(100))
    list_175_2_item_1_label = lv.label(list_175_2_item_1)
    list_175_2_item_1_label.set_text("Item 1")
    list_175_2_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_175_2_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_175_2_item_2 = lv.button(list_175_2)
    list_175_2_item_2.set_width(lv.pct(100))
    list_175_2_item_2_label = lv.label(list_175_2_item_2)
    list_175_2_item_2_label.set_text("Item 2")
    list_175_2_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_175_2_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_175_2_item_3 = lv.button(list_175_2)
    list_175_2_item_3.set_width(lv.pct(100))
    list_175_2_item_3_label = lv.label(list_175_2_item_3)
    list_175_2_item_3_label.set_text("Item 3")
    list_175_2_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_175_2_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_175_2_item_4 = lv.button(list_175_2)
    list_175_2_item_4.set_width(lv.pct(100))
    list_175_2_item_4_label = lv.label(list_175_2_item_4)
    list_175_2_item_4_label.set_text("Item 4")
    list_175_2_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_175_2_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_175_2_item_5 = lv.button(list_175_2)
    list_175_2_item_5.set_width(lv.pct(100))
    list_175_2_item_5_label = lv.label(list_175_2_item_5)
    list_175_2_item_5_label.set_text("Item 5")
    list_175_2_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_175_2_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_175_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_175_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_175_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_175_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_175_get_current_page():
    return current_screen

def random_175_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_175_load_page(0)
