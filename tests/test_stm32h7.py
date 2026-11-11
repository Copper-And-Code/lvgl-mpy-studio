import base64
import copy
import json
from pathlib import Path
import re
import threading

import pytest

from lvgl_mpy_studio.core.boards import builtin_profiles, validate_profile
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.device.service import DeviceError, DeviceSession
from lvgl_mpy_studio.device.uart import UartError, UartTransport
from lvgl_mpy_studio.gen.board_gen import generate_board
from test_device import FakeRunner


def stm32_profile():
    return next(profile for profile in builtin_profiles() if profile["id"] == "stm32h7_core_v1_3_1024x600")


def stm32_project():
    project = Project("stm32demo")
    project.set_display_size(1024, 600)
    project.board = copy.deepcopy(stm32_profile())
    project.add_widget(project.pages[0], "button")
    return project


class FakeSerial:
    def __init__(self):
        self.is_open = False
        self.open_calls = 0
        self.writes = []
        self.incoming = bytearray()
        self.code = bytearray()
        self.remote = {}
        self.fail_next = False

    def open(self):
        assert self.dtr is True
        assert self.rts is False
        self.is_open = True
        self.open_calls += 1

    def close(self):
        self.is_open = False

    def reset_input_buffer(self):
        self.incoming.clear()

    def write(self, data):
        assert self.is_open
        self.writes.append(data)
        if data == b"\r\x01":
            self.code.clear()
            self.incoming.extend(b"raw REPL; CTRL-B to exit\r\n>")
        elif data == b"\x04":
            if self.code:
                self.incoming.extend(self._execute(bytes(self.code)))
                self.code.clear()  # the raw REPL stays open and waits for the next command
            else:
                self.incoming.extend(b"soft reboot\r\n")
        elif data not in (b"\r\x03\x03\x03", b"\x02"):
            self.code.extend(data)
        return len(data)

    def _execute(self, code):
        if self.fail_next:
            self.fail_next = False
            return b"OK\x04Traceback: injected\x04>"
        if code == b"print('ciao')":
            return b"OKciao\r\n\x04\x04>"
        if b"f=open(" in code and b"'wb'" in code:
            path = re.search(rb"f=open\((['\"].*?['\"])", code).group(1).decode()
            self.remote[eval(path)] = bytearray()
        elif b"f.write(binascii.a2b_base64(" in code:
            chunk = re.search(rb"a2b_base64\((['\"].*?['\"])", code).group(1).decode()
            current = next(reversed(self.remote.values()))
            current.extend(base64.b64decode(eval(chunk)))
        elif b"LVGL_MPY_STUDIO_CHUNK=" in code:
            path = re.search(rb"f=open\((['\"].*?['\"])", code).group(1).decode()
            data = bytes(self.remote[eval(path)])
            output = b"LVGL_MPY_STUDIO_CHUNK=" + base64.b64encode(data) + b"\r\nLVGL_MPY_STUDIO_EOF=1\r\n"
            return b"OK" + output + b"\x04\x04>"
        return b"OK\x04\x04>"

    def read(self, size=1):
        if not self.incoming:
            return b""
        data = bytes(self.incoming[:size])
        del self.incoming[:size]
        return data

    @property
    def in_waiting(self):
        return len(self.incoming)


class FakeUart:
    def __init__(self, port):
        self.port = port
        self.runner = FakeRunner()
        self.runner.info.update({
            "width": 1024,
            "height": 600,
            "modules": {"lvgl": True, "display_driver": True, "gt911": True, "st_ltdc": True},
        })
        self.closed = 0

    def execute(self, source, timeout=20, cancel=None):
        return self.runner(["exec", source], timeout)

    def soft_reset(self, cancel=None):
        return self.runner(["soft-reset"], 15)

    def put(self, local, remote, timeout=30, cancel=None):
        return self.runner(["fs", "cp", local, ":" + remote], timeout)

    def get(self, remote, local, timeout=30, cancel=None):
        return self.runner(["fs", "cp", ":" + remote, local], timeout)

    def close(self):
        self.closed += 1


def test_stm32_profile_is_builtin_and_generates_1024x600(tmp_path):
    profile = validate_profile(stm32_profile())
    assert builtin_profiles()[0]["id"] == "waveshare_rp2350_touch_lcd_4_240"
    assert (profile["physicalWidth"], profile["physicalHeight"]) == (1024, 600)
    assert profile["scale"] == 1
    result = generate_board(stm32_project(), profile, tmp_path)
    assert result["manifest"]["profileId"] == profile["id"]
    main = (tmp_path / "app_main.py").read_text()
    assert "(1024, 600)" in main
    assert "display_driver.start()" in main
    adapter = (tmp_path / "board_adapter.py").read_text()
    assert "ADAPTER = 'stm32h7_uart'" in adapter


