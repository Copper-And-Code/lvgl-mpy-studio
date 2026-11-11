"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 41
Generated: 2023-11-14T22:14:33.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_41_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # calendar: calendar_41_0
    calendar_41_0 = lv.calendar(parent)
    objects["calendar_41_0"] = calendar_41_0
    calendar_41_0.set_pos(306, 312)
    calendar_41_0.set_size(192, 10)
    calendar_41_0.set_today_date(2026, 10, 28)
    calendar_41_0.set_month_shown(2026, 10)
    calendar_41_0_header = calendar_41_0.add_header_arrow()
    calendar_41_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # msgbox: msgbox_41_1
    msgbox_41_1 = lv.msgbox(parent)
    objects["msgbox_41_1"] = msgbox_41_1
    msgbox_41_1.set_pos(115, 370)
    msgbox_41_1.set_size(196, 95)
    msgbox_41_1_title = msgbox_41_1.add_title("Notice")
    msgbox_41_1_text = msgbox_41_1.add_text("Testo 41:1 \" \\ Città")
    msgbox_41_1_button_1 = msgbox_41_1.add_footer_button("OK")
    msgbox_41_1_button_2 = msgbox_41_1.add_footer_button("Cancel")
    msgbox_41_1_close = msgbox_41_1.add_close_button()
    msgbox_41_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_41_2
    buttonmatrix_41_2 = lv.buttonmatrix(parent)
    objects["buttonmatrix_41_2"] = buttonmatrix_41_2
    buttonmatrix_41_2.set_pos(319, 305)
    buttonmatrix_41_2.set_size(192, 34)
    buttonmatrix_41_2_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_41_2.set_map(buttonmatrix_41_2_map)
    buttonmatrix_41_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_41_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_41_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_41_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # imagebutton: imagebutton_41_3
    imagebutton_41_3 = lv.imagebutton(parent)
    objects["imagebutton_41_3"] = imagebutton_41_3
    imagebutton_41_3.set_pos(277, 129)
    imagebutton_41_3.set_size(124, 76)
    imagebutton_41_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_41_3.set_style_radius(5, lv.PART.MAIN)
    imagebutton_41_3_label = lv.label(imagebutton_41_3)
    imagebutton_41_3_label.set_text("Testo 41:3 \" \\ Città")
    imagebutton_41_3_label.center()
    imagebutton_41_3_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_41_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_41_4
    buttonmatrix_41_4 = lv.buttonmatrix(parent)
    objects["buttonmatrix_41_4"] = buttonmatrix_41_4
    buttonmatrix_41_4.set_pos(350, 211)
    buttonmatrix_41_4.set_size(252, 65)
    buttonmatrix_41_4_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_41_4.set_map(buttonmatrix_41_4_map)
    buttonmatrix_41_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_41_4.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_41_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_41_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # keyboard: keyboard_41_5
    keyboard_41_5 = lv.keyboard(parent)
    objects["keyboard_41_5"] = keyboard_41_5
    keyboard_41_5.set_pos(505, 36)
    keyboard_41_5.set_size(171, 109)

    # tileview: tileview_41_6
    tileview_41_6 = lv.tileview(parent)
    objects["tileview_41_6"] = tileview_41_6
    tileview_41_6.set_pos(360, 165)
    tileview_41_6.set_size(141, 156)
    tileview_41_6.add_tile(0, 0, lv.DIR.ALL)
    tileview_41_6.add_tile(1, 0, lv.DIR.ALL)
    tileview_41_6.add_tile(0, 1, lv.DIR.ALL)
    tileview_41_6.add_tile(1, 1, lv.DIR.ALL)
    tileview_41_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # keyboard: keyboard_41_7
    keyboard_41_7 = lv.keyboard(parent)
    objects["keyboard_41_7"] = keyboard_41_7
    keyboard_41_7.set_pos(568, 56)
    keyboard_41_7.set_size(100, 88)


def random_41_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_41_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_41_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_41_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_41_get_current_page():
    return current_screen

def random_41_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_41_load_page(0)
