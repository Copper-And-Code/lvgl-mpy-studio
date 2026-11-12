import json
from pathlib import Path

import pytest

from lvgl_mpy_studio.core import modules
from lvgl_mpy_studio.core.model import Project, UserModule
from lvgl_mpy_studio.core.modules import ModuleError, create_module, delete_module, module_files, patch_module, rename_module, set_module_source, validate_module_name
from lvgl_mpy_studio.core.validation import validate_project

ROOT = Path(__file__).parents[1]


def _project_with_module():
    project = Project("Moduli")
    create_module(project, "utils", "def greet():\n    return 'ciao'\n")
    return project


def test_project_without_modules_is_written_exactly_as_before(tmp_path):
    for path in sorted((ROOT / "examples").glob("*/project.json")):
        project = Project.load(path)
        data = project.to_dict()
        if project.modules:  # the weather example has one: it is covered by the round trip below
            assert data["schemaVersion"] == 3
            continue
        assert data["schemaVersion"] == 2 and "modules" not in data
        saved = tmp_path / "saved.json"
        project.save(saved)
        assert Project.load(saved).to_dict() == data, path


def test_modules_round_trip_and_raise_the_schema_to_3(tmp_path):
    project = _project_with_module()
    create_module(project, "levels", "LEVELS = [1, 2]\n")
    path = tmp_path / "project.json"
    project.save(path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw["schemaVersion"] == 3
    assert [module["name"] for module in raw["modules"]] == ["utils", "levels"]
    assert set(raw["modules"][0]) == {"id", "name", "source"}
    loaded = Project.load(path)
    assert [(module.name, module.source, module.id) for module in loaded.modules] == [(module.name, module.source, module.id) for module in project.modules]
    assert "modules" not in loaded.extensions
    assert loaded.to_dict() == project.to_dict()


def test_removing_the_last_module_goes_back_to_schema_2():
    project = _project_with_module()
    delete_module(project, "utils")
    data = project.to_dict()
    assert data["schemaVersion"] == 2 and "modules" not in data


def test_source_is_kept_verbatim():
    source = "\tdef f():\n\t\treturn 'à€'  # tab e unicode\n\n\n"
    project = Project()
    create_module(project, "verbatim", source)
    loaded = Project.from_dict(json.loads(json.dumps(project.to_dict())))
    assert loaded.modules[0].source == source
    assert module_files(loaded) == {"verbatim.py": source}


def test_module_files_normalises_only_line_endings():
    project = Project()
    create_module(project, "crlf", "a = 1\r\nb = 2\rc = 3\n")
    assert module_files(project) == {"crlf.py": "a = 1\nb = 2\nc = 3\n"}


def test_version_2_file_with_modules_is_read(tmp_path):
    """A modules key in a version 2 file, written by hand: it is read and saving moves to version 3."""
    data = Project().to_dict()
    data["modules"] = [{"id": "m1", "name": "utils", "source": "X = 1\n"}]
    path = tmp_path / "project.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    project = Project.load(path)
    assert project.modules[0].name == "utils"
    assert project.to_dict()["schemaVersion"] == 3


def test_unknown_future_version_is_still_refused():
    data = Project().to_dict()
    data["schemaVersion"] = 5
    with pytest.raises(ValueError, match="Unsupported"):
        Project.from_dict(data)
    with pytest.raises(ValueError, match="Unsupported"):
        validate_project(data)


@pytest.mark.parametrize("name", [
    "", "Utils", "utils.py", "../utils", "a/b", "a\\b", "/etc/passwd", "1utils", "util-s", "util s", "x" * 32, "è",
    "ui", "main", "app_events", "app_main", "display_driver", "board_adapter", "board_profile", "manifest", "sourcemap", "boot",
    "lms_buzzer", "lms_probe", "lvgl_idea", "lvgl_mpy_studio_x",
    "time", "json", "random", "asyncio", "machine", "lvgl", "lv", "os", "sys", "gc", "network", "esp32", "rp2", "utime", "ujson",
    "class", "import", "print", "len", "self", "__init__", "__main__",
])
def test_refused_names(name):
    assert validate_module_name(name) is not None


@pytest.mark.parametrize("name", ["utils", "levels", "_private", "game_logic2", "x" * 31])
def test_accepted_names(name):
    assert validate_module_name(name) is None


def test_names_must_be_unique_and_differ_from_handlers():
    project = _project_with_module()
    with pytest.raises(ModuleError, match="already exists"):
        create_module(project, "utils")
    button = project.add_widget(project.pages[0], "button")
    handler, _body = project.ensure_handler(button.name)
    with pytest.raises(ModuleError, match="handler"):
        create_module(project, handler)


def test_rename_reports_imports_left_behind():
    project = _project_with_module()
    project.code.module = "import utils\n"
    button = project.add_widget(project.pages[0], "button")
    handler, body = project.ensure_handler(button.name)
    body.body = "from utils import greet\nui.label.set_text(greet())"
    create_module(project, "other", "import os, utils\n")
    warnings = rename_module(project, "utils", "helpers")
    assert project.modules[0].name == "helpers"
    assert len(warnings) == 3 and all("utils" in warning for warning in warnings)
    assert project.code.module == "import utils\n"  # the code is not rewritten
    assert rename_module(project, "helpers", "helpers") == []
    with pytest.raises(ModuleError):
        rename_module(project, "helpers", "other")
    with pytest.raises(ModuleError):
        rename_module(project, "helpers", "time")
    with pytest.raises(ModuleError, match="no such module"):
        rename_module(project, "missing", "fine")


def test_delete_reports_code_that_still_imports_it():
    project = _project_with_module()
    project.code.module = "import utils\n"
    assert delete_module(project, "utils") == ["(General): still imports utils"]
    assert project.modules == []
    with pytest.raises(ModuleError):
        delete_module(project, "utils")


def test_references_ignore_mentions_that_are_not_imports():
    project = _project_with_module()
    project.code.module = "# utils non serve più\nutils_count = 0\nimport utilsx\n"
    assert modules.module_references(project, "utils") == []


def test_set_and_patch_source():
    project = _project_with_module()
    set_module_source(project, "utils", "A = 1\nA = 1\n")
    with pytest.raises(ModuleError, match="2 times"):
        patch_module(project, "utils", "A = 1", "A = 2")
    assert patch_module(project, "utils", "A = 1", "A = 2", replace_all=True) == 2
    assert project.modules[0].source == "A = 2\nA = 2\n"
    with pytest.raises(ModuleError, match="not found"):
        patch_module(project, "utils", "B", "C")
    with pytest.raises(ModuleError, match="not found"):
        patch_module(project, "utils", "", "C")
    with pytest.raises(ModuleError, match="text"):
        set_module_source(project, "utils", 3)


def test_module_files_refuses_a_name_that_could_leave_the_folder():
    project = Project()
    project.modules.append(UserModule("../../evil", "X = 1\n"))  # as from a file written by hand and not validated
    with pytest.raises(ModuleError):
        module_files(project)


def test_validation_reports_bad_modules():
    data = Project().to_dict()
    page = data["pages"][0]
    data["schemaVersion"] = 3
    data["modules"] = [
        {"id": "m1", "name": "utils", "source": ""},
        {"id": "m2", "name": "utils", "source": ""},
        {"id": "m3", "name": "../x", "source": ""},
        {"id": "m4", "name": "time", "source": ""},
        {"id": "m5", "name": "fine", "source": 3},
        {"id": page["id"], "name": "dup_id", "source": ""},
        "not an object",
    ]
    with pytest.raises(ValueError) as error:
        validate_project(data)
    message = str(error.value)
    for expected in ("modules[1].name: duplicate module", "modules[2].name", "modules[3].name", "modules[4].source", "modules[5].id: duplicate ID", "modules[6]: must be an object"):
        assert expected in message
    data["modules"] = "utils"
    with pytest.raises(ValueError, match="modules: must be a list"):
        validate_project(data)


def test_load_validates_version_3(tmp_path):
    data = _project_with_module().to_dict()
    data["modules"][0]["name"] = "ui"
    path = tmp_path / "project.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="file the IDE generates"):
        Project.load(path)


def test_from_dict_tolerates_malformed_modules_without_validation():
    """from_dict also serves undo and redo: it must not fail on odd entries, module_files refuses them later."""
    data = Project().to_dict()
    data["modules"] = [{"name": "ok", "source": "X = 1\n"}, "rotto", {"source": "Y = 2\n"}]
    project = Project.from_dict(data)
    assert [module.name for module in project.modules] == ["ok", ""]
    assert project.modules[0].id
    data["modules"] = {"not": "a list"}
    assert Project.from_dict(data).modules == []


def test_undo_and_redo_restore_modules(qtbot):
    from lvgl_mpy_studio.ui.document import ProjectDocument

    document = ProjectDocument()
    document.execute("New Module", lambda project: create_module(project, "utils", "A = 1\n"))
    document.execute("Modifica modulo", lambda project: set_module_source(project, "utils", "A = 2\n"))
    assert document.project.modules[0].source == "A = 2\n"
    document.undo_stack.undo()
    assert document.project.modules[0].source == "A = 1\n"
    document.undo_stack.undo()
    assert document.project.modules == []
    document.undo_stack.redo()
    document.undo_stack.redo()
    assert document.project.modules[0].source == "A = 2\n"


def test_core_modules_do_not_import_qt():
    import subprocess
    import sys

    code = "import sys, lvgl_mpy_studio.core.modules, lvgl_mpy_studio.core.model, lvgl_mpy_studio.core.validation; print(any(name.startswith('PySide6') for name in sys.modules))"
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=ROOT, check=True)
    assert result.stdout.strip() == "False"