def test_uart_configures_lines_once_and_uses_chunked_raw_repl(tmp_path):
    serial = FakeSerial()
    transport = UartTransport("/dev/ttyUSB0", serial_factory=lambda: serial, sleep=lambda _seconds: None)
    assert (serial.port, serial.baudrate, serial.timeout) == ("/dev/ttyUSB0", 115200, 0.1)
    assert serial.open_calls == 1
    assert transport.execute("print('ciao')") == "ciao\r\n"
    assert transport.execute("value = 1") == ""
    assert serial.open_calls == 1

    payload = bytes(range(256)) * 3
    local = tmp_path / "payload.bin"
    local.write_bytes(payload)
    entered = serial.writes.count(b"\r\x01")
    transport.put(local, "/flash/payload.bin")
    assert serial.writes.count(b"\r\x01") - entered == 2  # open and close: the chunks stay in the raw REPL
    restored = tmp_path / "restored.bin"
    transport.get("/flash/payload.bin", restored)
    assert restored.read_bytes() == payload
    code_writes = [len(data) for data in serial.writes if data not in (b"\r\x03\x03\x03", b"\r\x01", b"\x04")]
    assert max(code_writes) <= 256
    transport.close()
    assert serial.is_open is False


def test_uart_preserves_remote_traceback_and_supports_cancel():
    serial = FakeSerial()
    transport = UartTransport("/dev/ttyUSB0", serial_factory=lambda: serial, sleep=lambda _seconds: None)
    serial.fail_next = True
    with pytest.raises(UartError) as result:
        transport.execute("print('fail')")
    assert result.value.code == "device.command"
    assert "Traceback: injected" in result.value.output

    class Cancelled:
        def is_set(self):
            return True

    with pytest.raises(UartError) as result:
        transport.execute("print('cancel')", cancel=Cancelled())
    assert result.value.code == "device.cancelled"


def test_stm32_session_reuses_uart_for_upload_run_and_disconnect(tmp_path):
    transports = []

    def factory(port):
        transport = FakeUart(port)
        transports.append(transport)
        return transport

    session = DeviceSession(uart_factory=factory)
    info = session.connect("/dev/ttyUSB0", stm32_profile())
    assert info["compatible"] is True
    assert info["missingModules"] == []
    result = session.upload(stm32_project(), tmp_path / "one", run=True)
    assert result["active"] is True
    assert result["appPath"].startswith("/flash/lms_apps/")
    assert all(destination.startswith(":/flash/lms_apps/") for _source, destination in transports[0].runner.copies)
    assert session.upload(stm32_project(), tmp_path / "two", run=True)["active"] is True
    assert len(transports) == 1
    assert transports[0].closed == 0
    assert transports[0].runner.resets == 2
    assert all("rgbpanel" not in call[0][-1] for call, _timeout in transports[0].runner.calls if "LVGL_MPY_STUDIO_INFO=" in call[0][-1])
    session.disconnect()
    assert transports[0].closed == 1


@pytest.mark.parametrize("found", ("# main utente\n", "# LVGL_IDE_AUTOSTART_V2\nimport app_main\n", "# LMS_AUTOSTART_V2\nimport app_main\n"))
def test_stm32_autostart_uses_flash_main_and_restores_it(tmp_path, monkeypatch, found):
    """A launcher this PC did not install, also one written by 0.4, is never backed up as the user's main.py."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    class AutostartUart:
        def __init__(self):
            self.remote = {"/flash/main.py": found}

        def execute(self, source, timeout=20, cancel=None):
            if "LVGL_MPY_STUDIO_FILE=" in source:
                path = eval(re.search(r"open\((['\"].*?['\"])\)", source).group(1))
                return "LVGL_MPY_STUDIO_FILE=" + json.dumps(self.remote.get(path)) + "\n"
            if "os.stat" in source:
                path = eval(source.split("os.stat(", 1)[1].split(")", 1)[0])
                return "YES\n" if path in self.remote or path.endswith("/app_main.py") else "NO\n"
            if "os.remove(" in source:
                path = eval(re.search(r"os\.remove\((['\"].*?['\"])\)", source).group(1))
                self.remote.pop(path, None)
            return ""

        def put(self, local, remote, timeout=20, cancel=None):
            self.remote[remote] = Path(local).read_text(encoding="utf-8")
            return ""

        def get(self, remote, local, timeout=20, cancel=None):
            Path(local).write_text(self.remote[remote], encoding="utf-8")
            return ""

        def close(self):
            pass

    uart = AutostartUart()
    session = DeviceSession()
    session.port = "/dev/ttyUSB0"
    session.profile = stm32_profile()
    session.device_id = "stm32-a"
    session._uart = uart
    current = stm32_project()
    if "AUTOSTART" in found:
        with pytest.raises(DeviceError) as refused:
            session.install_autostart(current)
        assert refused.value.code == "device.autostart.ambiguous" and uart.remote["/flash/main.py"] == found
        return
    result = session.install_autostart(current)
    assert result["appPath"].startswith("/flash/lms_apps/")
    assert uart.remote["/flash/main.py"].startswith("# LMS_AUTOSTART_V2")
    assert (Path(result["backup"]) / "main.py").read_text() == "# main utente\n"
    assert session.remove_autostart(current) is True
    assert uart.remote["/flash/main.py"] == "# main utente\n"


def test_uart_console_does_not_close_or_reopen_port():
    class ConsoleUart:
        def __init__(self):
            self.payload = bytearray("primo ü\nsecondo\n".encode())
            self.closed = 0

        def read(self, size):
            if not self.payload:
                return b""
            data = bytes(self.payload[:size])
            del self.payload[:size]
            return data

        def close(self):
            self.closed += 1

    uart = ConsoleUart()
    session = DeviceSession()
    session.port = "/dev/ttyUSB0"
    session._uart = uart
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
    assert uart.closed == 0
    session.disconnect()
    assert uart.closed == 1
