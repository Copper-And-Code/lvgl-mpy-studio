import math

from .values import enum_member, has, to_int, v

DEFAULT_FONT_SIZE = 14
ANIM_PROPS = {"move_x": "x", "move_y": "y", "width": "width", "height": "height", "fade_in": "opa", "fade_out": "opa"}
BINDABLE_WIDGETS = {
    "slider": {"fn": "lv_slider_bind_value"}, "arc": {"fn": "lv_arc_bind_value"},
    "dropdown": {"fn": "lv_dropdown_bind_value"}, "roller": {"fn": "lv_roller_bind_value"},
    "switch": {"fn": "lv_obj_bind_checked"}, "checkbox": {"fn": "lv_obj_bind_checked"},
    "label": {"fn": "lv_label_bind_text", "format": True},
}


def lines(text):
    return [line.strip() for line in str(text or "").split("\n") if line.strip()]


def csv(text):
    return [item.strip() for item in str(text or "").split(",")]


def int_list(text):
    result = []
    for item in csv(text):
        if not item:
            continue
        try:
            number = float(item)
        except ValueError:
            continue
        if math.isfinite(number):
            result.append(math.floor(number + 0.5))
    return result


class Ops:
    def __init__(self, context, name):
        self.context, self.name = context, name
        self.self = v.ref(name)
        self.ops = []
        self.language = context["language"]
        self.widget = None
        self.parent = None

    @property
    def is_c(self):
        return self.language == "c"

    def push(self, op):
        self.ops.append(op)
        return self

    def comment(self, text):
        return self.push({"op": "comment", "text": text})

    def create(self, cls, parent):
        return self.push({"op": "create", "name": self.name, "cls": cls, "parent": parent})

    def on(self, target, fn, *args):
        if any(arg is None for arg in args):
            return self
        return self.push({"op": "call", "fn": fn, "target": target, "args": list(args)})

    def set(self, fn, *args):
        return self.on(self.self, fn, *args)

    def assign(self, base, ctype, fn, target, *args):
        name = self.context["temp"](base)
        self.push({"op": "call", "fn": fn, "target": target, "args": list(args), "assign": {"name": name, "ctype": ctype}})
        return name

    def construct(self, base, fn, cls, *args):
        name = self.context["temp"](base)
        self.push({"op": "construct", "name": name, "fn": fn, "cls": cls, "args": list(args)})
        return name

    def array(self, base, ctype, items):
        name = self.context["temp"](base)
        self.push({"op": "array", "name": name, "ctype": ctype, "items": items})
        return name

    def style(self, prop, value, selector=None):
        return self.set(f"lv_obj_set_style_{prop}", value, selector or v.sel())

    def font_value(self, size):
        custom = (self.widget or {}).get("props", {}).get("font")
        return v.font(size, self.context["font"](custom, to_int(size, DEFAULT_FONT_SIZE), self.widget) if custom else None)

    def font(self, size, target=None):
        target = target or self.self
        if not has(size) and not (self.widget or {}).get("props", {}).get("font"):
            return self
        return self.on(target, "lv_obj_set_style_text_font", self.font_value(size if has(size) else DEFAULT_FONT_SIZE), v.sel())

    def pos(self, props):
        return self.set("lv_obj_set_pos", v.int(props.get("x")), v.int(props.get("y")))

    def size(self, props):
        return self.set("lv_obj_set_size", v.int(props.get("width"), 100), v.int(props.get("height"), 100))


def add_button_label(b, p):
    if not p.get("text"):
        return
    label = b.construct(f"{b.name}_label", "lv_label_create", "label", b.self)
    ref = v.ref(label)
    b.on(ref, "lv_label_set_text", v.str(p["text"]))
    b.on(ref, "lv_obj_center")
    b.on(ref, "lv_obj_set_style_text_color", v.color(p.get("textColor")), v.sel())
    b.font(p.get("fontSize"), ref)


def flex_column(b, p):
    b.create("obj", b.parent).pos(p).size(p)
    b.set("lv_obj_set_flex_flow", v.enum("FLEX_FLOW", "COLUMN"))


def item_button(b, base, text, p):
    button = b.construct(base, "lv_button_create", "button", b.self)
    b.on(v.ref(button), "lv_obj_set_width", v.pct(100))
    label = b.construct(f"{base}_label", "lv_label_create", "label", v.ref(button))
    b.on(v.ref(label), "lv_label_set_text", v.str(text))
    b.on(v.ref(label), "lv_obj_set_style_text_color", v.color(p.get("textColor")), v.sel())
    b.font(p.get("fontSize"), v.ref(label))


