"""MCP tools for Python modules and revisions of the project file."""

import json
from pathlib import Path

import pytest

from lvgl_mpy_studio import mcp_server, mcp_tools
from lvgl_mpy_studio.core.model import Project, file_revision
from lvgl_mpy_studio.platform import runtime_path
from helpers import call, payload, error

needs_runtime = pytest.mark.skipif(not runtime_path().exists(), reason="runtime not built")

UTILS = "import helpers\n\n\ndef greeting(name):\n    return helpers.PREFIX + name\n"
HELPERS = "PREFIX = 'ciao '\n"


@pytest.fixture
def enabled(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("APPDATA", str(tmp_path / "config"))
    mcp_server.set_enabled(True)


@pytest.fixture
def project(tmp_path, enabled):
    path = tmp_path / "progetto.json"
    payload(call("create_project", path=str(path), width=240, height=240))
    return str(path)


def conflict(result):
    """A revision conflict: recognisable from the JSON text and from the structured content."""
    assert result.get("isError"), result
    data = json.loads(result["content"][0]["text"])
    assert data == result["structuredContent"] and data["error"] == "revision_conflict"
    return data


def test_create_list_read_and_patch_a_module(project):
    created = payload(call("create_module", project=project, name="helpers", source=HELPERS))
    assert created["module"] == "helpers" and created["file"] == "helpers.py" and created["warnings"] == []
    payload(call("create_module", project=project, name="utils", source=UTILS))
    listed = payload(call("list_modules", project=project))
    assert [(item["name"], item["file"], item["lines"]) for item in listed["modules"]] == [("helpers", "helpers.py", 1), ("utils", "utils.py", 5)]
    code = payload(call("get_code", project=project, module="utils"))
    assert code == {"module": "utils", "file": "utils.py", "source": UTILS, "revision": listed["revision"]}
    assert payload(call("patch_code", project=project, module="helpers", old="'ciao '", new="'salve '"))["replacements"] == 1
    assert payload(call("get_code", project=project, module="helpers"))["source"] == "PREFIX = 'salve '\n"
    assert payload(call("get_code", project=project))["modules"] == ["helpers", "utils"]
    info = payload(call("project_info", project=project))
    assert info["modules"] == [{"name": "helpers", "source": "PREFIX = 'salve '\n"}, {"name": "utils", "source": UTILS}]
    # The code stays in the modules: the shared code and the handlers do not change.
    assert info["module"] == "" and info["handlers"] == {}


def test_module_patch_refuses_ambiguous_missing_or_broken_text(project):
    payload(call("create_module", project=project, name="utils", source="a = 1\na = 1\n"))
    before = Path(project).read_bytes()
    assert "2 times" in error(call("patch_code", project=project, module="utils", old="a = 1", new="a = 2"))
    assert "not found" in error(call("patch_code", project=project, module="utils", old="zzz", new="a"))
    assert "Syntax error in utils.py" in error(call("patch_code", project=project, module="utils", old="a = 1", new="a = (", all=True))
    assert "Unknown module 'nessuno'" in error(call("get_code", project=project, module="nessuno"))
    assert "Unknown module" in error(call("patch_code", project=project, module="nessuno", old="a", new="b"))
    assert "not both" in error(call("get_code", project=project, module="utils", handler="x"))
    assert "not both" in error(call("patch_code", project=project, module="utils", handler="x", old="a", new="b"))
    assert Path(project).read_bytes() == before
    assert payload(call("patch_code", project=project, module="utils", old="a = 1", new="a = 2", all=True))["replacements"] == 2


def test_rename_warns_about_imports_left_behind(project):
    payload(call("create_module", project=project, name="helpers", source=HELPERS))
    payload(call("create_module", project=project, name="utils", source=UTILS))
    payload(call("set_module_code", project=project, code="from helpers import PREFIX\n"))
    payload(call("add_widget", project=project, type="button", name="pulsante"))
    handler = payload(call("set_handler", project=project, widget="pulsante", body="import helpers\nprint(helpers.PREFIX)"))["handler"]
    result = payload(call("rename_module", project=project, name="helpers", new_name="common"))
    assert result["module"] == "common"
    assert sorted(result["references"]) == sorted(["(General): still imports helpers", f"{handler}: still imports helpers", "utils.py: still imports helpers"])
    assert set(result["references"]) <= set(result["warnings"])
    # The code is not rewritten: the agent knows where to act.
    assert payload(call("get_code", project=project, module="utils"))["source"] == UTILS
    assert [item["name"] for item in payload(call("list_modules", project=project))["modules"]] == ["common", "utils"]
    assert "Unknown module" in error(call("rename_module", project=project, name="helpers", new_name="other"))


def test_delete_warns_about_code_that_still_imports_it(project):
    payload(call("create_module", project=project, name="helpers", source=HELPERS))
    payload(call("create_module", project=project, name="utils", source=UTILS))
    result = payload(call("delete_module", project=project, name="helpers"))
    assert result["deleted"] == "helpers" and result["references"] == ["utils.py: still imports helpers"]
    assert [item["name"] for item in payload(call("list_modules", project=project))["modules"]] == ["utils"]
    assert "Unknown module" in error(call("delete_module", project=project, name="helpers"))


@pytest.mark.parametrize("name, text", [
    ("time", "MicroPython"), ("lvgl", "MicroPython"), ("ui", "file the IDE generates"), ("main", "file the IDE generates"),
    ("lvgl_ide_x", "file the IDE generates"), ("class", "reserved"), ("Utils", "lower case"), ("../evil", "lower case"),
    ("a/b", "lower case"), ("", "lower case"),
])
def test_reserved_and_invalid_names_are_refused(project, name, text):
    before = Path(project).read_bytes()
    assert text in error(call("create_module", project=project, name=name))
    assert Path(project).read_bytes() == before


def test_duplicate_names_and_handler_names_are_refused(project):
    payload(call("create_module", project=project, name="utils"))
    payload(call("create_module", project=project, name="other"))
    payload(call("add_widget", project=project, type="button", name="pulsante"))
    handler = payload(call("set_handler", project=project, widget="pulsante", body="pass"))["handler"]
    before = Path(project).read_bytes()
    assert "already exists" in error(call("create_module", project=project, name="utils"))
    assert "handler" in error(call("create_module", project=project, name=handler))
    assert "already exists" in error(call("rename_module", project=project, name="other", new_name="utils"))
    assert "MicroPython" in error(call("rename_module", project=project, name="other", new_name="json"))
    assert "Syntax error in broken.py" in error(call("create_module", project=project, name="broken", source="def ("))
    assert "text" in error(call("create_module", project=project, name="numero", source=3))
    assert Path(project).read_bytes() == before


def test_read_tools_return_the_revision_of_the_file(project):
    revision = file_revision(project)
    assert payload(call("project_info", project=project))["revision"] == revision
    assert payload(call("get_code", project=project))["revision"] == revision
    assert payload(call("list_modules", project=project))["revision"] == revision
    written = payload(call("create_module", project=project, name="utils", expected_revision=revision))["revision"]
    assert written == file_revision(project) != revision
    # The revision returned by a change is valid for the next one, without reading again.
    payload(call("set_module_code", project=project, code="X = 1\n", expected_revision=written))


@pytest.mark.parametrize("tool, arguments", [
    ("create_module", {"name": "utils"}),
    ("set_module_code", {"code": "X = 2\n"}),
    ("add_widget", {"type": "label"}),
    ("add_page", {"name": "Seconda"}),
    ("set_resolution", {"width": 320, "height": 240}),
])
def test_a_stale_revision_changes_nothing(project, tool, arguments):
    stale = payload(call("project_info", project=project))["revision"]
    payload(call("set_module_code", project=project, code="X = 1\n"))  # a change that arrived in the meantime
    before = Path(project).read_bytes()
    data = conflict(call(tool, project=project, expected_revision=stale, **arguments))
    assert data["expected_revision"] == stale and data["current_revision"] == file_revision(project)
    assert data["project"] == project and "Read it again" in data["message"]
    assert Path(project).read_bytes() == before
    # The agent reads again and repeats the change knowingly.
    fresh = payload(call("project_info", project=project))["revision"]
    payload(call(tool, project=project, expected_revision=fresh, **arguments))


def test_a_stale_revision_is_refused_by_every_tool_that_writes(project):
    payload(call("add_widget", project=project, type="button", name="pulsante"))
    payload(call("create_module", project=project, name="utils", source="A = 1\n"))
    stale = "0" * 64
    before = Path(project).read_bytes()
    arguments = {
        "add_page": {"name": "P"}, "rename_page": {"name": "main", "new_name": "home"}, "remove_page": {"name": "main"},
        "add_widget": {"type": "label"}, "add_widgets": {"widgets": [{"type": "label"}]}, "move_widget": {"name": "pulsante", "order": "back"},
        "update_widget": {"name": "pulsante", "props": {"x": 3}}, "remove_widget": {"name": "pulsante"},
        "set_handler": {"widget": "pulsante", "body": "pass"}, "set_module_code": {"code": ""}, "patch_code": {"module": "utils", "old": "A", "new": "B"},
        "set_resolution": {"width": 100, "height": 100}, "adapt_page": {}, "set_board": {"board": "nessuna"},
        "create_module": {"name": "nuovo"}, "rename_module": {"name": "utils", "new_name": "nuovo"}, "delete_module": {"name": "utils"},
        "add_image": {"file": "missing.png"}, "remove_image": {"name": "missing.png"},
        "add_font": {"file": "missing.ttf"}, "remove_font": {"name": "missing.ttf"},
    }
    assert set(arguments) == set(mcp_tools.WRITES_PROJECT)
    for tool, extra in arguments.items():
        assert "expected_revision" in mcp_server.TOOLS[tool][2], tool
        conflict(call(tool, project=project, expected_revision=stale, **extra))
    assert Path(project).read_bytes() == before


def test_expected_revision_must_be_a_string(project):
    assert "revision string" in error(call("set_module_code", project=project, code="", expected_revision=3))


def test_a_save_between_read_and_write_is_not_overwritten(project, monkeypatch):
    """Without expected_revision: the file changes while the tool works on the copy in memory."""
    original = mcp_server.validate_project

    def concurrent_save(project_or_data):
        external = Project.load(project)
        external.code.module = "# salvato dall'IDE\n"
        external.save(project)
        return original(project_or_data)

    monkeypatch.setattr(mcp_server, "validate_project", concurrent_save)
    data = conflict(call("set_module_code", project=project, code="X = 1\n"))
    monkeypatch.setattr(mcp_server, "validate_project", original)
    assert data["current_revision"] == file_revision(project)
    assert Project.load(project).code.module == "# salvato dall'IDE\n"


def test_a_file_deleted_before_the_write_is_not_recreated(project, monkeypatch):
    original = mcp_server.validate_project

    def delete(project_or_data):
        Path(project).unlink()
        return original(project_or_data)

    monkeypatch.setattr(mcp_server, "validate_project", delete)
    data = conflict(call("set_module_code", project=project, code="X = 1\n"))
    assert data["current_revision"] is None and "deleted" in data["message"]
    assert not Path(project).exists()


def test_private_keys_sent_by_a_client_are_ignored(project):
    """The internal keys come from _load, never from the client: it cannot pass off a revision."""
    payload(call("set_module_code", project=project, code="X = 1\n", **{mcp_server.LOADED: "finta", mcp_server.SAVED: "finta"}))
    assert payload(call("get_code", project=project))["module"] == "X = 1\n"


def test_previous_tools_keep_their_arguments_and_answers(project):
    """Earlier signatures and answers stay: new fields are only added."""
    required = {name: spec[3] for name, spec in mcp_server.TOOLS.items()}
    assert required["get_code"] == ["project"] and required["patch_code"] == ["project", "old", "new"]
    assert required["project_info"] == ["project"] and required["set_module_code"] == ["project", "code"]
    assert {"project", "handler"} <= set(mcp_server.TOOLS["get_code"][2]) and {"project", "old", "new", "handler", "all"} <= set(mcp_server.TOOLS["patch_code"][2])
    payload(call("set_module_code", project=project, code="a = 1\n"))
    code = payload(call("get_code", project=project))
    assert code["module"] == "a = 1\n" and code["handlers"] == []
    payload(call("add_widget", project=project, type="button", name="pulsante"))
    handler = payload(call("set_handler", project=project, widget="pulsante", body="print(1)\n"))["handler"]
    assert payload(call("patch_code", project=project, handler=handler, old="print(1)", new="print(2)"))["replacements"] == 1
    body = payload(call("get_code", project=project, handler=handler))
    assert {key: body[key] for key in ("handler", "event", "body")} == {"handler": handler, "event": "CLICKED", "body": "print(2)\n"}
    info = payload(call("project_info", project=project))
    assert {"name", "display", "board", "pages", "module", "handlers", "outOfBounds"} <= set(info)
    # A project without modules stays at version 2, as 0.3 wrote it.
    assert json.loads(Path(project).read_text(encoding="utf-8"))["schemaVersion"] == 2


def test_tool_list_describes_the_new_tools(enabled):
    tools = {tool["name"]: tool for tool in mcp_server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})["result"]["tools"]}
    assert {"list_modules", "create_module", "rename_module", "delete_module"} <= set(tools)
    assert "module" in tools["get_code"]["inputSchema"]["properties"] and "module" in tools["patch_code"]["inputSchema"]["properties"]
    assert "expected_revision" in tools["patch_code"]["inputSchema"]["properties"]
    assert "expected_revision" not in tools["project_info"]["inputSchema"]["properties"]
    assert len(tools) == 49


