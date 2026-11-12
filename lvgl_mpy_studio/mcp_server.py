"""MCP server on stdio: an agent works on the project, the simulator and the board.

It has no limits compared with the IDE: it runs the project code, uploads to boards and installs
the autostart. That is why it is off by default: the entry in the Settings menu turns it on.
"""

import base64
import json
import os
from pathlib import Path
import re
import sys
import time

from . import __version__
from .build.budget import measure_budget
from .build.compiler import CompileError
from .build.preview import render_with_log
from .build.visual import PASSED, UPDATED, baseline_dir, encode_png, rgb565_to_rgb, run_visual_tests, save_scenario as save_scenario_file
from .core.actions import SCREEN_ACTIONS, actions_for
from .core.boards import ProfileStore, profile_fonts, portable_profile
from .core.components import COMPONENTS, is_component
from .core.events import events_for
from .core.i18n import device_error_text, set_language
from .core import assets
from .core import modules as user_modules
from .core.model import Project, file_revision, widget_definitions
from .core.validation import validate_project
from .device.service import DeviceError, DeviceSession
from .gen.live import live_script
from .gen.project_gen import design_warnings
from .mcp_tools import SPECS
from .platform import adopt_old_config, config_dir
from .sim.script import check_script, play

PROTOCOL_VERSIONS = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")
INSTRUCTIONS = (
    "Work on LVGL MPY Studio projects. Read a project with project_info, change it with the widget and code tools, "
    "and check the result with render_page, which returns the real LVGL rendering with the project code running. "
"Use simulate to try behaviour: it runs the app in real time and plays touch input, so games and handlers can be tested without a board. "
    "Python modules of the project are files the code imports: list_modules, create_module, rename_module, delete_module, and get_code or patch_code with module. "
    "project_info and get_code return the file revision; pass it as expected_revision to a tool that changes the project, "
    "so that a file changed in the meantime is reported as revision_conflict and left untouched: read it again before repeating the change. "
    "The device_ tools act on real hardware: connect first, then upload, run and read the console. "
    "The LVGL MPY Studio must not hold the same serial port."
)
DISABLED = "The MCP server is off. Turn it on in LVGL MPY Studio under Settings → MCP Server for AI Agents."
COLOR = re.compile(r"#[0-9A-Fa-f]{6}")


class ToolError(ValueError):
    pass


class RevisionConflict(ToolError):
    """The file is no longer the one that was read: no change, the agent reads again and decides."""

    def __init__(self, path, expected, current):
        self.data = {
            "error": "revision_conflict",
            "message": "The project file is not the revision expected: nothing was changed. Read it again with project_info or get_code, then repeat the change if it still applies."
            if current else "The project file was deleted: nothing was written.",
            "project": str(path),
            "expected_revision": expected,
            "current_revision": current,
        }
        super().__init__(self.data["message"])


# Private keys in the arguments of a call (a copy, never those of the client): the revision
# read by _load and the one written by _save, which _call_tool adds to the answer.
LOADED = "\0loaded_revision"
SAVED = "\0saved_revision"


class Content(list):
    """Result already in MCP form: text and images together."""


def config_path():
    """On Windows it stays in APPDATA, where it has been since the first version; elsewhere in the shared folder."""
    if os.name == "nt" and os.environ.get("APPDATA"):
        return adopt_old_config(os.environ["APPDATA"]) / "mcp.json"
    return config_dir() / "mcp.json"


def is_enabled():
    """A missing or unreadable file means off."""
    try:
        return json.loads(config_path().read_text(encoding="utf-8")).get("enabled") is True
    except (OSError, ValueError, AttributeError):
        return False


def set_enabled(enabled):
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"enabled": bool(enabled)}) + "\n", encoding="utf-8")


def _definitions():
    return {**widget_definitions(), **COMPONENTS}


