import base64
from datetime import datetime, timezone
import keyword
import re

from lvgl_mpy_studio.core.model import page_constant  # noqa: F401  (one definition, also used by whoever imports from here)
from .escaping import comment_text, indent_text, python_string
from .identifiers import IdentifierAllocator, sanitize_identifier
from .images import image_info, parse_data_url
from .legacy_widgets import build_widget_ops
from .values import MICROPYTHON_FONT_SIZES, nearest_font_size, v

EVENT_CODES = [
    "CLICKED", "SHORT_CLICKED", "SINGLE_CLICKED", "DOUBLE_CLICKED", "TRIPLE_CLICKED", "PRESSED",
    "PRESSING", "PRESS_LOST", "RELEASED", "LONG_PRESSED", "LONG_PRESSED_REPEAT", "VALUE_CHANGED",
    "FOCUSED", "DEFOCUSED", "LEAVE", "READY", "CANCEL", "KEY", "ROTARY", "GESTURE", "INSERT",
    "SCROLL", "SCROLL_BEGIN", "SCROLL_END", "HOVER_OVER", "HOVER_LEAVE", "SIZE_CHANGED", "DELETE",
    "SCREEN_LOAD_START", "SCREEN_LOADED", "SCREEN_UNLOAD_START", "SCREEN_UNLOADED",
]
LVGL_CLASSES = [
    "animimg", "arc", "bar", "button", "buttonmatrix", "calendar", "canvas", "chart", "checkbox",
    "dropdown", "image", "imagebutton", "keyboard", "label", "led", "line", "list", "menu",
    "menu_cont", "menu_page", "menu_section", "menu_separator", "msgbox", "obj", "roller", "scale",
    "slider", "spangroup", "spinbox", "spinner", "switch", "table", "tabview", "textarea", "tileview", "win",
]
FUNCTION_OWNERS = sorted(LVGL_CLASSES + ["anim", "style", "span", "event", "subject"], key=len, reverse=True)
ENUM_OWNERS = sorted(LVGL_CLASSES, key=len, reverse=True)
BASE_CHARACTERS = "".join(chr(value) for value in range(0x20, 0x7F))


def function_owner(fn):
    owner = next((name for name in FUNCTION_OWNERS if fn.startswith(f"lv_{name}_")), None)
    if not owner:
        raise ValueError(f"No MicroPython owner class for {fn}")
    method = fn[len(owner) + 4:]
    return method == "del" and "delete" or method


def python_enum_path(enum_name, member):
    lower = enum_name.lower()
    owner = next((name for name in ENUM_OWNERS if lower.startswith(f"{name}_")), None)
    py_member = f"_{member}" if member[0].isdigit() else member
    return f"lv.{owner}.{enum_name[len(owner) + 1:]}.{py_member}" if owner else f"lv.{enum_name}.{py_member}"


