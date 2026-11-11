"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 68
Generated: 2023-11-14T22:15:00.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_68_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # imagebutton: imagebutton_68_0
    imagebutton_68_0 = lv.imagebutton(parent)
    objects["imagebutton_68_0"] = imagebutton_68_0
    imagebutton_68_0.set_pos(283, 345)
    imagebutton_68_0.set_size(72, 134)
    imagebutton_68_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_68_0.set_style_radius(5, lv.PART.MAIN)
    imagebutton_68_0_label = lv.label(imagebutton_68_0)
    imagebutton_68_0_label.set_text("Testo 68:0 \" \\ Città")
    imagebutton_68_0_label.center()
    imagebutton_68_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_68_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # win: win_68_1
    win_68_1 = lv.obj(parent)
    objects["win_68_1"] = win_68_1
    win_68_1.set_pos(677, 60)
    win_68_1.set_size(119, 111)
    win_68_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_68_1.set_style_pad_all(0, lv.PART.MAIN)
    win_68_1.set_style_pad_row(0, lv.PART.MAIN)
    win_68_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_68_1_header = lv.obj(win_68_1)
    win_68_1_header.set_size(lv.pct(100), 40)
    win_68_1_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_68_1_header.set_style_radius(0, lv.PART.MAIN)
    win_68_1_title = lv.label(win_68_1_header)
    win_68_1_title.set_text("Window Title")
    win_68_1_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_68_1_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_68_1_content = lv.obj(win_68_1)
    win_68_1_content.set_width(lv.pct(100))
    win_68_1_content.set_flex_grow(1)


def random_68_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_68_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_68_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_68_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_68_get_current_page():
    return current_screen

def random_68_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_68_load_page(0)