def animate(b, prop, start, end, duration, delay=0, repeat=None, reverse=False, path="linear"):
    anim = b.context["temp"](f"{b.name}_anim")
    target = v.ref(anim)
    target["struct"] = True
    b.push({"op": "struct", "name": anim, "ctype": "lv_anim_t", "pyType": "anim_t"})
    b.on(target, "lv_anim_init")
    b.on(target, "lv_anim_set_var", b.self)
    b.on(target, "lv_anim_set_values", v.int(start), v.int(end))
    b.on(target, "lv_anim_set_duration", v.int(duration, 1000))
    if to_int(delay) > 0:
        b.on(target, "lv_anim_set_delay", v.int(delay))
    if repeat:
        b.on(target, "lv_anim_set_repeat_count", repeat)
    if reverse:
        b.on(target, "lv_anim_set_reverse_duration", v.int(duration, 1000))
    b.on(target, "lv_anim_set_path_cb", v.anim_path(path))
    b.push({"op": "animExec", "anim": anim, "target": b.self, "prop": prop})
    b.on(target, "lv_anim_start")


LABEL_LONG_MODES = ["WRAP", "DOTS", "SCROLL", "SCROLL_CIRCULAR", "CLIP"]
TEXT_ALIGNS = ["AUTO", "LEFT", "CENTER", "RIGHT"]
DIRS = ["NONE", "LEFT", "RIGHT", "TOP", "BOTTOM", "HOR", "VER", "ALL"]
BAR_MODES = ["NORMAL", "SYMMETRICAL", "RANGE"]
ARC_MODES = ["NORMAL", "SYMMETRICAL", "REVERSE"]
FLEX_FLOWS = ["ROW", "COLUMN", "ROW_WRAP", "ROW_REVERSE", "ROW_WRAP_REVERSE", "COLUMN_WRAP", "COLUMN_REVERSE", "COLUMN_WRAP_REVERSE"]
FLEX_ALIGNS = ["START", "END", "CENTER", "SPACE_EVENLY", "SPACE_AROUND", "SPACE_BETWEEN"]
SCROLLBAR_MODES = ["OFF", "ON", "ACTIVE", "AUTO"]


def button(b, p):
    b.create("button", b.parent).pos(p).size(p)
    b.style("bg_color", v.color(p.get("bgColor")))
    if has(p.get("radius")): b.style("radius", v.int(p.get("radius")))
    add_button_label(b, p)


def label(b, p):
    b.create("label", b.parent).pos(p).size(p)
    b.set("lv_label_set_text", v.str(p.get("text", "Label")))
    b.style("text_color", v.color(p.get("textColor")))
    b.font(p.get("fontSize"))
    mode = enum_member(p.get("longMode"), "LABEL_LONG_MODE", LABEL_LONG_MODES)
    if mode and mode != "WRAP": b.set("lv_label_set_long_mode", v.enum("LABEL_LONG_MODE", mode))
    align = enum_member(p.get("textAlign"), "TEXT_ALIGN", TEXT_ALIGNS)
    if align: b.style("text_align", v.enum("TEXT_ALIGN", align))
    if p.get("recolor"): b.set("lv_label_set_recolor", v.bool(True))


def slider(b, p):
    b.create("slider", b.parent).pos(p).size(p)
    b.set("lv_slider_set_range", v.int(p.get("min"), 0), v.int(p.get("max"), 100))
    mode = "RANGE" if p.get("mode") == "range" or p.get("isRange") else "SYMMETRICAL" if p.get("mode") == "symmetrical" else None
    if mode: b.set("lv_slider_set_mode", v.enum("SLIDER_MODE", mode))
    b.set("lv_slider_set_value", v.int(p.get("value"), 50), v.anim_enable(False))
    if mode == "RANGE" and has(p.get("leftValue")): b.set("lv_slider_set_start_value", v.int(p.get("leftValue")), v.anim_enable(False))
    b.style("bg_color", v.color(p.get("bgColor")))
    b.style("bg_color", v.color(p.get("indicatorColor")), v.sel("INDICATOR"))
    b.style("bg_color", v.color(p.get("knobColor")), v.sel("KNOB"))


def switch(b, p):
    b.create("switch", b.parent).pos(p).size(p)
    if p.get("checked"): b.set("lv_obj_add_state", v.enum("STATE", "CHECKED"))
    b.style("bg_color", v.color(p.get("offColor")))
    b.style("bg_color", v.color(p.get("onColor")), v.sel("INDICATOR", "CHECKED"))
    b.style("bg_color", v.color(p.get("knobColor")), v.sel("KNOB"))


def checkbox(b, p):
    b.create("checkbox", b.parent).pos(p)
    b.set("lv_checkbox_set_text", v.str(p.get("text", "Checkbox")))
    if p.get("checked"): b.set("lv_obj_add_state", v.enum("STATE", "CHECKED"))
    b.style("text_color", v.color(p.get("textColor")))
    b.font(p.get("fontSize"))
    b.style("bg_color", v.color(p.get("checkedColor")), v.sel("INDICATOR", "CHECKED"))


