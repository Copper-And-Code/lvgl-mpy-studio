import pytest
from PySide6.QtCore import QEvent, QPointF, QSettings, Qt
from PySide6.QtGui import QColor, QImage, QMouseEvent
from PySide6.QtWidgets import QApplication

from lvgl_mpy_studio.build.preview import design_key, render_page
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.platform import runtime_path
from lvgl_mpy_studio.ui.designer.preview import PreviewRenderer, frame_image
from lvgl_mpy_studio.ui.designer.scene import DesignerView
from lvgl_mpy_studio.ui.document import ProjectDocument
from lvgl_mpy_studio.ui.main_window import MainWindow

needs_runtime = pytest.mark.skipif(not runtime_path().exists(), reason="native runtime not built")


def red_panel_project():
    project = Project("anteprima")
    project.set_display_size(320, 240)
    project.add_widget(project.pages[0], "panel", {"x": 10, "y": 10, "width": 100, "height": 100, "bgColor": "#FF0000", "borderWidth": 0, "radius": 0}, "rosso")
    return project


def pixel(pixels, width, height, x, y):
    return frame_image(pixels, width, height).pixelColor(x, y)


@needs_runtime
def test_render_shows_the_real_widget():
    pixels = render_page(red_panel_project(), 0)
    assert len(pixels) == 320 * 240 * 2
    color = pixel(pixels, 320, 240, 60, 60)
    assert color.red() > 240 and color.green() < 20
    assert pixel(pixels, 320, 240, 200, 200).red() != color.green()


@needs_runtime
def test_render_selects_the_page():
    project = red_panel_project()
    project.pages.append(project.new_page("vuota"))
    first, second = render_page(project, 0), render_page(project, 1)
    assert first != second


@needs_runtime
def test_user_code_does_not_run_in_the_designer():
    clean = render_page(red_panel_project(), 0)
    project = red_panel_project()
    project.code.module = "raise ValueError('rotto')\n"
    project.ensure_handler("main", "SCREEN_LOADED")[1].body = "ui.rosso.add_flag(lv.obj.FLAG.HIDDEN)\n"
    assert render_page(project, 0) == clean


def test_design_key_ignores_code_but_not_widgets():
    project = red_panel_project()
    key = design_key(project, 0)
    project.code.module = "x = 1\n"
    assert design_key(project, 0) == key
    project.widgets[0].props["x"] = 11
    assert design_key(project, 0) != key
    assert design_key(project, 1) != design_key(project, 0)


def test_renderer_uses_latest_request_and_skips_identical_ones(qtbot):
    calls = []
    def render(project, page_index):
        calls.append(project.projectName)
        return b"\0" * (800 * 480 * 2)
    renderer = PreviewRenderer(render=render, delay=5)
    renderer.request(Project("primo"), "p", 0)
    last = Project("ultimo")
    renderer.request(last, "p", 0)
    with qtbot.waitSignal(renderer.rendered, timeout=2000):
        pass
    assert calls == ["ultimo"]
    assert renderer.request(last, "p", 0) is False


def test_renderer_failure_gives_empty_frame_and_can_retry(qtbot):
    def render(project, page_index):
        raise RuntimeError("boom")
    renderer = PreviewRenderer(render=render, delay=1)
    project = Project("x")
    renderer.request(project, "p", 0)
    with qtbot.waitSignal(renderer.rendered, timeout=2000) as signal:
        pass
    assert signal.args[1] is None
    assert renderer.request(project, "p", 0) is True
    renderer.stop()


def solid_image(document, color):
    image = QImage(document.project.display.width, document.project.display.height, QImage.Format_RGB16)
    image.fill(QColor(color))
    return image


