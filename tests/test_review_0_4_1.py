"""Defects found by the review of 0.4.0: each test fails on that release."""

import json

import pytest

from lvgl_mpy_studio import mcp_server
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.gen.board_gen import generate_board
from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.platform import runtime_path

needs_runtime = pytest.mark.skipif(not runtime_path().exists(), reason="runtime not built")


@pytest.fixture
def enabled(monkeypatch):
    monkeypatch.setattr(mcp_server, "is_enabled", lambda: True)


def call(tool, **arguments):
    return mcp_server._call_tool({"name": tool, "arguments": arguments})


def payload(result):
    assert not result.get("isError"), result["content"][0]["text"]
    return json.loads(result["content"][0]["text"])


def nested():
    project = Project()
    project.set_display_size(320, 240)
    page = project.pages[0]
    box = project.add_widget(page, "panel", {"x": 100, "y": 80, "width": 150, "height": 100}, "box")
    inner = project.add_widget(page, "panel", {"x": 5, "y": 5, "width": 100, "height": 60}, "inner")
    inner.parentId = box.id
    label = project.add_widget(page, "label", {"x": 10, "y": 10, "width": 60, "height": 20}, "lbl")
    label.parentId = inner.id
    project.add_widget(page, "label", {"x": 5, "y": 5, "width": 60, "height": 20}, "free")
    return project


def test_removing_a_container_removes_what_it_contains():
    project = nested()
    project.ensure_handler("lbl", "CLICKED")
    project.remove_widget("box")
    assert [widget.name for widget in project.widgets] == ["free"]
    assert project.code.handlers["lbl_clicked"].widget == ""  # the code is kept, as an orphan


def test_outside_uses_the_position_on_screen():
    project = nested()
    wide = project.add_widget(project.pages[0], "button", {"x": 120, "y": 10, "width": 100, "height": 30}, "wide")
    wide.parentId = project.find_widget("box").id  # 100 + 120 + 100 = 320: still inside
    assert project.widgets_outside() == []
    wide.props["x"] = 121
    assert project.widgets_outside() == ["wide"]
    project.add_widget(project.pages[0], "timer", name="tick")
    assert project.widgets_outside() == ["wide"]  # a component is not on the screen


def test_a_page_handler_defaults_to_screen_loaded_and_rejects_other_events():
    project = Project()
    name, _handler = project.ensure_handler("main")
    assert name == "main_screen_loaded"
    with pytest.raises(ValueError):
        project.ensure_handler("main", "CLICKED")
    project.add_widget(project.pages[0], "timer", name="tick")
    with pytest.raises(ValueError):
        project.ensure_handler("tick", "CLICKED")


def test_simulator_and_board_start_from_the_same_page(tmp_path):
    project = Project()
    project.pages.append(project.new_page("second"))
    project.currentPageId = project.pages[1].id
    generate_project(project, tmp_path / "py")
    assert "lv.screen_load(ui.screens[1])" in (tmp_path / "py" / "main.py").read_text()
    profile = builtin_profiles()[0]
    project.set_display_size(profile["logicalWidth"], profile["logicalHeight"])
    generate_board(project, profile, tmp_path / "board")
    assert "lv.screen_load(ui.screens[1])" in (tmp_path / "board" / "app_main.py").read_text()


def test_generated_ui_is_unchanged_unless_everything_is_exposed(tmp_path):
    project = nested()
    generate_project(project, tmp_path / "a")
    generate_project(project, tmp_path / "b", expose_all=True)
    assert "global" not in (tmp_path / "a" / "ui.py").read_text()
    assert "free" in (tmp_path / "b" / "ui.py").read_text().split("global", 1)[1].splitlines()[0]


@needs_runtime
def test_simulate_reads_a_widget_the_code_never_names(tmp_path, enabled):
    path = tmp_path / "p.json"
    project = nested()
    project.find_widget("free").props["text"] = "zero"
    project.save(path)
    result = call("simulate", project=str(path), steps=[{"action": "eval", "expr": "ui.free.get_text()"}])
    report = json.loads(result["content"][0]["text"])
    assert report["values"] == [{"label": "ui.free.get_text()", "ok": True, "value": "zero"}]


def test_mcp_remove_reports_everything_removed(tmp_path, enabled):
    path = tmp_path / "p.json"
    nested().save(path)
    assert payload(call("remove_widget", project=str(path), name="box"))["removed"] == ["box", "inner", "lbl"]
    assert payload(call("set_handler", project=str(path), widget="main", body="pass"))["handler"] == "main_screen_loaded"


