"""The Block Manager: what is installed, where it comes from, and how to add or remove a block."""

import html

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QTextBrowser, QTreeWidget, QTreeWidgetItem, QVBoxLayout

from lvgl_mpy_studio.core import blocks, components
from lvgl_mpy_studio.core.blocks import BlockError
from lvgl_mpy_studio.core.i18n import tr

ORIGINS = {"standard": "Shipped with the IDE", "user": "Installed by you", "project": "Only inside this project"}


def used_blocks(project):
    """{block id: names of the components of the project that use it}."""
    used = {}
    for widget in project.widgets:
        if components.block_for(widget.type) is not None:
            used.setdefault(widget.type, []).append(widget.name)
    return used


class BlocksDialog(QDialog):
    """Lists the blocks and changes the user's blocks folder; blocksChanged after each change."""

    blocksChanged = Signal()

    def __init__(self, document, parent=None):
        super().__init__(parent)
        self.document = document
        self.setWindowTitle(tr("Block Manager"))
        self.resize(820, 560)
        layout = QVBoxLayout(self)
        intro = QLabel(tr("Blocks add components to the toolbox: a folder with a description and MicroPython modules. The simulator runs the code of a block on this computer, as it runs the code of a project: install blocks from people you trust."))
        intro.setWordWrap(True)
        layout.addWidget(intro)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels([tr("Name"), tr("Version"), tr("Origin"), tr("Author"), tr("Licence"), tr("Used by")])
        self.tree.setRootIsDecorated(False)
        self.tree.itemSelectionChanged.connect(self._show_selected)
        layout.addWidget(self.tree, 2)
        self.details = QTextBrowser()
        self.details.setOpenExternalLinks(False)
        layout.addWidget(self.details, 1)
        self.problems = QLabel()
        self.problems.setWordWrap(True)
        self.problems.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.problems.setStyleSheet("color: #D00000")
        layout.addWidget(self.problems)
        row = QHBoxLayout()
        self.add_button = QPushButton(tr("Add from Folder…"))
        self.install_button = QPushButton(tr("Install from Project"))
        self.remove_button = QPushButton(tr("Remove"))
        self.reload_button = QPushButton(tr("Reload"))
        self.folder_button = QPushButton(tr("Open Blocks Folder"))
        for button, slot in ((self.add_button, self.add_block), (self.install_button, self.install_selected), (self.remove_button, self.remove_selected), (self.reload_button, self.reload), (self.folder_button, self.open_folder)):
            button.clicked.connect(slot)
            row.addWidget(button)
        row.addStretch(1)
        layout.addLayout(row)
        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.populate()

    def populate(self, select=None):
        used = used_blocks(self.document.project)
        self.tree.clear()
        for block in sorted(components.BLOCKS.values(), key=lambda item: (item.origin != "standard", item.manifest["name"].lower())):
            manifest = block.manifest
            item = QTreeWidgetItem([tr(manifest["name"]), manifest["version"], tr(ORIGINS[block.origin]), manifest["author"], manifest["license"], ", ".join(used.get(block.id, []))])
            item.setData(0, Qt.UserRole, block.id)
            self.tree.addTopLevelItem(item)
            if block.id == select:
                self.tree.setCurrentItem(item)
        for column in range(self.tree.columnCount()):
            self.tree.resizeColumnToContents(column)
        self.problems.setText("\n".join(tr("Not loaded: {folder} — {reason}", folder=folder, reason=reason) for folder, reason in components.PROBLEMS))
        self.problems.setVisible(bool(components.PROBLEMS))
        if self.tree.currentItem() is None and self.tree.topLevelItemCount():
            self.tree.setCurrentItem(self.tree.topLevelItem(0))
        self._show_selected()

    def selected(self):
        item = self.tree.currentItem()
        return components.BLOCKS.get(item.data(0, Qt.UserRole)) if item else None

    def _show_selected(self):
        block = self.selected()
        self.remove_button.setEnabled(bool(block and block.origin == "user"))
        self.install_button.setEnabled(bool(block and block.origin == "project"))
        if block is None:
            self.details.clear()
            return
        manifest = block.manifest
        lines = [f"<b>{html.escape(tr(manifest['name']))}</b> — <code>{manifest['id']}</code>", html.escape(tr(manifest["description"]))]
        if manifest["properties"]:
            lines.append("<b>" + tr("Properties") + ":</b> " + ", ".join(item["name"] for item in manifest["properties"]))
        if manifest["methods"]:
            lines.append("<b>" + tr("Methods") + ":</b> " + ", ".join(f"{item['name']}({item.get('arguments', '')})" for item in manifest["methods"]))
        if manifest["events"]:
            lines.append("<b>" + tr("Events") + ":</b> " + ", ".join(item["name"] for item in manifest["events"]))
        lines.append("<b>" + tr("In the simulator") + ":</b> " + (tr("its own module") if manifest.get("simulator") else tr("a stand-in whose methods do nothing")))
        if block.folder:
            lines.append("<b>" + tr("Folder") + ":</b> " + html.escape(block.folder))
        self.details.setHtml("<br>".join(lines))

    def _changed(self, select=None):
        """Read the blocks again, keeping those the open project carries, and tell the IDE."""
        carried = {"assets": {"blocks": {block.id: block.to_dict() for block in components.BLOCKS.values() if block.origin == "project"}}}
        components.reload_blocks()
        components.register_project_blocks(carried)
        self.populate(select)
        self.blocksChanged.emit()

    def reload(self):
        self._changed(self.selected().id if self.selected() else None)

    def open_folder(self):
        folder = blocks.user_dir()
        folder.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    def add_block(self):
        source = QFileDialog.getExistingDirectory(self, tr("Choose the folder of the block"), str(blocks.user_dir().parent))
        if source:
            self.install_folder(source)

    def install_folder(self, source):
        try:
            candidate = blocks.load_block(source, "user", check_name=False)
        except BlockError as exc:
            QMessageBox.warning(self, tr("Block Manager"), tr("This folder is not a block that can be used: {reason}", reason=exc))
            return False
        existing = components.BLOCKS.get(candidate.id)
        if candidate.id == "timer":
            QMessageBox.warning(self, tr("Block Manager"), tr("“timer” is the name of the built-in Timer: the block needs another id."))
            return False
        if existing is not None:
            question = tr("The block {name} {version} is already there ({origin}). Replace it with version {new}?", name=existing.manifest["name"], version=existing.manifest["version"], origin=tr(ORIGINS[existing.origin]), new=candidate.manifest["version"])
            if QMessageBox.question(self, tr("Block Manager"), question, QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
                return False
        try:
            blocks.install_block(source)
        except (BlockError, OSError) as exc:
            QMessageBox.critical(self, tr("Block Manager"), str(exc))
            return False
        self._changed(candidate.id)
        return True

    def install_selected(self):
        block = self.selected()
        if block is None or block.origin != "project":
            return False
        try:
            blocks.write_block(block)
        except OSError as exc:
            QMessageBox.critical(self, tr("Block Manager"), str(exc))
            return False
        self._changed(block.id)
        return True

    def remove_selected(self):
        block = self.selected()
        if block is None or block.origin != "user":
            return False
        users = used_blocks(self.document.project).get(block.id, [])
        question = tr("Remove the block {name} from this computer?", name=tr(block.manifest["name"]))
        if users:
            question += "\n\n" + tr("The open project uses it ({names}): it keeps working with the copy inside the project.", names=", ".join(users))
        if QMessageBox.question(self, tr("Block Manager"), question, QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
            return False
        kept = {"assets": {"blocks": {block.id: block.to_dict()}}} if users else {}
        blocks.remove_block(block.id)
        components.reload_blocks()
        components.register_project_blocks(kept)
        self._changed()
        return True