def textarea(b, p):
    b.create("textarea", b.parent).pos(p).size(p)
    if p.get("oneLine"): b.set("lv_textarea_set_one_line", v.bool(True))
    if p.get("password"): b.set("lv_textarea_set_password_mode", v.bool(True))
    if to_int(p.get("maxLength")) > 0: b.set("lv_textarea_set_max_length", v.int(p.get("maxLength")))
    if p.get("acceptedChars"): b.set("lv_textarea_set_accepted_chars", v.str(p.get("acceptedChars")))
    if p.get("text"): b.set("lv_textarea_set_text", v.str(p.get("text")))
    if p.get("placeholder"): b.set("lv_textarea_set_placeholder_text", v.str(p.get("placeholder")))
    b.style("bg_color", v.color(p.get("bgColor")))
    b.style("text_color", v.color(p.get("textColor")))
    b.font(p.get("fontSize"))


def dropdown(b, p):
    b.create("dropdown", b.parent).pos(p).size(p)
    if p.get("options"): b.set("lv_dropdown_set_options", v.str("\n".join(lines(p["options"]))))
    if to_int(p.get("selected")) > 0: b.set("lv_dropdown_set_selected", v.int(p.get("selected")))
    direction = enum_member(p.get("dir"), "DIR", DIRS)
    if direction and direction != "BOTTOM": b.set("lv_dropdown_set_dir", v.enum("DIR", direction))
    b.style("bg_color", v.color(p.get("bgColor")))
    b.style("text_color", v.color(p.get("textColor")))
    b.font(p.get("fontSize"))


def roller(b, p):
    b.create("roller", b.parent).pos(p).size(p)
    if p.get("options"): b.set("lv_roller_set_options", v.str("\n".join(lines(p["options"]))), v.enum("ROLLER_MODE", "INFINITE" if p.get("infinite") else "NORMAL"))
    if to_int(p.get("selected")) > 0: b.set("lv_roller_set_selected", v.int(p.get("selected")), v.anim_enable(False))
    if to_int(p.get("visibleRows")) > 0: b.set("lv_roller_set_visible_row_count", v.int(p.get("visibleRows")))
    b.style("bg_color", v.color(p.get("bgColor")))
    b.style("bg_color", v.color(p.get("selectedColor")), v.sel("SELECTED"))
    b.style("text_color", v.color(p.get("textColor")))
    b.font(p.get("fontSize"))


def spinbox(b, p):
    b.create("spinbox", b.parent).pos(p).size(p)
    digits = min(max(to_int(p.get("digitCount"), 4), 1), 10)
    separator = min(max(to_int(p.get("separatorPos"), 0), 0), digits)
    b.set("lv_spinbox_set_digit_format", v.int(digits), v.int(separator))
    b.set("lv_spinbox_set_range", v.int(p.get("min"), 0), v.int(p.get("max"), 999))
    b.set("lv_spinbox_set_value", v.int(p.get("value"), 0))
    if to_int(p.get("step"), 1) > 1: b.set("lv_spinbox_set_step", v.int(p.get("step")))
    if p.get("rollover"): b.set("lv_spinbox_set_rollover", v.bool(True))
    b.style("bg_color", v.color(p.get("bgColor")))
    b.style("text_color", v.color(p.get("textColor")))
    b.font(p.get("fontSize"))


def keyboard(b, p):
    b.create("keyboard", b.parent).pos(p).size(p)
    mode = {"text_lower": "TEXT_LOWER", "text_upper": "TEXT_UPPER", "text_special": "SPECIAL", "number": "NUMBER"}.get(p.get("mode"))
    if mode and mode != "TEXT_LOWER": b.set("lv_keyboard_set_mode", v.enum("KEYBOARD_MODE", mode))
    if p.get("popover") is False: b.set("lv_keyboard_set_popovers", v.bool(False))


def panel(b, p):
    b.create("obj", b.parent).pos(p).size(p)
    b.style("bg_color", v.color(p.get("bgColor")))
    if has(p.get("borderWidth")): b.style("border_width", v.int(p.get("borderWidth")))
    if to_int(p.get("borderWidth")) > 0: b.style("border_color", v.color(p.get("borderColor")))
    if has(p.get("radius")): b.style("radius", v.int(p.get("radius")))


