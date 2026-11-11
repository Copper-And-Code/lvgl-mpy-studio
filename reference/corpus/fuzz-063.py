"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 63
Generated: 2023-11-14T22:14:55.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_63_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tabview: tabview_63_0
    tabview_63_0 = lv.tabview(parent)
    objects["tabview_63_0"] = tabview_63_0
    tabview_63_0.set_pos(462, 133)
    tabview_63_0.set_size(102, 25)
    tabview_63_0.set_tab_bar_position(lv.DIR.TOP)
    tabview_63_0.set_tab_bar_size(40)
    tabview_63_0_tab_1 = tabview_63_0.add_tab("Tab 1")
    tabview_63_0_tab_2 = tabview_63_0.add_tab("Tab 2")
    tabview_63_0_tab_3 = tabview_63_0.add_tab("Tab 3")
    tabview_63_0.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # msgbox: msgbox_63_1
    msgbox_63_1 = lv.msgbox(parent)
    objects["msgbox_63_1"] = msgbox_63_1
    msgbox_63_1.set_pos(514, 263)
    msgbox_63_1.set_size(152, 31)
    msgbox_63_1_title = msgbox_63_1.add_title("Notice")
    msgbox_63_1_text = msgbox_63_1.add_text("Testo 63:1 \" \\ Città")
    msgbox_63_1_button_1 = msgbox_63_1.add_footer_button("OK")
    msgbox_63_1_button_2 = msgbox_63_1.add_footer_button("Cancel")
    msgbox_63_1_close = msgbox_63_1.add_close_button()
    msgbox_63_1.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # tabview: tabview_63_2
    tabview_63_2 = lv.tabview(parent)
    objects["tabview_63_2"] = tabview_63_2
    tabview_63_2.set_pos(696, 34)
    tabview_63_2.set_size(71, 35)
    tabview_63_2.set_tab_bar_position(lv.DIR.TOP)
    tabview_63_2.set_tab_bar_size(40)
    tabview_63_2_tab_1 = tabview_63_2.add_tab("Tab 1")
    tabview_63_2_tab_2 = tabview_63_2.add_tab("Tab 2")
    tabview_63_2_tab_3 = tabview_63_2.add_tab("Tab 3")
    tabview_63_2.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # scale: scale_63_3
    scale_63_3 = lv.scale(parent)
    objects["scale_63_3"] = scale_63_3
    scale_63_3.set_pos(271, 272)
    scale_63_3.set_size(186, 12)
    scale_63_3.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_63_3.set_range(0, 100)
    scale_63_3.set_total_tick_count(51)
    scale_63_3.set_major_tick_every(5)
    scale_63_3.set_style_length(15, lv.PART.INDICATOR)
    scale_63_3.set_style_length(8, lv.PART.ITEMS)
    scale_63_3.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_63_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # image: image_63_4
    image_63_4 = lv.image(parent)
    objects["image_63_4"] = image_63_4
    image_63_4.set_pos(575, 161)
    image_63_4.set_size(164, 143)

    # textarea: textarea_63_5
    textarea_63_5 = lv.textarea(parent)
    objects["textarea_63_5"] = textarea_63_5
    textarea_63_5.set_pos(518, 354)
    textarea_63_5.set_size(148, 24)
    textarea_63_5.set_text("Testo 63:5 \" \\ Città")
    textarea_63_5.set_placeholder_text("Type here")
    textarea_63_5.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_63_5.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_63_5.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_63_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_63_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_63_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_63_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_63_get_current_page():
    return current_screen

def random_63_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_63_load_page(0)
