import hashlib
import json
from pathlib import Path
import re
import shutil

from lvgl_mpy_studio.core.boards import profile_fonts
from lvgl_mpy_studio.core.components import is_component
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.core.modules import module_files
from lvgl_mpy_studio.core.validation import validate_project
from .components import block_files, component_lines, project_components, ui_imports
from .gen_python import build_project_code, generate_python, page_constant
from .identifiers import IdentifierAllocator


def legacy_data(project):
    data = project.to_dict() if isinstance(project, Project) else project
    pages = []
    for page in data["pages"]:
        size = {"width": data.get("display", {}).get("width", 800), "height": data.get("display", {}).get("height", 480)}
        widgets = []
        for widget in page["widgets"]:
            if is_component(widget.get("type")):
                continue
            widgets.append({**widget, "events": [], "animations": widget.get("animations", []), "customStyles": widget.get("customStyles", {})})
        pages.append({"id": page.get("id"), "name": page["name"], "canvasSize": size, "widgets": widgets})
    return {"projectName": data["projectName"], "pages": pages, "assets": data.get("assets", {}), "variables": data.get("variables", [])}


def active_handlers(code):
    """Empty handlers generate no code, unless something calls them."""
    handlers = code.get("handlers") or {}
    text = "\n".join([str(code.get("module") or "")] + [str(handler.get("body") or "") for handler in handlers.values()])
    return {name: handler for name, handler in handlers.items() if str(handler.get("body") or "").strip() or re.search(rf"\b{re.escape(name)}\b", text)}


UI_IMPORT = re.compile(r"^[ \t]*import[ \t]+ui[ \t]*(?:#.*)?$", re.MULTILINE)
UI_FROM = re.compile(r"^[ \t]*from[ \t]+ui[ \t]+import[ \t]+\(?([A-Za-z_][\w \t,]*?)\)?[ \t]*(?:#.*)?$", re.MULTILINE)


def _module_usage(source):
    """Text of a user module ready for the analysis of ui, plus the names taken with from ui import.

    A module must write import ui to use ui.<name>: that line alone does not mean "everything",
    and is removed. Any other use of ui (import ui as u, from ui import *, getattr) stays and
    leads to exposing everything, the cautious choice.
    """
    names = set()
    for match in UI_FROM.finditer(source):
        names.update(name.strip() for name in match.group(1).split(",") if name.strip())
    return UI_FROM.sub("", UI_IMPORT.sub("", source)), names


def code_usage(data):
    """What of the ui module the user code really needs, modules included; None means everything."""
    code = data.get("code") or {}
    active = active_handlers(code)
    text = "\n".join([str(code.get("module") or "")] + [str(handler.get("body") or "") for handler in active.values()])
    imported = set()
    for module in data.get("modules") or []:
        source, names = _module_usage(str(module.get("source") or ""))
        text += "\n" + source
        imported |= names
    if re.search(r"\bui\b(?!\s*\.)", text):
        return {"exposed": None, "helpers": None, "pages": None}
    referenced = set(re.findall(r"\bui\s*\.\s*([A-Za-z_]\w*)", text)) | imported
    owners = {handler.get("widget") for handler in active.values()}
    return {
        "exposed": referenced | owners,
        "helpers": referenced & {"load_page", "load_page_anim", "get_current_page"},
        "pages": referenced & {page_constant(page.get("name")) for page in data.get("pages") or []},
    }


def component_statements(data, expose_all=False):
    """The lines that create the timers and the objects of the blocks, with their handlers."""
    code = data.get("code") or {}
    identifiers = handler_identifiers(code)
    components = {widget["name"] for widget in project_components(data)}
    callbacks = {(handler.get("widget"), handler.get("event")): f"app_events.{identifiers[name]}" for name, handler in active_handlers(code).items() if handler.get("widget") in components}
    return component_lines(data, callbacks, None if expose_all else code_usage(data)["exposed"])


def handler_identifiers(code):
    identifiers = IdentifierAllocator()
    return {name: identifiers.allocate(name, "event_cb") for name in code.get("handlers") or {}}


def indent_body(body):
    normalized = str(body).expandtabs(4).replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.strip(): return ["    pass"], []
    lines = normalized.split("\n")
    if lines and not lines[-1]: lines.pop()
    return [f"    {line}" if line.strip() else "" for line in lines], lines


