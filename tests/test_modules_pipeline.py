"""User Python modules in every pipeline: simulator, Debug, Release, single file, board, budget, keys, diagnostics."""

import json
from pathlib import Path
import subprocess

import pytest

from lvgl_mpy_studio.build.compiler import CompileError, compile_python, default_mpy_cross, traceback_errors
from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.core.modules import create_module, delete_module, rename_module, set_module_source
from lvgl_mpy_studio.gen.project_gen import ManifestError, app_modules, code_usage, generate_project
from lvgl_mpy_studio.platform import runtime_path

ROOT = Path(__file__).parents[1]
needs_runtime = pytest.mark.skipif(not runtime_path().exists() or not default_mpy_cross().exists(), reason="runtime not built")

HELPERS = """import time

VALUE = "da helpers"


def now():
    return time.ticks_ms()
"""
UTILS = """import helpers
import ui

print("MODULE_OK", helpers.VALUE)


def greet():
    ui.label1.set_text(helpers.VALUE)
    return helpers.VALUE


def boom():
    x = 1
    raise ValueError("rotto nel modulo")
"""


def modular_project(width=480, height=320):
    """Handler → utils → helpers: the general code imports utils, the button uses it."""
    project = Project("modular")
    project.set_display_size(width, height)
    page = project.pages[0]
    project.add_widget(page, "label", {"x": 10, "y": 10, "width": 200, "height": 40, "text": "prima"})
    button = project.add_widget(page, "button", {"x": 10, "y": 80, "width": 140, "height": 60})
    project.code.module = "import utils\n"
    _name, handler = project.ensure_handler(button.name)
    handler.body = "utils.greet()"
    create_module(project, "utils", UTILS)
    create_module(project, "helpers", HELPERS)
    return project


def plain_project():
    project = Project("plain")
    project.add_widget(project.pages[0], "button")
    return project


# --- generation --------------------------------------------------------------------------------

def test_generate_project_writes_modules_verbatim_and_lists_them(tmp_path):
    result = generate_project(modular_project(), tmp_path)
    assert (tmp_path / "utils.py").read_text(encoding="utf-8") == UTILS
    assert (tmp_path / "helpers.py").read_text(encoding="utf-8") == HELPERS
    assert result["modules"] == ["main", "ui", "app_events", "display_driver", "utils", "helpers"]
    assert app_modules(tmp_path) == result["modules"]
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert {"utils.py", "helpers.py", "ui.py"} <= set(manifest["files"])


def test_project_without_modules_generates_the_same_files(tmp_path):
    result = generate_project(plain_project(), tmp_path)
    assert result["files"] == ["ui.py", "app_events.py", "main.py", "display_driver.py", "sourcemap.json"]
    assert result["modules"] == ["main", "ui", "app_events", "display_driver"]
    assert sorted(path.name for path in tmp_path.iterdir()) == sorted(result["files"] + ["manifest.json"])


def test_deleted_and_renamed_modules_leave_no_source_or_bytecode(tmp_path):
    project = modular_project()
    generate_project(project, tmp_path)
    compile_python(tmp_path)
    assert (tmp_path / "helpers.mpy").exists()
    rename_module(project, "helpers", "tools")
    delete_module(project, "utils")
    generate_project(project, tmp_path)
    names = {path.name for path in tmp_path.iterdir()}
    assert {"helpers.py", "helpers.mpy", "utils.py", "utils.mpy"}.isdisjoint(names)
    assert "tools.py" in names


def test_stale_cleanup_never_touches_files_it_did_not_write(tmp_path):
    (tmp_path / "mine.py").write_text("X = 1\n", encoding="utf-8")
    project = modular_project()
    generate_project(project, tmp_path)
    delete_module(project, "helpers")
    generate_project(project, tmp_path)
    assert (tmp_path / "mine.py").read_text(encoding="utf-8") == "X = 1\n"


def test_code_usage_sees_ui_names_used_only_in_modules():
    project = modular_project()
    data = project.to_dict()
    usage = code_usage(data)
    assert usage["exposed"] is not None and "label1" in usage["exposed"]  # import ui alone does not expose everything
    set_module_source(project, "helpers", "from ui import label1, button1\n")
    assert {"label1", "button1"} <= code_usage(project.to_dict())["exposed"]
    for dynamic in ("import ui as u\n", "from ui import *\n", "x = getattr(ui, name)\n"):
        set_module_source(project, "helpers", dynamic)
        assert code_usage(project.to_dict())["exposed"] is None, dynamic


def test_code_usage_without_modules_is_unchanged():
    project = plain_project()
    project.code.module = "import ui\n"  # in the general code the earlier rule still applies
    assert code_usage(project.to_dict())["exposed"] is None