def _load(arguments):
    path = Path(arguments["project"]).expanduser()
    if not path.is_file():
        raise ToolError(f"Project file not found: {path}")
    project, revision = Project.load_with_revision(path)
    expected = arguments.get("expected_revision")
    if expected is not None:
        if not isinstance(expected, str):
            raise ToolError("expected_revision is the revision string returned by project_info or get_code")
        if expected != revision:
            raise RevisionConflict(path, expected, revision)
    arguments[LOADED] = revision
    return path, project


def _save(path, project, arguments):
    """Validate and write, only if the file is still the one read by _load.

    The check happens even without expected_revision: between reading and writing the IDE or
    another agent may have saved. A short window remains, between this check and the atomic
    replacement of the file, in which an outside write would be lost: it is not a transaction,
    and without a lock it cannot be one.
    """
    warnings = validate_project(project) + design_warnings(project)
    current = file_revision(path)
    if current != arguments[LOADED]:
        raise RevisionConflict(path, arguments.get("expected_revision") or arguments[LOADED], current)
    arguments[SAVED] = project.save(path)
    return warnings


def _page(project, name):
    if not name:
        return next(page for page in project.pages if page.id == project.currentPageId)
    page = next((page for page in project.pages if page.name == name), None)
    if page is None:
        raise ToolError(f"Unknown page {name!r}. Pages: {[page.name for page in project.pages]}")
    return page


def _widget(project, name):
    widget = project.find_widget(name)
    if widget is None:
        raise ToolError(f"Unknown widget {name!r}. Widgets: {sorted(project.used_names)}")
    return widget


def _check_props(widget_type, props):
    definition = _definitions()[widget_type]
    described = {item["name"]: item for item in definition.get("properties") or []}
    known = set(described) | set(definition.get("defaultProps") or {})
    for key, value in props.items():
        if key not in known:
            raise ToolError(f"{widget_type} has no property {key!r}. Properties: {sorted(known)}")
        kind = described.get(key, {}).get("type")
        valid = {
            "number": isinstance(value, (int, float)) and not isinstance(value, bool),
            "boolean": isinstance(value, bool),
            "color": isinstance(value, str) and COLOR.fullmatch(value) is not None,
        }.get(kind, True)
        options = described.get(key, {}).get("options")
        if not valid or (kind == "select" and options and value not in options):
            raise ToolError(f"Invalid value {value!r} for {key} ({kind})" + (f": use one of {options}" if options else ""))


def _check_code(source, scope):
    try:
        compile(source, scope, "exec")
    except SyntaxError as exc:
        raise ToolError(f"Syntax error in {scope}, line {exc.lineno}: {exc.msg}") from exc


def _indented(body):
    return "def handler(e):\n" + "\n".join("    " + line for line in (body or "pass").splitlines())


def _summary(widget):
    return {"name": widget.name, "type": widget.type, "parent": widget.parentId, "props": widget.props}


def create_project(arguments):
    path = Path(arguments["path"]).expanduser()
    if path.suffix != ".json":
        raise ToolError("The project file must end in .json")
    if path.exists():
        raise ToolError(f"{path} already exists")
    project = Project(arguments.get("name") or path.stem)
    if arguments.get("board"):
        profile = portable_profile(_board(arguments["board"]))
        project.board = profile
        project.runTarget = {"kind": "board", "language": "micropython"}
        project.set_display_size(profile["logicalWidth"], profile["logicalHeight"])
    else:
        project.set_display_size(arguments.get("width", 800), arguments.get("height", 480))
    path.parent.mkdir(parents=True, exist_ok=True)
    return {"project": str(path), "revision": project.save(path)}


