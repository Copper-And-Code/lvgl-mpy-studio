"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 193
Generated: 2023-11-14T22:17:05.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_193_4_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # TODO: handle lv.EVENT.CLICKED
        pass

screens = [None] * 1
current_screen = 0

def random_193_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # label: label_193_0
    label_193_0 = lv.label(parent)
    objects["label_193_0"] = label_193_0
    label_193_0.set_pos(346, 266)
    label_193_0.set_size(225, 117)
    label_193_0.set_text("Testo 193:0 \" \\ Città")
    label_193_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_193_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_193_0.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # table: table_193_1
    table_193_1 = lv.table(parent)
    objects["table_193_1"] = table_193_1
    table_193_1.set_pos(59, 253)
    table_193_1.set_size(36, 13)
    table_193_1.set_column_count(3)
    table_193_1.set_column_width(0, 100)
    table_193_1.set_column_width(1, 100)
    table_193_1.set_column_width(2, 100)
    table_193_1.set_cell_value(0, 0, "Col 1")
    table_193_1.set_cell_value(0, 1, "Col 2")
    table_193_1.set_cell_value(0, 2, "Col 3")
    table_193_1.set_cell_value(1, 0, "A1")
    table_193_1.set_cell_value(1, 1, "B1")
    table_193_1.set_cell_value(1, 2, "C1")
    table_193_1.set_cell_value(2, 0, "A2")
    table_193_1.set_cell_value(2, 1, "B2")
    table_193_1.set_cell_value(2, 2, "C2")
    table_193_1.set_cell_value(3, 0, "A3")
    table_193_1.set_cell_value(3, 1, "B3")
    table_193_1.set_cell_value(3, 2, "C3")
    table_193_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_193_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_193_1.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_193_1.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # msgbox: msgbox_193_2
    msgbox_193_2 = lv.msgbox(parent)
    objects["msgbox_193_2"] = msgbox_193_2
    msgbox_193_2.set_pos(352, 130)
    msgbox_193_2.set_size(219, 147)
    msgbox_193_2_title = msgbox_193_2.add_title("Notice")
    msgbox_193_2_text = msgbox_193_2.add_text("Testo 193:2 \" \\ Città")
    msgbox_193_2_button_1 = msgbox_193_2.add_footer_button("OK")
    msgbox_193_2_button_2 = msgbox_193_2.add_footer_button("Cancel")
    msgbox_193_2_close = msgbox_193_2.add_close_button()
    msgbox_193_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # spinner: spinner_193_3
    spinner_193_3 = lv.arc(parent)
    objects["spinner_193_3"] = spinner_193_3
    spinner_193_3.set_pos(65, 330)
    spinner_193_3.set_size(255, 110)
    spinner_193_3.set_bg_angles(0, 360)
    spinner_193_3.set_angles(0, 60)
    spinner_193_3.remove_style(None, lv.PART.KNOB)
    spinner_193_3.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_193_3_anim = lv.anim_t()
    spinner_193_3_anim.init()
    spinner_193_3_anim.set_var(spinner_193_3)
    spinner_193_3_anim.set_values(0, 360)
    spinner_193_3_anim.set_duration(1000)
    spinner_193_3_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_193_3_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_193_3_anim.set_custom_exec_cb(lambda _anim, value: spinner_193_3.set_rotation(value))
    spinner_193_3_anim.start()
    spinner_193_3.set_style_arc_width(8, lv.PART.MAIN)
    spinner_193_3.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_193_3.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # button: button_193_4
    button_193_4 = lv.button(parent)
    objects["button_193_4"] = button_193_4
    button_193_4.set_pos(519, 202)
    button_193_4.set_size(153, 148)
    button_193_4.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_193_4.set_style_radius(5, lv.PART.MAIN)
    button_193_4_label = lv.label(button_193_4)
    button_193_4_label.set_text("Testo 193:4 \" \\ Città")
    button_193_4_label.center()
    button_193_4_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_193_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_193_4.add_event_cb(button_193_4_changed, lv.EVENT.CLICKED, None)


def random_193_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_193_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_193_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_193_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_193_get_current_page():
    return current_screen

def random_193_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_193_load_page(0)
