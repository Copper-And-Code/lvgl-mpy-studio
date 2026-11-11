"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 102
Generated: 2023-11-14T22:15:34.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_102_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # roller: roller_102_0
    roller_102_0 = lv.roller(parent)
    objects["roller_102_0"] = roller_102_0
    roller_102_0.set_pos(498, 88)
    roller_102_0.set_size(263, 31)
    roller_102_0.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_102_0.set_visible_row_count(3)
    roller_102_0.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_102_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_102_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_102_0.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # list: list_102_1
    list_102_1 = lv.obj(parent)
    objects["list_102_1"] = list_102_1
    list_102_1.set_pos(342, 82)
    list_102_1.set_size(125, 114)
    list_102_1.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_102_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_102_1_item_1 = lv.button(list_102_1)
    list_102_1_item_1.set_width(lv.pct(100))
    list_102_1_item_1_label = lv.label(list_102_1_item_1)
    list_102_1_item_1_label.set_text("Item 1")
    list_102_1_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_102_1_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_102_1_item_2 = lv.button(list_102_1)
    list_102_1_item_2.set_width(lv.pct(100))
    list_102_1_item_2_label = lv.label(list_102_1_item_2)
    list_102_1_item_2_label.set_text("Item 2")
    list_102_1_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_102_1_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_102_1_item_3 = lv.button(list_102_1)
    list_102_1_item_3.set_width(lv.pct(100))
    list_102_1_item_3_label = lv.label(list_102_1_item_3)
    list_102_1_item_3_label.set_text("Item 3")
    list_102_1_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_102_1_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_102_1_item_4 = lv.button(list_102_1)
    list_102_1_item_4.set_width(lv.pct(100))
    list_102_1_item_4_label = lv.label(list_102_1_item_4)
    list_102_1_item_4_label.set_text("Item 4")
    list_102_1_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_102_1_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_102_1_item_5 = lv.button(list_102_1)
    list_102_1_item_5.set_width(lv.pct(100))
    list_102_1_item_5_label = lv.label(list_102_1_item_5)
    list_102_1_item_5_label.set_text("Item 5")
    list_102_1_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_102_1_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # spinner: spinner_102_2
    spinner_102_2 = lv.arc(parent)
    objects["spinner_102_2"] = spinner_102_2
    spinner_102_2.set_pos(239, 281)
    spinner_102_2.set_size(117, 100)
    spinner_102_2.set_bg_angles(0, 360)
    spinner_102_2.set_angles(0, 60)
    spinner_102_2.remove_style(None, lv.PART.KNOB)
    spinner_102_2.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_102_2_anim = lv.anim_t()
    spinner_102_2_anim.init()
    spinner_102_2_anim.set_var(spinner_102_2)
    spinner_102_2_anim.set_values(0, 360)
    spinner_102_2_anim.set_duration(1000)
    spinner_102_2_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_102_2_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_102_2_anim.set_custom_exec_cb(lambda _anim, value: spinner_102_2.set_rotation(value))
    spinner_102_2_anim.start()
    spinner_102_2.set_style_arc_width(8, lv.PART.MAIN)
    spinner_102_2.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_102_2.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # spinner: spinner_102_3
    spinner_102_3 = lv.arc(parent)
    objects["spinner_102_3"] = spinner_102_3
    spinner_102_3.set_pos(588, 18)
    spinner_102_3.set_size(181, 54)
    spinner_102_3.set_bg_angles(0, 360)
    spinner_102_3.set_angles(0, 60)
    spinner_102_3.remove_style(None, lv.PART.KNOB)
    spinner_102_3.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_102_3_anim = lv.anim_t()
    spinner_102_3_anim.init()
    spinner_102_3_anim.set_var(spinner_102_3)
    spinner_102_3_anim.set_values(0, 360)
    spinner_102_3_anim.set_duration(1000)
    spinner_102_3_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_102_3_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_102_3_anim.set_custom_exec_cb(lambda _anim, value: spinner_102_3.set_rotation(value))
    spinner_102_3_anim.start()
    spinner_102_3.set_style_arc_width(8, lv.PART.MAIN)
    spinner_102_3.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_102_3.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_102_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_102_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_102_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_102_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_102_get_current_page():
    return current_screen

def random_102_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_102_load_page(0)
