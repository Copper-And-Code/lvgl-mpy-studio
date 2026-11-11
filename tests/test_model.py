import json
from pathlib import Path

from hypothesis import given, strategies as st

from lvgl_mpy_studio.core.events import default_event, handler_name
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.core.names import validate_name


def sample_project():
    project = Project()
    button = project.add_widget(project.pages[0], "button", name="ok")
    project.add_widget(project.pages[0], "label", name="counter")
    name, handler = project.ensure_handler("ok")
    handler.body = "global contatore\ncontatore += 1\nui.counter.set_text(str(contatore))\n"
    project.code.module = "contatore = 0\n"
    return project, button, name


def test_names_and_default_event():
    project = Project()
    first = project.add_widget(project.pages[0], "button")
    second = project.add_widget(project.pages[0], "button")
    assert (first.name, second.name) == ("button1", "button2")
    assert default_event(first.type) == "CLICKED"
    assert handler_name(first.name, "CLICKED") == "button1_clicked"
    for invalid in ("1x", "class", "lv_obj", "ui", "with space", "button1"):
        assert validate_name(invalid, project.used_names)


def test_rename_updates_handlers_but_not_user_code():
    project, _button, old_handler = sample_project()
    warnings = project.rename_widget("ok", "confirm")
    assert "confirm_clicked" in project.code.handlers
    assert old_handler not in project.code.handlers
    assert project.find_widget("confirm").events["CLICKED"] == "confirm_clicked"
    assert "ui.counter" in project.code.handlers["confirm_clicked"].body
    assert not warnings


def test_rename_warns_about_old_identifier():
    project, _button, _handler = sample_project()
    project.code.handlers["ok_clicked"].body += "ui.ok.set_width(100)\n"
    assert project.rename_widget("ok", "confirm")


def test_save_load_round_trip(tmp_path):
    project, _button, _handler = sample_project()
    path = tmp_path / "project.json"
    project.save(path)
    assert Project.load(path).to_dict() == project.to_dict()


@given(st.text(max_size=80))
def test_name_validation_never_crashes(text):
    validate_name(text)


def test_all_reference_projects_migrate_idempotently():
    for path in (Path(__file__).parents[1] / "reference" / "corpus").glob("*.json"):
        data = json.loads(path.read_text())["project"]
        migrated = Project.from_dict(data).to_dict()
        assert Project.from_dict(migrated).to_dict() == migrated


def test_v1_migration_preserves_each_widget_handler():
    raw = {
        "projectName": "migration",
        "pages": [
            {"id": "page1", "name": "main", "widgets": [
                {"id": "first", "type": "button", "name": "firstButton", "events": [{"type": "LV_EVENT_CLICKED", "code": 'print("first")'}]},
                {"id": "plain", "type": "label", "name": "statusLabel", "events": []},
            ]},
            {"id": "page2", "name": "secondary", "widgets": [
                {"id": "second", "type": "button", "name": "secondButton", "events": [{"type": "LV_EVENT_CLICKED", "code": 'print("second")'}]},
            ]},
        ],
    }
    project = Project.from_dict(raw)
    first_widget = project.pages[0].widgets[0]
    second_widget = project.pages[1].widgets[0]
    first = project.code.handlers[first_widget.events["CLICKED"]]
    second = project.code.handlers[second_widget.events["CLICKED"]]
    assert (first.widget, first.body) == (first_widget.name, 'print("first")')
    assert (second.widget, second.body) == (second_widget.name, 'print("second")')
    assert Project.from_dict(project.to_dict()).to_dict() == project.to_dict()