class PythonEmitter:
    def __init__(self, context):
        self.context = context

    def value(self, value):
        kind = value["k"]
        if kind == "int": return str(value["value"])
        if kind == "str": return python_string(value["value"])
        if kind == "bool": return "True" if value["value"] else "False"
        if kind == "color": return f"lv.color_hex(0x{value['value']:06X})"
        if kind == "enum": return python_enum_path(value["enumName"], value["member"])
        if kind == "sel": return " | ".join(filter(None, [f"lv.PART.{value['part']}", f"lv.STATE.{value['state']}" if value.get("state") else None]))
        if kind == "font":
            if value.get("symbol"): return value["symbol"]
            size = nearest_font_size(value["size"], self.context.get("fontSizes") or MICROPYTHON_FONT_SIZES)
            self.context["fonts"].add(size)
            return f"lv.font_montserrat_{size}"
        if kind in ("ref", "fn"): return value["name"]
        if kind == "null": return "None"
        if kind == "pct": return f"lv.pct({value['value']})"
        if kind == "constant": return f"lv.{value['name']}"
        if kind == "animEnable": return "True" if value["value"] else "False"
        if kind == "animPath": return f"lv.anim_t.path_{value['name']}"
        if kind == "image": return value.get("symbol") or python_string(value["source"])
        if kind == "point": return f'{{"x": {value["x"]}, "y": {value["y"]}}}'
        raise ValueError(f"Unknown value kind {kind}")

    def args(self, values):
        return ", ".join(self.value(value) for value in values)

    def op(self, op):
        kind = op["op"]
        if kind == "blank": return [""]
        if kind == "comment": return [f"# {comment_text(op['text'])}"]
        if kind == "create": return [f"{op['name']} = lv.{op['cls']}({self.value(op['parent'])})"]
        if kind == "construct": return [f"{op['name']} = lv.{op['cls']}({self.args(op['args'])})"]
        if kind == "call":
            call = f"{self.value(op['target'])}.{function_owner(op['fn'])}({self.args(op['args'])})"
            return [f"{op['assign']['name']} = {call}" if op.get("assign") else call]
        if kind == "struct": return [f"{op['name']} = lv.{op['pyType']}()"]
        if kind == "array": return [f"{op['name']} = [{self.args(op['items'])}]"]
        if kind == "animExec":
            target = op["target"]["name"]
            setter = {"x": f"{target}.set_x(value)", "y": f"{target}.set_y(value)", "width": f"{target}.set_width(value)", "height": f"{target}.set_height(value)", "opa": f"{target}.set_style_opa(value, lv.PART.MAIN)", "rotation": f"{target}.set_rotation(value)"}[op["prop"]]
            return [f"{op['anim']}.set_custom_exec_cb(lambda _anim, value: {setter})"]
        raise ValueError(f"Unknown operation {kind}")

    def emit(self, ops):
        return "\n".join("    " + line if line else "" for operation in ops for line in self.op(operation))


def order_widgets(widgets):
    by_id = {widget.get("id"): widget for widget in widgets}
    children, roots = {}, []
    for widget in widgets:
        parent = by_id.get(widget.get("parentId")) if widget.get("parentId") and widget.get("parentId") != widget.get("id") else None
        if parent is not None:
            children.setdefault(parent.get("id"), []).append(widget)
        else:
            roots.append(widget)
    ordered, visited = [], set()

    def visit(widget, parent):
        if widget.get("id") in visited: return
        visited.add(widget.get("id"))
        ordered.append({"widget": widget, "parent": parent})
        for child in children.get(widget.get("id"), []): visit(child, widget)

    for widget in roots: visit(widget, None)
    for widget in widgets: visit(widget, None)
    return ordered


def render_handler_body(handler, language="micropython"):
    branches = []
    for index, (event_code, code) in enumerate(handler["branches"].items()):
        if language == "c":
            body = code if code.strip() else f"/* TODO: handle LV_EVENT_{event_code} */"
            branches.append(f"{'else ' if index else ''}if (code == LV_EVENT_{event_code}) {{\n    {indent_text(body, 4)}\n}}")
        else:
            body = re.sub(r"^(\s*)//\s?", r"\1# ", code, flags=re.MULTILINE) if code.strip() else f"# TODO: handle lv.EVENT.{event_code}"
            branches.append(f"{'elif' if index else 'if'} code == lv.EVENT.{event_code}:\n    {indent_text(body, 4)}\n    pass")
    return "\n".join(branches)


def widget_characters(widget):
    texts = [value for value in (widget.get("props") or {}).values() if isinstance(value, str)]
    if widget.get("binding", {}).get("format"): texts.append(widget["binding"]["format"])
    return "".join(dict.fromkeys(re.sub(r"[\n\r\t]", "", "".join(texts))))


def font_notes(fonts):
    notes = []
    for font in fonts:
        result = font.get("result") or {}
        label = f'Font "{comment_text(font["name"])}" {font["size"]} px'
        if result.get("error"):
            notes.append(f"# {label} not converted ({comment_text(result['error'])}): Montserrat is used instead")
        elif result.get("missing"):
            missing = " ".join(f"U+{ord(char):04X}" for char in result["missing"])
            notes.append(f"# {label} has no glyph for: {missing}")
    return notes