def project_info(arguments):
    _path, project = _load(arguments)
    data = project.to_dict()
    return {
        "revision": arguments[LOADED],
        "name": project.projectName,
        "display": data["display"],
        "board": (project.board or {}).get("id"),
        "pages": [{"name": page.name, "widgets": [_summary(widget) for widget in page.widgets]} for page in project.pages],
        "module": project.code.module,
        "handlers": {name: {"widget": handler.widget, "event": handler.event, "body": handler.body} for name, handler in project.code.handlers.items()},
        "modules": [{"name": module.name, "source": module.source} for module in project.modules],
        "images": assets.images(project),
        "fonts": assets.fonts(project),
        "outOfBounds": project.widgets_outside(),
    }


def list_widget_types(arguments):
    definitions = _definitions()
    wanted = arguments.get("types")
    if wanted is None:  # the whole list is long: names first, details on request
        return {"types": sorted(definitions), "hint": "pass types, for example [\"label\", \"button\"], to get their properties, defaults and events"} if arguments.get("names_only") else {name: _type_description(name, definition) for name, definition in definitions.items()}
    unknown = [name for name in wanted if name not in definitions]
    if unknown:
        raise ToolError(f"Unknown widget types {unknown}. Types: {sorted(definitions)}")
    return {name: _type_description(name, definitions[name]) for name in wanted}


def _type_description(name, definition):
    properties = [{key: item[key] for key in ("name", "type", "options") if key in item} for item in definition.get("properties") or []]
    return {"properties": properties, "defaults": definition.get("defaultProps") or {}, "events": events_for(name)}


def suggest_code(arguments):
    project_path, project = _load(arguments)
    widget = _widget(project, arguments["widget"])
    return {label: code.replace("§", "") for label, code in [*actions_for(widget.type, widget.name), *SCREEN_ACTIONS]}


def add_page(arguments):
    path, project = _load(arguments)
    if any(page.name == arguments["name"] for page in project.pages):
        raise ToolError(f"Page {arguments['name']!r} already exists")
    project.pages.append(project.new_page(arguments["name"]))
    return {"warnings": _save(path, project, arguments)}


def _parent(project, name):
    parent = _widget(project, name)
    if is_component(parent.type):
        raise ToolError(f"{parent.name!r} is a {parent.type}: it is not on the screen and cannot hold widgets")
    return parent


def _add_widget(project, page, item):
    widget_type, props = item["type"], item.get("props") or {}
    if widget_type not in _definitions():
        raise ToolError(f"Unknown widget type {widget_type!r}. Types: {sorted(_definitions())}")
    _check_props(widget_type, props)
    widget = project.add_widget(_page(project, item.get("page") or page), widget_type, props, item.get("name"))
    if item.get("parent"):
        widget.parentId = _parent(project, item["parent"]).id
    return widget


def rename_page(arguments):
    path, project = _load(arguments)
    warnings = project.rename_page(_page(project, arguments["name"]), arguments["new_name"])
    return {"warnings": warnings + _save(path, project, arguments)}


def remove_page(arguments):
    path, project = _load(arguments)
    project.remove_page(_page(project, arguments["name"]))
    return {"warnings": _save(path, project, arguments)}


def add_widget(arguments):
    path, project = _load(arguments)
    widget = _add_widget(project, None, arguments)
    return {"name": widget.name, "warnings": _save(path, project, arguments)}


def add_widgets(arguments):
    """All or nothing: the project is saved only if every widget is valid."""
    path, project = _load(arguments)
    names = [_add_widget(project, arguments.get("page"), item).name for item in arguments["widgets"]]
    return {"names": names, "warnings": _save(path, project, arguments)}


def _page_of(project, widget):
    return next(page for page in project.pages if widget in page.widgets)


def _set_parent(project, widget, parent):
    """The widget stays where it is on screen: its coordinates are relative to the parent."""
    if parent is not None:
        widgets = {item.id: item for item in project.widgets}
        ancestor = parent
        while ancestor is not None:
            if ancestor is widget:
                raise ToolError(f"{widget.name!r} cannot move inside itself or one of its children")
            ancestor = widgets.get(ancestor.parentId)
        if _page_of(project, parent) is not _page_of(project, widget):
            raise ToolError(f"{widget.name!r} and {parent.name!r} are on different pages")
    x, y = project.screen_position(widget)
    origin_x, origin_y = project.screen_position(parent) if parent else (0, 0)
    widget.parentId = parent.id if parent else None
    if not is_component(widget.type):
        widget.props["x"], widget.props["y"] = x - origin_x, y - origin_y


