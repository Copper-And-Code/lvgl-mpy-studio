import json
import re
import tempfile
from pathlib import Path

from PySide6.QtCore import QRect, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QSyntaxHighlighter, QTextCharFormat, QTextCursor, QKeyEvent
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPlainTextEdit, QPushButton, QSplitter, QTextEdit, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

from lvgl_mpy_studio.build.compiler import CompileError, compile_python, map_error
from lvgl_mpy_studio.core.actions import CURSOR, SCREEN_ACTIONS, actions_for, method_entries, module_actions, page_actions
from lvgl_mpy_studio.core.components import is_component, methods_for
from lvgl_mpy_studio.core.events import PAGE_EVENTS, default_event, events_for, handler_name
from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.core.modules import set_module_source
from lvgl_mpy_studio.gen.gen_python import page_constant
from lvgl_mpy_studio.ui.theme import code_colors, error_color
from lvgl_mpy_studio.gen.project_gen import generate_project


def monospace_font():
    font = QFont()
    font.setFamilies(["Cascadia Mono", "Consolas", "Monospace"])
    font.setPointSize(10)
    return font


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_width(), 0)

    def paintEvent(self, event):
        self.editor.paint_line_numbers(event)


KEYWORDS = ("and", "as", "assert", "async", "await", "break", "class", "continue", "def", "del", "elif", "else", "except", "False", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "None", "nonlocal", "not", "or", "pass", "raise", "return", "True", "try", "while", "with", "yield")


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.apply_colors(code_colors(), rehighlight=False)

    def apply_colors(self, colors, rehighlight=True):
        def text_format(color, bold=False, italic=False):
            result = QTextCharFormat()
            result.setForeground(QColor(color))
            if bold:
                result.setFontWeight(QFont.Bold)
            result.setFontItalic(italic)
            return result

        self.string_format = text_format(colors.string)
        keyword = text_format(colors.keyword, bold=True)
        self.RULES = [(re.compile(rf"\b{word}\b"), keyword) for word in KEYWORDS]
        self.RULES.extend([
            (re.compile(r"\b0[xX][0-9a-fA-F]+\b|\b\d+(?:\.\d+)?\b"), text_format(colors.number)),
            (re.compile(r"\b(?:ui|lv)\b"), text_format(colors.module, bold=True)),
            (re.compile(r"#[^\n]*"), text_format(colors.comment, italic=True)),
            (re.compile(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\""), self.string_format),
        ])
        if rehighlight:
            self.rehighlight()

    def highlightBlock(self, text):
        for pattern, format_ in self.RULES:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), format_)
        self.setCurrentBlockState(0)
        for state, delimiter in ((1, '"""'), (2, "'''")):
            start = 0
            if self.previousBlockState() == state:
                end = text.find(delimiter)
                if end < 0:
                    self.setFormat(0, len(text), self.string_format)
                    self.setCurrentBlockState(state)
                    break
                self.setFormat(0, end + 3, self.string_format)
                start = end + 3
            while True:
                begin = text.find(delimiter, start)
                if begin < 0:
                    break
                end = text.find(delimiter, begin + 3)
                if end < 0:
                    self.setFormat(begin, len(text) - begin, self.string_format)
                    self.setCurrentBlockState(state)
                    break
                self.setFormat(begin, end + 3 - begin, self.string_format)
                start = end + 3


