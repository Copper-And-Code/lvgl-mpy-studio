"""
Auto-generated LVGL UI Code for MicroPython
Project: 1 My "Project" * /
Generated: 2023-11-14T22:13:51.000Z
Pages: 3

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def print_event_cb(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # handled by the application
        pass

def print_event_cb_2(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # other code
        pass

screens = [None] * 3
current_screen = 0

def ui_1_my_project_create_main(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # panel: Root panel
    root_panel = lv.obj(parent)
    objects["root_panel"] = root_panel
    root_panel.set_pos(50, 50)
    root_panel.set_size(200, 150)
    root_panel.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    root_panel.set_style_border_width(2, lv.PART.MAIN)
    root_panel.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    root_panel.set_style_radius(5, lv.PART.MAIN)
    root_panel.set_style_pad_all(0, lv.PART.MAIN)
    root_panel.set_style_pad_gap(0, lv.PART.MAIN)

    # panel: Child panel
    child_panel = lv.obj(root_panel)
    objects["child_panel"] = child_panel
    child_panel.set_pos(50, 50)
    child_panel.set_size(200, 150)
    child_panel.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    child_panel.set_style_border_width(2, lv.PART.MAIN)
    child_panel.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    child_panel.set_style_radius(5, lv.PART.MAIN)
    child_panel.set_style_pad_all(0, lv.PART.MAIN)
    child_panel.set_style_pad_gap(0, lv.PART.MAIN)

    # label: Grand child
    grand_child = lv.label(child_panel)
    objects["grand_child"] = grand_child
    grand_child.set_pos(50, 50)
    grand_child.set_size(120, 30)
    grand_child.set_text("Quote \" backslash \\ newline\nend */ \"\"\" ??= tab\t")
    grand_child.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    grand_child.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    grand_child.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # label: orphan
    orphan = lv.label(parent)
    objects["orphan"] = orphan
    orphan.set_pos(50, 50)
    orphan.set_size(120, 30)
    orphan.set_text("Label Text")
    orphan.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    orphan.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    orphan.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # button: Button 1
    button_1 = lv.button(parent)
    objects["button_1"] = button_1
    button_1.set_pos(50, 50)
    button_1.set_size(100, 40)
    button_1.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_1.set_style_radius(5, lv.PART.MAIN)
    button_1_label = lv.label(button_1)
    button_1_label.set_text("Quote \" backslash \\ newline\nend */ \"\"\" ??= tab\t")
    button_1_label.center()
    button_1_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_1.add_event_cb(print_event_cb, lv.EVENT.CLICKED, None)

    # button: button_1
    button_1_2 = lv.button(parent)
    objects["button_1_2"] = button_1_2
    button_1_2.set_pos(50, 50)
    button_1_2.set_size(100, 40)
    button_1_2.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_1_2.set_style_radius(5, lv.PART.MAIN)
    button_1_2_label = lv.label(button_1_2)
    button_1_2_label.set_text("Button")
    button_1_2_label.center()
    button_1_2_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_1_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_1_2.add_event_cb(print_event_cb_2, lv.EVENT.CLICKED, None)

    # button: Button 1
    button_1_3 = lv.button(parent)
    objects["button_1_3"] = button_1_3
    button_1_3.set_pos(50, 50)
    button_1_3.set_size(100, 40)
    button_1_3.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_1_3.set_style_radius(5, lv.PART.MAIN)
    button_1_3_label = lv.label(button_1_3)
    button_1_3_label.set_text("Button")
    button_1_3_label.center()
    button_1_3_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_1_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # label: 1st label
    label_1st_label = lv.label(parent)
    objects["label_1st_label"] = label_1st_label
    label_1st_label.set_pos(50, 50)
    label_1st_label.set_size(120, 30)
    label_1st_label.set_text("Label Text")
    label_1st_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_1st_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_1st_label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # label: lambda
    lambda_label = lv.label(parent)
    objects["lambda_label"] = lambda_label
    lambda_label.set_pos(50, 50)
    lambda_label.set_size(120, 30)
    lambda_label.set_text("Label Text")
    lambda_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    lambda_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    lambda_label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # label: lv_obj_create
    label_lv_obj_create = lv.label(parent)
    objects["label_lv_obj_create"] = label_lv_obj_create
    label_lv_obj_create.set_pos(50, 50)
    label_lv_obj_create.set_size(120, 30)
    label_lv_obj_create.set_text("Label Text")
    label_lv_obj_create.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_lv_obj_create.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label_lv_obj_create.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # label: print
    print_label = lv.label(parent)
    objects["print_label"] = print_label
    print_label.set_pos(50, 50)
    print_label.set_size(120, 30)
    print_label.set_text("Label Text")
    print_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    print_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    print_label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # label: ***
    label = lv.label(parent)
    objects["label"] = label
    label.set_pos(50, 50)
    label.set_size(120, 30)
    label.set_text("Label Text")
    label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # label: Città
    citta = lv.label(parent)
    objects["citta"] = citta
    citta.set_pos(50, 50)
    citta.set_size(120, 30)
    citta.set_text("Label Text")
    citta.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    citta.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    citta.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

    # slider: bad slider
    bad_slider = lv.slider(parent)
    objects["bad_slider"] = bad_slider
    bad_slider.set_pos(50, 50)
    bad_slider.set_size(200, 20)
    bad_slider.set_range(0, 100)
    bad_slider.set_value(50, False)
    bad_slider.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    bad_slider.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)

    # dropdown: options
    options = lv.dropdown(parent)
    objects["options"] = options
    options.set_pos(50, 50)
    options.set_size(150, 40)
    options.set_options("One\n\"Two\"\nThree\\")
    options.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    options.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    options.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # table: table
    table = lv.table(parent)
    objects["table"] = table
    table.set_pos(50, 50)
    table.set_size(300, 200)
    table.set_column_count(3)
    table.set_column_width(0, 100)
    table.set_column_width(1, 100)
    table.set_column_width(2, 100)
    table.set_cell_value(0, 0, "A")
    table.set_cell_value(0, 1, "\"B\"")
    table.set_cell_value(0, 2, "C")
    table.set_cell_value(1, 0, "1")
    table.set_cell_value(1, 1, "2")
    table.set_cell_value(1, 2, "3")
    table.set_cell_value(2, 0, "4")
    table.set_cell_value(2, 1, "5")
    table.set_cell_value(2, 2, "6")
    table.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # buttonmatrix: matrix
    matrix = lv.buttonmatrix(parent)
    objects["matrix"] = matrix
    matrix.set_pos(50, 50)
    matrix.set_size(250, 120)
    matrix_map = ["a", "\"b\"", "\n", "c", "\\", ""]
    matrix.set_map(matrix_map)
    matrix.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    matrix.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    matrix.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    matrix.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # chart: chart
    chart = lv.chart(parent)
    objects["chart"] = chart
    chart.set_pos(50, 50)
    chart.set_size(250, 150)
    chart.set_type(lv.chart.TYPE.LINE)
    chart.set_point_count(10)
    chart.set_div_line_count(3, 5)
    chart.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_series_1 = chart.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart.set_next_value(chart_series_1, 1)
    chart.set_next_value(chart_series_1, 3)
    chart.set_next_value(chart_series_1, 4)

    # scale: scale
    scale = lv.scale(parent)
    objects["scale"] = scale
    scale.set_pos(50, 50)
    scale.set_size(200, 60)
    scale.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
    scale.set_range(10, 10)
    scale.set_total_tick_count(6)
    scale.set_major_tick_every(5)
    scale.set_style_length(15, lv.PART.INDICATOR)
    scale.set_style_length(8, lv.PART.ITEMS)
    scale.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # panel: cycle a
    cycle_a = lv.obj(parent)
    objects["cycle_a"] = cycle_a
    cycle_a.set_pos(50, 50)
    cycle_a.set_size(200, 150)
    cycle_a.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    cycle_a.set_style_border_width(2, lv.PART.MAIN)
    cycle_a.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    cycle_a.set_style_radius(5, lv.PART.MAIN)
    cycle_a.set_style_pad_all(0, lv.PART.MAIN)
    cycle_a.set_style_pad_gap(0, lv.PART.MAIN)

    # panel: cycle b
    cycle_b = lv.obj(cycle_a)
    objects["cycle_b"] = cycle_b
    cycle_b.set_pos(50, 50)
    cycle_b.set_size(200, 150)
    cycle_b.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    cycle_b.set_style_border_width(2, lv.PART.MAIN)
    cycle_b.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    cycle_b.set_style_radius(5, lv.PART.MAIN)
    cycle_b.set_style_pad_all(0, lv.PART.MAIN)
    cycle_b.set_style_pad_gap(0, lv.PART.MAIN)


def ui_1_my_project_create_main_2(parent=None):
    if parent is None:
        parent = lv.screen_active()


def ui_1_my_project_create_init(parent=None):
    if parent is None:
        parent = lv.screen_active()


def ui_1_my_project_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 3:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            ui_1_my_project_create_main(screens[0])
        elif page_index == 1:
            ui_1_my_project_create_main_2(screens[1])
        elif page_index == 2:
            ui_1_my_project_create_init(screens[2])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def ui_1_my_project_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 3:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            ui_1_my_project_create_main(screens[0])
        elif page_index == 1:
            ui_1_my_project_create_main_2(screens[1])
        elif page_index == 2:
            ui_1_my_project_create_init(screens[2])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def ui_1_my_project_get_current_page():
    return current_screen

def ui_1_my_project_init():
    global screens, current_screen
    screens = [None] * 3
    current_screen = 0
    ui_1_my_project_load_page(0)
