import copy

from PySide6.QtCore import QMimeData, QPoint, QPointF, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QDrag, QFontMetrics, QKeySequence, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from lvgl_mpy_studio.core.components import COMPONENTS, is_component
from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.core.model import Widget, widget_definitions
from lvgl_mpy_studio.ui.theme import canvas_color, icon

WIDGET_ICONS = {
    "button": "gesture-tap-button", "label": "format-text", "panel": "card-outline", "slider": "tune-variant",
    "switch": "toggle-switch-outline", "checkbox": "checkbox-marked-outline", "textarea": "form-textbox",
    "dropdown": "form-dropdown", "roller": "format-list-group", "spinbox": "numeric", "keyboard": "keyboard-outline",
    "bar": "progress-helper", "arc": "circle-slice-3", "spinner": "loading", "led": "led-outline", "chart": "chart-line",
    "table": "table", "scale": "ruler", "image": "image-outline", "imagebutton": "image-filter-center-focus",
    "tabview": "tab", "tileview": "view-grid-outline", "menu": "menu", "win": "application-outline",
    "list": "format-list-bulleted", "msgbox": "message-text-outline", "buttonmatrix": "dialpad",
    "calendar": "calendar-month-outline", "line": "vector-line", "span": "format-letter-case",
    "buzzer": "volume-high", "timer": "timer-outline",
}
BLOCK_ICON = "chip"  # for a block that names no icon, or one the icon font lacks


def widget_icon(widget_type):
    """The icon of a widget or component; a block names its own in block.json, as mdi6.<name>."""
    if widget_type in WIDGET_ICONS:
        return icon(WIDGET_ICONS[widget_type])
    definition = COMPONENTS.get(widget_type)
    if definition is None:
        return icon("shape-outline")
    name = str(definition.get("icon") or "")
    found = icon(name.removeprefix("mdi6.")) if name.startswith("mdi6.") else None
    return found if found is not None and not found.isNull() else icon(BLOCK_ICON)
WIDGET_MIME = "application/x-lvgl-widget"
WIDGETS_MIME = "application/x-lvgl-widgets"
MINIMUM_SIZE = 8
DROP_PREVIEW_OPACITY = 0.7
DROP_PREVIEW_Z = 1_000_000
DRAG_CHIP_OFFSET = 14
CONTAINERS = {"obj", "panel", "tabview", "tileview", "window", "menu"}
THEMES = {
    "button": ("#2196F3", "#FFFFFF"), "imagebutton": ("#2196F3", "#FFFFFF"),
    "label": ("#00000000", "#000000"), "span": ("#FFFFFF", "#000000"),
    "panel": ("#F5F5F5", "#333333"), "obj": ("#F5F5F5", "#333333"),
    "slider": ("#E0E0E0", "#1976D2"), "switch": ("#BDBDBD", "#FFFFFF"),
    "checkbox": ("#FFFFFF", "#000000"), "textarea": ("#FFFFFF", "#000000"),
    "dropdown": ("#FFFFFF", "#000000"), "roller": ("#F5F5F5", "#000000"),
    "bar": ("#E0E0E0", "#4CAF50"), "arc": ("#E0E0E0", "#FF9800"),
    "chart": ("#FFFFFF", "#2196F3"), "table": ("#FFFFFF", "#000000"),
    "keyboard": ("#EEEEEE", "#222222"), "calendar": ("#FFFFFF", "#222222"),
}


def color(value, fallback):
    result = QColor(value or fallback)
    return result if result.isValid() else QColor(fallback)


def snapped(value, grid):
    return round(value / grid) * grid if grid > 1 else round(value)


