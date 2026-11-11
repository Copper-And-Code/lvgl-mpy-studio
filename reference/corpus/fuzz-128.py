"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 128
Generated: 2023-11-14T22:16:00.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def checkbox_128_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_128_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tileview: tileview_128_0
    tileview_128_0 = lv.tileview(parent)
    objects["tileview_128_0"] = tileview_128_0
    tileview_128_0.set_pos(69, 236)
    tileview_128_0.set_size(161, 143)
    tileview_128_0.add_tile(0, 0, lv.DIR.ALL)
    tileview_128_0.add_tile(1, 0, lv.DIR.ALL)
    tileview_128_0.add_tile(0, 1, lv.DIR.ALL)
    tileview_128_0.add_tile(1, 1, lv.DIR.ALL)
    tileview_128_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # checkbox: checkbox_128_1
    checkbox_128_1 = lv.checkbox(parent)
    objects["checkbox_128_1"] = checkbox_128_1
    checkbox_128_1.set_pos(650, 42)
    checkbox_128_1.set_text("Testo 128:1 \" \\ Città")
    checkbox_128_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_128_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_128_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_128_1.add_event_cb(checkbox_128_1_changed, lv.EVENT.VALUE_CHANGED, None)

    # button: button_128_2
    button_128_2 = lv.button(parent)
    objects["button_128_2"] = button_128_2
    button_128_2.set_pos(33, 259)
    button_128_2.set_size(179, 42)
    button_128_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_128_2.set_style_radius(5, lv.PART.MAIN)
    button_128_2_label = lv.label(button_128_2)
    button_128_2_label.set_text("Testo 128:2 \" \\ Città")
    button_128_2_label.center()
    button_128_2_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_128_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # win: win_128_3
    win_128_3 = lv.obj(parent)
    objects["win_128_3"] = win_128_3
    win_128_3.set_pos(670, 19)
    win_128_3.set_size(202, 90)
    win_128_3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_128_3.set_style_pad_all(0, lv.PART.MAIN)
    win_128_3.set_style_pad_row(0, lv.PART.MAIN)
    win_128_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_128_3_header = lv.obj(win_128_3)
    win_128_3_header.set_size(lv.pct(100), 40)
    win_128_3_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_128_3_header.set_style_radius(0, lv.PART.MAIN)
    win_128_3_title = lv.label(win_128_3_header)
    win_128_3_title.set_text("Window Title")
    win_128_3_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_128_3_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_128_3_content = lv.obj(win_128_3)
    win_128_3_content.set_width(lv.pct(100))
    win_128_3_content.set_flex_grow(1)

    # label: label_128_4
    label_128_4 = lv.label(parent)
    objects["label_128_4"] = label_128_4
    label_128_4.set_pos(475, 14)
    label_128_4.set_size(263, 73)
    label_128_4.set_text("Testo 128:4 \" \\ Città")
    label_128_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_128_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_128_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # spinner: spinner_128_5
    spinner_128_5 = lv.arc(parent)
    objects["spinner_128_5"] = spinner_128_5
    spinner_128_5.set_pos(652, 66)
    spinner_128_5.set_size(172, 28)
    spinner_128_5.set_bg_angles(0, 360)
    spinner_128_5.set_angles(0, 60)
    spinner_128_5.remove_style(None, lv.PART.KNOB)
    spinner_128_5.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_128_5_anim = lv.anim_t()
    spinner_128_5_anim.init()
    spinner_128_5_anim.set_var(spinner_128_5)
    spinner_128_5_anim.set_values(0, 360)
    spinner_128_5_anim.set_duration(1000)
    spinner_128_5_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_128_5_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_128_5_anim.set_custom_exec_cb(lambda _anim, value: spinner_128_5.set_rotation(value))
    spinner_128_5_anim.start()
    spinner_128_5.set_style_arc_width(8, lv.PART.MAIN)
    spinner_128_5.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_128_5.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # win: win_128_6
    win_128_6 = lv.obj(parent)
    objects["win_128_6"] = win_128_6
    win_128_6.set_pos(687, 378)
    win_128_6.set_size(60, 39)
    win_128_6.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_128_6.set_style_pad_all(0, lv.PART.MAIN)
    win_128_6.set_style_pad_row(0, lv.PART.MAIN)
    win_128_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_128_6_header = lv.obj(win_128_6)
    win_128_6_header.set_size(lv.pct(100), 40)
    win_128_6_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_128_6_header.set_style_radius(0, lv.PART.MAIN)
    win_128_6_title = lv.label(win_128_6_header)
    win_128_6_title.set_text("Window Title")
    win_128_6_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_128_6_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_128_6_content = lv.obj(win_128_6)
    win_128_6_content.set_width(lv.pct(100))
    win_128_6_content.set_flex_grow(1)

    # calendar: calendar_128_7
    calendar_128_7 = lv.calendar(parent)
    objects["calendar_128_7"] = calendar_128_7
    calendar_128_7.set_pos(5, 170)
    calendar_128_7.set_size(251, 84)
    calendar_128_7.set_today_date(2026, 10, 28)
    calendar_128_7.set_month_shown(2026, 10)
    calendar_128_7_header = calendar_128_7.add_header_arrow()
    calendar_128_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_128_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_128_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_128_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_128_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_128_get_current_page():
    return current_screen

def random_128_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_128_load_page(0)
