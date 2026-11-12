import json
import os
from pathlib import Path
import select
import socket
import subprocess
import time

import pytest

from lvgl_mpy_studio.build.compiler import compile_python
from lvgl_mpy_studio.core.model import Project, widget_definitions
from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.sim.protocol import Decoder, MessageType, encode_pointer, encode_quit, encode_stop

ROOT = Path(__file__).parents[1]
RUNTIME = ROOT / "runtime/out/lvsim-runtime"
MPY_CROSS = ROOT / "runtime/out/mpy-cross"
pytestmark = pytest.mark.skipif(not RUNTIME.exists() or not MPY_CROSS.exists(), reason="native runtime not built")


def make_project(kind="button"):
    project = Project(f"test_{kind}")
    project.add_widget(project.pages[0], kind, name=f"{kind}1")
    return project


def generate(tmp_path, project):
    output = tmp_path / "generated"
    generate_project(project, output)
    compile_python(output)
    return output


def run_headless(output, extra_env=None):
    env = os.environ.copy()
    env.update({"LVSIM_HEADLESS": "1", "LVSIM_DUMP": str(output / "frame.raw"), "LVSIM_FRAMES": "1", "MICROPYPATH": "."})
    env.update(extra_env or {})
    return subprocess.run([str(RUNTIME), "main.py"], cwd=output, env=env, capture_output=True, encoding="utf-8", errors="replace", timeout=15)