def move_widget(arguments):
    path, project = _load(arguments)
    widget = _widget(project, arguments["name"])
    if "parent" in arguments:
        _set_parent(project, widget, _parent(project, arguments["parent"]) if arguments["parent"] else None)
    page = _page_of(project, widget)
    order, before = arguments.get("order"), arguments.get("before")
    if order is not None and before:
        raise ToolError("Pass order or before, not both")
    if before:
        other = _widget(project, before)
        if other not in page.widgets or other is widget:
            raise ToolError(f"{other.name!r} is not another widget of this page")
        page.widgets.remove(widget)
        page.widgets.insert(page.widgets.index(other), widget)
    elif order is not None:
        page.widgets.remove(widget)
        page.widgets.insert({"front": len(page.widgets), "back": 0}[order] if order in ("front", "back") else int(order), widget)
    return {"parent": _parent_name(project, widget), "order": [item.name for item in page.widgets], "props": {"x": widget.props.get("x"), "y": widget.props.get("y")}, "warnings": _save(path, project, arguments)}


def _parent_name(project, widget):
    return next((item.name for item in project.widgets if item.id == widget.parentId), None)


def update_widget(arguments):
    path, project = _load(arguments)
    widget = _widget(project, arguments["name"])
    props = arguments.get("props") or {}
    _check_props(widget.type, props)
    widget.props.update(props)
    warnings = project.rename_widget(widget.name, arguments["new_name"]) if arguments.get("new_name") else []
    return {"warnings": warnings + _save(path, project, arguments)}


def remove_widget(arguments):
    path, project = _load(arguments)
    removed = [item.name for item in project.subtree(_widget(project, arguments["name"]))]
    project.remove_widget(arguments["name"])
    return {"removed": removed, "warnings": _save(path, project, arguments)}


def set_handler(arguments):
    path, project = _load(arguments)
    owner = arguments["widget"]
    if project.find_widget(owner) is None and all(page.name != owner for page in project.pages):
        raise ToolError(f"Unknown widget or page {owner!r}")
    _check_code(_indented(arguments["body"]), f"handler of {owner}")
    name, handler = project.ensure_handler(owner, arguments.get("event"))
    handler.body = arguments["body"]
    return {"handler": name, "warnings": _save(path, project, arguments)}


def _code_target(arguments):
    if arguments.get("handler") and arguments.get("module"):
        raise ToolError("Pass handler or module, not both")


def _user_module(project, name):
    try:
        return user_modules.find_module(project, name)
    except user_modules.ModuleError:
        raise ToolError(f"Unknown module {name!r}. Modules: {[module.name for module in project.modules]}") from None


def get_code(arguments):
    _code_target(arguments)
    _path, project = _load(arguments)
    revision = arguments[LOADED]
    if arguments.get("module"):
        module = _user_module(project, arguments["module"])
        return {"module": module.name, "file": f"{module.name}.py", "source": module.source, "revision": revision}
    if arguments.get("handler"):
        handler = project.code.handlers.get(arguments["handler"])
        if handler is None:
            raise ToolError(f"Unknown handler {arguments['handler']!r}. Handlers: {sorted(project.code.handlers)}")
        return {"handler": arguments["handler"], "widget": handler.widget, "event": handler.event, "body": handler.body, "revision": revision}
    return {"module": project.code.module, "handlers": sorted(project.code.handlers), "modules": [module.name for module in project.modules], "revision": revision}