def bar(b, p):
    b.create("bar", b.parent).pos(p).size(p)
    b.set("lv_bar_set_range", v.int(p.get("min"), 0), v.int(p.get("max"), 100))
    mode = enum_member(p.get("mode"), "BAR_MODE", BAR_MODES)
    if mode and mode != "NORMAL": b.set("lv_bar_set_mode", v.enum("BAR_MODE", mode))
    b.set("lv_bar_set_value", v.int(p.get("value"), 50), v.anim_enable(False))
    if mode == "RANGE" and has(p.get("startValue")): b.set("lv_bar_set_start_value", v.int(p.get("startValue")), v.anim_enable(False))
    b.style("bg_color", v.color(p.get("bgColor")))
    b.style("bg_color", v.color(p.get("indicatorColor")), v.sel("INDICATOR"))


def arc(b, p):
    b.create("arc", b.parent).pos(p).size(p)
    if to_int(p.get("rotation")): b.set("lv_arc_set_rotation", v.int(p.get("rotation")))
    if has(p.get("startAngle")) and has(p.get("endAngle")): b.set("lv_arc_set_bg_angles", v.int(p.get("startAngle")), v.int(p.get("endAngle")))
    mode = enum_member(p.get("mode"), "ARC_MODE", ARC_MODES)
    if mode and mode != "NORMAL": b.set("lv_arc_set_mode", v.enum("ARC_MODE", mode))
    b.set("lv_arc_set_range", v.int(p.get("min"), 0), v.int(p.get("max"), 100))
    b.set("lv_arc_set_value", v.int(p.get("value"), 50))
    if to_int(p.get("lineWidth")) > 0:
        b.style("arc_width", v.int(p.get("lineWidth")))
        b.style("arc_width", v.int(p.get("lineWidth")), v.sel("INDICATOR"))
    b.style("arc_color", v.color(p.get("bgColor")))
    b.style("arc_color", v.color(p.get("indicatorColor")), v.sel("INDICATOR"))
    b.style("bg_color", v.color(p.get("knobColor")), v.sel("KNOB"))


def spinner(b, p):
    b.create("arc", b.parent).pos(p).size(p)
    b.set("lv_arc_set_bg_angles", v.int(0), v.int(360))
    b.set("lv_arc_set_angles", v.int(0), v.int(p.get("arcLength"), 60))
    b.set("lv_obj_remove_style", v.null(), v.sel("KNOB"))
    b.set("lv_obj_remove_flag", v.enum("OBJ_FLAG", "CLICKABLE"))
    animate(b, "rotation", 0, 360, to_int(p.get("speed"), 1000), repeat=v.constant("ANIM_REPEAT_INFINITE"))
    if to_int(p.get("lineWidth")) > 0:
        b.style("arc_width", v.int(p.get("lineWidth")))
        b.style("arc_width", v.int(p.get("lineWidth")), v.sel("INDICATOR"))
    b.style("arc_color", v.color(p.get("color")), v.sel("INDICATOR"))


def led(b, p):
    b.create("led", b.parent).pos(p).size(p)
    b.set("lv_led_set_color", v.color(p.get("color")))
    if has(p.get("brightness")): b.set("lv_led_set_brightness", v.int(p.get("brightness"), 255))


def chart(b, p):
    b.create("chart", b.parent).pos(p).size(p)
    kind = {"line": "LINE", "bar": "BAR", "scatter": "SCATTER"}.get(p.get("chartType"), "LINE")
    b.set("lv_chart_set_type", v.enum("CHART_TYPE", kind))
    if to_int(p.get("pointCount")) > 0: b.set("lv_chart_set_point_count", v.int(p.get("pointCount")))
    if has(p.get("divLineCount")): b.set("lv_chart_set_div_line_count", v.int(p.get("divLineCount"), 3), v.int(p.get("divLineCountSec"), 5))
    b.set("lv_chart_set_axis_range", v.enum("CHART_AXIS", "PRIMARY_Y"), v.int(p.get("rangeYMin"), 0), v.int(p.get("rangeYMax"), 100))
    if p.get("updateMode") == "circular": b.set("lv_chart_set_update_mode", v.enum("CHART_UPDATE_MODE", "CIRCULAR"))
    b.style("bg_color", v.color(p.get("bgColor")))
    for index, (data, color) in enumerate([(p.get("data"), p.get("lineColor", "#2196F3")), (p.get("data2"), p.get("lineColor2", "#FF5722"))]):
        if index > 0 and not data: continue
        series = b.assign(f"{b.name}_series_{index + 1}", "lv_chart_series_t *", "lv_chart_add_series", b.self, v.color(color) or v.color("#2196F3"), v.enum("CHART_AXIS", "PRIMARY_Y"))
        for value in int_list(data): b.set("lv_chart_set_next_value", v.ref(series), v.int(value))


