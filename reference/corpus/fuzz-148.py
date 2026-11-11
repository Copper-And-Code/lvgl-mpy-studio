"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 148
Generated: 2023-11-14T22:16:20.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_148_2_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_148_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # win: win_148_0
    win_148_0 = lv.obj(parent)
    objects["win_148_0"] = win_148_0
    win_148_0.set_pos(84, 20)
    win_148_0.set_size(82, 132)
    win_148_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_148_0.set_style_pad_all(0, lv.PART.MAIN)
    win_148_0.set_style_pad_row(0, lv.PART.MAIN)
    win_148_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_148_0_header = lv.obj(win_148_0)
    win_148_0_header.set_size(lv.pct(100), 40)
    win_148_0_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_148_0_header.set_style_radius(0, lv.PART.MAIN)
    win_148_0_title = lv.label(win_148_0_header)
    win_148_0_title.set_text("Window Title")
    win_148_0_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_148_0_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_148_0_content = lv.obj(win_148_0)
    win_148_0_content.set_width(lv.pct(100))
    win_148_0_content.set_flex_grow(1)

    # panel: panel_148_1
    panel_148_1 = lv.obj(parent)
    objects["panel_148_1"] = panel_148_1
    panel_148_1.set_pos(439, 97)
    panel_148_1.set_size(236, 59)
    panel_148_1.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_148_1.set_style_border_width(2, lv.PART.MAIN)
    panel_148_1.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_148_1.set_style_radius(5, lv.PART.MAIN)
    panel_148_1.set_style_pad_all(0, lv.PART.MAIN)
    panel_148_1.set_style_pad_gap(0, lv.PART.MAIN)

    # slider: slider_148_2
    slider_148_2 = lv.slider(parent)
    objects["slider_148_2"] = slider_148_2
    slider_148_2.set_pos(75, 56)
    slider_148_2.set_size(109, 102)
    slider_148_2.set_range(0, 100)
    slider_148_2.set_value(50, False)
    slider_148_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_148_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_148_2.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_148_2.add_event_cb(slider_148_2_changed, lv.EVENT.VALUE_CHANGED, None)

    # slider: slider_148_3
    slider_148_3 = lv.slider(parent)
    objects["slider_148_3"] = slider_148_3
    slider_148_3.set_pos(483, 35)
    slider_148_3.set_size(88, 39)
    slider_148_3.set_range(0, 100)
    slider_148_3.set_value(50, False)
    slider_148_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_148_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_148_3.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)


def random_148_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_148_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_148_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_148_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_148_get_current_page():
    return current_screen

def random_148_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_148_load_page(0)
