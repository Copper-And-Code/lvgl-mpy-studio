import base64
import io
import json
import time
from pathlib import Path

import pytest

from lvgl_mpy_studio import mcp_server
from lvgl_mpy_studio.cli import main
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.device.service import DeviceError
from lvgl_mpy_studio.platform import runtime_path
from helpers import call, payload

needs_runtime = pytest.mark.skipif(not runtime_path().exists(), reason="runtime not built")


@pytest.fixture
def enabled(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("APPDATA", str(tmp_path / "config"))
    mcp_server.set_enabled(True)


@pytest.fixture
def project(tmp_path, enabled):
    path = tmp_path / "progetto.json"
    assert not call("create_project", path=str(path), width=240, height=240).get("isError")
    return str(path)


def test_off_by_default(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("APPDATA", str(tmp_path))
    assert not mcp_server.is_enabled()


def test_broken_config_counts_as_off(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("APPDATA", str(tmp_path))
    mcp_server.set_enabled(True)
    mcp_server.config_path().write_text("[1, 2", encoding="utf-8")
    assert not mcp_server.is_enabled()


def test_command_refuses_to_start_when_off(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("APPDATA", str(tmp_path))
    with pytest.raises(SystemExit) as stopped:
        main(["--language", "en", "mcp"])
    assert stopped.value.code == 1
    assert "MCP server is off" in capsys.readouterr().err


def test_turning_off_stops_a_running_server(project):
    assert not call("project_info", project=project).get("isError")
    mcp_server.set_enabled(False)
    result = call("project_info", project=project)
    assert result["isError"] and "off" in result["content"][0]["text"]


def test_initialize_and_list(enabled):
    answer = mcp_server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}})
    assert answer["result"]["protocolVersion"] == "2025-06-18"
    assert answer["result"]["capabilities"] == {"tools": {}}
    tools = mcp_server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})["result"]["tools"]
    assert {"render_page", "add_widget", "set_handler"} <= {tool["name"] for tool in tools}
    assert all(tool["inputSchema"]["type"] == "object" for tool in tools)


def test_unknown_protocol_gets_the_latest(enabled):
    answer = mcp_server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "1999"}})
    assert answer["result"]["protocolVersion"] == mcp_server.PROTOCOL_VERSIONS[0]


def test_notifications_get_no_answer():
    assert mcp_server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None


def test_unknown_method_is_an_error():
    assert mcp_server.handle({"jsonrpc": "2.0", "id": 1, "method": "x"})["error"]["code"] == -32601


def test_stream_keeps_stdout_clean_and_survives_bad_json(enabled):
    stdout = io.StringIO()
    mcp_server.serve(io.StringIO('non json\n\n{"jsonrpc":"2.0","id":7,"method":"ping"}\n'), stdout)
    lines = [json.loads(line) for line in stdout.getvalue().splitlines()]
    assert lines[0]["error"]["code"] == -32700
    assert lines[1] == {"jsonrpc": "2.0", "id": 7, "result": {}}


def test_widget_round_trip(project):
    name = payload(call("add_widget", project=project, type="label", name="titolo", props={"x": 10, "text": "Ciao"}))["name"]
    assert name == "titolo"
    payload(call("update_widget", project=project, name="titolo", props={"textColor": "#FF0000"}, new_name="testata"))
    widget = Project.load(project).find_widget("testata")
    assert widget.props["text"] == "Ciao" and widget.props["textColor"] == "#FF0000"
    payload(call("remove_widget", project=project, name="testata"))
    assert Project.load(project).find_widget("testata") is None


@pytest.mark.parametrize("props, text", (({"inesistente": 1}, "no property"), ({"x": "dieci"}, "Invalid value"), ({"textColor": "rosso"}, "Invalid value")))
def test_bad_properties_are_refused_and_change_nothing(project, props, text):
    payload(call("add_widget", project=project, type="label", name="titolo"))
    before = Project.load(project).to_dict()
    result = call("update_widget", project=project, name="titolo", props=props)
    assert result["isError"] and text in result["content"][0]["text"]
    assert Project.load(project).to_dict() == before


def test_unknown_widget_lists_what_exists(project):
    payload(call("add_widget", project=project, type="label", name="titolo"))
    result = call("update_widget", project=project, name="altro", props={})
    assert result["isError"] and "titolo" in result["content"][0]["text"]


def test_handler_is_saved_and_syntax_checked(project):
    payload(call("add_widget", project=project, type="button", name="ok"))
    payload(call("set_handler", project=project, widget="ok", event="CLICKED", body="ui.ok.add_flag(lv.obj.FLAG.HIDDEN)"))
    assert any(handler.widget == "ok" for handler in Project.load(project).code.handlers.values())
    result = call("set_handler", project=project, widget="ok", event="CLICKED", body="if")
    assert result["isError"] and "Syntax error" in result["content"][0]["text"]


