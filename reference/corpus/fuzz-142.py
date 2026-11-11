"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 142
Generated: 2023-11-14T22:16:14.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_142_0_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # TODO: handle lv.EVENT.CLICKED
        pass

screens = [None] * 1
current_screen = 0

def random_142_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # button: button_142_0
    button_142_0 = lv.button(parent)
    objects["button_142_0"] = button_142_0
    button_142_0.set_pos(398, 132)
    button_142_0.set_size(128, 37)
    button_142_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_142_0.set_style_radius(5, lv.PART.MAIN)
    button_142_0_label = lv.label(button_142_0)
    button_142_0_label.set_text("Testo 142:0 \" \\ Città")
    button_142_0_label.center()
    button_142_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_142_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_142_0.add_event_cb(button_142_0_changed, lv.EVENT.CLICKED, None)

    # table: table_142_1
    table_142_1 = lv.table(parent)
    objects["table_142_1"] = table_142_1
    table_142_1.set_pos(36, 100)
    table_142_1.set_size(261, 100)
    table_142_1.set_column_count(3)
    table_142_1.set_column_width(0, 100)
    table_142_1.set_column_width(1, 100)
    table_142_1.set_column_width(2, 100)
    table_142_1.set_cell_value(0, 0, "Col 1")
    table_142_1.set_cell_value(0, 1, "Col 2")
    table_142_1.set_cell_value(0, 2, "Col 3")
    table_142_1.set_cell_value(1, 0, "A1")
    table_142_1.set_cell_value(1, 1, "B1")
    table_142_1.set_cell_value(1, 2, "C1")
    table_142_1.set_cell_value(2, 0, "A2")
    table_142_1.set_cell_value(2, 1, "B2")
    table_142_1.set_cell_value(2, 2, "C2")
    table_142_1.set_cell_value(3, 0, "A3")
    table_142_1.set_cell_value(3, 1, "B3")
    table_142_1.set_cell_value(3, 2, "C3")
    table_142_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_142_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_142_1.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_142_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # span: span_142_2
    span_142_2 = lv.spangroup(parent)
    objects["span_142_2"] = span_142_2
    span_142_2.set_pos(422, 336)
    span_142_2.set_size(105, 122)
    span_142_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_142_2_span_1 = span_142_2.add_span()
    span_142_2_span_1.set_text("Normal text")
    span_142_2_span_1_style = span_142_2_span_1.get_style()
    span_142_2_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_142_2_span_1_style.set_text_font(lv.font_montserrat_14)
    span_142_2_span_2 = span_142_2.add_span()
    span_142_2_span_2.set_text("Bold text")
    span_142_2_span_2_style = span_142_2_span_2.get_style()
    span_142_2_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_142_2_span_2_style.set_text_font(lv.font_montserrat_16)
    span_142_2_span_3 = span_142_2.add_span()
    span_142_2_span_3.set_text("Small text")
    span_142_2_span_3_style = span_142_2_span_3.get_style()
    span_142_2_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_142_2_span_3_style.set_text_font(lv.font_montserrat_14)
    span_142_2.refresh()


def random_142_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_142_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_142_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_142_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_142_get_current_page():
    return current_screen

def random_142_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_142_load_page(0)
