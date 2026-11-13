import copy
import json

import pytest
from PySide6.QtWidgets import QDialog

from lvgl_mpy_studio.cli import main
from lvgl_mpy_studio.core.boards import ProfileStore, builtin_profiles
from lvgl_mpy_studio.core.i18n import set_language, tr
from lvgl_mpy_studio.gen.board_gen import generate_board
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.ui.document import ProjectDocument
from lvgl_mpy_studio.ui.main_window import MainWindow
from lvgl_mpy_studio.ui.profile_manager import ProfileManagerDialog
from lvgl_mpy_studio.ui.project_settings import ProjectSettingsDialog


def test_resolution_roundtrip_new_pages_and_single_undo(tmp_path):
    document = ProjectDocument()
    document.project.add_widget(document.project.pages[0], "button", {"x": 300, "y": 200})
    document.execute("Change Project Settings", lambda project: project.set_display_size(321, 241))
    assert document.project.display.width == 321
    assert all(page.canvasSize == (321, 241) for page in document.project.pages)
    assert document.project.widgets_outside() == ["button1"]
    document.execute("Add Page", lambda project: project.pages.append(project.new_page("other")))
    assert document.project.pages[-1].canvasSize == (321, 241)
    path = tmp_path / "odd.json"
    document.project.save(path)
    assert Project.load(path).pages[-1].canvasSize == (321, 241)
    document.undo_stack.undo()
    assert len(document.project.pages) == 1
    document.undo_stack.undo()
    assert document.project.display.width == 800
    assert document.project.pages[0].canvasSize == (800, 480)
    document.undo_stack.redo()
    assert document.project.pages[0].canvasSize == (321, 241)
    assert document.project.widgets[0].props["x"] == 300


@pytest.mark.parametrize("size", [(240, 240), (480, 480), (1024, 600), (1024, 1024)])
def test_project_settings_presets(qtbot, size):
    project = Project()
    dialog = ProjectSettingsDialog(project, [])
    qtbot.addWidget(dialog)
    index = next(index for index in range(dialog.preset.count()) if dialog.preset.itemData(index) and tuple(dialog.preset.itemData(index)) == size)
    dialog.preset.setCurrentIndex(index)
    dialog._preset_selected()
    assert (dialog.width.value(), dialog.height.value()) == size
    dialog.reject()
    assert (project.display.width, project.display.height) == (800, 480)


def test_profile_store_customize_hide_restore_and_invalid_data(tmp_path):
    path = tmp_path / "profiles.json"
    store = ProfileStore(path)
    original = store.profiles()[0]
    custom = copy.deepcopy(original)
    custom["name"] = "My board"
    custom["revision"] = 2
    store.save_profile(custom)
    store.save()
    loaded = ProfileStore(path)
    assert loaded.get(original["id"])["name"] == "My board"
    loaded.delete(original["id"])
    assert loaded.get(original["id"]) is None
    loaded.save()
    assert ProfileStore(path).get(original["id"]) is None
    loaded.restore_hidden()
    assert loaded.get(original["id"])["origin"] == "builtin"
    duplicate = loaded.new_profile(original)
    assert duplicate["id"] != original["id"]
    loaded.save_profile(duplicate)
    loaded.delete(duplicate["id"])
    assert loaded.get(duplicate["id"]) is None
    path.write_text(json.dumps({"schemaVersion": 1, "custom": {original["id"]: {"id": "broken"}}, "hidden": []}))
    with pytest.raises(ValueError, match="profile.required"):
        ProfileStore(path)


def test_profile_manager_cancel_and_apply(qtbot, tmp_path, monkeypatch):
    store = ProfileStore(tmp_path / "profiles.json")
    dialog = ProfileManagerDialog(store)
    qtbot.addWidget(dialog)
    dialog.name.setText("Draft only")
    dialog.apply_edit()
    dialog.reject()
    assert store.profiles()[0]["name"] != "Draft only"
    dialog = ProfileManagerDialog(store)
    qtbot.addWidget(dialog)
    dialog.name.setText("Persisted")
    dialog.apply_edit()
    dialog.apply_to_store()
    store.save()
    assert ProfileStore(store.path).profiles()[0]["name"] == "Persisted"
    monkeypatch.setattr(store, "save", lambda: (_ for _ in ()).throw(OSError("read only")))
    monkeypatch.setattr("lvgl_mpy_studio.ui.profile_manager.QMessageBox.critical", lambda *args: None)
    dialog._apply()
    assert dialog.result() != QDialog.Accepted


def test_board_generation_uses_firmware_driver_only(tmp_path):
    project = Project("board")
    project.set_display_size(240, 240)
    project.board = builtin_profiles()[0]
    project.add_widget(project.pages[0], "button")
    result = generate_board(project, project.board, tmp_path)
    main = (tmp_path / "app_main.py").read_text()
    assert "import display_driver" in main
    assert "display_driver.start()" in main
    assert "lvsim" not in main
    assert "timer_handler" not in main
    assert "lv.init" not in main
    assert "lv.display_create" not in main
    assert result["manifest"]["entryPoint"] == "app_main.py"
    assert set(result["files"]) == {"ui.py", "app_events.py", "app_main.py", "sourcemap.json", "board_profile.json", "board_adapter.py", "manifest.json"}