def test_module_code_refuses_broken_syntax(project):
    assert call("set_module_code", project=project, code="def (")["isError"]
    assert Project.load(project).code.module == ""


def test_resolution_scales_widgets(project):
    payload(call("add_widget", project=project, type="label", name="titolo", props={"x": 100, "width": 100}))
    assert payload(call("set_resolution", project=project, width=480, height=480))["outOfBounds"] == []
    assert Project.load(project).find_widget("titolo").props["x"] == 200


def test_existing_file_is_not_overwritten(project):
    result = call("create_project", path=project)
    assert result["isError"] and "already exists" in result["content"][0]["text"]


def test_missing_arguments_and_tools_are_reported(project):
    assert "Missing" in call("add_widget", project=project)["content"][0]["text"]
    assert call("non_esiste")["isError"]


def test_suggestions_have_no_cursor_marker(project):
    payload(call("add_widget", project=project, type="label", name="titolo"))
    suggestions = payload(call("suggest_code", project=project, widget="titolo"))
    assert any("set_text" in code for code in suggestions.values())
    assert not any("§" in code for code in suggestions.values())


@needs_runtime
def test_render_returns_a_real_png(project):
    payload(call("add_widget", project=project, type="label", name="titolo", props={"text": "Ciao"}))
    content = call("render_page", project=project)["content"][0]
    assert content["type"] == "image" and content["mimeType"] == "image/png"
    assert base64.b64decode(content["data"]).startswith(b"\x89PNG")


@needs_runtime
def test_render_runs_project_code_unless_design_only(project):
    payload(call("add_widget", project=project, type="label", name="titolo", props={"text": "Prima"}))
    design = call("render_page", project=project, design_only=True)["content"][0]["data"]
    payload(call("set_handler", project=project, widget="main", event="SCREEN_LOADED", body="ui.titolo.set_text('Dopo')"))
    assert call("render_page", project=project)["content"][0]["data"] != design
    assert call("render_page", project=project, design_only=True)["content"][0]["data"] == design


@needs_runtime
def test_broken_code_is_reported_by_render(project):
    payload(call("add_widget", project=project, type="label", name="titolo"))
    payload(call("set_handler", project=project, widget="main", event="SCREEN_LOADED", body="ui.titolo.non_esiste()"))
    result = call("render_page", project=project)
    assert result["isError"] and "non_esiste" in result["content"][0]["text"]


@needs_runtime
def test_measure_reports_flash_and_ram(project):
    payload(call("add_widget", project=project, type="label", name="titolo"))
    result = payload(call("measure", project=project))
    assert result["flashBytes"] > 0 and result["ramBytes"] > 0


def test_generate_c_writes_portable_files(project, tmp_path):
    payload(call("add_widget", project=project, type="label", name="titolo"))
    result = payload(call("generate_code", project=project, target="c", output=str(tmp_path / "c")))
    assert (tmp_path / "c" / "ui.c").exists() and "ui.c" in result["files"]


def test_set_board_applies_profile_and_scales(project):
    payload(call("add_widget", project=project, type="label", name="titolo", props={"x": 120}))
    board = next(item for item in payload(call("list_boards")) if item["id"] == "esp32_4848s040_480")
    payload(call("set_board", project=project, board=board["id"]))
    saved = Project.load(project)
    assert saved.board["id"] == board["id"] and saved.display.width == 480
    assert saved.find_widget("titolo").props["x"] == 240


class FakeDevice:
    def __init__(self):
        self.calls = []

    def list_ports(self):
        return ["/dev/ttyUSB0"]

    def connect(self, port, profile):
        self.calls.append(("connect", port, profile["id"]))

    def upload(self, project, run=False):
        self.calls.append(("upload", run))
        return {"appPath": "/app", "files": ["ui.mpy"], "warnings": [], "output": "ok", "active": run, "sourcemap": {}}

    def evaluate(self, code):
        self.calls.append(("evaluate", code))
        return "42\n"

    def stop(self):
        self.calls.append(("stop",))
        return "LVGL_MPY_STUDIO_STOPPED"

    def live_update(self, script):
        self.calls.append(("live", "exec(" in script))
        return "LVGL_MPY_STUDIO_LIVE_OK"

    def start_console(self, on_output):
        on_output("riga\n")

    def stop_console(self):
        self.calls.append(("stop_console",))

    def install_autostart(self, project):
        self.calls.append(("autostart",))
        return {"appPath": "/app"}

    def remove_autostart(self, project):
        self.calls.append(("autostart_off",))