def test_copy_and_cut_take_the_children_of_a_container(qtbot):
    from lvgl_mpy_studio.ui.designer.scene import DesignerView
    from lvgl_mpy_studio.ui.document import ProjectDocument

    document = ProjectDocument(nested())
    view = DesignerView(document)
    qtbot.addWidget(view)
    scene = view.designer_scene
    box = document.project.find_widget("box")
    scene.widget_items[box.id].setSelected(True)
    scene.duplicate_selected()
    copies = [widget for widget in document.project.widgets if widget.name not in ("box", "inner", "lbl", "free")]
    assert [widget.type for widget in copies] == ["panel", "panel", "label"]
    assert (copies[0].props["x"], copies[0].props["y"]) == (112, 92)  # only the container moves
    assert copies[1].parentId == copies[0].id and (copies[1].props["x"], copies[1].props["y"]) == (5, 5)
    assert copies[2].parentId == copies[1].id and (copies[2].props["x"], copies[2].props["y"]) == (10, 10)
    document.undo_stack.undo()
    scene.clearSelection()
    scene.widget_items[document.project.find_widget("box").id].setSelected(True)
    scene.copy_selected(cut=True)
    assert [widget.name for widget in document.project.widgets] == ["free"]
    document.undo_stack.undo()
    assert len(document.project.widgets) == 4


def test_the_default_language_is_english(monkeypatch, capsys):
    from lvgl_mpy_studio import cli
    from lvgl_mpy_studio.core import i18n

    assert i18n.DEFAULT_LANGUAGE == "en"
    assert i18n.set_language("xx") == "en"
    with pytest.raises(SystemExit):
        cli.main(["--help"])
    assert "Visual IDE" in capsys.readouterr().out
    assert i18n.set_language("it") == "it" and i18n.tr("Cancel") == "Annulla" and i18n.tr("Annulla") == "Annulla"
    assert i18n.set_language("en") == "en" and i18n.tr("Annulla") == "Cancel"  # a text shown in Italian goes back


def test_mcp_answers_in_english_and_survives_an_unexpected_error(tmp_path, enabled, monkeypatch):
    import io
    from lvgl_mpy_studio.core import i18n

    path = tmp_path / "p.json"
    nested().save(path)
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "update_widget", "arguments": {"project": str(path), "name": "free", "new_name": "class"}}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "set_resolution", "arguments": {"project": str(path), "width": 0, "height": 10}}},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "move_widget", "arguments": {"project": str(path), "name": "free", "order": []}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/list"},
    ]
    output = io.StringIO()
    i18n.set_language("it")  # whatever the IDE uses, agents read English
    mcp_server.serve(io.StringIO("".join(json.dumps(item) + "\n" for item in requests)), output)
    answers = [json.loads(line) for line in output.getvalue().splitlines()]
    assert [answer["id"] for answer in answers] == [1, 2, 3, 4]
    texts = [answer["result"]["content"][0]["text"] for answer in answers[:3]]
    assert texts[0] == "The name 'class' is reserved"
    assert texts[1] == "Invalid display size"
    assert answers[2]["result"]["isError"] and texts[2].startswith("TypeError")


def test_a_malformed_v1_project_says_what_is_wrong(tmp_path):
    path = tmp_path / "v1.json"
    path.write_text(json.dumps({"projectName": "x", "pages": ["oops"]}))
    with pytest.raises(ValueError, match=r"pages\[0\]"):
        Project.load(path)


def test_port_errors_are_not_read_from_the_output_of_the_app():
    from lvgl_mpy_studio.device.service import _port_error

    trace = 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nOSError: resource not found, busy\n'
    assert _port_error(trace) == "device.command"
    assert _port_error("mpremote: failed to access /dev/ttyACM0 (it may be in use by another program)") == "device.absent"
    assert _port_error("could not open port: [Errno 16] Device or resource busy") == "device.busy"
    assert _port_error("[Errno 13] Permission denied: '/dev/ttyUSB0'") == "device.permissions"


def test_an_unexpected_error_does_not_leave_the_session_transferring(monkeypatch):
    from lvgl_mpy_studio.device import service

    profile = builtin_profiles()[0]
    project = Project()
    project.board = profile
    project.set_display_size(profile["logicalWidth"], profile["logicalHeight"])
    session = service.DeviceSession(runner=lambda command, timeout: "")
    session.port, session.profile = "/dev/null", profile
    monkeypatch.setattr(session, "_info", lambda profile=None: {"compatible": True, "mpy": None})
    monkeypatch.setattr(session, "_reset", lambda: (_ for _ in ()).throw(OSError("unplugged")))
    with pytest.raises(OSError):
        session.upload(project)
    assert session.state == "error"


def test_a_profile_without_minimum_versions_accepts_any(monkeypatch):
    from lvgl_mpy_studio.device import service

    profile = builtin_profiles()[0]
    profile["firmware"] = {"modules": profile["firmware"]["modules"]}
    reply = {"implementation": "micropython", "implementationVersion": [1, 20, 0], "lvglVersion": "9.1.0", "modules": {name: True for name in profile["firmware"]["modules"]}, "width": profile["logicalWidth"], "height": profile["logicalHeight"], "touch": True, "apis": {}}
    session = service.DeviceSession(runner=lambda command, timeout: "LVGL_MPY_STUDIO_INFO=" + json.dumps(reply))
    session.port, session.profile = "/dev/null", profile
    info = session.info()
    assert "microPython" not in info["missingRequirements"] and "lvgl" not in info["missingRequirements"]