def start_ide_session(output):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    token = os.urandom(16)
    env = os.environ.copy()
    env.update({"LVSIM_CONNECT": f"127.0.0.1:{server.getsockname()[1]}", "LVSIM_TOKEN": token.hex(), "MICROPYPATH": "."})
    env.pop("LVSIM_HEADLESS", None)
    process = subprocess.Popen([str(RUNTIME), "main.py"], cwd=output, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", errors="replace")
    try:
        server.settimeout(5)
        connection, address = server.accept()
        assert address[0] == "127.0.0.1"
        connection.setblocking(False)
        return server, connection, process, token
    except Exception:
        process.kill()
        process.wait(timeout=5)
        server.close()
        raise


def receive_until_present(connection):
    decoder = Decoder()
    messages = []
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and not any(kind == MessageType.PRESENT for kind, _data in messages):
        ready, _w, _x = select.select([connection], [], [], 0.2)
        if ready:
            messages.extend(decoder.feed(connection.recv(1024 * 1024)))
    return messages


def close_ide_session(server, connection, process):
    connection.close()
    server.close()
    if process.poll() is None:
        process.kill()
        process.wait(timeout=5)


@pytest.mark.parametrize("kind", list(widget_definitions()))
def test_all_30_widgets_render_non_black_frames(tmp_path, kind):
    output = generate(tmp_path, make_project(kind))
    result = run_headless(output)
    assert result.returncode == 0, result.stderr
    frame = (output / "frame.raw").read_bytes()
    assert len(frame) == 800 * 480 * 2
    assert any(frame)


def test_socket_frame_and_button_event(tmp_path):
    project = Project("test_colliding_names")
    project.add_widget(project.pages[0], "button", {"x": 50, "y": 50}, "MyButton")
    project.add_widget(project.pages[0], "button", {"x": 200, "y": 50}, "mybutton")
    project.add_widget(project.pages[0], "label", {"x": 30, "y": 200}, "statusLabel")
    _name, first = project.ensure_handler("MyButton")
    first.body = 'ui.MyButton.set_width(120)\nui.statusLabel.set_text("Primo")\nprint("FIRST_OK")'
    _name, second = project.ensure_handler("mybutton")
    second.body = 'ui.mybutton.set_width(120)\nprint("SECOND_OK")'
    long_name = "widget_" + "a" * 60
    for index, name in enumerate((long_name, long_name + "_other")):
        project.add_widget(project.pages[0], "button", {"x": 10 + index * 150, "y": 300}, name)
        project.ensure_handler(name)
    output = generate(tmp_path, project)
    for x, expected in ((70, "FIRST_OK"), (220, "SECOND_OK")):
        server, connection, process, token = start_ide_session(output)
        try:
            messages = receive_until_present(connection)
            hello = next(data for kind, data in messages if kind == MessageType.HELLO)
            assert hello["token"] == token
            assert hello["version"] == 2
            assert any(kind == MessageType.RECT for kind, _data in messages)
            connection.sendall(encode_pointer(x, 70, True))
            time.sleep(0.08)
            connection.sendall(encode_pointer(x, 70, False))
            time.sleep(0.15)
            connection.sendall(encode_quit())
            stdout, stderr = process.communicate(timeout=5)
            assert process.returncode == 0, stderr
            assert expected in stdout
        finally:
            close_ide_session(server, connection, process)


def test_recreated_widget_uses_preserved_orphan_handler(tmp_path):
    project = Project("test_orphan_reattachment")
    project.add_widget(project.pages[0], "button", {"x": 50, "y": 50}, "button1")
    _name, handler = project.ensure_handler("button1", "CLICKED")
    handler.body = 'print("ORPHAN_REATTACHED")'
    project.remove_widget("button1")
    project.add_widget(project.pages[0], "button", {"x": 50, "y": 50}, "button1")
    project.ensure_handler("button1", "CLICKED")
    assert project.code.handlers["button1_clicked"].body == 'print("ORPHAN_REATTACHED")'
    output = generate(tmp_path, project)
    server, connection, process, _token = start_ide_session(output)
    try:
        assert any(kind == MessageType.PRESENT for kind, _data in receive_until_present(connection))
        connection.sendall(encode_pointer(70, 70, True))
        time.sleep(0.08)
        connection.sendall(encode_pointer(70, 70, False))
        time.sleep(0.15)
        connection.sendall(encode_quit())
        stdout, stderr = process.communicate(timeout=5)
        assert process.returncode == 0, stderr
        assert "ORPHAN_REATTACHED" in stdout
    finally:
        close_ide_session(server, connection, process)


def test_stop_interrupts_waiting_handler_then_quit(tmp_path):
    project = make_project()
    _name, handler = project.ensure_handler("button1")
    handler.body = "import display_driver\nwhile True:\n    display_driver.wait(5)"
    output = generate(tmp_path, project)
    server, connection, process, _token = start_ide_session(output)
    try:
        assert any(kind == MessageType.PRESENT for kind, _data in receive_until_present(connection))
        connection.sendall(encode_pointer(70, 70, True))
        time.sleep(0.08)
        connection.sendall(encode_pointer(70, 70, False))
        time.sleep(0.15)
        connection.sendall(encode_stop())
        time.sleep(0.1)
        try:
            connection.sendall(encode_quit())
        except OSError:
            pass
        stdout, stderr = process.communicate(timeout=5)
        assert "KeyboardInterrupt" in stdout + stderr, (stdout, stderr)
    finally:
        close_ide_session(server, connection, process)


def test_socket_close_stops_runtime(tmp_path):
    output = generate(tmp_path, make_project())
    server, connection, process, _token = start_ide_session(output)
    try:
        assert any(kind == MessageType.PRESENT for kind, _data in receive_until_present(connection))
        connection.close()
        server.close()
        _stdout, stderr = process.communicate(timeout=5)
        assert process.returncode == 0, stderr
    finally:
        close_ide_session(server, connection, process)


def test_sdl_selftest_under_xvfb(tmp_path):
    output = generate(tmp_path, make_project())
    env = os.environ.copy()
    env.update({"LVSIM_FRAMES": "1", "MICROPYPATH": "."})
    env.pop("LVSIM_HEADLESS", None)
    env.pop("LVSIM_CONNECT", None)
    env.pop("LVSIM_TOKEN", None)
    # starting a display server takes a second here and many on a shared machine
    result = subprocess.run(["xvfb-run", "-a", str(RUNTIME), "main.py"], cwd=output, env=env, capture_output=True, encoding="utf-8", errors="replace", timeout=90)
    assert result.returncode == 0, result.stderr


def test_sourcemap_points_to_user_handler(tmp_path):
    project = make_project()
    _name, handler = project.ensure_handler("button1")
    handler.body = "x = 1\ndef broken(\n"
    output = tmp_path / "generated"
    generate_project(project, output)
    with pytest.raises(Exception) as caught:
        compile_python(output)
    assert "app_events.py" in str(caught.value)
    sourcemap = json.loads((output / "sourcemap.json").read_text())
    entry = next(item for item in sourcemap["entries"] if item["handler"] == "button1_clicked" and item["sourceLine"] == 2)
    assert entry["line"] > 0
