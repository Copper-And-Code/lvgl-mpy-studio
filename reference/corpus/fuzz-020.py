"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 20
Generated: 2023-11-14T22:14:12.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def textarea_20_0_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

def checkbox_20_1_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_20_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # textarea: textarea_20_0
    textarea_20_0 = lv.textarea(parent)
    objects["textarea_20_0"] = textarea_20_0
    textarea_20_0.set_pos(2, 244)
    textarea_20_0.set_size(172, 72)
    textarea_20_0.set_text("Testo 20:0 \" \\ Città")
    textarea_20_0.set_placeholder_text("Type here")
    textarea_20_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_20_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_20_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    textarea_20_0.add_event_cb(textarea_20_0_changed, lv.EVENT.VALUE_CHANGED, None)

    # checkbox: checkbox_20_1
    checkbox_20_1 = lv.checkbox(parent)
    objects["checkbox_20_1"] = checkbox_20_1
    checkbox_20_1.set_pos(297, 128)
    checkbox_20_1.set_text("Testo 20:1 \" \\ Città")
    checkbox_20_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_20_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_20_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_20_1.add_event_cb(checkbox_20_1_changed, lv.EVENT.VALUE_CHANGED, None)

    # tabview: tabview_20_2
    tabview_20_2 = lv.tabview(parent)
    objects["tabview_20_2"] = tabview_20_2
    tabview_20_2.set_pos(230, 70)
    tabview_20_2.set_size(46, 126)
    tabview_20_2.set_tab_bar_position(lv.DIR.TOP)
    tabview_20_2.set_tab_bar_size(40)
    tabview_20_2_tab_1 = tabview_20_2.add_tab("Tab 1")
    tabview_20_2_tab_2 = tabview_20_2.add_tab("Tab 2")
    tabview_20_2_tab_3 = tabview_20_2.add_tab("Tab 3")
    tabview_20_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # keyboard: keyboard_20_3
    keyboard_20_3 = lv.keyboard(parent)
    objects["keyboard_20_3"] = keyboard_20_3
    keyboard_20_3.set_pos(11, 345)
    keyboard_20_3.set_size(171, 154)

    # menu: menu_20_4
    menu_20_4 = lv.obj(parent)
    objects["menu_20_4"] = menu_20_4
    menu_20_4.set_pos(306, 367)
    menu_20_4.set_size(132, 31)
    menu_20_4.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_20_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_20_4_title = lv.label(menu_20_4)
    menu_20_4_title.set_text("Menu")
    menu_20_4_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_20_4_item_1 = lv.button(menu_20_4)
    menu_20_4_item_1.set_width(lv.pct(100))
    menu_20_4_item_1_label = lv.label(menu_20_4_item_1)
    menu_20_4_item_1_label.set_text("Item 1")
    menu_20_4_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_20_4_item_2 = lv.button(menu_20_4)
    menu_20_4_item_2.set_width(lv.pct(100))
    menu_20_4_item_2_label = lv.label(menu_20_4_item_2)
    menu_20_4_item_2_label.set_text("Item 2")
    menu_20_4_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_20_4_item_3 = lv.button(menu_20_4)
    menu_20_4_item_3.set_width(lv.pct(100))
    menu_20_4_item_3_label = lv.label(menu_20_4_item_3)
    menu_20_4_item_3_label.set_text("Item 3")
    menu_20_4_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_20_4_item_4 = lv.button(menu_20_4)
    menu_20_4_item_4.set_width(lv.pct(100))
    menu_20_4_item_4_label = lv.label(menu_20_4_item_4)
    menu_20_4_item_4_label.set_text("Item 4")
    menu_20_4_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # win: win_20_5
    win_20_5 = lv.obj(parent)
    objects["win_20_5"] = win_20_5
    win_20_5.set_pos(232, 329)
    win_20_5.set_size(213, 76)
    win_20_5.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_20_5.set_style_pad_all(0, lv.PART.MAIN)
    win_20_5.set_style_pad_row(0, lv.PART.MAIN)
    win_20_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_20_5_header = lv.obj(win_20_5)
    win_20_5_header.set_size(lv.pct(100), 40)
    win_20_5_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_20_5_header.set_style_radius(0, lv.PART.MAIN)
    win_20_5_title = lv.label(win_20_5_header)
    win_20_5_title.set_text("Window Title")
    win_20_5_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_20_5_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_20_5_content = lv.obj(win_20_5)
    win_20_5_content.set_width(lv.pct(100))
    win_20_5_content.set_flex_grow(1)

    # line: line_20_6
    line_20_6 = lv.line(parent)
    objects["line_20_6"] = line_20_6
    line_20_6.set_pos(237, 27)
    line_20_6_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_20_6.set_points(line_20_6_points, 2)
    line_20_6.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_20_6.set_style_line_width(2, lv.PART.MAIN)

    # span: span_20_7
    span_20_7 = lv.spangroup(parent)
    objects["span_20_7"] = span_20_7
    span_20_7.set_pos(367, 0)
    span_20_7.set_size(52, 12)
    span_20_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_20_7_span_1 = span_20_7.add_span()
    span_20_7_span_1.set_text("Normal text")
    span_20_7_span_1_style = span_20_7_span_1.get_style()
    span_20_7_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_20_7_span_1_style.set_text_font(lv.font_montserrat_14)
    span_20_7_span_2 = span_20_7.add_span()
    span_20_7_span_2.set_text("Bold text")
    span_20_7_span_2_style = span_20_7_span_2.get_style()
    span_20_7_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_20_7_span_2_style.set_text_font(lv.font_montserrat_16)
    span_20_7_span_3 = span_20_7.add_span()
    span_20_7_span_3.set_text("Small text")
    span_20_7_span_3_style = span_20_7_span_3.get_style()
    span_20_7_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_20_7_span_3_style.set_text_font(lv.font_montserrat_14)
    span_20_7.refresh()


def random_20_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_20_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_20_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_20_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_20_get_current_page():
    return current_screen

def random_20_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_20_load_page(0)
