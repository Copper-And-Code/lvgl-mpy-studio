import copy
import io
import json
from pathlib import Path
import re
import subprocess
import threading

import pytest

from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.model import Handler
from lvgl_mpy_studio.device.service import DeviceError, DeviceSession
from test_device import FakeRunner, connected, project


def test_syntax_error_preserves_active_app_and_launcher(tmp_path):
    runner = FakeRunner()
    session = connected(runner)
    current = project()
    current.code.handlers["button1_CLICKED"] = Handler("button1", "CLICKED", "if :")
    current.widgets[0].events["CLICKED"] = "button1_CLICKED"
    with pytest.raises(DeviceError) as result:
        session.upload(current, tmp_path, run=True)
    assert result.value.code == "device.syntax"
    assert result.value.errors[0]["handler"] == "button1_CLICKED"
    assert result.value.errors[0]["sourceLine"] == 1
    assert runner.activations == 0
    assert runner.resets == 0
    assert runner.copies == []
    assert all(":/main.py" not in destination for _source, destination in runner.copies)
    current.code.handlers["button1_CLICKED"].body = "print('ok')"
    assert session.upload(current, tmp_path, run=True)["active"] is True
    assert runner.activations == 1


def test_general_module_syntax_error_is_mapped(tmp_path):
    runner = FakeRunner()
    session = connected(runner)
    current = project()
    current.code.module = "value = 1\nif :"
    with pytest.raises(DeviceError) as result:
        session.upload(current, tmp_path)
    assert result.value.code == "device.syntax"
    assert result.value.errors[0]["handler"] == "module"
    assert result.value.errors[0]["sourceLine"] == 2
    assert runner.activations == 0


def test_upload_uses_changed_project_profile_after_connection(tmp_path):
    runner = FakeRunner()
    session = connected(runner)
    current = project()
    changed = copy.deepcopy(current.board)
    changed["id"] = "custom_changed"
    changed["revision"] = 2
    changed["name"] = "Changed profile"
    current.board = changed
    result = session.upload(current, tmp_path)
    assert result["manifest"]["profileId"] == "custom_changed"
    assert result["manifest"]["profileRevision"] == 2
    assert json.loads((tmp_path / "board_profile.json").read_text())["name"] == "Changed profile"
    assert session.profile["id"] == builtin_profiles()[0]["id"]


@pytest.mark.parametrize(
    "change,status",
    [
        ({"implementationVersion": [1, 29, 0], "lvglVersion": "9.5.0"}, "compatible"),
        ({"implementationVersion": [1, 20, 0]}, "incompatible"),
        ({"lvglVersion": "8.3.0"}, "incompatible"),
        ({"implementationVersion": None}, "incomplete"),
        ({"lvglVersion": "malformed"}, "incomplete"),
        ({"modules": {"lvgl": True, "rgbpanel": True, "gt911": True, "display_driver": False}}, "incompatible"),
    ],
)
def test_firmware_compatibility_policy(change, status):
    runner = FakeRunner()
    runner.info.update(change)
    session = DeviceSession(runner)
    info = session.connect("/dev/fake", builtin_profiles()[0])
    assert info["compatibilityStatus"] == status
    assert info["compatible"] is (status == "compatible")
    if status != "compatible":
        assert info["missingRequirements"]


def test_missing_essential_api_blocks_before_transfer(tmp_path):
    runner = FakeRunner()
    runner.info["apis"]["display_driver"]["stop"] = False
    session = DeviceSession(runner)
    session.connect("/dev/fake", builtin_profiles()[0])
    with pytest.raises(DeviceError) as result:
        session.upload(project(), tmp_path)
    assert result.value.code == "device.prerequisites"
    assert "display_driver.stop" in result.value.output
    assert runner.activations == 0
    assert runner.copies == []


class RemoteRunner:
    def __init__(self, identity, original):
        self.identity = identity
        self.remote = {"/main.py": original} if original is not None else {}
        self.fail_remote_write = False

    def __call__(self, command, timeout):
        args = command[3:] if command[:3] == ["python", "-m", "mpremote"] else command
        if "connect" in args:
            args = args[args.index("connect") + 2:]
        if args[:2] == ["fs", "cp"]:
            source, destination = args[2:4]
            if source.startswith(":"):
                Path(destination).write_text(self.remote[source[1:]], encoding="utf-8")
            else:
                if self.fail_remote_write:
                    raise DeviceError("device.command", "injected copy failure")
                self.remote[destination[1:]] = Path(source).read_text(encoding="utf-8")
            return ""
        script = args[-1] if args else ""
        if "LVGL_MPY_STUDIO_IDENTITY=" in script:
            return f"LVGL_MPY_STUDIO_IDENTITY={self.identity}\n"
        if "LVGL_MPY_STUDIO_FILE=" in script:
            path = re.search(r"open\((['\"].*?['\"])\)", script).group(1)
            path = eval(path)
            return "LVGL_MPY_STUDIO_FILE=" + json.dumps(self.remote.get(path)) + "\n"
        if "os.stat" in script:
            path = eval(script.split("os.stat(", 1)[1].split(")", 1)[0])
            return "YES\n" if path in self.remote or path.endswith("/app_main.py") else "NO\n"
        if "os.remove('/main.py')" in script:
            self.remote.pop("/main.py", None)
        return ""


