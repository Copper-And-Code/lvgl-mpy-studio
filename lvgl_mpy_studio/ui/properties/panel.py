import copy
from pathlib import Path

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QIcon, QImage, QPixmap, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QColorDialog,
    QComboBox,
    QCompleter,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QStyledItemDelegate,
    QTabWidget,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from lvgl_mpy_studio.core.assets import AssetError, add_font, add_image, font_name, fonts, free_image_name
from lvgl_mpy_studio.core.components import COMPONENTS
from lvgl_mpy_studio.core.events import EVENTS, events_for
from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.core.model import Project, widget_definitions
from lvgl_mpy_studio.core.names import validate_name
from lvgl_mpy_studio.ui.theme import error_color

DESCRIPTOR_ROLE = Qt.UserRole + 1
CATEGORY_ROLE = Qt.UserRole + 2
CHECKED_ROLE = Qt.UserRole + 3


def display_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return str(value)
    return str(value)


class PropertyDelegate(QStyledItemDelegate):
    project_fonts = staticmethod(lambda: [])  # set by the panel: names of the fonts of the project

    def createEditor(self, parent, option, index):
        descriptor = index.data(DESCRIPTOR_ROLE) or {"type": "string"}
        kind = descriptor.get("type")
        if kind == "number":
            editor = QSpinBox(parent)
            editor.setRange(int(descriptor.get("min", -1000000)), int(descriptor.get("max", 1000000)))
            return editor
        if kind in ("select", "enum"):
            editor = QComboBox(parent)
            editor.setEditable(True)
            editor.addItems(descriptor.get("options") or [])
            return editor
        if kind in ("color", "image", "font"):
            editor = QWidget(parent)
            layout = QHBoxLayout(editor)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(1)
            text = QLineEdit(editor)
            button = QPushButton("…", editor)
            button.setMaximumWidth(28)
            layout.addWidget(text)
            layout.addWidget(button)
            def choose_color():
                chosen = QColorDialog.getColor(QColor(text.text()), editor)
                if chosen.isValid():
                    text.setText(chosen.name().upper())
            def choose_image():
                path, _filter = QFileDialog.getOpenFileName(editor, tr("Choose an image"), text.text(), tr("Images (*.png *.jpg *.jpeg *.bmp)"))
                if path:
                    text.setText(path)
            def choose_font():
                path, _filter = QFileDialog.getOpenFileName(editor, tr("Choose a font"), text.text(), tr("Fonts (*.ttf *.otf)"))
                if path:
                    text.setText(path)
            if kind == "font":  # the fonts already in the project, or a file to add to it
                text.setPlaceholderText(tr("built-in font"))
                text.setCompleter(QCompleter(self.project_fonts(), editor))
            button.clicked.connect({"color": choose_color, "image": choose_image, "font": choose_font}[kind])
            editor.value = text
            return editor
        return QLineEdit(parent)

    def setEditorData(self, editor, index):
        value = index.data(Qt.EditRole) or ""
        if isinstance(editor, QSpinBox):
            editor.setValue(int(value or 0))
        elif isinstance(editor, QComboBox):
            editor.setCurrentText(value)
        elif hasattr(editor, "value"):
            editor.value.setText(value)
        else:
            editor.setText(value)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QSpinBox):
            value = str(editor.value())
        elif isinstance(editor, QComboBox):
            value = editor.currentText()
        elif hasattr(editor, "value"):
            value = editor.value.text()
        else:
            value = editor.text()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class PropertiesPanel(QWidget):
    handlerRequested = Signal(str, str)

    def __init__(self, document, parent=None):
        super().__init__(parent)
        self.document = document
        self.names = []
        self._loading = False
        self.definitions = {**widget_definitions(), **COMPONENTS}
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.error = QLabel()
        self.apply_error_color()
        self.error.setWordWrap(True)
        self.error.hide()
        layout.addWidget(self.error)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        properties_page = QWidget()
        properties_layout = QVBoxLayout(properties_page)
        properties_layout.setContentsMargins(0, 0, 0, 0)
        self.order = QComboBox()
        self.order.addItems((tr("By Category"), tr("Alphabetical")))
        properties_layout.addWidget(self.order)
        self.model = QStandardItemModel(0, 2)
        self.model.setHorizontalHeaderLabels((tr("Properties"), tr("Value")))
        self.view = QTreeView()
        self.view.setModel(self.model)
        delegate = PropertyDelegate(self.view)
        delegate.project_fonts = lambda: [item["name"] for item in fonts(self.document.project)]
        self.view.setItemDelegate(delegate)
        self.view.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.view.setRootIsDecorated(True)
        self.view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.view.header().setSectionResizeMode(1, QHeaderView.Stretch)
        properties_layout.addWidget(self.view)
        self.tabs.addTab(properties_page, tr("Properties"))
        self.events_model = QStandardItemModel(0, 3)
        self.events_model.setHorizontalHeaderLabels((tr("Event"), tr("Description"), tr("Handler")))
        self.events_view = QTreeView()
        self.events_view.setModel(self.events_model)
        self.events_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.events_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.events_view.header().setSectionResizeMode(1, QHeaderView.Stretch)
        self.events_view.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tabs.addTab(self.events_view, tr("Events"))
        self.order.currentTextChanged.connect(self.rebuild)
        self.model.itemChanged.connect(self._item_changed)
        self.events_view.doubleClicked.connect(self._event_activated)
        self.document.reset.connect(self.schedule_rebuild)
        self.rebuild()

    def apply_error_color(self):
        self.error.setStyleSheet(f"color: {error_color()}; padding: 3px")

    def retranslate(self):
        self.model.setHorizontalHeaderLabels((tr("Properties"), tr("Value")))
        self.events_model.setHorizontalHeaderLabels((tr("Event"), tr("Description"), tr("Handler")))
        self.rebuild()

    def schedule_rebuild(self):
        QTimer.singleShot(0, self.rebuild)

    def set_selection(self, names):
        self.names = [name for name in names if self.document.project.find_widget(name)]
        self.rebuild()

    def _widgets(self):
        widgets = [self.document.project.find_widget(name) for name in self.names]
        return [widget for widget in widgets if widget is not None]

    def _descriptors(self, widgets):
        if not widgets:
            return []
        common = None
        definitions = {}
        for widget in widgets:
            properties = self.definitions.get(widget.type, {}).get("properties") or []
            definitions[widget.type] = {item["name"]: item for item in properties}
            names = set(definitions[widget.type]) | set(widget.props)
            common = names if common is None else common & names
        descriptors = []
        first = list(definitions[widgets[0].type])
        ordered = [name for name in first if name in (common or ())] + sorted(set(common or ()) - set(first))
        for name in ordered:
            descriptor = copy.deepcopy(next((definitions[widget.type].get(name) for widget in widgets if definitions[widget.type].get(name)), {"name": name, "type": "string"}))
            descriptors.append(descriptor)
        return descriptors

    def rebuild(self):
        self._loading = True
        self.model.removeRows(0, self.model.rowCount())
        self.events_model.removeRows(0, self.events_model.rowCount())
        widgets = self._widgets()
        if widgets:
            name_item = QStandardItem(tr("Name"))
            name_item.setEditable(False)
            value_item = QStandardItem(widgets[0].name if len(widgets) == 1 else "")
            value_item.setData({"name": "Name", "type": "name"}, DESCRIPTOR_ROLE)
            value_item.setData("Identity", CATEGORY_ROLE)
            self.model.appendRow((name_item, value_item))
            categories = {}
            for descriptor in self._descriptors(widgets):
                name = descriptor["name"]
                category = "Position" if name in ("x", "y", "width", "height") else "Behavior" if name in ("value", "checked", "selected", "options", "min", "max", "period", "enabled") else "Appearance"
                values = [widget.props.get(name) for widget in widgets]
                value = values[0] if all(item == values[0] for item in values) else ""
                label_item = QStandardItem(tr(descriptor.get("label", name)))
                label_item.setEditable(False)
                value_item = QStandardItem(display_value(value))
                value_item.setData(descriptor, DESCRIPTOR_ROLE)
                value_item.setData(category, CATEGORY_ROLE)
                if descriptor.get("type") == "color" and QColor(display_value(value)).isValid():
                    swatch = QPixmap(14, 14)
                    swatch.fill(QColor(display_value(value)))
                    value_item.setIcon(QIcon(swatch))
                elif descriptor.get("type") == "boolean":
                    value_item.setEditable(False)
                    value_item.setCheckable(True)
                    value_item.setCheckState(Qt.Checked if value is True else Qt.Unchecked)
                    value_item.setData(value is True, CHECKED_ROLE)
                categories.setdefault(category, []).append((label_item, value_item))
            if self.order.currentIndex() == 1:
                rows = [row for category in categories.values() for row in category]
                for row in sorted(rows, key=lambda row: row[0].text().lower()):
                    self.model.appendRow(row)
            else:
                for category in ("Identity", "Position", "Appearance", "Behavior"):
                    rows = categories.get(category)
                    if not rows:
                        continue
                    group = QStandardItem(tr(category))
                    group.setEditable(False)
                    font = group.font()
                    font.setBold(True)
                    group.setFont(font)
                    for row in rows:
                        group.appendRow(row)
                    self.model.appendRow(group)
            self.view.expandAll()
            if len(widgets) == 1:
                widget = widgets[0]
                for name in events_for(widget.type):
                    event = EVENTS[name]
                    font = QFont()
                    font.setBold(name in widget.events)
                    row = [QStandardItem(name), QStandardItem(tr(event.description)), QStandardItem(widget.events.get(name, ""))]
                    for item in row:
                        item.setEditable(False)
                        item.setFont(font)
                    row[0].setData(widget.name, Qt.UserRole)
                    self.events_model.appendRow(row)
        self._loading = False

    def _item_changed(self, item):
        if self._loading or item.column() != 1:
            return
        descriptor = item.data(DESCRIPTOR_ROLE)
        if not descriptor:
            return
        name, kind, text = descriptor["name"], descriptor.get("type"), item.text()
        widgets = self._widgets()
        self.error.hide()
        if name == "Name":
            if len(widgets) != 1:
                self.schedule_rebuild()
                return
            old_name = widgets[0].name
            error = validate_name(text, self.document.project.used_names - {old_name})
            if error:
                self.error.setText(error)
                self.error.show()
                self.schedule_rebuild()
                return
            warnings = []
            self.document.execute(tr("Rename Widget"), lambda project: warnings.extend(project.rename_widget(old_name, text)))
            self.names = [text]
            if warnings:
                self.error.setText("\n".join(warnings))
                self.error.show()
            self.schedule_rebuild()
            return
        try:
            if kind == "number":
                value = int(text)
            elif kind == "boolean":
                previous = item.data(CHECKED_ROLE)
                written = text.lower() == "true"
                value = written if written != previous else item.checkState() == Qt.Checked
            else:
                value = text
        except ValueError:
            self.error.setText(tr("Invalid value for {name}", name=name))
            self.error.show()
            self.schedule_rebuild()
            return
        image = None
        if kind == "image" and text and Path(text).is_file():  # a file was chosen: it becomes an image of the project
            try:
                image = self._read_image(Path(text))
            except AssetError as exc:
                self.error.setText(str(exc))
                self.error.show()
                self.schedule_rebuild()
                return
            value = image[0]
        font = None
        if kind == "font" and text and Path(text).is_file():  # a font file was chosen: it becomes a font of the project
            try:
                data = Path(text).read_bytes()
                existing = next((item["name"] for item in fonts(self.document.project) if item["name"] == font_name(text)), None)
                font = (font_name(text), data) if existing is None else None
                value = font_name(text)
                if font:
                    add_font(Project(), *font)  # the checks, before anything changes
            except (OSError, AssetError) as exc:
                self.error.setText(str(exc))
                self.error.show()
                self.schedule_rebuild()
                return
        self.document.undo_stack.beginMacro(tr("Change {name}", name=name))
        try:
            if image:
                self.document.execute(tr("Add Image"), lambda project: add_image(project, *image))
            if font:
                self.document.execute(tr("Add Font"), lambda project: add_font(project, *font))
            for old_name in self.names:
                self.document.execute(tr("Change {name}", name=name), lambda project, widget_name=old_name: project.find_widget(widget_name).props.__setitem__(name, value))
        finally:
            self.document.undo_stack.endMacro()
        self.schedule_rebuild()

    def _read_image(self, path):
        """(name, PNG bytes) for a picture file: converted to PNG and made no larger than the screen."""
        picture = QImage(str(path))
        if picture.isNull():
            raise AssetError(tr("{file} is not a picture this program can read", file=path.name))
        display = self.document.project.display
        if picture.width() > display.width or picture.height() > display.height:
            picture = picture.scaled(display.width, display.height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        data = QByteArray()
        buffer = QBuffer(data)
        buffer.open(QIODevice.WriteOnly)
        picture.save(buffer, "PNG")
        buffer.close()
        name, data = free_image_name(self.document.project, path.name), bytes(data.data())
        add_image(Project(), name, data)  # the checks, before anything changes: a large photo is still too heavy as PNG
        return name, data

    def _event_activated(self, index):
        if not self.names:
            return
        event = self.events_model.item(index.row(), 0).text()
        widget_name = self.names[0]
        self.document.execute(tr("Create Handler"), lambda project: project.ensure_handler(widget_name, event))
        self.handlerRequested.emit(widget_name, event)
