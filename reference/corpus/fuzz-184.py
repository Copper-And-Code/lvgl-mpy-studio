"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 184
Generated: 2023-11-14T22:16:56.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_184_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # switch: switch_184_0
    switch_184_0 = lv.switch(parent)
    objects["switch_184_0"] = switch_184_0
    switch_184_0.set_pos(114, 19)
    switch_184_0.set_size(160, 148)
    switch_184_0.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_184_0.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_184_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # label: label_184_1
    label_184_1 = lv.label(parent)
    objects["label_184_1"] = label_184_1
    label_184_1.set_pos(698, 289)
    label_184_1.set_size(26, 52)
    label_184_1.set_text("Testo 184:1 \" \\ Città")
    label_184_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_184_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_184_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # span: span_184_2
    span_184_2 = lv.spangroup(parent)
    objects["span_184_2"] = span_184_2
    span_184_2.set_pos(379, 58)
    span_184_2.set_size(154, 32)
    span_184_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_184_2_span_1 = span_184_2.add_span()
    span_184_2_span_1.set_text("Normal text")
    span_184_2_span_1_style = span_184_2_span_1.get_style()
    span_184_2_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_184_2_span_1_style.set_text_font(lv.font_montserrat_14)
    span_184_2_span_2 = span_184_2.add_span()
    span_184_2_span_2.set_text("Bold text")
    span_184_2_span_2_style = span_184_2_span_2.get_style()
    span_184_2_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_184_2_span_2_style.set_text_font(lv.font_montserrat_16)
    span_184_2_span_3 = span_184_2.add_span()
    span_184_2_span_3.set_text("Small text")
    span_184_2_span_3_style = span_184_2_span_3.get_style()
    span_184_2_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_184_2_span_3_style.set_text_font(lv.font_montserrat_14)
    span_184_2.refresh()

    # scale: scale_184_3
    scale_184_3 = lv.scale(parent)
    objects["scale_184_3"] = scale_184_3
    scale_184_3.set_pos(601, 158)
    scale_184_3.set_size(48, 132)
    scale_184_3.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_184_3.set_range(0, 100)
    scale_184_3.set_total_tick_count(51)
    scale_184_3.set_major_tick_every(5)
    scale_184_3.set_style_length(15, lv.PART.INDICATOR)
    scale_184_3.set_style_length(8, lv.PART.ITEMS)
    scale_184_3.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_184_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)


def random_184_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_184_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_184_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_184_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_184_get_current_page():
    return current_screen

def random_184_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_184_load_page(0)