def patch_code(arguments):
    _code_target(arguments)
    path, project = _load(arguments)
    if arguments.get("module"):
        module = _user_module(project, arguments["module"])
        count = user_modules.patch_module(project, module.name, arguments["old"], arguments["new"], bool(arguments.get("all")))
        _check_code(module.source, f"{module.name}.py")
        return {"replacements": count, "warnings": _save(path, project, arguments)}
    name = arguments.get("handler")
    handler = project.code.handlers.get(name) if name else None
    if name and handler is None:
        raise ToolError(f"Unknown handler {name!r}. Handlers: {sorted(project.code.handlers)}")
    source = handler.body if handler else project.code.module
    old, new = arguments["old"], arguments["new"]
    count = source.count(old) if old else 0
    if count == 0:
        raise ToolError("The old text was not found")
    if count > 1 and not arguments.get("all"):
        raise ToolError(f"The old text occurs {count} times: add context to make it unique, or pass all")
    patched = source.replace(old, new)
    if handler:
        _check_code(_indented(patched), f"handler {name}")
        handler.body = patched
    else:
        _check_code(patched, "module code")
        project.code.module = patched
    return {"replacements": count, "warnings": _save(path, project, arguments)}


def set_module_code(arguments):
    path, project = _load(arguments)
    _check_code(arguments["code"], "module code")
    project.code.module = arguments["code"]
    return {"warnings": _save(path, project, arguments)}


def list_modules(arguments):
    _path, project = _load(arguments)
    return {
        "modules": [{"name": module.name, "file": f"{module.name}.py", "lines": len(module.source.splitlines())} for module in project.modules],
        "revision": arguments[LOADED],
    }


def create_module(arguments):
    path, project = _load(arguments)
    source = arguments.get("source", "")
    module = user_modules.create_module(project, arguments["name"], source)
    _check_code(module.source, f"{module.name}.py")
    return {"module": module.name, "file": f"{module.name}.py", "warnings": _save(path, project, arguments)}


def rename_module(arguments):
    """Code importing the old name is not rewritten: the warnings list it."""
    path, project = _load(arguments)
    _user_module(project, arguments["name"])
    references = user_modules.rename_module(project, arguments["name"], arguments["new_name"])
    return {"module": arguments["new_name"], "references": references, "warnings": references + _save(path, project, arguments)}


def delete_module(arguments):
    path, project = _load(arguments)
    _user_module(project, arguments["name"])
    references = user_modules.delete_module(project, arguments["name"])
    return {"deleted": arguments["name"], "references": references, "warnings": references + _save(path, project, arguments)}


def add_image(arguments):
    """The file is read on the machine of the server; only PNG, as the core has no picture converter."""
    path, project = _load(arguments)
    source = Path(arguments["file"]).expanduser()
    if not source.is_file():
        raise ToolError(f"Image file not found: {source}")
    name = assets.add_image(project, arguments.get("name") or source.name, source.read_bytes(), replace=bool(arguments.get("replace")))
    return {"image": name, "use": f"set the src property of an image widget to {name!r}", "warnings": _save(path, project, arguments)}


def add_font(arguments):
    path, project = _load(arguments)
    source = Path(arguments["file"]).expanduser()
    if not source.is_file():
        raise ToolError(f"Font file not found: {source}")
    name = assets.add_font(project, arguments.get("name") or source.name, source.read_bytes(), replace=bool(arguments.get("replace")))
    return {"font": name, "use": f"set the font property of a widget to {name!r}, with fontSize for the size", "warnings": _save(path, project, arguments)}


def remove_font(arguments):
    path, project = _load(arguments)
    used = assets.remove_font(project, arguments["name"])
    return {"removed": arguments["name"], "stillUsedBy": used, "warnings": _save(path, project, arguments)}


def remove_image(arguments):
    path, project = _load(arguments)
    used = assets.remove_image(project, arguments["name"])
    return {"removed": arguments["name"], "stillUsedBy": used, "warnings": _save(path, project, arguments)}