class SuggestionList(QListWidget):
    """List of suggestions inside the editor.

    It is a child widget: on Wayland the QCompleter popup is refused and does not appear.
    """

    MAX_ROWS = 8

    def __init__(self, editor):
        super().__init__(editor.viewport())
        self.editor = editor
        self.setFocusPolicy(Qt.NoFocus)
        self.itemClicked.connect(lambda item: editor.insert_completion(item.text()))
        self.hide()

    def show_at(self, names, rect):
        self.clear()
        self.addItems(names)
        self.setCurrentRow(0)
        row_height = self.sizeHintForRow(0)
        height = row_height * min(self.MAX_ROWS, len(names)) + 2 * self.frameWidth()
        area = self.parentWidget().rect()
        width = min(area.width(), self.sizeHintForColumn(0) + self.verticalScrollBar().sizeHint().width() + 2 * self.frameWidth())
        x = max(0, min(rect.left(), area.width() - width))
        y = rect.bottom() + 2 if rect.bottom() + 2 + height <= area.height() else max(0, rect.top() - height - 2)
        self.setGeometry(x, y, width, height)
        self.show()
        self.raise_()

    def move_selection(self, step):
        self.setCurrentRow(max(0, min(self.count() - 1, self.currentRow() + step)))


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(monospace_font())
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(" "))
        self.line_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_width()
        self.highlighter = PythonHighlighter(self.document())
        self.suggestions = SuggestionList(self)
        self.completion_provider = lambda text: []
        self._insertions = {}
        self.textChanged.connect(self.update_completion)

    def line_number_width(self):
        return 12 + self.fontMetrics().horizontalAdvance("9") * max(2, len(str(self.blockCount())))

    def update_line_number_width(self):
        self.setViewportMargins(self.line_number_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_area.scroll(0, dy)
        else:
            self.line_area.update(0, rect.y(), self.line_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_width()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        rect = self.contentsRect()
        self.line_area.setGeometry(QRect(rect.left(), rect.top(), self.line_number_width(), rect.height()))

    def paint_line_numbers(self, event):
        painter = QPainter(self.line_area)
        painter.fillRect(event.rect(), self.palette().alternateBase())
        block = self.firstVisibleBlock()
        number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(self.palette().placeholderText().color())
                painter.drawText(0, top, self.line_area.width() - 5, self.fontMetrics().height(), Qt.AlignRight, str(number + 1))
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            number += 1

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space and event.modifiers() & Qt.ControlModifier:
            self.update_completion(forced=True)
            return
        if self.suggestions.isVisible():
            if event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_PageUp, Qt.Key_PageDown):
                step = {Qt.Key_Up: -1, Qt.Key_Down: 1, Qt.Key_PageUp: -SuggestionList.MAX_ROWS, Qt.Key_PageDown: SuggestionList.MAX_ROWS}[event.key()]
                self.suggestions.move_selection(step)
                return
            if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab):
                self.insert_completion(self.suggestions.currentItem().text())
                return
            if event.key() == Qt.Key_Escape:
                self.suggestions.hide()
                return
        if event.key() == Qt.Key_Tab:
            self.insertPlainText("    ")
            return
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            cursor = self.textCursor()
            line = cursor.block().text()[:cursor.positionInBlock()]
            indent = re.match(r"\s*", line).group()
            if line.rstrip().endswith(":"):
                indent += "    "
            super().keyPressEvent(event)
            self.insertPlainText(indent)
            return
        super().keyPressEvent(event)

    def insert_completion(self, completion):
        cursor = self.textCursor()
        prefix = re.search(r"[A-Za-z_][A-Za-z0-9_]*$", cursor.block().text()[:cursor.positionInBlock()])
        length = len(prefix.group()) if prefix else 0
        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, length)
        self.setTextCursor(cursor)
        self.suggestions.hide()
        self.insert_code(self._insertions.get(completion, completion))

    def insert_code(self, code):
        """Insert the code and leave the cursor where it must be completed."""
        cursor = self.textCursor()
        cursor.insertText(code.replace(CURSOR, ""))
        if CURSOR in code:
            cursor.setPosition(cursor.position() - (len(code) - code.index(CURSOR) - 1))
        self.setTextCursor(cursor)
        if code.endswith("."):
            QTimer.singleShot(0, self.update_completion)

    @staticmethod
    def _inside_text(line):
        return "#" in line or line.count('"') % 2 == 1 or line.count("'") % 2 == 1

    def update_completion(self, forced=False):
        text = self.textCursor().block().text()[:self.textCursor().positionInBlock()]
        match = re.search(r"([A-Za-z_][A-Za-z0-9_.]*)$", text)
        qualified = match.group(1) if match else ""
        if self._inside_text(text) or (not forced and ("." not in qualified and len(qualified) < 2)):
            self.suggestions.hide()
            return
        prefix = qualified.rsplit(".", 1)[-1].lower()
        self._insertions = {}
        names = []
        for choice in self.completion_provider(qualified):
            label, code = choice if isinstance(choice, tuple) else (choice, choice)
            if label not in self._insertions and label.lower().startswith(prefix):
                names.append(label)
                self._insertions[label] = code
        if not names or names == [prefix]:
            self.suggestions.hide()
            return
        self.suggestions.show_at(names, self.cursorRect())

    def focusOutEvent(self, event):
        self.suggestions.hide()
        super().focusOutEvent(event)

    def show_errors(self, lines):
        selections = []
        for line in lines:
            block = self.document().findBlockByNumber(max(0, line - 1))
            if not block.isValid():
                continue
            selection = QTextEditExtraSelection()
            selection.cursor = QTextCursor(block)
            selection.format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
            selection.format.setUnderlineColor(QColor(code_colors().error))
            selection.format.setBackground(QColor(255, 0, 0, 20))
            selection.format.setProperty(QTextCharFormat.FullWidthSelection, True)
            selections.append(selection)
        self.setExtraSelections(selections)


