"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 83
Generated: 2023-11-14T22:15:15.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_83_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # textarea: textarea_83_0
    textarea_83_0 = lv.textarea(parent)
    objects["textarea_83_0"] = textarea_83_0
    textarea_83_0.set_pos(7, 187)
    textarea_83_0.set_size(211, 34)
    textarea_83_0.set_text("Testo 83:0 \" \\ Città")
    textarea_83_0.set_placeholder_text("Type here")
    textarea_83_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_83_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_83_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # span: span_83_1
    span_83_1 = lv.spangroup(parent)
    objects["span_83_1"] = span_83_1
    span_83_1.set_pos(337, 58)
    span_83_1.set_size(247, 123)
    span_83_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_83_1_span_1 = span_83_1.add_span()
    span_83_1_span_1.set_text("Normal text")
    span_83_1_span_1_style = span_83_1_span_1.get_style()
    span_83_1_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_83_1_span_1_style.set_text_font(lv.font_montserrat_14)
    span_83_1_span_2 = span_83_1.add_span()
    span_83_1_span_2.set_text("Bold text")
    span_83_1_span_2_style = span_83_1_span_2.get_style()
    span_83_1_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_83_1_span_2_style.set_text_font(lv.font_montserrat_16)
    span_83_1_span_3 = span_83_1.add_span()
    span_83_1_span_3.set_text("Small text")
    span_83_1_span_3_style = span_83_1_span_3.get_style()
    span_83_1_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_83_1_span_3_style.set_text_font(lv.font_montserrat_14)
    span_83_1.refresh()

    # line: line_83_2
    line_83_2 = lv.line(parent)
    objects["line_83_2"] = line_83_2
    line_83_2.set_pos(600, 47)
    line_83_2_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_83_2.set_points(line_83_2_points, 2)
    line_83_2.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_83_2.set_style_line_width(2, lv.PART.MAIN)

    # msgbox: msgbox_83_3
    msgbox_83_3 = lv.msgbox(parent)
    objects["msgbox_83_3"] = msgbox_83_3
    msgbox_83_3.set_pos(585, 26)
    msgbox_83_3.set_size(239, 125)
    msgbox_83_3_title = msgbox_83_3.add_title("Notice")
    msgbox_83_3_text = msgbox_83_3.add_text("Testo 83:3 \" \\ Città")
    msgbox_83_3_button_1 = msgbox_83_3.add_footer_button("OK")
    msgbox_83_3_button_2 = msgbox_83_3.add_footer_button("Cancel")
    msgbox_83_3_close = msgbox_83_3.add_close_button()
    msgbox_83_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # tabview: tabview_83_4
    tabview_83_4 = lv.tabview(parent)
    objects["tabview_83_4"] = tabview_83_4
    tabview_83_4.set_pos(585, 250)
    tabview_83_4.set_size(263, 88)
    tabview_83_4.set_tab_bar_position(lv.DIR.TOP)
    tabview_83_4.set_tab_bar_size(40)
    tabview_83_4_tab_1 = tabview_83_4.add_tab("Tab 1")
    tabview_83_4_tab_2 = tabview_83_4.add_tab("Tab 2")
    tabview_83_4_tab_3 = tabview_83_4.add_tab("Tab 3")
    tabview_83_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # imagebutton: imagebutton_83_5
    imagebutton_83_5 = lv.imagebutton(parent)
    objects["imagebutton_83_5"] = imagebutton_83_5
    imagebutton_83_5.set_pos(484, 348)
    imagebutton_83_5.set_size(198, 74)
    imagebutton_83_5.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_83_5.set_style_radius(5, lv.PART.MAIN)
    imagebutton_83_5_label = lv.label(imagebutton_83_5)
    imagebutton_83_5_label.set_text("Testo 83:5 \" \\ Città")
    imagebutton_83_5_label.center()
    imagebutton_83_5_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_83_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_83_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_83_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_83_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_83_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_83_get_current_page():
    return current_screen

def random_83_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_83_load_page(0)