def generate_app_events(project):
    data = project.to_dict() if isinstance(project, Project) else project
    code = data.get("code") or {}
    identifiers = handler_identifiers(code)
    lines = ["import lvgl as lv", "import ui", ""]
    sourcemap = []
    module = str(code.get("module") or "").expandtabs(4).replace("\r\n", "\n").replace("\r", "\n")
    for source_line, text in enumerate(module.split("\n"), 1):
        if source_line == len(module.split("\n")) and not text: break
        lines.append(text)
        sourcemap.append({"line": len(lines), "handler": "module", "sourceLine": source_line})
    if module: lines.append("")
    for name, handler in active_handlers(code).items():
        lines.append(f"def {identifiers[name]}(e):")
        body_lines, original = indent_body(handler.get("body") or "")
        if not original:
            lines.append(body_lines[0])
            sourcemap.append({"line": len(lines), "handler": name, "sourceLine": 1})
        else:
            for offset, _text in enumerate(original):
                lines.append(body_lines[offset])
                sourcemap.append({"line": len(lines), "handler": name, "sourceLine": offset + 1})
        lines.append("")
    return "\n".join(lines).rstrip() + "\n", {"version": 1, "file": "app_events.py", "entries": sourcemap}


def screen_statements(project, model, expose_all=False):
    """Create all pages, connect the events and start the timers. Loads no page.

    The same lines start the app in the simulator, on a board and after a live update.
    """
    data = project.to_dict() if isinstance(project, Project) else project
    code = data.get("code") or {}
    identifiers = handler_identifiers(code)
    lines = [f"ui.screens = [None] * {len(model['pages'])}"]
    for index, page in enumerate(model["pages"]):
        lines.append(f"ui.screens[{index}] = lv.obj()")
        lines.append(f"ui.{page['functionName']}(ui.screens[{index}])")
    widget_names = {node["widget"]["name"] for page in model["model"]["pages"] for node in page["nodes"]}
    page_names = [page["name"] for page in data["pages"]]
    for name, handler in active_handlers(code).items():
        owner, event = handler.get("widget"), handler.get("event")
        if owner in widget_names:
            lines.append(f"ui.{owner}.add_event_cb(app_events.{identifiers[name]}, lv.EVENT.{event}, None)")
        elif owner in page_names:
            lines.append(f"ui.screens[{page_names.index(owner)}].add_event_cb(app_events.{identifiers[name]}, lv.EVENT.{event}, None)")
    lines.extend(component_statements(data, expose_all))
    return lines


def generate_main(project, model, initial_page=0, expose_all=False, loop_module=None):
    """main.py of the simulator. loop_module: a module imported first and stepped after every LVGL turn."""
    data = project.to_dict() if isinstance(project, Project) else project
    width, height = data.get("display", {}).get("width", 800), data.get("display", {}).get("height", 480)
    lines = [f"import {loop_module}"] if loop_module else []
    loop = [f"        {loop_module}.step()"] if loop_module else []
    # A font of the project is created when ui is imported, and LVGL must be initialised by then.
    # display_driver.init initialises it again, which LVGL ignores.
    early = ["lv.init()"] if (data.get("assets") or {}).get("fonts") else []
    lines += ["import lvgl as lv", "import display_driver", *early, "import ui", "import app_events", "", "", "def main():", f"    display_driver.init({width}, {height})"]
    lines.extend(f"    {line}" for line in screen_statements(data, model, expose_all))
    lines.extend([f"    lv.screen_load(ui.screens[{initial_page}])", f"    ui.current_screen = {initial_page}", "", "    while display_driver.poll():", "        lv.tick_inc(display_driver.tick())", "        lv.timer_handler()", *loop, "        display_driver.wait(display_driver.idle_ms())", "", "", 'if __name__ == "__main__":', "    main()", ""])
    return "\n".join(lines)


MANIFEST = "manifest.json"
APP_MODULES = ("main", "ui", "app_events", "display_driver")
MODULE_ENTRY = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


class ManifestError(RuntimeError):
    """The manifest of the generated folder is missing, broken or does not match the files."""


def _previous_files(output):
    """Files written by the previous generation in this folder, according to its manifest."""
    try:
        files = json.loads((output / MANIFEST).read_text(encoding="utf-8"))["files"]
        return {name for name in files if isinstance(name, str) and Path(name).name == name}
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return set()


