"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 116
Generated: 2023-11-14T22:15:48.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_116_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tileview: tileview_116_0
    tileview_116_0 = lv.tileview(parent)
    objects["tileview_116_0"] = tileview_116_0
    tileview_116_0.set_pos(99, 191)
    tileview_116_0.set_size(184, 19)
    tileview_116_0.add_tile(0, 0, lv.DIR.ALL)
    tileview_116_0.add_tile(1, 0, lv.DIR.ALL)
    tileview_116_0.add_tile(0, 1, lv.DIR.ALL)
    tileview_116_0.add_tile(1, 1, lv.DIR.ALL)
    tileview_116_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # span: span_116_1
    span_116_1 = lv.spangroup(parent)
    objects["span_116_1"] = span_116_1
    span_116_1.set_pos(265, 91)
    span_116_1.set_size(99, 114)
    span_116_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_116_1_span_1 = span_116_1.add_span()
    span_116_1_span_1.set_text("Normal text")
    span_116_1_span_1_style = span_116_1_span_1.get_style()
    span_116_1_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_116_1_span_1_style.set_text_font(lv.font_montserrat_14)
    span_116_1_span_2 = span_116_1.add_span()
    span_116_1_span_2.set_text("Bold text")
    span_116_1_span_2_style = span_116_1_span_2.get_style()
    span_116_1_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_116_1_span_2_style.set_text_font(lv.font_montserrat_16)
    span_116_1_span_3 = span_116_1.add_span()
    span_116_1_span_3.set_text("Small text")
    span_116_1_span_3_style = span_116_1_span_3.get_style()
    span_116_1_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_116_1_span_3_style.set_text_font(lv.font_montserrat_14)
    span_116_1.refresh()

    # roller: roller_116_2
    roller_116_2 = lv.roller(parent)
    objects["roller_116_2"] = roller_116_2
    roller_116_2.set_pos(403, 296)
    roller_116_2.set_size(249, 20)
    roller_116_2.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_116_2.set_visible_row_count(3)
    roller_116_2.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_116_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_116_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_116_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # imagebutton: imagebutton_116_3
    imagebutton_116_3 = lv.imagebutton(parent)
    objects["imagebutton_116_3"] = imagebutton_116_3
    imagebutton_116_3.set_pos(267, 56)
    imagebutton_116_3.set_size(227, 144)
    imagebutton_116_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_116_3.set_style_radius(5, lv.PART.MAIN)
    imagebutton_116_3_label = lv.label(imagebutton_116_3)
    imagebutton_116_3_label.set_text("Testo 116:3 \" \\ Città")
    imagebutton_116_3_label.center()
    imagebutton_116_3_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_116_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # msgbox: msgbox_116_4
    msgbox_116_4 = lv.msgbox(parent)
    objects["msgbox_116_4"] = msgbox_116_4
    msgbox_116_4.set_pos(200, 100)
    msgbox_116_4.set_size(74, 37)
    msgbox_116_4_title = msgbox_116_4.add_title("Notice")
    msgbox_116_4_text = msgbox_116_4.add_text("Testo 116:4 \" \\ Città")
    msgbox_116_4_button_1 = msgbox_116_4.add_footer_button("OK")
    msgbox_116_4_button_2 = msgbox_116_4.add_footer_button("Cancel")
    msgbox_116_4_close = msgbox_116_4.add_close_button()
    msgbox_116_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_116_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_116_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_116_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_116_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_116_get_current_page():
    return current_screen

def random_116_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_116_load_page(0)
