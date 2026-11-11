"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 87
Generated: 2023-11-14T22:15:19.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_87_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinner: spinner_87_0
    spinner_87_0 = lv.arc(parent)
    objects["spinner_87_0"] = spinner_87_0
    spinner_87_0.set_pos(222, 166)
    spinner_87_0.set_size(196, 89)
    spinner_87_0.set_bg_angles(0, 360)
    spinner_87_0.set_angles(0, 60)
    spinner_87_0.remove_style(None, lv.PART.KNOB)
    spinner_87_0.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_87_0_anim = lv.anim_t()
    spinner_87_0_anim.init()
    spinner_87_0_anim.set_var(spinner_87_0)
    spinner_87_0_anim.set_values(0, 360)
    spinner_87_0_anim.set_duration(1000)
    spinner_87_0_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_87_0_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_87_0_anim.set_custom_exec_cb(lambda _anim, value: spinner_87_0.set_rotation(value))
    spinner_87_0_anim.start()
    spinner_87_0.set_style_arc_width(8, lv.PART.MAIN)
    spinner_87_0.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_87_0.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # spinner: spinner_87_1
    spinner_87_1 = lv.arc(parent)
    objects["spinner_87_1"] = spinner_87_1
    spinner_87_1.set_pos(58, 107)
    spinner_87_1.set_size(35, 73)
    spinner_87_1.set_bg_angles(0, 360)
    spinner_87_1.set_angles(0, 60)
    spinner_87_1.remove_style(None, lv.PART.KNOB)
    spinner_87_1.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_87_1_anim = lv.anim_t()
    spinner_87_1_anim.init()
    spinner_87_1_anim.set_var(spinner_87_1)
    spinner_87_1_anim.set_values(0, 360)
    spinner_87_1_anim.set_duration(1000)
    spinner_87_1_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_87_1_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_87_1_anim.set_custom_exec_cb(lambda _anim, value: spinner_87_1.set_rotation(value))
    spinner_87_1_anim.start()
    spinner_87_1.set_style_arc_width(8, lv.PART.MAIN)
    spinner_87_1.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_87_1.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # spinbox: spinbox_87_2
    spinbox_87_2 = lv.spinbox(parent)
    objects["spinbox_87_2"] = spinbox_87_2
    spinbox_87_2.set_pos(272, 153)
    spinbox_87_2.set_size(243, 154)
    spinbox_87_2.set_digit_format(4, 0)
    spinbox_87_2.set_range(0, 999)
    spinbox_87_2.set_value(0)
    spinbox_87_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_87_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_87_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # win: win_87_3
    win_87_3 = lv.obj(parent)
    objects["win_87_3"] = win_87_3
    win_87_3.set_pos(121, 273)
    win_87_3.set_size(131, 141)
    win_87_3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_87_3.set_style_pad_all(0, lv.PART.MAIN)
    win_87_3.set_style_pad_row(0, lv.PART.MAIN)
    win_87_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_87_3_header = lv.obj(win_87_3)
    win_87_3_header.set_size(lv.pct(100), 40)
    win_87_3_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_87_3_header.set_style_radius(0, lv.PART.MAIN)
    win_87_3_title = lv.label(win_87_3_header)
    win_87_3_title.set_text("Window Title")
    win_87_3_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_87_3_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_87_3_content = lv.obj(win_87_3)
    win_87_3_content.set_width(lv.pct(100))
    win_87_3_content.set_flex_grow(1)

    # image: image_87_4
    image_87_4 = lv.image(parent)
    objects["image_87_4"] = image_87_4
    image_87_4.set_pos(168, 267)
    image_87_4.set_size(97, 46)

    # win: win_87_5
    win_87_5 = lv.obj(parent)
    objects["win_87_5"] = win_87_5
    win_87_5.set_pos(520, 187)
    win_87_5.set_size(37, 84)
    win_87_5.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_87_5.set_style_pad_all(0, lv.PART.MAIN)
    win_87_5.set_style_pad_row(0, lv.PART.MAIN)
    win_87_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_87_5_header = lv.obj(win_87_5)
    win_87_5_header.set_size(lv.pct(100), 40)
    win_87_5_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_87_5_header.set_style_radius(0, lv.PART.MAIN)
    win_87_5_title = lv.label(win_87_5_header)
    win_87_5_title.set_text("Window Title")
    win_87_5_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_87_5_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_87_5_content = lv.obj(win_87_5)
    win_87_5_content.set_width(lv.pct(100))
    win_87_5_content.set_flex_grow(1)


def random_87_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_87_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_87_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_87_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_87_get_current_page():
    return current_screen

def random_87_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_87_load_page(0)
