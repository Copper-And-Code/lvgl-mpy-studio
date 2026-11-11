"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 163
Generated: 2023-11-14T22:16:35.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def textarea_163_3_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_163_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # imagebutton: imagebutton_163_0
    imagebutton_163_0 = lv.imagebutton(parent)
    objects["imagebutton_163_0"] = imagebutton_163_0
    imagebutton_163_0.set_pos(237, 286)
    imagebutton_163_0.set_size(246, 45)
    imagebutton_163_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_163_0.set_style_radius(5, lv.PART.MAIN)
    imagebutton_163_0_label = lv.label(imagebutton_163_0)
    imagebutton_163_0_label.set_text("Testo 163:0 \" \\ Città")
    imagebutton_163_0_label.center()
    imagebutton_163_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_163_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # chart: chart_163_1
    chart_163_1 = lv.chart(parent)
    objects["chart_163_1"] = chart_163_1
    chart_163_1.set_pos(420, 368)
    chart_163_1.set_size(24, 50)
    chart_163_1.set_type(lv.chart.TYPE.LINE)
    chart_163_1.set_point_count(10)
    chart_163_1.set_div_line_count(3, 5)
    chart_163_1.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_163_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_163_1_series_1 = chart_163_1.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_163_1.set_next_value(chart_163_1_series_1, 10)
    chart_163_1.set_next_value(chart_163_1_series_1, 20)
    chart_163_1.set_next_value(chart_163_1_series_1, 30)
    chart_163_1.set_next_value(chart_163_1_series_1, 25)
    chart_163_1.set_next_value(chart_163_1_series_1, 40)
    chart_163_1.set_next_value(chart_163_1_series_1, 35)
    chart_163_1.set_next_value(chart_163_1_series_1, 50)

    # keyboard: keyboard_163_2
    keyboard_163_2 = lv.keyboard(parent)
    objects["keyboard_163_2"] = keyboard_163_2
    keyboard_163_2.set_pos(320, 228)
    keyboard_163_2.set_size(258, 102)

    # textarea: textarea_163_3
    textarea_163_3 = lv.textarea(parent)
    objects["textarea_163_3"] = textarea_163_3
    textarea_163_3.set_pos(145, 106)
    textarea_163_3.set_size(119, 106)
    textarea_163_3.set_text("Testo 163:3 \" \\ Città")
    textarea_163_3.set_placeholder_text("Type here")
    textarea_163_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_163_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_163_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    textarea_163_3.add_event_cb(textarea_163_3_changed, lv.EVENT.VALUE_CHANGED, None)

    # image: image_163_4
    image_163_4 = lv.image(parent)
    objects["image_163_4"] = image_163_4
    image_163_4.set_pos(224, 280)
    image_163_4.set_size(138, 104)


def random_163_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_163_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_163_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_163_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_163_get_current_page():
    return current_screen

def random_163_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_163_load_page(0)