@pytest.fixture
def device(monkeypatch):
    fake = FakeDevice()
    monkeypatch.setattr(mcp_server, "_session", fake)
    return fake


def test_board_session_goes_through_every_step(project, device):
    payload(call("set_board", project=project, board="esp32_4848s040_480"))
    assert payload(call("device_list_ports")) == ["/dev/ttyUSB0"]
    payload(call("device_connect", port="/dev/ttyUSB0", project=project))
    assert payload(call("device_upload", project=project, run=True))["active"] is True
    assert payload(call("device_exec", code="print(42)"))["output"] == "42\n"
    assert payload(call("device_read_console", seconds=0))["output"] == "riga\n"
    payload(call("device_live_update", project=project))
    payload(call("device_autostart_install", project=project))
    payload(call("device_autostart_remove", project=project))
    payload(call("device_stop"))
    assert [item[0] for item in device.calls] == ["connect", "upload", "evaluate", "stop_console", "live", "autostart", "autostart_off", "stop"]
    assert ("live", True) in device.calls


def test_device_errors_reach_the_agent(project, device, monkeypatch):
    def busy(_code):
        raise DeviceError("device.busy", "porta occupata")
    monkeypatch.setattr(device, "evaluate", busy)
    result = call("device_exec", code="1")
    assert result["isError"] and "device.busy" in result["content"][0]["text"]


def test_device_tools_stay_off_with_the_switch(project, device):
    mcp_server.set_enabled(False)
    assert call("device_exec", code="print(1)")["isError"]
    assert device.calls == []


@needs_runtime
def test_visual_test_round_trip(project):
    assert not payload(call("visual_test", project=project))["passed"]
    assert payload(call("visual_test", project=project, update=True))["passed"]
    assert payload(call("visual_test", project=project))["passed"]


def test_menu_switch_is_off_by_default_and_saves(qtbot, tmp_path, monkeypatch):
    from lvgl_mpy_studio.ui.main_window import MainWindow

    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("APPDATA", str(tmp_path))
    window = MainWindow()
    qtbot.addWidget(window)
    assert not window.mcp_action.isChecked()
    window.mcp_action.trigger()
    assert mcp_server.is_enabled()
    window.mcp_action.trigger()
    assert not mcp_server.is_enabled()


def report(result):
    assert not result.get("isError"), result
    assert result["content"][0]["type"] == "text"
    return json.loads(result["content"][0]["text"]), [item["data"] for item in result["content"][1:]]


def clickable(project, body):
    payload(call("add_widget", project=project, type="button", name="pulsante", props={"x": 20, "y": 20, "width": 100, "height": 50}))
    payload(call("add_widget", project=project, type="label", name="titolo", props={"x": 20, "y": 100, "text": "Prima"}))
    payload(call("set_handler", project=project, widget="pulsante", event="CLICKED", body=body))


@needs_runtime
def test_simulated_tap_runs_the_handler(project):
    clickable(project, "ui.titolo.set_text('Dopo')\nprint('premuto')")
    data, images = report(call("simulate", project=project, steps=[{"action": "wait", "ms": 100}, {"action": "screenshot", "label": "prima"}, {"action": "tap", "widget": "pulsante"}, {"action": "wait", "ms": 100}]))
    assert "premuto" in data["console"] and data["running"] and not data["traceback"]
    assert data["images"] == ["prima", "final"]
    assert images[0] != images[1]


@needs_runtime
def test_simulated_tap_outside_the_button_does_nothing(project):
    clickable(project, "print('premuto')")
    data, _images = report(call("simulate", project=project, steps=[{"action": "tap", "x": 200, "y": 200}]))
    assert "premuto" not in data["console"]


@needs_runtime
def test_simulation_reports_a_handler_error(project):
    clickable(project, "ui.titolo.non_esiste()")
    data, _images = report(call("simulate", project=project, steps=[{"action": "tap", "x": 70, "y": 45}, {"action": "wait", "ms": 100}]))
    assert data["traceback"] and "non_esiste" in data["console"]


@needs_runtime
def test_simulation_plays_a_real_game(enabled):
    example = str(Path(__file__).parent.parent / "examples" / "breakout" / "project.json")
    data, images = report(call("simulate", project=example, steps=[{"action": "wait", "ms": 200}, {"action": "screenshot"}, {"action": "tap", "x": 512, "y": 300}, {"action": "wait", "ms": 2000}]))
    assert data["running"] and not data["traceback"] and data["frames"] > 5
    assert data["tones"] and images[0] != images[1]


