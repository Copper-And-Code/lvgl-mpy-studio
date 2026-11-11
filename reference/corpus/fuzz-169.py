"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 169
Generated: 2023-11-14T22:16:41.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_169_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # span: span_169_0
    span_169_0 = lv.spangroup(parent)
    objects["span_169_0"] = span_169_0
    span_169_0.set_pos(281, 114)
    span_169_0.set_size(258, 157)
    span_169_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_169_0_span_1 = span_169_0.add_span()
    span_169_0_span_1.set_text("Normal text")
    span_169_0_span_1_style = span_169_0_span_1.get_style()
    span_169_0_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_169_0_span_1_style.set_text_font(lv.font_montserrat_14)
    span_169_0_span_2 = span_169_0.add_span()
    span_169_0_span_2.set_text("Bold text")
    span_169_0_span_2_style = span_169_0_span_2.get_style()
    span_169_0_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_169_0_span_2_style.set_text_font(lv.font_montserrat_16)
    span_169_0_span_3 = span_169_0.add_span()
    span_169_0_span_3.set_text("Small text")
    span_169_0_span_3_style = span_169_0_span_3.get_style()
    span_169_0_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_169_0_span_3_style.set_text_font(lv.font_montserrat_14)
    span_169_0.refresh()

    # imagebutton: imagebutton_169_1
    imagebutton_169_1 = lv.imagebutton(parent)
    objects["imagebutton_169_1"] = imagebutton_169_1
    imagebutton_169_1.set_pos(171, 195)
    imagebutton_169_1.set_size(234, 146)
    imagebutton_169_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_169_1.set_style_radius(5, lv.PART.MAIN)
    imagebutton_169_1_label = lv.label(imagebutton_169_1)
    imagebutton_169_1_label.set_text("Testo 169:1 \" \\ Città")
    imagebutton_169_1_label.center()
    imagebutton_169_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_169_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # span: span_169_2
    span_169_2 = lv.spangroup(parent)
    objects["span_169_2"] = span_169_2
    span_169_2.set_pos(497, 320)
    span_169_2.set_size(145, 50)
    span_169_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_169_2_span_1 = span_169_2.add_span()
    span_169_2_span_1.set_text("Normal text")
    span_169_2_span_1_style = span_169_2_span_1.get_style()
    span_169_2_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_169_2_span_1_style.set_text_font(lv.font_montserrat_14)
    span_169_2_span_2 = span_169_2.add_span()
    span_169_2_span_2.set_text("Bold text")
    span_169_2_span_2_style = span_169_2_span_2.get_style()
    span_169_2_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_169_2_span_2_style.set_text_font(lv.font_montserrat_16)
    span_169_2_span_3 = span_169_2.add_span()
    span_169_2_span_3.set_text("Small text")
    span_169_2_span_3_style = span_169_2_span_3.get_style()
    span_169_2_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_169_2_span_3_style.set_text_font(lv.font_montserrat_14)
    span_169_2.refresh()


def random_169_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_169_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_169_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_169_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_169_get_current_page():
    return current_screen

def random_169_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_169_load_page(0)
