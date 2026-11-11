"""Live editing: recreate the pages on the board while the app runs, without restarting it."""

import ast
import json

from .gen_python import build_project_code, generate_python
from .components import ui_imports
from lvgl_mpy_studio.core.boards import profile_fonts
from .fonts import convert_fonts
from .project_gen import code_usage, legacy_data, screen_statements

LIVE_OK = "LVGL_MPY_STUDIO_LIVE_OK"
LIVE_FAILED = "LVGL_MPY_STUDIO_LIVE_FAILED"
COMPONENTS = ("buzzer", "timer")


def upload_key(project):
    """Changes when a new upload is needed: live editing replaces only the graphics."""
    data = project.to_dict()
    widgets = [(widget["name"], widget["type"], widget.get("events")) for page in data["pages"] for widget in page["widgets"] if widget["type"] in COMPONENTS]
    return json.dumps([data.get("code"), data.get("modules"), widgets, data.get("display"), (data.get("board") or {}).get("id")], sort_keys=True, default=str)


def design_key(project, page_index):
    data = project.to_dict()
    for key in ("code", "modules", "runTarget", "schemaVersion"):  # code, modules included, is not seen
        data.pop(key, None)
    return json.dumps([page_index, data], sort_keys=True, default=str)


def _compact(source):
    """Without comments and docstrings: every byte goes through the serial line and is compiled on the board."""
    tree = ast.parse(source)
    first = tree.body[0] if tree.body else None
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
        tree.body.pop(0)
    return ast.unparse(tree)


def live_script(project, page_index):
    data = legacy_data(project)
    model = build_project_code(data)
    converted = convert_fonts(data) if (data.get("assets") or {}).get("fonts") else None
    source = generate_python(data, "2026-01-01T00:00:00.000Z", converted_fonts=converted, usage=code_usage(project.to_dict()), font_sizes=profile_fonts(project.board)) + ui_imports(project.to_dict())
    statements = "\n".join("    " + line for line in screen_statements(project, model))
    # They are the same as in the upload: adding one changes upload_key.
    timers = [widget.name for widget in project.widgets if widget.type == "timer"]
    # The old page stays on screen until the new one is ready.
    return f"""import gc, sys
import lvgl as lv
try:
    ui = sys.modules["ui"]
    app_events = sys.modules["app_events"]
    old = ui.screens
    for name in {timers!r}:
        timer = getattr(ui, name, None)
        if timer is not None:
            timer.delete()
    gc.collect()
    exec({_compact(source)!r}, ui.__dict__)
{statements}
    lv.screen_load(ui.screens[{page_index}])
    ui.current_screen = {page_index}
    for screen in old:
        if screen is not None:
            screen.delete()
    gc.collect()
    print({LIVE_OK!r})
except Exception as error:
    print({LIVE_FAILED!r}, repr(error))
"""
