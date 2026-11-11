"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 114
Generated: 2023-11-14T22:15:46.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_114_5_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_114_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinbox: spinbox_114_0
    spinbox_114_0 = lv.spinbox(parent)
    objects["spinbox_114_0"] = spinbox_114_0
    spinbox_114_0.set_pos(391, 298)
    spinbox_114_0.set_size(241, 67)
    spinbox_114_0.set_digit_format(4, 0)
    spinbox_114_0.set_range(0, 999)
    spinbox_114_0.set_value(0)
    spinbox_114_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_114_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_114_0.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # win: win_114_1
    win_114_1 = lv.obj(parent)
    objects["win_114_1"] = win_114_1
    win_114_1.set_pos(34, 244)
    win_114_1.set_size(41, 124)
    win_114_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_114_1.set_style_pad_all(0, lv.PART.MAIN)
    win_114_1.set_style_pad_row(0, lv.PART.MAIN)
    win_114_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_114_1_header = lv.obj(win_114_1)
    win_114_1_header.set_size(lv.pct(100), 40)
    win_114_1_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_114_1_header.set_style_radius(0, lv.PART.MAIN)
    win_114_1_title = lv.label(win_114_1_header)
    win_114_1_title.set_text("Window Title")
    win_114_1_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_114_1_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_114_1_content = lv.obj(win_114_1)
    win_114_1_content.set_width(lv.pct(100))
    win_114_1_content.set_flex_grow(1)

    # spinbox: spinbox_114_2
    spinbox_114_2 = lv.spinbox(parent)
    objects["spinbox_114_2"] = spinbox_114_2
    spinbox_114_2.set_pos(158, 242)
    spinbox_114_2.set_size(142, 37)
    spinbox_114_2.set_digit_format(4, 0)
    spinbox_114_2.set_range(0, 999)
    spinbox_114_2.set_value(0)
    spinbox_114_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_114_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_114_2.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # list: list_114_3
    list_114_3 = lv.obj(parent)
    objects["list_114_3"] = list_114_3
    list_114_3.set_pos(501, 21)
    list_114_3.set_size(153, 30)
    list_114_3.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_114_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_114_3_item_1 = lv.button(list_114_3)
    list_114_3_item_1.set_width(lv.pct(100))
    list_114_3_item_1_label = lv.label(list_114_3_item_1)
    list_114_3_item_1_label.set_text("Item 1")
    list_114_3_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_114_3_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_114_3_item_2 = lv.button(list_114_3)
    list_114_3_item_2.set_width(lv.pct(100))
    list_114_3_item_2_label = lv.label(list_114_3_item_2)
    list_114_3_item_2_label.set_text("Item 2")
    list_114_3_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_114_3_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_114_3_item_3 = lv.button(list_114_3)
    list_114_3_item_3.set_width(lv.pct(100))
    list_114_3_item_3_label = lv.label(list_114_3_item_3)
    list_114_3_item_3_label.set_text("Item 3")
    list_114_3_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_114_3_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_114_3_item_4 = lv.button(list_114_3)
    list_114_3_item_4.set_width(lv.pct(100))
    list_114_3_item_4_label = lv.label(list_114_3_item_4)
    list_114_3_item_4_label.set_text("Item 4")
    list_114_3_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_114_3_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_114_3_item_5 = lv.button(list_114_3)
    list_114_3_item_5.set_width(lv.pct(100))
    list_114_3_item_5_label = lv.label(list_114_3_item_5)
    list_114_3_item_5_label.set_text("Item 5")
    list_114_3_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_114_3_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # image: image_114_4
    image_114_4 = lv.image(parent)
    objects["image_114_4"] = image_114_4
    image_114_4.set_pos(307, 394)
    image_114_4.set_size(29, 16)

    # slider: slider_114_5
    slider_114_5 = lv.slider(parent)
    objects["slider_114_5"] = slider_114_5
    slider_114_5.set_pos(195, 352)
    slider_114_5.set_size(186, 35)
    slider_114_5.set_range(0, 100)
    slider_114_5.set_value(50, False)
    slider_114_5.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_114_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_114_5.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_114_5.add_event_cb(slider_114_5_changed, lv.EVENT.VALUE_CHANGED, None)

    # arc: arc_114_6
    arc_114_6 = lv.arc(parent)
    objects["arc_114_6"] = arc_114_6
    arc_114_6.set_pos(393, 47)
    arc_114_6.set_size(126, 59)
    arc_114_6.set_bg_angles(135, 45)
    arc_114_6.set_range(0, 100)
    arc_114_6.set_value(50)
    arc_114_6.set_style_arc_width(10, lv.PART.MAIN)
    arc_114_6.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_114_6.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_114_6.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_114_6.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # panel: panel_114_7
    panel_114_7 = lv.obj(parent)
    objects["panel_114_7"] = panel_114_7
    panel_114_7.set_pos(421, 0)
    panel_114_7.set_size(202, 21)
    panel_114_7.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_114_7.set_style_border_width(2, lv.PART.MAIN)
    panel_114_7.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_114_7.set_style_radius(5, lv.PART.MAIN)
    panel_114_7.set_style_pad_all(0, lv.PART.MAIN)
    panel_114_7.set_style_pad_gap(0, lv.PART.MAIN)


def random_114_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_114_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_114_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_114_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_114_get_current_page():
    return current_screen

def random_114_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_114_load_page(0)