@needs_runtime
def test_simulation_drag_reaches_a_slider(project):
    payload(call("add_widget", project=project, type="slider", name="cursore", props={"x": 20, "y": 100, "width": 200, "height": 20}))
    payload(call("set_handler", project=project, widget="cursore", event="VALUE_CHANGED", body="print('valore', ui.cursore.get_value())"))
    data, _images = report(call("simulate", project=project, steps=[{"action": "drag", "x": 30, "y": 110, "x_to": 200, "y_to": 110, "ms": 200}]))
    assert "valore" in data["console"]


def test_simulation_refuses_a_script_that_waits_too_long(project):
    result = call("simulate", project=project, clock="real", steps=[{"action": "wait", "ms": 31000}])
    assert result["isError"] and "30 s" in result["content"][0]["text"]


@needs_runtime
def test_simulation_refuses_an_unknown_step(project):
    result = call("simulate", project=project, steps=[{"action": "balla"}])
    assert result["isError"] and "balla" in result["content"][0]["text"]


def test_a_component_cannot_hold_widgets(project):
    payload(call("add_widget", project=project, type="timer", name="orologio"))
    result = call("add_widget", project=project, type="label", name="titolo", parent="orologio")
    assert result["isError"] and "orologio" in result["content"][0]["text"]
    assert "titolo" not in json.dumps(payload(call("project_info", project=project)))


def test_arguments_of_the_wrong_type_are_a_tool_error(project):
    result = call("simulate", project=project, steps=[{"action": "wait", "ms": "tanto"}])
    assert result["isError"]
    result = call("device_read_console", seconds="tanto")
    assert result["isError"]


def test_generate_code_for_the_board_needs_one(project):
    result = call("generate_code", project=project, target="board")
    assert result["isError"] and "set_board" in result["content"][0]["text"]


def test_generate_code_for_the_board_writes_export_py(project):
    payload(call("set_board", project=project, board="waveshare_rp2350_touch_lcd_4_240"))
    data = payload(call("generate_code", project=project, target="board"))
    assert data["output"].endswith("export_py") and "app_main.py" in data["files"]


def test_generate_code_takes_a_board_without_saving_it(project):
    data = payload(call("generate_code", project=project, target="board", board="waveshare_rp2350_touch_lcd_4_240"))
    assert "app_main.py" in data["files"]
    assert payload(call("project_info", project=project)).get("board") in (None, {})


def test_generate_code_keeps_changed_exports_unless_told(project):
    payload(call("set_board", project=project, board="waveshare_rp2350_touch_lcd_4_240"))
    output = Path(payload(call("generate_code", project=project, target="board"))["output"])
    (output / "ui.py").write_text("# mio\n", encoding="utf-8")
    result = call("generate_code", project=project, target="board")
    assert result["isError"] and "ui.py" in result["content"][0]["text"]
    assert (output / "ui.py").read_text(encoding="utf-8") == "# mio\n"
    payload(call("generate_code", project=project, target="board", overwrite=True))
    assert (output / "ui.py").read_text(encoding="utf-8") != "# mio\n"


def test_patch_code_changes_only_the_named_text(project):
    payload(call("set_module_code", project=project, code="a = 1\nb = 2\n"))
    assert payload(call("patch_code", project=project, old="b = 2", new="b = 3"))["replacements"] == 1
    assert payload(call("get_code", project=project))["module"] == "a = 1\nb = 3\n"


def test_patch_code_refuses_ambiguous_missing_or_broken_text(project):
    payload(call("set_module_code", project=project, code="a = 1\na = 1\n"))
    assert "2 times" in call("patch_code", project=project, old="a = 1", new="a = 2")["content"][0]["text"]
    assert "not found" in call("patch_code", project=project, old="zzz", new="a")["content"][0]["text"]
    assert call("patch_code", project=project, old="", new="a")["isError"]
    assert "Syntax" in call("patch_code", project=project, old="a = 1", new="a = (", all=True)["content"][0]["text"]
    assert payload(call("get_code", project=project))["module"] == "a = 1\na = 1\n"
    assert payload(call("patch_code", project=project, old="a = 1", new="a = 2", all=True))["replacements"] == 2


def test_patch_code_reaches_a_handler(project):
    payload(call("add_widget", project=project, type="button", name="pulsante"))
    handler = payload(call("set_handler", project=project, widget="pulsante", body="print(1)\n"))["handler"]
    payload(call("patch_code", project=project, handler=handler, old="print(1)", new="print(2)"))
    assert payload(call("get_code", project=project, handler=handler))["body"] == "print(2)\n"
    assert handler in payload(call("get_code", project=project))["handlers"]
    assert call("get_code", project=project, handler="nessuno")["isError"]


