from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QAbstractButton, QComboBox, QDockWidget, QGroupBox, QLabel, QLineEdit, QMenu, QPlainTextEdit, QTabWidget, QTreeWidget
from PySide6.QtGui import QAction

from lvgl_mpy_studio.core.i18n import set_language, tr


def _translate_property(obj, prop, setter, value=None):
    key = f"_lvgl_source_{prop}"
    source = obj.property(key)
    if source is None:
        source = getattr(obj, prop)() if value is None else value
        if not source:
            return
        obj.setProperty(key, source)
    setter(tr(source))


def retranslate_widget(root):
    objects = [root, *root.findChildren(object)]
    for obj in objects:
        if hasattr(obj, "retranslate"):
            obj.retranslate()
        if isinstance(obj, QAction):
            _translate_property(obj, "text", obj.setText)
            _translate_property(obj, "toolTip", obj.setToolTip)
            _translate_property(obj, "statusTip", obj.setStatusTip)
        if isinstance(obj, (QAbstractButton, QLabel)):
            _translate_property(obj, "text", obj.setText)
        if isinstance(obj, (QLineEdit, QPlainTextEdit)):
            _translate_property(obj, "placeholderText", obj.setPlaceholderText)
        if isinstance(obj, QDockWidget):
            _translate_property(obj, "windowTitle", obj.setWindowTitle)
        if isinstance(obj, (QGroupBox, QMenu)):
            _translate_property(obj, "title", obj.setTitle)
        if isinstance(obj, QComboBox) and not obj.property("_lvgl_dynamic_items"):
            for index in range(obj.count()):
                key = f"_lvgl_source_item_{index}"
                source = obj.property(key)
                if source is None:
                    source = obj.itemText(index)
                    obj.setProperty(key, source)
                obj.setItemText(index, tr(source))
        if isinstance(obj, QTabWidget):
            for index in range(obj.count()):
                page = obj.widget(index)
                if page.property("_lvgl_dynamic_tab"):
                    continue
                source = page.property("_lvgl_source_tab")
                if source is None:
                    source = obj.tabText(index)
                    page.setProperty("_lvgl_source_tab", source)
                obj.setTabText(index, tr(source))
        if isinstance(obj, QTreeWidget):
            item = obj.headerItem()
            sources = obj.property("_lvgl_source_headers")
            if sources is None:
                sources = [item.text(index) for index in range(obj.columnCount())]
                obj.setProperty("_lvgl_source_headers", sources)
            for index, source in enumerate(sources):
                item.setText(index, tr(source))


def apply_language(root, language):
    selected = set_language(language)
    QSettings("CopperAndCode", "LVGL MPY Studio").setValue("language", selected)
    retranslate_widget(root)
    return selected
