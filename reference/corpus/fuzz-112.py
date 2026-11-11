"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 112
Generated: 2023-11-14T22:15:44.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_112_2_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_112_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # arc: arc_112_0
    arc_112_0 = lv.arc(parent)
    objects["arc_112_0"] = arc_112_0
    arc_112_0.set_pos(595, 158)
    arc_112_0.set_size(35, 148)
    arc_112_0.set_bg_angles(135, 45)
    arc_112_0.set_range(0, 100)
    arc_112_0.set_value(50)
    arc_112_0.set_style_arc_width(10, lv.PART.MAIN)
    arc_112_0.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_112_0.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_112_0.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_112_0.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # dropdown: dropdown_112_1
    dropdown_112_1 = lv.dropdown(parent)
    objects["dropdown_112_1"] = dropdown_112_1
    dropdown_112_1.set_pos(113, 144)
    dropdown_112_1.set_size(152, 27)
    dropdown_112_1.set_options("Option 1\nOption 2\nOption 3")
    dropdown_112_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_112_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_112_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # slider: slider_112_2
    slider_112_2 = lv.slider(parent)
    objects["slider_112_2"] = slider_112_2
    slider_112_2.set_pos(573, 375)
    slider_112_2.set_size(161, 74)
    slider_112_2.set_range(0, 100)
    slider_112_2.set_value(50, False)
    slider_112_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_112_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_112_2.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_112_2.add_event_cb(slider_112_2_changed, lv.EVENT.VALUE_CHANGED, None)


def random_112_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_112_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_112_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_112_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_112_get_current_page():
    return current_screen

def random_112_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_112_load_page(0)