class ResizeHandle(QGraphicsRectItem):
    def __init__(self, owner, index):
        super().__init__(-4, -4, 8, 8, owner)
        self.owner, self.index = owner, index
        self.setZValue(1000)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self._origin = None

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(QColor("#1976D2"), 1))
        painter.setBrush(Qt.white)
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        self._origin = (event.scenePos(), QRectF(self.owner.rect()), QPointF(self.owner.pos()))
        event.accept()

    def mouseMoveEvent(self, event):
        if self._origin is None:
            return
        start, rect, pos = self._origin
        delta = event.scenePos() - start
        grid = self.owner.designer_scene.grid_size
        dx, dy = snapped(delta.x(), grid), snapped(delta.y(), grid)
        left, right = self.index in (0, 6, 7), self.index in (2, 3, 4)
        top, bottom = self.index in (0, 1, 2), self.index in (4, 5, 6)
        width = rect.width() - dx if left else rect.width() + dx if right else rect.width()
        height = rect.height() - dy if top else rect.height() + dy if bottom else rect.height()
        width, height = max(MINIMUM_SIZE, width), max(MINIMUM_SIZE, height)
        x = pos.x() + rect.width() - width if left else pos.x()
        y = pos.y() + rect.height() - height if top else pos.y()
        self.owner.set_geometry(x, y, width, height)
        self.owner.designer_scene.widgetsReshaped.emit()
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._origin is not None:
            self.owner.commit_geometry()
        self._origin = None
        event.accept()


