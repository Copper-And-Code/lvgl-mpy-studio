import json
from pathlib import Path

import pytest

from lvgl_mpy_studio.build.compiler import default_mpy_cross
from lvgl_mpy_studio.gen.board_gen import generate_board, precompile_board

from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.device.service import AUTOSTART_MARKER_V2, DeviceError, DeviceSession


INFO = {
    "implementation": "micropython",
    "implementationVersion": [1, 29, 0],
    "lvglVersion": "9.5.0",
    "version": [3, 4, 0],
    "deviceId": "board-a",
    "modules": {"lvgl": True, "rgbpanel": True, "gt911": True, "display_driver": True},
    "apis": {"lvgl": {"obj": True, "screen_load": True, "EVENT": True}, "display_driver": {"start": True, "stop": True, "WIDTH": True, "HEIGHT": True, "BUFFERS": True, "indev": True}},
    "width": 240,
    "height": 240,
    "buffers": 2,
    "touch": True,
    "memoryFree": 123456,
    "filesystemFree": 987654,
}


class FakeRunner:
    def __init__(self):
        self.calls = []
        self.copies = []
        self.resets = 0
        self.activations = 0
        self.incomplete = False
        self.output = "bootstrap\n"
        self.info = json.loads(json.dumps(INFO))

    def fs_copy(self, command):
        if "fs" not in command or "cp" not in command:
            return False
        cp = command.index("cp")
        source, destination = command[cp + 1:cp + 3]
        self.copies.append((source, destination))
        return True

    def __call__(self, command, timeout):  # noqa: PLR0912
        self.calls.append((command, timeout))
        if command[-2:] == ["devs"] or command[-1] == "devs":
            return "/dev/ttyACM0 abc123 2e8a:0005 MicroPython Board in FS mode\n"
        if self.fs_copy(command):
            return "copied\n"
        if "soft-reset" in command:
            self.resets += 1
            return "reset\n"
        script = command[-1] if command else ""
        if "LVGL_MPY_STUDIO_INFO=" in script:
            return "noise before\nLVGL_MPY_STUDIO_INFO=" + json.dumps(self.info) + "\n"
        if "LVGL_MPY_STUDIO_SIZES=" in script:
            if self.incomplete:
                return "LVGL_MPY_STUDIO_SIZES=" + json.dumps({"broken": -1})
            sizes = {Path(source).name: Path(source).stat().st_size for source, destination in self.copies if destination.startswith(":") and "/lms_apps/" in destination}
            return "LVGL_MPY_STUDIO_SIZES=" + json.dumps(sizes)
        if "os.rename" in script and ".uploading" in script:
            self.activations += 1
            return ""
        if "import app_main" in script:
            return self.output
        if "LVGL_MPY_STUDIO_STOPPED" in script:
            return "interrupted\nLVGL_MPY_STUDIO_STOPPED\n"
        return ""


def project():
    result = Project("demo")
    result.set_display_size(240, 240)
    result.board = builtin_profiles()[0]
    result.add_widget(result.pages[0], "button")
    return result


def connected(runner):
    session = DeviceSession(runner)
    session.connect("/dev/fake", builtin_profiles()[0])
    return session


def test_list_info_and_explicit_connection():
    runner = FakeRunner()
    session = DeviceSession(runner)
    assert session.list_ports()[0] == {"port": "/dev/ttyACM0", "id": "abc123", "usb": "2e8a:0005", "description": "MicroPython Board in FS mode"}
    assert not any("display_driver" in call[0][-1] for call in runner.calls)
    info = session.connect("/dev/fake", builtin_profiles()[0])
    assert info["compatible"] is True
    assert info["buffers"] == 2
    session.disconnect()
    with pytest.raises(DeviceError, match="device.not.connected"):
        session.info()


def test_upload_run_second_upload_and_profile_snapshot(tmp_path):
    runner = FakeRunner()
    original = builtin_profiles()[0]
    session = connected(runner)
    original["logicalWidth"] = 999
    current = project()
    result = session.upload(current, tmp_path / "one", run=True)
    assert result["active"] is True
    assert result["output"] == "bootstrap\n"
    assert runner.activations == 1
    assert runner.resets == 1
    assert all("resume" in call for call, _timeout in runner.calls if "exec" in call)
    assert all(":/main.py" not in destination for _source, destination in runner.copies)
    assert not any("rm -rf" in part for call, _timeout in runner.calls for part in call)
    runner.output = "second version\n"
    result = session.upload(current, tmp_path / "two", run=True)
    assert result["output"] == "second version\n"
    assert runner.activations == 2
    assert runner.resets == 2
    assert any(".previous" in call[-1] for call, _timeout in runner.calls if "os.rename" in call[-1])