def set_resolution(arguments):
    path, project = _load(arguments)
    mode = arguments.get("mode", "stretch")
    if mode not in ("keep", "adapt", "stretch"):
        raise ToolError("mode is keep, adapt or stretch")
    project.resize(arguments["width"], arguments["height"], mode)
    pending = [page.name for page in project.pages if page.designSize]
    return {"outOfBounds": project.widgets_outside(), "pagesToAdapt": pending, "warnings": _save(path, project, arguments)}


def adapt_page(arguments):
    path, project = _load(arguments)
    page = _page(project, arguments.get("page"))
    if not page.designSize:
        raise ToolError(f"Page {page.name!r} is already drawn for the current resolution")
    mode = arguments.get("mode", "adapt")
    if mode not in ("adapt", "stretch"):
        raise ToolError("mode is adapt or stretch")
    project.adapt_page(page, mode)
    return {"outOfBounds": project.widgets_outside(), "warnings": _save(path, project, arguments)}


def validate(arguments):
    _path, project = _load(arguments)
    return {"warnings": validate_project(project) + design_warnings(project), "outOfBounds": project.widgets_outside()}


def render_page(arguments):
    _path, project = _load(arguments)
    index = project.pages.index(_page(project, arguments.get("page")))
    pixels, log = render_with_log(project, index, design_only=arguments.get("design_only", False))
    if pixels is None:
        raise ToolError(f"Rendering failed: {log[-500:]}")
    return _png_content(project, pixels)


def _png_content(project, pixels):
    image = encode_png(rgb565_to_rgb(pixels), project.display.width, project.display.height)
    return {"type": "image", "data": base64.b64encode(image).decode("ascii"), "mimeType": "image/png"}


def simulate(arguments):
    _path, project = _load(arguments)
    index = project.pages.index(_page(project, arguments.get("page")))
    result = play(project, index, arguments.get("steps", []), arguments.get("clock", "virtual"), arguments.get("seed"), arguments.get("design_only", False))
    images = result.pop("images")
    report = {**result, "console": result["console"][-4000:], "images": [label for label, _pixels in images]}
    return Content([{"type": "text", "text": _text(report)}, *(_png_content(project, pixels) for _label, pixels in images)])


def save_scenario(arguments):
    path, project = _load(arguments)
    name, steps = arguments["name"], arguments.get("steps", [])
    if not isinstance(name, str) or not name.strip():
        raise ToolError("name must not be empty")
    page = _page(project, arguments.get("page")).name
    check_script(steps, "virtual")
    scenario = {"name": name, "page": page, "seed": arguments.get("seed", 0), "steps": steps}
    if isinstance(scenario["seed"], bool) or not isinstance(scenario["seed"], int):
        raise ToolError("seed is a whole number")
    saved = save_scenario_file(baseline_dir(path.resolve(), project), scenario)
    return {"file": str(saved), "next": "run visual_test with update true to write its baselines, after checking the run with simulate"}


def visual_test(arguments):
    path, project = _load(arguments)
    results = run_visual_tests(project, baseline_dir(path.resolve(), project), update=arguments.get("update", False), design_only=arguments.get("design_only", False), pages=arguments.get("pages"), scenarios=arguments.get("scenarios"))
    return {
        "passed": all(result.status in (PASSED, UPDATED) for result in results),
        "pages": [{"page": result.page, "status": result.status, "differentPixels": result.different, "box": result.box, "detail": result.message} for result in results],
    }


def measure(arguments):
    _path, project = _load(arguments)
    result = measure_budget(project)
    if result is None:
        raise ToolError("The project does not compile")
    return {"flashBytes": result["flash"], "ramBytes": result["ram"], "note": "RAM is measured on the 64-bit runtime, so it overestimates 32-bit boards"}