def test_scene_shows_frame_and_keeps_widgets_interactive(qtbot):
    document = ProjectDocument()
    view = DesignerView(document)
    qtbot.addWidget(view)
    view.resize(1000, 700)
    view.designer_scene.add_widget("button", QPointF(100, 100))
    view.designer_scene.set_preview(True, solid_image(document, "#00FF00"))
    view.show()
    qtbot.waitExposed(view)
    point = view.mapFromScene(QPointF(120, 120))
    color = view.grab().toImage().pixelColor(point)
    assert color.green() > 240 and color.blue() < 20
    item = next(iter(view.designer_scene.widget_items.values()))
    qtbot.mouseClick(view.viewport(), Qt.LeftButton, pos=point)
    assert view.designer_scene.selected_names() == [item.name]


def test_drop_preview_stays_visible_over_the_frame(qtbot):
    document = ProjectDocument()
    view = DesignerView(document)
    qtbot.addWidget(view)
    view.resize(1000, 700)
    scene = view.designer_scene
    scene.set_preview(True, solid_image(document, "#00FF00"))
    view.show()
    qtbot.waitExposed(view)
    point = QPointF(300, 200)
    scene.show_drop_preview("button", point)
    color = view.grab().toImage().pixelColor(view.mapFromScene(point))
    assert not (color.green() > 240 and color.blue() < 20)
    scene.hide_drop_preview()


def mouse(view, kind, point, buttons):
    viewport = view.viewport()
    QApplication.sendEvent(viewport, QMouseEvent(kind, QPointF(point), QPointF(viewport.mapToGlobal(point)), Qt.LeftButton, buttons, Qt.NoModifier))


@needs_runtime
def test_frame_follows_a_widget_while_dragging(qtbot, tmp_path):
    project = red_panel_project()
    project.board = None
    path = tmp_path / "drag.json"
    project.save(path)
    window = MainWindow()
    qtbot.addWidget(window)
    window.settings = QSettings(str(tmp_path / "settings.ini"), QSettings.IniFormat)
    window.preview_action.setChecked(True)
    window._toggle_preview(True)
    window.show()
    qtbot.waitExposed(window)
    assert window.open_project(path)
    view = window.current_designer()
    scene = view.designer_scene
    qtbot.waitUntil(lambda: scene.preview_active, timeout=3000)
    item = next(iter(scene.widget_items.values()))
    start = view.mapFromScene(QPointF(60, 60))
    end = view.mapFromScene(QPointF(160, 130))
    mouse(view, QEvent.MouseButtonPress, start, Qt.LeftButton)
    mouse(view, QEvent.MouseMove, end, Qt.LeftButton)
    red = lambda x, y: scene.preview_image.pixelColor(x, y).red() > 240 and scene.preview_image.pixelColor(x, y).green() < 20
    qtbot.waitUntil(lambda: red(190, 150) and not red(20, 20), timeout=3000)
    assert window.document.project.widgets[0].props["x"] == 10
    assert item.geometry()[:2] == (110, 80)
    assert not window.document.undo_stack.count()
    mouse(view, QEvent.MouseButtonRelease, end, Qt.NoButton)
    assert window.document.project.widgets[0].props["x"] == 110
    assert window.document.undo_stack.count() == 1
    window.document.undo_stack.setClean()


def test_scene_falls_back_when_no_frame_exists(qtbot):
    view = DesignerView(ProjectDocument())
    qtbot.addWidget(view)
    view.designer_scene.set_preview(True, None)
    assert not view.designer_scene.preview_active


def test_window_applies_frame_and_toggle(qtbot, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    window.preview_renderer.stop()
    window.settings = QSettings(str(tmp_path / "settings.ini"), QSettings.IniFormat)
    window.preview_action.setChecked(True)
    project = window.document.project
    width, height = project.display.width, project.display.height
    page_id, scene = project.pages[0].id, window.current_designer().designer_scene
    window._preview_rendered(page_id, b"\0" * (width * height * 2), width, height)
    assert scene.preview_active
    window._preview_rendered(page_id, None, width, height)
    assert not scene.preview_active
    window._preview_rendered(page_id, b"\0" * (width * height * 2), width, height)
    window.preview_action.setChecked(False)
    window._toggle_preview(False)
    assert not scene.preview_active
    window.preview_renderer.stop()