def test_incomplete_transfer_does_not_activate(tmp_path):
    runner = FakeRunner()
    runner.incomplete = True
    session = connected(runner)
    with pytest.raises(DeviceError) as result:
        session.upload(project(), tmp_path)
    assert result.value.code == "device.transfer.incomplete"
    assert runner.activations == 0
    assert session.state == "error"


def test_missing_prerequisites_and_cancel_do_not_copy(tmp_path):
    runner = FakeRunner()
    session = connected(runner)
    invalid_project = project()
    invalid_project.board["firmware"]["modules"].append("missing_module")
    with pytest.raises(DeviceError) as result:
        session.upload(invalid_project, tmp_path)
    assert result.value.code == "device.prerequisites"
    assert not runner.copies

    class Cancelled:
        def is_set(self):
            return True

    session = connected(runner)
    with pytest.raises(DeviceError) as result:
        session.upload(project(), tmp_path, cancel=Cancelled())
    assert result.value.code == "device.cancelled"
    assert not runner.copies


def test_stop_restart_evaluate_and_disconnect():
    runner = FakeRunner()
    session = connected(runner)
    assert "LVGL_MPY_STUDIO_STOPPED" in session.stop()
    assert session.evaluate("print('ciao')") == ""
    assert "reset" in session.restart()
    session.disconnect()
    assert session.state == "disconnected"
    assert session.port is None


def test_process_errors_are_classified():
    def timeout(_command, _timeout):
        raise DeviceError("device.timeout", "slow")

    session = DeviceSession(timeout)
    with pytest.raises(DeviceError) as result:
        session.list_ports()
    assert result.value.code == "device.timeout"


