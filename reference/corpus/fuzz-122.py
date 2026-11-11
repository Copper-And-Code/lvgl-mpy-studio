"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 122
Generated: 2023-11-14T22:15:54.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_122_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # button: button_122_0
    button_122_0 = lv.button(parent)
    objects["button_122_0"] = button_122_0
    button_122_0.set_pos(307, 38)
    button_122_0.set_size(116, 26)
    button_122_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_122_0.set_style_radius(5, lv.PART.MAIN)
    button_122_0_label = lv.label(button_122_0)
    button_122_0_label.set_text("Testo 122:0 \" \\ Città")
    button_122_0_label.center()
    button_122_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_122_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # textarea: textarea_122_1
    textarea_122_1 = lv.textarea(parent)
    objects["textarea_122_1"] = textarea_122_1
    textarea_122_1.set_pos(116, 71)
    textarea_122_1.set_size(28, 38)
    textarea_122_1.set_text("Testo 122:1 \" \\ Città")
    textarea_122_1.set_placeholder_text("Type here")
    textarea_122_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_122_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_122_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # roller: roller_122_2
    roller_122_2 = lv.roller(parent)
    objects["roller_122_2"] = roller_122_2
    roller_122_2.set_pos(439, 357)
    roller_122_2.set_size(179, 129)
    roller_122_2.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_122_2.set_visible_row_count(3)
    roller_122_2.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_122_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_122_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_122_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # image: image_122_3
    image_122_3 = lv.image(parent)
    objects["image_122_3"] = image_122_3
    image_122_3.set_pos(131, 204)
    image_122_3.set_size(135, 142)

    # bar: bar_122_4
    bar_122_4 = lv.bar(parent)
    objects["bar_122_4"] = bar_122_4
    bar_122_4.set_pos(601, 38)
    bar_122_4.set_size(109, 65)
    bar_122_4.set_range(0, 100)
    bar_122_4.set_value(50, False)
    bar_122_4.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_122_4.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # switch: switch_122_5
    switch_122_5 = lv.switch(parent)
    objects["switch_122_5"] = switch_122_5
    switch_122_5.set_pos(476, 182)
    switch_122_5.set_size(200, 84)
    switch_122_5.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_122_5.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_122_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # scale: scale_122_6
    scale_122_6 = lv.scale(parent)
    objects["scale_122_6"] = scale_122_6
    scale_122_6.set_pos(504, 131)
    scale_122_6.set_size(191, 34)
    scale_122_6.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_122_6.set_range(0, 100)
    scale_122_6.set_total_tick_count(51)
    scale_122_6.set_major_tick_every(5)
    scale_122_6.set_style_length(15, lv.PART.INDICATOR)
    scale_122_6.set_style_length(8, lv.PART.ITEMS)
    scale_122_6.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_122_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # arc: arc_122_7
    arc_122_7 = lv.arc(parent)
    objects["arc_122_7"] = arc_122_7
    arc_122_7.set_pos(176, 33)
    arc_122_7.set_size(46, 49)
    arc_122_7.set_bg_angles(135, 45)
    arc_122_7.set_range(0, 100)
    arc_122_7.set_value(50)
    arc_122_7.set_style_arc_width(10, lv.PART.MAIN)
    arc_122_7.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_122_7.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_122_7.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_122_7.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)


def random_122_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_122_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_122_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_122_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_122_get_current_page():
    return current_screen

def random_122_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_122_load_page(0)
