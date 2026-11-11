import re
from pathlib import Path

from .components import project_components
from .output.c_templates import MAIN_TEMPLATE, MAKEFILE_TEMPLATE
from lvgl_mpy_studio.core.i18n import tr
from .escaping import c_comment_lines, c_string, comment_text
from .values import C_FONT_SIZES, nearest_font_size

NEW_HANDLERS_BEGIN = "// <lms:new-handlers>"
NEW_HANDLERS_END = "// </lms:new-handlers>"
OLD_HANDLERS_END = "// </lvgl-ide:new-handlers>"  # in files exported up to 0.4


class CEmitter:
    def __init__(self, context):
        self.context = context

    def name(self, identifier):
        name = self.context.get("widgetNames", {}).get(identifier, identifier)
        return f"ui_{name}" if self.context["isWidget"](identifier) else name

    def value(self, value):
        kind = value["k"]
        if kind == "int": return str(value["value"])
        if kind == "str": return c_string(value["value"])
        if kind == "bool": return "true" if value["value"] else "false"
        if kind == "color": return f"lv_color_hex(0x{value['value']:06X})"
        if kind == "enum": return f"LV_{value['enumName']}_{value['member']}"
        if kind == "sel": return " | ".join(filter(None, [f"LV_PART_{value['part']}", f"LV_STATE_{value['state']}" if value.get("state") else None]))
        if kind == "font":
            if value.get("symbol"): return value["symbol"]  # a pointer, set by ui_load_fonts
            size = nearest_font_size(value["size"], C_FONT_SIZES)
            self.context["fonts"].add(size)
            return f"&lv_font_montserrat_{size}"
        if kind == "ref": return f"&{self.name(value['name'])}" if value.get("struct") else self.name(value["name"])
        if kind == "fn": return value["name"]
        if kind == "null": return "NULL"
        if kind == "pct": return f"lv_pct({value['value']})"
        if kind == "constant": return f"LV_{value['name']}"
        if kind == "animEnable": return "LV_ANIM_ON" if value["value"] else "LV_ANIM_OFF"
        if kind == "animPath": return f"lv_anim_path_{value['name']}"
        if kind == "image": return f"&{value['symbol']}" if value.get("symbol") else c_string(value["source"])
        if kind == "point": return f"{{{value['x']}, {value['y']}}}"
        raise ValueError(f"Unknown value kind {kind}")

    def args(self, values):
        return ", ".join(self.value(value) for value in values)

    def op(self, op):
        kind = op["op"]
        if kind == "blank": return [""]
        if kind == "comment": return [f"/* {comment_text(op['text'])} */"]
        if kind == "create": return [f"{self.name(op['name'])} = lv_{op['cls']}_create({self.value(op['parent'])});"]
        if kind == "construct": return [f"lv_obj_t * {self.name(op['name'])} = {op['fn']}({self.args(op['args'])});", f"LV_UNUSED({self.name(op['name'])});"]
        if kind == "call":
            call = f"{op['fn']}({self.args([op['target'], *op['args']])});"
            return [f"{op['assign']['ctype']} {self.name(op['assign']['name'])} = {call}", f"LV_UNUSED({self.name(op['assign']['name'])});"] if op.get("assign") else [call]
        if kind == "struct": return [f"{op['ctype']} {op['name']};"]
        if kind == "array": return [f"static {op['ctype']} {op['name']}[] = {{{self.args(op['items'])}}};"]
        if kind == "animExec":
            if op["prop"] == "opa":
                setter = self.context["opaHelper"]()
            elif op["prop"] == "rotation":
                setter = "(lv_anim_exec_xcb_t)lv_arc_set_rotation"
            else:
                setter = f"(lv_anim_exec_xcb_t)lv_obj_set_{op['prop']}"
            return [f"lv_anim_set_exec_cb(&{op['anim']}, {setter});"]
        raise ValueError(f"Unknown operation {kind}")

    def emit(self, ops):
        return "\n".join("    " + line if line else "" for operation in ops for line in self.op(operation))


