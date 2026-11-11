import copy

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QSpinBox, QTreeWidget, QTreeWidgetItem, QVBoxLayout

from lvgl_mpy_studio.core.boards import ADAPTERS, builtin_profiles, portable_profile, profile_diagnostics
from lvgl_mpy_studio.core.i18n import tr


class ProfileManagerDialog(QDialog):
    def __init__(self, store, parent=None):
        super().__init__(parent)
        self.store = store
        self.state = store.snapshot()
        self.profiles_data = {profile["id"]: profile for profile in store.profiles()}
        self._loading = False
        self.setWindowTitle(tr("Board Profile Manager"))
        self.resize(1050, 600)
        layout = QVBoxLayout(self)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels([tr("Name"), tr("Origin"), tr("Adapter"), tr("Logical"), tr("Physical"), tr("Revision"), tr("Status")])
        self.tree.setRootIsDecorated(False)
        self.tree.itemSelectionChanged.connect(self._load_selected)
        layout.addWidget(self.tree, 1)
        form = QFormLayout()
        self.name = QLineEdit()
        self.identifier = QLineEdit()
        self.identifier.setReadOnly(True)
        self.adapter = QComboBox()
        self.adapter.addItems(sorted(ADAPTERS))
        self.revision = QSpinBox(minimum=1, maximum=1000000)
        self.logical_width = QSpinBox(minimum=1, maximum=10000)
        self.logical_height = QSpinBox(minimum=1, maximum=10000)
        self.physical_width = QSpinBox(minimum=1, maximum=10000)
        self.physical_height = QSpinBox(minimum=1, maximum=10000)
        self.scale = QSpinBox(minimum=1, maximum=16)
        self.name.textEdited.connect(self._draft_changed)
        self.adapter.activated.connect(self._draft_changed)
        for editor in (self.revision, self.logical_width, self.logical_height, self.physical_width, self.physical_height, self.scale):
            editor.valueChanged.connect(self._draft_changed)
        form.addRow(tr("Name"), self.name)
        form.addRow(tr("Stable ID"), self.identifier)
        form.addRow(tr("Adapter"), self.adapter)
        form.addRow(tr("Revision"), self.revision)
        form.addRow(tr("Logical Resolution"), self.logical_width)
        form.addRow("", self.logical_height)
        form.addRow(tr("Physical Resolution"), self.physical_width)
        form.addRow("", self.physical_height)
        form.addRow(tr("Scale"), self.scale)
        form.addRow("", QLabel(tr("Driver and buffers are fixed by the adapter firmware.")))
        layout.addLayout(form)
        buttons = QHBoxLayout()
        for text, callback in ((tr("New"), self.new), (tr("Edit"), self.apply_edit), (tr("Duplicate"), self.duplicate), (tr("Delete"), self.delete), (tr("Restore Default"), self.restore_default), (tr("Restore Hidden Profiles"), self.restore_hidden)):
            button = QPushButton(text)
            button.clicked.connect(callback)
            buttons.addWidget(button)
        layout.addLayout(buttons)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        self.buttons.button(QDialogButtonBox.Apply).setText(tr("Apply"))
        self.buttons.button(QDialogButtonBox.Cancel).setText(tr("Cancel"))
        self.buttons.button(QDialogButtonBox.Apply).clicked.connect(self._apply)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        self.refresh()

    def refresh(self, selected=None):
        self.tree.clear()
        names = [profile["name"] for profile in self.profiles_data.values()]
        for profile in self.profiles_data.values():
            origin = tr("Built-in") if profile.get("origin") == "builtin" else tr("Custom profile")
            valid = not profile_diagnostics(profile)
            display_name = f"{profile['name']} [{profile['id']}]" if names.count(profile["name"]) > 1 else profile["name"]
            item = QTreeWidgetItem([display_name, origin, profile["adapter"], f"{profile['logicalWidth']}×{profile['logicalHeight']}", f"{profile['physicalWidth']}×{profile['physicalHeight']}", str(profile["revision"]), tr("Valid") if valid else tr("Invalid")])
            item.setData(0, Qt.UserRole, profile["id"])
            self.tree.addTopLevelItem(item)
            if profile["id"] == selected:
                self.tree.setCurrentItem(item)
        if self.tree.currentItem() is None and self.tree.topLevelItemCount():
            self.tree.setCurrentItem(self.tree.topLevelItem(0))

    def selected(self):
        items = self.tree.selectedItems()
        return self.profiles_data.get(items[0].data(0, Qt.UserRole)) if items else None

    def _load_selected(self):
        profile = self.selected()
        if not profile:
            return
        self._loading = True
        self.name.setText(profile["name"])
        self.identifier.setText(profile["id"])
        self.adapter.setCurrentText(profile["adapter"])
        self.revision.setValue(profile["revision"])
        self.logical_width.setValue(profile["logicalWidth"])
        self.logical_height.setValue(profile["logicalHeight"])
        self.physical_width.setValue(profile["physicalWidth"])
        self.physical_height.setValue(profile["physicalHeight"])
        self.scale.setValue(profile["scale"])
        self._loading = False

    def _draft_changed(self, *_args):
        if self._loading or not self.selected():
            return
        original = self.selected()
        profile = self._edited_profile()
        old_content = {key: value for key, value in original.items() if key not in {"origin", "revision"}}
        new_content = {key: value for key, value in profile.items() if key not in {"origin", "revision"}}
        if old_content != new_content and profile["revision"] <= original["revision"]:
            profile["revision"] = original["revision"] + 1
            self._loading = True
            self.revision.setValue(profile["revision"])
            self._loading = False
        self.profiles_data[profile["id"]] = profile

    def _edited_profile(self):
        original = self.selected()
        if not original:
            raise ValueError("profile.selection")
        profile = copy.deepcopy(original)
        profile.update(name=self.name.text(), adapter=self.adapter.currentText(), revision=self.revision.value(), logicalWidth=self.logical_width.value(), logicalHeight=self.logical_height.value(), physicalWidth=self.physical_width.value(), physicalHeight=self.physical_height.value(), scale=self.scale.value(), origin="custom")
        return profile

    def new(self):
        profile = self.store.new_profile()
        profile["origin"] = "custom"
        self.profiles_data[profile["id"]] = profile
        self.refresh(profile["id"])

    def apply_edit(self):
        self._draft_changed()
        profile = self._edited_profile()
        errors = profile_diagnostics(profile)
        if errors:
            QMessageBox.warning(self, tr("Invalid"), "; ".join(f"{item['code']}:{item['path']}" for item in errors))
            return
        self.profiles_data[profile["id"]] = profile
        self.refresh(profile["id"])

    def duplicate(self):
        source = self.selected()
        if source:
            profile = self.store.new_profile(source)
            profile["origin"] = "custom"
            self.profiles_data[profile["id"]] = profile
            self.refresh(profile["id"])

    def delete(self):
        profile = self.selected()
        if profile and QMessageBox.question(self, tr("Delete"), tr("Delete profile {name}? Projects keep their portable copy.", name=profile["name"])) == QMessageBox.Yes:
            del self.profiles_data[profile["id"]]
            self.refresh()

    def restore_default(self):
        profile = self.selected()
        if not profile:
            return
        defaults = {item["id"]: item for item in builtin_profiles()}
        if profile["id"] in defaults:
            restored = copy.deepcopy(defaults[profile["id"]])
            restored["origin"] = "builtin"
            self.profiles_data[profile["id"]] = restored
            self.refresh(profile["id"])

    def restore_hidden(self):
        customized = self.state["custom"]
        for default in builtin_profiles():
            profile = copy.deepcopy(customized.get(default["id"], default))
            profile["origin"] = "custom" if default["id"] in customized else "builtin"
            self.profiles_data.setdefault(profile["id"], profile)
        self.refresh()

    def _diagnostics(self):
        return [(profile, profile_diagnostics(profile)) for profile in self.profiles_data.values() if profile_diagnostics(profile)]

    def _apply(self):
        if self.selected():
            self.apply_edit()
        invalid = self._diagnostics()
        if invalid:
            QMessageBox.warning(self, tr("Invalid"), "; ".join(f"{item['code']}:{item['path']}" for _profile, errors in invalid for item in errors))
            return
        try:
            self.apply_to_store()
        except (OSError, ValueError) as exc:
            QMessageBox.critical(self, tr("Save Error"), str(exc))
            return
        self.accept()

    def apply_to_store(self):
        custom = {}
        for profile_id, profile in self.profiles_data.items():
            if profile.get("origin") == "custom":
                value = portable_profile(profile)
                custom[profile_id] = value
        builtin_ids = {profile["id"] for profile in builtin_profiles()}
        hidden = [profile_id for profile_id in builtin_ids if profile_id not in self.profiles_data]
        previous = self.store.snapshot()
        self.store.restore({"custom": custom, "hidden": hidden})
        try:
            self.store.save()
        except Exception:
            self.store.restore(previous)
            raise
