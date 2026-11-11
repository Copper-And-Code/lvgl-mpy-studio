import json
from pathlib import Path

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox

from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.platform import runtime_path
from lvgl_mpy_studio.ui.main_window import MainWindow

ROOT = Path(__file__).parents[1]


def test_shell_opens_real_project_and_populates_tree(qtbot, tmp_path):
    raw = json.loads((ROOT / "reference/corpus/widget-01-button.json").read_text())
    path = tmp_path / "project.json"
    path.write_text(json.dumps(raw["project"]))
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.open_project(path)
    assert window.project_tree.topLevelItemCount() == 2  # the page, then the Python Modules node
    assert window.project_tree.topLevelItem(0).childCount() > 0
    assert window.project_tree.topLevelItem(1).data(0, Qt.UserRole) == ("modules", None)
    assert window.project_tree.topLevelItem(1).childCount() == 0
    assert window.tabs.count() == len(window.document.project.pages) + 2
    assert window.document.save(tmp_path / "roundtrip.json")
    assert Project.load(tmp_path / "roundtrip.json").widgets
    window.add_page()
    assert len(window.document.project.pages) == 2
    window.document.undo_stack.undo()
    assert len(window.document.project.pages) == 1


@pytest.mark.skipif(not runtime_path().exists(), reason="native runtime not built")
def test_run_action_reaches_frame_and_stops(qtbot, tmp_path):
    project = Project("window_run")
    project.add_widget(project.pages[0], "button")
    path = tmp_path / "project.json"
    project.save(path)
    window = MainWindow()
    qtbot.addWidget(window)
    window.open_project(path)
    window.show()
    assert window.run_project()
    with qtbot.waitSignal(window.sim_panel.frameReady, timeout=5000, raising=True):
        pass
    assert window.stop_action.isEnabled()
    window.stop_simulation()
    with qtbot.waitSignal(window.sim_panel.stopped, timeout=5000, raising=True):
        pass
    assert not window.sim_panel.running
    assert not window.document.read_only


def recent_window(qtbot, tmp_path):
    old_path = tmp_path / "old.json"
    new_path = tmp_path / "new.json"
    Project("old").save(old_path)
    Project("new").save(new_path)
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.open_project(old_path)
    window.document.execute("Edit", lambda project: setattr(project, "projectName", "edited"))
    window.settings.setValue("recentFiles", [str(new_path.resolve())])
    window._populate_recent()
    return window, old_path, new_path


@pytest.mark.parametrize("answer", [QMessageBox.Cancel, QMessageBox.Discard, QMessageBox.Save])
def test_recent_file_confirmation(qtbot, tmp_path, monkeypatch, answer):
    window, old_path, new_path = recent_window(qtbot, tmp_path)
    calls = []
    monkeypatch.setattr(QMessageBox, "question", lambda *args: calls.append(args) or answer)
    window.recent_menu.actions()[0].trigger()
    assert len(calls) == 1
    if answer == QMessageBox.Cancel:
        assert window.document.project.projectName == "edited"
        assert window.document.modified
        assert window.document.undo_stack.canUndo()
    else:
        assert window.document.project.projectName == "new"
        assert window.document.path == new_path
    if answer == QMessageBox.Save:
        assert Project.load(old_path).projectName == "edited"


@pytest.mark.parametrize("failure", ["cancelled", "failed"])
def test_recent_file_save_failure_preserves_document(qtbot, tmp_path, monkeypatch, failure):
    window, _old_path, _new_path = recent_window(qtbot, tmp_path)
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Save)
    monkeypatch.setattr(QMessageBox, "critical", lambda *args: QMessageBox.Ok)
    if failure == "cancelled":
        window.document.path = None
        monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args, **kwargs: ("", ""))
    else:
        def fail_save(*args, **kwargs):
            raise OSError("disco non disponibile")
        monkeypatch.setattr(window.document, "save", fail_save)
    window.recent_menu.actions()[0].trigger()
    assert window.document.project.projectName == "edited"
    assert window.document.modified
    assert window.document.undo_stack.canUndo()


def test_normal_open_asks_for_confirmation_once(qtbot, tmp_path, monkeypatch):
    window, _old_path, new_path = recent_window(qtbot, tmp_path)
    calls = []
    monkeypatch.setattr(QMessageBox, "question", lambda *args: calls.append(args) or QMessageBox.Discard)
    monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda *args, **kwargs: (str(new_path), ""))
    window.open_project_dialog()
    assert len(calls) == 1
    assert window.document.project.projectName == "new"


