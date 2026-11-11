"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 123
Generated: 2023-11-14T22:15:55.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_123_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # scale: scale_123_0
    scale_123_0 = lv.scale(parent)
    objects["scale_123_0"] = scale_123_0
    scale_123_0.set_pos(99, 144)
    scale_123_0.set_size(159, 17)
    scale_123_0.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_123_0.set_range(0, 100)
    scale_123_0.set_total_tick_count(51)
    scale_123_0.set_major_tick_every(5)
    scale_123_0.set_style_length(15, lv.PART.INDICATOR)
    scale_123_0.set_style_length(8, lv.PART.ITEMS)
    scale_123_0.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_123_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # button: button_123_1
    button_123_1 = lv.button(parent)
    objects["button_123_1"] = button_123_1
    button_123_1.set_pos(228, 176)
    button_123_1.set_size(52, 131)
    button_123_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_123_1.set_style_radius(5, lv.PART.MAIN)
    button_123_1_label = lv.label(button_123_1)
    button_123_1_label.set_text("Testo 123:1 \" \\ Città")
    button_123_1_label.center()
    button_123_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_123_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # line: line_123_2
    line_123_2 = lv.line(parent)
    objects["line_123_2"] = line_123_2
    line_123_2.set_pos(16, 103)
    line_123_2_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_123_2.set_points(line_123_2_points, 2)
    line_123_2.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_123_2.set_style_line_width(2, lv.PART.MAIN)

    # list: list_123_3
    list_123_3 = lv.obj(parent)
    objects["list_123_3"] = list_123_3
    list_123_3.set_pos(171, 102)
    list_123_3.set_size(136, 82)
    list_123_3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_123_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_123_3_item_1 = lv.button(list_123_3)
    list_123_3_item_1.set_width(lv.pct(100))
    list_123_3_item_1_label = lv.label(list_123_3_item_1)
    list_123_3_item_1_label.set_text("Item 1")
    list_123_3_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_123_3_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_123_3_item_2 = lv.button(list_123_3)
    list_123_3_item_2.set_width(lv.pct(100))
    list_123_3_item_2_label = lv.label(list_123_3_item_2)
    list_123_3_item_2_label.set_text("Item 2")
    list_123_3_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_123_3_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_123_3_item_3 = lv.button(list_123_3)
    list_123_3_item_3.set_width(lv.pct(100))
    list_123_3_item_3_label = lv.label(list_123_3_item_3)
    list_123_3_item_3_label.set_text("Item 3")
    list_123_3_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_123_3_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_123_3_item_4 = lv.button(list_123_3)
    list_123_3_item_4.set_width(lv.pct(100))
    list_123_3_item_4_label = lv.label(list_123_3_item_4)
    list_123_3_item_4_label.set_text("Item 4")
    list_123_3_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_123_3_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_123_3_item_5 = lv.button(list_123_3)
    list_123_3_item_5.set_width(lv.pct(100))
    list_123_3_item_5_label = lv.label(list_123_3_item_5)
    list_123_3_item_5_label.set_text("Item 5")
    list_123_3_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_123_3_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # win: win_123_4
    win_123_4 = lv.obj(parent)
    objects["win_123_4"] = win_123_4
    win_123_4.set_pos(509, 181)
    win_123_4.set_size(188, 82)
    win_123_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_123_4.set_style_pad_all(0, lv.PART.MAIN)
    win_123_4.set_style_pad_row(0, lv.PART.MAIN)
    win_123_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_123_4_header = lv.obj(win_123_4)
    win_123_4_header.set_size(lv.pct(100), 40)
    win_123_4_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_123_4_header.set_style_radius(0, lv.PART.MAIN)
    win_123_4_title = lv.label(win_123_4_header)
    win_123_4_title.set_text("Window Title")
    win_123_4_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_123_4_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_123_4_content = lv.obj(win_123_4)
    win_123_4_content.set_width(lv.pct(100))
    win_123_4_content.set_flex_grow(1)

    # line: line_123_5
    line_123_5 = lv.line(parent)
    objects["line_123_5"] = line_123_5
    line_123_5.set_pos(415, 275)
    line_123_5_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_123_5.set_points(line_123_5_points, 2)
    line_123_5.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_123_5.set_style_line_width(2, lv.PART.MAIN)

    # label: label_123_6
    label_123_6 = lv.label(parent)
    objects["label_123_6"] = label_123_6
    label_123_6.set_pos(242, 232)
    label_123_6.set_size(212, 58)
    label_123_6.set_text("Testo 123:6 \" \\ Città")
    label_123_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_123_6.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_123_6.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)


def random_123_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_123_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_123_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_123_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_123_get_current_page():
    return current_screen

def random_123_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_123_load_page(0)
