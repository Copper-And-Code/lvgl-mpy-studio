"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 119
Generated: 2023-11-14T22:15:51.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_119_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # list: list_119_0
    list_119_0 = lv.obj(parent)
    objects["list_119_0"] = list_119_0
    list_119_0.set_pos(578, 137)
    list_119_0.set_size(38, 28)
    list_119_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_119_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_119_0_item_1 = lv.button(list_119_0)
    list_119_0_item_1.set_width(lv.pct(100))
    list_119_0_item_1_label = lv.label(list_119_0_item_1)
    list_119_0_item_1_label.set_text("Item 1")
    list_119_0_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_119_0_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_119_0_item_2 = lv.button(list_119_0)
    list_119_0_item_2.set_width(lv.pct(100))
    list_119_0_item_2_label = lv.label(list_119_0_item_2)
    list_119_0_item_2_label.set_text("Item 2")
    list_119_0_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_119_0_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_119_0_item_3 = lv.button(list_119_0)
    list_119_0_item_3.set_width(lv.pct(100))
    list_119_0_item_3_label = lv.label(list_119_0_item_3)
    list_119_0_item_3_label.set_text("Item 3")
    list_119_0_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_119_0_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_119_0_item_4 = lv.button(list_119_0)
    list_119_0_item_4.set_width(lv.pct(100))
    list_119_0_item_4_label = lv.label(list_119_0_item_4)
    list_119_0_item_4_label.set_text("Item 4")
    list_119_0_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_119_0_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_119_0_item_5 = lv.button(list_119_0)
    list_119_0_item_5.set_width(lv.pct(100))
    list_119_0_item_5_label = lv.label(list_119_0_item_5)
    list_119_0_item_5_label.set_text("Item 5")
    list_119_0_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_119_0_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # bar: bar_119_1
    bar_119_1 = lv.bar(parent)
    objects["bar_119_1"] = bar_119_1
    bar_119_1.set_pos(522, 72)
    bar_119_1.set_size(210, 44)
    bar_119_1.set_range(0, 100)
    bar_119_1.set_value(50, False)
    bar_119_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_119_1.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # spinner: spinner_119_2
    spinner_119_2 = lv.arc(parent)
    objects["spinner_119_2"] = spinner_119_2
    spinner_119_2.set_pos(143, 36)
    spinner_119_2.set_size(24, 82)
    spinner_119_2.set_bg_angles(0, 360)
    spinner_119_2.set_angles(0, 60)
    spinner_119_2.remove_style(None, lv.PART.KNOB)
    spinner_119_2.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_119_2_anim = lv.anim_t()
    spinner_119_2_anim.init()
    spinner_119_2_anim.set_var(spinner_119_2)
    spinner_119_2_anim.set_values(0, 360)
    spinner_119_2_anim.set_duration(1000)
    spinner_119_2_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_119_2_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_119_2_anim.set_custom_exec_cb(lambda _anim, value: spinner_119_2.set_rotation(value))
    spinner_119_2_anim.start()
    spinner_119_2.set_style_arc_width(8, lv.PART.MAIN)
    spinner_119_2.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_119_2.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # spinbox: spinbox_119_3
    spinbox_119_3 = lv.spinbox(parent)
    objects["spinbox_119_3"] = spinbox_119_3
    spinbox_119_3.set_pos(197, 245)
    spinbox_119_3.set_size(52, 23)
    spinbox_119_3.set_digit_format(4, 0)
    spinbox_119_3.set_range(0, 999)
    spinbox_119_3.set_value(0)
    spinbox_119_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_119_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_119_3.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # led: led_119_4
    led_119_4 = lv.led(parent)
    objects["led_119_4"] = led_119_4
    led_119_4.set_pos(689, 159)
    led_119_4.set_size(26, 100)
    led_119_4.set_color(lv.color_hex(0xFF0000))
    led_119_4.set_brightness(255)

    # switch: switch_119_5
    switch_119_5 = lv.switch(parent)
    objects["switch_119_5"] = switch_119_5
    switch_119_5.set_pos(235, 86)
    switch_119_5.set_size(227, 108)
    switch_119_5.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_119_5.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_119_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)


def random_119_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_119_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_119_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_119_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_119_get_current_page():
    return current_screen

def random_119_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_119_load_page(0)
