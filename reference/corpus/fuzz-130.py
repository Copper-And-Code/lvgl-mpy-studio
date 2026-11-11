"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 130
Generated: 2023-11-14T22:16:02.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_130_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # msgbox: msgbox_130_0
    msgbox_130_0 = lv.msgbox(parent)
    objects["msgbox_130_0"] = msgbox_130_0
    msgbox_130_0.set_pos(200, 16)
    msgbox_130_0.set_size(138, 62)
    msgbox_130_0_title = msgbox_130_0.add_title("Notice")
    msgbox_130_0_text = msgbox_130_0.add_text("Testo 130:0 \" \\ Città")
    msgbox_130_0_button_1 = msgbox_130_0.add_footer_button("OK")
    msgbox_130_0_button_2 = msgbox_130_0.add_footer_button("Cancel")
    msgbox_130_0_close = msgbox_130_0.add_close_button()
    msgbox_130_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # spinner: spinner_130_1
    spinner_130_1 = lv.arc(parent)
    objects["spinner_130_1"] = spinner_130_1
    spinner_130_1.set_pos(51, 58)
    spinner_130_1.set_size(213, 47)
    spinner_130_1.set_bg_angles(0, 360)
    spinner_130_1.set_angles(0, 60)
    spinner_130_1.remove_style(None, lv.PART.KNOB)
    spinner_130_1.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_130_1_anim = lv.anim_t()
    spinner_130_1_anim.init()
    spinner_130_1_anim.set_var(spinner_130_1)
    spinner_130_1_anim.set_values(0, 360)
    spinner_130_1_anim.set_duration(1000)
    spinner_130_1_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_130_1_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_130_1_anim.set_custom_exec_cb(lambda _anim, value: spinner_130_1.set_rotation(value))
    spinner_130_1_anim.start()
    spinner_130_1.set_style_arc_width(8, lv.PART.MAIN)
    spinner_130_1.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_130_1.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_130_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_130_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_130_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_130_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_130_get_current_page():
    return current_screen

def random_130_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_130_load_page(0)
