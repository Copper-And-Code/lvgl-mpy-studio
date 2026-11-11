"""
Auto-generated LVGL UI Code for MicroPython
Project: One tileview
Generated: 2023-11-14T22:13:41.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


screens = [None] * 1
current_screen = 0

def one_tileview_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # tileview: Tile View_w21
    tile_view_w21 = lv.tileview(parent)
    objects["tile_view_w21"] = tile_view_w21
    tile_view_w21.set_pos(83, 72)
    tile_view_w21.set_size(300, 250)
    tile_view_w21.add_tile(0, 0, lv.DIR.ALL)
    tile_view_w21.add_tile(1, 0, lv.DIR.ALL)
    tile_view_w21.add_tile(0, 1, lv.DIR.ALL)
    tile_view_w21.add_tile(1, 1, lv.DIR.ALL)
    tile_view_w21.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)


def one_tileview_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_tileview_create_main(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def one_tileview_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            one_tileview_create_main(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def one_tileview_get_current_page():
    return current_screen

def one_tileview_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    one_tileview_load_page(0)