def test_rename_page_keeps_its_handlers(project):
    payload(call("add_page", project=project, name="seconda"))
    handler = payload(call("set_handler", project=project, widget="seconda", event="SCREEN_LOADED", body="print('qui')\n"))["handler"]
    payload(call("set_module_code", project=project, code="X = ui.PAGE_SECONDA\n"))
    data = payload(call("rename_page", project=project, name="seconda", new_name="terza"))
    assert any("PAGE_SECONDA" in warning for warning in data["warnings"])
    code = payload(call("get_code", project=project))["handlers"]
    assert handler not in code and len(code) == 1
    assert payload(call("get_code", project=project, handler=code[0]))["widget"] == "terza"
    assert call("rename_page", project=project, name="terza", new_name="main")["isError"]
    assert call("rename_page", project=project, name="terza", new_name="")["isError"]


def test_remove_page_takes_its_widgets_and_keeps_the_last_page(project):
    payload(call("add_page", project=project, name="seconda"))
    payload(call("add_widget", project=project, type="label", name="titolo", page="seconda"))
    payload(call("remove_page", project=project, name="seconda"))
    info = payload(call("project_info", project=project))
    assert [page["name"] for page in info["pages"]] == ["main"]
    assert call("remove_page", project=project, name="main")["isError"]


def test_add_widgets_is_all_or_nothing(project):
    data = payload(call("add_widgets", project=project, widgets=[{"type": "panel", "name": "fondo"}, {"type": "label", "name": "titolo", "parent": "fondo"}]))
    assert data["names"] == ["fondo", "titolo"]
    assert call("add_widgets", project=project, widgets=[{"type": "label", "name": "altro"}, {"type": "inesistente"}])["isError"]
    assert "altro" not in json.dumps(payload(call("project_info", project=project)))


def test_move_widget_changes_draw_order(project):
    payload(call("add_widgets", project=project, widgets=[{"type": "panel", "name": "a"}, {"type": "panel", "name": "b"}, {"type": "panel", "name": "c"}]))
    assert payload(call("move_widget", project=project, name="c", order="back"))["order"] == ["c", "a", "b"]
    assert payload(call("move_widget", project=project, name="c", order="front"))["order"] == ["a", "b", "c"]
    assert payload(call("move_widget", project=project, name="c", before="a"))["order"] == ["c", "a", "b"]
    assert payload(call("move_widget", project=project, name="a", order=2))["order"] == ["c", "b", "a"]
    assert call("move_widget", project=project, name="a", order="front", before="b")["isError"]


def test_move_widget_keeps_the_position_on_screen(project):
    payload(call("add_widgets", project=project, widgets=[{"type": "panel", "name": "fondo", "props": {"x": 50, "y": 60}}, {"type": "label", "name": "titolo", "props": {"x": 70, "y": 90}}]))
    data = payload(call("move_widget", project=project, name="titolo", parent="fondo"))
    assert data["parent"] == "fondo" and data["props"] == {"x": 20, "y": 30}
    data = payload(call("move_widget", project=project, name="titolo", parent=None))
    assert data["parent"] is None and data["props"] == {"x": 70, "y": 90}


def test_move_widget_refuses_impossible_parents(project):
    payload(call("add_widgets", project=project, widgets=[{"type": "panel", "name": "fondo"}, {"type": "panel", "name": "dentro", "parent": "fondo"}, {"type": "timer", "name": "orologio"}]))
    assert call("move_widget", project=project, name="fondo", parent="dentro")["isError"]
    assert call("move_widget", project=project, name="dentro", parent="orologio")["isError"]
    payload(call("add_page", project=project, name="seconda"))
    payload(call("add_widget", project=project, type="panel", name="altrove", page="seconda"))
    assert call("move_widget", project=project, name="dentro", parent="altrove")["isError"]


@needs_runtime
def test_moved_widget_really_draws_on_top(project):
    payload(call("add_widgets", project=project, widgets=[{"type": "panel", "name": "sopra", "props": {"x": 0, "y": 0, "width": 240, "height": 240, "bgColor": "#FF0000"}}, {"type": "panel", "name": "sotto", "props": {"x": 0, "y": 0, "width": 240, "height": 240, "bgColor": "#00FF00"}}]))
    before = call("render_page", project=project)["content"][0]["data"]
    payload(call("move_widget", project=project, name="sotto", order="back"))
    assert call("render_page", project=project)["content"][0]["data"] != before


