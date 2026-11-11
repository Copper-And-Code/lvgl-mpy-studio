"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 165
Generated: 2023-11-14T22:16:37.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_165_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinner: spinner_165_0
    spinner_165_0 = lv.arc(parent)
    objects["spinner_165_0"] = spinner_165_0
    spinner_165_0.set_pos(419, 147)
    spinner_165_0.set_size(203, 129)
    spinner_165_0.set_bg_angles(0, 360)
    spinner_165_0.set_angles(0, 60)
    spinner_165_0.remove_style(None, lv.PART.KNOB)
    spinner_165_0.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_165_0_anim = lv.anim_t()
    spinner_165_0_anim.init()
    spinner_165_0_anim.set_var(spinner_165_0)
    spinner_165_0_anim.set_values(0, 360)
    spinner_165_0_anim.set_duration(1000)
    spinner_165_0_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_165_0_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_165_0_anim.set_custom_exec_cb(lambda _anim, value: spinner_165_0.set_rotation(value))
    spinner_165_0_anim.start()
    spinner_165_0.set_style_arc_width(8, lv.PART.MAIN)
    spinner_165_0.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_165_0.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # switch: switch_165_1
    switch_165_1 = lv.switch(parent)
    objects["switch_165_1"] = switch_165_1
    switch_165_1.set_pos(431, 242)
    switch_165_1.set_size(142, 148)
    switch_165_1.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_165_1.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_165_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # dropdown: dropdown_165_2
    dropdown_165_2 = lv.dropdown(parent)
    objects["dropdown_165_2"] = dropdown_165_2
    dropdown_165_2.set_pos(481, 146)
    dropdown_165_2.set_size(258, 136)
    dropdown_165_2.set_options("Option 1\nOption 2\nOption 3")
    dropdown_165_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_165_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_165_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # spinner: spinner_165_3
    spinner_165_3 = lv.arc(parent)
    objects["spinner_165_3"] = spinner_165_3
    spinner_165_3.set_pos(69, 90)
    spinner_165_3.set_size(179, 11)
    spinner_165_3.set_bg_angles(0, 360)
    spinner_165_3.set_angles(0, 60)
    spinner_165_3.remove_style(None, lv.PART.KNOB)
    spinner_165_3.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_165_3_anim = lv.anim_t()
    spinner_165_3_anim.init()
    spinner_165_3_anim.set_var(spinner_165_3)
    spinner_165_3_anim.set_values(0, 360)
    spinner_165_3_anim.set_duration(1000)
    spinner_165_3_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_165_3_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_165_3_anim.set_custom_exec_cb(lambda _anim, value: spinner_165_3.set_rotation(value))
    spinner_165_3_anim.start()
    spinner_165_3.set_style_arc_width(8, lv.PART.MAIN)
    spinner_165_3.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_165_3.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_165_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_165_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_165_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_165_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_165_get_current_page():
    return current_screen

def random_165_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_165_load_page(0)
