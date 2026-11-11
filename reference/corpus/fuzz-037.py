"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 37
Generated: 2023-11-14T22:14:29.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_37_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: win_37_0
    win_37_0 = lv.obj(parent)
    objects["win_37_0"] = win_37_0
    win_37_0.set_pos(692, 78)
    win_37_0.set_size(61, 60)
    win_37_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_37_0.set_style_pad_all(0, lv.PART.MAIN)
    win_37_0.set_style_pad_row(0, lv.PART.MAIN)
    win_37_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_37_0_header = lv.obj(win_37_0)
    win_37_0_header.set_size(lv.pct(100), 40)
    win_37_0_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_37_0_header.set_style_radius(0, lv.PART.MAIN)
    win_37_0_title = lv.label(win_37_0_header)
    win_37_0_title.set_text("Window Title")
    win_37_0_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_37_0_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_37_0_content = lv.obj(win_37_0)
    win_37_0_content.set_width(lv.pct(100))
    win_37_0_content.set_flex_grow(1)

    # scale: scale_37_1
    scale_37_1 = lv.scale(parent)
    objects["scale_37_1"] = scale_37_1
    scale_37_1.set_pos(61, 226)
    scale_37_1.set_size(114, 145)
    scale_37_1.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_37_1.set_range(0, 100)
    scale_37_1.set_total_tick_count(51)
    scale_37_1.set_major_tick_every(5)
    scale_37_1.set_style_length(15, lv.PART.INDICATOR)
    scale_37_1.set_style_length(8, lv.PART.ITEMS)
    scale_37_1.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_37_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # bar: bar_37_2
    bar_37_2 = lv.bar(parent)
    objects["bar_37_2"] = bar_37_2
    bar_37_2.set_pos(469, 155)
    bar_37_2.set_size(62, 78)
    bar_37_2.set_range(0, 100)
    bar_37_2.set_value(50, False)
    bar_37_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_37_2.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # arc: arc_37_3
    arc_37_3 = lv.arc(parent)
    objects["arc_37_3"] = arc_37_3
    arc_37_3.set_pos(479, 31)
    arc_37_3.set_size(266, 135)
    arc_37_3.set_bg_angles(135, 45)
    arc_37_3.set_range(0, 100)
    arc_37_3.set_value(50)
    arc_37_3.set_style_arc_width(10, lv.PART.MAIN)
    arc_37_3.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_37_3.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_37_3.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_37_3.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # imagebutton: imagebutton_37_4
    imagebutton_37_4 = lv.imagebutton(parent)
    objects["imagebutton_37_4"] = imagebutton_37_4
    imagebutton_37_4.set_pos(492, 228)
    imagebutton_37_4.set_size(190, 131)
    imagebutton_37_4.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_37_4.set_style_radius(5, lv.PART.MAIN)
    imagebutton_37_4_label = lv.label(imagebutton_37_4)
    imagebutton_37_4_label.set_text("Testo 37:4 \" \\ Città")
    imagebutton_37_4_label.center()
    imagebutton_37_4_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_37_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # roller: roller_37_5
    roller_37_5 = lv.roller(parent)
    objects["roller_37_5"] = roller_37_5
    roller_37_5.set_pos(634, 237)
    roller_37_5.set_size(218, 155)
    roller_37_5.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_37_5.set_visible_row_count(3)
    roller_37_5.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_37_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_37_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_37_5.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # imagebutton: imagebutton_37_6
    imagebutton_37_6 = lv.imagebutton(parent)
    objects["imagebutton_37_6"] = imagebutton_37_6
    imagebutton_37_6.set_pos(245, 136)
    imagebutton_37_6.set_size(209, 37)
    imagebutton_37_6.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_37_6.set_style_radius(5, lv.PART.MAIN)
    imagebutton_37_6_label = lv.label(imagebutton_37_6)
    imagebutton_37_6_label.set_text("Testo 37:6 \" \\ Città")
    imagebutton_37_6_label.center()
    imagebutton_37_6_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_37_6_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # spinner: spinner_37_7
    spinner_37_7 = lv.arc(parent)
    objects["spinner_37_7"] = spinner_37_7
    spinner_37_7.set_pos(505, 151)
    spinner_37_7.set_size(226, 132)
    spinner_37_7.set_bg_angles(0, 360)
    spinner_37_7.set_angles(0, 60)
    spinner_37_7.remove_style(None, lv.PART.KNOB)
    spinner_37_7.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_37_7_anim = lv.anim_t()
    spinner_37_7_anim.init()
    spinner_37_7_anim.set_var(spinner_37_7)
    spinner_37_7_anim.set_values(0, 360)
    spinner_37_7_anim.set_duration(1000)
    spinner_37_7_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_37_7_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_37_7_anim.set_custom_exec_cb(lambda _anim, value: spinner_37_7.set_rotation(value))
    spinner_37_7_anim.start()
    spinner_37_7.set_style_arc_width(8, lv.PART.MAIN)
    spinner_37_7.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_37_7.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_37_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_37_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_37_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_37_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_37_get_current_page():
    return current_screen

def random_37_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_37_load_page(0)