def test_delete_initial_page_round_trip_generation_and_undo(qtbot, tmp_path):
    from lvgl_mpy_studio.core.validation import validate_project
    from lvgl_mpy_studio.gen.gen_c import generate_c
    from lvgl_mpy_studio.gen.project_gen import generate_project

    window = MainWindow()
    qtbot.addWidget(window)
    initial_id = window.document.project.currentPageId
    window.document.execute("Aggiungi gestore pagina", lambda project: project.ensure_handler("main", "SCREEN_LOADED"))
    window.add_page()
    remaining_id = window.document.project.pages[1].id
    window.project_tree.setCurrentItem(window.project_tree.topLevelItem(0))
    window.delete_page()
    assert [page.id for page in window.document.project.pages] == [remaining_id]
    assert window.document.project.currentPageId == remaining_id
    assert window.document.project.code.handlers["main_screen_loaded"].widget == "main"
    validate_project(window.document.project)
    path = tmp_path / "page.json"
    window.document.save(path)
    assert Project.load(path).currentPageId == remaining_id
    generate_project(window.document.project, tmp_path / "python")
    generate_c(window.document.project, tmp_path / "c")

    window.document.undo_stack.undo()
    assert window.document.project.currentPageId == initial_id
    assert len(window.document.project.pages) == 2
    window.document.undo_stack.redo()
    assert window.document.project.currentPageId == remaining_id
    assert len(window.document.project.pages) == 1
    window.document.undo_stack.setClean()


def test_delete_non_initial_and_last_page(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    initial_id = window.document.project.currentPageId
    window.add_page()
    window.project_tree.setCurrentItem(window.project_tree.topLevelItem(1))
    window.delete_page()
    assert window.document.project.currentPageId == initial_id
    window.delete_page()
    assert len(window.document.project.pages) == 1
    assert window.document.project.currentPageId == initial_id
    window.document.undo_stack.setClean()


def test_recreating_widget_reattaches_orphan_from_code_editor(qtbot, tmp_path):
    from lvgl_mpy_studio.gen.project_gen import generate_project

    window = MainWindow()
    qtbot.addWidget(window)
    window.document.execute("Aggiungi pulsante", lambda project: project.add_widget(project.pages[0], "button", name="button1"))
    window.open_handler("button1", "CLICKED")
    window.code_panel.editor.setPlainText('print("preserved")')
    window.document.execute("Elimina pulsante", lambda project: project.remove_widget("button1"))
    assert window.document.project.code.handlers["button1_clicked"].widget == ""
    window.document.execute("Ricrea pulsante", lambda project: project.add_widget(project.pages[0], "button", name="button1"))
    window.open_handler("button1", "CLICKED")
    handler = window.document.project.code.handlers["button1_clicked"]
    assert handler.widget == "button1"
    assert handler.body == 'print("preserved")'
    assert window.document.project.find_widget("button1").events["CLICKED"] == "button1_clicked"
    window.document.undo_stack.undo()
    assert window.document.project.code.handlers["button1_clicked"].widget == ""
    window.document.undo_stack.redo()
    assert window.document.project.code.handlers["button1_clicked"].widget == "button1"
    path = tmp_path / "orphan.json"
    window.document.save(path)
    loaded = Project.load(path)
    assert loaded.code.handlers["button1_clicked"].body == 'print("preserved")'
    generate_project(loaded, tmp_path / "generated")
    assert "ui.button1.add_event_cb(app_events.button1_clicked" in (tmp_path / "generated/main.py").read_text()
    window.document.undo_stack.setClean()


def _changed_outside(path, name):
    project = Project.load(path)
    project.projectName = name
    project.save(path)


@pytest.mark.parametrize("choice", [None, "reload", "copy", "overwrite"])
def test_save_asks_before_overwriting_an_external_change(qtbot, tmp_path, monkeypatch, choice):
    path = tmp_path / "project.json"
    Project().save(path)
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.open_project(path)
    window.document.execute("Edit", lambda project: setattr(project, "projectName", "locale"))
    _changed_outside(path, "da MCP")
    asked = []
    monkeypatch.setattr(window, "_ask_external_change", lambda deleted=False: asked.append(deleted) or choice)
    copy = tmp_path / "project-copy.json"
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args: (str(copy), ""))
    saved = window.save_project()
    assert asked == [False]
    if choice is None:
        assert not saved
        assert Project.load(path).projectName == "da MCP"
        assert window.document.project.projectName == "locale" and window.document.modified
    elif choice == "reload":
        assert saved and window.document.project.projectName == "da MCP" and not window.document.modified
    elif choice == "copy":
        assert saved and Project.load(path).projectName == "da MCP"
        assert Project.load(copy).projectName == "locale" and window.document.path == copy
    else:
        assert saved and Project.load(path).projectName == "locale"
    window.document.undo_stack.setClean()  # closing the test must not ask


def test_closing_with_an_external_change_does_not_lose_anything(qtbot, tmp_path, monkeypatch):
    path = tmp_path / "project.json"
    Project().save(path)
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.open_project(path)
    window.document.execute("Edit", lambda project: setattr(project, "projectName", "locale"))
    _changed_outside(path, "da MCP")
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Save)
    monkeypatch.setattr(window, "_ask_external_change", lambda deleted=False: None)
    assert not window._confirm_discard()  # cancelled: the window stays open
    assert Project.load(path).projectName == "da MCP"
    assert window.document.project.projectName == "locale"
    window.document.undo_stack.setClean()


