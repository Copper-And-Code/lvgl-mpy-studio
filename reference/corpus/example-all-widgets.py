"""
Auto-generated LVGL UI Code for MicroPython
Project: All Widgets
Generated: 2023-11-14T22:13:50.000Z
Pages: 1

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

# Fonts used: lv.font_montserrat_14, lv.font_montserrat_16, lv.font_montserrat_24 (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)
# Images loaded from files need an LVGL file system driver: A:images/background.png
# Not generated (only PNG and JPEG images are supported): anim.gif
# Font "DejaVuSans-Latin1.ttf" 14 px not converted (fonts are converted by the desktop app): Montserrat is used instead
# Font "DejaVuSans-Latin1.ttf" 22 px not converted (fonts are converted by the desktop app): Montserrat is used instead
# Font "DejaVuSans-Latin1.ttf" 18 px not converted (fonts are converted by the desktop app): Montserrat is used instead
# Font "broken.ttf" 14 px not converted (fonts are converted by the desktop app): Montserrat is used instead
# Font "DejaVuSans-Latin1.ttf" 16 px not converted (fonts are converted by the desktop app): Montserrat is used instead
# Font "DejaVuSans-Latin1.ttf" 12 px not converted (fonts are converted by the desktop app): Montserrat is used instead
import binascii
# Image "logo.png" (6x4 PNG), decoded at run time by LVGL
img_logo_data = binascii.a2b_base64("iVBORw0KGgoAAAANSUhEUgAAAAYAAAAECAYAAACtBE5DAAAAEklEQVR4nGP4z8DwHxtmoJ4EAFeLL9Fq2vKHAAAAAElFTkSuQmCC")
img_logo = lv.image_dsc_t({"header": {"magic": lv.IMAGE_HEADER_MAGIC, "cf": lv.COLOR_FORMAT.RAW_ALPHA, "w": 6, "h": 4}, "data_size": len(img_logo_data), "data": img_logo_data})
# Image "photo.jpg" (8x5 JPEG), decoded at run time by LVGL
img_photo_data = binascii.a2b_base64("/9j/4AAQSkZJRgABAQAAAAAAAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAFAAgDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAb/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFAEBAAAAAAAAAAAAAAAAAAAAB//EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AJ8Awip//9k=")
img_photo = lv.image_dsc_t({"header": {"magic": lv.IMAGE_HEADER_MAGIC, "cf": lv.COLOR_FORMAT.RAW, "w": 8, "h": 5}, "data_size": len(img_photo_data), "data": img_photo_data})
# Variables for data binding (LVGL subjects): read and write them with get_int()/set_int()
var_level = lv.subject_t()
var_level.init_int(3)
var_enabled = lv.subject_t()
var_enabled.init_int(1)
# Created widgets, by name (e.g. objects["ok_button"])
objects = {}


def on_button(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.CLICKED:
        # handled by the application
        pass
    elif code == lv.EVENT.LONG_PRESSED:
        # TODO: handle lv.EVENT.LONG_PRESSED
        pass

def on_value(e):
    code = e.get_code()
    obj = e.get_target_obj()

    if code == lv.EVENT.VALUE_CHANGED:
        # handled by the application
        pass

screens = [None] * 1
current_screen = 0

def all_widgets_create_widgets(parent=None):
    if parent is None:
        parent = lv.screen_active()

    # button: button_widget
    button_widget = lv.button(parent)
    objects["button_widget"] = button_widget
    button_widget.set_pos(50, 50)
    button_widget.set_size(100, 40)
    button_widget.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    button_widget.set_style_radius(5, lv.PART.MAIN)
    button_widget_label = lv.label(button_widget)
    button_widget_label.set_text("Avvia ▶ è")
    button_widget_label.center()
    button_widget_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_widget_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    button_widget.set_style_bg_color(lv.color_hex(0x123456), lv.PART.MAIN)
    button_widget.set_style_bg_opa(200, lv.PART.MAIN)
    button_widget.set_style_border_color(lv.color_hex(0xAABBCC), lv.PART.MAIN)
    button_widget.set_style_border_width(2, lv.PART.MAIN)
    button_widget.set_style_border_opa(100, lv.PART.MAIN)
    button_widget.set_style_pad_top(1, lv.PART.MAIN)
    button_widget.set_style_pad_bottom(2, lv.PART.MAIN)
    button_widget.set_style_pad_left(3, lv.PART.MAIN)
    button_widget.set_style_pad_right(4, lv.PART.MAIN)
    button_widget.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    button_widget.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)
    button_widget.set_style_radius(6, lv.PART.MAIN)
    button_widget.set_style_shadow_width(3, lv.PART.MAIN)
    button_widget.set_style_shadow_offset_x(1, lv.PART.MAIN)
    button_widget.set_style_shadow_offset_y(2, lv.PART.MAIN)
    button_widget.set_style_shadow_color(lv.color_hex(0x000000), lv.PART.MAIN)
    button_widget.add_event_cb(on_button, lv.EVENT.CLICKED, None)
    button_widget.add_event_cb(on_button, lv.EVENT.LONG_PRESSED, None)
    button_widget_anim = lv.anim_t()
    button_widget_anim.init()
    button_widget_anim.set_var(button_widget)
    button_widget_anim.set_values(0, 100)
    button_widget_anim.set_duration(300)
    button_widget_anim.set_reverse_duration(300)
    button_widget_anim.set_path_cb(lv.anim_t.path_ease_in_out)
    button_widget_anim.set_custom_exec_cb(lambda _anim, value: button_widget.set_x(value))
    button_widget_anim.start()
    button_widget_anim_2 = lv.anim_t()
    button_widget_anim_2.init()
    button_widget_anim_2.set_var(button_widget)
    button_widget_anim_2.set_values(0, 100)
    button_widget_anim_2.set_duration(300)
    button_widget_anim_2.set_delay(10)
    button_widget_anim_2.set_repeat_count(1)
    button_widget_anim_2.set_path_cb(lv.anim_t.path_ease_in_out)
    button_widget_anim_2.set_custom_exec_cb(lambda _anim, value: button_widget.set_y(value))
    button_widget_anim_2.start()
    button_widget_anim_3 = lv.anim_t()
    button_widget_anim_3.init()
    button_widget_anim_3.set_var(button_widget)
    button_widget_anim_3.set_values(0, 100)
    button_widget_anim_3.set_duration(300)
    button_widget_anim_3.set_delay(20)
    button_widget_anim_3.set_reverse_duration(300)
    button_widget_anim_3.set_path_cb(lv.anim_t.path_ease_in_out)
    button_widget_anim_3.set_custom_exec_cb(lambda _anim, value: button_widget.set_width(value))
    button_widget_anim_3.start()
    button_widget_anim_4 = lv.anim_t()
    button_widget_anim_4.init()
    button_widget_anim_4.set_var(button_widget)
    button_widget_anim_4.set_values(0, 100)
    button_widget_anim_4.set_duration(300)
    button_widget_anim_4.set_delay(30)
    button_widget_anim_4.set_repeat_count(1)
    button_widget_anim_4.set_path_cb(lv.anim_t.path_ease_in_out)
    button_widget_anim_4.set_custom_exec_cb(lambda _anim, value: button_widget.set_height(value))
    button_widget_anim_4.start()
    button_widget_anim_5 = lv.anim_t()
    button_widget_anim_5.init()
    button_widget_anim_5.set_var(button_widget)
    button_widget_anim_5.set_values(0, 100)
    button_widget_anim_5.set_duration(300)
    button_widget_anim_5.set_delay(40)
    button_widget_anim_5.set_reverse_duration(300)
    button_widget_anim_5.set_path_cb(lv.anim_t.path_ease_in_out)
    button_widget_anim_5.set_custom_exec_cb(lambda _anim, value: button_widget.set_style_opa(value, lv.PART.MAIN))
    button_widget_anim_5.start()
    button_widget_anim_6 = lv.anim_t()
    button_widget_anim_6.init()
    button_widget_anim_6.set_var(button_widget)
    button_widget_anim_6.set_values(0, 100)
    button_widget_anim_6.set_duration(300)
    button_widget_anim_6.set_delay(50)
    button_widget_anim_6.set_repeat_count(1)
    button_widget_anim_6.set_path_cb(lv.anim_t.path_ease_in_out)
    button_widget_anim_6.set_custom_exec_cb(lambda _anim, value: button_widget.set_style_opa(value, lv.PART.MAIN))
    button_widget_anim_6.start()

    # label: label_widget
    label_widget = lv.label(parent)
    objects["label_widget"] = label_widget
    label_widget.set_pos(50, 50)
    label_widget.set_size(120, 30)
    label_widget.set_text("Label Text")
    label_widget.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    label_widget.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)
    label_widget.set_long_mode(lv.label.LONG_MODE.DOTS)
    label_widget.set_style_text_align(lv.TEXT_ALIGN.RIGHT, lv.PART.MAIN)
    label_widget.set_recolor(True)
    label_widget.bind_text(var_level, "Level: %d")

    # panel: panel_widget
    panel_widget = lv.obj(parent)
    objects["panel_widget"] = panel_widget
    panel_widget.set_pos(50, 50)
    panel_widget.set_size(200, 150)
    panel_widget.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    panel_widget.set_style_border_width(2, lv.PART.MAIN)
    panel_widget.set_style_border_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    panel_widget.set_style_radius(5, lv.PART.MAIN)
    panel_widget.set_style_opa(200, lv.PART.MAIN)
    panel_widget.set_style_bg_opa(128, lv.PART.MAIN)
    panel_widget.set_style_pad_top(4, lv.PART.MAIN)
    panel_widget.set_style_pad_bottom(0, lv.PART.MAIN)
    panel_widget.set_style_pad_left(0, lv.PART.MAIN)
    panel_widget.set_style_pad_right(0, lv.PART.MAIN)
    panel_widget.set_style_pad_row(2, lv.PART.MAIN)
    panel_widget.set_style_pad_column(0, lv.PART.MAIN)
    panel_widget.set_style_shadow_width(6, lv.PART.MAIN)
    panel_widget.set_style_shadow_color(lv.color_hex(0x333333), lv.PART.MAIN)
    panel_widget.set_style_shadow_offset_x(2, lv.PART.MAIN)
    panel_widget.set_style_shadow_offset_y(3, lv.PART.MAIN)
    panel_widget.set_style_outline_width(1, lv.PART.MAIN)
    panel_widget.set_style_outline_color(lv.color_hex(0x00FF00), lv.PART.MAIN)
    panel_widget.set_style_transform_rotation(10, lv.PART.MAIN)
    panel_widget.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
    panel_widget.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
    panel_widget.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
    panel_widget.set_scroll_dir(lv.DIR.VER)
    panel_widget.remove_flag(lv.obj.FLAG.CLICKABLE)

    # slider: slider_widget
    slider_widget = lv.slider(parent)
    objects["slider_widget"] = slider_widget
    slider_widget.set_pos(50, 50)
    slider_widget.set_size(200, 20)
    slider_widget.set_range(0, 100)
    slider_widget.set_mode(lv.slider.MODE.RANGE)
    slider_widget.set_value(0, False)
    slider_widget.set_start_value(10, False)
    slider_widget.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    slider_widget.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)
    slider_widget.set_style_bg_color(lv.color_hex(0x1976D2), lv.PART.KNOB)
    slider_widget.bind_value(var_level)
    slider_widget.add_event_cb(on_value, lv.EVENT.VALUE_CHANGED, None)

    # switch: switch_widget
    switch_widget = lv.switch(parent)
    objects["switch_widget"] = switch_widget
    switch_widget.set_pos(50, 50)
    switch_widget.set_size(60, 30)
    switch_widget.add_state(lv.STATE.CHECKED)
    switch_widget.set_style_bg_color(lv.color_hex(0xBDBDBD), lv.PART.MAIN)
    switch_widget.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR | lv.STATE.CHECKED)
    switch_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB)
    switch_widget.add_state(lv.STATE.DISABLED)
    switch_widget.bind_checked(var_enabled)

    # checkbox: checkbox_widget
    checkbox_widget = lv.checkbox(parent)
    objects["checkbox_widget"] = checkbox_widget
    checkbox_widget.set_pos(50, 50)
    checkbox_widget.set_text("Checkbox")
    checkbox_widget.add_state(lv.STATE.CHECKED)
    checkbox_widget.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    checkbox_widget.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    checkbox_widget.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR | lv.STATE.CHECKED)
    checkbox_widget.bind_checked(var_enabled)

    # textarea: textarea_widget
    textarea_widget = lv.textarea(parent)
    objects["textarea_widget"] = textarea_widget
    textarea_widget.set_pos(50, 50)
    textarea_widget.set_size(200, 100)
    textarea_widget.set_one_line(True)
    textarea_widget.set_password_mode(True)
    textarea_widget.set_max_length(20)
    textarea_widget.set_accepted_chars("0123456789")
    textarea_widget.set_text("abc")
    textarea_widget.set_placeholder_text("Type here")
    textarea_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    textarea_widget.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    textarea_widget.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # dropdown: dropdown_widget
    dropdown_widget = lv.dropdown(parent)
    objects["dropdown_widget"] = dropdown_widget
    dropdown_widget.set_pos(50, 50)
    dropdown_widget.set_size(150, 40)
    dropdown_widget.set_options("Option 1\nOption 2\nOption 3")
    dropdown_widget.set_selected(1)
    dropdown_widget.set_dir(lv.DIR.TOP)
    dropdown_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    dropdown_widget.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    dropdown_widget.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # roller: roller_widget
    roller_widget = lv.roller(parent)
    objects["roller_widget"] = roller_widget
    roller_widget.set_pos(50, 50)
    roller_widget.set_size(100, 150)
    roller_widget.set_options("Option 1\nOption 2\nOption 3\nOption 4\nOption 5", lv.roller.MODE.INFINITE)
    roller_widget.set_selected(2, False)
    roller_widget.set_visible_row_count(3)
    roller_widget.set_style_bg_color(lv.color_hex(0xF5F5F5), lv.PART.MAIN)
    roller_widget.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.SELECTED)
    roller_widget.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    roller_widget.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)
    roller_widget.bind_value(var_level)

    # spinbox: spinbox_widget
    spinbox_widget = lv.spinbox(parent)
    objects["spinbox_widget"] = spinbox_widget
    spinbox_widget.set_pos(50, 50)
    spinbox_widget.set_size(120, 40)
    spinbox_widget.set_digit_format(4, 2)
    spinbox_widget.set_range(0, 999)
    spinbox_widget.set_value(0)
    spinbox_widget.set_step(5)
    spinbox_widget.set_rollover(True)
    spinbox_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    spinbox_widget.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    spinbox_widget.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

    # keyboard: keyboard_widget
    keyboard_widget = lv.keyboard(parent)
    objects["keyboard_widget"] = keyboard_widget
    keyboard_widget.set_pos(0, 280)
    keyboard_widget.set_size(480, 200)
    keyboard_widget.set_mode(lv.keyboard.MODE.NUMBER)
    keyboard_widget.set_popovers(False)

    # bar: bar_widget
    bar_widget = lv.bar(parent)
    objects["bar_widget"] = bar_widget
    bar_widget.set_pos(50, 50)
    bar_widget.set_size(200, 20)
    bar_widget.set_range(0, 100)
    bar_widget.set_mode(lv.bar.MODE.RANGE)
    bar_widget.set_value(50, False)
    bar_widget.set_start_value(10, False)
    bar_widget.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    bar_widget.set_style_bg_color(lv.color_hex(0x4CAF50), lv.PART.INDICATOR)

    # arc: arc_widget
    arc_widget = lv.arc(parent)
    objects["arc_widget"] = arc_widget
    arc_widget.set_pos(50, 50)
    arc_widget.set_size(100, 100)
    arc_widget.set_rotation(90)
    arc_widget.set_bg_angles(135, 45)
    arc_widget.set_mode(lv.arc.MODE.REVERSE)
    arc_widget.set_range(0, 100)
    arc_widget.set_value(50)
    arc_widget.set_style_arc_width(10, lv.PART.MAIN)
    arc_widget.set_style_arc_width(10, lv.PART.INDICATOR)
    arc_widget.set_style_arc_color(lv.color_hex(0xE0E0E0), lv.PART.MAIN)
    arc_widget.set_style_arc_color(lv.color_hex(0xFF9800), lv.PART.INDICATOR)
    arc_widget.set_style_bg_color(lv.color_hex(0xFF9800), lv.PART.KNOB)
    arc_widget.bind_value(var_level)

    # spinner: spinner_widget
    spinner_widget = lv.arc(parent)
    objects["spinner_widget"] = spinner_widget
    spinner_widget.set_pos(50, 50)
    spinner_widget.set_size(50, 50)
    spinner_widget.set_bg_angles(0, 360)
    spinner_widget.set_angles(0, 60)
    spinner_widget.remove_style(None, lv.PART.KNOB)
    spinner_widget.remove_flag(lv.obj.FLAG.CLICKABLE)
    spinner_widget_anim = lv.anim_t()
    spinner_widget_anim.init()
    spinner_widget_anim.set_var(spinner_widget)
    spinner_widget_anim.set_values(0, 360)
    spinner_widget_anim.set_duration(1000)
    spinner_widget_anim.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    spinner_widget_anim.set_path_cb(lv.anim_t.path_linear)
    spinner_widget_anim.set_custom_exec_cb(lambda _anim, value: spinner_widget.set_rotation(value))
    spinner_widget_anim.start()
    spinner_widget.set_style_arc_width(8, lv.PART.MAIN)
    spinner_widget.set_style_arc_width(8, lv.PART.INDICATOR)
    spinner_widget.set_style_arc_color(lv.color_hex(0x2196F3), lv.PART.INDICATOR)

    # led: led_widget
    led_widget = lv.led(parent)
    objects["led_widget"] = led_widget
    led_widget.set_pos(50, 50)
    led_widget.set_size(30, 30)
    led_widget.set_color(lv.color_hex(0xFF0000))
    led_widget.set_brightness(255)

    # chart: chart_widget
    chart_widget = lv.chart(parent)
    objects["chart_widget"] = chart_widget
    chart_widget.set_pos(50, 50)
    chart_widget.set_size(250, 150)
    chart_widget.set_type(lv.chart.TYPE.BAR)
    chart_widget.set_point_count(10)
    chart_widget.set_div_line_count(3, 5)
    chart_widget.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 100)
    chart_widget.set_update_mode(lv.chart.UPDATE_MODE.CIRCULAR)
    chart_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    chart_widget_series_1 = chart_widget.add_series(lv.color_hex(0x2196F3), lv.chart.AXIS.PRIMARY_Y)
    chart_widget.set_next_value(chart_widget_series_1, 10)
    chart_widget.set_next_value(chart_widget_series_1, 20)
    chart_widget.set_next_value(chart_widget_series_1, 30)
    chart_widget.set_next_value(chart_widget_series_1, 25)
    chart_widget.set_next_value(chart_widget_series_1, 40)
    chart_widget.set_next_value(chart_widget_series_1, 35)
    chart_widget.set_next_value(chart_widget_series_1, 50)
    chart_widget_series_2 = chart_widget.add_series(lv.color_hex(0xFF5722), lv.chart.AXIS.PRIMARY_Y)
    chart_widget.set_next_value(chart_widget_series_2, 5)
    chart_widget.set_next_value(chart_widget_series_2, 15)
    chart_widget.set_next_value(chart_widget_series_2, 25)

    # table: table_widget
    table_widget = lv.table(parent)
    objects["table_widget"] = table_widget
    table_widget.set_pos(50, 50)
    table_widget.set_size(300, 200)
    table_widget.set_column_count(3)
    table_widget.set_column_width(0, 100)
    table_widget.set_column_width(1, 100)
    table_widget.set_column_width(2, 100)
    table_widget.set_cell_value(0, 0, "Col 1")
    table_widget.set_cell_value(0, 1, "Col 2")
    table_widget.set_cell_value(0, 2, "Col 3")
    table_widget.set_cell_value(1, 0, "A1")
    table_widget.set_cell_value(1, 1, "B1")
    table_widget.set_cell_value(1, 2, "C1")
    table_widget.set_cell_value(2, 0, "A2")
    table_widget.set_cell_value(2, 1, "B2")
    table_widget.set_cell_value(2, 2, "C2")
    table_widget.set_cell_value(3, 0, "A3")
    table_widget.set_cell_value(3, 1, "B3")
    table_widget.set_cell_value(3, 2, "C3")
    table_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.ITEMS)
    table_widget.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    table_widget.set_style_border_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    table_widget.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # scale: scale_widget
    scale_widget = lv.scale(parent)
    objects["scale_widget"] = scale_widget
    scale_widget.set_pos(50, 50)
    scale_widget.set_size(200, 60)
    scale_widget.set_mode(lv.scale.MODE.ROUND_INNER)
    scale_widget.set_range(0, 100)
    scale_widget.set_total_tick_count(51)
    scale_widget.set_major_tick_every(5)
    scale_widget.set_label_show(False)
    scale_widget.set_style_length(15, lv.PART.INDICATOR)
    scale_widget.set_style_length(8, lv.PART.ITEMS)
    scale_widget.set_style_line_color(lv.color_hex(0x000000), lv.PART.INDICATOR)
    scale_widget.set_style_text_color(lv.color_hex(0x000000), lv.PART.INDICATOR)

    # image: image_widget
    image_widget = lv.image(parent)
    objects["image_widget"] = image_widget
    image_widget.set_pos(50, 50)
    image_widget.set_size(100, 100)
    image_widget.set_src(img_logo)
    image_widget.set_rotation(10)
    image_widget.set_scale(512)
    image_widget.set_pivot(5, 0)
    image_widget.set_antialias(False)

    # imagebutton: imagebutton_widget
    imagebutton_widget = lv.imagebutton(parent)
    objects["imagebutton_widget"] = imagebutton_widget
    imagebutton_widget.set_pos(50, 50)
    imagebutton_widget.set_size(120, 120)
    imagebutton_widget.set_src(lv.imagebutton.STATE.RELEASED, None, img_photo, None)
    imagebutton_widget.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    imagebutton_widget.set_style_radius(5, lv.PART.MAIN)
    imagebutton_widget_label = lv.label(imagebutton_widget)
    imagebutton_widget_label.set_text("Button")
    imagebutton_widget_label.center()
    imagebutton_widget_label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    imagebutton_widget_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # tabview: tabview_widget
    tabview_widget = lv.tabview(parent)
    objects["tabview_widget"] = tabview_widget
    tabview_widget.set_pos(50, 50)
    tabview_widget.set_size(300, 250)
    tabview_widget.set_tab_bar_position(lv.DIR.LEFT)
    tabview_widget.set_tab_bar_size(40)
    tabview_widget_tab_1 = tabview_widget.add_tab("Tab 1")
    tabview_widget_tab_2 = tabview_widget.add_tab("Tab 2")
    tabview_widget_tab_3 = tabview_widget.add_tab("Tab 3")
    tabview_widget.set_active(1, False)
    tabview_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # tileview: tileview_widget
    tileview_widget = lv.tileview(parent)
    objects["tileview_widget"] = tileview_widget
    tileview_widget.set_pos(50, 50)
    tileview_widget.set_size(300, 250)
    tileview_widget.add_tile(0, 0, lv.DIR.ALL)
    tileview_widget.add_tile(1, 0, lv.DIR.ALL)
    tileview_widget.add_tile(0, 1, lv.DIR.ALL)
    tileview_widget.add_tile(1, 1, lv.DIR.ALL)
    tileview_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # menu: menu_widget
    menu_widget = lv.obj(parent)
    objects["menu_widget"] = menu_widget
    menu_widget.set_pos(50, 50)
    menu_widget.set_size(250, 300)
    menu_widget.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    menu_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    menu_widget_title = lv.label(menu_widget)
    menu_widget_title.set_text("Menu")
    menu_widget_title.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_widget_item_1 = lv.button(menu_widget)
    menu_widget_item_1.set_width(lv.pct(100))
    menu_widget_item_1_label = lv.label(menu_widget_item_1)
    menu_widget_item_1_label.set_text("Item 1")
    menu_widget_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_widget_item_2 = lv.button(menu_widget)
    menu_widget_item_2.set_width(lv.pct(100))
    menu_widget_item_2_label = lv.label(menu_widget_item_2)
    menu_widget_item_2_label.set_text("Item 2")
    menu_widget_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_widget_item_3 = lv.button(menu_widget)
    menu_widget_item_3.set_width(lv.pct(100))
    menu_widget_item_3_label = lv.label(menu_widget_item_3)
    menu_widget_item_3_label.set_text("Item 3")
    menu_widget_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    menu_widget_item_4 = lv.button(menu_widget)
    menu_widget_item_4.set_width(lv.pct(100))
    menu_widget_item_4_label = lv.label(menu_widget_item_4)
    menu_widget_item_4_label.set_text("Item 4")
    menu_widget_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)

    # win: win_widget
    win_widget = lv.obj(parent)
    objects["win_widget"] = win_widget
    win_widget.set_pos(50, 50)
    win_widget.set_size(300, 250)
    win_widget.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    win_widget.set_style_pad_all(0, lv.PART.MAIN)
    win_widget.set_style_pad_row(0, lv.PART.MAIN)
    win_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_widget_header = lv.obj(win_widget)
    win_widget_header.set_size(lv.pct(100), 40)
    win_widget_header.set_style_bg_color(lv.color_hex(0x2196F3), lv.PART.MAIN)
    win_widget_header.set_style_radius(0, lv.PART.MAIN)
    win_widget_title = lv.label(win_widget_header)
    win_widget_title.set_text("Window Title")
    win_widget_title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    win_widget_title.align(lv.ALIGN.LEFT_MID, 0, 0)
    win_widget_content = lv.obj(win_widget)
    win_widget_content.set_width(lv.pct(100))
    win_widget_content.set_flex_grow(1)

    # list: list_widget
    list_widget = lv.obj(parent)
    objects["list_widget"] = list_widget
    list_widget.set_pos(50, 50)
    list_widget.set_size(200, 300)
    list_widget.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    list_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    list_widget_item_1 = lv.button(list_widget)
    list_widget_item_1.set_width(lv.pct(100))
    list_widget_item_1_label = lv.label(list_widget_item_1)
    list_widget_item_1_label.set_text("Item 1")
    list_widget_item_1_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_widget_item_1_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_widget_item_2 = lv.button(list_widget)
    list_widget_item_2.set_width(lv.pct(100))
    list_widget_item_2_label = lv.label(list_widget_item_2)
    list_widget_item_2_label.set_text("Item 2")
    list_widget_item_2_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_widget_item_2_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_widget_item_3 = lv.button(list_widget)
    list_widget_item_3.set_width(lv.pct(100))
    list_widget_item_3_label = lv.label(list_widget_item_3)
    list_widget_item_3_label.set_text("Item 3")
    list_widget_item_3_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_widget_item_3_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_widget_item_4 = lv.button(list_widget)
    list_widget_item_4.set_width(lv.pct(100))
    list_widget_item_4_label = lv.label(list_widget_item_4)
    list_widget_item_4_label.set_text("Item 4")
    list_widget_item_4_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_widget_item_4_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    list_widget_item_5 = lv.button(list_widget)
    list_widget_item_5.set_width(lv.pct(100))
    list_widget_item_5_label = lv.label(list_widget_item_5)
    list_widget_item_5_label.set_text("Item 5")
    list_widget_item_5_label.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_widget_item_5_label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # msgbox: msgbox_widget
    msgbox_widget = lv.msgbox(parent)
    objects["msgbox_widget"] = msgbox_widget
    msgbox_widget.set_pos(50, 50)
    msgbox_widget.set_size(250, 180)
    msgbox_widget_title = msgbox_widget.add_title("Notice")
    msgbox_widget_text = msgbox_widget.add_text("This is a message box")
    msgbox_widget_button_1 = msgbox_widget.add_footer_button("OK")
    msgbox_widget_button_2 = msgbox_widget.add_footer_button("Cancel")
    msgbox_widget_close = msgbox_widget.add_close_button()
    msgbox_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # buttonmatrix: buttonmatrix_widget
    buttonmatrix_widget = lv.buttonmatrix(parent)
    objects["buttonmatrix_widget"] = buttonmatrix_widget
    buttonmatrix_widget.set_pos(50, 50)
    buttonmatrix_widget.set_size(250, 120)
    buttonmatrix_widget_map = ["1", "2", "3", "\n", "4", "5", "6", "\n", "7", "8", "9", "\n", "*", "0", "#", ""]
    buttonmatrix_widget.set_map(buttonmatrix_widget_map)
    buttonmatrix_widget.set_one_checked(True)
    buttonmatrix_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    buttonmatrix_widget.set_style_bg_color(lv.color_hex(0xE0E0E0), lv.PART.ITEMS)
    buttonmatrix_widget.set_style_text_color(lv.color_hex(0x000000), lv.PART.ITEMS)
    buttonmatrix_widget.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    # calendar: calendar_widget
    calendar_widget = lv.calendar(parent)
    objects["calendar_widget"] = calendar_widget
    calendar_widget.set_pos(50, 50)
    calendar_widget.set_size(230, 230)
    calendar_widget.set_today_date(2026, 10, 28)
    calendar_widget.set_month_shown(2026, 10)
    calendar_widget_header = calendar_widget.add_header_arrow()
    calendar_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    # line: line_widget
    line_widget = lv.line(parent)
    objects["line_widget"] = line_widget
    line_widget.set_pos(50, 50)
    line_widget_points = [{"x": 0, "y": 0}, {"x": 200, "y": 0}]
    line_widget.set_points(line_widget_points, 2)
    line_widget.set_style_line_color(lv.color_hex(0x000000), lv.PART.MAIN)
    line_widget.set_style_line_width(2, lv.PART.MAIN)
    line_widget.set_style_line_rounded(True, lv.PART.MAIN)

    # span: span_widget
    span_widget = lv.spangroup(parent)
    objects["span_widget"] = span_widget
    span_widget.set_pos(50, 50)
    span_widget.set_size(200, 60)
    span_widget.set_overflow(lv.SPAN_OVERFLOW.CLIP)
    span_widget.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_widget.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
    span_widget_span_1 = span_widget.add_span()
    span_widget_span_1.set_text("Normal text")
    span_widget_span_1_style = span_widget_span_1.get_style()
    span_widget_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_widget_span_1_style.set_text_font(lv.font_montserrat_14)
    span_widget_span_2 = span_widget.add_span()
    span_widget_span_2.set_text("Bold text")
    span_widget_span_2_style = span_widget_span_2.get_style()
    span_widget_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_widget_span_2_style.set_text_font(lv.font_montserrat_16)
    span_widget_span_3 = span_widget.add_span()
    span_widget_span_3.set_text("Small text")
    span_widget_span_3_style = span_widget_span_3.get_style()
    span_widget_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_widget_span_3_style.set_text_font(lv.font_montserrat_14)
    span_widget.refresh()

    # span: span_expand
    span_expand = lv.spangroup(parent)
    objects["span_expand"] = span_expand
    span_expand.set_pos(50, 50)
    span_expand.set_size(200, 60)
    span_expand.set_mode(lv.SPAN_MODE.EXPAND)
    span_expand.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
    span_expand_span_1 = span_expand.add_span()
    span_expand_span_1.set_text("Normal text")
    span_expand_span_1_style = span_expand_span_1.get_style()
    span_expand_span_1_style.set_text_color(lv.color_hex(0x000000))
    span_expand_span_1_style.set_text_font(lv.font_montserrat_14)
    span_expand_span_2 = span_expand.add_span()
    span_expand_span_2.set_text("Bold text")
    span_expand_span_2_style = span_expand_span_2.get_style()
    span_expand_span_2_style.set_text_color(lv.color_hex(0xFF0000))
    span_expand_span_2_style.set_text_font(lv.font_montserrat_16)
    span_expand_span_3 = span_expand.add_span()
    span_expand_span_3.set_text("Small text")
    span_expand_span_3_style = span_expand_span_3.get_style()
    span_expand_span_3_style.set_text_color(lv.color_hex(0x666666))
    span_expand_span_3_style.set_text_font(lv.font_montserrat_14)
    span_expand.refresh()

    # image: image_from_file
    image_from_file = lv.image(parent)
    objects["image_from_file"] = image_from_file
    image_from_file.set_pos(50, 50)
    image_from_file.set_size(100, 100)
    image_from_file.set_src("A:images/background.png")

    # image: image_gif
    image_gif = lv.image(parent)
    objects["image_gif"] = image_gif
    image_gif.set_pos(50, 50)
    image_gif.set_size(100, 100)

    # image: image_same_asset
    image_same_asset = lv.image(parent)
    objects["image_same_asset"] = image_same_asset
    image_same_asset.set_pos(50, 50)
    image_same_asset.set_size(100, 100)
    image_same_asset.set_src(img_logo)


def all_widgets_load_page(page_index):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            all_widgets_create_widgets(screens[0])

    lv.screen_load(screens[page_index])
    current_screen = page_index

def all_widgets_load_page_anim(page_index, anim, time_ms, delay_ms):
    global screens, current_screen

    if page_index < 0 or page_index >= 1:
        return

    if screens[page_index] is None:
        screens[page_index] = lv.obj()

        if page_index == 0:
            all_widgets_create_widgets(screens[0])

    lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)
    current_screen = page_index

def all_widgets_get_current_page():
    return current_screen

def all_widgets_init():
    global screens, current_screen
    screens = [None] * 1
    current_screen = 0
    all_widgets_load_page(0)