def test_language_switch_persists_without_changing_project(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.change_language("it")
    window.add_page()
    before = window.document.project.to_dict()
    window.change_language("en")
    assert window.new_action.text() == "New"
    assert window.undo_action.text() == "Undo Add Page"
    assert window.errors.headerItem().text(2) == "Message"
    assert window.device_console.clear_button.text() == "Clear"
    assert window.properties.events_model.horizontalHeaderItem(1).text() == "Description"
    assert window.settings.value("language") == "en"
    assert window.document.project.to_dict() == before
    window.document.execute("Add Widget", lambda project: None)
    assert "Add Widget" in window.undo_action.text()
    window.change_language("it")
    assert window.undo_action.text() == "Annulla modifica: Aggiungi widget"
    assert window.document.project.to_dict() == before
    assert tr("Cancel") == "Annulla"
    window.document.undo_stack.setClean()


def test_catalog_is_complete_for_literal_gui_strings():
    import ast
    from pathlib import Path

    catalog = json.loads((Path("lvgl_mpy_studio/translations/it.json")).read_text())
    missing = set()
    for path in Path("lvgl_mpy_studio").rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "tr" and node.args and isinstance(node.args[0], ast.Constant):
                text = node.args[0].value
                if text not in catalog:
                    missing.add(f"{path}: {text}")
    assert not missing


def test_cli_language_and_device_list(monkeypatch, capsys):
    class Session:
        def __init__(self):
            pass

        def list_ports(self):
            return [{"port": "/dev/fake", "id": "serial", "usb": "1:2", "description": "Fake"}]

    monkeypatch.setattr("lvgl_mpy_studio.device.service.DeviceSession", Session)
    assert main(["--language", "en", "device", "list"]) == 0
    assert "/dev/fake" in capsys.readouterr().out
    with pytest.raises(SystemExit) as result:
        main(["--language", "en", "device", "--help"])
    assert result.value.code == 0
    assert "MicroPython board operations" in capsys.readouterr().out
    set_language("it")



def test_project_settings_never_substitutes_catalog_copy(qtbot):
    project = Project("portable")
    project.board = copy.deepcopy(builtin_profiles()[0])
    catalog = copy.deepcopy(project.board)
    catalog["revision"] = project.board["revision"] + 1
    catalog["name"] = "Catalog revision"
    dialog = ProjectSettingsDialog(project, [catalog])
    qtbot.addWidget(dialog)
    assert dialog.values()[2] == project.board
    dialog.width.setValue(240)
    dialog.height.setValue(240)
    assert dialog.values()[2]["revision"] == project.board["revision"]
    assert dialog.values()[2]["name"] != "Catalog revision"
    dialog._profile_selected()
    assert dialog.values()[2] == project.board


def test_profile_manager_apply_captures_fields_and_rolls_back(qtbot, tmp_path, monkeypatch):
    store = ProfileStore(tmp_path / "profiles.json")
    dialog = ProfileManagerDialog(store)
    qtbot.addWidget(dialog)
    original = copy.deepcopy(store.profiles()[0])
    dialog.name.setText("Edited and applied")
    dialog._apply()
    assert dialog.result() == QDialog.Accepted
    saved = ProfileStore(store.path).get(original["id"])
    assert saved["name"] == "Edited and applied"
    assert saved["revision"] == original["revision"] + 1

    before = store.snapshot()
    dialog = ProfileManagerDialog(store)
    qtbot.addWidget(dialog)
    dialog.name.setText("Must roll back")
    monkeypatch.setattr(store, "save", lambda: (_ for _ in ()).throw(OSError("read only")))
    monkeypatch.setattr("lvgl_mpy_studio.ui.profile_manager.QMessageBox.critical", lambda *args: None)
    dialog._apply()
    assert store.snapshot() == before


def test_dynamic_tabs_and_object_names_survive_language_changes(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.change_language("it")
    window.add_page()
    window.document.execute("Rename Page", lambda project: setattr(project.pages[1], "name", "Code"))
    window._sync_designers()
    window.change_language("en")
    window.add_page()
    before = window.document.project.to_dict()
    window.change_language("it")
    for page in window.document.project.pages:
        view = window.designers[page.id][1]
        assert window.tabs.tabText(window.tabs.indexOf(view)) == page.name
    assert window.tabs.tabText(window.tabs.indexOf(window.code_panel)) == "Codice"
    page_items = [window.code_panel.object_combo.itemText(index) for index in range(window.code_panel.object_combo.count())]
    assert "Pagina: Code" in page_items
    assert window.document.project.to_dict() == before
    window.document.execute("Riordina pagine", lambda project: project.pages.reverse())
    window._sync_designers()
    window.change_language("en")
    for page in window.document.project.pages:
        view = window.designers[page.id][1]
        assert window.tabs.tabText(window.tabs.indexOf(view)) == page.name
    window.document.execute("Delete Page", lambda project: project.pages.pop(1))
    window._sync_designers()
    before = window.document.project.to_dict()
    window.change_language("it")
    assert window.document.project.to_dict() == before
    assert "Pagina: Codice" not in [window.code_panel.object_combo.itemText(index) for index in range(window.code_panel.object_combo.count())]
    window.document.undo_stack.setClean()