def python_declarations(fonts, custom, images, variables, font_sizes=None):
    parts = []
    converted = [font for font in custom if (font.get("result") or {}).get("output")]
    for font in converted:
        font["fallback"] = nearest_font_size(font["size"], font_sizes or MICROPYTHON_FONT_SIZES)
        fonts.add(font["fallback"])
    if fonts:
        sizes = sorted(fonts)
        parts.append(f"# Fonts used: {', '.join(f'lv.font_montserrat_{size}' for size in sizes)} (font sizes are mapped to the ones in the default lv_micropython build: 14, 16, 24)" if not font_sizes else f"# Fonts used: {', '.join(f'lv.font_montserrat_{size}' for size in sizes)} (font sizes are mapped to the ones available: {', '.join(str(size) for size in font_sizes)})")
    if images["filePaths"]:
        parts.append(f"# Images loaded from files need an LVGL file system driver: {', '.join(comment_text(path) for path in images['filePaths'])}")
    if images["unsupported"]:
        parts.append(f"# Not generated (only PNG and JPEG images are supported): {', '.join(comment_text(path) for path in images['unsupported'])}")
    parts.extend(font_notes(custom))
    if images["embedded"] or converted: parts.append("import binascii")
    if converted:
        parts.append("# Fonts of the project, converted to LVGL's binary format. Loading them needs\n# lv.binfont_create_from_buffer: a firmware without it draws the text with\n# the nearest Montserrat font")
    for font in converted:
        symbol, result = font["symbol"], font["result"]
        encoded = base64.b64encode(result["output"]).decode("ascii")
        parts.append(f'# Font "{comment_text(font["name"])}" {font["size"]} px\nif hasattr(lv, "binfont_create_from_buffer"):\n    {symbol}_data = binascii.a2b_base64("{encoded}")\n    {symbol} = lv.binfont_create_from_buffer({symbol}_data, len({symbol}_data))\n    del {symbol}_data  # LVGL keeps its own copy\nelse:\n    {symbol} = lv.font_montserrat_{font["fallback"]}')
    for image in images["embedded"]:
        symbol, info, data = image["symbol"], image["info"], image["data"]
        png = info["format"] == "png"
        parts.append(f'# Image "{comment_text(image["name"])}" ({info["width"]}x{info["height"]} {"PNG" if png else "JPEG"}), decoded at run time by LVGL\n{symbol}_data = binascii.a2b_base64("{data["base64"]}")\n{symbol} = lv.image_dsc_t({{"header": {{"magic": lv.IMAGE_HEADER_MAGIC, "cf": lv.COLOR_FORMAT.{"RAW_ALPHA" if png else "RAW"}, "w": {info["width"]}, "h": {info["height"]}}}, "data_size": len({symbol}_data), "data": {symbol}_data}})')
    if variables:
        parts.append("# Variables for data binding (LVGL subjects): read and write them with get_int()/set_int()\n" + "\n".join(f"{var['name']} = lv.subject_t()\n{var['name']}.init_int({var['initial']})" for var in variables))
    return "\n".join(parts)