def c_byte_lines(data, width=12):
    values = [f"0x{byte:02X}" for byte in data]
    return [", ".join(values[index:index + width]) + "," for index in range(0, len(values), width)]


FONT_LOADER = "ui_load_fonts"


def c_declarations(widget_names, fonts, custom, images, opa_helper, variables, variables_init):
    parts = []
    if fonts:
        parts.append("/* Fonts used: enable " + ", ".join(f"LV_FONT_MONTSERRAT_{size}" for size in sorted(fonts)) + " in lv_conf.h */")
    for image in images["embedded"]:
        symbol, info, data = image["symbol"], image["info"], image["data"]
        png = info["format"] == "png"
        body = "\n".join("    " + line for line in c_byte_lines(data["bytes"]))
        parts.append(f"/* Image \"{comment_text(image['name'])}\" ({info['width']}x{info['height']}) */\nstatic const uint8_t {symbol}_data[] = {{\n{body}\n}};\nstatic const lv_image_dsc_t {symbol} = {{\n    .header.magic = LV_IMAGE_HEADER_MAGIC,\n    .header.cf = {'LV_COLOR_FORMAT_RAW_ALPHA' if png else 'LV_COLOR_FORMAT_RAW'},\n    .header.w = {info['width']},\n    .header.h = {info['height']},\n    .data_size = sizeof({symbol}_data),\n    .data = {symbol}_data,\n}};")
    if images["filePaths"]:
        parts.append("/* Images loaded from files need an LVGL file system driver: " + ", ".join(comment_text(path) for path in images["filePaths"]) + " */")
    if images["unsupported"]:
        parts.append("/* Unsupported images: " + ", ".join(comment_text(path) for path in images["unsupported"]) + " */")
    loaded = [font for font in custom if (font.get("result") or {}).get("output")]
    for font in loaded:
        body = "\n".join("    " + line for line in c_byte_lines(font["result"]["output"]))
        parts.append(f"/* Font \"{comment_text(font['name'])}\" {font['size']} px, in LVGL's binary format */\nstatic const uint8_t {font['symbol']}_data[] = {{\n{body}\n}};\nstatic const lv_font_t * {font['symbol']};")
    if loaded:
        load = "\n".join(f"    if ({font['symbol']} == NULL) {font['symbol']} = lv_binfont_create_from_buffer((void *){font['symbol']}_data, sizeof({font['symbol']}_data));" for font in loaded)
        default = "\n".join(f"    if ({font['symbol']} == NULL) {font['symbol']} = LV_FONT_DEFAULT;" for font in loaded)
        parts.append(f"/* Fonts of the project are loaded from memory: this needs LV_USE_FS_MEMFS in lv_conf.h.\n   Without it, or if a font cannot be loaded, the default font is used. */\nstatic void {FONT_LOADER}(void)\n{{\n#if LV_USE_FS_MEMFS\n{load}\n#endif\n{default}\n}}")
    if variables:
        definitions = "\n".join(f"    {item['name']} = lv_subject_create(LV_SUBJECT_TYPE_INT);\n    lv_subject_set_int({item['name']}, {item['initial']});" for item in variables)
        parts.append("\n".join(f"lv_subject_t * {item['name']};" for item in variables) + f"\n\nvoid {variables_init}(void)\n{{\n    static bool initialized = false;\n    if (initialized) return;\n    initialized = true;\n\n{definitions}\n}}")
    if widget_names:
        parts.append("\n".join(f"lv_obj_t * ui_{name};" for name in sorted(widget_names)))  # a set: sorted, so two exports of the same project are identical
    if opa_helper:
        parts.append(f"static void {opa_helper}(void * obj, int32_t value)\n{{\n    lv_obj_set_style_opa((lv_obj_t *)obj, (lv_opa_t)value, LV_PART_MAIN);\n}}")
    return "\n\n".join(parts)


