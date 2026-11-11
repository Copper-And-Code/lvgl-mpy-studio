"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 42
Generated: 2023-11-14T22:14:34.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_42_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # calendar: calendar_42_0
    calendar_42_0 = lv.calendar(parent)
    objects["calendar_42_0"] = calendar_42_0
    calendar_42_0.set_pos(91, 396)
    calendar_42_0.set_size(246, 81)
    calendar_42_0.set_today_date(2026, 10, 28)
    calendar_42_0.set_month_shown(2026, 10)
    calendar_42_0_header = calendar_42_0.add_header_arrow()
    calendar_42_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_42_1
    buttonmatrix_42_1 = lv.buttonmatrix(parent)
    objects["buttonmatrix_42_1"] = buttonmatrix_42_1
    buttonmatrix_42_1.set_pos(608, 389)
    buttonmatrix_42_1.set_size(137, 150)
    buttonmatrix_42_1_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_42_1.set_map(buttonmatrix_42_1_map)
    buttonmatrix_42_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_42_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_42_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_42_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # led: led_42_2
    led_42_2 = lv.led(parent)
    objects["led_42_2"] = led_42_2
    led_42_2.set_pos(70, 27)
    led_42_2.set_size(168, 76)
    led_42_2.set_color(lv.color_hex(0xFF0000))
    led_42_2.set_brightness(255)

    # panel: panel_42_3
    panel_42_3 = lv.obj(parent)
    objects["panel_42_3"] = panel_42_3
    panel_42_3.set_pos(249, 389)
    panel_42_3.set_size(249, 54)
    panel_42_3.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_42_3.set_style_border_width(2, lv.PART.MAIN)
    panel_42_3.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_42_3.set_style_radius(5, lv.PART.MAIN)
    panel_42_3.set_style_pad_all(0, lv.PART.MAIN)
    panel_42_3.set_style_pad_gap(0, lv.PART.MAIN)

    # win: win_42_4
    win_42_4 = lv.obj(parent)
    objects["win_42_4"] = win_42_4
    win_42_4.set_pos(127, 35)
    win_42_4.set_size(214, 36)
    win_42_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_42_4.set_style_pad_all(0, lv.PART.MAIN)
    win_42_4.set_style_pad_row(0, lv.PART.MAIN)
    win_42_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_42_4_header = lv.obj(win_42_4)
    win_42_4_header.set_size(lv.pct(100), 40)
    win_42_4_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_42_4_header.set_style_radius(0, lv.PART.MAIN)
    win_42_4_title = lv.label(win_42_4_header)
    win_42_4_title.set_text("Window Title")
    win_42_4_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_42_4_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_42_4_content = lv.obj(win_42_4)
    win_42_4_content.set_width(lv.pct(100))
    win_42_4_content.set_flex_grow(1)

    # list: list_42_5
    list_42_5 = lv.obj(parent)
    objects["list_42_5"] = list_42_5
    list_42_5.set_pos(496, 224)
    list_42_5.set_size(240, 131)
    list_42_5.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_42_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_42_5_item_1 = lv.button(list_42_5)
    list_42_5_item_1.set_width(lv.pct(100))
    list_42_5_item_1_label = lv.label(list_42_5_item_1)
    list_42_5_item_1_label.set_text("Item 1")
    list_42_5_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_42_5_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_42_5_item_2 = lv.button(list_42_5)
    list_42_5_item_2.set_width(lv.pct(100))
    list_42_5_item_2_label = lv.label(list_42_5_item_2)
    list_42_5_item_2_label.set_text("Item 2")
    list_42_5_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_42_5_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_42_5_item_3 = lv.button(list_42_5)
    list_42_5_item_3.set_width(lv.pct(100))
    list_42_5_item_3_label = lv.label(list_42_5_item_3)
    list_42_5_item_3_label.set_text("Item 3")
    list_42_5_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_42_5_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_42_5_item_4 = lv.button(list_42_5)
    list_42_5_item_4.set_width(lv.pct(100))
    list_42_5_item_4_label = lv.label(list_42_5_item_4)
    list_42_5_item_4_label.set_text("Item 4")
    list_42_5_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_42_5_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_42_5_item_5 = lv.button(list_42_5)
    list_42_5_item_5.set_width(lv.pct(100))
    list_42_5_item_5_label = lv.label(list_42_5_item_5)
    list_42_5_item_5_label.set_text("Item 5")
    list_42_5_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_42_5_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # arc: arc_42_6
    arc_42_6 = lv.arc(parent)
    objects["arc_42_6"] = arc_42_6
    arc_42_6.set_pos(483, 89)
    arc_42_6.set_size(63, 152)
    arc_42_6.set_bg_angles(135, 45)
    arc_42_6.set_range(0, 100)
    arc_42_6.set_value(50)
    arc_42_6.set_style_arc_width(10, lv.PART.MAIN)
    arc_42_6.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_42_6.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_42_6.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_42_6.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # slider: slider_42_7
    slider_42_7 = lv.slider(parent)
    objects["slider_42_7"] = slider_42_7
    slider_42_7.set_pos(147, 21)
    slider_42_7.set_size(134, 124)
    slider_42_7.set_range(0, 100)
    slider_42_7.set_value(50, False)
    slider_42_7.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_42_7.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_42_7.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)


def random_42_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_42_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_42_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_42_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_42_get_current_page():
    return current_screen

def random_42_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_42_load_page(0)