def remote_session(runner, port="/dev/fake"):
    session = DeviceSession(runner)
    session.port = port
    session.profile = builtin_profiles()[0]
    return session


def test_autostart_two_boards_reconnection_and_app_chain(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    board_a, board_b = RemoteRunner("aa01", "print('original A')\n"), RemoteRunner("bb02", "print('original B')\n")
    session_a, session_b = remote_session(board_a), remote_session(board_b)
    current = project()
    session_a.install_autostart(current)
    session_a.install_autostart(current)
    session_b.install_autostart(current)
    launcher_a = board_a.remote["/main.py"]
    other = project()
    other.projectName = "other"
    session_a.install_autostart(other)
    assert board_a.remote["/main.py"] != launcher_a
    with pytest.raises(DeviceError):
        session_a.remove_autostart(current)
    assert session_a.remove_autostart(other) is True
    assert board_a.remote["/main.py"] == "print('original A')\n"
    assert session_b.remove_autostart(current) is True
    assert board_b.remote["/main.py"] == "print('original B')\n"
    reconnected = remote_session(board_a, "/dev/another-port")
    reconnected.install_autostart(current)
    assert "aa01" in str(Path(tmp_path / "lvgl-mpy-studio" / "autostart-backups" / "aa01"))


def test_autostart_modified_backup_and_manifest_never_overwrite(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    runner = RemoteRunner("aa01", "print('original')\n")
    session = remote_session(runner)
    current = project()
    result = session.install_autostart(current)
    launcher = runner.remote["/main.py"]
    runner.remote["/main.py"] = "print('manual')\n"
    with pytest.raises(DeviceError) as error:
        session.remove_autostart(current)
    assert error.value.code == "device.autostart.not-owned"
    assert runner.remote["/main.py"] == "print('manual')\n"
    runner.remote["/main.py"] = launcher
    Path(result["backup"], "main.py").unlink()
    with pytest.raises(DeviceError) as error:
        session.remove_autostart(current)
    assert error.value.code == "device.autostart.backup"
    assert runner.remote["/main.py"] == launcher
    Path(result["backup"], "manifest.json").write_text("not json")
    with pytest.raises(DeviceError) as error:
        session.remove_autostart(current)
    assert error.value.code == "device.autostart.manifest"
    assert runner.remote["/main.py"] == launcher


def test_autostart_copy_failure_is_not_success(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    runner = RemoteRunner("aa01", None)
    runner.fail_remote_write = True
    session = remote_session(runner)
    with pytest.raises(DeviceError):
        session.install_autostart(project())
    assert "/main.py" not in runner.remote
    assert not (tmp_path / "lvgl-mpy-studio" / "autostart-backups" / "aa01" / "current.json").exists()


class ConsoleProcess:
    def __init__(self, payload):
        self.stdout = io.BytesIO(payload)
        self.stdin = io.BytesIO()
        self.returncode = 0

    def wait(self, timeout=None):
        return 0

    def terminate(self):
        self.returncode = -15

    def kill(self):
        self.returncode = -9


def test_console_reads_fragmented_utf8_and_uses_resume_repl():
    process = ConsoleProcess("primo ü\nsecondo\n".encode())
    commands = []
    def factory(command, **kwargs):
        commands.append(command)
        return process
    session = DeviceSession(process_factory=factory)
    session.port = "/dev/fake"
    received = []
    done = threading.Event()
    def output(text):
        received.append(text)
        if "secondo\n" in "".join(received):
            done.set()
    session.start_console(output)
    assert done.wait(2)
    session.stop_console()
    assert "".join(received) == "primo ü\nsecondo\n"
    assert commands[0][-4:] == ["connect", "/dev/fake", "resume", "repl"]


def test_cancel_interrupts_blocked_process():
    class BlockedProcess:
        def __init__(self):
            self.interrupted = False
            self.returncode = None
        def communicate(self, timeout):
            if self.interrupted:
                self.returncode = -2
                return "", "interrupted"
            raise subprocess.TimeoutExpired("command", timeout)
        def send_signal(self, signal):
            self.interrupted = True
        def kill(self):
            self.returncode = -9
    process = BlockedProcess()
    cancel = threading.Event()
    cancel.set()
    session = DeviceSession(process_factory=lambda *args, **kwargs: process)
    with pytest.raises(DeviceError) as result:
        session._run_process(["mpremote"], 10, cancel)
    assert result.value.code == "device.cancelled"
    assert process.interrupted
