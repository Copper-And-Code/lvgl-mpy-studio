import json

import pytest
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QDialog, QMessageBox

from lvgl_mpy_studio import __version__
from lvgl_mpy_studio.cli import main
from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.device.service import DeviceError
from lvgl_mpy_studio.gen.components import BUZZER_MODULE
from lvgl_mpy_studio.gen.gen_c import generate_c
from lvgl_mpy_studio.ui.device_panel import DeviceConsole, UploadProgress
from lvgl_mpy_studio.ui.main_window import MainWindow
from lvgl_mpy_studio.ui.project_settings import ProjectSettingsDialog
from lvgl_mpy_studio.ui.run_target import SIMULATOR_MICROPYTHON, board_target


def board_window(qtbot, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    project = Project("gui-board")
    project.set_display_size(240, 240)
    project.board = builtin_profiles()[0]
    project.runTarget = {"kind": "board", "language": "micropython"}
    project.add_widget(project.pages[0], "button")
    path = tmp_path / "board.json"
    project.save(path)
    assert window.open_project(path)
    assert window.run_target == board_target(project.board["id"])
    window.selected_port = "/dev/fake"
    return window


def wait_worker(qtbot, window):
    qtbot.waitUntil(lambda: window._worker is None, timeout=3000)


def test_run_selector_lists_simulators_and_catalog_boards(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.run_selector.rebuild()
    targets = [action.data() for action in window.run_selector.target_actions()]
    assert targets[0] == SIMULATOR_MICROPYTHON
    assert {target.profile_id for target in targets[1:]} == {profile["id"] for profile in window.profile_store.profiles()}
    assert window.menuBar().cornerWidget() is None


def fake_connect(window, calls=None):
    def connect(port, profile):
        if calls is not None:
            calls.append(port)
        window.device.port = port
        window.device.profile = profile
        return {"compatible": True, "width": 240, "height": 240}
    return connect


def test_selecting_board_sets_profile_and_resolution_with_undo(qtbot, tmp_path, monkeypatch):
    monkeypatch.setattr("lvgl_mpy_studio.ui.resolution.ResizeDialog.exec", lambda self: QDialog.Accepted)
    window = MainWindow()
    qtbot.addWidget(window)
    path = tmp_path / "project.json"
    Project("plain").save(path)
    assert window.open_project(path)
    profile = next(item for item in window.profile_store.profiles() if item["logicalWidth"] == 240)
    assert window.select_run_target(board_target(profile["id"]))
    assert window.document.project.board["id"] == profile["id"]
    assert (window.document.project.display.width, window.document.project.display.height) == (240, 240)
    window.document.undo_stack.undo()
    assert window.document.project.board is None
    assert window.run_target == SIMULATOR_MICROPYTHON
    window.document.undo_stack.setClean()


def test_run_connects_automatically_with_single_port(qtbot, tmp_path, monkeypatch):
    window = board_window(qtbot, tmp_path)
    window.selected_port = ""
    connects, uploads = [], []
    monkeypatch.setattr(window, "_remember_port", lambda port: setattr(window, "selected_port", port))
    monkeypatch.setattr(window.device, "list_ports", lambda: [{"port": "/dev/only", "id": "1", "usb": "1:1", "description": "x"}])
    monkeypatch.setattr(window.device, "connect", fake_connect(window, connects))
    monkeypatch.setattr(window.device, "upload", lambda project, output, run, progress, cancel: uploads.append(run) or {"output": "", "active": run, "warnings": []})
    assert window.run_action.isEnabled()
    window.run_action.trigger()
    qtbot.waitUntil(lambda: bool(uploads) and window._worker is None, timeout=3000)
    assert connects == ["/dev/only"]
    assert uploads == [True]
    assert "/dev/only" in window.device_status.text()
    window.document.undo_stack.setClean()


def test_run_asks_port_when_several_and_stops_on_cancel(qtbot, tmp_path, monkeypatch):
    window = board_window(qtbot, tmp_path)
    window.selected_port = ""
    connects = []
    ports = [{"port": name, "id": "1", "usb": "1:1", "description": "x"} for name in ("/dev/a", "/dev/b")]
    monkeypatch.setattr(window.device, "list_ports", lambda: ports)
    monkeypatch.setattr(window.device, "connect", fake_connect(window, connects))
    monkeypatch.setattr("lvgl_mpy_studio.ui.device_panel.SelectDeviceDialog.exec", lambda self: QDialog.Rejected)
    window.run_action.trigger()
    wait_worker(qtbot, window)
    assert connects == []
    assert window._device_next is None
    assert window.device.port is None
    window.document.undo_stack.setClean()


def test_failed_connection_does_not_run_following_step(qtbot, tmp_path, monkeypatch):
    window = board_window(qtbot, tmp_path)
    uploads = []
    monkeypatch.setattr(window.device, "connect", lambda port, profile: (_ for _ in ()).throw(DeviceError("device.absent", "sparita")))
    monkeypatch.setattr(window.device, "upload", lambda *args, **kwargs: uploads.append(True))
    window.run_action.trigger()
    wait_worker(qtbot, window)
    assert uploads == []
    assert window._device_next is None
    assert "[device.absent] sparita" in window.device_console.output.toPlainText()
    window.document.undo_stack.setClean()


def test_incompatible_board_does_not_upload(qtbot, tmp_path, monkeypatch):
    window = board_window(qtbot, tmp_path)
    uploads = []
    def connect(port, profile):
        window.device.port = port
        window.device.profile = profile
        return {"compatible": False}
    monkeypatch.setattr(window.device, "connect", connect)
    monkeypatch.setattr(window.device, "upload", lambda *args, **kwargs: uploads.append(True))
    window.run_action.trigger()
    wait_worker(qtbot, window)
    assert uploads == []
    window.document.undo_stack.setClean()


def test_opening_project_with_other_profile_closes_session(qtbot, tmp_path, monkeypatch):
    window = board_window(qtbot, tmp_path)
    monkeypatch.setattr(window.device, "connect", fake_connect(window))
    window.connect_action.trigger()
    wait_worker(qtbot, window)
    assert window.device.port == "/dev/fake"
    other = Project("other-board")
    other.board = builtin_profiles()[1]
    other.runTarget = {"kind": "board", "language": "micropython"}
    other.set_display_size(other.board["logicalWidth"], other.board["logicalHeight"])
    path = tmp_path / "other.json"
    other.save(path)
    assert window.open_project(path)
    assert window.device.port is None
    assert window.run_target == board_target(other.board["id"])


def test_run_target_travels_with_project_file(qtbot, tmp_path, monkeypatch):
    monkeypatch.setattr("lvgl_mpy_studio.ui.resolution.ResizeDialog.exec", lambda self: QDialog.Accepted)
    window = MainWindow()
    qtbot.addWidget(window)
    path = tmp_path / "portable.json"
    Project("portable").save(path)
    assert window.open_project(path)
    profile = window.profile_store.profiles()[0]
    assert window.select_run_target(board_target(profile["id"]))
    assert window.save_project()
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["runTarget"] == {"kind": "board", "language": "micropython"}
    assert saved["board"]["id"] == profile["id"]
    other = MainWindow()
    qtbot.addWidget(other)
    assert other.open_project(path)
    assert other.run_target == board_target(profile["id"])


def test_default_target_leaves_project_file_unchanged():
    assert "runTarget" not in Project("plain").to_dict()


@pytest.mark.parametrize("value", ["board", {"kind": "cloud", "language": "c"}, {"kind": "board"}])
def test_unreadable_run_target_is_ignored(value):
    data = Project("bad").to_dict()
    data["runTarget"] = value
    assert Project.from_dict(data).runTarget is None
    assert "runTarget" not in Project.from_dict(data).to_dict()


def isolated_settings(window, tmp_path):
    window.settings = QSettings(str(tmp_path / "settings.ini"), QSettings.IniFormat)


def test_new_project_uses_saved_default_board(qtbot, tmp_path):
    window = board_window(qtbot, tmp_path)
    isolated_settings(window, tmp_path)
    expected = window.document.project.board["id"]
    window.save_new_project_defaults()
    window.new_project()
    project = window.document.project
    assert project.board["id"] == expected
    assert "origin" not in project.board
    assert (project.display.width, project.display.height) == (240, 240)
    assert window.run_target == board_target(expected)
    assert not window.document.modified
    window.clear_new_project_defaults()
    window.new_project()
    assert window.document.project.board is None
    assert window.run_target == SIMULATOR_MICROPYTHON


def test_default_with_deleted_profile_falls_back_to_simulator(qtbot, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    isolated_settings(window, tmp_path)
    window.settings.setValue("defaults/newProject", json.dumps({"board": "sparito", "runTarget": {"kind": "board", "language": "micropython"}, "width": 320, "height": 240}))
    window.new_project()
    assert window.document.project.board is None
    assert window.document.project.display.width == 320
    assert window.run_target == SIMULATOR_MICROPYTHON


def test_corrupt_default_is_ignored(qtbot, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    isolated_settings(window, tmp_path)
    window.settings.setValue("defaults/newProject", "{non json")
    window.new_project()
    assert window.document.project.board is None


def test_opening_project_without_profile_returns_to_simulator(qtbot, tmp_path):
    window = board_window(qtbot, tmp_path)
    path = tmp_path / "plain.json"
    Project("plain").save(path)
    assert window.open_project(path)
    assert window.run_target == SIMULATOR_MICROPYTHON


def test_changing_port_while_connected_closes_old_session(qtbot, tmp_path, monkeypatch):
    window = board_window(qtbot, tmp_path)
    monkeypatch.setattr(window.device, "connect", fake_connect(window))
    window.connect_action.trigger()
    wait_worker(qtbot, window)
    remembered = []
    monkeypatch.setattr(window, "_remember_port", remembered.append)
    monkeypatch.setattr("lvgl_mpy_studio.ui.device_panel.SelectDeviceDialog.exec", lambda self: QDialog.Accepted)
    monkeypatch.setattr("lvgl_mpy_studio.ui.device_panel.SelectDeviceDialog.selected_port", lambda self: "/dev/new")
    window._choose_port([])
    assert remembered == ["/dev/new"]
    assert window.device.port is None
    window.document.undo_stack.setClean()


def test_project_settings_locks_resolution_to_profile(qtbot):
    project = Project("locked")
    project.board = builtin_profiles()[0]
    dialog = ProjectSettingsDialog(project, [])
    qtbot.addWidget(dialog)
    assert not dialog.width.isEnabled()
    assert dialog.values()[:2] == (project.board["logicalWidth"], project.board["logicalHeight"])
    dialog.profile.setCurrentIndex(0)
    dialog._profile_selected()
    assert dialog.width.isEnabled()
    dialog.reject()


def test_upload_progress_follows_bytes_and_estimates_inside_a_file(qtbot):
    now = [100.0]
    dialog = UploadProgress(clock=lambda: now[0], rate=5_000)
    qtbot.addWidget(dialog)
    assert dialog.bar.maximum() == 0 and dialog.shown_bytes() == 0  # busy until the first report
    now[0] += 4  # preparation: it does not count as writing
    dialog.report(0, 100_000, "app_main.py", 20_000)
    now[0] += 1  # nothing measured yet: the speed of the last upload moves the bar
    dialog._refresh()
    assert dialog.shown_bytes() == 5_000 and "about 19 s left" in dialog.detail_label.text()
    now[0] += 1
    dialog.report(20_000, 100_000, "ui.mpy", 80_000)  # 10 kB/s so far
    assert dialog.bar.value() == 200 and "ui.mpy" in dialog.file_label.text()
    assert dialog.rate == 10_000
    assert "20 of 98 kB" in dialog.detail_label.text() and "about 8 s left" in dialog.detail_label.text()
    now[0] += 3  # nothing reported: the estimate moves the bar
    dialog._refresh()
    assert dialog.shown_bytes() == 50_000 and dialog.bar.value() == 500
    now[0] += 60  # a slow file: the bar waits just before its end
    dialog._refresh()
    assert dialog.shown_bytes() == 96_000
    dialog.report(100_000, 100_000, "", 0)
    assert dialog.bar.value() == 1000 and "left" not in dialog.detail_label.text()
    assert UploadProgress(clock=lambda: now[0]).rate == UploadProgress.FIRST_RATE

    asked = []
    dialog.cancelRequested.connect(lambda: asked.append(True))
    dialog.reject()
    dialog.reject()
    assert asked == [True] and not dialog.cancel_button.isEnabled()
    assert "Cancelling" in dialog.detail_label.text()
    dialog.finish()


def test_slow_upload_shows_its_progress_and_can_be_cancelled(qtbot, tmp_path, monkeypatch):
    import threading

    window = board_window(qtbot, tmp_path)
    window.show()
    monkeypatch.setattr(UploadProgress, "DELAY_MS", 0)
    window.settings.remove("device/uploadRate")
    release = threading.Event()

    def upload(project, output, run, progress, cancel):
        progress(2048, 8192, "ui.mpy", 4096)
        release.wait(3)
        if cancel.is_set():
            raise DeviceError("device.cancelled")
        return {"output": "", "active": False, "warnings": []}

    monkeypatch.setattr(window.device, "upload", upload)
    window.device.port = "/dev/fake"
    window._update_device_actions()
    assert window.upload_board()
    dialog = window._upload_progress
    qtbot.waitUntil(lambda: dialog.isVisible() and dialog.bar.maximum() == 1000, timeout=3000)
    assert "ui.mpy" in dialog.file_label.text()
    dialog.cancel_button.click()
    assert window._device_cancel.is_set()
    release.set()
    wait_worker(qtbot, window)
    assert not window.settings.contains(window._upload_rate_key)  # a cancelled upload teaches no speed
    assert window._upload_progress is None  # closed and deleted with the operation
    assert not [widget for widget in window.findChildren(UploadProgress) if widget.isVisible()]


def test_a_failed_start_still_shows_the_warnings(qtbot, tmp_path, monkeypatch):
    window = board_window(qtbot, tmp_path)

    def upload(project, output, run, progress, cancel):
        error = DeviceError("device.command", "MemoryError: memory allocation failed")
        error.warnings = ["The fonts of the project need about 143 kB of RAM"]
        raise error

    monkeypatch.setattr(window.device, "upload", upload)
    window.device.port = "/dev/fake"
    window._update_device_actions()
    assert window.upload_board(run=True)
    wait_worker(qtbot, window)
    assert "need about 143 kB" in window.output.toPlainText()
    assert window.errors.topLevelItemCount() == 1


def test_board_actions_upload_console_stop_and_failure(qtbot, tmp_path, monkeypatch):
    window = board_window(qtbot, tmp_path)
    calls = []

    def upload(project, output, run, progress, cancel):
        calls.append((project.projectName, output, run))
        progress(2048, 8192, "ui.mpy", 4096)
        return {"output": "pronto ü\n", "active": run, "warnings": []}

    monkeypatch.setattr(window.device, "upload", upload)
    window.device.port = "/dev/fake"
    window._update_device_actions()
    assert window.upload_run_action.isEnabled()
    window.upload_run_action.trigger()
    wait_worker(qtbot, window)
    assert calls[0][0] == "gui-board"
    assert calls[0][2] is True
    assert window.device_app_active
    assert "pronto ü" in window.device_console.output.toPlainText()
    assert window.stop_action.isEnabled()

    monkeypatch.setattr(window.device, "evaluate", lambda source, cancel=None: "risposta: " + source)
    window.device_console.input.setText("1 + 1")
    window.device_console.submit()
    wait_worker(qtbot, window)
    assert ">>> 1 + 1" in window.device_console.output.toPlainText()
    assert "risposta: 1 + 1" in window.device_console.output.toPlainText()

    monkeypatch.setattr(window.device, "stop", lambda: "LVGL_MPY_STUDIO_STOPPED\n")
    window.stop_action.trigger()
    wait_worker(qtbot, window)
    assert not window.device_app_active

    monkeypatch.setattr(window.device, "evaluate", lambda source, cancel=None: (_ for _ in ()).throw(DeviceError("device.timeout", "board lenta")))
    window.device_console.input.setText("2 + 2")
    window.device_console.submit()
    wait_worker(qtbot, window)
    assert "[device.timeout] board lenta" in window.device_console.output.toPlainText()
    window.document.undo_stack.setClean()


def test_simulator_keeps_board_session_and_disables_upload(qtbot, tmp_path):
    window = board_window(qtbot, tmp_path)
    window.device.port = "/dev/fake"
    assert window.select_run_target(SIMULATOR_MICROPYTHON)
    assert window.run_action.isEnabled()
    assert not window.upload_action.isEnabled()
    assert window.upload_board() is False
    assert window.device.port == "/dev/fake"
    window.document.undo_stack.setClean()


def test_project_saved_with_c_target_opens_on_simulator(qtbot, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    project = Project("vecchio")
    project.runTarget = {"kind": "simulator", "language": "c"}
    path = tmp_path / "vecchio.json"
    project.save(path)
    assert window.open_project(path)
    assert window.run_target == SIMULATOR_MICROPYTHON


def export_window(qtbot, monkeypatch, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    project = Project("esporta")
    project.add_widget(project.pages[0], "button", name="button1")
    project.ensure_handler("button1")[1].body = "print(1)\n"
    path = tmp_path / "progetto.json"
    project.save(path)
    assert window.open_project(path)
    shown = []
    monkeypatch.setattr("PySide6.QtWidgets.QMessageBox.exec", lambda box: shown.append(box.informativeText()))
    return window, shown


def test_export_c_goes_next_to_the_project_without_asking(qtbot, tmp_path, monkeypatch):
    window, shown = export_window(qtbot, monkeypatch, tmp_path)
    def fail(*args):
        raise AssertionError("the dialog is not needed if the project is saved")
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getExistingDirectory", fail)
    window.export_c_action.trigger()
    assert sorted(path.name for path in (tmp_path / "export_c").iterdir()) == ["ui.c", "ui.h", "ui_events.c", "ui_events.h"]
    assert "ui_events.c" in shown[0]


def test_export_c_keeps_handlers_written_by_hand(qtbot, tmp_path, monkeypatch):
    window, _shown = export_window(qtbot, monkeypatch, tmp_path)
    window.export_c()
    events = tmp_path / "export_c" / "ui_events.c"
    source = events.read_text().replace("LV_UNUSED(e);", "lv_label_set_text(ui_lab, \"mio\");")
    events.write_text(source)
    window.document.execute("x", lambda project: project.add_widget(project.pages[0], "label", name="lab"))
    window.export_c()
    assert "lv_label_set_text(ui_lab, \"mio\");" in events.read_text()
    assert "ui_lab" in (tmp_path / "export_c" / "ui.c").read_text()
    window.document.undo_stack.setClean()


def test_export_c_of_unsaved_project_asks_for_a_folder(qtbot, tmp_path, monkeypatch):
    window = MainWindow()
    qtbot.addWidget(window)
    monkeypatch.setattr("PySide6.QtWidgets.QMessageBox.exec", lambda box: None)
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getExistingDirectory", lambda *args: str(tmp_path))
    assert window.export_c() is True
    assert (tmp_path / "ui.c").exists()
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getExistingDirectory", lambda *args: "")
    assert window.export_c() is False


def test_portable_export_needs_no_development_sources(tmp_path):
    project = Project("portabile")
    project.add_widget(project.pages[0], "button", name="button1")
    result = generate_c(project, tmp_path / "out", root_dir=tmp_path / "missing", portable=True)
    assert result["files"] == ["ui.c", "ui.h", "ui_events.c", "ui_events.h"]
    for name in result["files"]:
        assert "/opt/" not in (tmp_path / "out" / name).read_text()


def test_connect_and_disconnect_actions(qtbot, tmp_path, monkeypatch):
    window = board_window(qtbot, tmp_path)

    def connect(port, profile):
        window.device.port = port
        window.device.profile = profile
        return {"compatible": True, "width": 240, "height": 240}

    monkeypatch.setattr(window.device, "connect", connect)
    assert window.connect_action.isEnabled()
    window.connect_action.trigger()
    wait_worker(qtbot, window)
    assert window.device.port == "/dev/fake"
    assert window.upload_action.isEnabled()
    assert window.connect_action.text() == "Disconnect"
    assert window.connect_disconnect() is True
    assert window.device.port is None
    assert window.connect_action.text() == "Connect"
    assert window.upload_action.isEnabled()
    window.document.undo_stack.setClean()


def test_about_shows_ide_firmware_versions_and_credits(qtbot, tmp_path, monkeypatch):
    window = board_window(qtbot, tmp_path)
    messages = []
    monkeypatch.setattr(QMessageBox, "about", lambda *args: messages.append(args))

    window.about_action.trigger()
    assert "Board not connected" in messages[-1][2]

    window.device.port = "/dev/fake"
    window._device_info = {"implementationVersion": [1, 29, 0, ""], "lvglVersion": "9.5.0"}
    window.about_action.trigger()
    text = messages[-1][2]
    assert __version__ == "0.6.0"
    assert f"IDE version:</b> {__version__}" in text
    assert "<b>MicroPython:</b> 1.29.0<br>" in text
    assert "<b>LVGL:</b> 9.5.0" in text
    assert "Nunzio Raciti (in vibe coding)" in text
    assert "GPL-3.0-or-later" in text
    assert "MIT" in text
    window.document.undo_stack.setClean()


def test_device_console_preserves_utf8_and_ignores_empty(qtbot):
    console = DeviceConsole()
    qtbot.addWidget(console)
    received = []
    console.commandRequested.connect(received.append)
    console.set_ready(True)
    console.input.setText("   ")
    console.submit()
    assert received == []
    console.append("tracce à\n")
    assert console.output.toPlainText() == "tracce à\n"


def test_cli_upload_uses_embedded_project_profile(tmp_path, monkeypatch, capsys):
    current = Project("cli-board")
    current.set_display_size(240, 240)
    current.board = builtin_profiles()[0]
    path = tmp_path / "project.json"
    current.save(path)
    calls = []

    class Session:
        def connect(self, port, profile):
            calls.append(("connect", port, profile["id"]))

        def upload(self, project, output_dir=None):
            calls.append(("upload", project.projectName, output_dir))
            return {"appPath": "/lms_apps/app_test", "files": ["app_main.py"], "warnings": []}

    monkeypatch.setattr("lvgl_mpy_studio.device.service.DeviceSession", Session)
    output = tmp_path / "build"
    assert main(["--language", "en", "device", "upload", str(path), "--port", "/dev/fake", "--output", str(output)]) == 0
    assert calls == [("connect", "/dev/fake", current.board["id"]), ("upload", "cli-board", output)]
    assert json.loads(capsys.readouterr().out)["appPath"] == "/lms_apps/app_test"



def test_destination_change_preserves_board_session_and_dedicated_stop(qtbot, tmp_path, monkeypatch):
    window = board_window(qtbot, tmp_path)
    window.device.port = "/dev/fake"
    window.device_app_active = True
    calls = []
    monkeypatch.setattr(window.device, "stop", lambda: calls.append("board") or "stopped\n")
    monkeypatch.setattr(window.sim_panel, "stop", lambda: calls.append("simulator"))
    assert window.select_run_target(SIMULATOR_MICROPYTHON)
    assert window.device_app_active
    assert calls == []
    assert window.board_stop_action.isEnabled()
    assert not window.stop_action.isEnabled()
    sim_state = {"running": True}
    monkeypatch.setattr(type(window.sim_panel), "running", property(lambda _self: sim_state["running"]))
    window._update_device_actions()
    assert window.stop_action.isEnabled()
    window.stop_action.trigger()
    assert calls == ["simulator"]
    sim_state["running"] = False
    window.board_stop_action.trigger()
    wait_worker(qtbot, window)
    assert calls == ["simulator", "board"]
    assert not window.device_app_active
    window.document.undo_stack.setClean()


def test_delayed_device_traceback_uses_deployed_sourcemap(qtbot, tmp_path):
    window = board_window(qtbot, tmp_path)
    window._device_sourcemap = {"version": 1, "file": "app_events.py", "entries": [{"line": 8, "handler": "button1_CLICKED", "sourceLine": 3}]}
    window._device_output('Traceback (most recent call last):\n  File "/lms_apps/app/app_ev')
    window._device_output('ents.py", line 8, in handler\n')
    assert window.errors.topLevelItemCount() == 1
    error = window.errors.topLevelItem(0).data(0, 256)
    assert error["handler"] == "button1_CLICKED"
    assert error["sourceLine"] == 3
    window._device_output('File "/lms_apps/app/app_events.py", line 8, in handler\n')
    assert window.errors.topLevelItemCount() == 1
    window.document.undo_stack.setClean()


def board_export_window(qtbot, monkeypatch, tmp_path, buzzer=False):
    window, shown = export_window(qtbot, monkeypatch, tmp_path)
    profile = next(item for item in builtin_profiles() if item["id"] == "esp32_4848s040_480")
    window.document.project.scale_to(profile["logicalWidth"], profile["logicalHeight"])
    window.document.project.board = dict(profile)
    if buzzer:
        window.document.project.add_widget(window.document.project.pages[0], "buzzer", name="bip")
    return window, shown


def test_export_python_writes_board_files_next_to_the_project(qtbot, tmp_path, monkeypatch):
    window, shown = board_export_window(qtbot, monkeypatch, tmp_path)
    assert window.export_python() is True
    output = tmp_path / "export_py"
    assert {"app_main.py", "app_events.py", "ui.py", "manifest.json"} <= {path.name for path in output.iterdir()}
    assert "print(1)" in (output / "app_events.py").read_text(encoding="utf-8")
    assert not list(output.glob("*.mpy"))
    assert "app_main.py" in shown[0]
    window.document.undo_stack.setClean()


def test_export_python_without_a_board_asks_only_for_compatible_ones(qtbot, tmp_path, monkeypatch):
    window, _shown = export_window(qtbot, monkeypatch, tmp_path)
    window.document.project.scale_to(480, 480)
    asked = []
    def choose(_parent, _title, _label, names, _current, _editable):
        asked.extend(names)
        return names[0], True
    monkeypatch.setattr("PySide6.QtWidgets.QInputDialog.getItem", choose)
    assert window.export_python() is True
    offered = " ".join(asked)
    assert asked and all(item["id"] in offered for item in builtin_profiles() if (item["logicalWidth"], item["logicalHeight"]) == (480, 480))
    assert not any(item["id"] in offered for item in builtin_profiles() if (item["logicalWidth"], item["logicalHeight"]) != (480, 480))
    assert window.document.project.board is None
    window.document.undo_stack.setClean()


def test_export_python_cancelled_board_choice_writes_nothing(qtbot, tmp_path, monkeypatch):
    window, _shown = export_window(qtbot, monkeypatch, tmp_path)
    window.document.project.scale_to(480, 480)
    monkeypatch.setattr("PySide6.QtWidgets.QInputDialog.getItem", lambda *args: ("", False))
    assert window.export_python() is False
    assert not (tmp_path / "export_py").exists()
    window.document.undo_stack.setClean()


def test_export_python_asks_before_overwriting_a_changed_file(qtbot, tmp_path, monkeypatch):
    window, _shown = board_export_window(qtbot, monkeypatch, tmp_path)
    assert window.export_python() is True
    events = tmp_path / "export_py" / "app_events.py"
    events.write_text("# mio\n", encoding="utf-8")
    warned = []
    answers = [QMessageBox.Cancel, QMessageBox.Yes]
    def answer(_parent, _title, text, *_args):
        warned.append(text)
        return answers.pop(0)
    monkeypatch.setattr("PySide6.QtWidgets.QMessageBox.warning", answer)
    assert window.export_python() is False
    assert events.read_text(encoding="utf-8") == "# mio\n"
    assert "app_events.py" in warned[0]
    assert window.export_python() is True
    assert "print(1)" in events.read_text(encoding="utf-8")
    window.document.undo_stack.setClean()


def test_export_python_does_not_ask_when_nothing_changed(qtbot, tmp_path, monkeypatch):
    window, _shown = board_export_window(qtbot, monkeypatch, tmp_path)
    assert window.export_python() is True
    def fail(*args):
        raise AssertionError("no file was changed")
    monkeypatch.setattr("PySide6.QtWidgets.QMessageBox.warning", fail)
    assert window.export_python() is True
    window.document.undo_stack.setClean()


def test_export_python_removes_files_it_no_longer_needs(qtbot, tmp_path, monkeypatch):
    window, _shown = board_export_window(qtbot, monkeypatch, tmp_path, buzzer=True)
    assert window.export_python() is True
    output = tmp_path / "export_py"
    assert (output / f"{BUZZER_MODULE}.py").exists()
    window.document.project.pages[0].widgets.pop()
    (output / "appunti.txt").write_text("mio", encoding="utf-8")
    assert window.export_python() is True
    assert not (output / f"{BUZZER_MODULE}.py").exists()
    assert (output / "appunti.txt").exists()
    window.document.undo_stack.setClean()


def test_export_python_with_wrong_resolution_reports_it(qtbot, tmp_path, monkeypatch):
    window, _shown = board_export_window(qtbot, monkeypatch, tmp_path)
    window.document.project.scale_to(320, 240)
    assert window.export_python() is False
    assert "resolution" in window.errors.topLevelItem(0).text(2).lower()
    assert not (tmp_path / "export_py").exists()
    window.document.undo_stack.setClean()


def test_cli_exports_for_the_board(tmp_path, capsys):
    project = Project("esporta")
    profile = next(item for item in builtin_profiles() if item["id"] == "esp32_4848s040_480")
    project.scale_to(profile["logicalWidth"], profile["logicalHeight"])
    project.board = dict(profile)
    path = tmp_path / "progetto.json"
    project.save(path)
    assert main(["generate", str(path), "--target", "board"]) == 0
    assert (tmp_path / "export_py" / "app_main.py").exists()


def test_cli_board_export_needs_a_board(tmp_path, capsys):
    path = tmp_path / "progetto.json"
    Project("esporta").save(path)
    with pytest.raises(SystemExit) as caught:
        main(["generate", str(path), "--target", "board"])
    assert caught.value.code == 1
    assert "board profile" in capsys.readouterr().err


def test_export_python_tells_boards_with_the_same_name_apart(qtbot, tmp_path, monkeypatch):
    window, _shown = export_window(qtbot, monkeypatch, tmp_path)
    window.document.project.scale_to(480, 480)
    twins = [dict(item, name="Stessa board") for item in builtin_profiles() if (item["logicalWidth"], item["logicalHeight"]) == (480, 480)][:1]
    twins = [twins[0], dict(twins[0], id="gemella")]
    monkeypatch.setattr(window.profile_store, "profiles", lambda: twins)
    monkeypatch.setattr("PySide6.QtWidgets.QInputDialog.getItem", lambda _parent, _title, _label, names, _current, _editable: (names[1], True))
    assert window.export_python() is True
    assert json.loads((tmp_path / "export_py" / "board_profile.json").read_text(encoding="utf-8"))["id"] == "gemella"
    window.document.undo_stack.setClean()


def test_export_python_shows_where_the_syntax_error_is(qtbot, tmp_path, monkeypatch):
    window, _shown = board_export_window(qtbot, monkeypatch, tmp_path)
    window.document.project.code.handlers[next(iter(window.document.project.code.handlers))].body = "def rotto(\n"
    assert window.export_python() is False
    assert window.errors.topLevelItem(0).text(0) == "app_events.py"
    window.document.undo_stack.setClean()


def cli_board_project(tmp_path):
    project = Project("esporta")
    profile = next(item for item in builtin_profiles() if item["id"] == "esp32_4848s040_480")
    project.scale_to(profile["logicalWidth"], profile["logicalHeight"])
    path = tmp_path / "progetto.json"
    project.save(path)
    return path, profile


def test_cli_exports_for_a_named_board_without_saving_it(tmp_path):
    path, profile = cli_board_project(tmp_path)
    assert main(["generate", str(path), "--target", "board", "--board-profile", profile["id"]]) == 0
    assert (tmp_path / "export_py" / "app_main.py").exists()
    assert Project.load(path).board is None


def test_cli_keeps_changed_exports_without_force(tmp_path, capsys):
    path, profile = cli_board_project(tmp_path)
    command = ["generate", str(path), "--target", "board", "--board-profile", profile["id"]]
    assert main(command) == 0
    events = tmp_path / "export_py" / "app_events.py"
    events.write_text("# mio\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        main(command)
    assert "app_events.py" in capsys.readouterr().err and events.read_text(encoding="utf-8") == "# mio\n"
    assert main([*command, "--force"]) == 0
    assert events.read_text(encoding="utf-8") != "# mio\n"


def test_renaming_a_page_keeps_its_handlers(qtbot, tmp_path, monkeypatch):
    window, _shown = export_window(qtbot, monkeypatch, tmp_path)
    project = window.document.project
    project.ensure_handler(project.pages[0].name, "SCREEN_LOADED")[1].body = "print(1)\n"
    old_name = project.pages[0].name
    monkeypatch.setattr("PySide6.QtWidgets.QInputDialog.getText", lambda *args, **kwargs: ("Nuova", True))
    window.rename_page()
    project = window.document.project
    assert project.pages[0].name == "Nuova"
    assert [handler.widget for handler in project.code.handlers.values() if handler.event == "SCREEN_LOADED"] == ["Nuova"]
    assert not any(handler.widget == old_name for handler in project.code.handlers.values())
    window.document.undo_stack.setClean()


def test_renaming_a_page_refuses_a_name_in_use(qtbot, tmp_path, monkeypatch):
    window, _shown = export_window(qtbot, monkeypatch, tmp_path)
    window.document.execute("pagina", lambda project: project.pages.append(project.new_page("Altra")))
    monkeypatch.setattr("PySide6.QtWidgets.QInputDialog.getText", lambda *args, **kwargs: ("Altra", True))
    window.rename_page()
    assert [page.name for page in window.document.project.pages].count("Altra") == 1
    assert window.errors.topLevelItemCount() == 1
    window.document.undo_stack.setClean()


def resolution_window(qtbot, tmp_path, monkeypatch, mode="adapt", accept=True):
    asked = []
    def answer(dialog):
        asked.append(dialog)
        dialog.options[mode].setChecked(True)
        return QDialog.Accepted if accept else QDialog.Rejected
    monkeypatch.setattr("lvgl_mpy_studio.ui.resolution.ResizeDialog.exec", answer)
    window = MainWindow()
    qtbot.addWidget(window)
    window.settings.remove("resolution/mode")
    project = Project("risoluzione")
    project.set_display_size(480, 480)
    project.add_widget(project.pages[0], "panel", {"x": 140, "y": 140, "width": 200, "height": 200}, name="cerchio")
    path = tmp_path / "progetto.json"
    project.save(path)
    assert window.open_project(path)
    return window, asked


def test_resolution_picker_lists_board_sizes_and_rotation(qtbot, tmp_path, monkeypatch):
    window, _asked = resolution_window(qtbot, tmp_path, monkeypatch)
    selector = window.resolution_selector
    selector.rebuild()
    texts = [action.text() for action in selector.menu().actions()]
    assert selector.text() == "480×480"
    assert any(text.startswith("240×240 — ") for text in texts)
    assert any("Ruota" in text or "Rotate" in text for text in texts)
    window.document.undo_stack.setClean()


def test_adapt_keeps_shapes_and_undo_restores(qtbot, tmp_path, monkeypatch):
    window, asked = resolution_window(qtbot, tmp_path, monkeypatch, "adapt")
    assert window.change_resolution(800, 480)
    widget = window.document.project.find_widget("cerchio")
    assert widget.props["width"] == widget.props["height"] == 200
    assert asked and window.resolution_selector.text() == "800×480"
    window.document.undo_stack.undo()
    assert window.document.project.display.width == 480
    window.document.undo_stack.setClean()


def test_stretch_fills_each_axis(qtbot, tmp_path, monkeypatch):
    window, _asked = resolution_window(qtbot, tmp_path, monkeypatch, "stretch")
    assert window.change_resolution(800, 480)
    widget = window.document.project.find_widget("cerchio")
    assert (widget.props["width"], widget.props["height"]) == (333, 200)
    window.document.undo_stack.setClean()


def test_keep_then_adapt_the_page_later(qtbot, tmp_path, monkeypatch):
    window, asked = resolution_window(qtbot, tmp_path, monkeypatch, "keep")
    assert window.change_resolution(240, 240)
    page = window.document.project.pages[0]
    assert page.designSize == (480, 480) and window.document.project.find_widget("cerchio").props["width"] == 200
    window._update_adapt_page_action()
    assert window.adapt_page_action.isEnabled()
    monkeypatch.setattr("lvgl_mpy_studio.ui.resolution.ResizeDialog.exec", lambda dialog: (dialog.options["adapt"].setChecked(True), QDialog.Accepted)[1])
    assert window.adapt_current_page()
    assert window.document.project.pages[0].designSize is None
    assert window.document.project.find_widget("cerchio").props["width"] == 100
    window._update_adapt_page_action()
    assert not window.adapt_page_action.isEnabled()
    window.document.undo_stack.setClean()


def test_cancelled_resolution_change_changes_nothing(qtbot, tmp_path, monkeypatch):
    window, _asked = resolution_window(qtbot, tmp_path, monkeypatch, accept=False)
    assert not window.change_resolution(800, 480)
    assert window.document.project.display.width == 480 and not window.document.undo_stack.canUndo()
    window.document.undo_stack.setClean()


def test_resolution_change_unlinks_a_board_of_another_size(qtbot, tmp_path, monkeypatch):
    window, asked = resolution_window(qtbot, tmp_path, monkeypatch)
    profile = next(item for item in window.profile_store.profiles() if (item["logicalWidth"], item["logicalHeight"]) == (480, 480))
    def link(project):
        project.board = dict(profile)
        project.runTarget = {"kind": "board", "language": "micropython"}
    window.document.execute("board", link)
    assert window.run_target != SIMULATOR_MICROPYTHON
    assert window.change_resolution(320, 240)
    assert window.document.project.board is None and window.run_target == SIMULATOR_MICROPYTHON
    window.document.undo_stack.setClean()


def test_board_names_are_not_repeated_in_the_picker(qtbot, tmp_path, monkeypatch):
    window, _asked = resolution_window(qtbot, tmp_path, monkeypatch)
    window.resolution_selector.rebuild()
    texts = [action.text() for action in window.resolution_selector.menu().actions()]
    assert not any(text.count("480×480") > 1 for text in texts)
    window.document.undo_stack.setClean()


def test_a_preview_of_another_resolution_is_not_stretched(qtbot, tmp_path, monkeypatch):
    from PySide6.QtGui import QImage
    window, _asked = resolution_window(qtbot, tmp_path, monkeypatch)
    scene = window.current_designer().designer_scene
    scene.set_preview(True, QImage(480, 480, QImage.Format_RGB16))
    assert scene.preview_active
    assert window.change_resolution(800, 480)
    scene = window.current_designer().designer_scene
    scene.set_preview(True, QImage(480, 480, QImage.Format_RGB16))  # the old drawing, still on its way
    assert not scene.preview_active
    scene.set_preview(True, QImage(800, 480, QImage.Format_RGB16))
    assert scene.preview_active
    window.document.undo_stack.setClean()


def test_custom_size_from_the_menu_opens_the_dialog(qtbot, tmp_path, monkeypatch):
    window, asked = resolution_window(qtbot, tmp_path, monkeypatch)
    sizes = []
    def answer(dialog):
        dialog.width.setValue(1024)
        dialog.height.setValue(600)
        sizes.append(dialog.size())
        return QDialog.Accepted
    monkeypatch.setattr("lvgl_mpy_studio.ui.resolution.CustomSizeDialog.exec", answer)
    window.resolution_selector.rebuild()
    custom = window.resolution_selector.menu().actions()[-1]
    custom.trigger()
    assert sizes == [(1024, 600)] and asked
    assert (window.document.project.display.width, window.document.project.display.height) == (1024, 600)
    window.document.undo_stack.setClean()


def test_project_settings_offer_the_board_sizes(qtbot):
    profiles = builtin_profiles()
    dialog = ProjectSettingsDialog(Project("misure"), profiles)
    qtbot.addWidget(dialog)
    sizes = [dialog.preset.itemData(index) for index in range(dialog.preset.count())]
    assert (1024, 600) in sizes and (480, 480) in sizes and (240, 240) in sizes  # 240×240 comes from the Waveshare board
    labels = [dialog.preset.itemText(index) for index in range(dialog.preset.count())]
    assert any(label.startswith("1024×600 — ") for label in labels)


def test_every_entry_of_the_destination_menu_reaches_its_handler(qtbot, tmp_path, monkeypatch):
    window = MainWindow()
    qtbot.addWidget(window)
    selector = window.run_selector
    received = []
    for name in ("changePortRequested", "manageProfilesRequested", "saveDefaultRequested", "clearDefaultRequested"):
        getattr(selector, name).connect(lambda name=name: received.append(name))
    monkeypatch.setattr(window, "select_device", lambda: None)
    monkeypatch.setattr(window, "manage_profiles", lambda: None)
    monkeypatch.setattr(window, "save_new_project_defaults", lambda: None)
    monkeypatch.setattr(window, "clear_new_project_defaults", lambda: None)
    selector.rebuild()
    for action in selector.menu().actions():
        if action.text().startswith(("Cambia porta", "Gestisci", "Usa come", "Rimuovi", "Change Port", "Manage", "Use as", "Remove")):
            action.setEnabled(True)
            action.trigger()
    assert sorted(received) == ["changePortRequested", "clearDefaultRequested", "manageProfilesRequested", "saveDefaultRequested"]
    window.document.undo_stack.setClean()


def test_no_signal_is_handed_over_as_a_menu_callback():
    import re
    from pathlib import Path
    root = Path(__file__).parents[1] / "lvgl_mpy_studio" / "ui"
    sources = {path: path.read_text(encoding="utf-8") for path in root.rglob("*.py")}
    signals = {match for text in sources.values() for match in re.findall(r"^\s*(\w+) = Signal\(", text, re.M)}
    offenders = [f"{path.name}:{number}" for path, text in sources.items() for number, line in enumerate(text.splitlines(), 1)
                 if "addAction(" in line and any(re.search(rf"[(,]\s*self\.{name}\)", line) for name in signals)]
    assert offenders == [], "a Qt signal passed as a function is never called: use lambda: self.<signal>.emit()"