def test_autostart_backup_restore_and_ownership(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    remote = {"/main.py": "print('user')\n"}
    session = DeviceSession()
    session.port = "/dev/fake"
    session.profile = builtin_profiles()[0]
    session.device_id = "board-a"

    def execute(args, timeout=20):
        if args[:2] == ["connect", "/dev/fake"]:
            args = args[2:]
        if args[:2] == ["fs", "cp"]:
            source, destination = args[2:4]
            if source == ":/main.py":
                Path(destination).write_text(remote["/main.py"])
            elif destination == ":/main.py":
                remote["/main.py"] = Path(source).read_text()
            return ""
        script = args[-1]
        if "os.stat" in script:
            path = script.split("os.stat(", 1)[1].split(")", 1)[0]
            path = eval(path)
            return "YES\n" if path in remote or path.endswith("/app_main.py") else "NO\n"
        if "LVGL_MPY_STUDIO_FILE=" in script:
            return "LVGL_MPY_STUDIO_FILE=" + json.dumps(remote.get("/main.py"))
        if "os.remove('/main.py')" in script:
            remote.pop("/main.py", None)
        return ""

    session._execute = execute
    current = project()
    result = session.install_autostart(current)
    backup = Path(result["backup"]) / "main.py"
    assert backup.read_text() == "print('user')\n"
    assert remote["/main.py"].startswith(AUTOSTART_MARKER_V2)
    assert session.remove_autostart(current) is True
    assert remote["/main.py"] == "print('user')\n"
    session.install_autostart(current)
    remote["/main.py"] = "print('other')\n"
    with pytest.raises(DeviceError) as error:
        session.remove_autostart(current)
    assert error.value.code == "device.autostart.not-owned"
    assert remote["/main.py"] == "print('other')\n"


def board_output(tmp_path):
    current = project()
    current.board = builtin_profiles()[0]
    return generate_board(current, current.board, tmp_path)


@pytest.mark.skipif(not default_mpy_cross().is_file(), reason="mpy-cross not built")
def test_board_files_become_bytecode_when_firmware_matches(tmp_path):
    result = precompile_board(board_output(tmp_path), tmp_path, 0xB06)
    assert "ui.mpy" in result["files"] and "app_events.mpy" in result["files"]
    assert "ui.py" not in result["files"] and "app_events.py" not in result["files"]
    assert "app_main.py" in result["files"]
    assert (tmp_path / "ui.mpy").read_bytes()[:2] == b"M\x06"
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    assert set(manifest["files"]) >= {"ui.mpy", "app_events.mpy"}
    assert "ui.py" not in manifest["files"]


@pytest.mark.parametrize("board_mpy", [None, 0xB05, "6"])
def test_board_keeps_source_without_matching_bytecode(tmp_path, board_mpy):
    generated = board_output(tmp_path)
    result = precompile_board(generated, tmp_path, board_mpy)
    assert result["files"] == generated["files"]
    assert len(result["warnings"]) == len(generated["warnings"]) + 1


@pytest.mark.skipif(not default_mpy_cross().is_file(), reason="mpy-cross not built")
def test_upload_sends_bytecode_and_verifies_sizes(tmp_path):
    runner = FakeRunner()
    runner.info["mpy"] = 0xB06
    session = DeviceSession(runner=runner)
    current = project()
    current.board = builtin_profiles()[0]
    session.connect("/dev/fake", current.board)
    result = session.upload(current, tmp_path)
    copied = {Path(source).name for source, _destination in runner.copies}
    assert {"ui.mpy", "app_events.mpy", "app_main.py"} <= copied
    assert not {"ui.py", "app_events.py"} & copied
    assert runner.activations == 1
    assert "ui.mpy" in result["files"]


def test_upload_sends_the_user_modules_and_stop_forgets_them(tmp_path):
    from lvgl_mpy_studio.core.modules import create_module

    runner = FakeRunner()
    runner.info["mpy"] = 0xB06
    session = connected(runner)
    current = project()
    current.code.module = "import utils\n"
    create_module(current, "utils", "import helpers\n")
    create_module(current, "helpers", "VALUE = 1\n")
    result = session.upload(current, tmp_path)
    copied = {Path(source).name: destination for source, destination in runner.copies}
    assert {"utils.mpy", "helpers.mpy"} <= set(copied) and not {"utils.py", "helpers.py"} & set(copied)
    assert all(destination.startswith(":/lms_apps/") for destination in copied.values())
    assert {"utils.mpy", "helpers.mpy"} <= set(result["files"])
    session.stop()
    script = runner.calls[-1][0][-1]
    assert "startswith('/lms_apps/')" in script and "LVGL_MPY_STUDIO_STOPPED" in script


class ShellRunner(FakeRunner):
    """A board with a shell in the firmware: the first raw REPL fails until more Ctrl+C arrive."""

    def __init__(self, failures=1):
        super().__init__()
        self.failures = failures

    def __call__(self, command, timeout):
        if "connect" in command and self.failures:
            self.failures -= 1
            raise DeviceError("device.command", "b'mpy@esp32:/$ ^C\\r\\nCtrl-C again leaves the shell'\\nmpremote.transport.TransportError: could not enter raw repl\\n")
        return super().__call__(command, timeout)


def test_a_shell_that_wants_two_ctrl_c_is_interrupted_and_the_command_retried():
    interrupted = []
    runner = ShellRunner()
    session = DeviceSession(runner=runner, interrupt=interrupted.append)
    info = session.connect("/dev/ttyUSB0", builtin_profiles()[0])
    # Once on connecting and once after the failed raw REPL.
    assert info["memoryFree"] == INFO["memoryFree"] and interrupted == ["/dev/ttyUSB0", "/dev/ttyUSB0"]
    assert session.state == "ready"
    session.evaluate("print(1)")
    assert len(interrupted) == 2  # commands that succeed send nothing more


def test_connect_interrupts_the_board_first_except_over_the_stm32_uart():
    interrupted = []
    session = DeviceSession(runner=FakeRunner(), interrupt=interrupted.append)
    session.connect("/dev/ttyUSB0", builtin_profiles()[0])
    assert interrupted == ["/dev/ttyUSB0"]


def test_the_retry_happens_once_and_only_for_the_raw_repl_error():
    interrupted = []
    session = DeviceSession(runner=ShellRunner(failures=2), interrupt=interrupted.append)
    with pytest.raises(DeviceError, match="could not enter raw repl"):
        session.connect("/dev/ttyUSB0", builtin_profiles()[0])
    assert interrupted == ["/dev/ttyUSB0", "/dev/ttyUSB0"]  # on connecting and one retry only

    def busy(command, timeout):
        raise DeviceError("device.busy", "port is busy")
    interrupted.clear()
    session = DeviceSession(runner=busy, interrupt=interrupted.append)
    with pytest.raises(DeviceError, match="busy"):
        session.connect("/dev/ttyUSB0", builtin_profiles()[0])
    assert interrupted == ["/dev/ttyUSB0"]  # only the one on connecting: no retry for other errors


def test_break_in_sends_ctrl_c_with_pauses(monkeypatch):
    import serial

    from lvgl_mpy_studio.device import service

    written, pauses = [], []

    class Link:
        def __init__(self, port, baudrate, timeout):
            self.port = port
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def write(self, data):
            written.append(data)
        def flush(self):
            pass
        def read(self, size):
            return b""

    monkeypatch.setattr(serial, "Serial", Link)
    service.break_in("/dev/ttyUSB0", sleep=pauses.append)
    assert written == [b"\r\x03", b"\x03", b"\x03"] and pauses == [0.3, 0.3, 0.3]

    def absent(*args, **kwargs):
        raise serial.SerialException("could not open port")
    monkeypatch.setattr(serial, "Serial", absent)
    service.break_in("/dev/missing", sleep=pauses.append)  # no exception: mpremote will say so
