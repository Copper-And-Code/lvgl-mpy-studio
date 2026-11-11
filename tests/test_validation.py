import json

import pytest
from PySide6.QtWidgets import QMessageBox

from lvgl_mpy_studio.cli import main
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.core.validation import validate_project
from lvgl_mpy_studio.gen.gen_c import generate_c
from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.ui.main_window import MainWindow


def project_with_child():
    project = Project("validation")
    panel = project.add_widget(project.pages[0], "panel", name="container")
    button = project.add_widget(project.pages[0], "button", name="okButton")
    button.parentId = panel.id
    project.ensure_handler("okButton")
    return project, panel, button


def test_valid_project_and_unknown_properties_are_preserved(tmp_path):
    project, panel, _button = project_with_child()
    panel.props["legacyProperty"] = "keep"
    project.remove_widget("okButton")
    warnings = validate_project(project)
    assert any("props.legacyProperty" in warning for warning in warnings)
    assert any("orphan handler" in warning for warning in warnings)
    path = tmp_path / "valid.json"
    project.save(path)
    loaded = Project.load(path)
    assert loaded.pages[0].widgets[0].props["legacyProperty"] == "keep"
    assert loaded.code.handlers["okButton_clicked"].widget == ""


def test_validation_reports_field_paths_and_multiple_errors():
    project, panel, button = project_with_child()
    data = project.to_dict()
    data["display"]["width"] = 0
    data["pages"][0]["widgets"][1]["id"] = panel.id
    data["pages"][0]["widgets"][1]["name"] = "not valid"
    data["pages"][0]["widgets"][1]["parentId"] = "missing"
    data["pages"][0]["widgets"][1]["events"]["UNKNOWN"] = "bad"
    with pytest.raises(ValueError) as caught:
        validate_project(data)
    message = str(caught.value)
    for expected in ("display.width", "pages[0].widgets[1].id", "pages[0].widgets[1].name", "pages[0].widgets[1].parentId", "pages[0].widgets[1].events.UNKNOWN"):
        assert expected in message


def test_validation_rejects_parent_cycles():
    project = Project("cycles")
    first = project.add_widget(project.pages[0], "panel", name="firstPanel")
    second = project.add_widget(project.pages[0], "panel", name="secondPanel")
    first.parentId = second.id
    second.parentId = first.id
    with pytest.raises(ValueError, match="cycle in the containers"):
        validate_project(project)


def test_validation_rejects_incoherent_handler_association():
    project, _panel, button = project_with_child()
    project.ensure_handler("okButton", "FOCUSED")
    button.events["CLICKED"] = "okButton_focused"
    with pytest.raises(ValueError, match="does not match"):
        validate_project(project)


def test_validation_rejects_missing_widget_handler():
    project, _panel, _button = project_with_child()
    del project.code.handlers["okButton_clicked"]
    with pytest.raises(ValueError, match="missing handler"):
        validate_project(project)


def test_generators_share_validation_and_do_not_create_output(tmp_path):
    project, panel, button = project_with_child()
    button.id = panel.id
    messages = []
    for generator in (generate_project, generate_c):
        output = tmp_path / generator.__name__
        with pytest.raises(ValueError) as caught:
            generator(project, output)
        messages.append(str(caught.value))
        assert not output.exists()
    assert messages[0] == messages[1]


def test_cli_and_gui_reject_same_invalid_file_without_replacing_document(qtbot, tmp_path, monkeypatch, capsys):
    project, panel, button = project_with_child()
    data = project.to_dict()
    data["pages"][0]["widgets"][1]["id"] = panel.id
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    output = tmp_path / "output"
    with pytest.raises(SystemExit) as caught:
        main(["generate", str(path), "--output", str(output)])
    assert caught.value.code == 1
    assert "pages[0].widgets[1].id" in capsys.readouterr().err
    assert not output.exists()

    window = MainWindow()
    qtbot.addWidget(window)
    original = window.document.project
    monkeypatch.setattr(QMessageBox, "critical", lambda *args: QMessageBox.Ok)
    assert not window.open_project(path)
    assert window.document.project is original


