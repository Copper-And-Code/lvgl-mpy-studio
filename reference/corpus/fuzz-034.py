"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 34
Generated: 2023-11-14T22:14:26.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_34_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # calendar: calendar_34_0
    calendar_34_0 = lv.calendar(parent)
    objects["calendar_34_0"] = calendar_34_0
    calendar_34_0.set_pos(615, 371)
    calendar_34_0.set_size(256, 119)
    calendar_34_0.set_today_date(2026, 10, 28)
    calendar_34_0.set_month_shown(2026, 10)
    calendar_34_0_header = calendar_34_0.add_header_arrow()
    calendar_34_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # imagebutton: imagebutton_34_1
    imagebutton_34_1 = lv.imagebutton(parent)
    objects["imagebutton_34_1"] = imagebutton_34_1
    imagebutton_34_1.set_pos(212, 205)
    imagebutton_34_1.set_size(78, 78)
    imagebutton_34_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_34_1.set_style_radius(5, lv.PART.MAIN)
    imagebutton_34_1_label = lv.label(imagebutton_34_1)
    imagebutton_34_1_label.set_text("Testo 34:1 \" \\ Città")
    imagebutton_34_1_label.center()
    imagebutton_34_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_34_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # spinbox: spinbox_34_2
    spinbox_34_2 = lv.spinbox(parent)
    objects["spinbox_34_2"] = spinbox_34_2
    spinbox_34_2.set_pos(605, 359)
    spinbox_34_2.set_size(177, 89)
    spinbox_34_2.set_digit_format(4, 0)
    spinbox_34_2.set_range(0, 999)
    spinbox_34_2.set_value(0)
    spinbox_34_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_34_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_34_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)


def random_34_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_34_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_34_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_34_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_34_get_current_page():
    return current_screen

def random_34_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_34_load_page(0)
