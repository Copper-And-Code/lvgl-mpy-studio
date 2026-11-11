"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 45
Generated: 2023-11-14T22:14:37.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_45_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # span: span_45_0
    span_45_0 = lv.spangroup(parent)
    objects["span_45_0"] = span_45_0
    span_45_0.set_pos(467, 318)
    span_45_0.set_size(109, 77)
    span_45_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_45_0_span_1 = span_45_0.add_span()
    span_45_0_span_1.set_text("Normal text")
    span_45_0_span_1_style = span_45_0_span_1.get_style()
    span_45_0_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_45_0_span_1_style.set_text_font(lv.font_montserrat_14)
    span_45_0_span_2 = span_45_0.add_span()
    span_45_0_span_2.set_text("Bold text")
    span_45_0_span_2_style = span_45_0_span_2.get_style()
    span_45_0_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_45_0_span_2_style.set_text_font(lv.font_montserrat_16)
    span_45_0_span_3 = span_45_0.add_span()
    span_45_0_span_3.set_text("Small text")
    span_45_0_span_3_style = span_45_0_span_3.get_style()
    span_45_0_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_45_0_span_3_style.set_text_font(lv.font_montserrat_14)
    span_45_0.refresh()

    # textarea: textarea_45_1
    textarea_45_1 = lv.textarea(parent)
    objects["textarea_45_1"] = textarea_45_1
    textarea_45_1.set_pos(641, 316)
    textarea_45_1.set_size(45, 102)
    textarea_45_1.set_text("Testo 45:1 \" \\ Città")
    textarea_45_1.set_placeholder_text("Type here")
    textarea_45_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_45_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_45_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # msgbox: msgbox_45_2
    msgbox_45_2 = lv.msgbox(parent)
    objects["msgbox_45_2"] = msgbox_45_2
    msgbox_45_2.set_pos(441, 19)
    msgbox_45_2.set_size(90, 49)
    msgbox_45_2_title = msgbox_45_2.add_title("Notice")
    msgbox_45_2_text = msgbox_45_2.add_text("Testo 45:2 \" \\ Città")
    msgbox_45_2_button_1 = msgbox_45_2.add_footer_button("OK")
    msgbox_45_2_button_2 = msgbox_45_2.add_footer_button("Cancel")
    msgbox_45_2_close = msgbox_45_2.add_close_button()
    msgbox_45_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_45_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_45_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_45_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_45_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_45_get_current_page():
    return current_screen

def random_45_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_45_load_page(0)
