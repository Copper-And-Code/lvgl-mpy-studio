
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QInputDialog, QMenu, QMessageBox, QTreeWidgetItem

from lvgl_mpy_studio.core.components import is_component
from lvgl_mpy_studio.core.events import events_for
from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.core.model import page_constant
from lvgl_mpy_studio.core.modules import ModuleError, create_module, delete_module, module_references, rename_module, validate_module_name
from lvgl_mpy_studio.ui.designer.scene import DesignerView


# A new module starts with the same imports as handlers: without them ui and lv do not exist in the module.
NEW_MODULE_SOURCE = "import lvgl as lv\nimport ui\n\n\n"


class ProjectTreeMixin:
    """Project tree: pages, components and Python modules. A part of MainWindow."""

    def rebuild_project_tree(self):
        self.project_tree.blockSignals(True)
        self.project_tree.clear()
        for page in self.document.project.pages:
            page_item = QTreeWidgetItem((page.name,))
            page_item.setData(0, Qt.UserRole, ("page", page.id))
            self.project_tree.addTopLevelItem(page_item)
            for widget in page.widgets:
                item = QTreeWidgetItem((f"{widget.name} — {widget.type}",))
                item.setData(0, Qt.UserRole, ("widget", widget.name))
                page_item.addChild(item)
        # After the pages, so their positions in the tree do not change.
        modules_item = QTreeWidgetItem((tr("Python Modules"),))
        modules_item.setData(0, Qt.UserRole, ("modules", None))
        modules_item.setToolTip(0, tr(".py files of the project, imported by name from handlers, the general code and each other"))
        self.project_tree.addTopLevelItem(modules_item)
        for module in self.document.project.modules:  # in project order, the same as the code editor
            item = QTreeWidgetItem((f"{module.name}.py",))
            item.setData(0, Qt.UserRole, ("pymodule", module.id))
            modules_item.addChild(item)
        self.project_tree.expandAll()
        self.project_tree.blockSignals(False)

    def current_designer(self):
        widget = self.tabs.currentWidget()
        if isinstance(widget, DesignerView):
            return widget
        return next(iter(self.designers.values()))[1]

    def _tree_selection(self):
        items = self.project_tree.selectedItems()
        if not items:
            return
        kind, value = items[0].data(0, Qt.UserRole)
        if kind == "page":
            self.tabs.setCurrentWidget(self.designers[value][1])
            return
        if kind in ("modules", "pymodule"):  # opened with a double click, like handlers
            return
        widget = self.document.project.find_widget(value)
        if not widget:
            return
        if is_component(widget.type):
            self.properties.set_selection([widget.name])
            return
        page = next(page for page in self.document.project.pages if widget in page.widgets)
        view = self.designers[page.id][1]
        view.designer_scene.clearSelection()
        view.designer_scene.widget_items[widget.id].setSelected(True)
        self.tabs.setCurrentWidget(view)

    def _tree_activated(self, item):
        kind, value = item.data(0, Qt.UserRole)
        if kind == "widget":
            self.open_handler(value)
        elif kind == "pymodule":
            self.open_module(self._module_name(value))

    def _project_context_menu(self, position):
        self._project_menu(self.project_tree.itemAt(position)).exec(self.project_tree.viewport().mapToGlobal(position))

    def _project_menu(self, item):
        """The menu of the node: module actions on the Python Modules branch, page actions elsewhere."""
        menu = QMenu(self)
        kind = item.data(0, Qt.UserRole)[0] if item else None
        if kind in ("modules", "pymodule"):
            self.project_tree.setCurrentItem(item)
            menu.addAction(self.new_module_action)
            if kind == "pymodule":
                menu.addSeparator()
                menu.addActions((self.open_module_action, self.rename_module_action, self.delete_module_action))
        else:
            menu.addActions((self.add_page_action, self.rename_page_action, self.delete_page_action, self.initial_page_action))
        return menu

    def _component_activated(self, name):
        widget = self.document.project.find_widget(name)
        if widget and events_for(widget.type):
            self.open_handler(name)

    def open_handler(self, name, event=None):
        self.tabs.setCurrentWidget(self.code_panel)
        self.code_panel.open_handler(name, event)

    def _module_name(self, module_id):
        return next((module.name for module in self.document.project.modules if module.id == module_id), None)

    def _selected_module_name(self):
        items = self.project_tree.selectedItems()
        if items:
            kind, value = items[0].data(0, Qt.UserRole)
            if kind == "pymodule":
                return self._module_name(value)
        current = self.code_panel.module() if self.tabs.currentWidget() is self.code_panel else None
        return current.name if current else None

    def open_module(self, name, line=None):
        if not name:
            return False
        self.tabs.setCurrentWidget(self.code_panel)
        return self.code_panel.open_module(name, line)

    def _ask_module_name(self, title, current=""):
        """Ask for a name until it is valid or the user cancels; the check is that of core.modules."""
        renamed = next((module for module in self.document.project.modules if module.name == current), None)
        text = current
        while True:
            name, accepted = QInputDialog.getText(self, title, tr("Module name, without .py:"), text=text)
            name = name.strip().removesuffix(".py")
            if not accepted or not name or (current and name == current):
                return None
            error = validate_module_name(name, self.document.project, exclude=renamed)
            if error is None:
                return name
            message = tr("Invalid module name: {error}", error=error)
            self.append_error(message)
            QMessageBox.warning(self, title, message)
            text = name

    def _show_module_warnings(self, warnings):
        self._show_warnings(warnings)
        if warnings:
            self.statusBar().showMessage(tr("Code still imports a module that no longer has that name: see Output ({count})", count=len(warnings)), 8000)

    def new_module(self):
        if self.document.read_only:
            return False
        name = self._ask_module_name(tr("New Python Module"))
        if name is None:
            return False
        try:
            self.document.execute(tr("New Module"), lambda project: create_module(project, name, NEW_MODULE_SOURCE))
        except ModuleError as exc:
            self.append_error(str(exc))
            return False
        self.open_module(name)
        return True

    def rename_module(self):
        old = self._selected_module_name()
        if old is None or self.document.read_only:
            return False
        name = self._ask_module_name(tr("Rename Module"), old)
        if name is None:
            return False
        references = module_references(self.document.project, old)
        if references:  # imports are not rewritten: the risk is stated before, not after
            text = tr("Code still imports {old}: after renaming it to {new}, those imports will stop with ImportError until you update them by hand.", old=old, new=name)
            if QMessageBox.warning(self, tr("Rename Module"), text + "\n" + "\n".join(references), QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
                return False
        warnings = []
        try:
            self.document.execute(tr("Rename Module"), lambda project: warnings.extend(rename_module(project, old, name)))
        except ModuleError as exc:
            self.append_error(str(exc))
            return False
        self._show_module_warnings(warnings)
        return True

    def delete_module(self):
        name = self._selected_module_name()
        if name is None or self.document.read_only:
            return False
        references = module_references(self.document.project, name)
        question = tr("Delete the module {name}.py? Undo can bring it back.", name=name)
        if references:
            # The risk is stated before: the error would come only when running, on the PC or on the board.
            question += "\n\n" + tr("Code still imports it: until you update it, the app will stop with ImportError when it reaches that import.") + "\n" + "\n".join(references)
            answer = QMessageBox.warning(self, tr("Delete Module"), question, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            answer = QMessageBox.question(self, tr("Delete Module"), question, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer != QMessageBox.Yes:
            return False
        warnings = []
        self.document.execute(tr("Delete Module"), lambda project: warnings.extend(delete_module(project, name)))
        self._show_module_warnings(warnings)
        return True

    def add_page(self):
        name = f"page{len(self.document.project.pages) + 1}"
        self.document.execute(tr("Add Page"), lambda project: project.pages.append(project.new_page(name)))

    def _selected_page(self):
        items = self.project_tree.selectedItems()
        if items:
            kind, value = items[0].data(0, Qt.UserRole)
            if kind == "page":
                return next(page for page in self.document.project.pages if page.id == value)
        return self.current_designer().designer_scene.page

    def rename_page(self):
        page = self._selected_page()
        name, accepted = QInputDialog.getText(self, tr("Rename Page"), tr("Name:"), text=page.name)
        if not accepted or not name or name == page.name:
            return
        if any(page_constant(item.name) == page_constant(name) for item in self.document.project.pages if item.id != page.id):
            self.append_error(tr("A page named {name} already exists", name=name))
            return
        warnings = []
        self.document.execute(tr("Rename Page"), lambda project: warnings.extend(project.rename_page(next(item for item in project.pages if item.id == page.id), name)))
        self._show_warnings(warnings)

    def delete_page(self):
        if len(self.document.project.pages) == 1:
            self.append_error(tr("The last page cannot be deleted"))
            return
        page = self._selected_page()
        self.document.execute(tr("Delete Page"), lambda project: project.remove_page(next(item for item in project.pages if item.id == page.id)))

    def set_initial_page(self):
        page = self._selected_page()
        def mutate(project):
            selected = next(item for item in project.pages if item.id == page.id)
            project.pages.remove(selected)
            project.pages.insert(0, selected)
            project.currentPageId = selected.id
        self.document.execute(tr("Initial Page"), mutate)