@needs_runtime
def test_repeat_plays_its_steps_and_counts_in_the_time_limit(project):
    clickable(project, "print('colpo')")
    data, images = report(call("simulate", project=project, steps=[{"action": "repeat", "times": 3, "steps": [{"action": "tap", "x": 70, "y": 45}, {"action": "screenshot"}]}]))
    assert data["console"].count("colpo") == 3 and len(images) == 4
    result = call("simulate", project=project, clock="real", steps=[{"action": "repeat", "times": 1000, "steps": [{"action": "wait", "ms": 100}]}])
    assert result["isError"] and "30 s" in result["content"][0]["text"]
    assert call("simulate", project=project, steps=[{"action": "repeat", "times": 10000000, "steps": [{"action": "press", "x": 1, "y": 1}]}])["isError"]


@needs_runtime
def test_simulation_reports_redraw(project):
    clickable(project, "ui.titolo.set_text('Dopo')")
    data, _images = report(call("simulate", project=project, steps=[{"action": "wait", "ms": 100}]))
    assert data["redraw"]["peakScreenShare"] == 1 and data["redraw"]["framesDrawn"] >= 1
    data, _images = report(call("simulate", project=project, steps=[{"action": "wait", "ms": 100}, {"action": "reset_redraw"}, {"action": "tap", "x": 70, "y": 45}, {"action": "wait", "ms": 100}]))
    assert 0 < data["redraw"]["peakScreenShare"] < 1 and data["redraw"]["pixelsPerSecond"] > 0


def test_simulation_refuses_negative_or_endless_steps(project):
    for steps in (
        [{"action": "wait", "ms": -60000}, {"action": "wait", "ms": 60000}],
        [{"action": "repeat", "times": 10 ** 12, "steps": []}],
        [{"action": "repeat", "times": -5, "steps": [{"action": "wait", "ms": 1000}]}, {"action": "wait", "ms": 29000}],
        [{"action": "wait", "ms": True}],
        [{"action": "repeat", "times": 2.5, "steps": []}],
    ):
        assert call("simulate", project=project, steps=steps)["isError"], steps


def test_rename_page_refuses_a_name_with_the_same_constant(project):
    payload(call("add_page", project=project, name="Home-Page"))
    payload(call("add_page", project=project, name="seconda"))
    assert "PAGE_HOME_PAGE" in call("rename_page", project=project, name="seconda", new_name="Home_Page")["content"][0]["text"]


def test_rename_page_leaves_a_widget_with_the_same_name_alone(project):
    payload(call("add_page", project=project, name="gioco"))
    payload(call("add_widget", project=project, type="button", name="Gioco", page="gioco"))
    widget_handler = payload(call("set_handler", project=project, widget="Gioco", body="print(1)\n"))["handler"]
    payload(call("set_handler", project=project, widget="gioco", event="SCREEN_LOADED", body="print(2)\n"))
    payload(call("rename_page", project=project, name="gioco", new_name="partita"))
    assert payload(call("get_code", project=project, handler=widget_handler))["widget"] == "Gioco"
    assert payload(call("validate", project=project))["warnings"] == []


def counter_project(project):
    clickable(project, "conta[0] += 1\nui.titolo.set_text(str(conta[0]))")
    payload(call("set_module_code", project=project, code="conta = [0]\n"))
    payload(call("add_page", project=project, name="seconda"))
    payload(call("add_widget", project=project, type="button", name="vai", page="seconda", props={"x": 20, "y": 150, "width": 100, "height": 50}))
    payload(call("set_handler", project=project, widget="pulsante", event="LONG_PRESSED", body="ui.load_page(ui.PAGE_SECONDA)"))


@needs_runtime
def test_eval_reads_the_app_state(project):
    counter_project(project)
    data, _images = report(call("simulate", project=project, steps=[{"action": "tap", "x": 70, "y": 45}, {"action": "tap", "x": 70, "y": 45}, {"action": "eval", "expr": "conta[0]"}, {"action": "eval", "expr": "page()", "label": "pagina"}, {"action": "eval", "expr": "objects()"}]))
    assert data["passed"] and data["failure"] is None
    assert [item["value"] for item in data["values"]] == [2, "main", 3]  # a button with its label, plus the title
    assert data["values"][1]["label"] == "pagina"
    assert "LVSIM_PROBE" not in data["console"]


@needs_runtime
def test_exec_sets_a_state_and_assert_checks_it(project):
    counter_project(project)
    data, _images = report(call("simulate", project=project, steps=[{"action": "exec", "code": "conta[0] = 41"}, {"action": "tap", "x": 70, "y": 45}, {"action": "assert", "expr": "conta[0] == 42"}, {"action": "assert", "page": "main"}]))
    assert data["passed"], data


@needs_runtime
def test_a_false_assert_stops_the_script(project):
    counter_project(project)
    data, images = report(call("simulate", project=project, steps=[{"action": "assert", "expr": "conta[0] == 5"}, {"action": "screenshot"}]))
    assert not data["passed"] and "conta[0] == 5 is False" in data["failure"]["reason"]
    assert data["images"] == ["final"] and len(images) == 1


