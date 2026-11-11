"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 181
Generated: 2023-11-14T22:16:53.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_181_4_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_181_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # line: line_181_0
    line_181_0 = lv.line(parent)
    objects["line_181_0"] = line_181_0
    line_181_0.set_pos(213, 377)
    line_181_0_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_181_0.set_points(line_181_0_points, 2)
    line_181_0.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_181_0.set_style_line_width(2, lv.PART.MAIN)

    # calendar: calendar_181_1
    calendar_181_1 = lv.calendar(parent)
    objects["calendar_181_1"] = calendar_181_1
    calendar_181_1.set_pos(679, 14)
    calendar_181_1.set_size(268, 140)
    calendar_181_1.set_today_date(2026, 10, 28)
    calendar_181_1.set_month_shown(2026, 10)
    calendar_181_1_header = calendar_181_1.add_header_arrow()
    calendar_181_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # dropdown: dropdown_181_2
    dropdown_181_2 = lv.dropdown(parent)
    objects["dropdown_181_2"] = dropdown_181_2
    dropdown_181_2.set_pos(526, 382)
    dropdown_181_2.set_size(90, 18)
    dropdown_181_2.set_options("Option 1\nOption 2\nOption 3")
    dropdown_181_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_181_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_181_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # win: win_181_3
    win_181_3 = lv.obj(parent)
    objects["win_181_3"] = win_181_3
    win_181_3.set_pos(549, 253)
    win_181_3.set_size(204, 53)
    win_181_3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_181_3.set_style_pad_all(0, lv.PART.MAIN)
    win_181_3.set_style_pad_row(0, lv.PART.MAIN)
    win_181_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_181_3_header = lv.obj(win_181_3)
    win_181_3_header.set_size(lv.pct(100), 40)
    win_181_3_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_181_3_header.set_style_radius(0, lv.PART.MAIN)
    win_181_3_title = lv.label(win_181_3_header)
    win_181_3_title.set_text("Window Title")
    win_181_3_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_181_3_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_181_3_content = lv.obj(win_181_3)
    win_181_3_content.set_width(lv.pct(100))
    win_181_3_content.set_flex_grow(1)

    # slider: slider_181_4
    slider_181_4 = lv.slider(parent)
    objects["slider_181_4"] = slider_181_4
    slider_181_4.set_pos(348, 369)
    slider_181_4.set_size(163, 45)
    slider_181_4.set_range(0, 100)
    slider_181_4.set_value(50, False)
    slider_181_4.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_181_4.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_181_4.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_181_4.add_event_cb(slider_181_4_changed, lv.EVENT.VALUE_CHANGED, None)

    # scale: scale_181_5
    scale_181_5 = lv.scale(parent)
    objects["scale_181_5"] = scale_181_5
    scale_181_5.set_pos(221, 114)
    scale_181_5.set_size(55, 113)
    scale_181_5.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_181_5.set_range(0, 100)
    scale_181_5.set_total_tick_count(51)
    scale_181_5.set_major_tick_every(5)
    scale_181_5.set_style_length(15, lv.PART.INDICATOR)
    scale_181_5.set_style_length(8, lv.PART.ITEMS)
    scale_181_5.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_181_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # spinbox: spinbox_181_6
    spinbox_181_6 = lv.spinbox(parent)
    objects["spinbox_181_6"] = spinbox_181_6
    spinbox_181_6.set_pos(389, 13)
    spinbox_181_6.set_size(150, 16)
    spinbox_181_6.set_digit_format(4, 0)
    spinbox_181_6.set_range(0, 999)
    spinbox_181_6.set_value(0)
    spinbox_181_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_181_6.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_181_6.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # spinbox: spinbox_181_7
    spinbox_181_7 = lv.spinbox(parent)
    objects["spinbox_181_7"] = spinbox_181_7
    spinbox_181_7.set_pos(484, 23)
    spinbox_181_7.set_size(50, 17)
    spinbox_181_7.set_digit_format(4, 0)
    spinbox_181_7.set_range(0, 999)
    spinbox_181_7.set_value(0)
    spinbox_181_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_181_7.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_181_7.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_181_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_181_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_181_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_181_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_181_get_current_page():
    return current_screen

def random_181_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_181_load_page(0)