class QTextEditExtraSelection(QTextEdit.ExtraSelection):
    pass


class ActionHelper(QWidget):
    """List what can be done with each object, without knowing the LVGL API."""

    insertRequested = Signal(str)

    def __init__(self, document, parent=None):
        super().__init__(parent)
        self.document = document
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(tr("What do you want to do?"))
        layout.addWidget(self.title)
        self.search = QLineEdit()
        self.search.setPlaceholderText(tr("Search an object or action"))
        self.search.textChanged.connect(self._filter)
        layout.addWidget(self.search)
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemActivated.connect(self._activated)
        layout.addWidget(self.tree, 1)
        self.hint = QLabel(tr("Double-click to insert the code"))
        self.hint.setWordWrap(True)
        layout.addWidget(self.hint)

    def _add_group(self, title, actions):
        group = QTreeWidgetItem(self.tree, [title])
        for label, code in actions:
            shown = code.replace(CURSOR, "")
            item = QTreeWidgetItem(group, [tr(label)])
            item.setData(0, Qt.UserRole, code)
            item.setToolTip(0, shown)
        return group

    def rebuild(self, current=None, open_module=None):
        expanded = {self.tree.topLevelItem(index).text(0) for index in range(self.tree.topLevelItemCount()) if self.tree.topLevelItem(index).isExpanded()}
        self.tree.clear()
        project = self.document.project
        for widget in project.widgets:
            group = self._add_group(f"{widget.name} ({widget.type})", actions_for(widget.type, widget.name))
            group.setExpanded(group.text(0) in expanded or widget.name == current)
        # Like components: the functions of the modules, except those of the open module, which has them at hand.
        for module in project.modules:
            if module.id == open_module:  # the open module: its functions, without the name in front
                group = self._add_group(tr("This module: {name}", name=f"{module.name}.py"), module_actions(module, own=True))
                group.setExpanded(True)
            else:
                group = self._add_group(tr("Module: {name}", name=f"{module.name}.py"), module_actions(module))
                group.setExpanded(group.text(0) in expanded)
        for page in project.pages:
            self._add_group(tr("Page: {name}", name=page.name), page_actions(page_constant(page.name)))
        self._add_group(tr("Screen"), SCREEN_ACTIONS)
        self._filter(self.search.text())

    def _filter(self, text):
        needle = text.strip().lower()
        for index in range(self.tree.topLevelItemCount()):
            group = self.tree.topLevelItem(index)
            group_match = needle in group.text(0).lower()
            visible = 0
            for child_index in range(group.childCount()):
                child = group.child(child_index)
                shown = not needle or group_match or needle in child.text(0).lower()
                child.setHidden(not shown)
                visible += shown
            group.setHidden(not visible)
            if needle and visible:
                group.setExpanded(True)

    def _activated(self, item):
        code = item.data(0, Qt.UserRole)
        if code:
            self.insertRequested.emit(code)