def test_a_broken_profile_file_keeps_the_builtin_profiles_and_is_not_overwritten(tmp_path):
    from lvgl_mpy_studio.core.boards import ProfileStore

    path = tmp_path / "board-profiles.json"
    path.write_text("{not json")
    store = ProfileStore.tolerant(path)
    assert store.load_error and len(store.profiles()) == len(builtin_profiles())
    with pytest.raises(OSError):
        store.save()
    assert path.read_text() == "{not json"


def test_a_line_that_looks_like_a_probe_answer_is_plain_output():
    from lvgl_mpy_studio.sim.session import PROBE_LINE

    assert PROBE_LINE.search(b"\x1bLVSIM_PROBE 3 ok not-json")  # the reader must cope with it


def test_the_old_configuration_folder_is_copied_once(tmp_path, monkeypatch):
    from lvgl_mpy_studio import platform

    old = tmp_path / "lvgl-ide"
    (old / "autostart-backups").mkdir(parents=True)
    (old / "board-profiles.json").write_text("{}")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    current = platform.config_dir()
    assert current == tmp_path / "lvgl-mpy-studio" and (current / "board-profiles.json").read_text() == "{}"
    assert (old / "board-profiles.json").exists()  # an older IDE still finds its files
    (current / "board-profiles.json").write_text("new")
    assert (platform.config_dir() / "board-profiles.json").read_text() == "new"


def test_settings_saved_under_the_old_name_are_kept(qtbot):
    from PySide6.QtCore import QSettings
    from lvgl_mpy_studio.ui.main_window import MainWindow

    QSettings("CopperAndCode", "LVGL MPY Studio").clear()
    old = QSettings("CopperAndCode", "LVGL IDE")
    old.setValue("recentFiles", ["/tmp/old.json"])
    old.sync()
    try:
        window = MainWindow()
        qtbot.addWidget(window)
        assert window.settings.value("recentFiles", [], list) == ["/tmp/old.json"]
        assert window.windowTitle().endswith("LVGL MPY Studio")
    finally:
        old.clear()
        QSettings("CopperAndCode", "LVGL MPY Studio").clear()


def font_project(board=None):
    project = Project()
    if board:
        project.board = board
        project.set_display_size(board["logicalWidth"], board["logicalHeight"])
    project.add_widget(project.pages[0], "label", {"x": 10, "y": 10, "width": 200, "height": 50, "text": "Big", "fontSize": 32}, "big")
    return project


def test_text_uses_the_fonts_the_target_has(tmp_path):
    from lvgl_mpy_studio.core.boards import profile_fonts

    profiles = {profile["id"]: profile for profile in builtin_profiles()}
    waveshare, stm32 = profiles["waveshare_rp2350_touch_lcd_4_240"], profiles["stm32h7_core_v1_3_1024x600"]
    waveshare.pop("fonts")  # as a profile written by hand, with no list
    assert profile_fonts(None) == [14, 16, 24, 32, 40]  # the simulator runtime
    assert profile_fonts(waveshare) == [14, 16, 24]      # a profile that lists none
    assert profile_fonts(stm32) == [14, 16, 24, 32, 40]  # read from the board
    generate_project(font_project(), tmp_path / "sim")
    assert "lv.font_montserrat_32" in (tmp_path / "sim" / "ui.py").read_text()
    generate_project(font_project(waveshare), tmp_path / "small")
    assert "lv.font_montserrat_24" in (tmp_path / "small" / "ui.py").read_text()
    generate_board(font_project(stm32), stm32, tmp_path / "stm32")
    assert "lv.font_montserrat_32" in (tmp_path / "stm32" / "ui.py").read_text()
    generate_board(font_project(waveshare), waveshare, tmp_path / "found", fonts=[14, 32])
    assert "lv.font_montserrat_32" in (tmp_path / "found" / "ui.py").read_text()


def test_a_profile_with_a_bad_font_list_is_refused():
    from lvgl_mpy_studio.core.boards import profile_diagnostics

    profile = builtin_profiles()[0]
    profile["fonts"] = [14, "big"]
    assert [item["code"] for item in profile_diagnostics(profile)] == ["profile.fonts"]


def test_resizing_picks_a_font_the_target_has():
    profiles = {profile["id"]: profile for profile in builtin_profiles()}
    profiles["waveshare_rp2350_touch_lcd_4_240"].pop("fonts")  # a board taken to have 14, 16 and 24
    small = font_project(profiles["waveshare_rp2350_touch_lcd_4_240"])
    small.find_widget("big").props["fontSize"] = 16
    small.resize(1024, 600, "stretch")
    assert small.find_widget("big").props["fontSize"] == 24  # the largest this board has
    free = font_project()
    free.find_widget("big").props["fontSize"] = 16
    free.resize(1600, 960, "stretch")
    assert free.find_widget("big").props["fontSize"] == 32
