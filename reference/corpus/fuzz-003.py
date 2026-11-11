"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 3
Generated: 2023-11-14T22:13:55.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_3_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: win_3_0
    win_3_0 = lv.obj(parent)
    objects["win_3_0"] = win_3_0
    win_3_0.set_pos(51, 213)
    win_3_0.set_size(111, 62)
    win_3_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_3_0.set_style_pad_all(0, lv.PART.MAIN)
    win_3_0.set_style_pad_row(0, lv.PART.MAIN)
    win_3_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_3_0_header = lv.obj(win_3_0)
    win_3_0_header.set_size(lv.pct(100), 40)
    win_3_0_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_3_0_header.set_style_radius(0, lv.PART.MAIN)
    win_3_0_title = lv.label(win_3_0_header)
    win_3_0_title.set_text("Window Title")
    win_3_0_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_3_0_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_3_0_content = lv.obj(win_3_0)
    win_3_0_content.set_width(lv.pct(100))
    win_3_0_content.set_flex_grow(1)

    # scale: scale_3_1
    scale_3_1 = lv.scale(parent)
    objects["scale_3_1"] = scale_3_1
    scale_3_1.set_pos(3, 83)
    scale_3_1.set_size(46, 45)
    scale_3_1.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_3_1.set_range(0, 100)
    scale_3_1.set_total_tick_count(51)
    scale_3_1.set_major_tick_every(5)
    scale_3_1.set_style_length(15, lv.PART.INDICATOR)
    scale_3_1.set_style_length(8, lv.PART.ITEMS)
    scale_3_1.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_3_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # button: button_3_2
    button_3_2 = lv.button(parent)
    objects["button_3_2"] = button_3_2
    button_3_2.set_pos(512, 315)
    button_3_2.set_size(117, 154)
    button_3_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_3_2.set_style_radius(5, lv.PART.MAIN)
    button_3_2_label = lv.label(button_3_2)
    button_3_2_label.set_text("Testo 3:2 \" \\ Città")
    button_3_2_label.center()
    button_3_2_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_3_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # panel: panel_3_3
    panel_3_3 = lv.obj(parent)
    objects["panel_3_3"] = panel_3_3
    panel_3_3.set_pos(299, 91)
    panel_3_3.set_size(268, 92)
    panel_3_3.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_3_3.set_style_border_width(2, lv.PART.MAIN)
    panel_3_3.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_3_3.set_style_radius(5, lv.PART.MAIN)
    panel_3_3.set_style_pad_all(0, lv.PART.MAIN)
    panel_3_3.set_style_pad_gap(0, lv.PART.MAIN)

    # image: image_3_4
    image_3_4 = lv.image(parent)
    objects["image_3_4"] = image_3_4
    image_3_4.set_pos(447, 172)
    image_3_4.set_size(104, 41)


def random_3_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_3_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_3_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_3_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_3_get_current_page():
    return current_screen

def random_3_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_3_load_page(0)
