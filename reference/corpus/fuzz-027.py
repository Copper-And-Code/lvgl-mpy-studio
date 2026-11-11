"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 27
Generated: 2023-11-14T22:14:19.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_27_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # arc: arc_27_0
    arc_27_0 = lv.arc(parent)
    objects["arc_27_0"] = arc_27_0
    arc_27_0.set_pos(675, 66)
    arc_27_0.set_size(57, 86)
    arc_27_0.set_bg_angles(135, 45)
    arc_27_0.set_range(0, 100)
    arc_27_0.set_value(50)
    arc_27_0.set_style_arc_width(10, lv.PART.MAIN)
    arc_27_0.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_27_0.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_27_0.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_27_0.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # msgbox: msgbox_27_1
    msgbox_27_1 = lv.msgbox(parent)
    objects["msgbox_27_1"] = msgbox_27_1
    msgbox_27_1.set_pos(672, 270)
    msgbox_27_1.set_size(36, 148)
    msgbox_27_1_title = msgbox_27_1.add_title("Notice")
    msgbox_27_1_text = msgbox_27_1.add_text("Testo 27:1 \" \\ Città")
    msgbox_27_1_button_1 = msgbox_27_1.add_footer_button("OK")
    msgbox_27_1_button_2 = msgbox_27_1.add_footer_button("Cancel")
    msgbox_27_1_close = msgbox_27_1.add_close_button()
    msgbox_27_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_27_2
    buttonmatrix_27_2 = lv.buttonmatrix(parent)
    objects["buttonmatrix_27_2"] = buttonmatrix_27_2
    buttonmatrix_27_2.set_pos(664, 222)
    buttonmatrix_27_2.set_size(224, 57)
    buttonmatrix_27_2_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_27_2.set_map(buttonmatrix_27_2_map)
    buttonmatrix_27_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_27_2.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_27_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_27_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # imagebutton: imagebutton_27_3
    imagebutton_27_3 = lv.imagebutton(parent)
    objects["imagebutton_27_3"] = imagebutton_27_3
    imagebutton_27_3.set_pos(318, 306)
    imagebutton_27_3.set_size(81, 14)
    imagebutton_27_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_27_3.set_style_radius(5, lv.PART.MAIN)
    imagebutton_27_3_label = lv.label(imagebutton_27_3)
    imagebutton_27_3_label.set_text("Testo 27:3 \" \\ Città")
    imagebutton_27_3_label.center()
    imagebutton_27_3_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_27_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # list: list_27_4
    list_27_4 = lv.obj(parent)
    objects["list_27_4"] = list_27_4
    list_27_4.set_pos(646, 227)
    list_27_4.set_size(145, 141)
    list_27_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_27_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_27_4_item_1 = lv.button(list_27_4)
    list_27_4_item_1.set_width(lv.pct(100))
    list_27_4_item_1_label = lv.label(list_27_4_item_1)
    list_27_4_item_1_label.set_text("Item 1")
    list_27_4_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_27_4_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_27_4_item_2 = lv.button(list_27_4)
    list_27_4_item_2.set_width(lv.pct(100))
    list_27_4_item_2_label = lv.label(list_27_4_item_2)
    list_27_4_item_2_label.set_text("Item 2")
    list_27_4_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_27_4_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_27_4_item_3 = lv.button(list_27_4)
    list_27_4_item_3.set_width(lv.pct(100))
    list_27_4_item_3_label = lv.label(list_27_4_item_3)
    list_27_4_item_3_label.set_text("Item 3")
    list_27_4_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_27_4_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_27_4_item_4 = lv.button(list_27_4)
    list_27_4_item_4.set_width(lv.pct(100))
    list_27_4_item_4_label = lv.label(list_27_4_item_4)
    list_27_4_item_4_label.set_text("Item 4")
    list_27_4_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_27_4_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_27_4_item_5 = lv.button(list_27_4)
    list_27_4_item_5.set_width(lv.pct(100))
    list_27_4_item_5_label = lv.label(list_27_4_item_5)
    list_27_4_item_5_label.set_text("Item 5")
    list_27_4_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_27_4_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_27_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_27_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_27_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_27_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_27_get_current_page():
    return current_screen

def random_27_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_27_load_page(0)
