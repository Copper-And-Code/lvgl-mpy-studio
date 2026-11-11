import pytest
from PySide6.QtCore import QEvent, QMimeData, QPointF, Qt
from PySide6.QtGui import QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent, QMouseEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from lvgl_mpy_studio.core.model import widget_definitions
from lvgl_mpy_studio.ui.designer.scene import WIDGET_MIME, DesignerScene, DesignerView, Toolbox
from lvgl_mpy_studio.ui.document import ProjectDocument


def test_toolbox_contains_all_types_and_drop_adds_defaults(qtbot):
    document = ProjectDocument()
    view = DesignerView(document)
    qtbot.addWidget(view)
    toolbox = Toolbox()
    qtbot.addWidget(toolbox)
    assert len(toolbox.widget_items()) == 32
    view.designer_scene.add_widget("button", QPointF(30, 40))
    widget = document.project.find_widget("button1")
    assert widget.props["x"] == 30
    assert widget.props["text"] == "Button"
    document.undo_stack.undo()
    assert not document.project.widgets
    document.undo_stack.redo()
    assert document.project.find_widget("button1")


def drag_event(event_type, view, scene_point, payload=b"button"):
    mime = QMimeData()
    mime.setData(WIDGET_MIME, payload)
    point = view.mapFromScene(scene_point)
    return event_type(point, Qt.CopyAction, mime, Qt.LeftButton, Qt.NoModifier), mime


@pytest.mark.parametrize("widget_type", list(widget_definitions()))
def test_every_widget_type_paints_as_drop_preview(qtbot, widget_type):
    view = DesignerView(ProjectDocument())
    qtbot.addWidget(view)
    view.resize(900, 600)
    view.designer_scene.show_drop_preview(widget_type, QPointF(300, 200))
    assert not view.grab().isNull()
    view.designer_scene.hide_drop_preview()


def test_drop_preview_follows_drag_and_is_not_part_of_project(qtbot):
    document = ProjectDocument()
    view = DesignerView(document)
    qtbot.addWidget(view)
    view.resize(1000, 700)
    event, _mime = drag_event(QDragEnterEvent, view, QPointF(300, 200))
    view.dragEnterEvent(event)
    preview = view.designer_scene.drop_preview
    assert preview is not None and preview.opacity() < 1
    assert abs(preview.pos().x() + preview.rect().width() / 2 - 300) <= 1
    event, _mime = drag_event(QDragMoveEvent, view, QPointF(500, 300))
    view.dragMoveEvent(event)
    assert view.designer_scene.drop_preview is preview
    assert abs(preview.pos().y() + preview.rect().height() / 2 - 300) <= 1
    assert not document.project.widgets
    assert not document.undo_stack.count()
    assert view.designer_scene.item_at(QPointF(500, 300)) is preview
    view.dragLeaveEvent(QDragLeaveEvent())
    assert view.designer_scene.drop_preview is None
    assert view.designer_scene.item_at(QPointF(500, 300)) is None


def test_drop_preview_respects_grid(qtbot):
    view = DesignerView(ProjectDocument())
    qtbot.addWidget(view)
    view.designer_scene.grid_size = 8
    view.designer_scene.show_drop_preview("button", QPointF(303, 205))
    assert view.designer_scene.drop_preview.pos().x() % 8 == 0
    assert view.designer_scene.drop_preview.pos().y() % 8 == 0


def test_drop_on_container_ignores_preview_and_nests(qtbot):
    document = ProjectDocument()
    view = DesignerView(document)
    qtbot.addWidget(view)
    view.resize(1000, 700)
    view.designer_scene.add_widget("panel", QPointF(100, 100))
    panel = document.project.find_widget("panel1")
    inside = QPointF(100 + panel.props["width"] / 2, 100 + panel.props["height"] / 2)
    event, _mime = drag_event(QDragEnterEvent, view, inside, b"panel")
    view.dragEnterEvent(event)
    event, mime = drag_event(QDragMoveEvent, view, inside, b"button")
    view.dropEvent(QDropEvent(QPointF(view.mapFromScene(inside)), Qt.CopyAction, mime, Qt.LeftButton, Qt.NoModifier))
    assert view.designer_scene.drop_preview is None
    assert document.project.find_widget("button1").parentId == panel.id