def table(b, p):
    b.create("table", b.parent).pos(p).size(p)
    cols = max(to_int(p.get("cols"), 3), 1)
    b.set("lv_table_set_column_count", v.int(cols))
    for column, width in enumerate(int_list(p.get("colWidths"))[:cols]): b.set("lv_table_set_column_width", v.int(column), v.int(width))
    rows = []
    if p.get("headerRow"): rows.append(csv(p["headerRow"]))
    rows.extend(csv(row) for row in lines(p.get("cellData")))
    for row, cells in enumerate(rows):
        for column, cell in enumerate(cells[:cols]): b.set("lv_table_set_cell_value", v.int(row), v.int(column), v.str(cell))
    b.style("bg_color", v.color(p.get("bgColor")), v.sel("ITEMS"))
    b.style("text_color", v.color(p.get("textColor")), v.sel("ITEMS"))
    b.style("border_color", v.color(p.get("borderColor")), v.sel("ITEMS"))
    b.font(p.get("fontSize"))


def scale(b, p):
    b.create("scale", b.parent).pos(p).size(p)
    mode = {"horizontal": "HORIZONTAL_BOTTOM", "vertical": "VERTICAL_LEFT", "round_inner": "ROUND_INNER", "round_outer": "ROUND_OUTER"}.get(p.get("mode"), "HORIZONTAL_BOTTOM")
    b.set("lv_scale_set_mode", v.enum("SCALE_MODE", mode))
    minimum, maximum = to_int(p.get("min"), 0), to_int(p.get("max"), 100)
    b.set("lv_scale_set_range", v.int(minimum), v.int(maximum))
    major_step = max(to_int(p.get("majorTickEvery"), 10), 1)
    minor_per_major = max(to_int(p.get("minorTickCount"), 4), 0) + 1
    major_count = max(math.floor(abs(maximum - minimum) / major_step + 0.5), 1)
    b.set("lv_scale_set_total_tick_count", v.int(major_count * minor_per_major + 1))
    b.set("lv_scale_set_major_tick_every", v.int(minor_per_major))
    if p.get("labelShow") is False: b.set("lv_scale_set_label_show", v.bool(False))
    if has(p.get("majorTickLength")): b.style("length", v.int(p.get("majorTickLength")), v.sel("INDICATOR"))
    if has(p.get("minorTickLength")): b.style("length", v.int(p.get("minorTickLength")), v.sel("ITEMS"))
    b.style("line_color", v.color(p.get("lineColor")), v.sel("INDICATOR"))
    b.style("text_color", v.color(p.get("textColor")), v.sel("INDICATOR"))


def image(b, p):
    b.create("image", b.parent).pos(p).size(p)
    if p.get("src"): b.set("lv_image_set_src", b.context["image"](p["src"]))
    if to_int(p.get("rotation")): b.set("lv_image_set_rotation", v.int(p.get("rotation")))
    if has(p.get("zoom")) and to_int(p.get("zoom"), 256) != 256: b.set("lv_image_set_scale", v.int(p.get("zoom"), 256))
    if to_int(p.get("pivotX")) or to_int(p.get("pivotY")): b.set("lv_image_set_pivot", v.int(p.get("pivotX")), v.int(p.get("pivotY")))
    if p.get("antialias") is False: b.set("lv_image_set_antialias", v.bool(False))


def imagebutton(b, p):
    b.create("imagebutton", b.parent).pos(p).size(p)
    if p.get("src"): b.set("lv_imagebutton_set_src", v.enum("IMAGEBUTTON_STATE", "RELEASED"), v.null(), b.context["image"](p["src"]), v.null())
    b.style("bg_color", v.color(p.get("bgColor")))
    if has(p.get("radius")): b.style("radius", v.int(p.get("radius")))
    add_button_label(b, p)


def tabview(b, p):
    b.create("tabview", b.parent).pos(p).size(p)
    position = {"top": "TOP", "bottom": "BOTTOM", "left": "LEFT", "right": "RIGHT"}.get(p.get("tabPosition"), "TOP")
    b.set("lv_tabview_set_tab_bar_position", v.enum("DIR", position))
    b.set("lv_tabview_set_tab_bar_size", v.int(p.get("tabBarSize"), 40))
    tabs = lines(p.get("tabs"))
    for index, tab in enumerate(tabs): b.assign(f"{b.name}_tab_{index + 1}", "lv_obj_t *", "lv_tabview_add_tab", b.self, v.str(tab))
    active = to_int(p.get("activeTab"), 0)
    if active > 0 and active < len(tabs): b.set("lv_tabview_set_active", v.int(active), v.anim_enable(False))
    b.style("bg_color", v.color(p.get("bgColor")))


def tileview(b, p):
    b.create("tileview", b.parent).pos(p).size(p)
    rows, cols = min(max(to_int(p.get("rows"), 2), 1), 16), min(max(to_int(p.get("cols"), 2), 1), 16)
    for row in range(rows):
        for col in range(cols): b.set("lv_tileview_add_tile", v.int(col), v.int(row), v.enum("DIR", "ALL"))
    b.style("bg_color", v.color(p.get("bgColor")))


