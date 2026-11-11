"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 2
Generated: 2023-11-14T22:13:54.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def checkbox_2_0_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

def button_2_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_2_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # checkbox: checkbox_2_0
    checkbox_2_0 = lv.checkbox(parent)
    objects["checkbox_2_0"] = checkbox_2_0
    checkbox_2_0.set_pos(683, 177)
    checkbox_2_0.set_text("Testo 2:0 \" \\ Città")
    checkbox_2_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_2_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_2_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_2_0.add_event_cb(checkbox_2_0_changed, lv.EVENT.VALUE_CHANGED, None)

    # button: button_2_1
    button_2_1 = lv.button(parent)
    objects["button_2_1"] = button_2_1
    button_2_1.set_pos(380, 196)
    button_2_1.set_size(219, 54)
    button_2_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_2_1.set_style_radius(5, lv.PART.MAIN)
    button_2_1_label = lv.label(button_2_1)
    button_2_1_label.set_text("Testo 2:1 \" \\ Città")
    button_2_1_label.center()
    button_2_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_2_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_2_1.add_event_cb(button_2_1_changed, lv.EVENT.CLICKED, None)

    # led: led_2_2
    led_2_2 = lv.led(parent)
    objects["led_2_2"] = led_2_2
    led_2_2.set_pos(146, 86)
    led_2_2.set_size(195, 157)
    led_2_2.set_color(lv.color_hex(0xFF0000))
    led_2_2.set_brightness(255)


def random_2_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_2_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_2_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_2_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_2_get_current_page():
    return current_screen

def random_2_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_2_load_page(0)
