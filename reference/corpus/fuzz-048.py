"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 48
Generated: 2023-11-14T22:14:40.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_48_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinner: spinner_48_0
    spinner_48_0 = lv.arc(parent)
    objects["spinner_48_0"] = spinner_48_0
    spinner_48_0.set_pos(205, 390)
    spinner_48_0.set_size(218, 107)
    spinner_48_0.set_bg_angles(0, 360)
    spinner_48_0.set_angles(0, 60)
    spinner_48_0.remove_style(None, lv.PART.KNOB)
    spinner_48_0.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_48_0_anim = lv.anim_t()
    spinner_48_0_anim.init()
    spinner_48_0_anim.set_var(spinner_48_0)
    spinner_48_0_anim.set_values(0, 360)
    spinner_48_0_anim.set_duration(1000)
    spinner_48_0_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_48_0_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_48_0_anim.set_custom_exec_cb(lambda _anim, value: spinner_48_0.set_rotation(value))
    spinner_48_0_anim.start()
    spinner_48_0.set_style_arc_width(8, lv.PART.MAIN)
    spinner_48_0.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_48_0.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # spinbox: spinbox_48_1
    spinbox_48_1 = lv.spinbox(parent)
    objects["spinbox_48_1"] = spinbox_48_1
    spinbox_48_1.set_pos(607, 314)
    spinbox_48_1.set_size(167, 36)
    spinbox_48_1.set_digit_format(4, 0)
    spinbox_48_1.set_range(0, 999)
    spinbox_48_1.set_value(0)
    spinbox_48_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_48_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_48_1.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # dropdown: dropdown_48_2
    dropdown_48_2 = lv.dropdown(parent)
    objects["dropdown_48_2"] = dropdown_48_2
    dropdown_48_2.set_pos(415, 276)
    dropdown_48_2.set_size(182, 119)
    dropdown_48_2.set_options("Option 1\nOption 2\nOption 3")
    dropdown_48_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_48_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_48_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_48_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_48_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_48_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_48_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_48_get_current_page():
    return current_screen

def random_48_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_48_load_page(0)