def handler_stub(name, body=""):
    reference = c_comment_lines(body, "// ")
    return f"void {name}(lv_event_t * e)\n{{\n    // Python, for reference: translate it by hand\n{reference}\n    LV_UNUSED(e);\n}}\n"


def update_handlers(path, handlers):
    path = Path(path)
    if not path.exists():
        path.write_text('#include "ui_events.h"\n\n' + NEW_HANDLERS_BEGIN + "\n" + NEW_HANDLERS_END + "\n", encoding="utf-8", newline="\n")
    source = path.read_text(encoding="utf-8")
    existing = set(re.findall(r"\bvoid\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(lv_event_t\s*\*\s*e\s*\)", source))
    missing = [(name, handler) for name, handler in handlers.items() if name not in existing]
    if missing:
        addition = "\n" + "\n".join(handler_stub(name, handler.get("body", "")) for name, handler in missing)
        end = next((marker for marker in (NEW_HANDLERS_END, OLD_HANDLERS_END) if marker in source), None)
        if end:
            source = source.replace(end, addition + end)
        else:
            source += "\n" + NEW_HANDLERS_BEGIN + addition + NEW_HANDLERS_END + "\n"
        path.write_text(source, encoding="utf-8", newline="\n")


PORTABLE_FILES = ["ui.c", "ui.h", "ui_events.c", "ui_events.h"]


