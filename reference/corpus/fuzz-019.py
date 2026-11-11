"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 19
Generated: 2023-11-14T22:14:11.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_19_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # checkbox: checkbox_19_0
    checkbox_19_0 = lv.checkbox(parent)
    objects["checkbox_19_0"] = checkbox_19_0
    checkbox_19_0.set_pos(150, 137)
    checkbox_19_0.set_text("Testo 19:0 \" \\ Città")
    checkbox_19_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_19_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_19_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # table: table_19_1
    table_19_1 = lv.table(parent)
    objects["table_19_1"] = table_19_1
    table_19_1.set_pos(479, 128)
    table_19_1.set_size(176, 91)
    table_19_1.set_column_count(3)
    table_19_1.set_column_width(0, 100)
    table_19_1.set_column_width(1, 100)
    table_19_1.set_column_width(2, 100)
    table_19_1.set_cell_value(0, 0, "Col 1")
    table_19_1.set_cell_value(0, 1, "Col 2")
    table_19_1.set_cell_value(0, 2, "Col 3")
    table_19_1.set_cell_value(1, 0, "A1")
    table_19_1.set_cell_value(1, 1, "B1")
    table_19_1.set_cell_value(1, 2, "C1")
    table_19_1.set_cell_value(2, 0, "A2")
    table_19_1.set_cell_value(2, 1, "B2")
    table_19_1.set_cell_value(2, 2, "C2")
    table_19_1.set_cell_value(3, 0, "A3")
    table_19_1.set_cell_value(3, 1, "B3")
    table_19_1.set_cell_value(3, 2, "C3")
    table_19_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_19_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_19_1.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_19_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # checkbox: checkbox_19_2
    checkbox_19_2 = lv.checkbox(parent)
    objects["checkbox_19_2"] = checkbox_19_2
    checkbox_19_2.set_pos(454, 298)
    checkbox_19_2.set_text("Testo 19:2 \" \\ Città")
    checkbox_19_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_19_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_19_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # calendar: calendar_19_3
    calendar_19_3 = lv.calendar(parent)
    objects["calendar_19_3"] = calendar_19_3
    calendar_19_3.set_pos(669, 308)
    calendar_19_3.set_size(214, 122)
    calendar_19_3.set_today_date(2026, 10, 28)
    calendar_19_3.set_month_shown(2026, 10)
    calendar_19_3_header = calendar_19_3.add_header_arrow()
    calendar_19_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # spinner: spinner_19_4
    spinner_19_4 = lv.arc(parent)
    objects["spinner_19_4"] = spinner_19_4
    spinner_19_4.set_pos(265, 381)
    spinner_19_4.set_size(149, 75)
    spinner_19_4.set_bg_angles(0, 360)
    spinner_19_4.set_angles(0, 60)
    spinner_19_4.remove_style(None, lv.PART.KNOB)
    spinner_19_4.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_19_4_anim = lv.anim_t()
    spinner_19_4_anim.init()
    spinner_19_4_anim.set_var(spinner_19_4)
    spinner_19_4_anim.set_values(0, 360)
    spinner_19_4_anim.set_duration(1000)
    spinner_19_4_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_19_4_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_19_4_anim.set_custom_exec_cb(lambda _anim, value: spinner_19_4.set_rotation(value))
    spinner_19_4_anim.start()
    spinner_19_4.set_style_arc_width(8, lv.PART.MAIN)
    spinner_19_4.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_19_4.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_19_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_19_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_19_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_19_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_19_get_current_page():
    return current_screen

def random_19_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_19_load_page(0)