def menu(b, p):
    flex_column(b, p)
    b.style("bg_color", v.color(p.get("bgColor")))
    title = b.construct(f"{b.name}_title", "lv_label_create", "label", b.self)
    b.on(v.ref(title), "lv_label_set_text", v.str(p.get("headerTitle", "Menu")))
    b.on(v.ref(title), "lv_obj_set_style_text_color", v.color(p.get("textColor")), v.sel())
    for index, item in enumerate(lines(p.get("items"))): item_button(b, f"{b.name}_item_{index + 1}", item, p)


def win(b, p):
    flex_column(b, p)
    b.style("pad_all", v.int(0)); b.style("pad_row", v.int(0)); b.style("bg_color", v.color(p.get("bgColor")))
    header = b.construct(f"{b.name}_header", "lv_obj_create", "obj", b.self)
    href = v.ref(header)
    b.on(href, "lv_obj_set_size", v.pct(100), v.int(p.get("headerHeight"), 40))
    b.on(href, "lv_obj_set_style_bg_color", v.color(p.get("headerBgColor")), v.sel())
    b.on(href, "lv_obj_set_style_radius", v.int(0), v.sel())
    title = b.construct(f"{b.name}_title", "lv_label_create", "label", href)
    b.on(v.ref(title), "lv_label_set_text", v.str(p.get("title", "")))
    b.on(v.ref(title), "lv_obj_set_style_text_color", v.color(p.get("titleColor")), v.sel())
    b.on(v.ref(title), "lv_obj_align", v.enum("ALIGN", "LEFT_MID"), v.int(0), v.int(0))
    content = b.construct(f"{b.name}_content", "lv_obj_create", "obj", b.self)
    b.on(v.ref(content), "lv_obj_set_width", v.pct(100))
    b.on(v.ref(content), "lv_obj_set_flex_grow", v.int(1))


def list_widget(b, p):
    flex_column(b, p)
    b.style("bg_color", v.color(p.get("bgColor")))
    for index, item in enumerate(lines(p.get("items"))): item_button(b, f"{b.name}_item_{index + 1}", item, p)


def msgbox(b, p):
    b.create("msgbox", b.parent).pos(p).size(p)
    b.assign(f"{b.name}_title", "lv_obj_t *", "lv_msgbox_add_title", b.self, v.str(p.get("title", "Notice")))
    if p.get("text"): b.assign(f"{b.name}_text", "lv_obj_t *", "lv_msgbox_add_text", b.self, v.str(p["text"]))
    for index, text in enumerate(lines(p.get("buttons"))): b.assign(f"{b.name}_button_{index + 1}", "lv_obj_t *", "lv_msgbox_add_footer_button", b.self, v.str(text))
    if p.get("closeButton"): b.assign(f"{b.name}_close", "lv_obj_t *", "lv_msgbox_add_close_button", b.self)
    b.style("bg_color", v.color(p.get("bgColor")))


def buttonmatrix(b, p):
    b.create("buttonmatrix", b.parent).pos(p).size(p)
    rows = [[button for button in csv(row) if button] for row in lines(p.get("map"))]
    if rows:
        items = []
        for index, row in enumerate(rows):
            items.extend(v.str(text) for text in row)
            if index < len(rows) - 1: items.append(v.str("\n"))
        items.append(v.str(""))
        array = b.array(f"{b.name}_map", "const char *", items)
        b.set("lv_buttonmatrix_set_map", v.ref(array))
    if p.get("oneCheck"): b.set("lv_buttonmatrix_set_one_checked", v.bool(True))
    b.style("bg_color", v.color(p.get("bgColor")))
    b.style("bg_color", v.color(p.get("btnColor")), v.sel("ITEMS"))
    b.style("text_color", v.color(p.get("textColor")), v.sel("ITEMS"))
    b.font(p.get("fontSize"))


def calendar(b, p):
    b.create("calendar", b.parent).pos(p).size(p)
    year, month, day = to_int(p.get("year"), 2026), min(max(to_int(p.get("month"), 1), 1), 12), min(max(to_int(p.get("day"), 1), 1), 31)
    b.set("lv_calendar_set_today_date", v.int(year), v.int(month), v.int(day))
    b.set("lv_calendar_set_month_shown", v.int(year), v.int(month))
    if p.get("showHeader"): b.assign(f"{b.name}_header", "lv_obj_t *", "lv_calendar_add_header_arrow", b.self)
    b.style("bg_color", v.color(p.get("bgColor")))