@needs_runtime
def test_wait_until_follows_the_page(project):
    counter_project(project)
    steps = [{"action": "exec", "code": "ui.load_page(ui.PAGE_SECONDA)"}, {"action": "wait_until", "page": "seconda", "ms": 2000}, {"action": "eval", "expr": "objects()"}]
    data, _images = report(call("simulate", project=project, steps=steps))
    assert data["passed"] and data["values"][0]["value"] == 2  # the button and its label
    data, _images = report(call("simulate", project=project, steps=[{"action": "wait_until", "page": "seconda", "ms": 300}]))
    assert not data["passed"] and "300 ms" in data["failure"]["reason"]


@needs_runtime
def test_simulation_starting_on_another_page_knows_it(project):
    counter_project(project)
    data, _images = report(call("simulate", project=project, page="seconda", steps=[{"action": "assert", "page": "seconda"}]))
    assert data["passed"], data


@needs_runtime
def test_probe_errors_are_reported_not_raised(project):
    counter_project(project)
    data, _images = report(call("simulate", project=project, steps=[{"action": "eval", "expr": "non_esiste"}, {"action": "exec", "code": "x = ("}]))
    assert data["values"][0]["ok"] is False and "NameError" in data["values"][0]["value"]
    assert data["passed"] is False
    assert "SyntaxError" in data["failure"]["reason"] and data["running"]


@needs_runtime
def test_probe_steps_need_their_text(project):
    for step in ({"action": "eval"}, {"action": "exec", "code": " "}, {"action": "assert"}, {"action": "wait_until", "ms": -1, "page": "main"}):
        assert call("simulate", project=project, steps=[step])["isError"], step
    assert call("simulate", project=project, clock="real", steps=[{"action": "wait_until", "page": "main", "ms": 31000}])["isError"]


@needs_runtime
def test_virtual_clock_repeats_a_run_exactly(enabled):
    example = str(Path(__file__).parent.parent / "examples" / "breakout" / "project.json")
    steps = [{"action": "tap", "x": 512, "y": 300}, {"action": "wait", "ms": 1500}, {"action": "screenshot"}, {"action": "drag", "x": 512, "y": 560, "x_to": 200, "y_to": 560, "ms": 400}, {"action": "wait", "ms": 1500}]
    first = call("simulate", project=example, steps=steps)
    second = call("simulate", project=example, steps=steps)
    assert [item.get("data") for item in first["content"][1:]] == [item.get("data") for item in second["content"][1:]]
    data, images = report(first)
    assert data["clock"] == "virtual" and data["passed"] and images[0] != images[1]


@needs_runtime
def test_virtual_clock_runs_faster_than_real_time(project, enabled):
    clickable(project, "print('ok')")
    started = time.monotonic()
    data, _images = report(call("simulate", project=project, steps=[{"action": "wait", "ms": 120000}]))
    assert data["seconds"] >= 120 and data["passed"]
    assert time.monotonic() - started < 60
    assert call("simulate", project=project, steps=[{"action": "wait", "ms": 601000}])["isError"]


@needs_runtime
def test_game_code_sees_the_simulated_time(project):
    clickable(project, "print('t', time.ticks_ms())")
    payload(call("set_module_code", project=project, code="import time\nstart = time.ticks_ms()\n"))
    data, _images = report(call("simulate", project=project, steps=[{"action": "wait", "ms": 5000}, {"action": "eval", "expr": "time.ticks_diff(time.ticks_ms(), start)", "label": "trascorso"}]))
    assert 4900 <= data["values"][0]["value"] <= 5100


@needs_runtime
def test_seed_makes_random_repeatable(project):
    clickable(project, "pass")
    payload(call("set_module_code", project=project, code="import random\nvalore = random.getrandbits(30)\n"))
    def value(seed):
        data, _images = report(call("simulate", project=project, seed=seed, steps=[{"action": "eval", "expr": "valore"}]))
        return data["values"][0]["value"]
    assert value(7) == value(7)
    assert value(7) != value(8)
    assert call("simulate", project=project, seed="sette", steps=[])["isError"]
    assert call("simulate", project=project, clock="lento", steps=[])["isError"]


@needs_runtime
def test_real_clock_still_plays_touch(project):
    clickable(project, "print('premuto')")
    data, _images = report(call("simulate", project=project, clock="real", steps=[{"action": "tap", "x": 70, "y": 45}, {"action": "wait", "ms": 100}]))
    assert data["clock"] == "real" and "premuto" in data["console"]


