"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 150
Generated: 2023-11-14T22:16:22.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def checkbox_150_0_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_150_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # checkbox: checkbox_150_0
    checkbox_150_0 = lv.checkbox(parent)
    objects["checkbox_150_0"] = checkbox_150_0
    checkbox_150_0.set_pos(594, 350)
    checkbox_150_0.set_text("Testo 150:0 \" \\ Città")
    checkbox_150_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_150_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_150_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_150_0.add_event_cb(checkbox_150_0_changed, lv.EVENT.VALUE_CHANGED, None)

    # dropdown: dropdown_150_1
    dropdown_150_1 = lv.dropdown(parent)
    objects["dropdown_150_1"] = dropdown_150_1
    dropdown_150_1.set_pos(653, 104)
    dropdown_150_1.set_size(257, 139)
    dropdown_150_1.set_options("Option 1\nOption 2\nOption 3")
    dropdown_150_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_150_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_150_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # tileview: tileview_150_2
    tileview_150_2 = lv.tileview(parent)
    objects["tileview_150_2"] = tileview_150_2
    tileview_150_2.set_pos(175, 297)
    tileview_150_2.set_size(117, 76)
    tileview_150_2.add_tile(0, 0, lv.DIR.ALL)
    tileview_150_2.add_tile(1, 0, lv.DIR.ALL)
    tileview_150_2.add_tile(0, 1, lv.DIR.ALL)
    tileview_150_2.add_tile(1, 1, lv.DIR.ALL)
    tileview_150_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_150_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_150_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_150_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_150_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_150_get_current_page():
    return current_screen

def random_150_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_150_load_page(0)
