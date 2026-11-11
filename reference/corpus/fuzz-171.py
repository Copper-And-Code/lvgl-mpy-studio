"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 171
Generated: 2023-11-14T22:16:43.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_171_0_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_171_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # slider: slider_171_0
    slider_171_0 = lv.slider(parent)
    objects["slider_171_0"] = slider_171_0
    slider_171_0.set_pos(694, 353)
    slider_171_0.set_size(190, 33)
    slider_171_0.set_range(0, 100)
    slider_171_0.set_value(50, False)
    slider_171_0.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_171_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_171_0.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_171_0.add_event_cb(slider_171_0_changed, lv.EVENT.VALUE_CHANGED, None)

    # spinner: spinner_171_1
    spinner_171_1 = lv.arc(parent)
    objects["spinner_171_1"] = spinner_171_1
    spinner_171_1.set_pos(446, 211)
    spinner_171_1.set_size(196, 144)
    spinner_171_1.set_bg_angles(0, 360)
    spinner_171_1.set_angles(0, 60)
    spinner_171_1.remove_style(None, lv.PART.KNOB)
    spinner_171_1.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_171_1_anim = lv.anim_t()
    spinner_171_1_anim.init()
    spinner_171_1_anim.set_var(spinner_171_1)
    spinner_171_1_anim.set_values(0, 360)
    spinner_171_1_anim.set_duration(1000)
    spinner_171_1_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_171_1_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_171_1_anim.set_custom_exec_cb(lambda _anim, value: spinner_171_1.set_rotation(value))
    spinner_171_1_anim.start()
    spinner_171_1.set_style_arc_width(8, lv.PART.MAIN)
    spinner_171_1.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_171_1.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # msgbox: msgbox_171_2
    msgbox_171_2 = lv.msgbox(parent)
    objects["msgbox_171_2"] = msgbox_171_2
    msgbox_171_2.set_pos(0, 30)
    msgbox_171_2.set_size(84, 33)
    msgbox_171_2_title = msgbox_171_2.add_title("Notice")
    msgbox_171_2_text = msgbox_171_2.add_text("Testo 171:2 \" \\ Città")
    msgbox_171_2_button_1 = msgbox_171_2.add_footer_button("OK")
    msgbox_171_2_button_2 = msgbox_171_2.add_footer_button("Cancel")
    msgbox_171_2_close = msgbox_171_2.add_close_button()
    msgbox_171_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # bar: bar_171_3
    bar_171_3 = lv.bar(parent)
    objects["bar_171_3"] = bar_171_3
    bar_171_3.set_pos(206, 330)
    bar_171_3.set_size(48, 150)
    bar_171_3.set_range(0, 100)
    bar_171_3.set_value(50, False)
    bar_171_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_171_3.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # dropdown: dropdown_171_4
    dropdown_171_4 = lv.dropdown(parent)
    objects["dropdown_171_4"] = dropdown_171_4
    dropdown_171_4.set_pos(34, 14)
    dropdown_171_4.set_size(223, 63)
    dropdown_171_4.set_options("Option 1\nOption 2\nOption 3")
    dropdown_171_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_171_4.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_171_4.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # label: label_171_5
    label_171_5 = lv.label(parent)
    objects["label_171_5"] = label_171_5
    label_171_5.set_pos(328, 280)
    label_171_5.set_size(88, 67)
    label_171_5.set_text("Testo 171:5 \" \\ Città")
    label_171_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_171_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_171_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)


def random_171_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_171_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_171_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_171_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_171_get_current_page():
    return current_screen

def random_171_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_171_load_page(0)