def generate_c(project, output_dir, root_dir=None, portable=False):
    """Generate the C; portable writes only the files to take into another project."""
    from .gen_python import build_project_code
    from .project_gen import legacy_data

    from lvgl_mpy_studio.core.validation import validate_project

    data = project.to_dict()
    warnings = validate_project(data)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    legacy = legacy_data(project)
    from .fonts import convert_fonts, font_warnings

    model = build_project_code(legacy, convert_fonts(legacy), language="c")
    warnings += font_warnings(legacy)
    base = model["baseName"]
    components = {widget["name"] for widget in project_components(data)}
    handlers = {name: handler for name, handler in (data.get("code", {}).get("handlers") or {}).items() if handler.get("widget") not in components}
    if components:
        warnings.append(tr("Components {names} are not available on the C target.", names=", ".join(sorted(components))))
    if data.get("modules"):
        warnings.append(tr("The Python modules {names} are not part of the C export.", names=", ".join(module["name"] for module in data["modules"])))
    root = Path(root_dir) if root_dir else Path(__file__).parents[2]
    nodes = [node for page in model["model"]["pages"] for node in page["nodes"]]
    widget_names = sorted({node["widget"]["name"] for node in nodes})
    header = ["#ifndef LVGL_MPY_STUDIO_UI_H", "#define LVGL_MPY_STUDIO_UI_H", "", "#include <stdbool.h>", "#include <stdint.h>", '#include "lvgl.h"', "", *[f"extern lv_obj_t * ui_{name};" for name in widget_names], "", "void ui_create(void);", f"void {base}_load_page(int page_index);", "", "#endif", ""]
    (output / "ui.h").write_text("\n".join(header), encoding="utf-8", newline="\n")
    event_header = ["#ifndef LVGL_MPY_STUDIO_UI_EVENTS_H", "#define LVGL_MPY_STUDIO_UI_EVENTS_H", "", '#include "lvgl.h"', ""]
    event_header += [f"void {name}(lv_event_t * e);" for name in list(handlers) + [item["name"] for item in model["eventCallbacks"]]]
    event_header += ["", "#endif", ""]
    (output / "ui_events.h").write_text("\n".join(event_header), encoding="utf-8", newline="\n")
    update_handlers(output / "ui_events.c", handlers)
    source = ['#include "ui.h"', '#include "ui_events.h"', "", model["declarations"], ""]
    for callback in model["eventCallbacks"]:
        source.append(f"void {callback['name']}(lv_event_t * e)\n{{\n    lv_event_code_t code = lv_event_get_code(e);\n    LV_UNUSED(e);\n{callback['body']}\n}}\n")
    source.append(f"static lv_obj_t * screens[{len(model['pages'])}];\nstatic int current_screen;\n")
    for page in model["pages"]:
        source.append(f"static void {page['functionName']}(lv_obj_t * parent)\n{{\n    if (parent == NULL) parent = lv_screen_active();\n" + "\n".join(page["widgets"]) + "}\n")
    loader = f"    {FONT_LOADER}();\n" if f"void {FONT_LOADER}(" in model["declarations"] else ""
    source.append(f"void {base}_load_page(int page_index)\n{{\n    if (page_index < 0 || page_index >= {len(model['pages'])}) return;\n{loader}    if (screens[page_index] == NULL) {{\n        screens[page_index] = lv_obj_create(NULL);")
    for index, page in enumerate(model["pages"]):
        source.append(f"        {'if' if index == 0 else 'else if'} (page_index == {index}) {{\n            {page['functionName']}(screens[page_index]);")
        widget_names_on_page = {node["widget"]["name"] for node in model["model"]["pages"][index]["nodes"]}
        for name, handler in handlers.items():
            widget_name, event = handler.get("widget"), handler.get("event")
            if widget_name in widget_names_on_page:
                source.append(f"            lv_obj_add_event_cb(ui_{widget_name}, {name}, LV_EVENT_{event}, NULL);")
            elif widget_name == data["pages"][index]["name"]:
                source.append(f"            lv_obj_add_event_cb(screens[{index}], {name}, LV_EVENT_{event}, NULL);")
        source.append("        }")
    source.append("    }\n    lv_screen_load(screens[page_index]);\n    current_screen = page_index;\n}\n")
    source.append("void ui_create(void)\n{\n    current_screen = 0;\n    " + base + "_load_page(0);\n}\n")
    (output / "ui.c").write_text("\n".join(source), encoding="utf-8", newline="\n")
    # Main and Makefile are for building and need the LVGL sources.
    if portable or not (root / ".reference" / "lvgl-bindings" / "lv_conf.h").exists():
        return {"files": list(PORTABLE_FILES), "warnings": warnings}
    width, height = data["display"]["width"], data["display"]["height"]
    main = MAIN_TEMPLATE.replace("@WIDTH@", str(width)).replace("@HEIGHT@", str(height)).replace("@TITLE@", c_string(data["projectName"]))
    (output / "main.c").write_text(main, encoding="utf-8", newline="\n")
    lvgl_dir = root / ".reference" / "lvgl-bindings" / "lvgl"
    conf_dir = root / ".reference" / "lvgl-bindings"
    lvsim_dir = root / "native" / "lvsim"
    import hashlib
    from lvgl_mpy_studio.platform import IS_WINDOWS
    config_hash = hashlib.sha256((conf_dir / "lv_conf.h").read_bytes() + b"LV_CPYTHON_BUILD").hexdigest()[:12]
    from lvgl_mpy_studio.build.compiler import cache_root
    cache_dir = root / "runtime" / "out-win64" if IS_WINDOWS else cache_root() / f"lvgl-9.5.0-{config_hash}"
    sdl_dir = root / "runtime" / "out-win64" / "SDL2"
    replacements = {"@LVGL_DIR@": lvgl_dir, "@CONF_DIR@": conf_dir, "@LVSIM_DIR@": lvsim_dir, "@CACHE_DIR@": cache_dir, "@SDL2_DIR@": sdl_dir}
    makefile = MAKEFILE_TEMPLATE
    for placeholder, value in replacements.items():
        makefile = makefile.replace(placeholder, Path(value).as_posix())
    (output / "Makefile").write_text(makefile, encoding="utf-8", newline="\n")
    warnings += [f"Handler not connected: {name}" for name, handler in handlers.items() if handler.get("widget") and not project.find_widget(handler["widget"]) and handler["widget"] not in {page.name for page in project.pages}]
    return {"files": ["ui.c", "ui.h", "ui_events.c", "ui_events.h", "main.c", "Makefile"], "warnings": warnings}
