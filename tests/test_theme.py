from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QTextCharFormat
from PySide6.QtWidgets import QDockWidget, QToolBar

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
    assert set(widget_definitions()) | set(COMPONENTS) == set(WIDGET_ICONS)
    assert not [name for name in WIDGET_ICONS.values() if theme.icon(name).isNull()]


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
    assert len(headers) == 8
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
