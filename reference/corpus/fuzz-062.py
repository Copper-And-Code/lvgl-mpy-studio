"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 62
Generated: 2023-11-14T22:14:54.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_62_0_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_62_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # button: button_62_0
    button_62_0 = lv.button(parent)
    objects["button_62_0"] = button_62_0
    button_62_0.set_pos(143, 157)
    button_62_0.set_size(99, 117)
    button_62_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_62_0.set_style_radius(5, lv.PART.MAIN)
    button_62_0_label = lv.label(button_62_0)
    button_62_0_label.set_text("Testo 62:0 \" \\ Città")
    button_62_0_label.center()
    button_62_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_62_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_62_0.add_event_cb(button_62_0_changed, lv.EVENT.CLICKED, None)

    # bar: bar_62_1
    bar_62_1 = lv.bar(parent)
    objects["bar_62_1"] = bar_62_1
    bar_62_1.set_pos(513, 120)
    bar_62_1.set_size(31, 25)
    bar_62_1.set_range(0, 100)
    bar_62_1.set_value(50, False)
    bar_62_1.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_62_1.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # table: table_62_2
    table_62_2 = lv.table(parent)
    objects["table_62_2"] = table_62_2
    table_62_2.set_pos(646, 19)
    table_62_2.set_size(105, 63)
    table_62_2.set_column_count(3)
    table_62_2.set_column_width(0, 100)
    table_62_2.set_column_width(1, 100)
    table_62_2.set_column_width(2, 100)
    table_62_2.set_cell_value(0, 0, "Col 1")
    table_62_2.set_cell_value(0, 1, "Col 2")
    table_62_2.set_cell_value(0, 2, "Col 3")
    table_62_2.set_cell_value(1, 0, "A1")
    table_62_2.set_cell_value(1, 1, "B1")
    table_62_2.set_cell_value(1, 2, "C1")
    table_62_2.set_cell_value(2, 0, "A2")
    table_62_2.set_cell_value(2, 1, "B2")
    table_62_2.set_cell_value(2, 2, "C2")
    table_62_2.set_cell_value(3, 0, "A3")
    table_62_2.set_cell_value(3, 1, "B3")
    table_62_2.set_cell_value(3, 2, "C3")
    table_62_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_62_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_62_2.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_62_2.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # led: led_62_3
    led_62_3 = lv.led(parent)
    objects["led_62_3"] = led_62_3
    led_62_3.set_pos(155, 38)
    led_62_3.set_size(242, 121)
    led_62_3.set_color(lv.color_hex(0xFF0000))
    led_62_3.set_brightness(255)


def random_62_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_62_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_62_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_62_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_62_get_current_page():
    return current_screen

def random_62_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_62_load_page(0)
