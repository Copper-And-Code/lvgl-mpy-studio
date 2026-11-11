"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 159
Generated: 2023-11-14T22:16:31.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_159_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_159_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # line: line_159_0
    line_159_0 = lv.line(parent)
    objects["line_159_0"] = line_159_0
    line_159_0.set_pos(624, 41)
    line_159_0_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_159_0.set_points(line_159_0_points, 2)
    line_159_0.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_159_0.set_style_line_width(2, lv.PART.MAIN)

    # slider: slider_159_1
    slider_159_1 = lv.slider(parent)
    objects["slider_159_1"] = slider_159_1
    slider_159_1.set_pos(410, 239)
    slider_159_1.set_size(222, 98)
    slider_159_1.set_range(0, 100)
    slider_159_1.set_value(50, False)
    slider_159_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_159_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_159_1.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_159_1.add_event_cb(slider_159_1_changed, lv.EVENT.VALUE_CHANGED, None)

    # panel: panel_159_2
    panel_159_2 = lv.obj(parent)
    objects["panel_159_2"] = panel_159_2
    panel_159_2.set_pos(117, 259)
    panel_159_2.set_size(163, 32)
    panel_159_2.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_159_2.set_style_border_width(2, lv.PART.MAIN)
    panel_159_2.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_159_2.set_style_radius(5, lv.PART.MAIN)
    panel_159_2.set_style_pad_all(0, lv.PART.MAIN)
    panel_159_2.set_style_pad_gap(0, lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_159_3
    buttonmatrix_159_3 = lv.buttonmatrix(parent)
    objects["buttonmatrix_159_3"] = buttonmatrix_159_3
    buttonmatrix_159_3.set_pos(548, 84)
    buttonmatrix_159_3.set_size(268, 95)
    buttonmatrix_159_3_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_159_3.set_map(buttonmatrix_159_3_map)
    buttonmatrix_159_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_159_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_159_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_159_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # bar: bar_159_4
    bar_159_4 = lv.bar(parent)
    objects["bar_159_4"] = bar_159_4
    bar_159_4.set_pos(126, 366)
    bar_159_4.set_size(257, 139)
    bar_159_4.set_range(0, 100)
    bar_159_4.set_value(50, False)
    bar_159_4.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_159_4.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # scale: scale_159_5
    scale_159_5 = lv.scale(parent)
    objects["scale_159_5"] = scale_159_5
    scale_159_5.set_pos(615, 263)
    scale_159_5.set_size(66, 150)
    scale_159_5.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_159_5.set_range(0, 100)
    scale_159_5.set_total_tick_count(51)
    scale_159_5.set_major_tick_every(5)
    scale_159_5.set_style_length(15, lv.PART.INDICATOR)
    scale_159_5.set_style_length(8, lv.PART.ITEMS)
    scale_159_5.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_159_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)


def random_159_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_159_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_159_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_159_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_159_get_current_page():
    return current_screen

def random_159_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_159_load_page(0)
