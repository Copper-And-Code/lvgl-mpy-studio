"""Print the sources of the project: paged, with line numbers and syntax colours."""

from datetime import date

from PySide6.QtCore import QMarginsF, QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPageLayout, QPainter, QPen, QTextDocument, QTextLayout, QTextOption
from PySide6.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PySide6.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QRadioButton, QVBoxLayout

from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.ui.code.editor import PythonHighlighter, monospace_font
from lvgl_mpy_studio.ui.theme import LIGHT

POINT_SIZE = 9
MARGIN_MM = 15
CONTINUATION = 4  # characters a wrapped line is indented by
GREY = "#6E7781"


def handler_source(name, handler):
    """A handler as the function it becomes: the editor shows only its body."""
    body = "\n".join(f"    {line}" if line.strip() else "" for line in handler.body.splitlines()) or "    pass"
    return f"def {name}(e):\n{body}\n"


def all_sources(project):
    """Every source of the project as (title, text): the general code, the handlers, each module."""
    result = [(tr("(General)"), project.code.module)]
    handlers = "\n\n".join(handler_source(name, handler) for name, handler in sorted(project.code.handlers.items()))
    if handlers:
        result.append((tr("Handlers"), handlers))
    result.extend((f"{module.name}.py", module.source) for module in project.modules)
    return [(title, text) for title, text in result if text.strip()]


def open_source(project, current):
    """The source open in the code panel, as (title, text); current is CodePanel.current."""
    kind, name = current
    if kind == "pymodule":
        module = next((module for module in project.modules if module.id == name), None)
        return (f"{module.name}.py", module.source) if module else None
    if kind == "handler":
        handler = project.code.handlers.get(name)
        return (name, handler_source(name, handler)) if handler else None
    return tr("(General)"), project.code.module


class Pages:
    """The sources laid out on the pages of a printer.

    Laid out before drawing, because the footer says how many pages there are. Each section
    starts on a new page; a long line wraps, indented, and keeps one line number."""

    def __init__(self, device, area, project_name, sections, numbers=True):
        self.area = QRectF(area)
        self.project_name = project_name
        self.numbers = numbers
        self.font = monospace_font()
        self.font.setStyleHint(QFont.Monospace)
        self.font.setPointSizeF(POINT_SIZE)
        self.device = device
        metrics = QFontMetricsF(self.font, device)
        self.line_height = metrics.lineSpacing()
        self.ascent = metrics.ascent()
        self.char = metrics.horizontalAdvance("0")
        longest = max((text.count("\n") + 1 for _title, text in sections), default=1)
        self.gutter = (len(str(longest)) + 2) * self.char if numbers else 0
        self.band = self.line_height * 2  # header and footer, each with its rule
        self.pages = []  # each: (title, [(y, QTextLine, number or None)])
        self._layouts = []  # keeps the layouts alive: the lines belong to them
        for title, text in sections:
            self._add(title, text)

    @property
    def columns(self):
        return int((self.area.width() - self.gutter) / self.char)

    def _add(self, title, text):
        document = QTextDocument()
        document.setPlainText(text.rstrip("\n"))
        highlighter = PythonHighlighter(document)
        highlighter.apply_colors(LIGHT)  # paper is white whatever the theme of the IDE
        width = self.area.width() - self.gutter
        indent = CONTINUATION * self.char
        bottom = self.area.height() - self.band
        lines, y = [], self.band
        block = document.begin()
        while block.isValid():
            layout = QTextLayout(block.text(), self.font, self.device)
            option = QTextOption()
            option.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
            layout.setTextOption(option)
            layout.setFormats(block.layout().formats())
            layout.beginLayout()
            first = True
            while True:
                line = layout.createLine()
                if not line.isValid():
                    break
                line.setLineWidth(width if first else width - indent)
                if y + self.line_height > bottom:
                    self.pages.append((title, lines))
                    lines, y = [], self.band
                line.setPosition(QPointF(0, 0))
                lines.append((y, line, block.blockNumber() + 1 if first else None))
                y += self.line_height
                first = False
            layout.endLayout()
            self._layouts.append(layout)
            block = block.next()
        self.pages.append((title, lines))

    def draw(self, painter, index):
        title, lines = self.pages[index]
        area, grey = self.area, QColor(GREY)
        painter.save()
        painter.translate(area.topLeft())
        painter.setFont(self.font)
        painter.setPen(QPen(grey, 0))
        rule = self.line_height * 1.4
        painter.drawLine(QPointF(0, rule), QPointF(area.width(), rule))
        painter.drawLine(QPointF(0, area.height() - rule), QPointF(area.width(), area.height() - rule))
        top = QRectF(0, 0, area.width(), self.line_height)
        bottom = QRectF(0, area.height() - self.line_height, area.width(), self.line_height)
        painter.setPen(Qt.black)
        painter.drawText(top, Qt.AlignLeft | Qt.AlignVCenter, f"{self.project_name} — {title}")
        painter.setPen(grey)
        painter.drawText(bottom, Qt.AlignLeft | Qt.AlignVCenter, date.today().isoformat())
        painter.drawText(bottom, Qt.AlignRight | Qt.AlignVCenter, tr("Page {page} of {pages}", page=index + 1, pages=len(self.pages)))
        indent = CONTINUATION * self.char
        for y, line, number in lines:
            if number is not None and self.numbers:
                painter.setPen(grey)
                painter.drawText(QRectF(0, y, self.gutter - self.char, self.line_height), Qt.AlignRight | Qt.AlignVCenter, str(number))
            painter.setPen(Qt.black)
            line.draw(painter, QPointF(self.gutter + (0 if number is not None else indent), y))
        painter.restore()