def test_future_schema_version_is_rejected(tmp_path):
    path = tmp_path / "future.json"
    path.write_text(json.dumps({"schemaVersion": 99, "pages": []}), encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported project version"):
        Project.load(path)


def test_wrong_json_types_report_validation_errors_not_type_errors():
    project, _panel, button = project_with_child()
    data = project.to_dict()
    data["currentPageId"] = [1]
    data["pages"][0]["widgets"][1]["name"] = []
    data["pages"][0]["widgets"][1]["parentId"] = [1]
    data["code"]["handlers"]["okButton_clicked"]["widget"] = [1]
    data["code"]["handlers"]["okButton_clicked"]["event"] = []
    with pytest.raises(ValueError) as caught:
        validate_project(data)
    message = str(caught.value)
    assert "currentPageId" in message
    assert "pages[0].widgets[1].parentId" in message
    assert "code.handlers.okButton_clicked.widget" in message
    assert "code.handlers.okButton_clicked.event" in message


@pytest.mark.parametrize("path,value,expected", [
    (("display",), [], "display"),
    (("currentPageId",), {}, "currentPageId"),
    (("pages", 0, "canvasSize"), 42, "pages[0].canvasSize"),
    (("pages", 0, "widgets"), {}, "pages[0].widgets"),
    (("pages", 0, "widgets", 1, "type"), [], "pages[0].widgets[1].type"),
    (("pages", 0, "widgets", 1, "id"), [], "pages[0].widgets[1].id"),
    (("pages", 0, "widgets", 1, "props"), [], "pages[0].widgets[1].props"),
    (("pages", 0, "widgets", 1, "events"), None, "pages[0].widgets[1].events"),
    (("code",), [], "code"),
    (("code", "module"), None, "code.module"),
    (("code", "handlers"), [], "code.handlers"),
    (("code", "handlers", "okButton_clicked"), [], "code.handlers.okButton_clicked"),
    (("code", "handlers", "okButton_clicked", "event"), {}, "code.handlers.okButton_clicked.event"),
    (("code", "handlers", "okButton_clicked", "widget"), [], "code.handlers.okButton_clicked.widget"),
    (("code", "handlers", "okButton_clicked", "body"), None, "code.handlers.okButton_clicked.body"),
])
def test_structural_json_types_are_controlled(path, value, expected):
    project, panel, _button = project_with_child()
    data = project.to_dict()
    target = data
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    if path[-1] == "id":
        data["pages"][0]["widgets"][1]["parentId"] = panel.id
    with pytest.raises(ValueError) as caught:
        validate_project(data)
    assert expected in str(caught.value)


def test_widget_pointing_to_orphan_or_wrong_owner_is_rejected():
    project, _panel, button = project_with_child()
    project.code.handlers["okButton_clicked"].widget = ""
    with pytest.raises(ValueError, match="does not match"):
        validate_project(project)
    project.code.handlers["okButton_clicked"].widget = "container"
    with pytest.raises(ValueError, match="does not match"):
        validate_project(project)


def test_invalid_widget_type_cli_and_gui_are_controlled(qtbot, tmp_path, monkeypatch, capsys):
    project, _panel, _button = project_with_child()
    data = project.to_dict()
    data["pages"][0]["widgets"][1]["type"] = []
    path = tmp_path / "invalid-type.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    output = tmp_path / "output"
    with pytest.raises(SystemExit) as caught:
        main(["generate", str(path), "--output", str(output)])
    assert caught.value.code == 1
    assert "pages[0].widgets[1].type" in capsys.readouterr().err
    assert not output.exists()

    window = MainWindow()
    qtbot.addWidget(window)
    original = window.document.project
    before = original.to_dict()
    monkeypatch.setattr(QMessageBox, "critical", lambda *args: QMessageBox.Ok)
    assert not window.open_project(path)
    assert window.document.project is original
    assert window.document.project.to_dict() == before
    assert not window.document.undo_stack.canUndo()