def app_modules(directory):
    """Python modules of the app generated in directory, in import order: the only list to use.

    generate_project writes it in the manifest; every pipeline (single file, Release, Debug, web)
    reads it from here instead of keeping a list of its own.
    """
    directory = Path(directory)
    try:
        manifest = json.loads((directory / MANIFEST).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ManifestError(f"No manifest in {directory}: generate the project again") from None
    except (OSError, ValueError) as exc:
        raise ManifestError(f"Unreadable manifest in {directory}: {exc}") from None
    modules = manifest.get("modules") if isinstance(manifest, dict) else None
    if not isinstance(modules, list) or not modules:
        raise ManifestError(f"Incomplete manifest in {directory}: the module list is missing")
    # Each name becomes a path in the copies: identifiers only, never folders.
    invalid = [name for name in modules if not isinstance(name, str) or not MODULE_ENTRY.fullmatch(name)]
    if invalid:
        raise ManifestError(f"Invalid manifest in {directory}: modules {invalid!r}")
    missing = [f"{name}.py" for name in modules if not (directory / f"{name}.py").is_file()]
    if missing:
        raise ManifestError(f"The manifest in {directory} lists missing files: {', '.join(missing)}")
    return list(modules)


LEGACY_HEADER = "LVGL Version: 9.3 (lv_micropython binding)"
HEADER = "LVGL Version: 9.5 (PyDevices binding)"


def ui_source(data, full, expose_all=False, fonts=None):
    """ui.py: the legacy generator stays byte for byte as it is, the version line is corrected here.

    fonts: Montserrat sizes of the target; by default those of the project's board, or of the simulator.
    """
    usage = None if expose_all else code_usage(full)
    fonts = fonts or profile_fonts(full.get("board"))
    from .fonts import convert_fonts  # it imports this package's generator: not at the top

    converted = convert_fonts(data) if (data.get("assets") or {}).get("fonts") else None
    return generate_python(data, "2026-01-01T00:00:00.000Z", converted_fonts=converted, usage=usage, font_sizes=fonts).replace(LEGACY_HEADER, HEADER) + ui_imports(full)


def design_warnings(project):
    """Everything that will not be drawn as designed: sizes, characters, images and fonts."""
    from .fonts import font_warnings

    if not isinstance(project, Project):
        return []
    return project.text_warnings() + (font_warnings(legacy_data(project)) if (project.assets or {}).get("fonts") else [])


def generate_project(project, output_dir, runtime_dir=None, initial_page=None, expose_all=False, loop_module=None):
    """initial_page: index of the page to start from, otherwise the initial page of the project.

    expose_all: ui exposes every widget and helper, even those the code does not use; it serves
    whoever looks inside the app from outside, such as the simulator probe.
    """
    warnings = validate_project(project) + design_warnings(project)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    previous = _previous_files(output)
    data = legacy_data(project)
    model = build_project_code(data)
    full = project.to_dict() if isinstance(project, Project) else project
    app_source, sourcemap = generate_app_events(project)
    if initial_page is None:
        current = full.get("currentPageId")
        initial_page = next((index for index, page in enumerate(full["pages"]) if page.get("id") == current), 0)
    (output / "ui.py").write_text(ui_source(data, full, expose_all), encoding="utf-8", newline="\n")
    (output / "app_events.py").write_text(app_source, encoding="utf-8", newline="\n")
    (output / "main.py").write_text(generate_main(project, model, initial_page, expose_all, loop_module), encoding="utf-8", newline="\n")
    (output / "sourcemap.json").write_text(json.dumps(sourcemap, indent=2) + "\n", encoding="utf-8", newline="\n")
    runtime_dir = Path(runtime_dir) if runtime_dir else Path(__file__).parents[2] / "runtime"
    shutil.copyfile(runtime_dir / "display_driver.py", output / "display_driver.py")
    files = ["ui.py", "app_events.py", "main.py", "display_driver.py", "sourcemap.json"]
    modules = list(APP_MODULES)
    for name, source in block_files(full)[0].items():
        (output / name).write_text(source, encoding="utf-8", newline="\n")
        files.append(name)
        modules.append(name[:-3])
    for name, source in (module_files(project) if isinstance(project, Project) else module_files(Project.from_dict(full))).items():
        (output / name).write_text(source, encoding="utf-8", newline="\n")
        files.append(name)
        modules.append(name[:-3])
    # A removed or renamed module must not stay importable, as .py or as old bytecode.
    for name in previous - set(files):
        (output / name).unlink(missing_ok=True)
        if name.endswith(".py"):
            (output / (name[:-3] + ".mpy")).unlink(missing_ok=True)
    manifest = {"schemaVersion": 1, "entryPoint": "main.py", "modules": modules, "files": {name: hashlib.sha256((output / name).read_bytes()).hexdigest() for name in files}}
    (output / MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    return {"baseName": model["baseName"], "files": files, "warnings": warnings, "modules": modules}
