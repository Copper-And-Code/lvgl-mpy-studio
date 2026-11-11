import os
import re
import subprocess

import pytest

from lvgl_mpy_studio.build.preview import render_page
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.device.service import DeviceError, DeviceSession
from lvgl_mpy_studio.gen.live import LIVE_FAILED, LIVE_OK, design_key, live_script, upload_key
from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.platform import RUNTIME_ENTRY, runtime_path

needs_runtime = pytest.mark.skipif(not runtime_path().exists(), reason="runtime not built")


def project_with(text="Prima"):
    project = Project()
    page = project.pages[0]
    project.add_widget(page, "label", {"x": 20, "y": 20, "text": text}, "label1")
    project.add_widget(page, "button", {"x": 20, "y": 70}, "button1")
    return project


def run_live(tmp_path, first, second, page=0):
    """Start first in the runtime, apply the script of second half way and save the frame."""
    generate_project(first, tmp_path)
    (tmp_path / "live.py").write_text(live_script(second, page), encoding="utf-8")
    main = tmp_path / "main.py"
    source = main.read_text(encoding="utf-8")
    source, count = re.subn(r"\n    while display_driver\.poll\(\):", "\n    lv.timer_handler()\n    exec(open('live.py').read(), {})\n    while display_driver.poll():", source)
    assert count == 1
    main.write_text(source, encoding="utf-8")
    environment = {**os.environ, "MICROPYPATH": ".", "LVSIM_HEADLESS": "1", "LVSIM_FRAMES": "2", "LVSIM_TICK_MS": "50", "LVSIM_DUMP": "frame.raw"}
    for name in ("LVSIM_CONNECT", "LVSIM_TOKEN", "LVSIM_SOCKET"):
        environment.pop(name, None)
    done = subprocess.run([str(runtime_path()), *RUNTIME_ENTRY], cwd=tmp_path, env=environment, capture_output=True, text=True, timeout=10)
    return done.stdout + done.stderr, (tmp_path / "frame.raw").read_bytes()


@needs_runtime
def test_board_shows_the_same_pixels_as_a_fresh_start(tmp_path):
    first, second = project_with("Prima"), project_with("Dopo")
    second.widgets[0].props["textColor"] = "#C62828"
    second.widgets[1].props["x"] = 200
    output, frame = run_live(tmp_path, first, second)
    assert LIVE_OK in output, output
    assert frame == render_page(second, 0)
    assert frame != render_page(first, 0)


@needs_runtime
def test_added_and_removed_widgets_are_applied(tmp_path):
    first, second = project_with(), project_with()
    second.pages[0].widgets[:] = [widget for widget in second.pages[0].widgets if widget.name != "button1"]
    second.add_widget(second.pages[0], "slider", {"x": 20, "y": 200}, "slider1")
    output, frame = run_live(tmp_path, first, second)
    assert LIVE_OK in output, output
    assert frame == render_page(second, 0)


@needs_runtime
def test_timer_is_replaced_with_its_new_period(tmp_path):
    first, second = project_with(), project_with()
    for project in (first, second):
        project.add_widget(project.pages[0], "timer", {"period": 50}, "timer1")
        project.ensure_handler("timer1", "TICK")[1].body = "print('TICK')"
    second.pages[0].widgets[-1].props["period"] = 100
    generate_project(first, tmp_path)
    (tmp_path / "live.py").write_text(live_script(second, 0), encoding="utf-8")
    main = tmp_path / "main.py"
    loop = "\n    for _step in range(20):\n        lv.tick_inc(50)\n        lv.timer_handler()\n    print('END')\n    return\n"
    source = main.read_text(encoding="utf-8").replace("\n    while display_driver.poll():", "\n    lv.timer_handler()\n    exec(open('live.py').read(), {})" + loop + "    while display_driver.poll():")
    main.write_text(source, encoding="utf-8")
    environment = {**os.environ, "MICROPYPATH": ".", "LVSIM_HEADLESS": "1", "LVSIM_TICK_MS": "50"}
    for name in ("LVSIM_CONNECT", "LVSIM_TOKEN", "LVSIM_SOCKET"):
        environment.pop(name, None)
    done = subprocess.run([str(runtime_path()), *RUNTIME_ENTRY], cwd=tmp_path, env=environment, capture_output=True, text=True, timeout=10)
    output = done.stdout + done.stderr
    assert LIVE_OK in output and "END" in output, output
    ticks = output.split(LIVE_OK)[1].count("TICK")
    assert 8 <= ticks <= 11, output  # one 100 ms timer: with two they would be twice or three times as many


@needs_runtime
def test_failed_update_keeps_the_running_page(tmp_path):
    project = project_with()
    broken = live_script(project_with("Dopo"), 0).replace("    lv.screen_load(ui.screens[0])\n", "    raise ValueError('rotto')\n")
    generate_project(project, tmp_path)
    main = tmp_path / "main.py"
    (tmp_path / "live.py").write_text(broken, encoding="utf-8")
    source = main.read_text(encoding="utf-8").replace("\n    while display_driver.poll():", "\n    exec(open('live.py').read(), {})\n    while display_driver.poll():")
    main.write_text(source, encoding="utf-8")
    environment = {**os.environ, "MICROPYPATH": ".", "LVSIM_HEADLESS": "1", "LVSIM_FRAMES": "1", "LVSIM_TICK_MS": "50", "LVSIM_DUMP": "frame.raw"}
    for name in ("LVSIM_CONNECT", "LVSIM_TOKEN", "LVSIM_SOCKET"):
        environment.pop(name, None)
    done = subprocess.run([str(runtime_path()), *RUNTIME_ENTRY], cwd=tmp_path, env=environment, capture_output=True, text=True, timeout=10)
    assert LIVE_FAILED in done.stdout + done.stderr
    assert (tmp_path / "frame.raw").read_bytes() == render_page(project, 0)