def test_c_export_warns_about_modules(tmp_path):
    from lvgl_mpy_studio.gen.gen_c import generate_c

    result = generate_c(modular_project(), tmp_path / "c", portable=True)
    assert any("utils" in warning and "helpers" in warning for warning in result["warnings"])
    plain = generate_c(plain_project(), tmp_path / "plain", portable=True)
    assert not any("moduli Python" in warning or "Python modules" in warning for warning in plain["warnings"])


# --- simulator -----------------------------------------------------------------------------------

@needs_runtime
def test_handler_module_module_in_the_simulator_with_the_virtual_clock():
    from lvgl_mpy_studio.sim.script import play

    steps = [
        {"action": "wait", "ms": 300},
        {"action": "eval", "expr": "ui.label1.get_text()", "label": "before"},
        {"action": "tap", "widget": "button1"},
        {"action": "wait", "ms": 200},
        {"action": "eval", "expr": "ui.label1.get_text()", "label": "after"},
        {"action": "eval", "expr": "utils.helpers.now()", "label": "clock"},
        {"action": "wait", "ms": 1000},
        {"action": "eval", "expr": "utils.helpers.now()", "label": "clock_later"},
    ]
    report = play(modular_project(), 0, steps)
    values = {item["label"]: item["value"] for item in report["values"]}
    assert report["passed"], report
    assert "MODULE_OK da helpers" in report["console"]
    assert values["before"] == "prima" and values["after"] == "da helpers"
    # time.ticks_ms() of an imported module follows the simulated clock, in 10 ms steps.
    assert values["clock_later"] - values["clock"] == 1000


@needs_runtime
def test_traceback_from_a_module_points_to_its_file_and_line():
    from lvgl_mpy_studio.sim.script import play

    project = modular_project()
    project.code.handlers[next(iter(project.code.handlers))].body = "utils.boom()"
    report = play(project, 0, [{"action": "wait", "ms": 200}, {"action": "tap", "widget": "button1"}, {"action": "wait", "ms": 300}])
    assert report["traceback"]
    errors = traceback_errors(report["console"], None, {"utils", "helpers"})
    module_error = next(error for error in errors if error.get("module") == "utils")
    line = UTILS.splitlines().index('    raise ValueError("rotto nel modulo")') + 1
    assert module_error["sourceLine"] == line and module_error["file"].endswith("utils.py")


def test_traceback_errors_maps_handlers_and_modules_and_ignores_the_rest():
    sourcemap = {"entries": [{"line": 4, "handler": "module", "sourceLine": 1}, {"line": 7, "handler": "button1_clicked", "sourceLine": 1}]}
    text = (
        'Traceback (most recent call last):\n'
        '  File "main.py", line 20, in main\n'
        '  File "/lms_apps/abc/app_events.py", line 7, in button1_clicked\n'
        '  File "/lms_apps/abc/utils.py", line 12, in boom\n'
        '  File "utils.py", line 12, in boom\n'
        '  File "display_driver.py", line 3, in tick\n'
        'ValueError: rotto\n'
    )
    errors = traceback_errors(text, sourcemap, {"utils"})
    assert [(error.get("handler"), error.get("module"), error["sourceLine"]) for error in errors] == [("button1_clicked", None, 1), (None, "utils", 12), (None, "utils", 12)]


def test_compile_error_in_a_module_keeps_file_and_line(tmp_path):
    if not default_mpy_cross().exists():
        pytest.skip("mpy-cross not built")
    project = modular_project()
    set_module_source(project, "helpers", "X = 1\n\ndef broken(:\n    pass\n")
    generate_project(project, tmp_path)
    with pytest.raises(CompileError) as error:
        compile_python(tmp_path)
    found = [item for item in error.value.errors if Path(item["file"]).name == "helpers.py"]
    assert found and found[0]["line"] == 3


def test_simulator_console_errors_name_the_module(qtbot, tmp_path):
    from lvgl_mpy_studio.ui.main_window import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)
    window.document.project = modular_project()
    window._sim_output('Traceback (most recent call last):\n  File "utils.py", line 14, in boom\nValueError: rotto\n', True)
    rows = [window.errors.topLevelItem(index) for index in range(window.errors.topLevelItemCount())]
    assert [(row.text(0), row.text(1)) for row in rows] == [("utils.py", "14")]
    window.document.undo_stack.setClean()


# --- keys ----------------------------------------------------------------------------------------

