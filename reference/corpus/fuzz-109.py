"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 109
Generated: 2023-11-14T22:15:41.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_109_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # scale: scale_109_0
    scale_109_0 = lv.scale(parent)
    objects["scale_109_0"] = scale_109_0
    scale_109_0.set_pos(347, 257)
    scale_109_0.set_size(123, 19)
    scale_109_0.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_109_0.set_range(0, 100)
    scale_109_0.set_total_tick_count(51)
    scale_109_0.set_major_tick_every(5)
    scale_109_0.set_style_length(15, lv.PART.INDICATOR)
    scale_109_0.set_style_length(8, lv.PART.ITEMS)
    scale_109_0.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_109_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # led: led_109_1
    led_109_1 = lv.led(parent)
    objects["led_109_1"] = led_109_1
    led_109_1.set_pos(497, 19)
    led_109_1.set_size(55, 33)
    led_109_1.set_color(lv.color_hex(0xFF0000))
    led_109_1.set_brightness(255)

    # win: win_109_2
    win_109_2 = lv.obj(parent)
    objects["win_109_2"] = win_109_2
    win_109_2.set_pos(410, 72)
    win_109_2.set_size(168, 57)
    win_109_2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_109_2.set_style_pad_all(0, lv.PART.MAIN)
    win_109_2.set_style_pad_row(0, lv.PART.MAIN)
    win_109_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_109_2_header = lv.obj(win_109_2)
    win_109_2_header.set_size(lv.pct(100), 40)
    win_109_2_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_109_2_header.set_style_radius(0, lv.PART.MAIN)
    win_109_2_title = lv.label(win_109_2_header)
    win_109_2_title.set_text("Window Title")
    win_109_2_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_109_2_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_109_2_content = lv.obj(win_109_2)
    win_109_2_content.set_width(lv.pct(100))
    win_109_2_content.set_flex_grow(1)

    # textarea: textarea_109_3
    textarea_109_3 = lv.textarea(parent)
    objects["textarea_109_3"] = textarea_109_3
    textarea_109_3.set_pos(435, 39)
    textarea_109_3.set_size(22, 86)
    textarea_109_3.set_text("Testo 109:3 \" \\ Città")
    textarea_109_3.set_placeholder_text("Type here")
    textarea_109_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_109_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_109_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # spinner: spinner_109_4
    spinner_109_4 = lv.arc(parent)
    objects["spinner_109_4"] = spinner_109_4
    spinner_109_4.set_pos(674, 4)
    spinner_109_4.set_size(236, 18)
    spinner_109_4.set_bg_angles(0, 360)
    spinner_109_4.set_angles(0, 60)
    spinner_109_4.remove_style(None, lv.PART.KNOB)
    spinner_109_4.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_109_4_anim = lv.anim_t()
    spinner_109_4_anim.init()
    spinner_109_4_anim.set_var(spinner_109_4)
    spinner_109_4_anim.set_values(0, 360)
    spinner_109_4_anim.set_duration(1000)
    spinner_109_4_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_109_4_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_109_4_anim.set_custom_exec_cb(lambda _anim, value: spinner_109_4.set_rotation(value))
    spinner_109_4_anim.start()
    spinner_109_4.set_style_arc_width(8, lv.PART.MAIN)
    spinner_109_4.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_109_4.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)


def random_109_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_109_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_109_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_109_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_109_get_current_page():
    return current_screen

def random_109_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_109_load_page(0)
