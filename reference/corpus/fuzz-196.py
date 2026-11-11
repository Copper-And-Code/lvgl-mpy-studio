"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 196
Generated: 2023-11-14T22:17:08.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_196_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # image: image_196_0
    image_196_0 = lv.image(parent)
    objects["image_196_0"] = image_196_0
    image_196_0.set_pos(129, 221)
    image_196_0.set_size(146, 22)

    # label: label_196_1
    label_196_1 = lv.label(parent)
    objects["label_196_1"] = label_196_1
    label_196_1.set_pos(418, 399)
    label_196_1.set_size(219, 16)
    label_196_1.set_text("Testo 196:1 \" \\ Città")
    label_196_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_196_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_196_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # span: span_196_2
    span_196_2 = lv.spangroup(parent)
    objects["span_196_2"] = span_196_2
    span_196_2.set_pos(485, 178)
    span_196_2.set_size(72, 87)
    span_196_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_196_2_span_1 = span_196_2.add_span()
    span_196_2_span_1.set_text("Normal text")
    span_196_2_span_1_style = span_196_2_span_1.get_style()
    span_196_2_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_196_2_span_1_style.set_text_font(lv.font_montserrat_14)
    span_196_2_span_2 = span_196_2.add_span()
    span_196_2_span_2.set_text("Bold text")
    span_196_2_span_2_style = span_196_2_span_2.get_style()
    span_196_2_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_196_2_span_2_style.set_text_font(lv.font_montserrat_16)
    span_196_2_span_3 = span_196_2.add_span()
    span_196_2_span_3.set_text("Small text")
    span_196_2_span_3_style = span_196_2_span_3.get_style()
    span_196_2_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_196_2_span_3_style.set_text_font(lv.font_montserrat_14)
    span_196_2.refresh()

    # arc: arc_196_3
    arc_196_3 = lv.arc(parent)
    objects["arc_196_3"] = arc_196_3
    arc_196_3.set_pos(421, 10)
    arc_196_3.set_size(47, 45)
    arc_196_3.set_bg_angles(135, 45)
    arc_196_3.set_range(0, 100)
    arc_196_3.set_value(50)
    arc_196_3.set_style_arc_width(10, lv.PART.MAIN)
    arc_196_3.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_196_3.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_196_3.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_196_3.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # roller: roller_196_4
    roller_196_4 = lv.roller(parent)
    objects["roller_196_4"] = roller_196_4
    roller_196_4.set_pos(673, 339)
    roller_196_4.set_size(51, 44)
    roller_196_4.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_196_4.set_visible_row_count(3)
    roller_196_4.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_196_4.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_196_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_196_4.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # tileview: tileview_196_5
    tileview_196_5 = lv.tileview(parent)
    objects["tileview_196_5"] = tileview_196_5
    tileview_196_5.set_pos(47, 327)
    tileview_196_5.set_size(177, 74)
    tileview_196_5.add_tile(0, 0, lv.DIR.ALL)
    tileview_196_5.add_tile(1, 0, lv.DIR.ALL)
    tileview_196_5.add_tile(0, 1, lv.DIR.ALL)
    tileview_196_5.add_tile(1, 1, lv.DIR.ALL)
    tileview_196_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_196_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_196_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_196_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_196_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_196_get_current_page():
    return current_screen

def random_196_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_196_load_page(0)