def render(printer, project_name, sections, numbers=True):
    """Draw the sources on the printer; return the number of pages."""
    painter = QPainter(printer)
    try:
        area = printer.pageLayout().paintRectPixels(printer.resolution())
        pages = Pages(printer, QRectF(0, 0, area.width(), area.height()), project_name, sections, numbers)
        first, last = printer.fromPage() or 1, printer.toPage() or len(pages.pages)
        wanted = [index for index in range(len(pages.pages)) if first <= index + 1 <= last]
        for position, index in enumerate(wanted):
            if position:
                printer.newPage()
            pages.draw(painter, index)
        return len(pages.pages)
    finally:
        painter.end()


def new_printer():
    printer = QPrinter(QPrinter.HighResolution)
    printer.setPageMargins(QMarginsF(MARGIN_MM, MARGIN_MM, MARGIN_MM, MARGIN_MM), QPageLayout.Millimeter)
    return printer


class PrintSourcesDialog(QDialog):
    """What to print, then the preview or the printer."""

    def __init__(self, project, current, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Print Sources"))
        self.project = project
        self.opened = open_source(project, current)
        self.everything = all_sources(project)
        layout = QVBoxLayout(self)
        self.open_choice = QRadioButton(tr("The open source: {name}", name=self.opened[0] if self.opened else ""))
        self.all_choice = QRadioButton(tr("All the sources of the project ({count})", count=len(self.everything)))
        has_open = bool(self.opened and self.opened[1].strip())
        self.open_choice.setEnabled(has_open)
        self.all_choice.setEnabled(bool(self.everything))
        (self.open_choice if has_open else self.all_choice).setChecked(True)
        self.numbers = QCheckBox(tr("Line numbers"))
        self.numbers.setChecked(True)
        layout.addWidget(self.open_choice)
        layout.addWidget(self.all_choice)
        layout.addWidget(self.numbers)
        buttons = QDialogButtonBox(QDialogButtonBox.Cancel)
        self.preview_button = buttons.addButton(tr("Preview…"), QDialogButtonBox.ActionRole)
        self.print_button = buttons.addButton(tr("Print…"), QDialogButtonBox.AcceptRole)
        for button in (self.preview_button, self.print_button):
            button.setEnabled(has_open or bool(self.everything))
        self.preview_button.clicked.connect(self.preview)
        self.print_button.clicked.connect(self.print)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def sections(self):
        return [self.opened] if self.open_choice.isChecked() else self.everything

    def render(self, printer):
        return render(printer, self.project.projectName, self.sections(), self.numbers.isChecked())

    def preview(self):
        dialog = QPrintPreviewDialog(new_printer(), self)
        dialog.paintRequested.connect(self.render)
        dialog.exec()

    def print(self):
        printer = new_printer()
        if QPrintDialog(printer, self).exec() == QDialog.Accepted:
            self.render(printer)
            self.accept()
