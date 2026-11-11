"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 138
Generated: 2023-11-14T22:16:10.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def textarea_138_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_138_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # table: table_138_0
    table_138_0 = lv.table(parent)
    objects["table_138_0"] = table_138_0
    table_138_0.set_pos(458, 69)
    table_138_0.set_size(52, 74)
    table_138_0.set_column_count(3)
    table_138_0.set_column_width(0, 100)
    table_138_0.set_column_width(1, 100)
    table_138_0.set_column_width(2, 100)
    table_138_0.set_cell_value(0, 0, "Col 1")
    table_138_0.set_cell_value(0, 1, "Col 2")
    table_138_0.set_cell_value(0, 2, "Col 3")
    table_138_0.set_cell_value(1, 0, "A1")
    table_138_0.set_cell_value(1, 1, "B1")
    table_138_0.set_cell_value(1, 2, "C1")
    table_138_0.set_cell_value(2, 0, "A2")
    table_138_0.set_cell_value(2, 1, "B2")
    table_138_0.set_cell_value(2, 2, "C2")
    table_138_0.set_cell_value(3, 0, "A3")
    table_138_0.set_cell_value(3, 1, "B3")
    table_138_0.set_cell_value(3, 2, "C3")
    table_138_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_138_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_138_0.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_138_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # textarea: textarea_138_1
    textarea_138_1 = lv.textarea(parent)
    objects["textarea_138_1"] = textarea_138_1
    textarea_138_1.set_pos(426, 340)
    textarea_138_1.set_size(78, 123)
    textarea_138_1.set_text("Testo 138:1 \" \\ Città")
    textarea_138_1.set_placeholder_text("Type here")
    textarea_138_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_138_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_138_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    textarea_138_1.add_event_cb(textarea_138_1_changed, lv.EVENT.VALUE_CHANGED, None)

    # dropdown: dropdown_138_2
    dropdown_138_2 = lv.dropdown(parent)
    objects["dropdown_138_2"] = dropdown_138_2
    dropdown_138_2.set_pos(454, 168)
    dropdown_138_2.set_size(165, 143)
    dropdown_138_2.set_options("Option 1\nOption 2\nOption 3")
    dropdown_138_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_138_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_138_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # label: label_138_3
    label_138_3 = lv.label(parent)
    objects["label_138_3"] = label_138_3
    label_138_3.set_pos(143, 259)
    label_138_3.set_size(214, 11)
    label_138_3.set_text("Testo 138:3 \" \\ Città")
    label_138_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_138_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_138_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # dropdown: dropdown_138_4
    dropdown_138_4 = lv.dropdown(parent)
    objects["dropdown_138_4"] = dropdown_138_4
    dropdown_138_4.set_pos(555, 223)
    dropdown_138_4.set_size(195, 29)
    dropdown_138_4.set_options("Option 1\nOption 2\nOption 3")
    dropdown_138_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_138_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_138_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # roller: roller_138_5
    roller_138_5 = lv.roller(parent)
    objects["roller_138_5"] = roller_138_5
    roller_138_5.set_pos(237, 149)
    roller_138_5.set_size(65, 18)
    roller_138_5.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_138_5.set_visible_row_count(3)
    roller_138_5.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_138_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_138_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_138_5.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # tabview: tabview_138_6
    tabview_138_6 = lv.tabview(parent)
    objects["tabview_138_6"] = tabview_138_6
    tabview_138_6.set_pos(408, 72)
    tabview_138_6.set_size(83, 85)
    tabview_138_6.set_tab_bar_position(lv.DIR.TOP)
    tabview_138_6.set_tab_bar_size(40)
    tabview_138_6_tab_1 = tabview_138_6.add_tab("Tab 1")
    tabview_138_6_tab_2 = tabview_138_6.add_tab("Tab 2")
    tabview_138_6_tab_3 = tabview_138_6.add_tab("Tab 3")
    tabview_138_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # line: line_138_7
    line_138_7 = lv.line(parent)
    objects["line_138_7"] = line_138_7
    line_138_7.set_pos(4, 240)
    line_138_7_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_138_7.set_points(line_138_7_points, 2)
    line_138_7.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_138_7.set_style_line_width(2, lv.PART.MAIN)


def random_138_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_138_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_138_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_138_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_138_get_current_page():
    return current_screen

def random_138_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_138_load_page(0)
