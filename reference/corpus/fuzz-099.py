"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 99
Generated: 2023-11-14T22:15:31.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_99_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: win_99_0
    win_99_0 = lv.obj(parent)
    objects["win_99_0"] = win_99_0
    win_99_0.set_pos(626, 309)
    win_99_0.set_size(80, 118)
    win_99_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_99_0.set_style_pad_all(0, lv.PART.MAIN)
    win_99_0.set_style_pad_row(0, lv.PART.MAIN)
    win_99_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_99_0_header = lv.obj(win_99_0)
    win_99_0_header.set_size(lv.pct(100), 40)
    win_99_0_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_99_0_header.set_style_radius(0, lv.PART.MAIN)
    win_99_0_title = lv.label(win_99_0_header)
    win_99_0_title.set_text("Window Title")
    win_99_0_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_99_0_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_99_0_content = lv.obj(win_99_0)
    win_99_0_content.set_width(lv.pct(100))
    win_99_0_content.set_flex_grow(1)

    # span: span_99_1
    span_99_1 = lv.spangroup(parent)
    objects["span_99_1"] = span_99_1
    span_99_1.set_pos(374, 384)
    span_99_1.set_size(93, 113)
    span_99_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_99_1_span_1 = span_99_1.add_span()
    span_99_1_span_1.set_text("Normal text")
    span_99_1_span_1_style = span_99_1_span_1.get_style()
    span_99_1_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_99_1_span_1_style.set_text_font(lv.font_montserrat_14)
    span_99_1_span_2 = span_99_1.add_span()
    span_99_1_span_2.set_text("Bold text")
    span_99_1_span_2_style = span_99_1_span_2.get_style()
    span_99_1_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_99_1_span_2_style.set_text_font(lv.font_montserrat_16)
    span_99_1_span_3 = span_99_1.add_span()
    span_99_1_span_3.set_text("Small text")
    span_99_1_span_3_style = span_99_1_span_3.get_style()
    span_99_1_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_99_1_span_3_style.set_text_font(lv.font_montserrat_14)
    span_99_1.refresh()


def random_99_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_99_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_99_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_99_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_99_get_current_page():
    return current_screen

def random_99_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_99_load_page(0)
