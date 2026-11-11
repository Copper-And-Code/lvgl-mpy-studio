import json

import pytest

from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.device.service import DeviceSession
from lvgl_mpy_studio.ui.document import ProjectDocument

PROFILE = next(item for item in builtin_profiles() if item["id"] == "esp32_4848s040_480")


def app_id(project):
    return DeviceSession()._app_id(project, PROFILE)


def legacy_file(path):
    data = Project().to_dict()
    data.pop("projectId")
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_same_name_gets_different_apps():
    assert Project().projectName == Project().projectName
    assert app_id(Project()) != app_id(Project())


def test_renaming_keeps_the_app():
    project = Project()
    before = app_id(project)
    project.projectName = "Altro nome"
    assert app_id(project) == before


def test_id_survives_save_and_load(tmp_path):
    project = Project()
    path = tmp_path / "progetto.json"
    project.save(path)
    assert Project.load(path).projectId == project.projectId


def test_legacy_file_keeps_its_app_until_saved(tmp_path):
    path = legacy_file(tmp_path / "vecchio.json")
    document = ProjectDocument()
    document.open(path)
    legacy = app_id(document.project)
    assert document.project.projectId == ""
    assert legacy == DeviceSession()._hashed_app_id(document.project.projectName, PROFILE)
    document.save()
    assert document.project.projectId
    assert Project.load(path).projectId == document.project.projectId
    assert app_id(document.project) != legacy


def test_save_keeps_the_id_and_save_as_creates_a_new_one(tmp_path):
    document = ProjectDocument()
    first = document.project.projectId
    document.save(tmp_path / "a.json")
    assert document.project.projectId == first
    document.save(tmp_path / "a.json")
    assert document.project.projectId == first
    document.save(tmp_path / "b.json")
    assert document.project.projectId != first
    assert Project.load(tmp_path / "a.json").projectId == first


def test_undo_does_not_restore_an_old_id(tmp_path):
    document = ProjectDocument()
    document.save(tmp_path / "a.json")
    document.execute("x", lambda project: project.add_widget(project.pages[0], "label", {}, "l1"))
    current = document.project.projectId
    document.save(tmp_path / "b.json")
    assert document.project.projectId != current
    saved = document.project.projectId
    document.undo_stack.undo()
    assert document.project.projectId == saved


def test_examples_have_distinct_ids():
    from pathlib import Path

    root = Path(__file__).parents[1] / "examples"
    ids = [Project.load(root / name).projectId for name in ("tictactoe/project.json", "simon/project.json", "snake/project.json", "breakout/project.json", "demo.json")]
    assert all(ids) and len(set(ids)) == len(ids)


def test_failed_save_as_keeps_the_id(tmp_path, monkeypatch):
    document = ProjectDocument()
    document.save(tmp_path / "a.json")
    identity = document.project.projectId
    def fail(path):
        raise OSError("disco pieno")
    monkeypatch.setattr(document.project, "save", fail)
    with pytest.raises(OSError):
        document.save(tmp_path / "b.json")
    assert document.project.projectId == identity
