"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 124
Generated: 2023-11-14T22:15:56.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_124_4_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # TODO: handle lv.EVENT.CLICKED
        pass

screens = [None] * 1
current_screen = 0

def random_124_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # msgbox: msgbox_124_0
    msgbox_124_0 = lv.msgbox(parent)
    objects["msgbox_124_0"] = msgbox_124_0
    msgbox_124_0.set_pos(539, 350)
    msgbox_124_0.set_size(40, 130)
    msgbox_124_0_title = msgbox_124_0.add_title("Notice")
    msgbox_124_0_text = msgbox_124_0.add_text("Testo 124:0 \" \\ Città")
    msgbox_124_0_button_1 = msgbox_124_0.add_footer_button("OK")
    msgbox_124_0_button_2 = msgbox_124_0.add_footer_button("Cancel")
    msgbox_124_0_close = msgbox_124_0.add_close_button()
    msgbox_124_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # calendar: calendar_124_1
    calendar_124_1 = lv.calendar(parent)
    objects["calendar_124_1"] = calendar_124_1
    calendar_124_1.set_pos(665, 83)
    calendar_124_1.set_size(244, 15)
    calendar_124_1.set_today_date(2026, 10, 28)
    calendar_124_1.set_month_shown(2026, 10)
    calendar_124_1_header = calendar_124_1.add_header_arrow()
    calendar_124_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # switch: switch_124_2
    switch_124_2 = lv.switch(parent)
    objects["switch_124_2"] = switch_124_2
    switch_124_2.set_pos(208, 331)
    switch_124_2.set_size(36, 64)
    switch_124_2.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_124_2.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_124_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # buttonmatrix: buttonmatrix_124_3
    buttonmatrix_124_3 = lv.buttonmatrix(parent)
    objects["buttonmatrix_124_3"] = buttonmatrix_124_3
    buttonmatrix_124_3.set_pos(178, 260)
    buttonmatrix_124_3.set_size(105, 62)
    buttonmatrix_124_3_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_124_3.set_map(buttonmatrix_124_3_map)
    buttonmatrix_124_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_124_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_124_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_124_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # button: button_124_4
    button_124_4 = lv.button(parent)
    objects["button_124_4"] = button_124_4
    button_124_4.set_pos(89, 357)
    button_124_4.set_size(60, 65)
    button_124_4.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_124_4.set_style_radius(5, lv.PART.MAIN)
    button_124_4_label = lv.label(button_124_4)
    button_124_4_label.set_text("Testo 124:4 \" \\ Città")
    button_124_4_label.center()
    button_124_4_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_124_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_124_4.add_event_cb(button_124_4_changed, lv.EVENT.CLICKED, None)

    # imagebutton: imagebutton_124_5
    imagebutton_124_5 = lv.imagebutton(parent)
    objects["imagebutton_124_5"] = imagebutton_124_5
    imagebutton_124_5.set_pos(559, 254)
    imagebutton_124_5.set_size(208, 63)
    imagebutton_124_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_124_5.set_style_radius(5, lv.PART.MAIN)
    imagebutton_124_5_label = lv.label(imagebutton_124_5)
    imagebutton_124_5_label.set_text("Testo 124:5 \" \\ Città")
    imagebutton_124_5_label.center()
    imagebutton_124_5_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_124_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # arc: arc_124_6
    arc_124_6 = lv.arc(parent)
    objects["arc_124_6"] = arc_124_6
    arc_124_6.set_pos(514, 75)
    arc_124_6.set_size(28, 14)
    arc_124_6.set_bg_angles(135, 45)
    arc_124_6.set_range(0, 100)
    arc_124_6.set_value(50)
    arc_124_6.set_style_arc_width(10, lv.PART.MAIN)
    arc_124_6.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_124_6.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_124_6.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_124_6.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # slider: slider_124_7
    slider_124_7 = lv.slider(parent)
    objects["slider_124_7"] = slider_124_7
    slider_124_7.set_pos(12, 352)
    slider_124_7.set_size(39, 26)
    slider_124_7.set_range(0, 100)
    slider_124_7.set_value(50, False)
    slider_124_7.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_124_7.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_124_7.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)


def random_124_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_124_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_124_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_124_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_124_get_current_page():
    return current_screen

def random_124_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_124_load_page(0)
