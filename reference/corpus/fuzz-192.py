"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 192
Generated: 2023-11-14T22:17:04.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_192_0_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # TODO: handle lv.EVENT.CLICKED
        pass

screens = [None] * 1
current_screen = 0

def random_192_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # button: button_192_0
    button_192_0 = lv.button(parent)
    objects["button_192_0"] = button_192_0
    button_192_0.set_pos(179, 92)
    button_192_0.set_size(182, 144)
    button_192_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_192_0.set_style_radius(5, lv.PART.MAIN)
    button_192_0_label = lv.label(button_192_0)
    button_192_0_label.set_text("Testo 192:0 \" \\ Città")
    button_192_0_label.center()
    button_192_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_192_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_192_0.add_event_cb(button_192_0_changed, lv.EVENT.CLICKED, None)

    # list: list_192_1
    list_192_1 = lv.obj(parent)
    objects["list_192_1"] = list_192_1
    list_192_1.set_pos(506, 157)
    list_192_1.set_size(192, 65)
    list_192_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_192_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_192_1_item_1 = lv.button(list_192_1)
    list_192_1_item_1.set_width(lv.pct(100))
    list_192_1_item_1_label = lv.label(list_192_1_item_1)
    list_192_1_item_1_label.set_text("Item 1")
    list_192_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_192_1_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_192_1_item_2 = lv.button(list_192_1)
    list_192_1_item_2.set_width(lv.pct(100))
    list_192_1_item_2_label = lv.label(list_192_1_item_2)
    list_192_1_item_2_label.set_text("Item 2")
    list_192_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_192_1_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_192_1_item_3 = lv.button(list_192_1)
    list_192_1_item_3.set_width(lv.pct(100))
    list_192_1_item_3_label = lv.label(list_192_1_item_3)
    list_192_1_item_3_label.set_text("Item 3")
    list_192_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_192_1_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_192_1_item_4 = lv.button(list_192_1)
    list_192_1_item_4.set_width(lv.pct(100))
    list_192_1_item_4_label = lv.label(list_192_1_item_4)
    list_192_1_item_4_label.set_text("Item 4")
    list_192_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_192_1_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_192_1_item_5 = lv.button(list_192_1)
    list_192_1_item_5.set_width(lv.pct(100))
    list_192_1_item_5_label = lv.label(list_192_1_item_5)
    list_192_1_item_5_label.set_text("Item 5")
    list_192_1_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_192_1_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # keyboard: keyboard_192_2
    keyboard_192_2 = lv.keyboard(parent)
    objects["keyboard_192_2"] = keyboard_192_2
    keyboard_192_2.set_pos(361, 92)
    keyboard_192_2.set_size(257, 44)

    # scale: scale_192_3
    scale_192_3 = lv.scale(parent)
    objects["scale_192_3"] = scale_192_3
    scale_192_3.set_pos(139, 329)
    scale_192_3.set_size(222, 21)
    scale_192_3.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_192_3.set_range(0, 100)
    scale_192_3.set_total_tick_count(51)
    scale_192_3.set_major_tick_every(5)
    scale_192_3.set_style_length(15, lv.PART.INDICATOR)
    scale_192_3.set_style_length(8, lv.PART.ITEMS)
    scale_192_3.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_192_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # span: span_192_4
    span_192_4 = lv.spangroup(parent)
    objects["span_192_4"] = span_192_4
    span_192_4.set_pos(671, 142)
    span_192_4.set_size(138, 154)
    span_192_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_192_4_span_1 = span_192_4.add_span()
    span_192_4_span_1.set_text("Normal text")
    span_192_4_span_1_style = span_192_4_span_1.get_style()
    span_192_4_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_192_4_span_1_style.set_text_font(lv.font_montserrat_14)
    span_192_4_span_2 = span_192_4.add_span()
    span_192_4_span_2.set_text("Bold text")
    span_192_4_span_2_style = span_192_4_span_2.get_style()
    span_192_4_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_192_4_span_2_style.set_text_font(lv.font_montserrat_16)
    span_192_4_span_3 = span_192_4.add_span()
    span_192_4_span_3.set_text("Small text")
    span_192_4_span_3_style = span_192_4_span_3.get_style()
    span_192_4_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_192_4_span_3_style.set_text_font(lv.font_montserrat_14)
    span_192_4.refresh()

    # bar: bar_192_5
    bar_192_5 = lv.bar(parent)
    objects["bar_192_5"] = bar_192_5
    bar_192_5.set_pos(144, 383)
    bar_192_5.set_size(84, 18)
    bar_192_5.set_range(0, 100)
    bar_192_5.set_value(50, False)
    bar_192_5.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_192_5.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # bar: bar_192_6
    bar_192_6 = lv.bar(parent)
    objects["bar_192_6"] = bar_192_6
    bar_192_6.set_pos(473, 16)
    bar_192_6.set_size(117, 52)
    bar_192_6.set_range(0, 100)
    bar_192_6.set_value(50, False)
    bar_192_6.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_192_6.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # arc: arc_192_7
    arc_192_7 = lv.arc(parent)
    objects["arc_192_7"] = arc_192_7
    arc_192_7.set_pos(475, 289)
    arc_192_7.set_size(195, 80)
    arc_192_7.set_bg_angles(135, 45)
    arc_192_7.set_range(0, 100)
    arc_192_7.set_value(50)
    arc_192_7.set_style_arc_width(10, lv.PART.MAIN)
    arc_192_7.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_192_7.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_192_7.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_192_7.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)


def random_192_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_192_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_192_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_192_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_192_get_current_page():
    return current_screen

def random_192_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_192_load_page(0)