class WidgetItem(QGraphicsItem):
    def __init__(self, designer_scene, widget):
        super().__init__()
        self.designer_scene = designer_scene
        self.widget_id = widget.id
        self.widget_type = widget.type
        self.name = widget.name
        self.props = copy.deepcopy(widget.props)
        self._origin = None
        self.always_drawn = False    # the drag preview is not in the LVGL frame yet
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.setToolTip(f"{widget.name} ({widget.type})")
        self.set_geometry(self.props.get("x", 0), self.props.get("y", 0), self.props.get("width", 100), self.props.get("height", 40))
        self.handles = []    # created at the first selection: with hundreds of widgets they weigh
        self.start_geometry = self.geometry()

    def boundingRect(self):
        return self.rect()

    def rect(self):
        return QRectF(0, 0, max(MINIMUM_SIZE, float(self.props.get("width", 100))), max(MINIMUM_SIZE, float(self.props.get("height", 40))))

    def geometry(self):
        return tuple(int(self.props[key]) for key in ("x", "y", "width", "height"))

    def set_geometry(self, x, y, width, height):
        self.prepareGeometryChange()
        self.props.update(x=round(x), y=round(y), width=round(width), height=round(height))
        self.setPos(round(x), round(y))
        self.update()
        if hasattr(self, "handles"):
            self._update_handles()

    def _update_handles(self):
        rect = self.rect()
        points = [
            rect.topLeft(), QPointF(rect.center().x(), rect.top()), rect.topRight(),
            QPointF(rect.right(), rect.center().y()), rect.bottomRight(),
            QPointF(rect.center().x(), rect.bottom()), rect.bottomLeft(),
            QPointF(rect.left(), rect.center().y()),
        ]
        for handle, point in zip(self.handles, points):
            handle.setPos(point)
            handle.setVisible(self.isSelected())

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged and hasattr(self, "handles"):
            if value and not self.handles:
                self.handles = [ResizeHandle(self, index) for index in range(8)]
                self._update_handles()
            for handle in self.handles:
                handle.setVisible(bool(value))
        return super().itemChange(change, value)

    def paint(self, painter, option, widget=None):
        rect = self.rect()
        if self.designer_scene.preview_active and not self.always_drawn:
            display = self.designer_scene.document.project.display
            if not QRectF(0, 0, display.width, display.height).contains(self.sceneBoundingRect()):
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QPen(QColor("#E08A00"), 1, Qt.DotLine))
                painter.drawRect(rect)
            self._paint_selection(painter, rect)
            return
        background, foreground = THEMES.get(self.widget_type, ("#F5F5F5", "#222222"))
        background = color(self.props.get("bgColor"), background)
        foreground = color(self.props.get("textColor"), foreground)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(color(self.props.get("borderColor"), "#9E9E9E"), max(0, int(self.props.get("borderWidth", 1)))))
        painter.setBrush(QBrush(background))
        radius = min(float(self.props.get("radius", 4)), rect.width() / 2, rect.height() / 2)
        painter.drawRoundedRect(rect.adjusted(0.5, 0.5, -0.5, -0.5), radius, radius)
        self._paint_control(painter, rect, foreground)
        self._paint_selection(painter, rect)

    def _paint_selection(self, painter, rect):
        if self.isSelected():
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QColor("#1976D2"), 1, Qt.DashLine))
            painter.drawRect(rect)

    def _paint_control(self, painter, rect, foreground):
        kind = self.widget_type
        painter.setPen(QPen(foreground, 2))
        if kind in ("slider", "bar"):
            low, high = float(self.props.get("min", 0)), float(self.props.get("max", 100))
            ratio = (float(self.props.get("value", 50)) - low) / max(1, high - low)
            groove = QRectF(rect.left() + 5, rect.center().y() - 3, rect.width() - 10, 6)
            painter.setBrush(color(self.props.get("indicatorColor"), foreground))
            painter.drawRoundedRect(groove, 3, 3)
            painter.setBrush(Qt.white)
            painter.drawEllipse(QPointF(groove.left() + groove.width() * max(0, min(1, ratio)), groove.center().y()), 6, 6)
            return
        if kind == "switch":
            checked = bool(self.props.get("checked"))
            painter.setBrush(color(self.props.get("onColor") if checked else self.props.get("offColor"), foreground))
            painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), rect.height() / 2, rect.height() / 2)
            painter.setBrush(Qt.white)
            center = rect.right() - rect.height() / 2 if checked else rect.left() + rect.height() / 2
            painter.drawEllipse(QPointF(center, rect.center().y()), rect.height() / 2 - 4, rect.height() / 2 - 4)
            return
        if kind == "checkbox":
            box = QRectF(rect.left() + 2, rect.center().y() - 8, 16, 16)
            painter.setBrush(color(self.props.get("checkedColor"), "#2196F3") if self.props.get("checked") else Qt.white)
            painter.drawRect(box)
            if self.props.get("checked"):
                painter.drawLine(box.bottomLeft() + QPointF(3, -5), box.center() + QPointF(-1, 3))
                painter.drawLine(box.center() + QPointF(-1, 3), box.topRight() + QPointF(-2, 3))
            self._paint_text(painter, rect.adjusted(24, 0, 0, 0), foreground)
            return
        if kind in ("arc", "chart"):
            painter.setBrush(Qt.NoBrush)
            if kind == "arc":
                painter.drawArc(rect.adjusted(7, 7, -7, -7), 35 * 16, 290 * 16)
            else:
                painter.drawPolyline([rect.bottomLeft() + QPointF(5, -5), rect.center(), rect.topRight() + QPointF(-5, 5)])
            return
        if kind in ("table", "keyboard", "calendar"):
            rows, columns = (3, 3) if kind != "keyboard" else (4, 8)
            for row in range(1, rows):
                y = rect.top() + rect.height() * row / rows
                painter.drawLine(QPointF(rect.left(), y), QPointF(rect.right(), y))
            for column in range(1, columns):
                x = rect.left() + rect.width() * column / columns
                painter.drawLine(QPointF(x, rect.top()), QPointF(x, rect.bottom()))
            return
        self._paint_text(painter, rect, foreground)

    def _paint_text(self, painter, rect, foreground):
        text = self.props.get("text") or self.props.get("placeholder") or self.name
        font = painter.font()
        font.setPixelSize(max(8, int(self.props.get("fontSize", 14))))
        painter.setFont(font)
        painter.setPen(foreground)
        painter.drawText(rect.adjusted(4, 2, -4, -2), Qt.AlignCenter | Qt.TextWordWrap, str(text))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not event.modifiers() & Qt.ControlModifier and not self.isSelected():
                self.scene().clearSelection()
            self.setSelected(True)
            self._origin = (event.scenePos(), {item: QPointF(item.pos()) for item in self.designer_scene.drag_group(self)})
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._origin is None:
            return
        start, positions = self._origin
        grid = self.designer_scene.grid_size
        delta = event.scenePos() - start
        for item, position in positions.items():
            rect = item.rect()
            item.set_geometry(snapped(position.x() + delta.x(), grid), snapped(position.y() + delta.y(), grid), rect.width(), rect.height())
        self.designer_scene.widgetsReshaped.emit()
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._origin is not None:
            self.designer_scene.commit_items(list(self._origin[1]))
        self._origin = None
        event.accept()

    def mouseDoubleClickEvent(self, event):
        self.designer_scene.widgetActivated.emit(self.name)
        event.accept()

    def commit_geometry(self):
        self.designer_scene.commit_items([self])


