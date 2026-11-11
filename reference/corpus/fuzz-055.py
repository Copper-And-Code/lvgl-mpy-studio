"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 55
Generated: 2023-11-14T22:14:47.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def textarea_55_6_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_55_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # table: table_55_0
    table_55_0 = lv.table(parent)
    objects["table_55_0"] = table_55_0
    table_55_0.set_pos(236, 219)
    table_55_0.set_size(114, 121)
    table_55_0.set_column_count(3)
    table_55_0.set_column_width(0, 100)
    table_55_0.set_column_width(1, 100)
    table_55_0.set_column_width(2, 100)
    table_55_0.set_cell_value(0, 0, "Col 1")
    table_55_0.set_cell_value(0, 1, "Col 2")
    table_55_0.set_cell_value(0, 2, "Col 3")
    table_55_0.set_cell_value(1, 0, "A1")
    table_55_0.set_cell_value(1, 1, "B1")
    table_55_0.set_cell_value(1, 2, "C1")
    table_55_0.set_cell_value(2, 0, "A2")
    table_55_0.set_cell_value(2, 1, "B2")
    table_55_0.set_cell_value(2, 2, "C2")
    table_55_0.set_cell_value(3, 0, "A3")
    table_55_0.set_cell_value(3, 1, "B3")
    table_55_0.set_cell_value(3, 2, "C3")
    table_55_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_55_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_55_0.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_55_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # label: label_55_1
    label_55_1 = lv.label(parent)
    objects["label_55_1"] = label_55_1
    label_55_1.set_pos(155, 99)
    label_55_1.set_size(139, 73)
    label_55_1.set_text("Testo 55:1 \" \\ Città")
    label_55_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_55_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_55_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # checkbox: checkbox_55_2
    checkbox_55_2 = lv.checkbox(parent)
    objects["checkbox_55_2"] = checkbox_55_2
    checkbox_55_2.set_pos(569, 37)
    checkbox_55_2.set_text("Testo 55:2 \" \\ Città")
    checkbox_55_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_55_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_55_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # label: label_55_3
    label_55_3 = lv.label(parent)
    objects["label_55_3"] = label_55_3
    label_55_3.set_pos(550, 1)
    label_55_3.set_size(235, 90)
    label_55_3.set_text("Testo 55:3 \" \\ Città")
    label_55_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_55_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_55_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # win: win_55_4
    win_55_4 = lv.obj(parent)
    objects["win_55_4"] = win_55_4
    win_55_4.set_pos(100, 360)
    win_55_4.set_size(250, 109)
    win_55_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_55_4.set_style_pad_all(0, lv.PART.MAIN)
    win_55_4.set_style_pad_row(0, lv.PART.MAIN)
    win_55_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_55_4_header = lv.obj(win_55_4)
    win_55_4_header.set_size(lv.pct(100), 40)
    win_55_4_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_55_4_header.set_style_radius(0, lv.PART.MAIN)
    win_55_4_title = lv.label(win_55_4_header)
    win_55_4_title.set_text("Window Title")
    win_55_4_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_55_4_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_55_4_content = lv.obj(win_55_4)
    win_55_4_content.set_width(lv.pct(100))
    win_55_4_content.set_flex_grow(1)

    # tabview: tabview_55_5
    tabview_55_5 = lv.tabview(parent)
    objects["tabview_55_5"] = tabview_55_5
    tabview_55_5.set_pos(539, 348)
    tabview_55_5.set_size(167, 64)
    tabview_55_5.set_tab_bar_position(lv.DIR.TOP)
    tabview_55_5.set_tab_bar_size(40)
    tabview_55_5_tab_1 = tabview_55_5.add_tab("Tab 1")
    tabview_55_5_tab_2 = tabview_55_5.add_tab("Tab 2")
    tabview_55_5_tab_3 = tabview_55_5.add_tab("Tab 3")
    tabview_55_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # textarea: textarea_55_6
    textarea_55_6 = lv.textarea(parent)
    objects["textarea_55_6"] = textarea_55_6
    textarea_55_6.set_pos(150, 47)
    textarea_55_6.set_size(249, 126)
    textarea_55_6.set_text("Testo 55:6 \" \\ Città")
    textarea_55_6.set_placeholder_text("Type here")
    textarea_55_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_55_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_55_6.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    textarea_55_6.add_event_cb(textarea_55_6_changed, lv.EVENT.VALUE_CHANGED, None)


def random_55_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_55_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_55_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_55_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_55_get_current_page():
    return current_screen

def random_55_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_55_load_page(0)
