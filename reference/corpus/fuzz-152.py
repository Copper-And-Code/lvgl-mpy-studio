"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 152
Generated: 2023-11-14T22:16:24.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_152_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # scale: scale_152_0
    scale_152_0 = lv.scale(parent)
    objects["scale_152_0"] = scale_152_0
    scale_152_0.set_pos(142, 314)
    scale_152_0.set_size(107, 89)
    scale_152_0.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_152_0.set_range(0, 100)
    scale_152_0.set_total_tick_count(51)
    scale_152_0.set_major_tick_every(5)
    scale_152_0.set_style_length(15, lv.PART.INDICATOR)
    scale_152_0.set_style_length(8, lv.PART.ITEMS)
    scale_152_0.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_152_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # line: line_152_1
    line_152_1 = lv.line(parent)
    objects["line_152_1"] = line_152_1
    line_152_1.set_pos(603, 4)
    line_152_1_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_152_1.set_points(line_152_1_points, 2)
    line_152_1.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_152_1.set_style_line_width(2, lv.PART.MAIN)

    # spinbox: spinbox_152_2
    spinbox_152_2 = lv.spinbox(parent)
    objects["spinbox_152_2"] = spinbox_152_2
    spinbox_152_2.set_pos(590, 35)
    spinbox_152_2.set_size(216, 154)
    spinbox_152_2.set_digit_format(4, 0)
    spinbox_152_2.set_range(0, 999)
    spinbox_152_2.set_value(0)
    spinbox_152_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_152_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_152_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # led: led_152_3
    led_152_3 = lv.led(parent)
    objects["led_152_3"] = led_152_3
    led_152_3.set_pos(87, 93)
    led_152_3.set_size(196, 63)
    led_152_3.set_color(lv.color_hex(0xFF0000))
    led_152_3.set_brightness(255)

    # list: list_152_4
    list_152_4 = lv.obj(parent)
    objects["list_152_4"] = list_152_4
    list_152_4.set_pos(611, 75)
    list_152_4.set_size(198, 109)
    list_152_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_152_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_152_4_item_1 = lv.button(list_152_4)
    list_152_4_item_1.set_width(lv.pct(100))
    list_152_4_item_1_label = lv.label(list_152_4_item_1)
    list_152_4_item_1_label.set_text("Item 1")
    list_152_4_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_152_4_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_152_4_item_2 = lv.button(list_152_4)
    list_152_4_item_2.set_width(lv.pct(100))
    list_152_4_item_2_label = lv.label(list_152_4_item_2)
    list_152_4_item_2_label.set_text("Item 2")
    list_152_4_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_152_4_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_152_4_item_3 = lv.button(list_152_4)
    list_152_4_item_3.set_width(lv.pct(100))
    list_152_4_item_3_label = lv.label(list_152_4_item_3)
    list_152_4_item_3_label.set_text("Item 3")
    list_152_4_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_152_4_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_152_4_item_4 = lv.button(list_152_4)
    list_152_4_item_4.set_width(lv.pct(100))
    list_152_4_item_4_label = lv.label(list_152_4_item_4)
    list_152_4_item_4_label.set_text("Item 4")
    list_152_4_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_152_4_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_152_4_item_5 = lv.button(list_152_4)
    list_152_4_item_5.set_width(lv.pct(100))
    list_152_4_item_5_label = lv.label(list_152_4_item_5)
    list_152_4_item_5_label.set_text("Item 5")
    list_152_4_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_152_4_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # dropdown: dropdown_152_5
    dropdown_152_5 = lv.dropdown(parent)
    objects["dropdown_152_5"] = dropdown_152_5
    dropdown_152_5.set_pos(693, 10)
    dropdown_152_5.set_size(66, 124)
    dropdown_152_5.set_options("Option 1\nOption 2\nOption 3")
    dropdown_152_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_152_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_152_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # label: label_152_6
    label_152_6 = lv.label(parent)
    objects["label_152_6"] = label_152_6
    label_152_6.set_pos(617, 161)
    label_152_6.set_size(191, 137)
    label_152_6.set_text("Testo 152:6 \" \\ Città")
    label_152_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_152_6.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_152_6.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # keyboard: keyboard_152_7
    keyboard_152_7 = lv.keyboard(parent)
    objects["keyboard_152_7"] = keyboard_152_7
    keyboard_152_7.set_pos(524, 392)
    keyboard_152_7.set_size(163, 65)


def random_152_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_152_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_152_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_152_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_152_get_current_page():
    return current_screen

def random_152_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_152_load_page(0)
