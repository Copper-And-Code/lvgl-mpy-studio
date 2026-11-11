"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 134
Generated: 2023-11-14T22:16:06.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_134_6_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_134_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # arc: arc_134_0
    arc_134_0 = lv.arc(parent)
    objects["arc_134_0"] = arc_134_0
    arc_134_0.set_pos(484, 68)
    arc_134_0.set_size(236, 54)
    arc_134_0.set_bg_angles(135, 45)
    arc_134_0.set_range(0, 100)
    arc_134_0.set_value(50)
    arc_134_0.set_style_arc_width(10, lv.PART.MAIN)
    arc_134_0.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_134_0.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_134_0.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_134_0.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # tabview: tabview_134_1
    tabview_134_1 = lv.tabview(parent)
    objects["tabview_134_1"] = tabview_134_1
    tabview_134_1.set_pos(565, 232)
    tabview_134_1.set_size(142, 28)
    tabview_134_1.set_tab_bar_position(lv.DIR.TOP)
    tabview_134_1.set_tab_bar_size(40)
    tabview_134_1_tab_1 = tabview_134_1.add_tab("Tab 1")
    tabview_134_1_tab_2 = tabview_134_1.add_tab("Tab 2")
    tabview_134_1_tab_3 = tabview_134_1.add_tab("Tab 3")
    tabview_134_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # win: win_134_2
    win_134_2 = lv.obj(parent)
    objects["win_134_2"] = win_134_2
    win_134_2.set_pos(342, 119)
    win_134_2.set_size(119, 16)
    win_134_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_134_2.set_style_pad_all(0, lv.PART.MAIN)
    win_134_2.set_style_pad_row(0, lv.PART.MAIN)
    win_134_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_134_2_header = lv.obj(win_134_2)
    win_134_2_header.set_size(lv.pct(100), 40)
    win_134_2_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_134_2_header.set_style_radius(0, lv.PART.MAIN)
    win_134_2_title = lv.label(win_134_2_header)
    win_134_2_title.set_text("Window Title")
    win_134_2_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_134_2_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_134_2_content = lv.obj(win_134_2)
    win_134_2_content.set_width(lv.pct(100))
    win_134_2_content.set_flex_grow(1)

    # line: line_134_3
    line_134_3 = lv.line(parent)
    objects["line_134_3"] = line_134_3
    line_134_3.set_pos(100, 299)
    line_134_3_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_134_3.set_points(line_134_3_points, 2)
    line_134_3.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_134_3.set_style_line_width(2, lv.PART.MAIN)

    # arc: arc_134_4
    arc_134_4 = lv.arc(parent)
    objects["arc_134_4"] = arc_134_4
    arc_134_4.set_pos(263, 102)
    arc_134_4.set_size(260, 111)
    arc_134_4.set_bg_angles(135, 45)
    arc_134_4.set_range(0, 100)
    arc_134_4.set_value(50)
    arc_134_4.set_style_arc_width(10, lv.PART.MAIN)
    arc_134_4.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_134_4.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_134_4.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_134_4.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # spinbox: spinbox_134_5
    spinbox_134_5 = lv.spinbox(parent)
    objects["spinbox_134_5"] = spinbox_134_5
    spinbox_134_5.set_pos(146, 115)
    spinbox_134_5.set_size(113, 13)
    spinbox_134_5.set_digit_format(4, 0)
    spinbox_134_5.set_range(0, 999)
    spinbox_134_5.set_value(0)
    spinbox_134_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_134_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_134_5.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # button: button_134_6
    button_134_6 = lv.button(parent)
    objects["button_134_6"] = button_134_6
    button_134_6.set_pos(133, 82)
    button_134_6.set_size(233, 120)
    button_134_6.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_134_6.set_style_radius(5, lv.PART.MAIN)
    button_134_6_label = lv.label(button_134_6)
    button_134_6_label.set_text("Testo 134:6 \" \\ Città")
    button_134_6_label.center()
    button_134_6_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_134_6_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_134_6.add_event_cb(button_134_6_changed, lv.EVENT.CLICKED, None)


def random_134_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_134_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_134_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_134_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_134_get_current_page():
    return current_screen

def random_134_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_134_load_page(0)