def test_module_change_invalidates_the_upload_but_not_the_designer_preview():
    from lvgl_mpy_studio.build import preview
    from lvgl_mpy_studio.gen import live

    project = modular_project()
    upload, design, live_design = live.upload_key(project), preview.design_key(project, 0), live.design_key(project, 0)
    set_module_source(project, "helpers", HELPERS + "\nEXTRA = 1\n")
    assert live.upload_key(project) != upload
    assert preview.design_key(project, 0) == design and live.design_key(project, 0) == live_design
    create_module(project, "more", "")
    assert live.upload_key(project) != upload
    assert preview.design_key(project, 0) == design


def test_first_and_last_module_do_not_change_the_preview_key():
    """The schemaVersion step 2 → 3 → 2 must not redraw the canvas."""
    from lvgl_mpy_studio.build import preview

    project = plain_project()
    key = preview.design_key(project, 0)
    create_module(project, "solo", "")
    assert project.to_dict()["schemaVersion"] == 3 and preview.design_key(project, 0) == key
    delete_module(project, "solo")
    assert project.to_dict()["schemaVersion"] == 2 and preview.design_key(project, 0) == key


# --- desktop builds -----------------------------------------------------------------------------

def _selftest(command, cwd):
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=120)


@needs_runtime
def test_debug_build_runs_modules_and_drops_stale_bytecode(tmp_path):
    from lvgl_mpy_studio.build.release import build_micropython_release

    project = modular_project()
    runner = build_micropython_release(project, tmp_path, "debug")
    output = runner.parent
    assert {"utils.mpy", "helpers.mpy"} <= {path.name for path in output.iterdir()}
    result = _selftest(["./run.sh", "--selftest"], output)
    assert result.returncode == 0 and "MODULE_OK da helpers" in result.stdout, result.stdout + result.stderr
    delete_module(project, "helpers")
    set_module_source(project, "utils", "print('MODULE_OK solo utils')\n")
    build_micropython_release(project, tmp_path, "debug")
    assert "helpers.mpy" not in {path.name for path in output.iterdir()}
    result = _selftest(["./run.sh", "--selftest"], output)
    assert result.returncode == 0 and "MODULE_OK solo utils" in result.stdout, result.stdout + result.stderr


@needs_runtime
def test_debug_build_without_modules_has_the_same_files(tmp_path):
    from lvgl_mpy_studio.build.release import build_micropython_release

    output = build_micropython_release(plain_project(), tmp_path, "debug").parent
    assert sorted(path.name for path in output.glob("*.mpy")) == ["app_events.mpy", "display_driver.mpy", "main.mpy", "ui.mpy"]


def _release_toolchain():
    return all((ROOT / "runtime/modules" / name).exists() for name in ("lvsim", "lvgl-bindings", "lvgl-micropython")) and (ROOT / ".reference/micropython/ports/unix").exists()


@needs_runtime
@pytest.mark.skipif(not _release_toolchain(), reason="MicroPython sources for the Release build not available")
def test_release_build_freezes_the_modules(tmp_path):
    from lvgl_mpy_studio.build.release import build_micropython_release

    runner = build_micropython_release(modular_project(), tmp_path, "release")
    output = runner.parent
    assert not list(output.glob("*.mpy")) and not list(output.glob("*.py"))
    result = _selftest(["./run.sh", "--selftest"], output)
    assert result.returncode == 0 and "MODULE_OK da helpers" in result.stdout, result.stdout + result.stderr


@pytest.mark.skipif(not (ROOT / "runtime/out/lvsim-onefile").exists() or not default_mpy_cross().exists(), reason="single-file launcher not built")
def test_single_file_contains_the_modules(tmp_path):
    from lvgl_mpy_studio.build.release import build_single_file

    executable = build_single_file(modular_project(), tmp_path / "dist")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / "helpers.py").write_text("VALUE = 'FAKE accanto al gioco'\n", encoding="utf-8")  # the ROMFS must win
    result = _selftest([str(executable), "--selftest"], elsewhere)
    assert result.returncode == 0 and "MODULE_OK da helpers" in result.stdout, result.stdout + result.stderr


# --- budget --------------------------------------------------------------------------------------

@needs_runtime
def test_budget_counts_the_modules():
    from lvgl_mpy_studio.build.budget import measure_budget

    project = modular_project()
    with_modules = measure_budget(project)
    big = project
    set_module_source(big, "helpers", HELPERS + "\nTABLE = " + repr(list(range(400))) + "\n")
    bigger = measure_budget(big)
    assert with_modules and bigger and bigger["flash"] > with_modules["flash"]
    assert bigger["ram"] is not None


# --- boards --------------------------------------------------------------------------------------

def _board_project():
    project = modular_project(240, 240)
    project.board = builtin_profiles()[0]
    return project


