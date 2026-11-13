"""Programs without pages in the simulator: preparation, the sandbox, the runtime, the IDE."""

import importlib.util
import os
from pathlib import Path
import subprocess
import threading
import time

import pytest

from lvgl_mpy_studio.build import program
from lvgl_mpy_studio.platform import root_dir, runtime_path

PROGRAM_DIR = root_dir() / "runtime" / "program"
needs_runtime = pytest.mark.skipif(not runtime_path().exists(), reason="runtime not built")


@pytest.fixture
def config(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    return tmp_path


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def test_prepare_copies_the_folder_like_an_upload(config):
    folder = config / "prog"
    entry = write(folder / "main.py", "print('hi')\n")
    write(folder / "lib" / "util.py", "")
    write(folder / "__pycache__" / "main.cpython.pyc", "")
    write(folder / ".git" / "HEAD", "")
    prepared = program.prepare_program(entry, 480, 320, "stm32h7_core")
    flash = prepared["flash"]
    assert sorted(str(path.relative_to(flash)) for path in flash.rglob("*") if path.is_file()) == ["lib/util.py", "main.py"]
    assert prepared["environment"] == {
        "LVSIM_WIDTH": "480", "LVSIM_HEIGHT": "320", "LMS_FLASH": str(flash), "LMS_ENTRY": "main.py", "LMS_BOARD": "stm32h7_core",
    }
    assert {path.name for path in prepared["boot"].iterdir()} >= {"lms_program_boot.py", "display_driver.py", "os.py", "machine.py", "lms_sandbox.py"}
    assert prepared["arguments"][-2:] == ["-c", "import lms_program_boot"]
    write(flash / "written-by-the-program.txt", "keep")
    write(folder / "main.py", "print('changed')\n")
    program.prepare_program(entry, 480, 320)
    assert (flash / "written-by-the-program.txt").read_text() == "keep"  # a board keeps its files
    assert (flash / "main.py").read_text() == "print('changed')\n"
    assert flash == program.flash_dir(folder)
    program.reset_flash(folder)
    assert not flash.exists()


def test_prepare_refuses_what_is_not_a_program(config, monkeypatch):
    with pytest.raises(ValueError):
        program.prepare_program(write(config / "notes.txt", ""), 480, 320)
    monkeypatch.setattr(program, "MAX_BYTES", 10)
    with pytest.raises(ValueError, match="MB"):
        program.prepare_program(write(config / "big" / "main.py", "x" * 100), 480, 320)


def test_sandbox_paths_never_leave_the_root():
    spec = importlib.util.spec_from_file_location("lms_sandbox", PROGRAM_DIR / "lms_sandbox.py")
    sandbox = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sandbox)
    normalize = sandbox.normalize
    assert normalize("/") == "/"
    assert normalize("/..") == "/"
    assert normalize("/../../etc/passwd") == "/etc/passwd"
    assert normalize("a/../../b", "/x/y") == "/x/b"
    assert normalize("./c//d/.", "/x") == "/x/c/d"
    assert normalize("..", "/") == "/"


# ---- In the real runtime ----


def run_runtime(cwd, arguments, keys=(), env=None, timeout=10):
    """The runtime headless, with keys written to its standard input one group at a time."""
    environment = {**os.environ, "MICROPYPATH": ".", "LVSIM_HEADLESS": "1", **(env or {})}
    process = subprocess.Popen([str(runtime_path()), *arguments], cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=environment)
    chunks = []
    reader = threading.Thread(target=lambda: chunks.extend(iter(lambda: process.stdout.read1(4096), b"")), daemon=True)
    reader.start()
    for delay, data in keys:
        time.sleep(delay)
        process.stdin.write(data)
        process.stdin.flush()
    process.stdin.close()
    process.wait(timeout=timeout)
    reader.join(timeout=2)
    return process.returncode, b"".join(chunks).decode("utf-8", "replace")


@needs_runtime
def test_runtime_serves_lvgl_while_the_program_waits_and_ctrl_c_follows_kbd_intr(tmp_path):
    write(tmp_path / "probe.py", """
import lvsim, sys, micropython, time
count = 0
def tick(_):
    global count
    count += 1
lvsim.keys()
lvsim.service(tick, 5)
c = sys.stdin.read(1)
print("got", repr(c), "ticks", count > 40)
try:
    while True:
        sys.stdin.read(1)
except KeyboardInterrupt:
    print("interrupted")
micropython.kbd_intr(-1)
print("key", repr(sys.stdin.read(1)))
micropython.kbd_intr(3)
before = count
time.sleep(0.2)
print("sleep served", count - before > 15)
""")
    code, output = run_runtime(tmp_path, ["probe.py"], keys=[(0.5, b"a"), (0.3, b"\x03"), (0.3, b"\x03")])
    assert code == 0, output
    assert "got 'a' ticks True" in output
    assert "interrupted" in output
    assert "key '\\x03'" in output
    assert "sleep served True" in output


