import pytest
from PySide6.QtCore import QEvent, QPoint, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication

from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.ui.background import run_in_background
from lvgl_mpy_studio.ui.designer.scene import DesignerView
from lvgl_mpy_studio.ui.document import ProjectDocument
from lvgl_mpy_studio.ui.main_window import MainWindow
from lvgl_mpy_studio.ui.sim_panel import SimPanel


def saved_project(tmp_path, count=2):
    project = Project("rivista")
    for index in range(count):
        project.add_widget(project.pages[0], "button", {"x": 40, "y": 40 + index * 80, "width": 100, "height": 40}, f"button{index}")
    path = tmp_path / "rivista.json"
    project.save(path)
    return path


def window_with(qtbot, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    qtbot.waitExposed(window)
    assert window.open_project(saved_project(tmp_path))
    return window



def filled_view(qtbot, count=2):
    document = ProjectDocument()
    for index in range(count):
        document.project.add_widget(document.project.pages[0], "button", {"x": 40, "y": 40 + index * 80, "width": 100, "height": 40}, f"button{index}")
    view = DesignerView(document)
    qtbot.addWidget(view)
    view.resize(1000, 700)
    view.show()
    qtbot.waitExposed(view)
    return document, view


def point_of(view, item):
    return view.mapFromScene(item.mapToScene(item.rect().center()))


def drag(view, start, end):
    viewport = view.viewport()
    send = lambda kind, point, buttons: QApplication.sendEvent(viewport, QMouseEvent(kind, QPointF(point), QPointF(viewport.mapToGlobal(point)), Qt.LeftButton, buttons, Qt.NoModifier))
    send(QEvent.MouseButtonPress, start, Qt.LeftButton)
    send(QEvent.MouseMove, end, Qt.LeftButton)
    send(QEvent.MouseButtonRelease, end, Qt.NoButton)


def test_failed_simulator_start_releases_the_ide(qtbot, tmp_path):
    runtime = tmp_path / "non-eseguibile"
    runtime.write_text("x", encoding="utf-8")
    runtime.chmod(0o644)
    document = ProjectDocument()
    panel = SimPanel(document, runtime=runtime)
    qtbot.addWidget(panel)
    stops, errors = [], []
    panel.stopped.connect(stops.append)
    panel.error.connect(errors.append)
    panel.start(tmp_path)
    qtbot.waitUntil(lambda: bool(stops), timeout=3000)
    assert not document.read_only
    assert not panel.running
    assert errors


def test_window_stays_editable_after_failed_simulator_start(qtbot, tmp_path, monkeypatch):
    window = window_with(qtbot, tmp_path)
    runtime = tmp_path / "non-eseguibile"
    runtime.write_text("x", encoding="utf-8")
    runtime.chmod(0o644)
    window.sim_panel.runtime = runtime
    window.run_project()
    qtbot.waitUntil(lambda: not window.document.read_only, timeout=3000)
    assert window.current_designer().isEnabled()
    assert not window.code_panel.editor.isReadOnly()
    assert window.run_action.isEnabled()


def test_delete_from_code_tab_does_not_touch_hidden_widgets(qtbot, tmp_path):
    window = window_with(qtbot, tmp_path)
    scene = window.current_designer().designer_scene
    next(iter(scene.widget_items.values())).setSelected(True)
    window.tabs.setCurrentWidget(window.code_panel)
    window.delete_action.trigger()
    assert len(window.document.project.widgets) == 2


def test_edit_menu_acts_on_the_code_editor(qtbot, tmp_path):
    window = window_with(qtbot, tmp_path)
    window.tabs.setCurrentWidget(window.code_panel)
    editor = window.code_panel.editor
    editor.setFocus()
    qtbot.waitUntil(lambda: QApplication.focusWidget() is editor, timeout=1000)
    editor.setPlainText("abc")
    editor.selectAll()
    window.copy_action.trigger()
    window.delete_action.trigger()
    assert editor.toPlainText() == ""
    window.paste_action.trigger()
    assert editor.toPlainText() == "abc"
    assert len(window.document.project.widgets) == 2
    window.document.undo_stack.setClean()


def test_zoom_ignores_hidden_designer(qtbot, tmp_path):
    window = window_with(qtbot, tmp_path)
    view = window.current_designer()
    window.tabs.setCurrentWidget(window.code_panel)
    before = view.transform().m11()
    window.zoom_in_action.trigger()
    assert view.transform().m11() == before


def test_simple_click_does_not_modify_the_project(qtbot):
    document, view = filled_view(qtbot)
    item = next(iter(view.designer_scene.widget_items.values()))
    point = point_of(view, item)
    drag(view, point, point)
    assert view.designer_scene.selected_names() == [item.name]
    assert not document.undo_stack.count()
    assert not document.modified


def test_dragging_moves_all_selected_widgets_in_one_step(qtbot):
    document, view = filled_view(qtbot)
    scene = view.designer_scene
    items = list(scene.widget_items.values())
    for item in items:
        item.setSelected(True)
    point = point_of(view, items[0])
    drag(view, point, point + QPoint(30, 20))
    widgets = {widget.name: widget.props for widget in document.project.widgets}
    assert (widgets["button0"]["x"], widgets["button0"]["y"]) == (70, 60)
    assert (widgets["button1"]["x"], widgets["button1"]["y"]) == (70, 140)
    assert document.undo_stack.count() == 1
    assert sorted(scene.selected_names()) == ["button0", "button1"]


def test_dragging_an_unselected_widget_moves_only_that_one(qtbot):
    document, view = filled_view(qtbot)
    scene = view.designer_scene
    items = list(scene.widget_items.values())
    items[0].setSelected(True)
    point = point_of(view, items[1])
    drag(view, point, point + QPoint(25, 0))
    widgets = {widget.name: widget.props for widget in document.project.widgets}
    assert widgets["button0"]["x"] == 40
    assert widgets["button1"]["x"] == 65


def test_copy_and_paste_work_across_pages(qtbot, tmp_path):
    window = window_with(qtbot, tmp_path)
    window.add_page()
    pages = window.document.project.pages
    first, second = (window.designers[page.id][1] for page in pages[:2])
    window.tabs.setCurrentWidget(first)
    next(iter(first.designer_scene.widget_items.values())).setSelected(True)
    first.setFocus()
    window.copy_action.trigger()
    window.tabs.setCurrentWidget(second)
    second.setFocus()
    window.paste_action.trigger()
    assert len(window.document.project.pages[1].widgets) == 1
    window.document.undo_stack.setClean()


def test_opening_a_project_shows_the_designer(qtbot, tmp_path):
    window = window_with(qtbot, tmp_path)
    assert isinstance(window.tabs.currentWidget(), DesignerView)
    window.new_project()
    assert isinstance(window.tabs.currentWidget(), DesignerView)


def test_typing_code_does_not_rebuild_the_canvas(qtbot, tmp_path):
    window = window_with(qtbot, tmp_path)
    scene = window.current_designer().designer_scene
    calls = []
    window.document.reset.connect(lambda: calls.append(1))
    panel = window.code_panel
    panel.editor.insertPlainText("x = 1\n")
    panel.editor.insertPlainText("y = 2\n")
    assert window.document.project.code.module == "x = 1\ny = 2\n"
    assert not calls
    assert scene.widget_items
    window.document.undo_stack.undo()
    assert window.document.project.code.module == ""
    window.document.undo_stack.setClean()


def test_build_runs_in_background_and_reports_the_result(qtbot, tmp_path, monkeypatch):
    window = window_with(qtbot, tmp_path)
    runner = tmp_path / "dist" / "run.sh"
    release = pytest.importorskip("lvgl_mpy_studio.build.release")
    monkeypatch.setattr(release, "build_release", lambda project, target, output: runner)
    assert window.build_executable() is True
    assert not window.build_action.isEnabled()
    assert window.build_executable() is False
    qtbot.waitUntil(window.build_action.isEnabled, timeout=2000)
    assert "run.sh" in window.output.toPlainText()


def test_build_failure_is_reported(qtbot, tmp_path, monkeypatch):
    window = window_with(qtbot, tmp_path)
    release = pytest.importorskip("lvgl_mpy_studio.build.release")
    def fail(project, target, output):
        raise OSError("disco pieno")
    monkeypatch.setattr(release, "build_release", fail)
    window.build_executable()
    qtbot.waitUntil(window.build_action.isEnabled, timeout=2000)
    assert "disco pieno" in window.output.toPlainText()


def test_background_helper_returns_in_the_main_thread(qtbot):
    results = []
    run_in_background(None, lambda: 42, lambda succeeded, value: results.append((succeeded, value)))
    qtbot.waitUntil(lambda: bool(results), timeout=2000)
    assert results == [(True, 42)]


def test_single_file_build_asks_for_release_and_a_single_file(qtbot, tmp_path, monkeypatch):
    window = window_with(qtbot, tmp_path)
    executable = tmp_path / "dist" / "gioco"
    release = pytest.importorskip("lvgl_mpy_studio.build.release")
    calls = []
    def build(project, target, output, profile="debug", single_file=False):
        calls.append((target, profile, single_file))
        return executable
    monkeypatch.setattr(release, "build_release", build)
    window.single_file_action.trigger()
    assert not window.single_file_action.isEnabled() and not window.build_action.isEnabled()
    qtbot.waitUntil(window.single_file_action.isEnabled, timeout=2000)
    assert calls == [("micropython", "release", True)]
    assert "gioco" in window.output.toPlainText()


def test_open_in_browser_builds_serves_and_opens(qtbot, tmp_path, monkeypatch):
    window = window_with(qtbot, tmp_path)
    web = pytest.importorskip("lvgl_mpy_studio.build.web")
    folder = tmp_path / "dist" / "gioco-web"
    folder.mkdir(parents=True)
    (folder / "index.html").write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(web, "build_web", lambda project, output: folder)
    opened = []
    monkeypatch.setattr("PySide6.QtGui.QDesktopServices.openUrl", lambda url: opened.append(url.toString()))
    assert window.open_in_browser() is True
    qtbot.waitUntil(lambda: bool(opened), timeout=3000)
    assert opened[0].startswith("http://127.0.0.1:")
    import urllib.request
    with urllib.request.urlopen(opened[0] + "index.html") as response:
        assert b"<html>" in response.read()
    window._web_server.shutdown()
    window._web_server = None
