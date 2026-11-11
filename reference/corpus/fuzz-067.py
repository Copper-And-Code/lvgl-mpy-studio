"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 67
Generated: 2023-11-14T22:14:59.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_67_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: win_67_0
    win_67_0 = lv.obj(parent)
    objects["win_67_0"] = win_67_0
    win_67_0.set_pos(285, 202)
    win_67_0.set_size(41, 34)
    win_67_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_67_0.set_style_pad_all(0, lv.PART.MAIN)
    win_67_0.set_style_pad_row(0, lv.PART.MAIN)
    win_67_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_67_0_header = lv.obj(win_67_0)
    win_67_0_header.set_size(lv.pct(100), 40)
    win_67_0_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_67_0_header.set_style_radius(0, lv.PART.MAIN)
    win_67_0_title = lv.label(win_67_0_header)
    win_67_0_title.set_text("Window Title")
    win_67_0_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_67_0_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_67_0_content = lv.obj(win_67_0)
    win_67_0_content.set_width(lv.pct(100))
    win_67_0_content.set_flex_grow(1)

    # led: led_67_1
    led_67_1 = lv.led(parent)
    objects["led_67_1"] = led_67_1
    led_67_1.set_pos(220, 160)
    led_67_1.set_size(222, 74)
    led_67_1.set_color(lv.color_hex(0xFF0000))
    led_67_1.set_brightness(255)

    # scale: scale_67_2
    scale_67_2 = lv.scale(parent)
    objects["scale_67_2"] = scale_67_2
    scale_67_2.set_pos(694, 397)
    scale_67_2.set_size(183, 33)
    scale_67_2.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_67_2.set_range(0, 100)
    scale_67_2.set_total_tick_count(51)
    scale_67_2.set_major_tick_every(5)
    scale_67_2.set_style_length(15, lv.PART.INDICATOR)
    scale_67_2.set_style_length(8, lv.PART.ITEMS)
    scale_67_2.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_67_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # buttonmatrix: buttonmatrix_67_3
    buttonmatrix_67_3 = lv.buttonmatrix(parent)
    objects["buttonmatrix_67_3"] = buttonmatrix_67_3
    buttonmatrix_67_3.set_pos(353, 134)
    buttonmatrix_67_3.set_size(114, 146)
    buttonmatrix_67_3_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_67_3.set_map(buttonmatrix_67_3_map)
    buttonmatrix_67_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_67_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_67_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_67_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # tileview: tileview_67_4
    tileview_67_4 = lv.tileview(parent)
    objects["tileview_67_4"] = tileview_67_4
    tileview_67_4.set_pos(331, 390)
    tileview_67_4.set_size(240, 111)
    tileview_67_4.add_tile(0, 0, lv.DIR.ALL)
    tileview_67_4.add_tile(1, 0, lv.DIR.ALL)
    tileview_67_4.add_tile(0, 1, lv.DIR.ALL)
    tileview_67_4.add_tile(1, 1, lv.DIR.ALL)
    tileview_67_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_67_5
    buttonmatrix_67_5 = lv.buttonmatrix(parent)
    objects["buttonmatrix_67_5"] = buttonmatrix_67_5
    buttonmatrix_67_5.set_pos(298, 109)
    buttonmatrix_67_5.set_size(60, 140)
    buttonmatrix_67_5_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_67_5.set_map(buttonmatrix_67_5_map)
    buttonmatrix_67_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_67_5.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_67_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_67_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_67_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_67_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_67_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_67_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_67_get_current_page():
    return current_screen

def random_67_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_67_load_page(0)
