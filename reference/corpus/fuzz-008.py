"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 8
Generated: 2023-11-14T22:14:00.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_8_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # table: table_8_0
    table_8_0 = lv.table(parent)
    objects["table_8_0"] = table_8_0
    table_8_0.set_pos(24, 64)
    table_8_0.set_size(21, 57)
    table_8_0.set_column_count(3)
    table_8_0.set_column_width(0, 100)
    table_8_0.set_column_width(1, 100)
    table_8_0.set_column_width(2, 100)
    table_8_0.set_cell_value(0, 0, "Col 1")
    table_8_0.set_cell_value(0, 1, "Col 2")
    table_8_0.set_cell_value(0, 2, "Col 3")
    table_8_0.set_cell_value(1, 0, "A1")
    table_8_0.set_cell_value(1, 1, "B1")
    table_8_0.set_cell_value(1, 2, "C1")
    table_8_0.set_cell_value(2, 0, "A2")
    table_8_0.set_cell_value(2, 1, "B2")
    table_8_0.set_cell_value(2, 2, "C2")
    table_8_0.set_cell_value(3, 0, "A3")
    table_8_0.set_cell_value(3, 1, "B3")
    table_8_0.set_cell_value(3, 2, "C3")
    table_8_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_8_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_8_0.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_8_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # keyboard: keyboard_8_1
    keyboard_8_1 = lv.keyboard(parent)
    objects["keyboard_8_1"] = keyboard_8_1
    keyboard_8_1.set_pos(436, 299)
    keyboard_8_1.set_size(211, 97)

    # dropdown: dropdown_8_2
    dropdown_8_2 = lv.dropdown(parent)
    objects["dropdown_8_2"] = dropdown_8_2
    dropdown_8_2.set_pos(399, 157)
    dropdown_8_2.set_size(68, 92)
    dropdown_8_2.set_options("Option 1\nOption 2\nOption 3")
    dropdown_8_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_8_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_8_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # spinbox: spinbox_8_3
    spinbox_8_3 = lv.spinbox(parent)
    objects["spinbox_8_3"] = spinbox_8_3
    spinbox_8_3.set_pos(542, 18)
    spinbox_8_3.set_size(246, 26)
    spinbox_8_3.set_digit_format(4, 0)
    spinbox_8_3.set_range(0, 999)
    spinbox_8_3.set_value(0)
    spinbox_8_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_8_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_8_3.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # spinner: spinner_8_4
    spinner_8_4 = lv.arc(parent)
    objects["spinner_8_4"] = spinner_8_4
    spinner_8_4.set_pos(316, 344)
    spinner_8_4.set_size(134, 35)
    spinner_8_4.set_bg_angles(0, 360)
    spinner_8_4.set_angles(0, 60)
    spinner_8_4.remove_style(None, lv.PART.KNOB)
    spinner_8_4.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_8_4_anim = lv.anim_t()
    spinner_8_4_anim.init()
    spinner_8_4_anim.set_var(spinner_8_4)
    spinner_8_4_anim.set_values(0, 360)
    spinner_8_4_anim.set_duration(1000)
    spinner_8_4_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_8_4_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_8_4_anim.set_custom_exec_cb(lambda _anim, value: spinner_8_4.set_rotation(value))
    spinner_8_4_anim.start()
    spinner_8_4.set_style_arc_width(8, lv.PART.MAIN)
    spinner_8_4.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_8_4.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_8_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_8_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_8_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_8_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_8_get_current_page():
    return current_screen

def random_8_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_8_load_page(0)
