import ast
from pathlib import Path

import PySide6


def test_pyside_version_is_pinned():
    assert PySide6.__version__ == "6.12.0"


def test_core_does_not_import_qt():
    root = Path(__file__).parents[1] / "lvgl_mpy_studio"
    for package in ("core", "gen", "build", "sim"):
        for path in (root / package).rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    assert all(not alias.name.startswith(("PySide6", "PyQt")) for alias in node.names), path
                elif isinstance(node, ast.ImportFrom) and node.module:
                    assert not node.module.startswith(("PySide6", "PyQt")), path


def test_main_window_opens(qtbot):
    from lvgl_mpy_studio.ui.main_window import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    assert window.isVisible()
    assert window.windowTitle() == "Untitled — LVGL MPY Studio"
