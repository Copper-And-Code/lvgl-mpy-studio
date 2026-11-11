"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 157
Generated: 2023-11-14T22:16:29.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_157_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinbox: spinbox_157_0
    spinbox_157_0 = lv.spinbox(parent)
    objects["spinbox_157_0"] = spinbox_157_0
    spinbox_157_0.set_pos(645, 270)
    spinbox_157_0.set_size(223, 125)
    spinbox_157_0.set_digit_format(4, 0)
    spinbox_157_0.set_range(0, 999)
    spinbox_157_0.set_value(0)
    spinbox_157_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_157_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_157_0.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # imagebutton: imagebutton_157_1
    imagebutton_157_1 = lv.imagebutton(parent)
    objects["imagebutton_157_1"] = imagebutton_157_1
    imagebutton_157_1.set_pos(641, 383)
    imagebutton_157_1.set_size(76, 82)
    imagebutton_157_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_157_1.set_style_radius(5, lv.PART.MAIN)
    imagebutton_157_1_label = lv.label(imagebutton_157_1)
    imagebutton_157_1_label.set_text("Testo 157:1 \" \\ Città")
    imagebutton_157_1_label.center()
    imagebutton_157_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_157_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # calendar: calendar_157_2
    calendar_157_2 = lv.calendar(parent)
    objects["calendar_157_2"] = calendar_157_2
    calendar_157_2.set_pos(101, 167)
    calendar_157_2.set_size(241, 19)
    calendar_157_2.set_today_date(2026, 10, 28)
    calendar_157_2.set_month_shown(2026, 10)
    calendar_157_2_header = calendar_157_2.add_header_arrow()
    calendar_157_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # menu: menu_157_3
    menu_157_3 = lv.obj(parent)
    objects["menu_157_3"] = menu_157_3
    menu_157_3.set_pos(558, 155)
    menu_157_3.set_size(200, 129)
    menu_157_3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_157_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_157_3_title = lv.label(menu_157_3)
    menu_157_3_title.set_text("Menu")
    menu_157_3_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_157_3_item_1 = lv.button(menu_157_3)
    menu_157_3_item_1.set_width(lv.pct(100))
    menu_157_3_item_1_label = lv.label(menu_157_3_item_1)
    menu_157_3_item_1_label.set_text("Item 1")
    menu_157_3_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_157_3_item_2 = lv.button(menu_157_3)
    menu_157_3_item_2.set_width(lv.pct(100))
    menu_157_3_item_2_label = lv.label(menu_157_3_item_2)
    menu_157_3_item_2_label.set_text("Item 2")
    menu_157_3_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_157_3_item_3 = lv.button(menu_157_3)
    menu_157_3_item_3.set_width(lv.pct(100))
    menu_157_3_item_3_label = lv.label(menu_157_3_item_3)
    menu_157_3_item_3_label.set_text("Item 3")
    menu_157_3_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_157_3_item_4 = lv.button(menu_157_3)
    menu_157_3_item_4.set_width(lv.pct(100))
    menu_157_3_item_4_label = lv.label(menu_157_3_item_4)
    menu_157_3_item_4_label.set_text("Item 4")
    menu_157_3_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # arc: arc_157_4
    arc_157_4 = lv.arc(parent)
    objects["arc_157_4"] = arc_157_4
    arc_157_4.set_pos(527, 234)
    arc_157_4.set_size(224, 13)
    arc_157_4.set_bg_angles(135, 45)
    arc_157_4.set_range(0, 100)
    arc_157_4.set_value(50)
    arc_157_4.set_style_arc_width(10, lv.PART.MAIN)
    arc_157_4.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_157_4.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_157_4.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_157_4.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # slider: slider_157_5
    slider_157_5 = lv.slider(parent)
    objects["slider_157_5"] = slider_157_5
    slider_157_5.set_pos(255, 197)
    slider_157_5.set_size(147, 57)
    slider_157_5.set_range(0, 100)
    slider_157_5.set_value(50, False)
    slider_157_5.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_157_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_157_5.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)


def random_157_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_157_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_157_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_157_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_157_get_current_page():
    return current_screen

def random_157_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_157_load_page(0)
