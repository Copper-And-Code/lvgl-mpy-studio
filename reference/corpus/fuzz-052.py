"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 52
Generated: 2023-11-14T22:14:44.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_52_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # imagebutton: imagebutton_52_0
    imagebutton_52_0 = lv.imagebutton(parent)
    objects["imagebutton_52_0"] = imagebutton_52_0
    imagebutton_52_0.set_pos(24, 212)
    imagebutton_52_0.set_size(66, 83)
    imagebutton_52_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_52_0.set_style_radius(5, lv.PART.MAIN)
    imagebutton_52_0_label = lv.label(imagebutton_52_0)
    imagebutton_52_0_label.set_text("Testo 52:0 \" \\ Città")
    imagebutton_52_0_label.center()
    imagebutton_52_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_52_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # keyboard: keyboard_52_1
    keyboard_52_1 = lv.keyboard(parent)
    objects["keyboard_52_1"] = keyboard_52_1
    keyboard_52_1.set_pos(114, 314)
    keyboard_52_1.set_size(89, 17)

    # checkbox: checkbox_52_2
    checkbox_52_2 = lv.checkbox(parent)
    objects["checkbox_52_2"] = checkbox_52_2
    checkbox_52_2.set_pos(543, 15)
    checkbox_52_2.set_text("Testo 52:2 \" \\ Città")
    checkbox_52_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_52_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_52_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # span: span_52_3
    span_52_3 = lv.spangroup(parent)
    objects["span_52_3"] = span_52_3
    span_52_3.set_pos(455, 144)
    span_52_3.set_size(160, 159)
    span_52_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_52_3_span_1 = span_52_3.add_span()
    span_52_3_span_1.set_text("Normal text")
    span_52_3_span_1_style = span_52_3_span_1.get_style()
    span_52_3_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_52_3_span_1_style.set_text_font(lv.font_montserrat_14)
    span_52_3_span_2 = span_52_3.add_span()
    span_52_3_span_2.set_text("Bold text")
    span_52_3_span_2_style = span_52_3_span_2.get_style()
    span_52_3_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_52_3_span_2_style.set_text_font(lv.font_montserrat_16)
    span_52_3_span_3 = span_52_3.add_span()
    span_52_3_span_3.set_text("Small text")
    span_52_3_span_3_style = span_52_3_span_3.get_style()
    span_52_3_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_52_3_span_3_style.set_text_font(lv.font_montserrat_14)
    span_52_3.refresh()

    # arc: arc_52_4
    arc_52_4 = lv.arc(parent)
    objects["arc_52_4"] = arc_52_4
    arc_52_4.set_pos(333, 41)
    arc_52_4.set_size(267, 82)
    arc_52_4.set_bg_angles(135, 45)
    arc_52_4.set_range(0, 100)
    arc_52_4.set_value(50)
    arc_52_4.set_style_arc_width(10, lv.PART.MAIN)
    arc_52_4.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_52_4.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_52_4.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_52_4.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # spinner: spinner_52_5
    spinner_52_5 = lv.arc(parent)
    objects["spinner_52_5"] = spinner_52_5
    spinner_52_5.set_pos(493, 366)
    spinner_52_5.set_size(126, 84)
    spinner_52_5.set_bg_angles(0, 360)
    spinner_52_5.set_angles(0, 60)
    spinner_52_5.remove_style(None, lv.PART.KNOB)
    spinner_52_5.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_52_5_anim = lv.anim_t()
    spinner_52_5_anim.init()
    spinner_52_5_anim.set_var(spinner_52_5)
    spinner_52_5_anim.set_values(0, 360)
    spinner_52_5_anim.set_duration(1000)
    spinner_52_5_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_52_5_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_52_5_anim.set_custom_exec_cb(lambda _anim, value: spinner_52_5.set_rotation(value))
    spinner_52_5_anim.start()
    spinner_52_5.set_style_arc_width(8, lv.PART.MAIN)
    spinner_52_5.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_52_5.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_52_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_52_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_52_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_52_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_52_get_current_page():
    return current_screen

def random_52_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_52_load_page(0)
