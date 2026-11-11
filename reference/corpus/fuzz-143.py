"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 143
Generated: 2023-11-14T22:16:15.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_143_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: win_143_0
    win_143_0 = lv.obj(parent)
    objects["win_143_0"] = win_143_0
    win_143_0.set_pos(626, 295)
    win_143_0.set_size(167, 137)
    win_143_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_143_0.set_style_pad_all(0, lv.PART.MAIN)
    win_143_0.set_style_pad_row(0, lv.PART.MAIN)
    win_143_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_143_0_header = lv.obj(win_143_0)
    win_143_0_header.set_size(lv.pct(100), 40)
    win_143_0_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_143_0_header.set_style_radius(0, lv.PART.MAIN)
    win_143_0_title = lv.label(win_143_0_header)
    win_143_0_title.set_text("Window Title")
    win_143_0_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_143_0_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_143_0_content = lv.obj(win_143_0)
    win_143_0_content.set_width(lv.pct(100))
    win_143_0_content.set_flex_grow(1)

    # textarea: textarea_143_1
    textarea_143_1 = lv.textarea(parent)
    objects["textarea_143_1"] = textarea_143_1
    textarea_143_1.set_pos(608, 139)
    textarea_143_1.set_size(71, 58)
    textarea_143_1.set_text("Testo 143:1 \" \\ Città")
    textarea_143_1.set_placeholder_text("Type here")
    textarea_143_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_143_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_143_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # panel: panel_143_2
    panel_143_2 = lv.obj(parent)
    objects["panel_143_2"] = panel_143_2
    panel_143_2.set_pos(561, 202)
    panel_143_2.set_size(199, 71)
    panel_143_2.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_143_2.set_style_border_width(2, lv.PART.MAIN)
    panel_143_2.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_143_2.set_style_radius(5, lv.PART.MAIN)
    panel_143_2.set_style_pad_all(0, lv.PART.MAIN)
    panel_143_2.set_style_pad_gap(0, lv.PART.MAIN)

    # spinner: spinner_143_3
    spinner_143_3 = lv.arc(parent)
    objects["spinner_143_3"] = spinner_143_3
    spinner_143_3.set_pos(31, 73)
    spinner_143_3.set_size(184, 84)
    spinner_143_3.set_bg_angles(0, 360)
    spinner_143_3.set_angles(0, 60)
    spinner_143_3.remove_style(None, lv.PART.KNOB)
    spinner_143_3.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_143_3_anim = lv.anim_t()
    spinner_143_3_anim.init()
    spinner_143_3_anim.set_var(spinner_143_3)
    spinner_143_3_anim.set_values(0, 360)
    spinner_143_3_anim.set_duration(1000)
    spinner_143_3_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_143_3_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_143_3_anim.set_custom_exec_cb(lambda _anim, value: spinner_143_3.set_rotation(value))
    spinner_143_3_anim.start()
    spinner_143_3.set_style_arc_width(8, lv.PART.MAIN)
    spinner_143_3.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_143_3.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # panel: panel_143_4
    panel_143_4 = lv.obj(parent)
    objects["panel_143_4"] = panel_143_4
    panel_143_4.set_pos(293, 180)
    panel_143_4.set_size(72, 88)
    panel_143_4.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_143_4.set_style_border_width(2, lv.PART.MAIN)
    panel_143_4.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_143_4.set_style_radius(5, lv.PART.MAIN)
    panel_143_4.set_style_pad_all(0, lv.PART.MAIN)
    panel_143_4.set_style_pad_gap(0, lv.PART.MAIN)


def random_143_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_143_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_143_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_143_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_143_get_current_page():
    return current_screen

def random_143_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_143_load_page(0)
