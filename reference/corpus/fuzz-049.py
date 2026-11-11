"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 49
Generated: 2023-11-14T22:14:41.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_49_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # label: label_49_0
    label_49_0 = lv.label(parent)
    objects["label_49_0"] = label_49_0
    label_49_0.set_pos(45, 235)
    label_49_0.set_size(218, 70)
    label_49_0.set_text("Testo 49:0 \" \\ Città")
    label_49_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_49_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_49_0.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # list: list_49_1
    list_49_1 = lv.obj(parent)
    objects["list_49_1"] = list_49_1
    list_49_1.set_pos(70, 200)
    list_49_1.set_size(151, 67)
    list_49_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_49_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_49_1_item_1 = lv.button(list_49_1)
    list_49_1_item_1.set_width(lv.pct(100))
    list_49_1_item_1_label = lv.label(list_49_1_item_1)
    list_49_1_item_1_label.set_text("Item 1")
    list_49_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_49_1_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_49_1_item_2 = lv.button(list_49_1)
    list_49_1_item_2.set_width(lv.pct(100))
    list_49_1_item_2_label = lv.label(list_49_1_item_2)
    list_49_1_item_2_label.set_text("Item 2")
    list_49_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_49_1_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_49_1_item_3 = lv.button(list_49_1)
    list_49_1_item_3.set_width(lv.pct(100))
    list_49_1_item_3_label = lv.label(list_49_1_item_3)
    list_49_1_item_3_label.set_text("Item 3")
    list_49_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_49_1_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_49_1_item_4 = lv.button(list_49_1)
    list_49_1_item_4.set_width(lv.pct(100))
    list_49_1_item_4_label = lv.label(list_49_1_item_4)
    list_49_1_item_4_label.set_text("Item 4")
    list_49_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_49_1_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_49_1_item_5 = lv.button(list_49_1)
    list_49_1_item_5.set_width(lv.pct(100))
    list_49_1_item_5_label = lv.label(list_49_1_item_5)
    list_49_1_item_5_label.set_text("Item 5")
    list_49_1_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_49_1_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # tabview: tabview_49_2
    tabview_49_2 = lv.tabview(parent)
    objects["tabview_49_2"] = tabview_49_2
    tabview_49_2.set_pos(353, 86)
    tabview_49_2.set_size(204, 74)
    tabview_49_2.set_tab_bar_position(lv.DIR.TOP)
    tabview_49_2.set_tab_bar_size(40)
    tabview_49_2_tab_1 = tabview_49_2.add_tab("Tab 1")
    tabview_49_2_tab_2 = tabview_49_2.add_tab("Tab 2")
    tabview_49_2_tab_3 = tabview_49_2.add_tab("Tab 3")
    tabview_49_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # calendar: calendar_49_3
    calendar_49_3 = lv.calendar(parent)
    objects["calendar_49_3"] = calendar_49_3
    calendar_49_3.set_pos(451, 36)
    calendar_49_3.set_size(163, 54)
    calendar_49_3.set_today_date(2026, 10, 28)
    calendar_49_3.set_month_shown(2026, 10)
    calendar_49_3_header = calendar_49_3.add_header_arrow()
    calendar_49_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_49_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_49_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_49_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_49_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_49_get_current_page():
    return current_screen

def random_49_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_49_load_page(0)
