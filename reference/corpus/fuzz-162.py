"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 162
Generated: 2023-11-14T22:16:34.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_162_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # dropdown: dropdown_162_0
    dropdown_162_0 = lv.dropdown(parent)
    objects["dropdown_162_0"] = dropdown_162_0
    dropdown_162_0.set_pos(261, 8)
    dropdown_162_0.set_size(165, 67)
    dropdown_162_0.set_options("Option 1\nOption 2\nOption 3")
    dropdown_162_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_162_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_162_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # calendar: calendar_162_1
    calendar_162_1 = lv.calendar(parent)
    objects["calendar_162_1"] = calendar_162_1
    calendar_162_1.set_pos(468, 374)
    calendar_162_1.set_size(165, 83)
    calendar_162_1.set_today_date(2026, 10, 28)
    calendar_162_1.set_month_shown(2026, 10)
    calendar_162_1_header = calendar_162_1.add_header_arrow()
    calendar_162_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # calendar: calendar_162_2
    calendar_162_2 = lv.calendar(parent)
    objects["calendar_162_2"] = calendar_162_2
    calendar_162_2.set_pos(61, 38)
    calendar_162_2.set_size(36, 11)
    calendar_162_2.set_today_date(2026, 10, 28)
    calendar_162_2.set_month_shown(2026, 10)
    calendar_162_2_header = calendar_162_2.add_header_arrow()
    calendar_162_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # image: image_162_3
    image_162_3 = lv.image(parent)
    objects["image_162_3"] = image_162_3
    image_162_3.set_pos(178, 360)
    image_162_3.set_size(202, 33)


def random_162_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_162_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_162_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_162_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_162_get_current_page():
    return current_screen

def random_162_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_162_load_page(0)
