"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 31
Generated: 2023-11-14T22:14:23.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_31_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # switch: switch_31_0
    switch_31_0 = lv.switch(parent)
    objects["switch_31_0"] = switch_31_0
    switch_31_0.set_pos(54, 336)
    switch_31_0.set_size(28, 44)
    switch_31_0.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_31_0.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_31_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # msgbox: msgbox_31_1
    msgbox_31_1 = lv.msgbox(parent)
    objects["msgbox_31_1"] = msgbox_31_1
    msgbox_31_1.set_pos(560, 139)
    msgbox_31_1.set_size(145, 124)
    msgbox_31_1_title = msgbox_31_1.add_title("Notice")
    msgbox_31_1_text = msgbox_31_1.add_text("Testo 31:1 \" \\ Città")
    msgbox_31_1_button_1 = msgbox_31_1.add_footer_button("OK")
    msgbox_31_1_button_2 = msgbox_31_1.add_footer_button("Cancel")
    msgbox_31_1_close = msgbox_31_1.add_close_button()
    msgbox_31_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_31_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_31_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_31_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_31_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_31_get_current_page():
    return current_screen

def random_31_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_31_load_page(0)