def line(b, p):
    b.create("line", b.parent).pos(p)
    points = []
    for pair in str(p.get("points") or "").strip().split():
        try:
            values = [float(value) for value in pair.split(",")]
        except ValueError:
            continue
        if len(values) == 2 and all(math.isfinite(value) for value in values):
            points.append({"k": "point", "x": math.floor(values[0] + 0.5), "y": math.floor(values[1] + 0.5)})
    if len(points) >= 2:
        array = b.array(f"{b.name}_points", "lv_point_precise_t", points)
        b.set("lv_line_set_points", v.ref(array), v.int(len(points)))
    b.style("line_color", v.color(p.get("lineColor")))
    if has(p.get("lineWidth")): b.style("line_width", v.int(p.get("lineWidth")))
    if p.get("rounded"): b.style("line_rounded", v.bool(True))


def span(b, p):
    b.create("spangroup", b.parent).pos(p).size(p)
    mode = {"wrap": "FIXED", "expand": "EXPAND", "break": "BREAK", "clip": "FIXED"}.get(p.get("mode"))
    if b.is_c:
        if mode == "EXPAND": b.set("lv_obj_set_size", v.constant("SIZE_CONTENT"), v.constant("SIZE_CONTENT"))
        if mode == "BREAK": b.set("lv_obj_set_height", v.constant("SIZE_CONTENT"))
    elif mode and mode != "FIXED":
        b.set("lv_spangroup_set_mode", v.enum("SPAN_MODE", mode))
    if p.get("mode") == "clip": b.set("lv_spangroup_set_overflow", v.enum("SPAN_OVERFLOW", "CLIP"))
    b.style("bg_color", v.color(p.get("bgColor")))
    b.font(p.get("fontSize"))
    for index, definition in enumerate(lines(p.get("spans"))):
        parts = [part.strip() for part in definition.split("|")]
        text, size, color = (parts + ["", None, None])[:3]
        item = b.assign(f"{b.name}_span_{index + 1}", "lv_span_t *", "lv_spangroup_add_span", b.self)
        b.on(v.ref(item), "lv_span_set_text", v.str(text))
        style = b.assign(f"{item}_style", "lv_style_t *", "lv_span_get_style", v.ref(item))
        b.on(v.ref(style), "lv_style_set_text_color", v.color(color))
        if size: b.on(v.ref(style), "lv_style_set_text_font", b.font_value(size))
    b.set("lv_spangroup_refresh")


BUILDERS = {name: obj for name, obj in list(globals().items()) if name in {
    "button", "label", "slider", "switch", "checkbox", "textarea", "dropdown", "roller", "spinbox", "keyboard", "panel", "bar", "arc", "spinner", "led", "chart", "table", "scale", "image", "imagebutton", "tabview", "tileview", "menu", "win", "msgbox", "buttonmatrix", "calendar", "line", "span"
}}
BUILDERS["list"] = list_widget
SUPPORTED_WIDGET_TYPES = list(BUILDERS)


