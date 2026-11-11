"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 50
Generated: 2023-11-14T22:14:42.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_50_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # arc: arc_50_0
    arc_50_0 = lv.arc(parent)
    objects["arc_50_0"] = arc_50_0
    arc_50_0.set_pos(73, 36)
    arc_50_0.set_size(269, 132)
    arc_50_0.set_bg_angles(135, 45)
    arc_50_0.set_range(0, 100)
    arc_50_0.set_value(50)
    arc_50_0.set_style_arc_width(10, lv.PART.MAIN)
    arc_50_0.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_50_0.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_50_0.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_50_0.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # arc: arc_50_1
    arc_50_1 = lv.arc(parent)
    objects["arc_50_1"] = arc_50_1
    arc_50_1.set_pos(222, 84)
    arc_50_1.set_size(74, 119)
    arc_50_1.set_bg_angles(135, 45)
    arc_50_1.set_range(0, 100)
    arc_50_1.set_value(50)
    arc_50_1.set_style_arc_width(10, lv.PART.MAIN)
    arc_50_1.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_50_1.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_50_1.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_50_1.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # line: line_50_2
    line_50_2 = lv.line(parent)
    objects["line_50_2"] = line_50_2
    line_50_2.set_pos(59, 230)
    line_50_2_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_50_2.set_points(line_50_2_points, 2)
    line_50_2.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_50_2.set_style_line_width(2, lv.PART.MAIN)

    # switch: switch_50_3
    switch_50_3 = lv.switch(parent)
    objects["switch_50_3"] = switch_50_3
    switch_50_3.set_pos(430, 270)
    switch_50_3.set_size(159, 12)
    switch_50_3.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_50_3.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_50_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # label: label_50_4
    label_50_4 = lv.label(parent)
    objects["label_50_4"] = label_50_4
    label_50_4.set_pos(578, 185)
    label_50_4.set_size(190, 71)
    label_50_4.set_text("Testo 50:4 \" \\ Città")
    label_50_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_50_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_50_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # span: span_50_5
    span_50_5 = lv.spangroup(parent)
    objects["span_50_5"] = span_50_5
    span_50_5.set_pos(375, 16)
    span_50_5.set_size(106, 100)
    span_50_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_50_5_span_1 = span_50_5.add_span()
    span_50_5_span_1.set_text("Normal text")
    span_50_5_span_1_style = span_50_5_span_1.get_style()
    span_50_5_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_50_5_span_1_style.set_text_font(lv.font_montserrat_14)
    span_50_5_span_2 = span_50_5.add_span()
    span_50_5_span_2.set_text("Bold text")
    span_50_5_span_2_style = span_50_5_span_2.get_style()
    span_50_5_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_50_5_span_2_style.set_text_font(lv.font_montserrat_16)
    span_50_5_span_3 = span_50_5.add_span()
    span_50_5_span_3.set_text("Small text")
    span_50_5_span_3_style = span_50_5_span_3.get_style()
    span_50_5_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_50_5_span_3_style.set_text_font(lv.font_montserrat_14)
    span_50_5.refresh()

    # spinner: spinner_50_6
    spinner_50_6 = lv.arc(parent)
    objects["spinner_50_6"] = spinner_50_6
    spinner_50_6.set_pos(624, 260)
    spinner_50_6.set_size(159, 108)
    spinner_50_6.set_bg_angles(0, 360)
    spinner_50_6.set_angles(0, 60)
    spinner_50_6.remove_style(None, lv.PART.KNOB)
    spinner_50_6.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_50_6_anim = lv.anim_t()
    spinner_50_6_anim.init()
    spinner_50_6_anim.set_var(spinner_50_6)
    spinner_50_6_anim.set_values(0, 360)
    spinner_50_6_anim.set_duration(1000)
    spinner_50_6_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_50_6_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_50_6_anim.set_custom_exec_cb(lambda _anim, value: spinner_50_6.set_rotation(value))
    spinner_50_6_anim.start()
    spinner_50_6.set_style_arc_width(8, lv.PART.MAIN)
    spinner_50_6.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_50_6.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_50_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_50_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_50_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_50_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_50_get_current_page():
    return current_screen

def random_50_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_50_load_page(0)