def test_script_has_no_comments_or_docstring():
    script = live_script(project_with(), 0)
    assert "Auto-generated" not in script
    assert "# button" not in script


def test_only_code_changes_need_an_upload():
    first, second = project_with(), project_with()
    second.widgets[0].props["text"] = "Altro"
    second.add_widget(second.pages[0], "slider", {}, "slider1")
    assert upload_key(first) == upload_key(second)
    assert design_key(first, 0) != design_key(second, 0)
    second.code.module = "VALORE = 1"
    assert upload_key(first) != upload_key(second)


def test_adding_a_buzzer_needs_an_upload():
    first, second = project_with(), project_with()
    second.add_widget(second.pages[0], "buzzer", {}, "buzzer1")
    assert upload_key(first) != upload_key(second)


def session_with(output):
    calls = []
    def runner(command, timeout):
        calls.append(command)
        return output
    session = DeviceSession(runner=runner)
    session.port = "/dev/null"
    session.state = "ready"
    session.profile = {}
    return session, calls


def test_device_reports_a_failed_update():
    session, _calls = session_with(LIVE_FAILED + " MemoryError()")
    with pytest.raises(DeviceError) as error:
        session.live_update("x")
    assert error.value.code == "device.live"


def test_device_accepts_a_successful_update():
    session, calls = session_with(LIVE_OK + "\n")
    assert LIVE_OK in session.live_update("print(1)")
    assert calls[0][-2:] == ["exec", "print(1)"]


class FakeDevice(DeviceSession):
    def __init__(self):
        super().__init__(runner=lambda command, timeout: LIVE_OK)
        self.port = "/dev/null"
        self.state = "ready"
        self.scripts = []

    def live_update(self, script, cancel=None):
        self.scripts.append(script)
        return LIVE_OK

    def start_console(self, on_output):
        return True


def running_window(qtbot, monkeypatch):
    from lvgl_mpy_studio.ui.main_window import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)
    window._confirm_discard = lambda: True
    window.live_action.setChecked(True)
    window._live_timer.setInterval(1)
    window.device = FakeDevice()
    monkeypatch.setattr(window, "_sync_device_session", lambda: None)
    window.device_app_active = True
    window._live_upload_key = upload_key(window.document.project)
    return window


def change(window, name="label1"):
    window.document.execute("x", lambda project: project.add_widget(project.pages[0], "label", {}, name))


def test_design_change_reaches_the_board(qtbot, monkeypatch):
    window = running_window(qtbot, monkeypatch)
    change(window)
    qtbot.waitUntil(lambda: bool(window.device.scripts), timeout=2000)
    assert "label1" in window.device.scripts[0]


def test_code_change_asks_for_f5_and_sends_nothing(qtbot, monkeypatch):
    window = running_window(qtbot, monkeypatch)
    window.document.project.code.module = "VALORE = 1"
    change(window)
    qtbot.wait(50)
    assert not window.device.scripts
    assert "F5" in window.statusBar().currentMessage()


def test_live_can_be_turned_off(qtbot, monkeypatch):
    window = running_window(qtbot, monkeypatch)
    window.live_action.setChecked(False)
    change(window)
    qtbot.wait(50)
    assert not window.device.scripts


def test_labels_are_italian_in_the_properties_panel():
    from lvgl_mpy_studio.core import i18n

    i18n.set_language("it")
    assert i18n.tr("Text Color") == "Colore testo"
    assert i18n.tr("X Position") == "Posizione X"
    i18n.set_language("en")
    assert i18n.tr("Text Color") == "Text Color"


def test_leaving_the_designer_keeps_the_board_on_the_same_page(qtbot, monkeypatch):
    window = running_window(qtbot, monkeypatch)
    window.document.execute("x", lambda project: project.pages.append(project.new_page("seconda")))
    second = window.document.project.pages[1]
    view = window.designers[second.id][1]
    window.tabs.setCurrentWidget(view)
    assert window._live_page() == 1
    window.tabs.setCurrentWidget(window.code_panel)
    assert window._live_page() == 1


def test_a_quick_switch_to_code_keeps_the_edited_page(qtbot, monkeypatch):
    window = running_window(qtbot, monkeypatch)
    window._live_timer.setInterval(10000)
    window.document.execute("x", lambda project: project.pages.append(project.new_page("seconda")))
    window._live_page_id = window.document.project.pages[0].id
    second = window.document.project.pages[1]
    window.tabs.setCurrentWidget(window.designers[second.id][1])
    window.document.execute("y", lambda project: project.add_widget(project.pages[1], "label", {}, "l2"))
    window.tabs.setCurrentWidget(window.code_panel)
    assert window._live_page() == 1


def test_a_removed_page_falls_back_to_the_initial_one(qtbot, monkeypatch):
    window = running_window(qtbot, monkeypatch)
    window._live_page_id = "non esiste"
    window.tabs.setCurrentWidget(window.code_panel)
    project = window.document.project
    assert window._live_page() == next(index for index, page in enumerate(project.pages) if page.id == project.currentPageId)
