from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.ui.document import ProjectDocument


def test_add_undo_redo_and_save_round_trip(qtbot, tmp_path):
    document = ProjectDocument()
    initial = document.project.to_dict()
    document.execute("Aggiungi bottone", lambda project: project.add_widget(project.pages[0], "button"))
    assert document.project.find_widget("button1")
    document.undo_stack.undo()
    assert document.project.to_dict() == initial
    document.undo_stack.redo()
    assert document.project.find_widget("button1")
    path = tmp_path / "saved.json"
    document.save(path)
    assert Project.load(path).to_dict() == document.project.to_dict()


def test_open_real_project_populates_tree_data(qtbot, tmp_path):
    import json

    source = json.loads(open("reference/corpus/widget-01-button.json", encoding="utf-8").read())
    path = tmp_path / "project.json"
    path.write_text(json.dumps(source["project"]), encoding="utf-8")
    document = ProjectDocument()
    document.open(path)
    assert len(document.project.pages) == 1
    assert document.project.widgets


def test_atomic_save_failure_preserves_file_document_and_undo(qtbot, tmp_path, monkeypatch):
    import pytest

    document = ProjectDocument()
    path = tmp_path / "project.json"
    document.save(path)
    original_bytes = path.read_bytes()
    document.execute("Edit", lambda project: setattr(project, "projectName", "non salvato"))
    project = document.project

    def fail_replace(source, target):
        raise OSError("sostituzione non riuscita")

    monkeypatch.setattr("lvgl_mpy_studio.core.model.os.replace", fail_replace)
    with pytest.raises(OSError, match="sostituzione non riuscita"):
        document.save()
    assert path.read_bytes() == original_bytes
    assert document.project is project
    assert document.project.projectName == "non salvato"
    assert document.modified
    assert document.undo_stack.canUndo()
    assert not list(tmp_path.glob(".project.json.*.tmp"))


