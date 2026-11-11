"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 161
Generated: 2023-11-14T22:16:33.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def checkbox_161_3_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_161_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # panel: panel_161_0
    panel_161_0 = lv.obj(parent)
    objects["panel_161_0"] = panel_161_0
    panel_161_0.set_pos(181, 33)
    panel_161_0.set_size(156, 96)
    panel_161_0.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_161_0.set_style_border_width(2, lv.PART.MAIN)
    panel_161_0.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_161_0.set_style_radius(5, lv.PART.MAIN)
    panel_161_0.set_style_pad_all(0, lv.PART.MAIN)
    panel_161_0.set_style_pad_gap(0, lv.PART.MAIN)

    # spinner: spinner_161_1
    spinner_161_1 = lv.arc(parent)
    objects["spinner_161_1"] = spinner_161_1
    spinner_161_1.set_pos(242, 105)
    spinner_161_1.set_size(79, 14)
    spinner_161_1.set_bg_angles(0, 360)
    spinner_161_1.set_angles(0, 60)
    spinner_161_1.remove_style(None, lv.PART.KNOB)
    spinner_161_1.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_161_1_anim = lv.anim_t()
    spinner_161_1_anim.init()
    spinner_161_1_anim.set_var(spinner_161_1)
    spinner_161_1_anim.set_values(0, 360)
    spinner_161_1_anim.set_duration(1000)
    spinner_161_1_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_161_1_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_161_1_anim.set_custom_exec_cb(lambda _anim, value: spinner_161_1.set_rotation(value))
    spinner_161_1_anim.start()
    spinner_161_1.set_style_arc_width(8, lv.PART.MAIN)
    spinner_161_1.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_161_1.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # calendar: calendar_161_2
    calendar_161_2 = lv.calendar(parent)
    objects["calendar_161_2"] = calendar_161_2
    calendar_161_2.set_pos(411, 102)
    calendar_161_2.set_size(109, 117)
    calendar_161_2.set_today_date(2026, 10, 28)
    calendar_161_2.set_month_shown(2026, 10)
    calendar_161_2_header = calendar_161_2.add_header_arrow()
    calendar_161_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # checkbox: checkbox_161_3
    checkbox_161_3 = lv.checkbox(parent)
    objects["checkbox_161_3"] = checkbox_161_3
    checkbox_161_3.set_pos(352, 210)
    checkbox_161_3.set_text("Testo 161:3 \" \\ Città")
    checkbox_161_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_161_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_161_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_161_3.add_event_cb(checkbox_161_3_changed, lv.EVENT.VALUE_CHANGED, None)

    # label: label_161_4
    label_161_4 = lv.label(parent)
    objects["label_161_4"] = label_161_4
    label_161_4.set_pos(266, 254)
    label_161_4.set_size(139, 20)
    label_161_4.set_text("Testo 161:4 \" \\ Città")
    label_161_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_161_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_161_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # label: label_161_5
    label_161_5 = lv.label(parent)
    objects["label_161_5"] = label_161_5
    label_161_5.set_pos(316, 122)
    label_161_5.set_size(146, 112)
    label_161_5.set_text("Testo 161:5 \" \\ Città")
    label_161_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_161_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_161_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # roller: roller_161_6
    roller_161_6 = lv.roller(parent)
    objects["roller_161_6"] = roller_161_6
    roller_161_6.set_pos(527, 220)
    roller_161_6.set_size(220, 46)
    roller_161_6.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_161_6.set_visible_row_count(3)
    roller_161_6.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_161_6.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_161_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_161_6.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_161_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_161_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_161_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_161_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_161_get_current_page():
    return current_screen

def random_161_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_161_load_page(0)
