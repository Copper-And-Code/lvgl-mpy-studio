import os
from pathlib import Path
import select
import socket
import subprocess
import time

import pytest

from lvgl_mpy_studio.platform import RUNTIME_ENTRY

from lvgl_mpy_studio.build.compiler import compile_python
from lvgl_mpy_studio.core.model import Project, widget_definitions
from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.sim.protocol import Decoder, MessageType, encode_pointer, encode_quit, encode_stop

ROOT = Path(__file__).parents[1]
LINUX_RUNTIME = ROOT / "runtime/out/lvsim-runtime"
WINDOWS_RUNTIME = ROOT / "runtime/out-win64/lvsim-runtime.exe"
WINDOWS_MPY_CROSS = ROOT / "runtime/out-win64/mpy-cross.exe"
pytestmark = pytest.mark.skipif(not WINDOWS_RUNTIME.exists(), reason="Windows runtime not built")


def windows_command(executable=WINDOWS_RUNTIME):
    return [str(executable)] if os.name == "nt" else ["wine", str(executable)]


def generate(tmp_path, kind="button"):
    project = Project(f"windows_{kind}")
    project.add_widget(project.pages[0], kind, {"x": 50, "y": 50}, f"{kind}1")
    output = tmp_path / "generated"
    generate_project(project, output)
    compile_python(output, WINDOWS_MPY_CROSS if os.name == "nt" else None)
    return project, output


def run_headless(runtime, output, dump_name):
    env = os.environ.copy()
    env.update({"LVSIM_HEADLESS": "1", "LVSIM_DUMP": dump_name, "LVSIM_FRAMES": "1", "LVSIM_TICK_MS": "0", "MICROPYPATH": ".", "WINEDEBUG": "-all"})
    command = windows_command(runtime) if runtime.suffix == ".exe" else [str(runtime)]
    return subprocess.run(command + ["main.py"], cwd=output, env=env, capture_output=True, encoding="utf-8", errors="replace", timeout=20)


def test_windows_headless_runtime(tmp_path):
    _project, output = generate(tmp_path)
    result = run_headless(WINDOWS_RUNTIME, output, "frame-windows.raw")
    assert result.returncode == 0, result.stdout + result.stderr
    frame = (output / "frame-windows.raw").read_bytes()
    assert len(frame) == 800 * 480 * 2
    assert any(frame)


@pytest.mark.skipif(os.name == "nt" or not LINUX_RUNTIME.exists(), reason="preliminary parity with the Linux runtime and Wine")
@pytest.mark.parametrize("kind", list(widget_definitions()))
def test_windows_and_linux_frames_are_identical(tmp_path, kind):
    _project, output = generate(tmp_path, kind)
    linux = run_headless(LINUX_RUNTIME, output, "frame-linux.raw")
    assert linux.returncode == 0, linux.stdout + linux.stderr
    windows = run_headless(WINDOWS_RUNTIME, output, "frame-windows.raw")
    assert windows.returncode == 0, windows.stdout + windows.stderr
    linux_frame = (output / "frame-linux.raw").read_bytes()
    windows_frame = (output / "frame-windows.raw").read_bytes()
    assert len(windows_frame) == 800 * 480 * 2
    assert windows_frame == linux_frame


def receive_until_present(connection):
    decoder = Decoder()
    messages = []
    deadline = time.monotonic() + 8
    while time.monotonic() < deadline and not any(kind == MessageType.PRESENT for kind, _data in messages):
        ready, _w, _x = select.select([connection], [], [], 0.2)
        if ready:
            messages.extend(decoder.feed(connection.recv(1024 * 1024)))
    return messages


@pytest.mark.skipif(not WINDOWS_RUNTIME.exists(), reason="Windows runtime not built")
def test_windows_runtime_accepts_accented_project_path(tmp_path):
    project = Project("Progetto è")
    project.add_widget(project.pages[0], "button", name="button1")
    output = tmp_path / "Nunzio Raciti" / "Progetto è"
    generate_project(project, output)
    env = {**os.environ, "LVSIM_HEADLESS": "1", "LVSIM_DUMP": "frame.raw", "LVSIM_FRAMES": "1", "LVSIM_TICK_MS": "0", "MICROPYPATH": ".", "WINEDEBUG": "-all"}
    result = subprocess.run(windows_command() + RUNTIME_ENTRY, cwd=output, env=env, capture_output=True, encoding="utf-8", errors="replace", timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (output / "frame.raw").stat().st_size == project.display.width * project.display.height * 2


def test_windows_protocol_click_stop_and_quit(tmp_path):
    project, output = generate(tmp_path)
    _name, handler = project.ensure_handler("button1")
    handler.body = 'print("WIN_CLICK")\nimport display_driver\nwhile True:\n    display_driver.wait(5)'
    generate_project(project, output)
    compile_python(output)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    token = os.urandom(16)
    env = os.environ.copy()
    env.update({"LVSIM_CONNECT": f"127.0.0.1:{server.getsockname()[1]}", "LVSIM_TOKEN": token.hex(), "MICROPYPATH": ".", "WINEDEBUG": "-all"})
    env.pop("LVSIM_HEADLESS", None)
    process = subprocess.Popen(windows_command() + ["main.py"], cwd=output, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", errors="replace")
    connection = None
    try:
        server.settimeout(8)
        connection, _address = server.accept()
        connection.setblocking(False)
        messages = receive_until_present(connection)
        hello = next(data for kind, data in messages if kind == MessageType.HELLO)
        assert hello["token"] == token
        assert hello["version"] == 2
        assert any(kind == MessageType.RECT for kind, _data in messages)
        connection.sendall(encode_pointer(70, 70, True))
        time.sleep(0.08)
        connection.sendall(encode_pointer(70, 70, False))
        time.sleep(0.2)
        connection.sendall(encode_stop())
        time.sleep(0.1)
        try:
            connection.sendall(encode_quit())
        except OSError:
            pass
        stdout, stderr = process.communicate(timeout=8)
        assert "WIN_CLICK" in stdout + stderr
        assert "KeyboardInterrupt" in stdout + stderr
    finally:
        if connection is not None:
            connection.close()
        server.close()
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
