import gc

import pytest
from PySide6.QtCore import QSettings

from lvgl_mpy_studio.build.budget import _instrument, measure_budget
from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.platform import runtime_path
from lvgl_mpy_studio.ui import gc_guard, theme
from lvgl_mpy_studio.ui.budget import BudgetMonitor, budget_level, budget_text, format_size
from lvgl_mpy_studio.ui.main_window import MainWindow

needs_runtime = pytest.mark.skipif(not runtime_path().exists(), reason="native runtime not built")


def project_with(count):
    project = Project("budget")
    for index in range(count):
        project.add_widget(project.pages[0], "button", {"x": index, "y": index}, f"button{index}")
    return project


@needs_runtime
def test_more_widgets_cost_more_flash_and_ram():
    small, large = measure_budget(project_with(2)), measure_budget(project_with(40))
    assert 0 < small["flash"] < large["flash"]
    assert 0 < small["ram"] < large["ram"]


@needs_runtime
def test_objects_created_by_code_are_counted():
    plain = measure_budget(project_with(1))
    project = project_with(1)
    project.code.module = "def build():\n    for _ in range(60):\n        lv.obj(lv.screen_active())\n"
    project.ensure_handler("main", "SCREEN_LOADED")[1].body = "build()\n"
    dynamic = measure_budget(project)
    assert dynamic["ram"] > plain["ram"] + 5000


@needs_runtime
def test_runtime_error_keeps_flash_and_hides_ram():
    project = project_with(1)
    project.code.module = "raise ValueError('rotto')\n"
    budget = measure_budget(project)
    assert budget["flash"] > 0
    assert budget["ram"] is None


def test_syntax_error_gives_no_budget():
    project = project_with(1)
    project.code.module = "def rotto(:\n"
    assert measure_budget(project) is None


@needs_runtime
def test_board_flash_counts_uploaded_files():
    project = project_with(1)
    project.set_display_size(240, 240)
    plain = measure_budget(project)
    project.board = builtin_profiles()[0]
    assert measure_budget(project)["flash"] > plain["flash"]


def test_instrumentation_targets_generated_main(tmp_path):
    generate_project(project_with(1), tmp_path)
    source = _instrument((tmp_path / "main.py").read_text())
    assert "_base = gc.mem_alloc()" in source
    assert "_display = gc.mem_alloc() - _before" in source
    assert "raise SystemExit" in source
    compile(source, "main.py", "exec")


def test_unknown_main_is_not_instrumented():
    assert _instrument("print('altro')\n") is None


def test_format_and_levels():
    assert format_size(2048) == "2 KB"
    assert format_size(3 * 1024 * 1024) == "3.0 MB"
    budget = {"flash": 900, "ram": 100}
    assert budget_level(budget, {}) == 0
    assert budget_level(budget, {"flash": 10000, "ram": 10000}) == 0
    assert budget_level(budget, {"flash": 1000}) == 1
    assert budget_level(budget, {"flash": 800}) == 2
    assert budget_level({"flash": 10, "ram": None}, {"flash": 100, "ram": 100}) == 0


def test_text_with_and_without_limits():
    assert "—" in budget_text(None, {})
    assert budget_text({"flash": 2048, "ram": None}, {}) == "Flash 2 KB · RAM ~—"
    assert budget_text({"flash": 2048, "ram": 4096}, {"ram": 8192}) == "Flash 2 KB · RAM ~4 KB / 8 KB"


def test_monitor_waits_for_pause_and_uses_latest_project(qtbot):
    calls = []
    monitor = BudgetMonitor(measure=lambda project, board_mpy: calls.append(project.projectName) or {"flash": 1, "ram": 1}, delay=20)
    for name in ("primo", "ultimo"):
        monitor.schedule(Project(name))
    with qtbot.waitSignal(monitor.updated, timeout=2000):
        pass
    assert calls == ["ultimo"]


def test_monitor_survives_measure_failure(qtbot):
    def fail(project, board_mpy):
        raise RuntimeError("boom")

    monitor = BudgetMonitor(measure=fail, delay=1)
    monitor.schedule(Project("x"))
    with qtbot.waitSignal(monitor.updated, timeout=2000) as signal:
        pass
    assert signal.args == [None]


def test_window_compares_budget_with_board_memory(qtbot, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    window.budget_monitor.stop()
    window.settings = QSettings(str(tmp_path / "settings.ini"), QSettings.IniFormat)
    project = Project("board")
    project.set_display_size(240, 240)
    project.board = builtin_profiles()[0]
    path = tmp_path / "board.json"
    project.save(path)
    assert window.open_project(path)
    window.budget_monitor.stop()
    window._budget_updated({"flash": 2048, "ram": 4096})
    assert window.budget_label.text() == "Flash 2 KB · RAM ~4 KB"
    assert "Connect" in window.budget_label.toolTip()
    window._remember_board_memory({"memoryFree": 4000, "filesystemFree": 100000, "mpy": 0xB06})
    window._show_budget()
    assert "/" in window.budget_label.text()
    assert theme.ERROR in window.budget_label.styleSheet()
    assert window._board_limits()["mpy"] == 0xB06


def test_garbage_collection_stays_in_the_main_thread(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert not gc.isenabled()
    assert gc_guard._timer.isActive()
    first = gc_guard._timer
    gc_guard.install()
    assert gc_guard._timer is first


def test_guard_collects_when_a_threshold_is_passed(monkeypatch):
    collected = []
    monkeypatch.setattr(gc_guard.gc, "get_count", lambda: (1000, 1, 1))
    monkeypatch.setattr(gc_guard.gc, "get_threshold", lambda: (700, 10, 10))
    monkeypatch.setattr(gc_guard.gc, "collect", collected.append)
    gc_guard._collect()
    assert collected == [0]