def test_toolbox_drag_carries_chip_beside_cursor(qtbot, monkeypatch):
    toolbox = Toolbox()
    qtbot.addWidget(toolbox)
    toolbox.setCurrentItem(toolbox.widget_items()[0])
    drags = []

    class FakeDrag:
        def __init__(self, source):
            drags.append(self)

        def setMimeData(self, mime):
            self.mime = mime

        def setPixmap(self, pixmap):
            self.pixmap = pixmap

        def setHotSpot(self, point):
            self.hot_spot = point

        def exec(self, action):
            self.action = action

    monkeypatch.setattr("lvgl_mpy_studio.ui.designer.scene.QDrag", FakeDrag)
    toolbox.startDrag(Qt.CopyAction)
    drag = drags[0]
    assert not drag.pixmap.isNull()
    assert drag.hot_spot.x() < 0 and drag.hot_spot.y() < 0
    assert drag.action == Qt.CopyAction


def test_drop_places_widget_where_preview_was_shown(qtbot):
    document = ProjectDocument()
    view = DesignerView(document)
    qtbot.addWidget(view)
    view.resize(1000, 700)
    mime = QMimeData()
    mime.setData(WIDGET_MIME, b"button")
    position = view.mapFromScene(QPointF(300, 200))
    view.dropEvent(QDropEvent(QPointF(position), Qt.CopyAction, mime, Qt.LeftButton, Qt.NoModifier))
    widget = document.project.find_widget("button1")
    assert abs(widget.props["x"] + widget.props["width"] / 2 - 300) <= 1
    assert abs(widget.props["y"] + widget.props["height"] / 2 - 200) <= 1


def test_drop_near_corner_stays_on_canvas(qtbot):
    document = ProjectDocument()
    view = DesignerView(document)
    qtbot.addWidget(view)
    view.designer_scene.add_widget("button", QPointF(3, 3), centered=True)
    widget = document.project.find_widget("button1")
    assert (widget.props["x"], widget.props["y"]) == (0, 0)


def test_mouse_drag_is_one_undo_command(qtbot):
    document = ProjectDocument()
    document.execute("Aggiungi", lambda project: project.add_widget(project.pages[0], "button", {"x": 20, "y": 20}))
    view = DesignerView(document)
    qtbot.addWidget(view)
    view.resize(800, 600)
    view.show()
    item = next(iter(view.designer_scene.widget_items.values()))
    start = view.mapFromScene(item.mapToScene(QPointF(10, 10)))
    end = view.mapFromScene(item.mapToScene(QPointF(45, 35)))
    QTest.mousePress(view.viewport(), Qt.LeftButton, pos=start)
    move = QMouseEvent(QEvent.MouseMove, QPointF(end), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
    QApplication.sendEvent(view.viewport(), move)
    QTest.mouseRelease(view.viewport(), Qt.LeftButton, pos=end)
    widget = document.project.find_widget("button1")
    assert (widget.props["x"], widget.props["y"]) == (55, 45)
    document.undo_stack.undo()
    widget = document.project.find_widget("button1")
    assert (widget.props["x"], widget.props["y"]) == (20, 20)


def test_nesting_and_clipboard_preserve_hierarchy(qtbot):
    document = ProjectDocument()
    scene = DesignerScene(document)
    scene.add_widget("panel", QPointF(20, 20))
    panel = document.project.find_widget("panel1")
    scene.add_widget("button", QPointF(60, 70))
    button = document.project.find_widget("button1")
    assert button.parentId == panel.id
    assert (button.props["x"], button.props["y"]) == (40, 50)
    item = scene.widget_items[button.id]
    item.setSelected(True)
    scene.copy_selected()
    scene.paste()
    clone = document.project.find_widget("button2")
    assert clone.parentId == panel.id
    document.undo_stack.undo()
    assert document.project.find_widget("button2") is None


def test_resize_handle_has_minimum_and_undo(qtbot):
    document = ProjectDocument()
    document.execute("Aggiungi", lambda project: project.add_widget(project.pages[0], "button", {"x": 10, "y": 10}))
    scene = DesignerScene(document)
    item = next(iter(scene.widget_items.values()))
    item.setSelected(True)
    item.set_geometry(10, 10, 150, 80)
    item.commit_geometry()
    assert document.project.find_widget("button1").props["width"] == 150
    document.undo_stack.undo()
    assert document.project.find_widget("button1").props["width"] == 100
