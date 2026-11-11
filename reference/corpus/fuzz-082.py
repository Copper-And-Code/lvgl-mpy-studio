"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 82
Generated: 2023-11-14T22:15:14.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def checkbox_82_5_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_82_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # line: line_82_0
    line_82_0 = lv.line(parent)
    objects["line_82_0"] = line_82_0
    line_82_0.set_pos(181, 252)
    line_82_0_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_82_0.set_points(line_82_0_points, 2)
    line_82_0.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_82_0.set_style_line_width(2, lv.PART.MAIN)

    # line: line_82_1
    line_82_1 = lv.line(parent)
    objects["line_82_1"] = line_82_1
    line_82_1.set_pos(138, 128)
    line_82_1_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_82_1.set_points(line_82_1_points, 2)
    line_82_1.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_82_1.set_style_line_width(2, lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_82_2
    buttonmatrix_82_2 = lv.buttonmatrix(parent)
    objects["buttonmatrix_82_2"] = buttonmatrix_82_2
    buttonmatrix_82_2.set_pos(345, 281)
    buttonmatrix_82_2.set_size(118, 63)
    buttonmatrix_82_2_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_82_2.set_map(buttonmatrix_82_2_map)
    buttonmatrix_82_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_82_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_82_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_82_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # panel: panel_82_3
    panel_82_3 = lv.obj(parent)
    objects["panel_82_3"] = panel_82_3
    panel_82_3.set_pos(311, 168)
    panel_82_3.set_size(105, 86)
    panel_82_3.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_82_3.set_style_border_width(2, lv.PART.MAIN)
    panel_82_3.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_82_3.set_style_radius(5, lv.PART.MAIN)
    panel_82_3.set_style_pad_all(0, lv.PART.MAIN)
    panel_82_3.set_style_pad_gap(0, lv.PART.MAIN)

    # label: label_82_4
    label_82_4 = lv.label(parent)
    objects["label_82_4"] = label_82_4
    label_82_4.set_pos(699, 268)
    label_82_4.set_size(129, 110)
    label_82_4.set_text("Testo 82:4 \" \\ Città")
    label_82_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_82_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_82_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # checkbox: checkbox_82_5
    checkbox_82_5 = lv.checkbox(parent)
    objects["checkbox_82_5"] = checkbox_82_5
    checkbox_82_5.set_pos(587, 357)
    checkbox_82_5.set_text("Testo 82:5 \" \\ Città")
    checkbox_82_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_82_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_82_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_82_5.add_event_cb(checkbox_82_5_changed, lv.EVENT.VALUE_CHANGED, None)


def random_82_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_82_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_82_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_82_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_82_get_current_page():
    return current_screen

def random_82_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_82_load_page(0)
