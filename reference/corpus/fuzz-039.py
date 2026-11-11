"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 39
Generated: 2023-11-14T22:14:31.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_39_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # buttonmatrix: buttonmatrix_39_0
    buttonmatrix_39_0 = lv.buttonmatrix(parent)
    objects["buttonmatrix_39_0"] = buttonmatrix_39_0
    buttonmatrix_39_0.set_pos(335, 339)
    buttonmatrix_39_0.set_size(169, 13)
    buttonmatrix_39_0_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_39_0.set_map(buttonmatrix_39_0_map)
    buttonmatrix_39_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_39_0.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_39_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_39_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # span: span_39_1
    span_39_1 = lv.spangroup(parent)
    objects["span_39_1"] = span_39_1
    span_39_1.set_pos(377, 350)
    span_39_1.set_size(44, 153)
    span_39_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_39_1_span_1 = span_39_1.add_span()
    span_39_1_span_1.set_text("Normal text")
    span_39_1_span_1_style = span_39_1_span_1.get_style()
    span_39_1_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_39_1_span_1_style.set_text_font(lv.font_montserrat_14)
    span_39_1_span_2 = span_39_1.add_span()
    span_39_1_span_2.set_text("Bold text")
    span_39_1_span_2_style = span_39_1_span_2.get_style()
    span_39_1_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_39_1_span_2_style.set_text_font(lv.font_montserrat_16)
    span_39_1_span_3 = span_39_1.add_span()
    span_39_1_span_3.set_text("Small text")
    span_39_1_span_3_style = span_39_1_span_3.get_style()
    span_39_1_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_39_1_span_3_style.set_text_font(lv.font_montserrat_14)
    span_39_1.refresh()

    # roller: roller_39_2
    roller_39_2 = lv.roller(parent)
    objects["roller_39_2"] = roller_39_2
    roller_39_2.set_pos(292, 311)
    roller_39_2.set_size(153, 47)
    roller_39_2.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_39_2.set_visible_row_count(3)
    roller_39_2.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_39_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_39_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_39_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # arc: arc_39_3
    arc_39_3 = lv.arc(parent)
    objects["arc_39_3"] = arc_39_3
    arc_39_3.set_pos(189, 84)
    arc_39_3.set_size(209, 45)
    arc_39_3.set_bg_angles(135, 45)
    arc_39_3.set_range(0, 100)
    arc_39_3.set_value(50)
    arc_39_3.set_style_arc_width(10, lv.PART.MAIN)
    arc_39_3.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_39_3.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_39_3.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_39_3.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # arc: arc_39_4
    arc_39_4 = lv.arc(parent)
    objects["arc_39_4"] = arc_39_4
    arc_39_4.set_pos(331, 210)
    arc_39_4.set_size(196, 79)
    arc_39_4.set_bg_angles(135, 45)
    arc_39_4.set_range(0, 100)
    arc_39_4.set_value(50)
    arc_39_4.set_style_arc_width(10, lv.PART.MAIN)
    arc_39_4.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_39_4.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_39_4.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_39_4.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # arc: arc_39_5
    arc_39_5 = lv.arc(parent)
    objects["arc_39_5"] = arc_39_5
    arc_39_5.set_pos(281, 221)
    arc_39_5.set_size(165, 106)
    arc_39_5.set_bg_angles(135, 45)
    arc_39_5.set_range(0, 100)
    arc_39_5.set_value(50)
    arc_39_5.set_style_arc_width(10, lv.PART.MAIN)
    arc_39_5.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_39_5.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_39_5.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_39_5.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # bar: bar_39_6
    bar_39_6 = lv.bar(parent)
    objects["bar_39_6"] = bar_39_6
    bar_39_6.set_pos(229, 73)
    bar_39_6.set_size(47, 54)
    bar_39_6.set_range(0, 100)
    bar_39_6.set_value(50, False)
    bar_39_6.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_39_6.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # msgbox: msgbox_39_7
    msgbox_39_7 = lv.msgbox(parent)
    objects["msgbox_39_7"] = msgbox_39_7
    msgbox_39_7.set_pos(441, 308)
    msgbox_39_7.set_size(247, 130)
    msgbox_39_7_title = msgbox_39_7.add_title("Notice")
    msgbox_39_7_text = msgbox_39_7.add_text("Testo 39:7 \" \\ Città")
    msgbox_39_7_button_1 = msgbox_39_7.add_footer_button("OK")
    msgbox_39_7_button_2 = msgbox_39_7.add_footer_button("Cancel")
    msgbox_39_7_close = msgbox_39_7.add_close_button()
    msgbox_39_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_39_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_39_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_39_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_39_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_39_get_current_page():
    return current_screen

def random_39_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_39_load_page(0)