def test_schema_goes_2_3_2_on_disk_and_back_to_identical_bytes(tmp_path):
    """A project without modules, then with one, then without again: the file is identical again."""
    path = tmp_path / "project.json"
    project = Project("Transizioni")
    project.add_widget(project.pages[0], "button")
    project.save(path)
    original = path.read_bytes()
    assert json.loads(original)["schemaVersion"] == 2
    loaded = Project.load(path)
    create_module(loaded, "utils", "X = 1\n")
    loaded.save(path)
    assert json.loads(path.read_text(encoding="utf-8"))["schemaVersion"] == 3
    reloaded = Project.load(path)
    assert [module.name for module in reloaded.modules] == ["utils"]
    delete_module(reloaded, "utils")
    reloaded.save(path)
    assert path.read_bytes() == original
    assert Project.load(path).modules == []


def test_version_3_file_keeps_widget_events_and_handlers(tmp_path):
    """Widget events are read as in version 2: earlier, version 3 went through the format of version 1."""
    path = tmp_path / "project.json"
    project = Project("Events")
    button = project.add_widget(project.pages[0], "button")
    handler, body = project.ensure_handler(button.name)
    body.body = "import utils\nutils.go()"
    create_module(project, "utils", "def go():\n    pass\n")
    project.save(path)
    assert json.loads(path.read_text(encoding="utf-8"))["schemaVersion"] == 3
    loaded = Project.load(path)
    assert loaded.find_widget(button.name).events == button.events and handler in button.events.values()
    assert loaded.code.handlers[handler].body == "import utils\nutils.go()"
    assert loaded.to_dict() == project.to_dict()


