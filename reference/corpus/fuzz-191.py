"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 191
Generated: 2023-11-14T22:17:03.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_191_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_191_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # checkbox: checkbox_191_0
    checkbox_191_0 = lv.checkbox(parent)
    objects["checkbox_191_0"] = checkbox_191_0
    checkbox_191_0.set_pos(122, 316)
    checkbox_191_0.set_text("Testo 191:0 \" \\ Città")
    checkbox_191_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_191_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_191_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)

    # button: button_191_1
    button_191_1 = lv.button(parent)
    objects["button_191_1"] = button_191_1
    button_191_1.set_pos(69, 398)
    button_191_1.set_size(130, 80)
    button_191_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_191_1.set_style_radius(5, lv.PART.MAIN)
    button_191_1_label = lv.label(button_191_1)
    button_191_1_label.set_text("Testo 191:1 \" \\ Città")
    button_191_1_label.center()
    button_191_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_191_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_191_1.add_event_cb(button_191_1_changed, lv.EVENT.CLICKED, None)

    # span: span_191_2
    span_191_2 = lv.spangroup(parent)
    objects["span_191_2"] = span_191_2
    span_191_2.set_pos(132, 91)
    span_191_2.set_size(258, 95)
    span_191_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_191_2_span_1 = span_191_2.add_span()
    span_191_2_span_1.set_text("Normal text")
    span_191_2_span_1_style = span_191_2_span_1.get_style()
    span_191_2_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_191_2_span_1_style.set_text_font(lv.font_montserrat_14)
    span_191_2_span_2 = span_191_2.add_span()
    span_191_2_span_2.set_text("Bold text")
    span_191_2_span_2_style = span_191_2_span_2.get_style()
    span_191_2_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_191_2_span_2_style.set_text_font(lv.font_montserrat_16)
    span_191_2_span_3 = span_191_2.add_span()
    span_191_2_span_3.set_text("Small text")
    span_191_2_span_3_style = span_191_2_span_3.get_style()
    span_191_2_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_191_2_span_3_style.set_text_font(lv.font_montserrat_14)
    span_191_2.refresh()

    # line: line_191_3
    line_191_3 = lv.line(parent)
    objects["line_191_3"] = line_191_3
    line_191_3.set_pos(383, 387)
    line_191_3_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_191_3.set_points(line_191_3_points, 2)
    line_191_3.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_191_3.set_style_line_width(2, lv.PART.MAIN)

    # led: led_191_4
    led_191_4 = lv.led(parent)
    objects["led_191_4"] = led_191_4
    led_191_4.set_pos(236, 151)
    led_191_4.set_size(65, 128)
    led_191_4.set_color(lv.color_hex(0xFF0000))
    led_191_4.set_brightness(255)

    # spinner: spinner_191_5
    spinner_191_5 = lv.arc(parent)
    objects["spinner_191_5"] = spinner_191_5
    spinner_191_5.set_pos(42, 31)
    spinner_191_5.set_size(54, 142)
    spinner_191_5.set_bg_angles(0, 360)
    spinner_191_5.set_angles(0, 60)
    spinner_191_5.remove_style(None, lv.PART.KNOB)
    spinner_191_5.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_191_5_anim = lv.anim_t()
    spinner_191_5_anim.init()
    spinner_191_5_anim.set_var(spinner_191_5)
    spinner_191_5_anim.set_values(0, 360)
    spinner_191_5_anim.set_duration(1000)
    spinner_191_5_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_191_5_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_191_5_anim.set_custom_exec_cb(lambda _anim, value: spinner_191_5.set_rotation(value))
    spinner_191_5_anim.start()
    spinner_191_5.set_style_arc_width(8, lv.PART.MAIN)
    spinner_191_5.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_191_5.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # win: win_191_6
    win_191_6 = lv.obj(parent)
    objects["win_191_6"] = win_191_6
    win_191_6.set_pos(302, 144)
    win_191_6.set_size(157, 35)
    win_191_6.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_191_6.set_style_pad_all(0, lv.PART.MAIN)
    win_191_6.set_style_pad_row(0, lv.PART.MAIN)
    win_191_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_191_6_header = lv.obj(win_191_6)
    win_191_6_header.set_size(lv.pct(100), 40)
    win_191_6_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_191_6_header.set_style_radius(0, lv.PART.MAIN)
    win_191_6_title = lv.label(win_191_6_header)
    win_191_6_title.set_text("Window Title")
    win_191_6_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_191_6_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_191_6_content = lv.obj(win_191_6)
    win_191_6_content.set_width(lv.pct(100))
    win_191_6_content.set_flex_grow(1)


def random_191_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_191_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_191_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_191_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_191_get_current_page():
    return current_screen

def random_191_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_191_load_page(0)