def test_round_trip_through_the_tools_loses_nothing(project):
    payload(call("add_widget", project=project, type="button", name="pulsante"))
    payload(call("set_handler", project=project, widget="pulsante", body="import utils\nprint(utils.greeting('Ada'))"))
    payload(call("create_module", project=project, name="helpers", source="PREFIX = '\tà€ '  # tab e unicode\n\n\n"))
    payload(call("create_module", project=project, name="utils", source=UTILS))
    raw = json.loads(Path(project).read_text(encoding="utf-8"))
    assert raw["schemaVersion"] == 3 and [module["name"] for module in raw["modules"]] == ["helpers", "utils"]
    loaded = Project.load(project)
    assert loaded.to_dict() == raw
    assert loaded.modules[0].source == "PREFIX = '\tà€ '  # tab e unicode\n\n\n"
    # A change without effects writes the same bytes again.
    before = Path(project).read_bytes()
    payload(call("update_widget", project=project, name="pulsante", props={}))
    assert Path(project).read_bytes() == before
    payload(call("delete_module", project=project, name="helpers"))
    payload(call("delete_module", project=project, name="utils"))
    raw = json.loads(Path(project).read_text(encoding="utf-8"))
    assert raw["schemaVersion"] == 2 and "modules" not in raw


@needs_runtime
def test_an_agent_builds_two_modules_wires_a_handler_and_simulates(project):
    revision = payload(call("project_info", project=project))["revision"]
    revision = payload(call("create_module", project=project, name="helpers", source=HELPERS, expected_revision=revision))["revision"]
    revision = payload(call("create_module", project=project, name="utils", source=UTILS, expected_revision=revision))["revision"]
    revision = payload(call("add_widget", project=project, type="button", name="pulsante", props={"x": 20, "y": 20, "width": 100, "height": 50}, expected_revision=revision))["revision"]
    revision = payload(call("add_widget", project=project, type="label", name="titolo", props={"x": 20, "y": 100, "text": "Prima"}, expected_revision=revision))["revision"]
    payload(call("set_handler", project=project, widget="pulsante", event="CLICKED", body="import utils\nui.titolo.set_text(utils.greeting('Ada'))\nprint('MODULI', utils.greeting('Ada'))", expected_revision=revision))
    result = call("simulate", project=project, steps=[{"action": "wait", "ms": 100}, {"action": "tap", "widget": "pulsante"}, {"action": "wait", "ms": 100}, {"action": "eval", "expr": "ui.titolo.get_text()"}])
    data = json.loads(result["content"][0]["text"])
    assert not result.get("isError") and data["passed"] and not data["traceback"], data
    assert "MODULI ciao Ada" in data["console"]
    assert data["values"][0]["value"] == "ciao Ada"
    # A change to the module reaches the next simulation.
    payload(call("patch_code", project=project, module="helpers", old="'ciao '", new="'salve '"))
    data = json.loads(call("simulate", project=project, steps=[{"action": "tap", "widget": "pulsante"}, {"action": "wait", "ms": 100}, {"action": "eval", "expr": "ui.titolo.get_text()"}])["content"][0]["text"])
    assert data["values"][0]["value"] == "salve Ada", data
