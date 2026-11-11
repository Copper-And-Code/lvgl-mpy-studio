"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 30
Generated: 2023-11-14T22:14:22.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_30_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # imagebutton: imagebutton_30_0
    imagebutton_30_0 = lv.imagebutton(parent)
    objects["imagebutton_30_0"] = imagebutton_30_0
    imagebutton_30_0.set_pos(343, 312)
    imagebutton_30_0.set_size(260, 95)
    imagebutton_30_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_30_0.set_style_radius(5, lv.PART.MAIN)
    imagebutton_30_0_label = lv.label(imagebutton_30_0)
    imagebutton_30_0_label.set_text("Testo 30:0 \" \\ Città")
    imagebutton_30_0_label.center()
    imagebutton_30_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_30_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # imagebutton: imagebutton_30_1
    imagebutton_30_1 = lv.imagebutton(parent)
    objects["imagebutton_30_1"] = imagebutton_30_1
    imagebutton_30_1.set_pos(125, 312)
    imagebutton_30_1.set_size(20, 147)
    imagebutton_30_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_30_1.set_style_radius(5, lv.PART.MAIN)
    imagebutton_30_1_label = lv.label(imagebutton_30_1)
    imagebutton_30_1_label.set_text("Testo 30:1 \" \\ Città")
    imagebutton_30_1_label.center()
    imagebutton_30_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_30_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # spinner: spinner_30_2
    spinner_30_2 = lv.arc(parent)
    objects["spinner_30_2"] = spinner_30_2
    spinner_30_2.set_pos(588, 4)
    spinner_30_2.set_size(205, 92)
    spinner_30_2.set_bg_angles(0, 360)
    spinner_30_2.set_angles(0, 60)
    spinner_30_2.remove_style(None, lv.PART.KNOB)
    spinner_30_2.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_30_2_anim = lv.anim_t()
    spinner_30_2_anim.init()
    spinner_30_2_anim.set_var(spinner_30_2)
    spinner_30_2_anim.set_values(0, 360)
    spinner_30_2_anim.set_duration(1000)
    spinner_30_2_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_30_2_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_30_2_anim.set_custom_exec_cb(lambda _anim, value: spinner_30_2.set_rotation(value))
    spinner_30_2_anim.start()
    spinner_30_2.set_style_arc_width(8, lv.PART.MAIN)
    spinner_30_2.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_30_2.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_30_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_30_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_30_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_30_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_30_get_current_page():
    return current_screen

def random_30_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_30_load_page(0)
