from PySide6.QtCore import QPointF, Qt

from lvgl_mpy_studio.core.events import events_for
from lvgl_mpy_studio.ui.designer.scene import ComponentTray, DesignerView
from lvgl_mpy_studio.ui.document import ProjectDocument
from lvgl_mpy_studio.ui.main_window import MainWindow
from lvgl_mpy_studio.ui.sim_audio import SAMPLE_RATE, TonePlayer, square_wave
from lvgl_mpy_studio.ui.sim_panel import SimPanel


def test_component_is_not_drawn_on_canvas(qtbot):
    document = ProjectDocument()
    view = DesignerView(document)
    qtbot.addWidget(view)
    view.designer_scene.add_widget("timer", QPointF(10, 10))
    assert [widget.name for widget in document.project.widgets] == ["timer1"]
    assert not view.designer_scene.widget_items


def test_tray_lists_selects_and_deletes_components(qtbot):
    document = ProjectDocument()
    tray = ComponentTray(document)
    qtbot.addWidget(tray)
    document.execute("x", lambda project: project.add_widget(project.pages[0], "buzzer", name="buzzer1"))
    assert tray.count() == 1
    with qtbot.waitSignal(tray.selectionChangedTo) as signal:
        tray.item(0).setSelected(True)
    assert signal.args == [["buzzer1"]]
    qtbot.keyClick(tray, Qt.Key_Delete)
    assert not document.project.widgets
    assert tray.count() == 0


def test_events_match_the_component():
    assert events_for("timer") == ["TICK"]
    assert events_for("buzzer") == []
    assert "TICK" not in events_for("button")


def test_main_window_shows_component_properties_and_opens_tick(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.document.execute("x", lambda project: project.add_widget(project.pages[0], "timer", name="timer1"))
    window.component_tray.item(0).setSelected(True)
    assert window.properties.names == ["timer1"]
    window._component_activated("timer1")
    assert window.code_panel.procedure_combo.currentText() == "TICK"
    assert window.code_panel._completions("ui.timer1.x")
    window.document.undo_stack.setClean()


def test_buzzer_completion_lists_its_calls(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.document.execute("x", lambda project: project.add_widget(project.pages[0], "buzzer", name="buzzer1"))
    assert window.code_panel._completions("ui.buzzer1.x") == ["beep", "off", "tone"]
    assert window.code_panel._find_object(("widget", "buzzer1")) < 0
    window.document.undo_stack.setClean()


def test_square_wave_has_the_requested_length_and_frequency():
    data = square_wave(1000, 100)
    assert len(data) == SAMPLE_RATE // 10
    transitions = sum(1 for first, second in zip(data, data[1:]) if first != second)
    assert 180 <= transitions <= 220


def test_tone_player_without_device_stays_silent(qapp):
    player = TonePlayer()
    player.play(440, 30)
    player.stop()


def fake_stdout(panel, monkeypatch, *chunks):
    pending = list(chunks)
    monkeypatch.setattr(panel.process, "readAllStandardOutput", lambda: pending.pop(0))


def test_tone_markers_become_sound_and_never_reach_output(qtbot, monkeypatch):
    panel = SimPanel()
    qtbot.addWidget(panel)
    tones, output = [], []
    panel.tone.connect(lambda frequency, milliseconds: tones.append((frequency, milliseconds)))
    panel.output.connect(lambda text, _error: output.append(text))
    fake_stdout(panel, monkeypatch, b"prima\n\x1bLVSIM_TONE 440 30\ndopo\n\x1bLVSIM_", b"TONE 880 0\nfine\n")
    panel._stdout()
    panel._stdout()
    assert tones == [(440, 30), (880, 0)]
    assert "".join(output) == "prima\ndopo\nfine\n"