def drag_chip(text, palette):
    """Label next to the cursor: not every system shows the drag image."""
    font = QApplication.font()
    metrics = QFontMetrics(font)
    pixmap = QPixmap(metrics.horizontalAdvance(text) + 20, metrics.height() + 10)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    try:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(palette.mid().color(), 1))
        painter.setBrush(palette.base())
        painter.drawRoundedRect(QRectF(pixmap.rect()).adjusted(0.5, 0.5, -0.5, -0.5), 5, 5)
        painter.setFont(font)
        painter.setPen(palette.text().color())
        painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
    finally:
        painter.end()
    return pixmap


class DesignerScene(QGraphicsScene):
    selectionNamesChanged = Signal(list)
    widgetActivated = Signal(str)
    widgetsReshaped = Signal()
    contextMenuRequested = Signal(QPoint)

    def __init__(self, document, page_id=None, parent=None):
        super().__init__(parent)
        self.document = document
        self.page_id = page_id or document.project.currentPageId
        self.grid_size = 1
        self.show_grid = False
        self.widget_items = {}
        self._rebuilding = False
        self.drop_preview = None
        self.show_preview = False
        self.preview_image = None
        self.document.reset.connect(self.rebuild)
        self.selectionChanged.connect(self._selection_changed)
        self.rebuild()

    @property
    def page(self):
        return next((page for page in self.document.project.pages if page.id == self.page_id), self.document.project.pages[0])

    def set_page(self, page_id):
        if page_id != self.page_id:
            self.page_id = page_id
            self.rebuild()

    @property
    def preview_active(self):
        """A preview of another resolution, stretched over the new one, would show wrong shapes."""
        display = self.document.project.display
        return self.show_preview and self.preview_image is not None and (self.preview_image.width(), self.preview_image.height()) == (display.width, display.height)

    def set_preview(self, enabled, image=None):
        self.show_preview = enabled
        self.preview_image = image
        self.update()

    def rebuild(self):
        selected = self.selected_names()
        self._rebuilding = True
        self.drop_preview = None
        self.clear()
        self.widget_items = {}
        page = self.page
        self.setSceneRect(-40, -40, self.document.project.display.width + 80, self.document.project.display.height + 80)
        pending = [widget for widget in page.widgets if not is_component(widget.type)]
        while pending:
            deferred = []
            for widget in pending:
                parent = self.widget_items.get(widget.parentId)
                if widget.parentId and parent is None and any(item.id == widget.parentId for item in page.widgets):
                    deferred.append(widget)
                    continue
                item = WidgetItem(self, widget)
                self.addItem(item)
                if parent:
                    item.setParentItem(parent)
                item.setZValue(len(self.widget_items))
                self.widget_items[widget.id] = item
                if widget.name in selected:
                    item.setSelected(True)
            pending = deferred
        self._rebuilding = False

    def drawBackground(self, painter, rect):
        painter.fillRect(rect, canvas_color())
        canvas = QRectF(0, 0, self.document.project.display.width, self.document.project.display.height)
        if self.preview_active:
            painter.drawImage(canvas, self.preview_image)
        else:
            painter.fillRect(canvas, QColor("#FFFFFF"))
        painter.setPen(QPen(QColor("#777777"), 1))
        painter.drawRect(canvas)
        if self.show_grid:
            painter.setPen(QPen(QColor(0, 0, 0, 20), 0))
            grid = max(5, self.grid_size)
            x, y = grid, grid
            while x < canvas.width():
                painter.drawLine(QPointF(x, 0), QPointF(x, canvas.height()))
                x += grid
            while y < canvas.height():
                painter.drawLine(QPointF(0, y), QPointF(canvas.width(), y))
                y += grid

    def drag_group(self, grabbed):
        """The objects to move together: a child already follows its container."""
        selected = {item for item in self.selectedItems() if isinstance(item, WidgetItem)}
        group = [item for item in selected if item.parentItem() not in selected]
        return group if grabbed in group else [grabbed]

    def pending_geometry(self):
        """The geometries being changed, not yet recorded in the project."""
        keys = ("x", "y", "width", "height")
        return {item.widget_id: dict(zip(keys, item.geometry())) for item in self.widget_items.values() if item.geometry() != item.start_geometry}

    def commit_items(self, items):
        """Record the moves in one step; a click without moves changes nothing."""
        changed = {item.widget_id: dict(zip(("x", "y", "width", "height"), item.geometry())) for item in items if item.geometry() != item.start_geometry}
        if not changed:
            self.update()
            return
        def mutate(project):
            for widget in project.widgets:
                if widget.id in changed:
                    widget.props.update(changed[widget.id])
        self.document.execute("Change Geometry", mutate)

    def selected_names(self):
        return [item.name for item in self.selectedItems() if isinstance(item, WidgetItem)]

    def _selection_changed(self):
        if not self._rebuilding:
            self.selectionNamesChanged.emit(self.selected_names())

    def item_at(self, scene_pos):
        candidates = [item for item in self.items(scene_pos) if isinstance(item, WidgetItem)]
        return candidates[0] if candidates else None

    @staticmethod
    def _centered(widget_type, position):
        defaults = widget_definitions()[widget_type].get("defaultProps") or {}
        return QPointF(max(0, position.x() - defaults.get("width", 100) / 2), max(0, position.y() - defaults.get("height", 40) / 2))

    def show_drop_preview(self, widget_type, scene_pos):
        if self.drop_preview is None:
            definition = widget_definitions()[widget_type]
            item = WidgetItem(self, Widget(widget_type, definition.get("name", widget_type), props=copy.deepcopy(definition.get("defaultProps") or {})))
            item.setFlags(QGraphicsItem.GraphicsItemFlag(0))
            item.setAcceptedMouseButtons(Qt.NoButton)
            item.setAcceptHoverEvents(False)
            item.setToolTip("")
            item.always_drawn = True
            item.setOpacity(DROP_PREVIEW_OPACITY)
            item.setZValue(DROP_PREVIEW_Z)
            self.addItem(item)
            self.drop_preview = item
        position = self._centered(widget_type, scene_pos)
        rect = self.drop_preview.rect()
        self.drop_preview.set_geometry(snapped(position.x(), self.grid_size), snapped(position.y(), self.grid_size), rect.width(), rect.height())

    def hide_drop_preview(self):
        if self.drop_preview is not None:
            self.removeItem(self.drop_preview)
            self.drop_preview = None

    def add_component(self, widget_type):
        def mutate(project):
            project.add_widget(next(page for page in project.pages if page.id == self.page_id), widget_type)
        return self.document.execute("Add component", mutate)

    def add_widget(self, widget_type, scene_pos, parent_item=None, centered=False):
        if is_component(widget_type):
            self.add_component(widget_type)
            return
        parent_item = parent_item or self.item_at(scene_pos)
        if parent_item and parent_item.widget_type not in CONTAINERS:
            parent_item = None
        local = parent_item.mapFromScene(scene_pos) if parent_item else scene_pos
        if centered:
            local = self._centered(widget_type, local)
        created = []
        def mutate(project):
            page = next(page for page in project.pages if page.id == self.page_id)
            widget = project.add_widget(page, widget_type, {"x": snapped(local.x(), self.grid_size), "y": snapped(local.y(), self.grid_size)})
            if parent_item:
                widget.parentId = parent_item.widget_id
            created.append(widget.id)
        if self.document.execute("Add Widget", mutate) and created:
            self.clearSelection()
            self.widget_items[created[0]].setSelected(True)

    def delete_selected(self):
        names = self.selected_names()
        if names:
            self.document.execute("Delete Widget", lambda project: [project.remove_widget(name) for name in names])

    def move_selected(self, dx, dy):
        selected = self.selected_names()
        if not selected:
            return
        def mutate(project):
            for name in selected:
                widget = project.find_widget(name)
                widget.props["x"] = int(widget.props.get("x", 0)) + dx
                widget.props["y"] = int(widget.props.get("y", 0)) + dy
        self.document.execute("Sposta widget", mutate)

    def copy_selected(self, cut=False):
        selected = set(self.selected_names())
        project = self.document.project
        # A container is copied with what it contains, as when it is deleted.
        inside = {item.id for widget in self.page.widgets if widget.name in selected for item in project.subtree(widget)}
        widgets = [widget for widget in self.page.widgets if widget.id in inside]
        self.document.clipboard = copy.deepcopy([widget.to_dict() for widget in widgets])
        if cut and selected:
            self.delete_selected()

    def paste(self, scene_pos=None):
        if not self.document.clipboard:
            return
        source = copy.deepcopy(self.document.clipboard)
        scene_pos = scene_pos or QPointF(20, 20)
        created = []
        def mutate(project):
            page = next(page for page in project.pages if page.id == self.page_id)
            id_map = {}
            for raw in source:
                old_id = raw["id"]
                widget = project.add_widget(page, raw["type"], raw.get("props"))
                widget.customStyles = copy.deepcopy(raw.get("customStyles") or {})
                widget.animations = copy.deepcopy(raw.get("animations") or [])
                widget.binding = copy.deepcopy(raw.get("binding"))
                id_map[old_id] = widget.id
                created.append(widget.name)
            for raw, widget in zip(source, [project.find_widget(name) for name in created]):
                parent_id = raw.get("parentId")
                if parent_id in id_map:
                    widget.parentId = id_map[parent_id]  # stays where it was inside the pasted container
                    continue
                if any(candidate.id == parent_id for candidate in page.widgets):
                    widget.parentId = parent_id
                widget.props["x"] = int(widget.props.get("x", 0)) + 12
                widget.props["y"] = int(widget.props.get("y", 0)) + 12
        if self.document.execute("Paste Widgets", mutate):
            self.clearSelection()
            for widget in self.page.widgets:
                if widget.name in created:
                    self.widget_items[widget.id].setSelected(True)

    def _selected_group(self):
        selected = {item for item in self.selectedItems() if isinstance(item, WidgetItem)}
        return [item for item in selected if item.parentItem() not in selected]

    def select_all(self):
        for item in self.widget_items.values():
            item.setSelected(True)

    def duplicate_selected(self):
        clipboard = self.document.clipboard
        self.copy_selected()
        self.paste()
        self.document.clipboard = clipboard

    def _apply_positions(self, description, positions):
        def mutate(project):
            for widget in project.widgets:
                if widget.id in positions:
                    widget.props.update(positions[widget.id])
        self.document.execute(description, mutate)

    @staticmethod
    def _parent_offset(item, axis):
        """Properties are relative to the container; the comparison is made on the scene."""
        parent = item.parentItem()
        if parent is None:
            return 0
        return int(parent.scenePos().x() if axis == "x" else parent.scenePos().y())

    def align_selected(self, side):
        items = self._selected_group()
        if len(items) < 2:
            return
        axis, size = ("x", "width") if side in ("left", "center", "right") else ("y", "height")
        starts = [item.props[axis] + self._parent_offset(item, axis) for item in items]
        ends = [start + item.props[size] for start, item in zip(starts, items)]
        positions = {}
        for item in items:
            if side in ("left", "top"):
                value = min(starts)
            elif side in ("right", "bottom"):
                value = max(ends) - item.props[size]
            else:
                value = (min(starts) + max(ends) - item.props[size]) // 2
            positions[item.widget_id] = {axis: value - self._parent_offset(item, axis)}
        self._apply_positions("Align widgets", positions)

    def distribute_selected(self, axis):
        items = self._selected_group()
        if len(items) < 3:
            return
        key, size = ("x", "width") if axis == "horizontal" else ("y", "height")
        absolute = lambda item: item.props[key] + self._parent_offset(item, key)
        ordered = sorted(items, key=absolute)
        start, end = absolute(ordered[0]), absolute(ordered[-1]) + ordered[-1].props[size]
        gap = (end - start - sum(item.props[size] for item in ordered)) / (len(ordered) - 1)
        positions, cursor = {}, float(start)
        for item in ordered:
            positions[item.widget_id] = {key: round(cursor) - self._parent_offset(item, key)}
            cursor += item.props[size] + gap
        self._apply_positions("Distribute widgets", positions)

    def change_z(self, front):
        names = self.selected_names()
        if not names:
            return
        def mutate(project):
            page = next(page for page in project.pages if page.id == self.page_id)
            for name in names:
                widget = project.find_widget(name)
                page.widgets.remove(widget)
                if front:
                    page.widgets.append(widget)
                else:
                    page.widgets.insert(0, widget)
        self.document.execute("Widget Order", mutate)


