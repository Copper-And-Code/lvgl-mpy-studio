"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 105
Generated: 2023-11-14T22:15:37.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_105_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # arc: arc_105_0
    arc_105_0 = lv.arc(parent)
    objects["arc_105_0"] = arc_105_0
    arc_105_0.set_pos(57, 74)
    arc_105_0.set_size(176, 128)
    arc_105_0.set_bg_angles(135, 45)
    arc_105_0.set_range(0, 100)
    arc_105_0.set_value(50)
    arc_105_0.set_style_arc_width(10, lv.PART.MAIN)
    arc_105_0.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_105_0.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_105_0.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_105_0.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # spinbox: spinbox_105_1
    spinbox_105_1 = lv.spinbox(parent)
    objects["spinbox_105_1"] = spinbox_105_1
    spinbox_105_1.set_pos(372, 224)
    spinbox_105_1.set_size(141, 96)
    spinbox_105_1.set_digit_format(4, 0)
    spinbox_105_1.set_range(0, 999)
    spinbox_105_1.set_value(0)
    spinbox_105_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_105_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_105_1.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # scale: scale_105_2
    scale_105_2 = lv.scale(parent)
    objects["scale_105_2"] = scale_105_2
    scale_105_2.set_pos(626, 166)
    scale_105_2.set_size(246, 154)
    scale_105_2.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_105_2.set_range(0, 100)
    scale_105_2.set_total_tick_count(51)
    scale_105_2.set_major_tick_every(5)
    scale_105_2.set_style_length(15, lv.PART.INDICATOR)
    scale_105_2.set_style_length(8, lv.PART.ITEMS)
    scale_105_2.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_105_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # buttonmatrix: buttonmatrix_105_3
    buttonmatrix_105_3 = lv.buttonmatrix(parent)
    objects["buttonmatrix_105_3"] = buttonmatrix_105_3
    buttonmatrix_105_3.set_pos(482, 156)
    buttonmatrix_105_3.set_size(109, 157)
    buttonmatrix_105_3_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_105_3.set_map(buttonmatrix_105_3_map)
    buttonmatrix_105_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_105_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_105_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_105_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # line: line_105_4
    line_105_4 = lv.line(parent)
    objects["line_105_4"] = line_105_4
    line_105_4.set_pos(625, 271)
    line_105_4_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_105_4.set_points(line_105_4_points, 2)
    line_105_4.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_105_4.set_style_line_width(2, lv.PART.MAIN)

    # led: led_105_5
    led_105_5 = lv.led(parent)
    objects["led_105_5"] = led_105_5
    led_105_5.set_pos(268, 281)
    led_105_5.set_size(90, 22)
    led_105_5.set_color(lv.color_hex(0xFF0000))
    led_105_5.set_brightness(255)

    # tabview: tabview_105_6
    tabview_105_6 = lv.tabview(parent)
    objects["tabview_105_6"] = tabview_105_6
    tabview_105_6.set_pos(162, 73)
    tabview_105_6.set_size(21, 85)
    tabview_105_6.set_tab_bar_position(lv.DIR.TOP)
    tabview_105_6.set_tab_bar_size(40)
    tabview_105_6_tab_1 = tabview_105_6.add_tab("Tab 1")
    tabview_105_6_tab_2 = tabview_105_6.add_tab("Tab 2")
    tabview_105_6_tab_3 = tabview_105_6.add_tab("Tab 3")
    tabview_105_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_105_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_105_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_105_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_105_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_105_get_current_page():
    return current_screen

def random_105_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_105_load_page(0)
