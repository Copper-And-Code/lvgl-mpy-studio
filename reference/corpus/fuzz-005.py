"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 5
Generated: 2023-11-14T22:13:57.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_5_5_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # TODO: handle lv.EVENT.CLICKED
        pass

screens = [None] * 1
current_screen = 0

def random_5_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # panel: panel_5_0
    panel_5_0 = lv.obj(parent)
    objects["panel_5_0"] = panel_5_0
    panel_5_0.set_pos(242, 355)
    panel_5_0.set_size(249, 54)
    panel_5_0.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_5_0.set_style_border_width(2, lv.PART.MAIN)
    panel_5_0.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_5_0.set_style_radius(5, lv.PART.MAIN)
    panel_5_0.set_style_pad_all(0, lv.PART.MAIN)
    panel_5_0.set_style_pad_gap(0, lv.PART.MAIN)

    # menu: menu_5_1
    menu_5_1 = lv.obj(parent)
    objects["menu_5_1"] = menu_5_1
    menu_5_1.set_pos(21, 274)
    menu_5_1.set_size(229, 80)
    menu_5_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_5_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_5_1_title = lv.label(menu_5_1)
    menu_5_1_title.set_text("Menu")
    menu_5_1_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_5_1_item_1 = lv.button(menu_5_1)
    menu_5_1_item_1.set_width(lv.pct(100))
    menu_5_1_item_1_label = lv.label(menu_5_1_item_1)
    menu_5_1_item_1_label.set_text("Item 1")
    menu_5_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_5_1_item_2 = lv.button(menu_5_1)
    menu_5_1_item_2.set_width(lv.pct(100))
    menu_5_1_item_2_label = lv.label(menu_5_1_item_2)
    menu_5_1_item_2_label.set_text("Item 2")
    menu_5_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_5_1_item_3 = lv.button(menu_5_1)
    menu_5_1_item_3.set_width(lv.pct(100))
    menu_5_1_item_3_label = lv.label(menu_5_1_item_3)
    menu_5_1_item_3_label.set_text("Item 3")
    menu_5_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_5_1_item_4 = lv.button(menu_5_1)
    menu_5_1_item_4.set_width(lv.pct(100))
    menu_5_1_item_4_label = lv.label(menu_5_1_item_4)
    menu_5_1_item_4_label.set_text("Item 4")
    menu_5_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # menu: menu_5_2
    menu_5_2 = lv.obj(parent)
    objects["menu_5_2"] = menu_5_2
    menu_5_2.set_pos(184, 19)
    menu_5_2.set_size(107, 103)
    menu_5_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_5_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_5_2_title = lv.label(menu_5_2)
    menu_5_2_title.set_text("Menu")
    menu_5_2_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_5_2_item_1 = lv.button(menu_5_2)
    menu_5_2_item_1.set_width(lv.pct(100))
    menu_5_2_item_1_label = lv.label(menu_5_2_item_1)
    menu_5_2_item_1_label.set_text("Item 1")
    menu_5_2_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_5_2_item_2 = lv.button(menu_5_2)
    menu_5_2_item_2.set_width(lv.pct(100))
    menu_5_2_item_2_label = lv.label(menu_5_2_item_2)
    menu_5_2_item_2_label.set_text("Item 2")
    menu_5_2_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_5_2_item_3 = lv.button(menu_5_2)
    menu_5_2_item_3.set_width(lv.pct(100))
    menu_5_2_item_3_label = lv.label(menu_5_2_item_3)
    menu_5_2_item_3_label.set_text("Item 3")
    menu_5_2_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_5_2_item_4 = lv.button(menu_5_2)
    menu_5_2_item_4.set_width(lv.pct(100))
    menu_5_2_item_4_label = lv.label(menu_5_2_item_4)
    menu_5_2_item_4_label.set_text("Item 4")
    menu_5_2_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # switch: switch_5_3
    switch_5_3 = lv.switch(parent)
    objects["switch_5_3"] = switch_5_3
    switch_5_3.set_pos(500, 48)
    switch_5_3.set_size(172, 59)
    switch_5_3.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_5_3.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_5_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)

    # spinner: spinner_5_4
    spinner_5_4 = lv.arc(parent)
    objects["spinner_5_4"] = spinner_5_4
    spinner_5_4.set_pos(428, 35)
    spinner_5_4.set_size(88, 147)
    spinner_5_4.set_bg_angles(0, 360)
    spinner_5_4.set_angles(0, 60)
    spinner_5_4.remove_style(None, lv.PART.KNOB)
    spinner_5_4.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_5_4_anim = lv.anim_t()
    spinner_5_4_anim.init()
    spinner_5_4_anim.set_var(spinner_5_4)
    spinner_5_4_anim.set_values(0, 360)
    spinner_5_4_anim.set_duration(1000)
    spinner_5_4_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_5_4_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_5_4_anim.set_custom_exec_cb(lambda _anim, value: spinner_5_4.set_rotation(value))
    spinner_5_4_anim.start()
    spinner_5_4.set_style_arc_width(8, lv.PART.MAIN)
    spinner_5_4.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_5_4.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # button: button_5_5
    button_5_5 = lv.button(parent)
    objects["button_5_5"] = button_5_5
    button_5_5.set_pos(92, 195)
    button_5_5.set_size(57, 76)
    button_5_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_5_5.set_style_radius(5, lv.PART.MAIN)
    button_5_5_label = lv.label(button_5_5)
    button_5_5_label.set_text("Testo 5:5 \" \\ Città")
    button_5_5_label.center()
    button_5_5_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_5_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_5_5.add_event_cb(button_5_5_changed, lv.EVENT.CLICKED, None)

    # menu: menu_5_6
    menu_5_6 = lv.obj(parent)
    objects["menu_5_6"] = menu_5_6
    menu_5_6.set_pos(619, 165)
    menu_5_6.set_size(212, 10)
    menu_5_6.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_5_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_5_6_title = lv.label(menu_5_6)
    menu_5_6_title.set_text("Menu")
    menu_5_6_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_5_6_item_1 = lv.button(menu_5_6)
    menu_5_6_item_1.set_width(lv.pct(100))
    menu_5_6_item_1_label = lv.label(menu_5_6_item_1)
    menu_5_6_item_1_label.set_text("Item 1")
    menu_5_6_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_5_6_item_2 = lv.button(menu_5_6)
    menu_5_6_item_2.set_width(lv.pct(100))
    menu_5_6_item_2_label = lv.label(menu_5_6_item_2)
    menu_5_6_item_2_label.set_text("Item 2")
    menu_5_6_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_5_6_item_3 = lv.button(menu_5_6)
    menu_5_6_item_3.set_width(lv.pct(100))
    menu_5_6_item_3_label = lv.label(menu_5_6_item_3)
    menu_5_6_item_3_label.set_text("Item 3")
    menu_5_6_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_5_6_item_4 = lv.button(menu_5_6)
    menu_5_6_item_4.set_width(lv.pct(100))
    menu_5_6_item_4_label = lv.label(menu_5_6_item_4)
    menu_5_6_item_4_label.set_text("Item 4")
    menu_5_6_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)


def random_5_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_5_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_5_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_5_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_5_get_current_page():
    return current_screen

def random_5_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_5_load_page(0)
