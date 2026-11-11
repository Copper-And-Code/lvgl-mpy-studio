"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 185
Generated: 2023-11-14T22:16:57.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_185_5_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # TODO: handle lv.EVENT.CLICKED
        pass

screens = [None] * 1
current_screen = 0

def random_185_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # span: span_185_0
    span_185_0 = lv.spangroup(parent)
    objects["span_185_0"] = span_185_0
    span_185_0.set_pos(428, 242)
    span_185_0.set_size(195, 155)
    span_185_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_185_0_span_1 = span_185_0.add_span()
    span_185_0_span_1.set_text("Normal text")
    span_185_0_span_1_style = span_185_0_span_1.get_style()
    span_185_0_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_185_0_span_1_style.set_text_font(lv.font_montserrat_14)
    span_185_0_span_2 = span_185_0.add_span()
    span_185_0_span_2.set_text("Bold text")
    span_185_0_span_2_style = span_185_0_span_2.get_style()
    span_185_0_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_185_0_span_2_style.set_text_font(lv.font_montserrat_16)
    span_185_0_span_3 = span_185_0.add_span()
    span_185_0_span_3.set_text("Small text")
    span_185_0_span_3_style = span_185_0_span_3.get_style()
    span_185_0_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_185_0_span_3_style.set_text_font(lv.font_montserrat_14)
    span_185_0.refresh()

    # buttonmatrix: buttonmatrix_185_1
    buttonmatrix_185_1 = lv.buttonmatrix(parent)
    objects["buttonmatrix_185_1"] = buttonmatrix_185_1
    buttonmatrix_185_1.set_pos(668, 360)
    buttonmatrix_185_1.set_size(73, 54)
    buttonmatrix_185_1_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_185_1.set_map(buttonmatrix_185_1_map)
    buttonmatrix_185_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_185_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_185_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_185_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # button: button_185_2
    button_185_2 = lv.button(parent)
    objects["button_185_2"] = button_185_2
    button_185_2.set_pos(304, 358)
    button_185_2.set_size(61, 32)
    button_185_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_185_2.set_style_radius(5, lv.PART.MAIN)
    button_185_2_label = lv.label(button_185_2)
    button_185_2_label.set_text("Testo 185:2 \" \\ Città")
    button_185_2_label.center()
    button_185_2_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_185_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # msgbox: msgbox_185_3
    msgbox_185_3 = lv.msgbox(parent)
    objects["msgbox_185_3"] = msgbox_185_3
    msgbox_185_3.set_pos(526, 22)
    msgbox_185_3.set_size(192, 63)
    msgbox_185_3_title = msgbox_185_3.add_title("Notice")
    msgbox_185_3_text = msgbox_185_3.add_text("Testo 185:3 \" \\ Città")
    msgbox_185_3_button_1 = msgbox_185_3.add_footer_button("OK")
    msgbox_185_3_button_2 = msgbox_185_3.add_footer_button("Cancel")
    msgbox_185_3_close = msgbox_185_3.add_close_button()
    msgbox_185_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # calendar: calendar_185_4
    calendar_185_4 = lv.calendar(parent)
    objects["calendar_185_4"] = calendar_185_4
    calendar_185_4.set_pos(479, 37)
    calendar_185_4.set_size(174, 103)
    calendar_185_4.set_today_date(2026, 10, 28)
    calendar_185_4.set_month_shown(2026, 10)
    calendar_185_4_header = calendar_185_4.add_header_arrow()
    calendar_185_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # button: button_185_5
    button_185_5 = lv.button(parent)
    objects["button_185_5"] = button_185_5
    button_185_5.set_pos(63, 333)
    button_185_5.set_size(229, 157)
    button_185_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_185_5.set_style_radius(5, lv.PART.MAIN)
    button_185_5_label = lv.label(button_185_5)
    button_185_5_label.set_text("Testo 185:5 \" \\ Città")
    button_185_5_label.center()
    button_185_5_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_185_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_185_5.add_event_cb(button_185_5_changed, lv.EVENT.CLICKED, None)


def random_185_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_185_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_185_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_185_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_185_get_current_page():
    return current_screen

def random_185_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_185_load_page(0)
