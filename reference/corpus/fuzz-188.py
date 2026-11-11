"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 188
Generated: 2023-11-14T22:17:00.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_188_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # span: span_188_0
    span_188_0 = lv.spangroup(parent)
    objects["span_188_0"] = span_188_0
    span_188_0.set_pos(158, 313)
    span_188_0.set_size(78, 122)
    span_188_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_188_0_span_1 = span_188_0.add_span()
    span_188_0_span_1.set_text("Normal text")
    span_188_0_span_1_style = span_188_0_span_1.get_style()
    span_188_0_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_188_0_span_1_style.set_text_font(lv.font_montserrat_14)
    span_188_0_span_2 = span_188_0.add_span()
    span_188_0_span_2.set_text("Bold text")
    span_188_0_span_2_style = span_188_0_span_2.get_style()
    span_188_0_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_188_0_span_2_style.set_text_font(lv.font_montserrat_16)
    span_188_0_span_3 = span_188_0.add_span()
    span_188_0_span_3.set_text("Small text")
    span_188_0_span_3_style = span_188_0_span_3.get_style()
    span_188_0_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_188_0_span_3_style.set_text_font(lv.font_montserrat_14)
    span_188_0.refresh()

    # menu: menu_188_1
    menu_188_1 = lv.obj(parent)
    objects["menu_188_1"] = menu_188_1
    menu_188_1.set_pos(218, 63)
    menu_188_1.set_size(193, 63)
    menu_188_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_188_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_188_1_title = lv.label(menu_188_1)
    menu_188_1_title.set_text("Menu")
    menu_188_1_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_188_1_item_1 = lv.button(menu_188_1)
    menu_188_1_item_1.set_width(lv.pct(100))
    menu_188_1_item_1_label = lv.label(menu_188_1_item_1)
    menu_188_1_item_1_label.set_text("Item 1")
    menu_188_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_188_1_item_2 = lv.button(menu_188_1)
    menu_188_1_item_2.set_width(lv.pct(100))
    menu_188_1_item_2_label = lv.label(menu_188_1_item_2)
    menu_188_1_item_2_label.set_text("Item 2")
    menu_188_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_188_1_item_3 = lv.button(menu_188_1)
    menu_188_1_item_3.set_width(lv.pct(100))
    menu_188_1_item_3_label = lv.label(menu_188_1_item_3)
    menu_188_1_item_3_label.set_text("Item 3")
    menu_188_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_188_1_item_4 = lv.button(menu_188_1)
    menu_188_1_item_4.set_width(lv.pct(100))
    menu_188_1_item_4_label = lv.label(menu_188_1_item_4)
    menu_188_1_item_4_label.set_text("Item 4")
    menu_188_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # msgbox: msgbox_188_2
    msgbox_188_2 = lv.msgbox(parent)
    objects["msgbox_188_2"] = msgbox_188_2
    msgbox_188_2.set_pos(30, 333)
    msgbox_188_2.set_size(146, 60)
    msgbox_188_2_title = msgbox_188_2.add_title("Notice")
    msgbox_188_2_text = msgbox_188_2.add_text("Testo 188:2 \" \\ Città")
    msgbox_188_2_button_1 = msgbox_188_2.add_footer_button("OK")
    msgbox_188_2_button_2 = msgbox_188_2.add_footer_button("Cancel")
    msgbox_188_2_close = msgbox_188_2.add_close_button()
    msgbox_188_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_188_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_188_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_188_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_188_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_188_get_current_page():
    return current_screen

def random_188_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_188_load_page(0)
