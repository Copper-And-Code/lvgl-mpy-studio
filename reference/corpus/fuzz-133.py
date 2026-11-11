"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 133
Generated: 2023-11-14T22:16:05.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_133_0_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_133_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # slider: slider_133_0
    slider_133_0 = lv.slider(parent)
    objects["slider_133_0"] = slider_133_0
    slider_133_0.set_pos(690, 297)
    slider_133_0.set_size(97, 65)
    slider_133_0.set_range(0, 100)
    slider_133_0.set_value(50, False)
    slider_133_0.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_133_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_133_0.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_133_0.add_event_cb(slider_133_0_changed, lv.EVENT.VALUE_CHANGED, None)

    # imagebutton: imagebutton_133_1
    imagebutton_133_1 = lv.imagebutton(parent)
    objects["imagebutton_133_1"] = imagebutton_133_1
    imagebutton_133_1.set_pos(81, 339)
    imagebutton_133_1.set_size(102, 46)
    imagebutton_133_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_133_1.set_style_radius(5, lv.PART.MAIN)
    imagebutton_133_1_label = lv.label(imagebutton_133_1)
    imagebutton_133_1_label.set_text("Testo 133:1 \" \\ Città")
    imagebutton_133_1_label.center()
    imagebutton_133_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_133_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # msgbox: msgbox_133_2
    msgbox_133_2 = lv.msgbox(parent)
    objects["msgbox_133_2"] = msgbox_133_2
    msgbox_133_2.set_pos(667, 79)
    msgbox_133_2.set_size(72, 37)
    msgbox_133_2_title = msgbox_133_2.add_title("Notice")
    msgbox_133_2_text = msgbox_133_2.add_text("Testo 133:2 \" \\ Città")
    msgbox_133_2_button_1 = msgbox_133_2.add_footer_button("OK")
    msgbox_133_2_button_2 = msgbox_133_2.add_footer_button("Cancel")
    msgbox_133_2_close = msgbox_133_2.add_close_button()
    msgbox_133_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # led: led_133_3
    led_133_3 = lv.led(parent)
    objects["led_133_3"] = led_133_3
    led_133_3.set_pos(151, 349)
    led_133_3.set_size(200, 157)
    led_133_3.set_color(lv.color_hex(0xFF0000))
    led_133_3.set_brightness(255)


def random_133_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_133_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_133_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_133_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_133_get_current_page():
    return current_screen

def random_133_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_133_load_page(0)