def test_invalid_open_does_not_replace_current_document(qtbot, tmp_path):
    import json
    import pytest

    document = ProjectDocument()
    path = tmp_path / "project.json"
    document.save(path)
    document.execute("Edit", lambda project: setattr(project, "projectName", "corrente"))
    project = document.project
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{not json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        document.open(invalid)
    assert document.project is project
    assert document.project.projectName == "corrente"
    assert document.path == path
    assert document.modified
    assert document.undo_stack.canUndo()


def _external_save(path, name):
    """As MCP or the CLI would: load the file, change it and save it with the atomic replacement."""
    project = Project.load(path)
    project.projectName = name
    project.save(path)


def test_save_refuses_to_overwrite_an_external_change_on_a_clean_document(qtbot, tmp_path):
    import pytest
    from lvgl_mpy_studio.ui.document import ExternalChangeError

    path = tmp_path / "project.json"
    Project().save(path)
    document = ProjectDocument()
    document.open(path)
    _external_save(path, "da MCP")
    external = path.read_bytes()
    assert document.external_change()
    with pytest.raises(ExternalChangeError):
        document.save()
    assert path.read_bytes() == external
    document.reload()
    assert document.project.projectName == "da MCP"
    assert not document.external_change()
    document.save()
    assert Project.load(path).projectName == "da MCP"


def test_local_changes_survive_an_external_change_until_the_user_chooses(qtbot, tmp_path):
    import pytest
    from lvgl_mpy_studio.ui.document import ExternalChangeError

    path = tmp_path / "project.json"
    Project().save(path)
    document = ProjectDocument()
    document.open(path)
    document.execute("Edit", lambda project: setattr(project, "projectName", "locale"))
    _external_save(path, "da MCP")
    with pytest.raises(ExternalChangeError):
        document.save()
    assert document.project.projectName == "locale"
    assert document.modified and document.undo_stack.canUndo()
    assert Project.load(path).projectName == "da MCP"
    document.save(overwrite_external=True)  # keeps the local one, after confirming
    assert Project.load(path).projectName == "locale"
    assert not document.modified and not document.external_change()


def test_save_a_copy_leaves_the_external_version_untouched(qtbot, tmp_path):
    path = tmp_path / "project.json"
    Project().save(path)
    document = ProjectDocument()
    document.open(path)
    document.execute("Edit", lambda project: setattr(project, "projectName", "locale"))
    _external_save(path, "da MCP")
    external = path.read_bytes()
    copy = tmp_path / "project-copia.json"
    document.save(copy)
    assert path.read_bytes() == external
    assert Project.load(copy).projectName == "locale"
    assert document.path == copy and not document.external_change()


def test_reload_of_a_malformed_file_keeps_the_local_state(qtbot, tmp_path):
    import json
    import pytest
    from lvgl_mpy_studio.ui.document import ExternalChangeError

    path = tmp_path / "project.json"
    Project().save(path)
    document = ProjectDocument()
    document.open(path)
    document.execute("Edit", lambda project: setattr(project, "projectName", "locale"))
    project = document.project
    path.write_text("{rotto", encoding="utf-8")
    with pytest.raises(ExternalChangeError):
        document.save()
    with pytest.raises(json.JSONDecodeError):
        document.reload()
    assert document.project is project and document.modified
    assert path.read_text(encoding="utf-8") == "{rotto"


def test_deleted_or_recreated_file_is_a_conflict(qtbot, tmp_path):
    import os
    import pytest
    from lvgl_mpy_studio.ui.document import ExternalChangeError

    path = tmp_path / "project.json"
    Project().save(path)
    document = ProjectDocument()
    document.open(path)
    path.unlink()
    assert document.external_change() == "deleted"
    with pytest.raises(ExternalChangeError) as error:
        document.save()  # whoever removed it must not see it come back on its own
    assert error.value.deleted and not path.exists()
    document.save(overwrite_external=True)  # "Recreate the file"
    assert path.is_file() and document.external_change() is None
    other = tmp_path / "other.json"
    replacement = Project()
    replacement.projectName = "sostituito"
    replacement.save(other)
    os.replace(other, path)  # deleted and created again with other content
    assert document.external_change() == "changed"
    with pytest.raises(ExternalChangeError) as error:
        document.save()
    assert not error.value.deleted


def test_same_bytes_written_again_are_not_a_conflict(qtbot, tmp_path):
    path = tmp_path / "project.json"
    Project().save(path)
    document = ProjectDocument()
    document.open(path)
    content = path.read_bytes()
    path.unlink()
    path.write_bytes(content)  # same content, new file: no change to lose
    assert not document.external_change()


def test_repeated_saves_without_external_changes(qtbot, tmp_path):
    path = tmp_path / "project.json"
    document = ProjectDocument()
    document.save(path)  # Save As of a new document
    for index in range(3):
        document.execute("Edit", lambda project, index=index: setattr(project, "projectName", f"n{index}"))
        document.save()
        document.save()
    assert Project.load(path).projectName == "n2"
    document.undo_stack.undo()
    document.save()
    assert Project.load(path).projectName == "n1"


def test_undo_history_is_cleared_after_reload(qtbot, tmp_path):
    path = tmp_path / "project.json"
    Project().save(path)
    document = ProjectDocument()
    document.open(path)
    document.execute("Edit", lambda project: setattr(project, "projectName", "locale"))
    _external_save(path, "da MCP")
    document.reload()
    assert not document.undo_stack.canUndo() and not document.undo_stack.canRedo()
    assert not document.modified
    document.execute("Edit", lambda project: setattr(project, "projectName", "dopo"))
    document.undo_stack.undo()
    assert document.project.projectName == "da MCP"


def test_save_returns_the_revision_of_the_written_bytes(tmp_path):
    from lvgl_mpy_studio.core.model import file_revision

    path = tmp_path / "project.json"
    revision = Project().save(path)
    assert revision == file_revision(path)
    project, loaded = Project.load_with_revision(path)
    assert loaded == revision
    assert file_revision(tmp_path / "missing.json") is None
