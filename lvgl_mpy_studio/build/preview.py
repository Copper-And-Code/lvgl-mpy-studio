"""Real rendering of a page with LVGL, for the designer."""

import copy
import json
import os
from pathlib import Path
import subprocess
import tempfile

from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.platform import CREATE_NO_WINDOW, RUNTIME_ENTRY, runtime_environment, runtime_path

RENDER_TIMEOUT = 5


def design_key(project, page_index):
    """Changes only when what is seen changes: code does not count."""
    data = project.to_dict()
    for key in ("code", "modules", "runTarget", "schemaVersion"):  # code, modules included, is not seen
        data.pop(key, None)
    return json.dumps([page_index, data], sort_keys=True, default=str)


def _design_only(project):
    """User code does not run in the designer: a broken handler must not touch the canvas."""
    design = copy.deepcopy(project)
    design.code.module = ""
    design.code.handlers = {}
    design.modules = []
    for widget in design.widgets:
        widget.events = {}
    return design


def prepare_page(project, page_index, directory, design_only=False, **options):
    """Generate the project in directory, starting from the chosen page. options go to generate_project."""
    generate_project(_design_only(project) if design_only else project, directory, initial_page=page_index, **options)


def render_page(project, page_index):
    """Return the RGB565 pixels of the page, or None if they cannot be obtained."""
    return render_with_log(project, page_index)[0]


def render_with_log(project, page_index, design_only=True):
    """Pixels of the page and output of the runtime. With design_only=False the project code runs too."""
    if not runtime_path().exists():
        return None, "runtime not built"
    with tempfile.TemporaryDirectory(prefix="lvgl-mpy-studio-preview-") as temporary:
        directory = Path(temporary)
        try:
            prepare_page(project, page_index, directory, design_only)
        except (OSError, ValueError) as exc:
            return None, str(exc)
        frame = directory / "frame.raw"
        environment = runtime_environment(LVSIM_HEADLESS="1", LVSIM_FRAMES="1", LVSIM_TICK_MS="0", LVSIM_DUMP=str(frame))
        try:
            done = subprocess.run([str(runtime_path()), *RUNTIME_ENTRY], cwd=directory, env=environment, capture_output=True, timeout=RENDER_TIMEOUT, creationflags=CREATE_NO_WINDOW)
            pixels = frame.read_bytes() if frame.exists() else None
        except subprocess.TimeoutExpired:
            return None, "the runtime did not draw a frame in time"
        except OSError as exc:
            return None, str(exc)
    log = (done.stdout + done.stderr).decode("utf-8", "replace")
    if "Traceback (most recent call last)" in log:  # the frame of an app that raised an error does not count
        return None, log
    expected = project.display.width * project.display.height * 2
    return (pixels, log) if pixels is not None and len(pixels) == expected else (None, log)
