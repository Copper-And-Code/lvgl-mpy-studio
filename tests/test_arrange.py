from PySide6.QtCore import QPointF, Qt

from lvgl_mpy_studio.ui.designer.scene import DesignerView
from lvgl_mpy_studio.ui.document import ProjectDocument
from lvgl_mpy_studio.ui.main_window import MainWindow
from lvgl_mpy_studio.ui.properties.panel import PropertiesPanel
from helpers import find_item


def arranged(qtbot, boxes):
    document = ProjectDocument()
    for index, (x, y, width, height) in enumerate(boxes):
        document.project.add_widget(document.project.pages[0], "button", {"x": x, "y": y, "width": width, "height": height}, f"b{index}")
    view = DesignerView(document)
    qtbot.addWidget(view)
    view.designer_scene.test_view = view  # qtbot keeps only a weak reference
    return document, view.designer_scene


def props(document, *keys):
    return [tuple(widget.props[key] for key in keys) for widget in document.project.widgets]


def test_align_left_and_bottom_in_one_undo_step(qtbot):
    document, scene = arranged(qtbot, [(10, 10, 50, 20), (40, 60, 30, 40)])
    scene.select_all()
    scene.align_selected("left")
    assert props(document, "x") == [(10,), (10,)]
    scene.select_all()
    scene.align_selected("bottom")
    assert props(document, "y") == [(80,), (60,)]
    assert document.undo_stack.count() == 2
    document.undo_stack.undo()
    assert props(document, "y") == [(10,), (60,)]


def test_align_center_keeps_the_group_centered(qtbot):
    document, scene = arranged(qtbot, [(0, 0, 100, 20), (200, 40, 50, 20)])
    scene.select_all()
    scene.align_selected("center")
    assert props(document, "x") == [(75,), (100,)]


def test_distribute_makes_gaps_equal(qtbot):
    document, scene = arranged(qtbot, [(0, 0, 10, 10), (20, 0, 10, 10), (90, 0, 10, 10)])
    scene.select_all()
    scene.distribute_selected("horizontal")
    assert props(document, "x") == [(0,), (45,), (90,)]


def test_align_compares_positions_on_the_canvas_across_containers(qtbot):
    document = ProjectDocument()
    page = document.project.pages[0]
    panel = document.project.add_widget(page, "panel", {"x": 100, "y": 0, "width": 200, "height": 200}, "box")
    inner = document.project.add_widget(page, "button", {"x": 10, "y": 10, "width": 40, "height": 20}, "inner")
    inner.parentId = panel.id
    outer = document.project.add_widget(page, "button", {"x": 50, "y": 300, "width": 40, "height": 20}, "outer")
    view = DesignerView(document)
    qtbot.addWidget(view)
    scene = view.designer_scene
    scene.test_view = view
    scene.widget_items[inner.id].setSelected(True)
    scene.widget_items[outer.id].setSelected(True)
    scene.align_selected("left")
    by_name = {widget.name: widget for widget in document.project.widgets}
    assert by_name["outer"].props["x"] == 50
    assert by_name["inner"].props["x"] == -50


def test_align_needs_a_selection(qtbot):
    document, scene = arranged(qtbot, [(10, 10, 50, 20), (40, 60, 30, 40)])
    scene.align_selected("left")
    assert not document.undo_stack.count()


def test_duplicate_selects_the_copy_and_keeps_the_clipboard(qtbot):
    document, scene = arranged(qtbot, [(10, 10, 50, 20)])
    document.clipboard = ["precedente"]
    scene.select_all()
    scene.duplicate_selected()
    assert len(document.project.widgets) == 2
    assert scene.selected_names() == [document.project.widgets[1].name]
    assert document.clipboard == ["precedente"]


def test_right_click_selects_and_asks_for_the_menu(qtbot):
    document, scene = arranged(qtbot, [(10, 10, 50, 20)])
    view = scene.test_view
    view.resize(900, 600)
    view.show()
    qtbot.waitExposed(view)
    requests = []
    scene.contextMenuRequested.connect(requests.append)
    from PySide6.QtGui import QContextMenuEvent
    point = view.mapFromScene(QPointF(30, 20))
    view.contextMenuEvent(QContextMenuEvent(QContextMenuEvent.Mouse, point, view.mapToGlobal(point)))
    assert scene.selected_names() == ["b0"]
    assert len(requests) == 1


def test_menus_have_unique_alt_letters_in_both_languages(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    for language in ("en", "it"):
        window.change_language(language)
        letters = [action.text()[action.text().index("&") + 1].lower() for action in window.menuBar().actions()]
        assert len(letters) == len(set(letters))
        titles = [action.text().replace("&", "") for action in window.menuBar().actions()]
        assert ("Arrange" if language == "en" else "Disponi") in titles


def test_select_all_acts_on_the_focused_text(qtbot, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    qtbot.waitExposed(window)
    window.tabs.setCurrentWidget(window.code_panel)
    editor = window.code_panel.editor
    editor.setFocus()
    qtbot.waitUntil(editor.hasFocus, timeout=1000)
    editor.setPlainText("abc")
    window.select_all_action.trigger()
    assert editor.textCursor().selectedText() == "abc"
    window.document.undo_stack.setClean()


def panel_with(qtbot, widget_type, props=None):
    document = ProjectDocument()
    document.project.add_widget(document.project.pages[0], widget_type, props or {}, "w")
    panel = PropertiesPanel(document)
    qtbot.addWidget(panel)
    panel.set_selection(["w"])
    return document, panel


def test_boolean_is_a_checkbox(qtbot):
    document, panel = panel_with(qtbot, "switch")
    item = find_item(panel, "checked")
    assert item.isCheckable()
    item.setCheckState(Qt.Checked)
    assert document.project.widgets[0].props["checked"] is True


def test_color_shows_a_swatch_and_stays_readable(qtbot):
    _document, panel = panel_with(qtbot, "label", {"textColor": "#000000"})
    item = find_item(panel, "textColor")
    assert not item.icon().isNull()
    assert item.background().style() == Qt.NoBrush


def test_number_editor_uses_the_widget_limits(qtbot):
    _document, panel = panel_with(qtbot, "timer")
    descriptor = next(item for item in panel.definitions["timer"]["properties"] if item["name"] == "period")
    item = find_item(panel, "period")
    editor = panel.view.itemDelegate().createEditor(panel.view.viewport(), None, item.index())
    assert editor.minimum() == descriptor["min"]
    assert editor.maximum() == descriptor["max"]


def test_position_comes_in_natural_order(qtbot):
    _document, panel = panel_with(qtbot, "button")
    names = [descriptor["name"] for descriptor in panel._descriptors(panel._widgets())]
    assert names[:4] == ["x", "y", "width", "height"]


def test_alphabetical_order_is_global(qtbot):
    _document, panel = panel_with(qtbot, "button")
    panel.order.setCurrentIndex(1)
    labels = [panel.model.item(row, 0).text().lower() for row in range(panel.model.rowCount())]
    assert labels[1:] == sorted(labels[1:])