@needs_runtime
def test_a_blocked_app_ends_the_script(project):
    clickable(project, "pass")
    started = time.monotonic()
    data, _images = report(call("simulate", project=project, clock="real", steps=[{"action": "exec", "code": "while True:\n    pass"}, {"action": "eval", "expr": "1"}, {"action": "eval", "expr": "2"}]))
    assert not data["passed"] and "did not answer" in data["failure"]["reason"]
    assert data["values"] == [] and time.monotonic() - started < 10


@needs_runtime
def test_a_chatty_app_keeps_the_console_bounded(project):
    clickable(project, "pass")
    payload(call("set_module_code", project=project, code="for _ in range(30000):\n    print('x' * 60)\n"))
    data, _images = report(call("simulate", project=project, steps=[{"action": "eval", "expr": "1 + 1"}]))
    assert data["values"][0]["value"] == 2 and len(data["console"]) <= 4000


@needs_runtime
def test_probe_answers_after_output_without_newline(project):
    clickable(project, "pass")
    payload(call("set_module_code", project=project, code="import sys\nsys.stdout.write('senza a capo')\n"))
    data, _images = report(call("simulate", project=project, steps=[{"action": "eval", "expr": "1 + 2"}]))
    assert data["passed"] and data["values"][0]["value"] == 3 and "senza a capo" in data["console"]


@needs_runtime
def test_callbacks_see_the_same_instant_as_lvgl(project):
    clickable(project, "visti.append(time.ticks_diff(time.ticks_ms(), lv.tick_get()))")
    payload(call("set_module_code", project=project, code="import time\nvisti = []\n"))
    steps = [{"action": "wait", "ms": 200}, {"action": "tap", "x": 70, "y": 45}, {"action": "wait", "ms": 300}, {"action": "tap", "x": 70, "y": 45}, {"action": "eval", "expr": "visti"}]
    data, _images = report(call("simulate", project=project, steps=steps))
    assert data["values"][0]["value"] == [0, 0], data


def test_create_project_takes_a_board(tmp_path, enabled):
    path = tmp_path / "board.json"
    payload(call("create_project", path=str(path), board="esp32_4848s040_480"))
    info = payload(call("project_info", project=str(path)))
    assert info["board"] == "esp32_4848s040_480" and info["display"]["width"] == 480
    assert call("create_project", path=str(tmp_path / "altro.json"), board="nessuna")["isError"]


def test_set_resolution_modes_and_adapt_page(project):
    payload(call("add_widget", project=project, type="panel", name="quadro", props={"x": 70, "y": 70, "width": 100, "height": 100}))
    data = payload(call("set_resolution", project=project, width=480, height=240, mode="keep"))
    assert data["pagesToAdapt"] == ["main"]
    assert payload(call("project_info", project=project))["pages"][0]["widgets"][0]["props"]["width"] == 100
    payload(call("adapt_page", project=project))
    props = payload(call("project_info", project=project))["pages"][0]["widgets"][0]["props"]
    assert props["width"] == props["height"] == 100
    assert call("adapt_page", project=project)["isError"]
    assert call("set_resolution", project=project, width=240, height=240, mode="storto")["isError"]


@needs_runtime
def test_save_scenario_then_visual_test(project):
    clickable(project, "ui.titolo.set_text('Dopo')")
    steps = [{"action": "tap", "widget": "pulsante"}, {"action": "wait", "ms": 200}]
    data = payload(call("save_scenario", project=project, name="tocco", steps=steps))
    assert data["file"].endswith("scenarios.json")
    assert payload(call("visual_test", project=project, update=True))["passed"]
    result = payload(call("visual_test", project=project, scenarios=["tocco"]))
    assert result["passed"] and [item["page"] for item in result["pages"]] == ["tocco: final"]
    assert call("save_scenario", project=project, name="", steps=[])["isError"]
    assert call("save_scenario", project=project, name="lungo", steps=[{"action": "wait", "ms": 700000}])["isError"]


def test_save_scenario_checks_the_steps(project):
    for steps in ([{"action": "balla"}], [{"action": "tap"}], [{"action": "drag", "x": 1, "y": 1}], ["tap"], [{"action": "key"}], {"action": "wait"}):
        assert call("save_scenario", project=project, name="prova", steps=steps)["isError"], steps


@needs_runtime
def test_simulated_dates_repeat(project):
    clickable(project, "pass")
    payload(call("set_module_code", project=project, code="import time\n"))
    data, _images = report(call("simulate", project=project, steps=[{"action": "wait", "ms": 1000}, {"action": "eval", "expr": "time.localtime()[:6]"}]))
    assert data["values"][0]["value"] == [2026, 1, 1, 0, 0, 1]
