"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 118
Generated: 2023-11-14T22:15:50.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def button_118_4_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_118_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tileview: tileview_118_0
    tileview_118_0 = lv.tileview(parent)
    objects["tileview_118_0"] = tileview_118_0
    tileview_118_0.set_pos(439, 63)
    tileview_118_0.set_size(26, 106)
    tileview_118_0.add_tile(0, 0, lv.DIR.ALL)
    tileview_118_0.add_tile(1, 0, lv.DIR.ALL)
    tileview_118_0.add_tile(0, 1, lv.DIR.ALL)
    tileview_118_0.add_tile(1, 1, lv.DIR.ALL)
    tileview_118_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # spinner: spinner_118_1
    spinner_118_1 = lv.arc(parent)
    objects["spinner_118_1"] = spinner_118_1
    spinner_118_1.set_pos(175, 354)
    spinner_118_1.set_size(208, 60)
    spinner_118_1.set_bg_angles(0, 360)
    spinner_118_1.set_angles(0, 60)
    spinner_118_1.remove_style(None, lv.PART.KNOB)
    spinner_118_1.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_118_1_anim = lv.anim_t()
    spinner_118_1_anim.init()
    spinner_118_1_anim.set_var(spinner_118_1)
    spinner_118_1_anim.set_values(0, 360)
    spinner_118_1_anim.set_duration(1000)
    spinner_118_1_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_118_1_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_118_1_anim.set_custom_exec_cb(lambda _anim, value: spinner_118_1.set_rotation(value))
    spinner_118_1_anim.start()
    spinner_118_1.set_style_arc_width(8, lv.PART.MAIN)
    spinner_118_1.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_118_1.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # tileview: tileview_118_2
    tileview_118_2 = lv.tileview(parent)
    objects["tileview_118_2"] = tileview_118_2
    tileview_118_2.set_pos(137, 64)
    tileview_118_2.set_size(144, 46)
    tileview_118_2.add_tile(0, 0, lv.DIR.ALL)
    tileview_118_2.add_tile(1, 0, lv.DIR.ALL)
    tileview_118_2.add_tile(0, 1, lv.DIR.ALL)
    tileview_118_2.add_tile(1, 1, lv.DIR.ALL)
    tileview_118_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_118_3
    buttonmatrix_118_3 = lv.buttonmatrix(parent)
    objects["buttonmatrix_118_3"] = buttonmatrix_118_3
    buttonmatrix_118_3.set_pos(344, 211)
    buttonmatrix_118_3.set_size(207, 75)
    buttonmatrix_118_3_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_118_3.set_map(buttonmatrix_118_3_map)
    buttonmatrix_118_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_118_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_118_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_118_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # button: button_118_4
    button_118_4 = lv.button(parent)
    objects["button_118_4"] = button_118_4
    button_118_4.set_pos(374, 134)
    button_118_4.set_size(253, 17)
    button_118_4.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_118_4.set_style_radius(5, lv.PART.MAIN)
    button_118_4_label = lv.label(button_118_4)
    button_118_4_label.set_text("Testo 118:4 \" \\ Città")
    button_118_4_label.center()
    button_118_4_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_118_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_118_4.add_event_cb(button_118_4_changed, lv.EVENT.CLICKED, None)

    # msgbox: msgbox_118_5
    msgbox_118_5 = lv.msgbox(parent)
    objects["msgbox_118_5"] = msgbox_118_5
    msgbox_118_5.set_pos(190, 143)
    msgbox_118_5.set_size(55, 43)
    msgbox_118_5_title = msgbox_118_5.add_title("Notice")
    msgbox_118_5_text = msgbox_118_5.add_text("Testo 118:5 \" \\ Città")
    msgbox_118_5_button_1 = msgbox_118_5.add_footer_button("OK")
    msgbox_118_5_button_2 = msgbox_118_5.add_footer_button("Cancel")
    msgbox_118_5_close = msgbox_118_5.add_close_button()
    msgbox_118_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # calendar: calendar_118_6
    calendar_118_6 = lv.calendar(parent)
    objects["calendar_118_6"] = calendar_118_6
    calendar_118_6.set_pos(575, 211)
    calendar_118_6.set_size(266, 142)
    calendar_118_6.set_today_date(2026, 10, 28)
    calendar_118_6.set_month_shown(2026, 10)
    calendar_118_6_header = calendar_118_6.add_header_arrow()
    calendar_118_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # tabview: tabview_118_7
    tabview_118_7 = lv.tabview(parent)
    objects["tabview_118_7"] = tabview_118_7
    tabview_118_7.set_pos(273, 21)
    tabview_118_7.set_size(87, 120)
    tabview_118_7.set_tab_bar_position(lv.DIR.TOP)
    tabview_118_7.set_tab_bar_size(40)
    tabview_118_7_tab_1 = tabview_118_7.add_tab("Tab 1")
    tabview_118_7_tab_2 = tabview_118_7.add_tab("Tab 2")
    tabview_118_7_tab_3 = tabview_118_7.add_tab("Tab 3")
    tabview_118_7.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_118_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_118_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_118_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_118_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_118_get_current_page():
    return current_screen

def random_118_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_118_load_page(0)