def build_project_code(project_data, converted_fonts=None, language="micropython", font_sizes=None):
    converted_fonts = converted_fonts or {}
    ids = IdentifierAllocator()
    base_name = ids.allocate(project_data.get("projectName") or "ui", "ui")
    ids.reserve("load_page", "load_page_anim", "get_current_page", f"{base_name}_init", f"{base_name}_load_page", f"{base_name}_load_page_anim", f"{base_name}_get_current_page", f"{base_name}_variables_init")
    raw_pages = project_data.get("pages")
    if not isinstance(raw_pages, list) or not raw_pages: raise ValueError("The project has no pages")
    pages = []
    for index, page in enumerate(raw_pages):
        pages.append({"name": page.get("name") or f"Page {index + 1}", "widgets": page.get("widgets") if isinstance(page.get("widgets"), list) else [], "canvasSize": page.get("canvasSize") or {"width": 800, "height": 480}, "functionName": ids.allocate(f"{base_name}_create_{page.get('name', '')}", "page")})
    names = {}
    for page in pages:
        page["nodes"] = []
        for ordered in order_widgets(page["widgets"]):
            widget = ordered["widget"]
            name = ids.allocate(widget.get("name") or widget["type"], sanitize_identifier(widget["type"], "obj"), lambda n: [f"ui_{n}"])
            names[id(widget)] = name
            page["nodes"].append({"widget": widget, "name": name, "parent": ordered["parent"]})
        for node in page["nodes"]:
            node["parentName"] = names.get(id(node["parent"])) if node["parent"] else None
    variables = {}
    for variable in project_data.get("variables") or []:
        if variable and isinstance(variable.get("id"), str) and variable["id"] not in variables:
            initial = variable.get("initial") or 0
            try: initial = int(float(initial))
            except (ValueError, TypeError): initial = 0
            variables[variable["id"]] = {"name": ids.allocate(f"var_{variable.get('name') or ''}", "var"), "initial": initial}
    handlers, handlers_by_request = {}, {}
    assets = {asset.get("name"): asset for asset in (project_data.get("assets") or {}).get("images", [])}
    embedded, file_paths, unsupported = {}, [], []
    font_assets = {asset.get("name"): asset for asset in (project_data.get("assets") or {}).get("fonts", [])}
    custom_fonts = {}

    def image_source(source):
        if source in embedded: return v.image(source, embedded[source]["symbol"])
        asset = assets.get(source)
        if not asset:
            if source not in file_paths: file_paths.append(source)
            return v.image(source)
        data = parse_data_url(asset.get("data"))
        info = data and image_info(data["bytes"])
        if not info:
            if source not in unsupported: unsupported.append(source)
            return None
        file = re.sub(r"\.[^.]*$", "", str(source))
        symbol = ids.allocate(f"img_{file}", "img", lambda n: [f"{n}_data"])
        embedded[source] = {"symbol": symbol, "name": source, "info": info, "data": data}
        return v.image(source, symbol)

    def custom_font(name, size, widget):
        asset = font_assets.get(name)
        if not asset or not isinstance(asset.get("data"), str): return None
        px = min(200, max(4, size))
        key = f"{name}\0{px}"
        font = custom_fonts.get(key)
        if not font:
            file = re.sub(r"\.[^.]*$", "", str(name))
            symbol = ids.allocate(f"font_{file}_{px}", "font", lambda n: [f"{n}_data"])
            characters = dict.fromkeys(BASE_CHARACTERS + str(asset.get("characters") or ""))
            font = {"key": key, "name": name, "size": px, "symbol": symbol, "asset": asset, "characters": characters}
            custom_fonts[key] = font
        for char in widget_characters(widget): font["characters"][char] = None
        return font["symbol"] if (converted_fonts.get(key) or {}).get("output") else None

    def callback_for(widget, event):
        event_code = re.sub(r"^LV_EVENT_", "", str(event.get("type") or ""))
        if event_code not in EVENT_CODES: return None
        code = str(event.get("code") or "")
        requested = sanitize_identifier(event.get("callback") or f"{names[id(widget)]}_event_cb", "event_cb")
        candidates = handlers_by_request.get(requested, [])
        handler = next((handlers[name] for name in candidates if event_code not in handlers[name]["branches"] or handlers[name]["branches"][event_code] == code), None)
        if not handler:
            handler = {"name": ids.allocate(requested, "event_cb"), "branches": {}}
            handlers[handler["name"]] = handler
            handlers_by_request[requested] = candidates + [handler["name"]]
        handler["branches"][event_code] = code
        return {"name": handler["name"], "eventCode": event_code}

    context = {"language": language, "temp": lambda base: ids.allocate(base, "tmp"), "variable": lambda key: (variables.get(key) or {}).get("name"), "image": image_source, "font": custom_font, "callback_for": callback_for}
    for page in pages:
        for node in page["nodes"]: node["ops"] = build_widget_ops(node, context)
    fonts = set()
    widget_names = set(names.values())
    public_widget_names = {node["widget"]["name"] for page in pages for node in page["nodes"]}
    public_names_by_internal = {node["name"]: node["widget"]["name"] for page in pages for node in page["nodes"]}
    opa_helper = []
    def get_opa_helper():
        if not opa_helper:
            opa_helper.append(ids.allocate("ui_anim_set_opa", "anim_cb"))
        return opa_helper[0]
    emitter_context = {"isWidget": lambda name: name in widget_names, "widgetNames": public_names_by_internal, "fonts": fonts, "opaHelper": get_opa_helper, "fontSizes": font_sizes}
    if language == "c":
        from .gen_c import CEmitter, c_declarations
        emitter = CEmitter(emitter_context)
    else:
        emitter = PythonEmitter(emitter_context)
    variables_init = f"{base_name}_variables_init"
    pages_data = []
    for page in pages:
        widgets = ([f"    {variables_init}();\n"] if variables and language == "c" else []) + [emitter.emit(node["ops"]) + "\n" for node in page["nodes"]]
        pages_data.append({"name": comment_text(page["name"]), "functionName": page["functionName"], "width": page["canvasSize"].get("width"), "height": page["canvasSize"].get("height"), "widgetCount": len(page["widgets"]), "widgets": widgets})
    event_callbacks = [{"name": handler["name"], "body": render_handler_body(handler, language)} for handler in handlers.values()]
    images = {"embedded": list(embedded.values()), "filePaths": file_paths, "unsupported": unsupported}
    custom = [dict(font, result=converted_fonts.get(font["key"])) for font in custom_fonts.values()]
    variable_list = list(variables.values())
    declarations = c_declarations(public_widget_names, fonts, custom, images, opa_helper[0] if opa_helper else None, variable_list, variables_init) if language == "c" else python_declarations(fonts, custom, images, variable_list, font_sizes)
    font_requests = [{"key": font["key"], "name": font["name"], "size": font["size"], "symbol": font["symbol"], "data": font["asset"].get("data"), "characters": "".join(font["characters"])} for font in custom_fonts.values()]
    model = {"pages": [{"name": page["name"], "nodes": page["nodes"]} for page in pages]}
    return {"baseName": base_name, "pages": pages_data, "eventCallbacks": event_callbacks, "declarations": declarations, "fontRequests": font_requests, "model": model}


