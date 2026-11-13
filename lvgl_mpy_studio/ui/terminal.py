"""The terminal widget of the Device Console: draws a vt.Screen and turns keys into bytes."""

from PySide6.QtCore import QEvent, QPoint, QRect, Qt, QTimer, Signal
from PySide6.QtGui import QAction, QColor, QFont, QFontDatabase, QFontMetrics, QGuiApplication, QPainter
from PySide6.QtWidgets import QAbstractScrollArea, QMenu

from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.core.vt import DEFAULT_BG, DEFAULT_FG, Screen, palette

REPAINT_MS = 16  # output is drawn at most this often, not at every byte

SPECIAL_KEYS = {
    Qt.Key_Up: b"\x1b[A", Qt.Key_Down: b"\x1b[B", Qt.Key_Right: b"\x1b[C", Qt.Key_Left: b"\x1b[D",
    Qt.Key_Home: b"\x1b[H", Qt.Key_End: b"\x1b[F", Qt.Key_Insert: b"\x1b[2~", Qt.Key_Delete: b"\x1b[3~",
    Qt.Key_PageUp: b"\x1b[5~", Qt.Key_PageDown: b"\x1b[6~",
    Qt.Key_Return: b"\r", Qt.Key_Enter: b"\r", Qt.Key_Backspace: b"\x7f", Qt.Key_Tab: b"\t",
    Qt.Key_Backtab: b"\x1b[Z", Qt.Key_Escape: b"\x1b",
    Qt.Key_F1: b"\x1bOP", Qt.Key_F2: b"\x1bOQ", Qt.Key_F3: b"\x1bOR", Qt.Key_F4: b"\x1bOS",
}
CONTROL_SYMBOLS = {Qt.Key_BracketLeft: 0x1B, Qt.Key_Backslash: 0x1C, Qt.Key_BracketRight: 0x1D, Qt.Key_Space: 0x00}


def key_bytes(key, modifiers, text):
    """The bytes xterm sends for a key, or b"" for a key that sends nothing."""
    control = bool(modifiers & Qt.ControlModifier)
    alt = bool(modifiers & Qt.AltModifier)
    if key in SPECIAL_KEYS:
        return SPECIAL_KEYS[key]
    if control and Qt.Key_A <= key <= Qt.Key_Z:
        return bytes([key - Qt.Key_A + 1])
    if control and key in CONTROL_SYMBOLS:
        return bytes([CONTROL_SYMBOLS[key]])
    if text and all(ord(char) >= 32 and ord(char) != 127 for char in text):
        return (b"\x1b" if alt else b"") + text.encode("utf-8")
    return b""


def paste_bytes(text):
    """A pasted text as typed: lines end with Enter, as on a terminal."""
    return text.replace("\r\n", "\n").replace("\n", "\r").encode("utf-8")


