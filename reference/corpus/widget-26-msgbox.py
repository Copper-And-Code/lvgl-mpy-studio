"""
Auto-generated LVGL UI Code for MicroPython
Project: One msgbox
Generated: 2023-11-14T22:13:45.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_msgbox_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # msgbox: Message Box_w25
    message_box_w25 = lv.msgbox(parent)
    objects["message_box_w25"] = message_box_w25
    message_box_w25.set_pos(95, 80)
    message_box_w25.set_size(250, 180)
    message_box_w25_title = message_box_w25.add_title("Notice")
    message_box_w25_text = message_box_w25.add_text("This is a message box")
    message_box_w25_button_1 = message_box_w25.add_footer_button("OK")
    message_box_w25_button_2 = message_box_w25.add_footer_button("Cancel")
    message_box_w25_close = message_box_w25.add_close_button()
    message_box_w25.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def one_msgbox_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_msgbox_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_msgbox_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_msgbox_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_msgbox_get_current_page():
    return current_screen

def one_msgbox_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_msgbox_load_page(0)
