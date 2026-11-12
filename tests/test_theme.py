from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QTextCharFormat
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QDialog, QDockWidget, QToolBar

from lvgl_mpy_studio.ui import theme
from lvgl_mpy_studio.ui.code.editor import PythonHighlighter
from lvgl_mpy_studio.ui.designer.scene import COMPONENTS, Toolbox, WIDGET_ICONS, ToolboxPanel
from lvgl_mpy_studio.core.model import widget_definitions
from lvgl_mpy_studio.ui.main_window import MainWindow


def window_for(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    return window


def test_every_widget_type_has_an_icon(qapp):
    from lvgl_mpy_studio.core.components import BLOCKS
    from lvgl_mpy_studio.ui.designer.scene import widget_icon

    assert (set(widget_definitions()) | set(COMPONENTS)) - set(BLOCKS) | {"buzzer"} == set(WIDGET_ICONS)
    assert not [name for name in WIDGET_ICONS.values() if theme.icon(name).isNull()]
    # A block names its icon in block.json; one it does not name, or that the font lacks, still gets one.
    assert not [name for name in set(widget_definitions()) | set(COMPONENTS) if widget_icon(name).isNull()]
    assert not [block.id for block in BLOCKS.values() if block.origin == "standard" and block.id != "buzzer" and theme.icon(block.manifest["icon"].removeprefix("mdi6.")).isNull()]


def test_missing_icon_font_does_not_break_the_ui(qapp):
    assert theme.icon("nome-inesistente").isNull()


def test_code_colors_are_readable_on_both_backgrounds():
    def contrast(foreground, background):
        def luminance(color):
            channels = [value / 255 for value in (color.red(), color.green(), color.blue())]
            linear = [value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
            return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
        lighter, darker = sorted((luminance(QColor(foreground)), luminance(QColor(background))), reverse=True)
        return (lighter + 0.05) / (darker + 0.05)

    for colors, background in ((theme.LIGHT, "#FFFFFF"), (theme.DARK, "#232323")):
        for color in (colors.keyword, colors.string, colors.comment, colors.number, colors.module):
            assert contrast(color, background) >= 4.5


def test_changing_system_theme_updates_the_open_ide(qtbot, monkeypatch):
    window = window_for(qtbot)
    highlighter = window.code_panel.editor.highlighter
    for colors in (theme.LIGHT, theme.DARK):
        monkeypatch.setattr(theme, "code_colors", lambda current=colors: current)
        window._theme_changed()
        assert highlighter.RULES[0][1].foreground().color().name().upper() == colors.keyword.upper()
    assert not window.document.modified


def test_highlighter_uses_the_current_palette(qapp):
    from PySide6.QtGui import QTextDocument

    highlighter = PythonHighlighter(QTextDocument())
    highlighter.apply_colors(theme.DARK, rehighlight=False)
    assert isinstance(highlighter.string_format, QTextCharFormat)
    assert highlighter.string_format.foreground().color().name().upper() == theme.DARK.string


def test_toolbar_has_main_commands_and_run_label(qtbot):
    window = window_for(qtbot)
    toolbar = window.findChild(QToolBar)
    assert {window.new_action, window.open_action, window.save_action, window.undo_action, window.fit_action} <= set(toolbar.actions())
    assert window.run_button.text() == window.run_action.text()


def test_bottom_panels_are_tabbed(qtbot):
    window = window_for(qtbot)
    docks = {dock.objectName(): dock for dock in window.findChildren(QDockWidget)}
    tabbed = window.tabifiedDockWidgets(docks["outputDock"])
    assert {docks["errorsDock"], docks["componentsDock"], docks["deviceConsoleDock"]} <= set(tabbed)


def test_old_saved_layout_is_ignored(qtbot):
    window = window_for(qtbot)
    old = window.saveState(1)
    assert not window.restoreState(old, window.LAYOUT_VERSION)


def test_toolbox_is_grouped_and_searchable(qtbot):
    panel = ToolboxPanel()
    qtbot.addWidget(panel)
    toolbox = panel.toolbox
    assert isinstance(toolbox, Toolbox)
    headers = [toolbox.item(row) for row in range(toolbox.count()) if not toolbox.item(row).data(Qt.UserRole)]
    assert len(headers) == 9
    assert not headers[0].flags() & Qt.ItemIsSelectable
    panel.search.setText("slid")
    visible = [item.text() for item in toolbox.widget_items() if not item.isHidden()]
    assert visible == ["Slider"]
    assert sum(not header.isHidden() for header in headers) == 1
    panel.search.clear()
    assert all(not item.isHidden() for item in toolbox.widget_items())


def test_dragging_a_category_header_does_nothing(qtbot):
    toolbox = Toolbox()
    qtbot.addWidget(toolbox)
    toolbox.setCurrentRow(0)
    toolbox.startDrag(Qt.CopyAction)


def test_a_new_resolution_fits_the_page_again(qtbot, monkeypatch):
    window = window_for(qtbot)
    window.resize(1200, 800)
    window.show()
    qtbot.waitExposed(window)
    monkeypatch.setattr("lvgl_mpy_studio.ui.resolution.ResizeDialog.exec", lambda self: QDialog.Accepted)
    window.document.execute("page", lambda project: project.pages.append(project.new_page("Second")))
    first, second = (window.designers[page.id][1] for page in window.document.project.pages)
    window.tabs.setCurrentWidget(first)
    window._zoom(1.25)
    zoomed = first.transform().m11()

    def whole(view):
        area = view.mapToScene(view.viewport().rect()).boundingRect()
        display = window.document.project.display
        return area.width() >= display.width and area.height() >= display.height

    window.document.execute("text", lambda project: setattr(project, "projectName", "other"))
    qtbot.wait(50)
    assert first.transform().m11() == zoomed  # a change that is not a resolution keeps the zoom
    assert window.change_resolution(1920, 1080)
    qtbot.waitUntil(lambda: whole(first), timeout=2000)
    assert not whole(second) or second.fitted_size != (1920, 1080)  # the hidden page waits
    window.tabs.setCurrentWidget(second)
    qtbot.waitUntil(lambda: whole(second) and second.fitted_size == (1920, 1080), timeout=2000)
    window.document.undo_stack.undo()
    qtbot.waitUntil(lambda: second.fitted_size != (1920, 1080) and whole(second), timeout=2000)


def test_a_widget_armed_from_the_toolbox_is_placed_once(qtbot):
    window = window_for(qtbot)
    window.show()
    qtbot.waitExposed(window)
    window.document.execute("page", lambda project: project.pages.append(project.new_page("Second")))
    first, second = (window.designers[page.id][1] for page in window.document.project.pages)
    toolbox = window.findChild(Toolbox)
    toolbox.itemDoubleClicked.emit(next(item for item in toolbox.widget_items() if item.data(Qt.UserRole) == "button"))
    assert first.pending_type == second.pending_type == "button"  # the toolbox does not know which page is shown
    window.tabs.setCurrentWidget(second)
    QTest.mouseClick(second.viewport(), Qt.LeftButton, pos=second.mapFromScene(QPointF(60, 60)))
    window.tabs.setCurrentWidget(first)
    QTest.mouseClick(first.viewport(), Qt.LeftButton, pos=first.mapFromScene(QPointF(60, 60)))
    assert [len(page.widgets) for page in window.document.project.pages] == [0, 1]
    assert first.pending_type is None and second.pending_type is None


def test_fit_shows_the_whole_page(qtbot):
    window = window_for(qtbot)
    window.resize(1200, 800)
    window.show()
    qtbot.waitExposed(window)
    window.fit_action.trigger()
    view = window.current_designer()
    display = window.document.project.display
    area = view.mapToScene(view.viewport().rect()).boundingRect()
    assert area.width() >= display.width and area.height() >= display.height


def test_window_frame_is_drawn_only_on_wayland():
    assert theme.frame_margins("wayland") == (1, 0, 1, 1)
    assert theme.frame_margins("wayland-egl") == (1, 0, 1, 1)
    assert theme.frame_margins("xcb") == (0, 0, 0, 0)
    assert theme.frame_margins("windows") == (0, 0, 0, 0)


def test_window_paints_its_border_when_margins_are_set(qtbot):
    window = window_for(qtbot)
    window.setContentsMargins(*theme.frame_margins("wayland"))
    window.resize(900, 620)
    window.show()
    qtbot.waitExposed(window)
    image = window.grab().toImage()
    edge = window.palette().dark().color().name()
    height, width = image.height(), image.width()
    assert image.pixelColor(width - 1, height // 2).name() == edge
    assert image.pixelColor(0, height // 2).name() == edge
    assert image.pixelColor(width // 2, height - 1).name() == edge
