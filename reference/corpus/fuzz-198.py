"""
Auto-generated LVGL UI Code for MicroPython
Project: Random 198
Generated: 2023-11-14T22:17:10.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def random_198_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # imagebutton: imagebutton_198_0
    imagebutton_198_0 = lv.imagebutton(parent)
    objects["imagebutton_198_0"] = imagebutton_198_0
    imagebutton_198_0.set_pos(165, 58)
    imagebutton_198_0.set_size(54, 13)
    imagebutton_198_0.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_198_0.set_style_radius(5, lv.PART.MAIN)
    imagebutton_198_0_label = lv.label(imagebutton_198_0)
    imagebutton_198_0_label.set_text("Testo 198:0 \" \\ Città")
    imagebutton_198_0_label.center()
    imagebutton_198_0_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_198_0_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # image: image_198_1
    image_198_1 = lv.image(parent)
    objects["image_198_1"] = image_198_1
    image_198_1.set_pos(647, 73)
    image_198_1.set_size(263, 50)

    # scale: scale_198_2
    scale_198_2 = lv.scale(parent)
    objects["scale_198_2"] = scale_198_2
    scale_198_2.set_pos(22, 157)
    scale_198_2.set_size(146, 55)
    scale_198_2.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale_198_2.set_range(0, 100)
    scale_198_2.set_total_tick_count(51)
    scale_198_2.set_major_tick_every(5)
    scale_198_2.set_style_length(15, lv.PART.INDICATOR)
    scale_198_2.set_style_length(8, lv.PART.ITEMS)
    scale_198_2.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_198_2.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # buttonmatrix: buttonmatrix_198_3
    buttonmatrix_198_3 = lv.buttonmatrix(parent)
    objects["buttonmatrix_198_3"] = buttonmatrix_198_3
    buttonmatrix_198_3.set_pos(421, 240)
    buttonmatrix_198_3.set_size(95, 134)
    buttonmatrix_198_3_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_198_3.set_map(buttonmatrix_198_3_map)
    buttonmatrix_198_3.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_198_3.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_198_3.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_198_3.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)


def random_198_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_198_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def random_198_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            random_198_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def random_198_get_current_page():
    return current_screen

def random_198_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    random_198_load_page(0)