class DesignerView(QGraphicsView):
    def __init__(self, document, page_id=None, parent=None):
        self.designer_scene = DesignerScene(document, page_id, parent)
        super().__init__(self.designer_scene, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setAcceptDrops(True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.pending_type = None

    @property
    def document(self):
        return self.designer_scene.document

    def arm_widget(self, widget_type):
        """The next click on the page places this widget; None takes that back."""
        self.pending_type = widget_type
        if widget_type:
            self.viewport().setCursor(Qt.CrossCursor)
        else:
            self.viewport().unsetCursor()

    def mousePressEvent(self, event):
        if self.pending_type and event.button() == Qt.LeftButton:
            self.designer_scene.add_widget(self.pending_type, self.mapToScene(event.position().toPoint()))
            # The toolbox armed every page, not knowing which one is shown: the others must not
            # place a second widget at the first click they get.
            for view in self.window().findChildren(DesignerView) or [self]:
                view.arm_widget(None)
            self.arm_widget(None)
            event.accept()
            return
        super().mousePressEvent(event)

    def contextMenuEvent(self, event):
        scene = self.designer_scene
        item = scene.item_at(self.mapToScene(event.pos()))
        if item is not None and not item.isSelected():
            scene.clearSelection()
            item.setSelected(True)
        scene.contextMenuRequested.emit(event.globalPos())
        event.accept()

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
            zoom = self.transform().m11() * factor
            if 0.5 <= zoom <= 4:
                self.scale(factor, factor)
            event.accept()
            return
        super().wheelEvent(event)

    def keyPressEvent(self, event):
        step = 10 if event.modifiers() & Qt.ShiftModifier else 1
        moves = {Qt.Key_Left: (-step, 0), Qt.Key_Right: (step, 0), Qt.Key_Up: (0, -step), Qt.Key_Down: (0, step)}
        if event.key() in moves:
            self.designer_scene.move_selected(*moves[event.key()])
        elif event.key() == Qt.Key_Delete:
            self.designer_scene.delete_selected()
        elif event.matches(QKeySequence.Copy):
            self.designer_scene.copy_selected()
        elif event.matches(QKeySequence.Cut):
            self.designer_scene.copy_selected(cut=True)
        elif event.matches(QKeySequence.Paste):
            self.designer_scene.paste()
        else:
            super().keyPressEvent(event)
            return
        event.accept()

    def _show_drop_preview(self, event):
        widget_type = bytes(event.mimeData().data(WIDGET_MIME)).decode()
        if is_component(widget_type):
            return
        self.designer_scene.show_drop_preview(widget_type, self.mapToScene(event.position().toPoint()))

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(WIDGET_MIME):
            self._show_drop_preview(event)
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat(WIDGET_MIME):
            self._show_drop_preview(event)
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dragLeaveEvent(self, event):
        self.designer_scene.hide_drop_preview()
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasFormat(WIDGET_MIME):
            self.designer_scene.hide_drop_preview()
            widget_type = bytes(event.mimeData().data(WIDGET_MIME)).decode()
            self.designer_scene.add_widget(widget_type, self.mapToScene(event.position().toPoint()), centered=True)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)


class ComponentTray(QListWidget):
    """Strip of the non-visual components, like that of the Timer in Visual Basic."""

    selectionChangedTo = Signal(list)
    activated_ = Signal(str)

    def __init__(self, document, parent=None):
        super().__init__(parent)
        self.document = document
        self.setFlow(QListWidget.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(QListWidget.Adjust)
        self.setAcceptDrops(True)
        self.setObjectName("componentTray")
        self.setIconSize(QSize(18, 18))
        self.document.reset.connect(self.rebuild)
        self.itemSelectionChanged.connect(self._selection_changed)
        self.itemDoubleClicked.connect(lambda item: self.activated_.emit(item.data(Qt.UserRole)))
        self.rebuild()

    def rebuild(self):
        self.blockSignals(True)
        selected = {item.data(Qt.UserRole) for item in self.selectedItems()}
        self.clear()
        for widget in self.document.project.widgets:
            if is_component(widget.type):
                item = QListWidgetItem(widget_icon(widget.type), widget.name)
                item.setData(Qt.UserRole, widget.name)
                self.addItem(item)
                item.setSelected(widget.name in selected)
        self.blockSignals(False)

    def _selection_changed(self):
        names = [item.data(Qt.UserRole) for item in self.selectedItems()]
        if names:
            self.selectionChangedTo.emit(names)

    def keyPressEvent(self, event):
        names = [item.data(Qt.UserRole) for item in self.selectedItems()]
        if event.key() == Qt.Key_Delete and names:
            self.document.execute("Delete Widget", lambda project: [project.remove_widget(name) for name in names])
            event.accept()
            return
        super().keyPressEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(WIDGET_MIME) and is_component(bytes(event.mimeData().data(WIDGET_MIME)).decode()):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        self.dragEnterEvent(event)

    def dropEvent(self, event):
        widget_type = bytes(event.mimeData().data(WIDGET_MIME)).decode()
        if is_component(widget_type):
            self.document.execute("Add component", lambda project: project.add_widget(project.pages[0], widget_type))
            event.acceptProposedAction()


class ToolboxPanel(QWidget):
    """The Toolbox with the search field."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        self.search = QLineEdit()
        self.search.setPlaceholderText(tr("Search a widget"))
        self.search.setClearButtonEnabled(True)
        layout.addWidget(self.search)
        self.toolbox = Toolbox()
        layout.addWidget(self.toolbox, 1)
        self.search.textChanged.connect(self.toolbox.filter)


class Toolbox(QListWidget):
    CATEGORY_ROLE = Qt.UserRole + 1
    NAMES = {"Basic": "Basic", "Input": "Input", "Display": "Display", "Data": "Data", "Media": "Media", "Navigation": "Navigation", "Container": "Containers", "Components": "Components", "Hardware": "Hardware"}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setIconSize(QSize(18, 18))
        self.definitions = {**widget_definitions(), **COMPONENTS}
        self.populate()
        self.itemDoubleClicked.connect(self._arm_views)

    def populate(self):
        self.clear()
        categories = {}
        for widget_type, definition in self.definitions.items():
            categories.setdefault(definition.get("category", "Basic"), []).append((widget_type, definition))
        for category, entries in categories.items():
            header = QListWidgetItem(tr(self.NAMES.get(category, category)))
            header.setFlags(Qt.NoItemFlags)
            font = header.font()
            font.setBold(True)
            header.setFont(font)
            header.setData(self.CATEGORY_ROLE, category)
            self.addItem(header)
            for widget_type, definition in entries:
                item = QListWidgetItem(widget_icon(widget_type), tr(definition.get("name", widget_type)))
                item.setData(Qt.UserRole, widget_type)
                item.setToolTip(widget_type)
                self.addItem(item)

    def retranslate(self):
        self.populate()

    def widget_items(self):
        return [self.item(row) for row in range(self.count()) if self.item(row).data(Qt.UserRole)]

    def filter(self, text):
        needle = text.strip().lower()
        visible = set()
        for row in range(self.count()):
            item = self.item(row)
            if item.data(Qt.UserRole):
                shown = needle in item.text().lower() or needle in item.data(Qt.UserRole).lower()
                item.setHidden(not shown)
                if shown:
                    visible.add(self.definitions[item.data(Qt.UserRole)].get("category", "Basic"))
        for row in range(self.count()):
            item = self.item(row)
            if not item.data(Qt.UserRole):
                item.setHidden(item.data(self.CATEGORY_ROLE) not in visible)

    @staticmethod
    def _views():
        return [view for widget in QApplication.topLevelWidgets() for view in widget.findChildren(DesignerView)]

    def _arm_views(self, item):
        for view in self._views():
            view.arm_widget(item.data(Qt.UserRole))

    def startDrag(self, actions):
        item = self.currentItem()
        if not item or not item.data(Qt.UserRole):
            return
        mime = QMimeData()
        mime.setData(WIDGET_MIME, item.data(Qt.UserRole).encode())
        mime.setText(item.data(Qt.UserRole))
        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.setPixmap(drag_chip(item.text().strip(), self.palette()))
        drag.setHotSpot(QPoint(-DRAG_CHIP_OFFSET, -DRAG_CHIP_OFFSET))
        drag.exec(Qt.CopyAction)
