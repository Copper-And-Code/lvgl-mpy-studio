"""Theme of the IDE: it follows the system, light or dark, without fixed colours in the panels."""

from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QObject, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QGuiApplication, QIcon, QImageReader, QPixmap
from PySide6.QtWidgets import QApplication

WARNING = "#B26A00"
ERROR = "#D32F2F"


@dataclass(frozen=True)
class CodeColors:
    keyword: str
    string: str
    comment: str
    number: str
    module: str
    error: str


LIGHT = CodeColors("#0033B3", "#067D17", "#6E7781", "#7A3E9D", "#00707A", "#D00000")
DARK = CodeColors("#6CB6FF", "#8DDB8C", "#8B949E", "#D2A8FF", "#56D4DD", "#FF7B72")

STYLE = """
QMainWindow::separator { width: 4px; height: 4px; }
QToolBar { border: none; spacing: 2px; padding: 3px 6px; }
QToolButton { padding: 4px; border-radius: 4px; }
QToolButton:hover { background: palette(midlight); }
QToolButton:checked { background: palette(mid); }
QToolButton#runButton { background: #2E7D32; color: white; font-weight: bold; padding: 4px 12px; }
QToolButton#runButton:hover { background: #388E3C; }
QToolButton#runButton:disabled { background: palette(mid); color: palette(midlight); }
QDockWidget::title { padding: 4px 6px; }
QTabBar::tab { padding: 5px 12px; }
QStatusBar QLabel { padding: 0 6px; }
QListWidget#componentTray::item { padding: 3px 8px; }
"""


# Only this font: the others included in QtAwesome have different licences and are not needed.
ICON_FONT = ("mdi6", "materialdesignicons6-webfont-6.9.96.ttf", "materialdesignicons6-webfont-charmap-6.9.96.json")
_icon_font = None


def error_color():
    return "#FF8A80" if is_dark() else ERROR


def frame_margins(platform):
    """Window border: left, top, right, bottom.

    On Wayland Qt draws the frame and the Adwaita plugin leaves the sides and bottom without a border.
    """
    return (1, 0, 1, 1) if platform.startswith("wayland") else (0, 0, 0, 0)


def is_dark():
    hints = QGuiApplication.styleHints()
    return hints.colorScheme() == Qt.ColorScheme.Dark


def code_colors():
    return DARK if is_dark() else LIGHT


def icon(name, color=None):
    """Material Design icon; without fonts it stays empty, the action keeps its text."""
    global _icon_font
    try:
        if _icon_font is None:
            from qtawesome.iconic_font import IconicFont

            _icon_font = IconicFont(ICON_FONT)
        return _icon_font.icon(f"mdi6.{name}", color=color or QApplication.palette().windowText().color().name())
    except Exception:
        return QIcon()


def app_icon():
    """The icon of the windows, with every size stored in the file."""
    result = QIcon()
    reader = QImageReader(str(Path(__file__).parent.parent / "icon.ico"))
    for index in range(reader.imageCount()):
        reader.jumpToImage(index)
        result.addPixmap(QPixmap.fromImage(reader.read()))
    return result


class Theme(QObject):
    changed = Signal()

    def __init__(self, app):
        super().__init__(app)
        app.setStyle("Fusion")
        app.setStyleSheet(STYLE)
        # The palette can update after the signal: it is redrawn at the next turn.
        app.styleHints().colorSchemeChanged.connect(lambda _scheme: QTimer.singleShot(0, self.changed.emit))


def install(app):
    existing = app.findChild(Theme)
    return existing or Theme(app)


def canvas_color():
    return QColor("#202020" if is_dark() else "#D9DCE1")
