"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 40
Generated: 2023-11-14T22:14:32.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_40_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # dropdown: dropdown_40_0
    dropdown_40_0 = lv.dropdown(parent)
    objects["dropdown_40_0"] = dropdown_40_0
    dropdown_40_0.set_pos(658, 82)
    dropdown_40_0.set_size(154, 125)
    dropdown_40_0.set_options("Option 1\nOption 2\nOption 3")
    dropdown_40_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_40_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_40_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # arc: arc_40_1
    arc_40_1 = lv.arc(parent)
    objects["arc_40_1"] = arc_40_1
    arc_40_1.set_pos(545, 40)
    arc_40_1.set_size(85, 84)
    arc_40_1.set_bg_angles(135, 45)
    arc_40_1.set_range(0, 100)
    arc_40_1.set_value(50)
    arc_40_1.set_style_arc_width(10, lv.PART.MAIN)
    arc_40_1.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_40_1.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_40_1.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_40_1.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # led: led_40_2
    led_40_2 = lv.led(parent)
    objects["led_40_2"] = led_40_2
    led_40_2.set_pos(121, 56)
    led_40_2.set_size(95, 118)
    led_40_2.set_color(lv.color_hex(0xFF0000))
    led_40_2.set_brightness(255)

    # button: button_40_3
    button_40_3 = lv.button(parent)
    objects["button_40_3"] = button_40_3
    button_40_3.set_pos(203, 333)
    button_40_3.set_size(29, 140)
    button_40_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_40_3.set_style_radius(5, lv.PART.MAIN)
    button_40_3_label = lv.label(button_40_3)
    button_40_3_label.set_text("Testo 40:3 \" \\ Città")
    button_40_3_label.center()
    button_40_3_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_40_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # tileview: tileview_40_4
    tileview_40_4 = lv.tileview(parent)
    objects["tileview_40_4"] = tileview_40_4
    tileview_40_4.set_pos(134, 230)
    tileview_40_4.set_size(102, 71)
    tileview_40_4.add_tile(0, 0, lv.DIR.ALL)
    tileview_40_4.add_tile(1, 0, lv.DIR.ALL)
    tileview_40_4.add_tile(0, 1, lv.DIR.ALL)
    tileview_40_4.add_tile(1, 1, lv.DIR.ALL)
    tileview_40_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # label: label_40_5
    label_40_5 = lv.label(parent)
    objects["label_40_5"] = label_40_5
    label_40_5.set_pos(221, 222)
    label_40_5.set_size(66, 109)
    label_40_5.set_text("Testo 40:5 \" \\ Città")
    label_40_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_40_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_40_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # calendar: calendar_40_6
    calendar_40_6 = lv.calendar(parent)
    objects["calendar_40_6"] = calendar_40_6
    calendar_40_6.set_pos(384, 381)
    calendar_40_6.set_size(110, 121)
    calendar_40_6.set_today_date(2026, 10, 28)
    calendar_40_6.set_month_shown(2026, 10)
    calendar_40_6_header = calendar_40_6.add_header_arrow()
    calendar_40_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # menu: menu_40_7
    menu_40_7 = lv.obj(parent)
    objects["menu_40_7"] = menu_40_7
    menu_40_7.set_pos(594, 365)
    menu_40_7.set_size(158, 103)
    menu_40_7.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_40_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_40_7_title = lv.label(menu_40_7)
    menu_40_7_title.set_text("Menu")
    menu_40_7_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_40_7_item_1 = lv.button(menu_40_7)
    menu_40_7_item_1.set_width(lv.pct(100))
    menu_40_7_item_1_label = lv.label(menu_40_7_item_1)
    menu_40_7_item_1_label.set_text("Item 1")
    menu_40_7_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_40_7_item_2 = lv.button(menu_40_7)
    menu_40_7_item_2.set_width(lv.pct(100))
    menu_40_7_item_2_label = lv.label(menu_40_7_item_2)
    menu_40_7_item_2_label.set_text("Item 2")
    menu_40_7_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_40_7_item_3 = lv.button(menu_40_7)
    menu_40_7_item_3.set_width(lv.pct(100))
    menu_40_7_item_3_label = lv.label(menu_40_7_item_3)
    menu_40_7_item_3_label.set_text("Item 3")
    menu_40_7_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_40_7_item_4 = lv.button(menu_40_7)
    menu_40_7_item_4.set_width(lv.pct(100))
    menu_40_7_item_4_label = lv.label(menu_40_7_item_4)
    menu_40_7_item_4_label.set_text("Item 4")
    menu_40_7_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)


def random_40_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_40_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_40_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_40_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_40_get_current_page():
    return current_screen

def random_40_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_40_load_page(0)
