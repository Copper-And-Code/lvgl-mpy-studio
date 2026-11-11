"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 111
Generated: 2023-11-14T22:15:43.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_111_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # menu: menu_111_0
    menu_111_0 = lv.obj(parent)
    objects["menu_111_0"] = menu_111_0
    menu_111_0.set_pos(135, 391)
    menu_111_0.set_size(140, 99)
    menu_111_0.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_111_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_111_0_title = lv.label(menu_111_0)
    menu_111_0_title.set_text("Menu")
    menu_111_0_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_111_0_item_1 = lv.button(menu_111_0)
    menu_111_0_item_1.set_width(lv.pct(100))
    menu_111_0_item_1_label = lv.label(menu_111_0_item_1)
    menu_111_0_item_1_label.set_text("Item 1")
    menu_111_0_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_111_0_item_2 = lv.button(menu_111_0)
    menu_111_0_item_2.set_width(lv.pct(100))
    menu_111_0_item_2_label = lv.label(menu_111_0_item_2)
    menu_111_0_item_2_label.set_text("Item 2")
    menu_111_0_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_111_0_item_3 = lv.button(menu_111_0)
    menu_111_0_item_3.set_width(lv.pct(100))
    menu_111_0_item_3_label = lv.label(menu_111_0_item_3)
    menu_111_0_item_3_label.set_text("Item 3")
    menu_111_0_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_111_0_item_4 = lv.button(menu_111_0)
    menu_111_0_item_4.set_width(lv.pct(100))
    menu_111_0_item_4_label = lv.label(menu_111_0_item_4)
    menu_111_0_item_4_label.set_text("Item 4")
    menu_111_0_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # line: line_111_1
    line_111_1 = lv.line(parent)
    objects["line_111_1"] = line_111_1
    line_111_1.set_pos(478, 221)
    line_111_1_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_111_1.set_points(line_111_1_points, 2)
    line_111_1.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_111_1.set_style_line_width(2, lv.PART.MAIN)

    # imagebutton: imagebutton_111_2
    imagebutton_111_2 = lv.imagebutton(parent)
    objects["imagebutton_111_2"] = imagebutton_111_2
    imagebutton_111_2.set_pos(312, 67)
    imagebutton_111_2.set_size(266, 127)
    imagebutton_111_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_111_2.set_style_radius(5, lv.PART.MAIN)
    imagebutton_111_2_label = lv.label(imagebutton_111_2)
    imagebutton_111_2_label.set_text("Testo 111:2 \" \\ Città")
    imagebutton_111_2_label.center()
    imagebutton_111_2_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_111_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # dropdown: dropdown_111_3
    dropdown_111_3 = lv.dropdown(parent)
    objects["dropdown_111_3"] = dropdown_111_3
    dropdown_111_3.set_pos(466, 167)
    dropdown_111_3.set_size(211, 37)
    dropdown_111_3.set_options("Option 1\nOption 2\nOption 3")
    dropdown_111_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_111_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_111_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # spinner: spinner_111_4
    spinner_111_4 = lv.arc(parent)
    objects["spinner_111_4"] = spinner_111_4
    spinner_111_4.set_pos(679, 396)
    spinner_111_4.set_size(46, 75)
    spinner_111_4.set_bg_angles(0, 360)
    spinner_111_4.set_angles(0, 60)
    spinner_111_4.remove_style(None, lv.PART.KNOB)
    spinner_111_4.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_111_4_anim = lv.anim_t()
    spinner_111_4_anim.init()
    spinner_111_4_anim.set_var(spinner_111_4)
    spinner_111_4_anim.set_values(0, 360)
    spinner_111_4_anim.set_duration(1000)
    spinner_111_4_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_111_4_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_111_4_anim.set_custom_exec_cb(lambda _anim, value: spinner_111_4.set_rotation(value))
    spinner_111_4_anim.start()
    spinner_111_4.set_style_arc_width(8, lv.PART.MAIN)
    spinner_111_4.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_111_4.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # bar: bar_111_5
    bar_111_5 = lv.bar(parent)
    objects["bar_111_5"] = bar_111_5
    bar_111_5.set_pos(267, 50)
    bar_111_5.set_size(133, 33)
    bar_111_5.set_range(0, 100)
    bar_111_5.set_value(50, False)
    bar_111_5.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_111_5.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)


def random_111_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_111_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_111_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_111_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_111_get_current_page():
    return current_screen

def random_111_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_111_load_page(0)
