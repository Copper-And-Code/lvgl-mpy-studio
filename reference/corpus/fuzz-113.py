"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 113
Generated: 2023-11-14T22:15:45.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_113_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # msgbox: msgbox_113_0
    msgbox_113_0 = lv.msgbox(parent)
    objects["msgbox_113_0"] = msgbox_113_0
    msgbox_113_0.set_pos(639, 135)
    msgbox_113_0.set_size(254, 126)
    msgbox_113_0_title = msgbox_113_0.add_title("Notice")
    msgbox_113_0_text = msgbox_113_0.add_text("Testo 113:0 \" \\ Città")
    msgbox_113_0_button_1 = msgbox_113_0.add_footer_button("OK")
    msgbox_113_0_button_2 = msgbox_113_0.add_footer_button("Cancel")
    msgbox_113_0_close = msgbox_113_0.add_close_button()
    msgbox_113_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # switch: switch_113_1
    switch_113_1 = lv.switch(parent)
    objects["switch_113_1"] = switch_113_1
    switch_113_1.set_pos(250, 191)
    switch_113_1.set_size(85, 73)
    switch_113_1.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_113_1.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_113_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # tileview: tileview_113_2
    tileview_113_2 = lv.tileview(parent)
    objects["tileview_113_2"] = tileview_113_2
    tileview_113_2.set_pos(690, 381)
    tileview_113_2.set_size(69, 95)
    tileview_113_2.add_tile(0, 0, lv.DIR.ALL)
    tileview_113_2.add_tile(1, 0, lv.DIR.ALL)
    tileview_113_2.add_tile(0, 1, lv.DIR.ALL)
    tileview_113_2.add_tile(1, 1, lv.DIR.ALL)
    tileview_113_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # panel: panel_113_3
    panel_113_3 = lv.obj(parent)
    objects["panel_113_3"] = panel_113_3
    panel_113_3.set_pos(252, 263)
    panel_113_3.set_size(115, 28)
    panel_113_3.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_113_3.set_style_border_width(2, lv.PART.MAIN)
    panel_113_3.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_113_3.set_style_radius(5, lv.PART.MAIN)
    panel_113_3.set_style_pad_all(0, lv.PART.MAIN)
    panel_113_3.set_style_pad_gap(0, lv.PART.MAIN)

    # keyboard: keyboard_113_4
    keyboard_113_4 = lv.keyboard(parent)
    objects["keyboard_113_4"] = keyboard_113_4
    keyboard_113_4.set_pos(49, 184)
    keyboard_113_4.set_size(128, 58)

    # keyboard: keyboard_113_5
    keyboard_113_5 = lv.keyboard(parent)
    objects["keyboard_113_5"] = keyboard_113_5
    keyboard_113_5.set_pos(670, 206)
    keyboard_113_5.set_size(191, 53)


def random_113_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_113_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_113_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_113_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_113_get_current_page():
    return current_screen

def random_113_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_113_load_page(0)
