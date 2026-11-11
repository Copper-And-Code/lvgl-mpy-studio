"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 75
Generated: 2023-11-14T22:15:07.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_75_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_75_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: win_75_0
    win_75_0 = lv.obj(parent)
    objects["win_75_0"] = win_75_0
    win_75_0.set_pos(56, 64)
    win_75_0.set_size(114, 44)
    win_75_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_75_0.set_style_pad_all(0, lv.PART.MAIN)
    win_75_0.set_style_pad_row(0, lv.PART.MAIN)
    win_75_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_75_0_header = lv.obj(win_75_0)
    win_75_0_header.set_size(lv.pct(100), 40)
    win_75_0_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_75_0_header.set_style_radius(0, lv.PART.MAIN)
    win_75_0_title = lv.label(win_75_0_header)
    win_75_0_title.set_text("Window Title")
    win_75_0_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_75_0_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_75_0_content = lv.obj(win_75_0)
    win_75_0_content.set_width(lv.pct(100))
    win_75_0_content.set_flex_grow(1)

    # slider: slider_75_1
    slider_75_1 = lv.slider(parent)
    objects["slider_75_1"] = slider_75_1
    slider_75_1.set_pos(635, 204)
    slider_75_1.set_size(257, 50)
    slider_75_1.set_range(0, 100)
    slider_75_1.set_value(50, False)
    slider_75_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_75_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_75_1.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_75_1.add_event_cb(slider_75_1_changed, lv.EVENT.VALUE_CHANGED, None)

    # bar: bar_75_2
    bar_75_2 = lv.bar(parent)
    objects["bar_75_2"] = bar_75_2
    bar_75_2.set_pos(522, 120)
    bar_75_2.set_size(61, 67)
    bar_75_2.set_range(0, 100)
    bar_75_2.set_value(50, False)
    bar_75_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_75_2.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)


def random_75_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_75_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_75_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_75_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_75_get_current_page():
    return current_screen

def random_75_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_75_load_page(0)
