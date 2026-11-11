"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 194
Generated: 2023-11-14T22:17:06.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def textarea_194_3_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # TODO: handle lv.EVENT.VALUE_CHANGED
        pass

screens = [None] * 1
current_screen = 0

def random_194_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # roller: roller_194_0
    roller_194_0 = lv.roller(parent)
    objects["roller_194_0"] = roller_194_0
    roller_194_0.set_pos(62, 140)
    roller_194_0.set_size(257, 117)
    roller_194_0.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.NORMAL)
    roller_194_0.set_visible_row_count(3)
    roller_194_0.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_194_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_194_0.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_194_0.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # msgbox: msgbox_194_1
    msgbox_194_1 = lv.msgbox(parent)
    objects["msgbox_194_1"] = msgbox_194_1
    msgbox_194_1.set_pos(287, 107)
    msgbox_194_1.set_size(262, 141)
    msgbox_194_1_title = msgbox_194_1.add_title("Notice")
    msgbox_194_1_text = msgbox_194_1.add_text("Testo 194:1 \" \\ Città")
    msgbox_194_1_button_1 = msgbox_194_1.add_footer_button("OK")
    msgbox_194_1_button_2 = msgbox_194_1.add_footer_button("Cancel")
    msgbox_194_1_close = msgbox_194_1.add_close_button()
    msgbox_194_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # chart: chart_194_2
    chart_194_2 = lv.chart(parent)
    objects["chart_194_2"] = chart_194_2
    chart_194_2.set_pos(374, 273)
    chart_194_2.set_size(118, 106)
    chart_194_2.set_type(lv.chart.TYPE.LINE)
    chart_194_2.set_point_count(10)
    chart_194_2.set_div_line_count(3, 5)
    chart_194_2.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_194_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_194_2_series_1 = chart_194_2.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_194_2.set_next_value(chart_194_2_series_1, 10)
    chart_194_2.set_next_value(chart_194_2_series_1, 20)
    chart_194_2.set_next_value(chart_194_2_series_1, 30)
    chart_194_2.set_next_value(chart_194_2_series_1, 25)
    chart_194_2.set_next_value(chart_194_2_series_1, 40)
    chart_194_2.set_next_value(chart_194_2_series_1, 35)
    chart_194_2.set_next_value(chart_194_2_series_1, 50)

    # textarea: textarea_194_3
    textarea_194_3 = lv.textarea(parent)
    objects["textarea_194_3"] = textarea_194_3
    textarea_194_3.set_pos(508, 207)
    textarea_194_3.set_size(48, 73)
    textarea_194_3.set_text("Testo 194:3 \" \\ Città")
    textarea_194_3.set_placeholder_text("Type here")
    textarea_194_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_194_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_194_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    textarea_194_3.add_event_cb(textarea_194_3_changed, lv.EVENT.VALUE_CHANGED, None)

    # msgbox: msgbox_194_4
    msgbox_194_4 = lv.msgbox(parent)
    objects["msgbox_194_4"] = msgbox_194_4
    msgbox_194_4.set_pos(259, 361)
    msgbox_194_4.set_size(247, 76)
    msgbox_194_4_title = msgbox_194_4.add_title("Notice")
    msgbox_194_4_text = msgbox_194_4.add_text("Testo 194:4 \" \\ Città")
    msgbox_194_4_button_1 = msgbox_194_4.add_footer_button("OK")
    msgbox_194_4_button_2 = msgbox_194_4.add_footer_button("Cancel")
    msgbox_194_4_close = msgbox_194_4.add_close_button()
    msgbox_194_4.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # dropdown: dropdown_194_5
    dropdown_194_5 = lv.dropdown(parent)
    objects["dropdown_194_5"] = dropdown_194_5
    dropdown_194_5.set_pos(39, 348)
    dropdown_194_5.set_size(267, 83)
    dropdown_194_5.set_options("Option 1\nOption 2\nOption 3")
    dropdown_194_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_194_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_194_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # tileview: tileview_194_6
    tileview_194_6 = lv.tileview(parent)
    objects["tileview_194_6"] = tileview_194_6
    tileview_194_6.set_pos(398, 67)
    tileview_194_6.set_size(235, 24)
    tileview_194_6.add_tile(0, 0, lv.DIR.ALL)
    tileview_194_6.add_tile(1, 0, lv.DIR.ALL)
    tileview_194_6.add_tile(0, 1, lv.DIR.ALL)
    tileview_194_6.add_tile(1, 1, lv.DIR.ALL)
    tileview_194_6.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def random_194_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_194_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_194_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_194_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_194_get_current_page():
    return current_screen

def random_194_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_194_load_page(0)
