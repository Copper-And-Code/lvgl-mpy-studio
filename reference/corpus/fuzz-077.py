"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 77
Generated: 2023-11-14T22:15:09.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_77_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # led: led_77_0
    led_77_0 = lv.led(parent)
    objects["led_77_0"] = led_77_0
    led_77_0.set_pos(429, 287)
    led_77_0.set_size(102, 50)
    led_77_0.set_color(lv.color_hex(0xFF0000))
    led_77_0.set_brightness(255)

    # dropdown: dropdown_77_1
    dropdown_77_1 = lv.dropdown(parent)
    objects["dropdown_77_1"] = dropdown_77_1
    dropdown_77_1.set_pos(689, 318)
    dropdown_77_1.set_size(40, 98)
    dropdown_77_1.set_options("Option 1\nOption 2\nOption 3")
    dropdown_77_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_77_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_77_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # msgbox: msgbox_77_2
    msgbox_77_2 = lv.msgbox(parent)
    objects["msgbox_77_2"] = msgbox_77_2
    msgbox_77_2.set_pos(233, 157)
    msgbox_77_2.set_size(111, 86)
    msgbox_77_2_title = msgbox_77_2.add_title("Notice")
    msgbox_77_2_text = msgbox_77_2.add_text("Testo 77:2 \" \\ Città")
    msgbox_77_2_button_1 = msgbox_77_2.add_footer_button("OK")
    msgbox_77_2_button_2 = msgbox_77_2.add_footer_button("Cancel")
    msgbox_77_2_close = msgbox_77_2.add_close_button()
    msgbox_77_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # textarea: textarea_77_3
    textarea_77_3 = lv.textarea(parent)
    objects["textarea_77_3"] = textarea_77_3
    textarea_77_3.set_pos(260, 101)
    textarea_77_3.set_size(237, 52)
    textarea_77_3.set_text("Testo 77:3 \" \\ Città")
    textarea_77_3.set_placeholder_text("Type here")
    textarea_77_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_77_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_77_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # panel: panel_77_4
    panel_77_4 = lv.obj(parent)
    objects["panel_77_4"] = panel_77_4
    panel_77_4.set_pos(469, 318)
    panel_77_4.set_size(56, 156)
    panel_77_4.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_77_4.set_style_border_width(2, lv.PART.MAIN)
    panel_77_4.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_77_4.set_style_radius(5, lv.PART.MAIN)
    panel_77_4.set_style_pad_all(0, lv.PART.MAIN)
    panel_77_4.set_style_pad_gap(0, lv.PART.MAIN)

    # image: image_77_5
    image_77_5 = lv.image(parent)
    objects["image_77_5"] = image_77_5
    image_77_5.set_pos(587, 65)
    image_77_5.set_size(153, 75)


def random_77_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_77_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_77_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_77_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_77_get_current_page():
    return current_screen

def random_77_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_77_load_page(0)