def common_styles(b, p):
    if has(p.get("opacity")) and to_int(p.get("opacity"), 255) != 255: b.style("opa", v.int(p.get("opacity"), 255))
    if has(p.get("bgOpa")): b.style("bg_opa", v.int(p.get("bgOpa"), 255))
    sides = [("padTop", "pad_top"), ("padBottom", "pad_bottom"), ("padLeft", "pad_left"), ("padRight", "pad_right")]
    values = [to_int(p[prop]) if has(p.get(prop)) else None for prop, _style in sides]
    if all(value is not None and value == values[0] for value in values):
        b.style("pad_all", v.int(values[0]))
    else:
        for prop, style in sides:
            if has(p.get(prop)): b.style(style, v.int(p[prop]))
    if has(p.get("padRow")) and has(p.get("padColumn")) and to_int(p["padRow"]) == to_int(p["padColumn"]):
        b.style("pad_gap", v.int(p["padRow"]))
    else:
        if has(p.get("padRow")): b.style("pad_row", v.int(p["padRow"]))
        if has(p.get("padColumn")): b.style("pad_column", v.int(p["padColumn"]))
    if to_int(p.get("shadowWidth")):
        b.style("shadow_width", v.int(p["shadowWidth"])); b.style("shadow_color", v.color(p.get("shadowColor")))
        if to_int(p.get("shadowOffsetX")): b.style("shadow_offset_x", v.int(p["shadowOffsetX"]))
        if to_int(p.get("shadowOffsetY")): b.style("shadow_offset_y", v.int(p["shadowOffsetY"]))
        if to_int(p.get("shadowSpread")): b.style("shadow_spread", v.int(p["shadowSpread"]))
    if to_int(p.get("outlineWidth")):
        b.style("outline_width", v.int(p["outlineWidth"])); b.style("outline_color", v.color(p.get("outlineColor")))
        if to_int(p.get("outlinePad")): b.style("outline_pad", v.int(p["outlinePad"]))
    for prop, style in [("transformRotation", "transform_rotation"), ("transformScaleX", "transform_scale_x"), ("transformScaleY", "transform_scale_y"), ("transformPivotX", "transform_pivot_x"), ("transformPivotY", "transform_pivot_y")]:
        if to_int(p.get(prop)): b.style(style, v.int(p[prop]))
    flow = enum_member(p.get("flexFlow"), "FLEX_FLOW", FLEX_FLOWS)
    if flow:
        b.set("lv_obj_set_flex_flow", v.enum("FLEX_FLOW", flow))
        main = enum_member(p.get("flexMainPlace"), "FLEX_ALIGN", FLEX_ALIGNS)
        if main:
            cross = enum_member(p.get("flexCrossPlace"), "FLEX_ALIGN", FLEX_ALIGNS) or "START"
            b.set("lv_obj_set_flex_align", v.enum("FLEX_ALIGN", main), v.enum("FLEX_ALIGN", cross), v.enum("FLEX_ALIGN", cross))
    scrollbar = enum_member(p.get("scrollbarMode"), "SCROLLBAR_MODE", SCROLLBAR_MODES)
    if scrollbar and scrollbar != "AUTO": b.set("lv_obj_set_scrollbar_mode", v.enum("SCROLLBAR_MODE", scrollbar))
    scroll_dir = enum_member(p.get("scrollDir"), "DIR", DIRS)
    if scroll_dir: b.set("lv_obj_set_scroll_dir", v.enum("DIR", scroll_dir))
    if p.get("hidden"):
        b.set("lv_obj_set_hidden", v.bool(True)) if b.is_c else b.set("lv_obj_add_flag", v.enum("OBJ_FLAG", "HIDDEN"))
    if p.get("clickable") is False:
        b.set("lv_obj_set_clickable", v.bool(False)) if b.is_c else b.set("lv_obj_remove_flag", v.enum("OBJ_FLAG", "CLICKABLE"))
    if p.get("disabled"): b.set("lv_obj_add_state", v.enum("STATE", "DISABLED"))


CUSTOM_STYLE_PROPS = {"bg_color": "color", "bg_opa": "int", "border_color": "color", "border_width": "int", "border_opa": "int", "pad_top": "int", "pad_bottom": "int", "pad_left": "int", "pad_right": "int", "text_color": "color", "text_font_size": "font", "radius": "int", "shadow_width": "int", "shadow_ofs_x": "int", "shadow_ofs_y": "int", "shadow_color": "color"}
CUSTOM_STYLE_NAMES = {"shadow_ofs_x": "shadow_offset_x", "shadow_ofs_y": "shadow_offset_y"}


def build_widget_ops(node, context):
    widget, name = node["widget"], node["name"]
    b = Ops(context, name)
    b.widget = widget
    b.parent = v.ref(node["parentName"]) if node.get("parentName") else v.ref("parent")
    props = widget.get("props") or {}
    b.comment(f"{widget['type']}: {widget.get('name') or name}")
    builder = BUILDERS.get(widget["type"])
    if not builder:
        b.comment(f"Unsupported widget type \"{widget['type']}\"")
        return b.ops
    builder(b, props)
    common_styles(b, props)
    for key, value in (widget.get("customStyles") or {}).items():
        kind = CUSTOM_STYLE_PROPS.get(key)
        if not kind or not has(value): continue
        if kind == "font": b.font(value)
        else: b.style(CUSTOM_STYLE_NAMES.get(key, key), v.color(value) if kind == "color" else v.int(value))
    bindable = BINDABLE_WIDGETS.get(widget["type"])
    variable = context["variable"](widget["binding"]["variableId"]) if bindable and widget.get("binding") else None
    if variable:
        args = [v.ref(variable), v.str(widget["binding"].get("format") or "%d")] if bindable.get("format") else [v.ref(variable)]
        b.set(bindable["fn"], *args)
    for event in widget.get("events") or []:
        handler = context["callback_for"](widget, event)
        if handler: b.set("lv_obj_add_event_cb", {"k": "fn", "name": handler["name"]}, v.enum("EVENT", handler["eventCode"]), v.null())
    for animation in widget.get("animations") or []:
        prop = ANIM_PROPS.get(animation.get("type"))
        if not prop:
            b.comment(f"Animation type \"{animation.get('type')}\" is not supported by the code generator")
            continue
        repeat = v.int(animation.get("repeat")) if to_int(animation.get("repeat")) > 0 else None
        animate(b, prop, animation.get("startValue"), animation.get("endValue"), animation.get("duration"), animation.get("delay", 0), repeat, bool(animation.get("playback")), animation.get("path", "linear"))
    return b.ops