STYLE_LINE = re.compile(r"^    (\w+)\.set_style_(\w+)\((.*), (lv\.PART\.\w+(?: \| lv\.STATE\.\w+)*|lv\.STATE\.\w+)\)$")
CONSTANT_VALUE = re.compile(r"^(-?\d+|0x[0-9A-Fa-f]+|True|False|lv\.[\w.]+(\([\w, .-]*\))?)$")




def _style_groups(block):
    """For each (object, selector): constant properties and the lines that set them."""
    groups = {}
    for number, line in enumerate(block.split("\n")):
        match = STYLE_LINE.match(line)
        if match and CONSTANT_VALUE.match(match.group(3)):
            target, prop, value, selector = match.groups()
            group = groups.setdefault((target, selector), {"props": {}, "lines": []})
            group["props"][prop] = value
            group["lines"].append(number)
    return groups


def _style_key(selector, group):
    return selector, tuple(sorted(group["props"].items()))


def share_styles(pages):
    """Move into shared lv.style_t the identical style groups used by several objects."""
    counts = {}
    for page in pages:
        for block in page["widgets"]:
            for (_target, selector), group in _style_groups(block).items():
                key = _style_key(selector, group)
                counts[key] = counts.get(key, 0) + 1
    shared = {}
    for key, count in counts.items():
        if count > 1:
            shared[key] = len(shared)
    if not shared:
        return []
    for page in pages:
        for index, block in enumerate(page["widgets"]):
            lines = block.split("\n")
            removed = set()
            for (target, selector), group in _style_groups(block).items():
                position = shared.get(_style_key(selector, group))
                if position is None:
                    continue
                lines[group["lines"][0]] = f"    {target}.add_style(_styles[{position}], {selector})"
                removed.update(group["lines"][1:])
            page["widgets"][index] = "\n".join(line for number, line in enumerate(lines) if number not in removed)
    source = ["_styles = []\n\ndef _init_styles():\n    if _styles:\n        return\n"]
    for _selector, props in shared:
        source.append("    style = lv.style_t()\n    style.init()\n")
        source.extend(f"    style.set_{prop}({value})\n" for prop, value in props)
        source.append("    _styles.append(style)\n")
    return ["".join(source) + "\n"]


