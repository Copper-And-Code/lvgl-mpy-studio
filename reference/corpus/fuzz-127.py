"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 127
Generated: 2023-11-14T22:15:59.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_127_0_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_127_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # slider: slider_127_0
    slider_127_0 = lv.slider(parent)
    objects["slider_127_0"] = slider_127_0
    slider_127_0.set_pos(51, 125)
    slider_127_0.set_size(119, 150)
    slider_127_0.set_range(0, 100)
    slider_127_0.set_value(50, False)
    slider_127_0.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_127_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_127_0.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_127_0.add_event_cb(slider_127_0_changed, lv.EVENT.VALUE_CHANGED, None)

    # calendar: calendar_127_1
    calendar_127_1 = lv.calendar(parent)
    objects["calendar_127_1"] = calendar_127_1
    calendar_127_1.set_pos(556, 242)
    calendar_127_1.set_size(87, 158)
    calendar_127_1.set_today_date(2026, 10, 28)
    calendar_127_1.set_month_shown(2026, 10)
    calendar_127_1_header = calendar_127_1.add_header_arrow()
    calendar_127_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # win: win_127_2
    win_127_2 = lv.obj(parent)
    objects["win_127_2"] = win_127_2
    win_127_2.set_pos(65, 222)
    win_127_2.set_size(31, 74)
    win_127_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_127_2.set_style_pad_all(0, lv.PART.MAIN)
    win_127_2.set_style_pad_row(0, lv.PART.MAIN)
    win_127_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_127_2_header = lv.obj(win_127_2)
    win_127_2_header.set_size(lv.pct(100), 40)
    win_127_2_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_127_2_header.set_style_radius(0, lv.PART.MAIN)
    win_127_2_title = lv.label(win_127_2_header)
    win_127_2_title.set_text("Window Title")
    win_127_2_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_127_2_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_127_2_content = lv.obj(win_127_2)
    win_127_2_content.set_width(lv.pct(100))
    win_127_2_content.set_flex_grow(1)

    # tileview: tileview_127_3
    tileview_127_3 = lv.tileview(parent)
    objects["tileview_127_3"] = tileview_127_3
    tileview_127_3.set_pos(132, 158)
    tileview_127_3.set_size(257, 62)
    tileview_127_3.add_tile(0, 0, lv.DIR.ALL)
    tileview_127_3.add_tile(1, 0, lv.DIR.ALL)
    tileview_127_3.add_tile(0, 1, lv.DIR.ALL)
    tileview_127_3.add_tile(1, 1, lv.DIR.ALL)
    tileview_127_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # textarea: textarea_127_4
    textarea_127_4 = lv.textarea(parent)
    objects["textarea_127_4"] = textarea_127_4
    textarea_127_4.set_pos(282, 290)
    textarea_127_4.set_size(203, 106)
    textarea_127_4.set_text("Testo 127:4 \" \\ Città")
    textarea_127_4.set_placeholder_text("Type here")
    textarea_127_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_127_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_127_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # keyboard: keyboard_127_5
    keyboard_127_5 = lv.keyboard(parent)
    objects["keyboard_127_5"] = keyboard_127_5
    keyboard_127_5.set_pos(691, 123)
    keyboard_127_5.set_size(260, 92)

    # button: button_127_6
    button_127_6 = lv.button(parent)
    objects["button_127_6"] = button_127_6
    button_127_6.set_pos(577, 342)
    button_127_6.set_size(253, 20)
    button_127_6.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_127_6.set_style_radius(5, lv.PART.MAIN)
    button_127_6_label = lv.label(button_127_6)
    button_127_6_label.set_text("Testo 127:6 \" \\ Città")
    button_127_6_label.center()
    button_127_6_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_127_6_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # arc: arc_127_7
    arc_127_7 = lv.arc(parent)
    objects["arc_127_7"] = arc_127_7
    arc_127_7.set_pos(92, 257)
    arc_127_7.set_size(246, 64)
    arc_127_7.set_bg_angles(135, 45)
    arc_127_7.set_range(0, 100)
    arc_127_7.set_value(50)
    arc_127_7.set_style_arc_width(10, lv.PART.MAIN)
    arc_127_7.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_127_7.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_127_7.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_127_7.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)


def random_127_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_127_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_127_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_127_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_127_get_current_page():
    return current_screen

def random_127_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_127_load_page(0)
