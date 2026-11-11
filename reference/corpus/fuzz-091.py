"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 91
Generated: 2023-11-14T22:15:23.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_91_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # label: label_91_0
    label_91_0 = lv.label(parent)
    objects["label_91_0"] = label_91_0
    label_91_0.set_pos(9, 156)
    label_91_0.set_size(77, 72)
    label_91_0.set_text("Testo 91:0 \" \\ Città")
    label_91_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_91_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_91_0.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # spinner: spinner_91_1
    spinner_91_1 = lv.arc(parent)
    objects["spinner_91_1"] = spinner_91_1
    spinner_91_1.set_pos(615, 369)
    spinner_91_1.set_size(59, 37)
    spinner_91_1.set_bg_angles(0, 360)
    spinner_91_1.set_angles(0, 60)
    spinner_91_1.remove_style(None, lv.PART.KNOB)
    spinner_91_1.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_91_1_anim = lv.anim_t()
    spinner_91_1_anim.init()
    spinner_91_1_anim.set_var(spinner_91_1)
    spinner_91_1_anim.set_values(0, 360)
    spinner_91_1_anim.set_duration(1000)
    spinner_91_1_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_91_1_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_91_1_anim.set_custom_exec_cb(lambda _anim, value: spinner_91_1.set_rotation(value))
    spinner_91_1_anim.start()
    spinner_91_1.set_style_arc_width(8, lv.PART.MAIN)
    spinner_91_1.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_91_1.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # spinner: spinner_91_2
    spinner_91_2 = lv.arc(parent)
    objects["spinner_91_2"] = spinner_91_2
    spinner_91_2.set_pos(325, 227)
    spinner_91_2.set_size(80, 57)
    spinner_91_2.set_bg_angles(0, 360)
    spinner_91_2.set_angles(0, 60)
    spinner_91_2.remove_style(None, lv.PART.KNOB)
    spinner_91_2.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_91_2_anim = lv.anim_t()
    spinner_91_2_anim.init()
    spinner_91_2_anim.set_var(spinner_91_2)
    spinner_91_2_anim.set_values(0, 360)
    spinner_91_2_anim.set_duration(1000)
    spinner_91_2_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_91_2_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_91_2_anim.set_custom_exec_cb(lambda _anim, value: spinner_91_2.set_rotation(value))
    spinner_91_2_anim.start()
    spinner_91_2.set_style_arc_width(8, lv.PART.MAIN)
    spinner_91_2.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_91_2.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # image: image_91_3
    image_91_3 = lv.image(parent)
    objects["image_91_3"] = image_91_3
    image_91_3.set_pos(678, 396)
    image_91_3.set_size(213, 142)

    # roller: roller_91_4
    roller_91_4 = lv.roller(parent)
    objects["roller_91_4"] = roller_91_4
    roller_91_4.set_pos(18, 399)
    roller_91_4.set_size(81, 90)
    roller_91_4.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_91_4.set_visible_row_count(3)
    roller_91_4.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_91_4.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_91_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_91_4.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # list: list_91_5
    list_91_5 = lv.obj(parent)
    objects["list_91_5"] = list_91_5
    list_91_5.set_pos(501, 26)
    list_91_5.set_size(96, 120)
    list_91_5.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_91_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_91_5_item_1 = lv.button(list_91_5)
    list_91_5_item_1.set_width(lv.pct(100))
    list_91_5_item_1_label = lv.label(list_91_5_item_1)
    list_91_5_item_1_label.set_text("Item 1")
    list_91_5_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_91_5_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_91_5_item_2 = lv.button(list_91_5)
    list_91_5_item_2.set_width(lv.pct(100))
    list_91_5_item_2_label = lv.label(list_91_5_item_2)
    list_91_5_item_2_label.set_text("Item 2")
    list_91_5_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_91_5_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_91_5_item_3 = lv.button(list_91_5)
    list_91_5_item_3.set_width(lv.pct(100))
    list_91_5_item_3_label = lv.label(list_91_5_item_3)
    list_91_5_item_3_label.set_text("Item 3")
    list_91_5_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_91_5_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_91_5_item_4 = lv.button(list_91_5)
    list_91_5_item_4.set_width(lv.pct(100))
    list_91_5_item_4_label = lv.label(list_91_5_item_4)
    list_91_5_item_4_label.set_text("Item 4")
    list_91_5_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_91_5_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_91_5_item_5 = lv.button(list_91_5)
    list_91_5_item_5.set_width(lv.pct(100))
    list_91_5_item_5_label = lv.label(list_91_5_item_5)
    list_91_5_item_5_label.set_text("Item 5")
    list_91_5_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_91_5_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # keyboard: keyboard_91_6
    keyboard_91_6 = lv.keyboard(parent)
    objects["keyboard_91_6"] = keyboard_91_6
    keyboard_91_6.set_pos(424, 335)
    keyboard_91_6.set_size(103, 12)

    # scale: scale_91_7
    scale_91_7 = lv.scale(parent)
    objects["scale_91_7"] = scale_91_7
    scale_91_7.set_pos(200, 18)
    scale_91_7.set_size(162, 86)
    scale_91_7.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_91_7.set_range(0, 100)
    scale_91_7.set_total_tick_count(51)
    scale_91_7.set_major_tick_every(5)
    scale_91_7.set_style_length(15, lv.PART.INDICATOR)
    scale_91_7.set_style_length(8, lv.PART.ITEMS)
    scale_91_7.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_91_7.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)


def random_91_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_91_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_91_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_91_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_91_get_current_page():
    return current_screen

def random_91_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_91_load_page(0)
