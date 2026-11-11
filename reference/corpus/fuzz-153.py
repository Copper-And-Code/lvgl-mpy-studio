"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 153
Generated: 2023-11-14T22:16:25.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_153_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # switch: switch_153_0
    switch_153_0 = lv.switch(parent)
    objects["switch_153_0"] = switch_153_0
    switch_153_0.set_pos(30, 195)
    switch_153_0.set_size(262, 62)
    switch_153_0.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_153_0.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_153_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # roller: roller_153_1
    roller_153_1 = lv.roller(parent)
    objects["roller_153_1"] = roller_153_1
    roller_153_1.set_pos(220, 94)
    roller_153_1.set_size(51, 40)
    roller_153_1.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_153_1.set_visible_row_count(3)
    roller_153_1.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_153_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_153_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_153_1.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # arc: arc_153_2
    arc_153_2 = lv.arc(parent)
    objects["arc_153_2"] = arc_153_2
    arc_153_2.set_pos(649, 326)
    arc_153_2.set_size(102, 31)
    arc_153_2.set_bg_angles(135, 45)
    arc_153_2.set_range(0, 100)
    arc_153_2.set_value(50)
    arc_153_2.set_style_arc_width(10, lv.PART.MAIN)
    arc_153_2.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_153_2.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_153_2.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_153_2.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # spinner: spinner_153_3
    spinner_153_3 = lv.arc(parent)
    objects["spinner_153_3"] = spinner_153_3
    spinner_153_3.set_pos(243, 381)
    spinner_153_3.set_size(104, 130)
    spinner_153_3.set_bg_angles(0, 360)
    spinner_153_3.set_angles(0, 60)
    spinner_153_3.remove_style(None, lv.PART.KNOB)
    spinner_153_3.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_153_3_anim = lv.anim_t()
    spinner_153_3_anim.init()
    spinner_153_3_anim.set_var(spinner_153_3)
    spinner_153_3_anim.set_values(0, 360)
    spinner_153_3_anim.set_duration(1000)
    spinner_153_3_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_153_3_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_153_3_anim.set_custom_exec_cb(lambda _anim, value: spinner_153_3.set_rotation(value))
    spinner_153_3_anim.start()
    spinner_153_3.set_style_arc_width(8, lv.PART.MAIN)
    spinner_153_3.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_153_3.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_153_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_153_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_153_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_153_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_153_get_current_page():
    return current_screen

def random_153_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_153_load_page(0)
