"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 36
Generated: 2023-11-14T22:14:28.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_36_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # imagebutton: imagebutton_36_0
    imagebutton_36_0 = lv.imagebutton(parent)
    objects["imagebutton_36_0"] = imagebutton_36_0
    imagebutton_36_0.set_pos(8, 190)
    imagebutton_36_0.set_size(248, 130)
    imagebutton_36_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_36_0.set_style_radius(5, lv.PART.MAIN)
    imagebutton_36_0_label = lv.label(imagebutton_36_0)
    imagebutton_36_0_label.set_text("Testo 36:0 \" \\ Città")
    imagebutton_36_0_label.center()
    imagebutton_36_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_36_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # span: span_36_1
    span_36_1 = lv.spangroup(parent)
    objects["span_36_1"] = span_36_1
    span_36_1.set_pos(644, 199)
    span_36_1.set_size(250, 124)
    span_36_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_36_1_span_1 = span_36_1.add_span()
    span_36_1_span_1.set_text("Normal text")
    span_36_1_span_1_style = span_36_1_span_1.get_style()
    span_36_1_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_36_1_span_1_style.set_text_font(lv.font_montserrat_14)
    span_36_1_span_2 = span_36_1.add_span()
    span_36_1_span_2.set_text("Bold text")
    span_36_1_span_2_style = span_36_1_span_2.get_style()
    span_36_1_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_36_1_span_2_style.set_text_font(lv.font_montserrat_16)
    span_36_1_span_3 = span_36_1.add_span()
    span_36_1_span_3.set_text("Small text")
    span_36_1_span_3_style = span_36_1_span_3.get_style()
    span_36_1_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_36_1_span_3_style.set_text_font(lv.font_montserrat_14)
    span_36_1.refresh()

    # dropdown: dropdown_36_2
    dropdown_36_2 = lv.dropdown(parent)
    objects["dropdown_36_2"] = dropdown_36_2
    dropdown_36_2.set_pos(315, 242)
    dropdown_36_2.set_size(264, 122)
    dropdown_36_2.set_options("Option 1\nOption 2\nOption 3")
    dropdown_36_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_36_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_36_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # tileview: tileview_36_3
    tileview_36_3 = lv.tileview(parent)
    objects["tileview_36_3"] = tileview_36_3
    tileview_36_3.set_pos(506, 331)
    tileview_36_3.set_size(191, 50)
    tileview_36_3.add_tile(0, 0, lv.DIR.ALL)
    tileview_36_3.add_tile(1, 0, lv.DIR.ALL)
    tileview_36_3.add_tile(0, 1, lv.DIR.ALL)
    tileview_36_3.add_tile(1, 1, lv.DIR.ALL)
    tileview_36_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # span: span_36_4
    span_36_4 = lv.spangroup(parent)
    objects["span_36_4"] = span_36_4
    span_36_4.set_pos(136, 127)
    span_36_4.set_size(123, 156)
    span_36_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_36_4_span_1 = span_36_4.add_span()
    span_36_4_span_1.set_text("Normal text")
    span_36_4_span_1_style = span_36_4_span_1.get_style()
    span_36_4_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_36_4_span_1_style.set_text_font(lv.font_montserrat_14)
    span_36_4_span_2 = span_36_4.add_span()
    span_36_4_span_2.set_text("Bold text")
    span_36_4_span_2_style = span_36_4_span_2.get_style()
    span_36_4_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_36_4_span_2_style.set_text_font(lv.font_montserrat_16)
    span_36_4_span_3 = span_36_4.add_span()
    span_36_4_span_3.set_text("Small text")
    span_36_4_span_3_style = span_36_4_span_3.get_style()
    span_36_4_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_36_4_span_3_style.set_text_font(lv.font_montserrat_14)
    span_36_4.refresh()


def random_36_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_36_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_36_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_36_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_36_get_current_page():
    return current_screen

def random_36_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_36_load_page(0)
