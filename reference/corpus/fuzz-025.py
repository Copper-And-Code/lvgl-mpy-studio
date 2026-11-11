"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 25
Generated: 2023-11-14T22:14:17.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_25_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: win_25_0
    win_25_0 = lv.obj(parent)
    objects["win_25_0"] = win_25_0
    win_25_0.set_pos(349, 386)
    win_25_0.set_size(179, 45)
    win_25_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_25_0.set_style_pad_all(0, lv.PART.MAIN)
    win_25_0.set_style_pad_row(0, lv.PART.MAIN)
    win_25_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_25_0_header = lv.obj(win_25_0)
    win_25_0_header.set_size(lv.pct(100), 40)
    win_25_0_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_25_0_header.set_style_radius(0, lv.PART.MAIN)
    win_25_0_title = lv.label(win_25_0_header)
    win_25_0_title.set_text("Window Title")
    win_25_0_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_25_0_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_25_0_content = lv.obj(win_25_0)
    win_25_0_content.set_width(lv.pct(100))
    win_25_0_content.set_flex_grow(1)

    # spinbox: spinbox_25_1
    spinbox_25_1 = lv.spinbox(parent)
    objects["spinbox_25_1"] = spinbox_25_1
    spinbox_25_1.set_pos(333, 153)
    spinbox_25_1.set_size(51, 52)
    spinbox_25_1.set_digit_format(4, 0)
    spinbox_25_1.set_range(0, 999)
    spinbox_25_1.set_value(0)
    spinbox_25_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_25_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_25_1.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # calendar: calendar_25_2
    calendar_25_2 = lv.calendar(parent)
    objects["calendar_25_2"] = calendar_25_2
    calendar_25_2.set_pos(171, 369)
    calendar_25_2.set_size(97, 63)
    calendar_25_2.set_today_date(2026, 10, 28)
    calendar_25_2.set_month_shown(2026, 10)
    calendar_25_2_header = calendar_25_2.add_header_arrow()
    calendar_25_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # span: span_25_3
    span_25_3 = lv.spangroup(parent)
    objects["span_25_3"] = span_25_3
    span_25_3.set_pos(426, 232)
    span_25_3.set_size(37, 79)
    span_25_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_25_3_span_1 = span_25_3.add_span()
    span_25_3_span_1.set_text("Normal text")
    span_25_3_span_1_style = span_25_3_span_1.get_style()
    span_25_3_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_25_3_span_1_style.set_text_font(lv.font_montserrat_14)
    span_25_3_span_2 = span_25_3.add_span()
    span_25_3_span_2.set_text("Bold text")
    span_25_3_span_2_style = span_25_3_span_2.get_style()
    span_25_3_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_25_3_span_2_style.set_text_font(lv.font_montserrat_16)
    span_25_3_span_3 = span_25_3.add_span()
    span_25_3_span_3.set_text("Small text")
    span_25_3_span_3_style = span_25_3_span_3.get_style()
    span_25_3_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_25_3_span_3_style.set_text_font(lv.font_montserrat_14)
    span_25_3.refresh()

    # scale: scale_25_4
    scale_25_4 = lv.scale(parent)
    objects["scale_25_4"] = scale_25_4
    scale_25_4.set_pos(100, 105)
    scale_25_4.set_size(27, 73)
    scale_25_4.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_25_4.set_range(0, 100)
    scale_25_4.set_total_tick_count(51)
    scale_25_4.set_major_tick_every(5)
    scale_25_4.set_style_length(15, lv.PART.INDICATOR)
    scale_25_4.set_style_length(8, lv.PART.ITEMS)
    scale_25_4.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_25_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # bar: bar_25_5
    bar_25_5 = lv.bar(parent)
    objects["bar_25_5"] = bar_25_5
    bar_25_5.set_pos(356, 302)
    bar_25_5.set_size(82, 92)
    bar_25_5.set_range(0, 100)
    bar_25_5.set_value(50, False)
    bar_25_5.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_25_5.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)


def random_25_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_25_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_25_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_25_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_25_get_current_page():
    return current_screen

def random_25_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_25_load_page(0)