def test_reload_of_a_broken_external_file_keeps_local_changes(qtbot, tmp_path, monkeypatch):
    path = tmp_path / "project.json"
    Project().save(path)
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.open_project(path)
    window.document.execute("Edit", lambda project: setattr(project, "projectName", "locale"))
    path.write_text("{rotto", encoding="utf-8")
    errors = []
    monkeypatch.setattr(QMessageBox, "critical", lambda *args: errors.append(args) or QMessageBox.Ok)
    monkeypatch.setattr(window, "_ask_external_change", lambda deleted=False: "reload")
    assert not window.save_project()
    assert errors
    assert window.document.project.projectName == "locale" and window.document.modified
    assert path.read_text(encoding="utf-8") == "{rotto"
    window.document.undo_stack.setClean()


@pytest.mark.parametrize("label, expected", [("Reload", "reload"), ("Save a copy…", "copy"), ("Overwrite", "overwrite")])
def test_external_change_dialog_maps_buttons_to_choices(qtbot, tmp_path, monkeypatch, label, expected):
    path = tmp_path / "project.json"
    Project().save(path)
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.open_project(path)

    def click(box):
        from lvgl_mpy_studio.core.i18n import tr

        next(button for button in box.buttons() if button.text() == tr(label)).click()  # another test may have changed the language

    monkeypatch.setattr(QMessageBox, "exec", click)
    assert window._ask_external_change() == expected


@pytest.mark.parametrize("choice", [None, "overwrite", "copy"])
def test_save_asks_before_recreating_a_deleted_file(qtbot, tmp_path, monkeypatch, choice):
    path = tmp_path / "project.json"
    Project().save(path)
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.open_project(path)
    window.document.execute("Edit", lambda project: setattr(project, "projectName", "locale"))
    path.unlink()
    asked = []
    monkeypatch.setattr(window, "_ask_external_change", lambda deleted=False: asked.append(deleted) or choice)
    copy = tmp_path / "altrove.json"
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args: (str(copy), ""))
    saved = window.save_project()
    assert asked == [True]
    if choice is None:
        assert not saved and not path.exists() and window.document.modified
    elif choice == "overwrite":
        assert saved and Project.load(path).projectName == "locale"
    else:
        assert saved and not path.exists() and Project.load(copy).projectName == "locale"
    window.document.undo_stack.setClean()


@pytest.mark.parametrize("label, expected", [("Recreate the file", "overwrite"), ("Save a copy…", "copy")])
def test_deleted_file_dialog_offers_no_reload(qtbot, tmp_path, monkeypatch, label, expected):
    from lvgl_mpy_studio.core.i18n import tr

    path = tmp_path / "project.json"
    Project().save(path)
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.open_project(path)
    seen = []

    def click(box):
        seen.extend(button.text() for button in box.buttons())
        next(button for button in box.buttons() if button.text() == tr(label)).click()

    monkeypatch.setattr(QMessageBox, "exec", click)
    assert window._ask_external_change(deleted=True) == expected
    assert tr("Reload") not in seen


@pytest.mark.parametrize("answer", [QMessageBox.No, QMessageBox.Yes])
def test_save_a_copy_never_replaces_another_project_without_asking(qtbot, tmp_path, monkeypatch, answer):
    path = tmp_path / "project.json"
    Project().save(path)
    other = tmp_path / "altro.json"
    neighbour = Project()
    neighbour.projectName = "altro progetto"
    neighbour.save(other)
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.open_project(path)
    window.document.execute("Edit", lambda project: setattr(project, "projectName", "locale"))
    _changed_outside(path, "da MCP")
    options = []
    monkeypatch.setattr(window, "_ask_external_change", lambda deleted=False: "copy")
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args: options.append(args[-1]) or (str(other), ""))
    questions = []
    monkeypatch.setattr(QMessageBox, "question", lambda *args: questions.append(args[2]) or answer)
    saved = window.save_project()
    assert options == [QFileDialog.DontConfirmOverwrite]  # the IDE asks to confirm, not the system dialog
    assert len(questions) == 1 and "altro.json" in questions[0]
    assert Project.load(path).projectName == "da MCP"
    if answer == QMessageBox.No:
        assert not saved and Project.load(other).projectName == "altro progetto"
        assert window.document.path == path and window.document.modified
    else:
        assert saved and Project.load(other).projectName == "locale"
    window.document.undo_stack.setClean()


def test_copy_name_is_free(qtbot, tmp_path):
    path = tmp_path / "project.json"
    Project().save(path)
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.open_project(path)
    first = window._copy_name()
    assert not first.exists()
    Project().save(first)
    second = window._copy_name()
    assert second != first and not second.exists() and second.parent == path.parent
