"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 17
Generated: 2023-11-14T22:14:09.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def checkbox_17_2_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_17_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # image: image_17_0
    image_17_0 = lv.image(parent)
    objects["image_17_0"] = image_17_0
    image_17_0.set_pos(54, 335)
    image_17_0.set_size(158, 118)

    # list: list_17_1
    list_17_1 = lv.obj(parent)
    objects["list_17_1"] = list_17_1
    list_17_1.set_pos(162, 233)
    list_17_1.set_size(120, 128)
    list_17_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_17_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_17_1_item_1 = lv.button(list_17_1)
    list_17_1_item_1.set_width(lv.pct(100))
    list_17_1_item_1_label = lv.label(list_17_1_item_1)
    list_17_1_item_1_label.set_text("Item 1")
    list_17_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_17_1_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_17_1_item_2 = lv.button(list_17_1)
    list_17_1_item_2.set_width(lv.pct(100))
    list_17_1_item_2_label = lv.label(list_17_1_item_2)
    list_17_1_item_2_label.set_text("Item 2")
    list_17_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_17_1_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_17_1_item_3 = lv.button(list_17_1)
    list_17_1_item_3.set_width(lv.pct(100))
    list_17_1_item_3_label = lv.label(list_17_1_item_3)
    list_17_1_item_3_label.set_text("Item 3")
    list_17_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_17_1_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_17_1_item_4 = lv.button(list_17_1)
    list_17_1_item_4.set_width(lv.pct(100))
    list_17_1_item_4_label = lv.label(list_17_1_item_4)
    list_17_1_item_4_label.set_text("Item 4")
    list_17_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_17_1_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_17_1_item_5 = lv.button(list_17_1)
    list_17_1_item_5.set_width(lv.pct(100))
    list_17_1_item_5_label = lv.label(list_17_1_item_5)
    list_17_1_item_5_label.set_text("Item 5")
    list_17_1_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_17_1_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # checkbox: checkbox_17_2
    checkbox_17_2 = lv.checkbox(parent)
    objects["checkbox_17_2"] = checkbox_17_2
    checkbox_17_2.set_pos(393, 15)
    checkbox_17_2.set_text("Testo 17:2 \" \\ Città")
    checkbox_17_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_17_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_17_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_17_2.add_event_cb(checkbox_17_2_changed, lv.EVENT.VALUE_CHANGED, None)

    # spinbox: spinbox_17_3
    spinbox_17_3 = lv.spinbox(parent)
    objects["spinbox_17_3"] = spinbox_17_3
    spinbox_17_3.set_pos(597, 193)
    spinbox_17_3.set_size(146, 148)
    spinbox_17_3.set_digit_format(4, 0)
    spinbox_17_3.set_range(0, 999)
    spinbox_17_3.set_value(0)
    spinbox_17_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_17_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_17_3.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # scale: scale_17_4
    scale_17_4 = lv.scale(parent)
    objects["scale_17_4"] = scale_17_4
    scale_17_4.set_pos(591, 323)
    scale_17_4.set_size(35, 74)
    scale_17_4.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_17_4.set_range(0, 100)
    scale_17_4.set_total_tick_count(51)
    scale_17_4.set_major_tick_every(5)
    scale_17_4.set_style_length(15, lv.PART.INDICATOR)
    scale_17_4.set_style_length(8, lv.PART.ITEMS)
    scale_17_4.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_17_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # spinner: spinner_17_5
    spinner_17_5 = lv.arc(parent)
    objects["spinner_17_5"] = spinner_17_5
    spinner_17_5.set_pos(351, 350)
    spinner_17_5.set_size(261, 150)
    spinner_17_5.set_bg_angles(0, 360)
    spinner_17_5.set_angles(0, 60)
    spinner_17_5.remove_style(None, lv.PART.KNOB)
    spinner_17_5.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_17_5_anim = lv.anim_t()
    spinner_17_5_anim.init()
    spinner_17_5_anim.set_var(spinner_17_5)
    spinner_17_5_anim.set_values(0, 360)
    spinner_17_5_anim.set_duration(1000)
    spinner_17_5_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_17_5_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_17_5_anim.set_custom_exec_cb(lambda _anim, value: spinner_17_5.set_rotation(value))
    spinner_17_5_anim.start()
    spinner_17_5.set_style_arc_width(8, lv.PART.MAIN)
    spinner_17_5.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_17_5.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # spinner: spinner_17_6
    spinner_17_6 = lv.arc(parent)
    objects["spinner_17_6"] = spinner_17_6
    spinner_17_6.set_pos(204, 143)
    spinner_17_6.set_size(220, 62)
    spinner_17_6.set_bg_angles(0, 360)
    spinner_17_6.set_angles(0, 60)
    spinner_17_6.remove_style(None, lv.PART.KNOB)
    spinner_17_6.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_17_6_anim = lv.anim_t()
    spinner_17_6_anim.init()
    spinner_17_6_anim.set_var(spinner_17_6)
    spinner_17_6_anim.set_values(0, 360)
    spinner_17_6_anim.set_duration(1000)
    spinner_17_6_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_17_6_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_17_6_anim.set_custom_exec_cb(lambda _anim, value: spinner_17_6.set_rotation(value))
    spinner_17_6_anim.start()
    spinner_17_6.set_style_arc_width(8, lv.PART.MAIN)
    spinner_17_6.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_17_6.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_17_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_17_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_17_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_17_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_17_get_current_page():
    return current_screen

def random_17_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_17_load_page(0)