class TerminalView(QAbstractScrollArea):
    typed = Signal(bytes)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.screen = Screen()
        self.colors = [QColor(value) for value in palette()]
        self.input_enabled = False
        self._selection = None  # (anchor, end) as (row, column), rows counted from the first of the history
        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAttribute(Qt.WA_InputMethodEnabled, True)
        self.viewport().setCursor(Qt.IBeamCursor)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalScrollBar().valueChanged.connect(self.viewport().update)
        self._repaint = QTimer(self)
        self._repaint.setSingleShot(True)
        self._repaint.setInterval(REPAINT_MS)
        self._repaint.timeout.connect(self._refresh)
        self._measure()

    # ---- Content ----

    def feed(self, text):
        self.screen.feed(text)
        replies = self.screen.take_replies()
        if replies and self.input_enabled:  # answers to 6n and the others go back as typed
            self.typed.emit(replies)
        if not self._repaint.isActive():
            self._repaint.start()

    def clear(self):
        self.screen.clear()
        self._selection = None
        self._refresh()

    def text(self):
        return self.screen.text()

    def _refresh(self):
        bar = self.verticalScrollBar()
        following = bar.value() >= bar.maximum()
        bar.setRange(0, len(self.screen.history))
        bar.setPageStep(self.screen.rows)
        if following:
            bar.setValue(bar.maximum())
        self.viewport().update()

    # ---- Geometry ----

    def _measure(self):
        metrics = QFontMetrics(self.font())
        self.cell_w = max(1, metrics.horizontalAdvance("M"))
        self.cell_h = max(1, metrics.height())
        self.ascent = metrics.ascent()

    def changeEvent(self, event):
        if event.type() == QEvent.FontChange:
            self._measure()
            self._fit()
        super().changeEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._fit()

    def _fit(self):
        size = self.viewport().size()
        self.screen.resize(size.width() // self.cell_w, size.height() // self.cell_h)
        self._refresh()

    def _cell_at(self, point):
        row = self.verticalScrollBar().value() + max(0, point.y()) // self.cell_h
        column = max(0, min(self.screen.cols - 1, point.x() // self.cell_w))
        return row, column

    def _rows(self):
        return list(self.screen.history) + self.screen.lines

    # ---- Drawing ----

    def _color(self, index):
        """The two defaults follow the theme; reverse video swaps them like any other colour."""
        if index == DEFAULT_FG:
            return self.palette().text().color()
        if index == DEFAULT_BG:
            return self.palette().base().color()
        return self.colors[index]

    def _selected(self, row, column):
        if self._selection is None:
            return False
        start, end = sorted(self._selection)
        return start <= (row, column) <= end

    def paintEvent(self, _event):
        painter = QPainter(self.viewport())
        painter.fillRect(self.viewport().rect(), self.palette().base())
        normal, bold = QFont(self.font()), QFont(self.font())
        bold.setBold(True)
        rows = self._rows()
        first = self.verticalScrollBar().value()
        highlight, highlighted = self.palette().highlight().color(), self.palette().highlightedText().color()
        for line in range(self.screen.rows):
            index = first + line
            if index >= len(rows):
                break
            y = line * self.cell_h
            for column, (char, fg, bg, heavy) in enumerate(rows[index]):
                x = column * self.cell_w
                if self._selected(index, column):
                    back, front = highlight, highlighted
                else:
                    back, front = self._color(bg), self._color(fg)
                if bg != DEFAULT_BG or self._selected(index, column):
                    painter.fillRect(x, y, self.cell_w, self.cell_h, back)
                if char != " ":
                    painter.setFont(bold if heavy else normal)
                    painter.setPen(front)
                    painter.drawText(QPoint(x, y + self.ascent), char)
        cursor_row = len(self.screen.history) + self.screen.y - first
        if self.screen.cursor_on and self.input_enabled and 0 <= cursor_row < self.screen.rows:
            rect = QRect(self.screen.x * self.cell_w, cursor_row * self.cell_h, self.cell_w, self.cell_h)
            painter.setCompositionMode(QPainter.RasterOp_SourceXorDestination)
            if self.hasFocus():
                painter.fillRect(rect, QColor(255, 255, 255))
            else:
                painter.setPen(QColor(255, 255, 255))
                painter.drawRect(rect.adjusted(0, 0, -1, -1))

    # ---- Keyboard ----

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Tab, Qt.Key_Backtab):
            self.keyPressEvent(event)  # Tab belongs to the program, not to the focus chain
            return True
        if event.type() == QEvent.ShortcutOverride and self.input_enabled and key_bytes(event.key(), event.modifiers(), event.text()):
            event.accept()  # Ctrl-S, Ctrl-Z and the others go to the board, not to the menus
            return True
        return super().event(event)

    def keyPressEvent(self, event):
        shifted_control = event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.ShiftModifier
        if shifted_control and event.key() == Qt.Key_C:
            self.copy()
            return
        if shifted_control and event.key() == Qt.Key_V:
            self.paste()
            return
        data = key_bytes(event.key(), event.modifiers(), event.text())
        if not data:
            super().keyPressEvent(event)
            return
        if self.input_enabled:
            self._selection = None
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
            self.typed.emit(data)

    def inputMethodEvent(self, event):
        if event.commitString() and self.input_enabled:
            self.typed.emit(event.commitString().encode("utf-8"))

    # ---- Mouse and clipboard ----

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            cell = self._cell_at(event.position().toPoint())
            self._selection = (cell, cell)
            self.viewport().update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._selection is not None and event.buttons() & Qt.LeftButton:
            self._selection = (self._selection[0], self._cell_at(event.position().toPoint()))
            self.viewport().update()

    def mouseReleaseEvent(self, event):
        if self._selection is not None and self._selection[0] == self._selection[1]:
            self._selection = None  # a click is not a selection
            self.viewport().update()
        super().mouseReleaseEvent(event)

    def selected_text(self):
        if self._selection is None:
            return ""
        (row0, col0), (row1, col1) = sorted(self._selection)
        rows = self._rows()
        lines = []
        for row in range(row0, min(row1, len(rows) - 1) + 1):
            start = col0 if row == row0 else 0
            end = col1 + 1 if row == row1 else self.screen.cols
            lines.append("".join(cell[0] for cell in rows[row][start:end]).rstrip())
        return "\n".join(lines)

    def select_all(self):
        rows = self._rows()
        self._selection = ((0, 0), (len(rows) - 1, self.screen.cols - 1))
        self.viewport().update()

    def copy(self):
        text = self.selected_text()
        if text:
            QGuiApplication.clipboard().setText(text)

    def paste(self):
        text = QGuiApplication.clipboard().text()
        if text and self.input_enabled:
            self.typed.emit(paste_bytes(text))

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        for label, slot, enabled in (
            (tr("Copy"), self.copy, bool(self.selected_text())),
            (tr("Paste"), self.paste, self.input_enabled),
            (tr("Select All"), self.select_all, True),
            (tr("Clear"), self.clear, True),
        ):
            action = QAction(label, menu)
            action.setEnabled(enabled)
            action.triggered.connect(slot)
            menu.addAction(action)
        menu.exec(event.globalPos())
