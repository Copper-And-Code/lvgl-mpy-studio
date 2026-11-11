"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 59
Generated: 2023-11-14T22:14:51.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_59_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinbox: spinbox_59_0
    spinbox_59_0 = lv.spinbox(parent)
    objects["spinbox_59_0"] = spinbox_59_0
    spinbox_59_0.set_pos(628, 366)
    spinbox_59_0.set_size(178, 147)
    spinbox_59_0.set_digit_format(4, 0)
    spinbox_59_0.set_range(0, 999)
    spinbox_59_0.set_value(0)
    spinbox_59_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_59_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_59_0.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # spinbox: spinbox_59_1
    spinbox_59_1 = lv.spinbox(parent)
    objects["spinbox_59_1"] = spinbox_59_1
    spinbox_59_1.set_pos(300, 220)
    spinbox_59_1.set_size(217, 105)
    spinbox_59_1.set_digit_format(4, 0)
    spinbox_59_1.set_range(0, 999)
    spinbox_59_1.set_value(0)
    spinbox_59_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_59_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_59_1.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # tileview: tileview_59_2
    tileview_59_2 = lv.tileview(parent)
    objects["tileview_59_2"] = tileview_59_2
    tileview_59_2.set_pos(649, 350)
    tileview_59_2.set_size(244, 44)
    tileview_59_2.add_tile(0, 0, lv.DIR.ALL)
    tileview_59_2.add_tile(1, 0, lv.DIR.ALL)
    tileview_59_2.add_tile(0, 1, lv.DIR.ALL)
    tileview_59_2.add_tile(1, 1, lv.DIR.ALL)
    tileview_59_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # msgbox: msgbox_59_3
    msgbox_59_3 = lv.msgbox(parent)
    objects["msgbox_59_3"] = msgbox_59_3
    msgbox_59_3.set_pos(327, 397)
    msgbox_59_3.set_size(260, 84)
    msgbox_59_3_title = msgbox_59_3.add_title("Notice")
    msgbox_59_3_text = msgbox_59_3.add_text("Testo 59:3 \" \\ Città")
    msgbox_59_3_button_1 = msgbox_59_3.add_footer_button("OK")
    msgbox_59_3_button_2 = msgbox_59_3.add_footer_button("Cancel")
    msgbox_59_3_close = msgbox_59_3.add_close_button()
    msgbox_59_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # table: table_59_4
    table_59_4 = lv.table(parent)
    objects["table_59_4"] = table_59_4
    table_59_4.set_pos(457, 45)
    table_59_4.set_size(84, 84)
    table_59_4.set_column_count(3)
    table_59_4.set_column_width(0, 100)
    table_59_4.set_column_width(1, 100)
    table_59_4.set_column_width(2, 100)
    table_59_4.set_cell_value(0, 0, "Col 1")
    table_59_4.set_cell_value(0, 1, "Col 2")
    table_59_4.set_cell_value(0, 2, "Col 3")
    table_59_4.set_cell_value(1, 0, "A1")
    table_59_4.set_cell_value(1, 1, "B1")
    table_59_4.set_cell_value(1, 2, "C1")
    table_59_4.set_cell_value(2, 0, "A2")
    table_59_4.set_cell_value(2, 1, "B2")
    table_59_4.set_cell_value(2, 2, "C2")
    table_59_4.set_cell_value(3, 0, "A3")
    table_59_4.set_cell_value(3, 1, "B3")
    table_59_4.set_cell_value(3, 2, "C3")
    table_59_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_59_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_59_4.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_59_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # label: label_59_5
    label_59_5 = lv.label(parent)
    objects["label_59_5"] = label_59_5
    label_59_5.set_pos(609, 355)
    label_59_5.set_size(243, 96)
    label_59_5.set_text("Testo 59:5 \" \\ Città")
    label_59_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_59_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_59_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # imagebutton: imagebutton_59_6
    imagebutton_59_6 = lv.imagebutton(parent)
    objects["imagebutton_59_6"] = imagebutton_59_6
    imagebutton_59_6.set_pos(501, 329)
    imagebutton_59_6.set_size(148, 92)
    imagebutton_59_6.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_59_6.set_style_radius(5, lv.PART.MAIN)
    imagebutton_59_6_label = lv.label(imagebutton_59_6)
    imagebutton_59_6_label.set_text("Testo 59:6 \" \\ Città")
    imagebutton_59_6_label.center()
    imagebutton_59_6_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_59_6_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # imagebutton: imagebutton_59_7
    imagebutton_59_7 = lv.imagebutton(parent)
    objects["imagebutton_59_7"] = imagebutton_59_7
    imagebutton_59_7.set_pos(553, 357)
    imagebutton_59_7.set_size(68, 44)
    imagebutton_59_7.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_59_7.set_style_radius(5, lv.PART.MAIN)
    imagebutton_59_7_label = lv.label(imagebutton_59_7)
    imagebutton_59_7_label.set_text("Testo 59:7 \" \\ Città")
    imagebutton_59_7_label.center()
    imagebutton_59_7_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_59_7_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_59_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_59_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_59_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_59_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_59_get_current_page():
    return current_screen

def random_59_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_59_load_page(0)
