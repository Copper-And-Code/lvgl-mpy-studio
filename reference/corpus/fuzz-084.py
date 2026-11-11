"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 84
Generated: 2023-11-14T22:15:16.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def textarea_84_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_84_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # keyboard: keyboard_84_0
    keyboard_84_0 = lv.keyboard(parent)
    objects["keyboard_84_0"] = keyboard_84_0
    keyboard_84_0.set_pos(414, 365)
    keyboard_84_0.set_size(202, 82)

    # textarea: textarea_84_1
    textarea_84_1 = lv.textarea(parent)
    objects["textarea_84_1"] = textarea_84_1
    textarea_84_1.set_pos(695, 195)
    textarea_84_1.set_size(210, 65)
    textarea_84_1.set_text("Testo 84:1 \" \\ Città")
    textarea_84_1.set_placeholder_text("Type here")
    textarea_84_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_84_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_84_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    textarea_84_1.add_event_cb(textarea_84_1_changed, lv.EVENT.VALUE_CHANGED, None)


def random_84_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_84_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_84_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_84_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_84_get_current_page():
    return current_screen

def random_84_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_84_load_page(0)