def test_module_actions_read_functions_classes_and_constants_without_running():
    from lvgl_mpy_studio.core.actions import CURSOR, module_actions

    module = UserModule("game", "import ui\nSPEED = 3\n_HIDDEN = 1\nlower = 2\n\ndef start():\n    raise SystemExit\n\nasync def tick(dt):\n    pass\n\nclass Ball:\n    pass\n\ndef _helper():\n    pass\n")
    assert module_actions(module) == [
        ("Import the module", "import game"), ("SPEED", "game.SPEED"), ("start()", "game.start()"),
        ("tick(dt)", f"game.tick({CURSOR})"), ("Ball()", f"game.Ball({CURSOR})"),
    ]
    broken = UserModule("game", "def ok(a):\n    pass\n\ndef rotto(:\n")
    # While typing: the function still incomplete stays in the list too.
    assert module_actions(broken) == [("Import the module", "import game"), ("ok()", f"game.ok({CURSOR})"), ("rotto()", f"game.rotto({CURSOR})")]



def test_module_actions_inside_the_module_itself_have_no_prefix_and_no_import():
    from lvgl_mpy_studio.core.actions import CURSOR, module_actions

    module = UserModule("game", "SPEED = 3\n\ndef start():\n    pass\n\ndef move(dx):\n    pass\n")
    assert module_actions(module, own=True) == [("SPEED", "SPEED"), ("start()", "start()"), ("move(dx)", f"move({CURSOR})")]