def generate_code(arguments):
    path, project = _load(arguments)
    target = arguments.get("target", "micropython")
    default = {"c": path.parent / "build" / "export_c", "board": path.parent / "export_py"}.get(target, path.parent / "build" / "py")
    output = Path(arguments.get("output") or default).expanduser()
    if target == "board":
        from .gen.board_gen import changed_exports, export_board
        if not arguments.get("board") and project.board is None:
            raise ToolError("The project has no board: pass board, or call set_board to save one")
        profile = portable_profile(_board(arguments["board"]) if arguments.get("board") else project.board)
        changed = changed_exports(output)
        if changed and not arguments.get("overwrite"):
            raise ToolError(f"These files changed after the last export: {changed}. Pass overwrite to replace them")
        result = export_board(project, profile, output)
    elif target == "c":
        from .gen.gen_c import generate_c
        result = generate_c(project, output, portable=True)
    else:
        from .gen.project_gen import generate_project
        result = generate_project(project, output)
    return {"output": str(output), "files": result["files"], "warnings": result["warnings"]}


def build(arguments):
    from .build.release import build_release
    _path, project = _load(arguments)
    output = arguments.get("output")
    return {"result": str(build_release(project, arguments.get("target", "micropython"), Path(output).expanduser() if output else None, arguments.get("profile", "debug")))}


def list_boards(_arguments):
    return [{"id": item["id"], "name": item.get("name"), "width": item["logicalWidth"], "height": item["logicalHeight"], "fonts": profile_fonts(item)} for item in ProfileStore().profiles()]


def _board(board_id):
    profile = ProfileStore().get(board_id)
    if profile is None:
        raise ToolError(f"Unknown board {board_id!r}. Boards: {[item['id'] for item in ProfileStore().profiles()]}")
    return profile


def set_board(arguments):
    path, project = _load(arguments)
    profile = portable_profile(_board(arguments["board"]))
    project.board = profile
    project.runTarget = {"kind": "board", "language": "micropython"}
    project.scale_to(profile["logicalWidth"], profile["logicalHeight"])
    return {"outOfBounds": project.widgets_outside(), "warnings": _save(path, project, arguments)}


_session = None


def _device():
    global _session
    if _session is None:
        _session = DeviceSession()
    return _session


def device_list_ports(_arguments):
    return _device().list_ports()


def device_connect(arguments):
    if arguments.get("project"):
        project = _load(arguments)[1]
        if project.board is None:
            raise ToolError("The project has no board: use set_board")
        profile = project.board
    elif arguments.get("board"):
        profile = _board(arguments["board"])
    else:
        raise ToolError("Give a project or a board")
    _device().connect(arguments["port"], profile)
    return {"port": arguments["port"], "board": profile["id"]}


def device_disconnect(_arguments):
    _device().disconnect()
    return {"disconnected": True}


def device_info(_arguments):
    return _device().info()


def device_upload(arguments):
    _path, project = _load(arguments)
    result = _device().upload(project, run=arguments.get("run", False))
    return {key: result[key] for key in ("appPath", "files", "warnings", "output", "active") if key in result}


def device_stop(_arguments):
    return {"output": _device().stop()}


def device_reset(_arguments):
    return {"output": _device().restart()}


def device_exec(arguments):
    return {"output": _device().evaluate(arguments["code"])}


def device_read_console(arguments):
    seconds = min(max(arguments.get("seconds", 2), 0), 30)
    lines, session = [], _device()
    session.start_console(lines.append)
    time.sleep(seconds)
    session.stop_console()
    return {"output": "".join(lines)}


def device_live_update(arguments):
    _path, project = _load(arguments)
    index = project.pages.index(_page(project, arguments.get("page")))
    return {"output": _device().live_update(live_script(project, index))}


def device_autostart_install(arguments):
    return _device().install_autostart(_load(arguments)[1])


def device_autostart_remove(arguments):
    _device().remove_autostart(_load(arguments)[1])
    return {"removed": True}


TOOLS = {name: (globals()[name], *spec) for name, spec in SPECS.items()}  # (function, description, arguments, required)


