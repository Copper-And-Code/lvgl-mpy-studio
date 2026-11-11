"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 180
Generated: 2023-11-14T22:16:52.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_180_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # spinner: spinner_180_0
    spinner_180_0 = lv.arc(parent)
    objects["spinner_180_0"] = spinner_180_0
    spinner_180_0.set_pos(475, 167)
    spinner_180_0.set_size(234, 98)
    spinner_180_0.set_bg_angles(0, 360)
    spinner_180_0.set_angles(0, 60)
    spinner_180_0.remove_style(None, lv.PART.KNOB)
    spinner_180_0.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_180_0_anim = lv.anim_t()
    spinner_180_0_anim.init()
    spinner_180_0_anim.set_var(spinner_180_0)
    spinner_180_0_anim.set_values(0, 360)
    spinner_180_0_anim.set_duration(1000)
    spinner_180_0_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_180_0_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_180_0_anim.set_custom_exec_cb(lambda _anim, value: spinner_180_0.set_rotation(value))
    spinner_180_0_anim.start()
    spinner_180_0.set_style_arc_width(8, lv.PART.MAIN)
    spinner_180_0.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_180_0.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # keyboard: keyboard_180_1
    keyboard_180_1 = lv.keyboard(parent)
    objects["keyboard_180_1"] = keyboard_180_1
    keyboard_180_1.set_pos(181, 46)
    keyboard_180_1.set_size(89, 21)

    # win: win_180_2
    win_180_2 = lv.obj(parent)
    objects["win_180_2"] = win_180_2
    win_180_2.set_pos(254, 184)
    win_180_2.set_size(123, 132)
    win_180_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_180_2.set_style_pad_all(0, lv.PART.MAIN)
    win_180_2.set_style_pad_row(0, lv.PART.MAIN)
    win_180_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_180_2_header = lv.obj(win_180_2)
    win_180_2_header.set_size(lv.pct(100), 40)
    win_180_2_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_180_2_header.set_style_radius(0, lv.PART.MAIN)
    win_180_2_title = lv.label(win_180_2_header)
    win_180_2_title.set_text("Window Title")
    win_180_2_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_180_2_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_180_2_content = lv.obj(win_180_2)
    win_180_2_content.set_width(lv.pct(100))
    win_180_2_content.set_flex_grow(1)

    # imagebutton: imagebutton_180_3
    imagebutton_180_3 = lv.imagebutton(parent)
    objects["imagebutton_180_3"] = imagebutton_180_3
    imagebutton_180_3.set_pos(190, 60)
    imagebutton_180_3.set_size(83, 16)
    imagebutton_180_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_180_3.set_style_radius(5, lv.PART.MAIN)
    imagebutton_180_3_label = lv.label(imagebutton_180_3)
    imagebutton_180_3_label.set_text("Testo 180:3 \" \\ Città")
    imagebutton_180_3_label.center()
    imagebutton_180_3_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_180_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_180_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_180_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_180_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_180_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_180_get_current_page():
    return current_screen

def random_180_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_180_load_page(0)
