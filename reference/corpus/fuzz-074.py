"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 74
Generated: 2023-11-14T22:15:06.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def slider_74_3_changed(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by app
        pass

screens = [None] * 1
current_screen = 0

def random_74_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # button: button_74_0
    button_74_0 = lv.button(parent)
    objects["button_74_0"] = button_74_0
    button_74_0.set_pos(642, 87)
    button_74_0.set_size(181, 38)
    button_74_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_74_0.set_style_radius(5, lv.PART.MAIN)
    button_74_0_label = lv.label(button_74_0)
    button_74_0_label.set_text("Testo 74:0 \" \\ Città")
    button_74_0_label.center()
    button_74_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_74_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # arc: arc_74_1
    arc_74_1 = lv.arc(parent)
    objects["arc_74_1"] = arc_74_1
    arc_74_1.set_pos(73, 394)
    arc_74_1.set_size(105, 44)
    arc_74_1.set_bg_angles(135, 45)
    arc_74_1.set_range(0, 100)
    arc_74_1.set_value(50)
    arc_74_1.set_style_arc_width(10, lv.PART.MAIN)
    arc_74_1.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_74_1.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_74_1.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_74_1.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)

    # tabview: tabview_74_2
    tabview_74_2 = lv.tabview(parent)
    objects["tabview_74_2"] = tabview_74_2
    tabview_74_2.set_pos(124, 139)
    tabview_74_2.set_size(155, 130)
    tabview_74_2.set_tab_bar_position(lv.DIR.TOP)
    tabview_74_2.set_tab_bar_size(40)
    tabview_74_2_tab_1 = tabview_74_2.add_tab("Tab 1")
    tabview_74_2_tab_2 = tabview_74_2.add_tab("Tab 2")
    tabview_74_2_tab_3 = tabview_74_2.add_tab("Tab 3")
    tabview_74_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # slider: slider_74_3
    slider_74_3 = lv.slider(parent)
    objects["slider_74_3"] = slider_74_3
    slider_74_3.set_pos(574, 309)
    slider_74_3.set_size(59, 139)
    slider_74_3.set_range(0, 100)
    slider_74_3.set_value(50, False)
    slider_74_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_74_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_74_3.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_74_3.add_event_cb(slider_74_3_changed, lv.EVENT.VALUE_CHANGED, None)


def random_74_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_74_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_74_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_74_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_74_get_current_page():
    return current_screen

def random_74_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_74_load_page(0)