def test_board_package_and_manifest_contain_the_modules(tmp_path):
    import hashlib

    from lvgl_mpy_studio.gen.board_gen import generate_board

    project = _board_project()
    profile = dict(project.board)
    profile.pop("origin", None)
    generated = generate_board(project, profile, tmp_path)
    assert {"utils.py", "helpers.py"} <= set(generated["files"])
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    for name, source in (("utils.py", UTILS), ("helpers.py", HELPERS)):
        assert manifest["files"][name] == hashlib.sha256(source.encode("utf-8")).hexdigest()
    assert {"utils.py", "helpers.py"} <= set(generated["precompile"])


def test_board_precompiles_the_modules_too(tmp_path):
    if not default_mpy_cross().exists():
        pytest.skip("mpy-cross not built")
    from lvgl_mpy_studio.gen.board_gen import generate_board, precompile_board

    project = _board_project()
    profile = dict(project.board)
    profile.pop("origin", None)
    generated = generate_board(project, profile, tmp_path)
    probe = tmp_path / "probe.mpy"
    subprocess.run([str(default_mpy_cross()), "-o", str(probe), str(tmp_path / "ui.py")], check=True)
    result = precompile_board(generated, tmp_path, probe.read_bytes()[1])
    assert {"utils.mpy", "helpers.mpy", "ui.mpy"} <= set(result["files"])
    assert not {"utils.py", "helpers.py"} & set(result["files"])
    assert {"utils.mpy", "helpers.mpy"} <= set(result["manifest"]["files"])


def test_board_export_removes_a_deleted_module(tmp_path):
    from lvgl_mpy_studio.gen.board_gen import export_board

    project = _board_project()
    profile = dict(project.board)
    profile.pop("origin", None)
    export_board(project, profile, tmp_path)
    assert (tmp_path / "helpers.py").exists()
    delete_module(project, "helpers")
    set_module_source(project, "utils", "X = 1\n")
    export_board(project, profile, tmp_path)
    assert not (tmp_path / "helpers.py").exists() and (tmp_path / "utils.py").exists()


def test_board_syntax_error_in_a_module_names_the_module(tmp_path):
    from lvgl_mpy_studio.gen.board_gen import BoardSyntaxError, generate_board

    project = _board_project()
    set_module_source(project, "helpers", "X = 1\nY = (\n")
    profile = dict(project.board)
    profile.pop("origin", None)
    with pytest.raises(BoardSyntaxError) as error:
        generate_board(project, profile, tmp_path)
    found = error.value.errors[0]
    assert found["file"] == "helpers.py" and found.get("module") == "helpers" and found.get("handler") is None


def test_stop_script_forgets_the_modules_of_the_app():
    from lvgl_mpy_studio.device.service import stop_script

    script = stop_script("/lms_apps")
    compile(script, "stop", "exec")
    assert "'/lms_apps/'" in script and "LVGL_MPY_STUDIO_STOPPED" in script
    assert "sys.modules.pop(name,None)" in script


@pytest.mark.parametrize("manifest, text", [
    (None, "No manifest"),
    ("{non json", "Unreadable"),
    ('["main"]', "Incomplete"),
    ('{"files": {}}', "Incomplete"),
    ('{"modules": []}', "Incomplete"),
    ('{"modules": "main"}', "Incomplete"),
    ('{"modules": ["main", "../fuori"]}', "Invalid manifest"),
    ('{"modules": ["main", "sub/mod"]}', "Invalid manifest"),
    ('{"modules": ["main", 3]}', "Invalid manifest"),
    ('{"modules": ["main", "utils"]}', "utils.py"),
])
def test_app_modules_refuses_a_missing_broken_or_inconsistent_manifest(tmp_path, manifest, text):
    """No pipeline copies files at random: without a coherent manifest it stops with a clear error."""
    (tmp_path / "main.py").write_text("", encoding="utf-8")
    if manifest is not None:
        (tmp_path / "manifest.json").write_text(manifest, encoding="utf-8")
    with pytest.raises(ManifestError, match=text):
        app_modules(tmp_path)


def test_a_broken_manifest_does_not_stop_the_next_generation(tmp_path):
    project = modular_project()
    generate_project(project, tmp_path)
    (tmp_path / "manifest.json").write_text("{rotto", encoding="utf-8")
    result = generate_project(project, tmp_path)
    assert app_modules(tmp_path) == result["modules"]


def test_a_frozen_build_stops_on_a_manifest_that_names_a_missing_file(tmp_path, monkeypatch):
    from lvgl_mpy_studio.build import release

    (tmp_path / "manifest.json").write_text('{"modules": ["main", "utils"], "files": {}}', encoding="utf-8")
    (tmp_path / "main.py").write_text("", encoding="utf-8")
    with pytest.raises(ManifestError, match="utils.py"):
        release._frozen_runtime(tmp_path)
    with pytest.raises(ManifestError, match="utils.py"):
        release._app_image(tmp_path)