def generate_python(project_data, generated_date=None, converted_fonts=None, usage=None, font_sizes=None):
    """usage limits the code to what the project uses; None generates everything.

    font_sizes: the Montserrat sizes the target has; None keeps the three of the legacy generator.
    """
    usage = usage or {}
    exposed = usage.get("exposed")
    helpers = usage.get("helpers")
    page_constants = usage.get("pages")
    if generated_date is None:
        generated_date = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    if converted_fonts is None:
        first = build_project_code(project_data)
        converted_fonts = {request["key"]: {"error": "fonts are converted by the desktop app"} for request in first["fontRequests"]}
    project = build_project_code(project_data, converted_fonts, font_sizes=font_sizes)
    style_source = share_styles(project["pages"])
    for page, model_page in zip(project["pages"], project["model"]["pages"]):
        page["globals"] = []
        for index, node in enumerate(model_page["nodes"]):
            name = node["widget"]["name"]
            if not re.fullmatch(r"[A-Za-z_]\w*", name, re.ASCII) or keyword.iskeyword(name) or (exposed is not None and name not in exposed):
                continue
            if name not in page["globals"]:
                page["globals"].append(name)
            if name != node["name"]:
                page["widgets"][index] = page["widgets"][index].rstrip("\n") + f"\n    {name} = {node['name']}\n"
    parts = [f'''"""
Auto-generated LVGL UI Code for MicroPython
Project: {comment_text(project_data.get("projectName") or "Untitled")}
Generated: {generated_date}
Pages: {len(project["pages"])}

LVGL Version: 9.3 (lv_micropython binding)
"""

import lvgl as lv

''']
    if project["declarations"]: parts.append(project["declarations"] + "\n\n\n")
    if project["eventCallbacks"]:
        for callback in project["eventCallbacks"]:
            parts.append(f"def {callback['name']}(e):\n    code = e.get_code()\n    obj = e.get_target_obj()\n\n    {indent_text(callback['body'], 4)}\n\n")
    parts.append(f"screens = [None] * {len(project['pages'])}\ncurrent_screen = 0\n")
    for index, page in enumerate(project["pages"]):
        constant = page_constant(page["name"])
        if page_constants is None or constant in page_constants:
            parts.append(f"{constant} = {index}\n")
    parts.append("\n")
    parts.extend(style_source)
    for page in project["pages"]:
        parts.append(f"def {page['functionName']}(parent=None):\n")
        if page["globals"]:
            parts.append(f"    global {', '.join(page['globals'])}\n")
        parts.append("    if parent is None:\n        parent = lv.screen_active()\n")
        if style_source:
            parts.append("    _init_styles()\n")
        parts.append("\n")
        for widget in page["widgets"]: parts.append(widget + "\n")
        parts.append("\n")
    for function, suffix in (("load_page", ""), ("load_page_anim", "_anim")):
        if helpers is not None and function not in helpers:
            continue
        args = "page_index" if not suffix else "page_index, anim, time_ms, delay_ms"
        parts.append(f"def {function}({args}):\n    global screens, current_screen\n\n    if page_index < 0 or page_index >= {len(project['pages'])}:\n        return\n\n    if screens[page_index] is None:\n        screens[page_index] = lv.obj()\n\n")
        for index, page in enumerate(project["pages"]):
            parts.append(f"        {'if' if index == 0 else 'elif'} page_index == {index}:\n            {page['functionName']}(screens[{index}])\n")
        call = "lv.screen_load(screens[page_index])" if not suffix else "lv.screen_load_anim(screens[page_index], anim, time_ms, delay_ms, False)"
        parts.append(f"\n    {call}\n    current_screen = page_index\n\n")
    if helpers is None or "get_current_page" in helpers:
        parts.append("def get_current_page():\n    return current_screen\n")
    return "".join(parts)