class CodePanel(QWidget):
    """One editor for the general code, the handlers and the Python modules.

    current says what is open: ("module", "module") the general code, ("handler", name) a
    handler, ("pymodule", id) a module, followed by id because the name changes on rename.
    """

    syntaxChecked = Signal(list)
    stopRequested = Signal()

    def __init__(self, document, parent=None):
        super().__init__(parent)
        self.document = document
        self.current = ("module", "module")
        self._unsaved_handler = None
        self._loading = False
        self._edit_session = 0
        self._errors = []
        layout = QVBoxLayout(self)
        selectors = QHBoxLayout()
        self.object_combo = QComboBox()
        self.object_combo.setProperty("_lvgl_dynamic_items", True)
        self.procedure_combo = QComboBox()
        self.procedure_combo.setProperty("_lvgl_dynamic_items", True)
        selectors.addWidget(QLabel(tr("Object")))
        selectors.addWidget(self.object_combo, 1)
        selectors.addWidget(QLabel(tr("Procedure")))
        selectors.addWidget(self.procedure_combo, 1)
        layout.addLayout(selectors)
        self.signature = QLabel()
        self.signature.setFont(monospace_font())
        self.signature.setStyleSheet("background: palette(alternate-base); padding: 5px")
        layout.addWidget(self.signature)
        # While the app runs the code is read-only: it must be said here, where one tries to type.
        self.running_bar = QWidget()
        bar = QHBoxLayout(self.running_bar)
        bar.setContentsMargins(5, 2, 5, 2)
        self.running_label = QLabel(tr("The simulator is running: the code can be read but not changed."))
        self.running_label.setWordWrap(True)
        bar.addWidget(self.running_label, 1)
        self.stop_button = QPushButton(tr("Stop and Edit"))
        self.stop_button.clicked.connect(lambda: self.stopRequested.emit())
        bar.addWidget(self.stop_button)
        self.running_bar.setStyleSheet("background: palette(alternate-base)")
        self.running_bar.hide()
        layout.addWidget(self.running_bar)
        self.editor = CodeEditor()
        self.editor.setPlaceholderText(tr("Type an object name, for example label1, or pick an action on the right. Ctrl+Space shows suggestions."))
        self.helper = ActionHelper(document)
        self.helper.insertRequested.connect(self.insert_action)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.helper)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter, 1)
        # A module is a file of its own: it does not get ui and lv as handlers do, and whoever uses it must import it.
        self.module_hint = QLabel(tr("A module does not get ui and lv the way handlers do: import them at the top, with import ui and import lvgl as lv. From handlers and the general code, use it with import followed by its name."))
        self.module_hint.setWordWrap(True)
        self.module_hint.setStyleSheet("color: palette(placeholder-text)")
        self.module_hint.hide()
        layout.addWidget(self.module_hint)
        self.error = QLabel()
        self.apply_error_color()
        self.error.hide()
        layout.addWidget(self.error)
        self.object_combo.currentIndexChanged.connect(self._object_changed)
        self.procedure_combo.currentIndexChanged.connect(self._procedure_changed)
        self.editor.textChanged.connect(self._text_changed)
        self.editor.completion_provider = self._entries
        self.document.reset.connect(self.populate)
        self.document.code_changed.connect(self._sync_text)
        self.check_timer = QTimer(self)
        self.check_timer.setSingleShot(True)
        self.check_timer.setInterval(500)
        self.check_timer.timeout.connect(self.check_syntax)
        # While a module is typed its functions change: the help follows them, without rebuilding at every key.
        self.helper_timer = QTimer(self)
        self.helper_timer.setSingleShot(True)
        self.helper_timer.setInterval(400)
        self.helper_timer.timeout.connect(self._rebuild_helper)
        self.populate()

    def apply_error_color(self):
        self.error.setStyleSheet(f"color: {error_color()}")

    def insert_action(self, code):
        if self.document.read_only:
            return
        self.editor.setFocus()
        cursor = self.editor.textCursor()
        if cursor.block().text().strip():
            cursor.movePosition(QTextCursor.EndOfBlock)
            cursor.insertText("\n" + re.match(r"\s*", cursor.block().text()).group())
            self.editor.setTextCursor(cursor)
        self.editor.insert_code(code)

    def _entries(self, qualified):
        project = self.document.project
        parts = qualified.split(".")
        if len(parts) == 1:
            needle = qualified.lower()
            return [(name, f"ui.{name}.") for name in sorted(project.used_names) if name.lower().startswith(needle)]
        if parts[0] == "ui" and len(parts) == 3 and project.find_widget(parts[1]):
            widget = project.find_widget(parts[1])
            suggested = method_entries(widget.type, widget.name)
            known = {label.split(" — ")[0] for label, _code in suggested}
            return suggested + sorted(name for name in set(self._completions(qualified)) if name not in known)
        return sorted(set(self._completions(qualified)))

    def _find_object(self, data):
        return next((index for index in range(self.object_combo.count()) if self.object_combo.itemData(index) == data), -1)

    def retranslate(self):
        self.populate()
        self._rebuild_helper()

    def populate(self):
        if self._loading:
            return
        current = self.current
        if current[0] == "handler":
            handler = self.document.project.code.handlers.get(current[1])
            if handler:
                if self.document.project.find_widget(handler.widget):
                    current = ("widget", handler.widget)
                elif handler.widget in {page.name for page in self.document.project.pages}:
                    current = ("page", handler.widget)
                else:
                    current = ("orphan", current[1])
            elif self._unsaved_handler and self._unsaved_handler[2] == current[1]:
                current = self._unsaved_handler[:2]
        self._loading = True
        self.object_combo.clear()
        self.object_combo.addItem(tr("(General)"), ("module", "module"))
        for module in self.document.project.modules:
            self.object_combo.addItem(tr("Module: {name}", name=f"{module.name}.py"), ("pymodule", module.id))
        for page in self.document.project.pages:
            self.object_combo.addItem(tr("Page: {name}", name=page.name), ("page", page.name))
        for widget in self.document.project.widgets:
            if events_for(widget.type):
                self.object_combo.addItem(f"{widget.name} ({widget.type})", ("widget", widget.name))
        page_names = {page.name for page in self.document.project.pages}
        for name, handler in self.document.project.code.handlers.items():
            if not self.document.project.find_widget(handler.widget) and handler.widget not in page_names:
                self.object_combo.addItem(tr("Orphan: {name}", name=name), ("orphan", name))
        index = self._find_object(current)
        self.object_combo.setCurrentIndex(max(0, index))
        self._loading = False
        self._load_object()
        self._rebuild_helper()

    def _rebuild_helper(self):
        kind, name = self.object_combo.currentData() or (None, None)
        self.helper.rebuild(name if kind == "widget" else None, open_module=name if kind == "pymodule" else None)

    def _object_changed(self):
        if not self._loading:
            self._load_object()
            self._rebuild_helper()

    def _load_object(self):
        data = self.object_combo.currentData()
        if data is None:
            return
        self._loading = True
        self.procedure_combo.clear()
        kind, name = data
        if kind == "module":
            self.procedure_combo.addItem(tr("(Declarations)"), "module")
        elif kind == "pymodule":
            self.procedure_combo.addItem(tr("(Module)"), "pymodule")
        elif kind == "orphan":
            handler = self.document.project.code.handlers.get(name)
            self.procedure_combo.addItem(handler.event if handler else "", name)
        else:
            if kind == "page":
                # Page handlers written outside the IDE too: they run, so they must be visible.
                extra = [handler.event for handler in self.document.project.code.handlers.values() if handler.widget == name and handler.event not in PAGE_EVENTS and not self.document.project.find_widget(name)]
                events = [*PAGE_EVENTS, *dict.fromkeys(extra)]
            else:
                events = events_for(self.document.project.find_widget(name).type)
            for event in events:
                handler = handler_name(name, event)
                self.procedure_combo.addItem(event, handler)
                exists = handler in self.document.project.code.handlers
                font = QFont(self.procedure_combo.font())
                font.setBold(exists)
                self.procedure_combo.setItemData(self.procedure_combo.count() - 1, font, Qt.FontRole)
        selected = self.procedure_combo.findData(self.current[1]) if self.current[0] == "handler" else -1
        if selected < 0 and kind == "widget":
            selected = self.procedure_combo.findText(default_event(self.document.project.find_widget(name).type))
        self.procedure_combo.setCurrentIndex(max(0, selected))
        self._loading = False
        self._load_body()

    def _procedure_changed(self):
        if not self._loading:
            self._load_body()

    def _load_body(self):
        data = self.object_combo.currentData()
        procedure = self.procedure_combo.currentData()
        if data is None or procedure is None:
            return
        kind, name = data
        if kind == "module":
            self.current = ("module", "module")
            body, signature = self.document.project.code.module, "' " + tr("(General)")
        elif kind == "pymodule":
            self.current = ("pymodule", name)
            module = self.module()
            body, signature = module.source, "' " + tr("{file}: imported with import {name}", file=f"{module.name}.py", name=module.name)
        elif kind == "orphan":
            self.current = ("handler", procedure)
            handler = self.document.project.code.handlers[procedure]
            body, signature = handler.body, f"def {procedure}(e):  ' " + tr("orphan handler")
        else:
            event = self.procedure_combo.currentText()
            procedure = handler_name(name, event)
            existing = self.document.project.code.handlers.get(procedure)
            if existing and (existing.widget != name or existing.event != event):
                # Orphan handler of an object created again with the same name: it is attached again.
                self._loading = True
                self.document.execute("Create Handler", lambda project: project.ensure_handler(name, event))
                existing = self.document.project.code.handlers[procedure]
            self.current = ("handler", procedure)
            self._unsaved_handler = None if existing else (kind, name, procedure, event)
            body, signature = existing.body if existing else "", f"def {procedure}(e):"
        self._edit_session += 1
        self._loading = True
        self.signature.setText(signature)
        self.editor.setPlainText(body)
        self.editor.setEnabled(not self.document.read_only)
        self._loading = False
        self.module_hint.setVisible(kind == "pymodule")
        self.show_errors([])

    def open_handler(self, name, event=None, line=None):
        widget = self.document.project.find_widget(name)
        kind = "widget" if widget else "page"
        event = event or (default_event(widget.type) if widget else "SCREEN_LOADED")
        index = self._find_object((kind, name))
        if index < 0:
            return
        self.object_combo.setCurrentIndex(index)
        procedure = self.procedure_combo.findText(event)
        if procedure >= 0:
            self.procedure_combo.setCurrentIndex(procedure)
        self._go_to_line(line)

    def open_source(self, handler_name, line=1):
        if handler_name == "module":
            self.object_combo.setCurrentIndex(0)
        else:
            handler = self.document.project.code.handlers.get(handler_name)
            if not handler:
                return
            page_names = {page.name for page in self.document.project.pages}
            if not self.document.project.find_widget(handler.widget) and handler.widget not in page_names:
                index = self._find_object(("orphan", handler_name))
                if index < 0:
                    return
                self.object_combo.setCurrentIndex(index)
                self._go_to_line(line)
                return
            self.open_handler(handler.widget, handler.event, line)
        if handler_name == "module" and line:
            self.editor.setTextCursor(QTextCursor(self.editor.document().findBlockByNumber(line - 1)))

    def _go_to_line(self, line):
        """Put the cursor on the line, if one is given, and give the editor the focus."""
        if line:
            self.editor.setTextCursor(QTextCursor(self.editor.document().findBlockByNumber(line - 1)))
            self.editor.centerCursor()
        self.editor.setFocus()

    def set_running(self, running):
        self.editor.setReadOnly(running)
        self.running_bar.setVisible(running)

    def mark_line(self, line):
        """The line of an error opened from the Errors panel: highlighted, so it shows even when read-only."""
        if line:
            self.editor.show_errors([line])
            QTimer.singleShot(0, self.editor.setFocus)  # after the double click the focus would go back to the list

    def module(self, module_id=None):
        """The open module, or the one with module_id; None if it is gone."""
        module_id = module_id or (self.current[1] if self.current[0] == "pymodule" else None)
        return next((module for module in self.document.project.modules if module.id == module_id), None)

    def open_module(self, name, line=None):
        """Open the module with that name, at the given line."""
        module = next((module for module in self.document.project.modules if module.name == name), None)
        index = self._find_object(("pymodule", module.id)) if module else -1
        if index < 0:
            return False
        self.object_combo.setCurrentIndex(index)
        if self.current != ("pymodule", module.id):  # already selected: the text was not loaded again
            self._load_object()
        self._go_to_line(line)
        return True

    def _stored_text(self):
        kind, name = self.current
        if kind == "module":
            return self.document.project.code.module
        if kind == "pymodule":
            module = self.module()
            return module.source if module else ""
        handler = self.document.project.code.handlers.get(name)
        return handler.body if handler else ""

    def _sync_text(self):
        body = self._stored_text()
        if self.editor.toPlainText() != body:
            position = self.editor.textCursor().position()
            self._loading = True
            self.editor.setPlainText(body)
            cursor = self.editor.textCursor()
            cursor.setPosition(min(position, len(body)))
            self.editor.setTextCursor(cursor)
            self._loading = False

    def _text_changed(self):
        if self._loading or self.document.read_only:
            return
        kind, name = self.current
        body = self.editor.toPlainText()
        if body == self._stored_text():  # recolouring the text also emits textChanged
            return
        code_only = True
        if kind == "module":
            mutator = lambda project: setattr(project.code, "module", body)
        elif kind == "pymodule":
            module = self.module()
            if module is None:
                return
            module_name = module.name
            mutator = lambda project: set_module_source(project, module_name, body)
        elif self._unsaved_handler and name not in self.document.project.code.handlers:
            _kind, owner, _procedure, event = self._unsaved_handler
            mutator = lambda project: setattr(project.ensure_handler(owner, event)[1], "body", body)
            code_only = False
        else:
            mutator = lambda project: setattr(project.code.handlers[name], "body", body)
        self._loading = True
        try:
            self.document.execute("Edit Code", mutator, 10000 + self._edit_session, code_only)
        finally:
            self._loading = False
        self.check_timer.start()
        if kind == "pymodule":
            self.helper_timer.start()

    def show_errors(self, errors):
        self._errors = errors
        lines = [error.get("sourceLine") for error in errors if error.get("sourceLine")]
        self.editor.show_errors(lines)
        self.error.setText("\n".join(error["message"] for error in errors))
        self.error.setVisible(bool(errors))

    def check_syntax(self):
        if not self.document.project:
            return
        with tempfile.TemporaryDirectory(prefix="lvgl-mpy-studio-check-") as directory:
            generate_project(self.document.project, directory)
            try:
                compile_python(directory)
                errors = []
            except CompileError as exc:
                modules = {module.name for module in self.document.project.modules}
                errors = [map_error(error, Path(directory) / "sourcemap.json", modules) for error in exc.errors]
            relevant = []
            kind, name = self.current
            module = self.module() if kind == "pymodule" else None
            for error in errors:
                if module is not None:
                    if error.get("module") == module.name:
                        relevant.append(error)
                elif error.get("handler") == ("module" if kind == "module" else name):
                    relevant.append(error)
            self.show_errors(relevant)
            self.syntaxChecked.emit(errors)

    def _completions(self, qualified):
        parts = qualified.split(".")
        if parts[0] == "lv":
            api = self._api()
            if len(parts) == 2:
                return [*api["constants"], *api["functions"], *api["objects"]]
            return []
        if parts[0] != "ui":
            return []
        if len(parts) == 2:
            pages = [page_constant(page.name) for page in self.document.project.pages]
            return [*self.document.project.used_names, *pages, "load_page", "load_page_anim", "get_current_page"]
        if len(parts) == 3:
            widget = self.document.project.find_widget(parts[1])
            if not widget:
                return []
            if is_component(widget.type):
                return list(methods_for(widget.type))
            object_name = "obj" if widget.type in ("panel", "page") else widget.type
            objects = self._api()["objects"]
            methods = []
            while object_name in objects:
                methods.extend(objects[object_name]["methods"])
                object_name = objects[object_name]["parent"]
            return methods
        return []

    def _api(self):
        """Names to complete, extracted from the binding by runtime/update_completion.py."""
        if not hasattr(self, "_api_data"):
            path = Path(__file__).parents[2] / "gen" / "completion.json"
            self._api_data = json.loads(path.read_text(encoding="utf-8"))
        return self._api_data