def _call_tool(params):
    name, arguments = params.get("name"), params.get("arguments") or {}
    if not is_enabled():
        return {"content": [{"type": "text", "text": DISABLED}], "isError": True}
    if name not in TOOLS:
        return {"content": [{"type": "text", "text": f"Unknown tool {name!r}"}], "isError": True}
    function, _description, _schema, required = TOOLS[name]
    try:
        missing = [key for key in required if key not in arguments]
        if missing:
            raise ToolError(f"Missing arguments: {missing}")
        arguments = {key: value for key, value in arguments.items() if key not in (LOADED, SAVED)}
        result = function(arguments)
    except RevisionConflict as exc:
        return {"content": [{"type": "text", "text": _text(exc.data)}], "structuredContent": exc.data, "isError": True}
    except DeviceError as exc:
        warnings = "".join(f"\nWarning: {warning}" for warning in exc.warnings)
        return {"content": [{"type": "text", "text": f"{exc.code}: {device_error_text(exc.code, exc.output)}\n{exc.output}{warnings}"}], "isError": True}
    except CompileError as exc:
        return {"content": [{"type": "text", "text": str(exc)}], "isError": True}
    except (ValueError, OSError, RuntimeError) as exc:  # expected errors: the message is enough
        return {"content": [{"type": "text", "text": str(exc)}], "isError": True}
    except Exception as exc:  # malformed arguments or a defect: the server must stay up and say what happened
        return {"content": [{"type": "text", "text": f"{type(exc).__name__}: {exc}"}], "isError": True}
    if isinstance(result, Content):
        return {"content": result}
    if isinstance(result, dict) and result.get("type") == "image":
        return {"content": [result]}
    if isinstance(result, dict) and SAVED in arguments:
        result["revision"] = arguments[SAVED]
    return {"content": [{"type": "text", "text": _text(result)}]}


def _text(result):
    """Results are read by a model, which pays for every character: no indentation."""
    return json.dumps(result, ensure_ascii=False, separators=(",", ":"))


def _list_tools():
    return {"tools": [
        {"name": name, "description": description, "inputSchema": {"type": "object", "properties": properties, "required": required}}
        for name, (_function, description, properties, required) in TOOLS.items()
    ]}


def _initialize(params):
    requested = params.get("protocolVersion")
    return {
        "protocolVersion": requested if requested in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0],
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "lvgl-mpy-studio", "version": __version__},
        "instructions": INSTRUCTIONS,
    }


def handle(message):
    """Answer a JSON-RPC message; notifications get no answer."""
    if not isinstance(message, dict) or not isinstance(message.get("method"), str):
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid request"}}
    if "id" not in message:
        return None
    method, params = message["method"], message.get("params") or {}
    handlers = {"initialize": _initialize, "ping": lambda _params: {}, "tools/list": lambda _params: _list_tools(), "tools/call": _call_tool}
    if method not in handlers:
        return {"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32601, "message": f"Method not found: {method}"}}
    return {"jsonrpc": "2.0", "id": message["id"], "result": handlers[method](params)}


def serve(stdin=None, stdout=None):
    stdin, stdout = stdin or sys.stdin, stdout or sys.stdout
    set_language("en")  # agents read descriptions and errors in the same language
    sys.stdout = sys.stderr  # stdout belongs to the protocol: nothing must be printed there
    try:
        for line in stdin:
            if not line.strip():
                continue
            try:
                message = json.loads(line)
            except ValueError:
                response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
            else:
                try:
                    response = handle(message)
                except Exception as exc:  # one request must not close the server for the next ones
                    response = {"jsonrpc": "2.0", "id": message.get("id") if isinstance(message, dict) else None, "error": {"code": -32603, "message": f"{type(exc).__name__}: {exc}"}}
            if response is not None:
                stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                stdout.flush()
    finally:
        sys.stdout = stdout
    return 0