def boot(config, source, keys=(), board="simulator"):
    entry = write(config / "prog" / "main.py", source)
    write(config / "outside.txt", "keep")
    prepared = program.prepare_program(entry, 320, 240, board)
    code, output = run_runtime(prepared["boot"], prepared["arguments"], keys=keys, env=prepared["environment"])
    return code, output, prepared["flash"]


@needs_runtime
def test_a_program_sees_only_its_flash(config):
    code, output, flash = boot(config, """
import os
print("root", sorted(os.listdir("/")))
print("up", sorted(os.listdir("/../..")))
with open("/../../outside.txt", "w") as f:
    f.write("inside")
def remove(path):
    for name in os.listdir(path):
        full = path.rstrip("/") + "/" + name
        if os.stat(full)[0] & 0x4000:
            remove(full)
            os.rmdir(full)
        else:
            os.remove(full)
remove("/..")
print("left", os.listdir("/"))
""")
    assert "root ['main.py']" in output
    assert "up ['main.py']" in output
    assert "left []" in output, output
    assert (config / "outside.txt").read_text() == "keep"
    assert (config / "prog" / "main.py").exists()  # the folder of the program is a source: only its copy goes
    assert list(flash.iterdir()) == []


@needs_runtime
def test_a_program_finds_a_board_then_the_repl(config):
    code, output, _flash = boot(config, """
import os, machine, display_driver
print("uname", os.uname().sysname, os.uname().machine)
print("display", display_driver.WIDTH, display_driver.HEIGHT, display_driver._timer is not None)
""", keys=[(1.5, b"1+1\r"), (0.3, b"x = 3; x * 2\r")], board="stm32h7_core")
    assert "uname stm32h7_core stm32h7_core (simulator)" in output
    assert "display 320 240 True" in output
    assert "The program ended" in output
    assert ">>> 1+1\r\n2" in output or "2\n" in output.split("1+1", 1)[1]
    assert "6" in output.split("x * 2", 1)[1]


@needs_runtime
def test_machine_reset_ends_with_the_restart_code(config):
    code, output, _flash = boot(config, "import machine\nprint('before')\nmachine.reset()\nprint('after')\n")
    assert code == program.RESET_EXIT_CODE, output
    assert "before" in output and "after" not in output


# ---- In the IDE ----


@needs_runtime
def test_run_program_in_the_ide_takes_keys_and_restarts_on_reset(qtbot, config):
    from lvgl_mpy_studio.ui.main_window import MainWindow

    entry = write(config / "prog" / "main.py", """
import sys, machine
import display_driver
import lvgl as lv
label = lv.label(lv.screen_active())
label.set_text("waiting")
print("ready")
while True:
    c = sys.stdin.read(1)
    if c == "r":
        machine.reset()
    label.set_text("key " + c)
    print("key", c)
""")
    window = MainWindow()
    qtbot.addWidget(window)
    started = []
    window.sim_panel.started.connect(lambda: started.append(1))
    assert window.run_program(entry)
    assert window.sim_panel.program and window.sim_panel.terminal.isVisible() or not window.isVisible()
    assert not window.document.read_only  # the open project stays editable
    terminal = window.sim_panel.terminal
    qtbot.waitUntil(lambda: "ready" in terminal.text(), timeout=10000)
    window.sim_panel.write_keys(b"x")
    qtbot.waitUntil(lambda: "key x" in terminal.text(), timeout=5000)
    assert "key x\n" in terminal.text()  # LF from the unix port shown as a new line, not a staircase
    window.sim_panel.write_keys(b"r")
    qtbot.waitUntil(lambda: len(started) == 2, timeout=10000)  # machine.reset() started it again
    qtbot.waitUntil(lambda: terminal.text().count("ready") >= 2, timeout=10000)
    window.sim_panel.shutdown()
    assert Path(window.settings.value("simulator/program")) == entry
    window.document.undo_stack.setClean()
