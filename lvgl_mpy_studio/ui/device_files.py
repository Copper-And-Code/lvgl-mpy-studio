"""Device → Upload Files…: files of the PC to a folder of the board, outside any project."""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFileDialog, QFormLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QVBoxLayout,
)

from lvgl_mpy_studio.core.i18n import tr

DESTINATIONS = ("/flash", "/sd", "/sd/bin", "/flash/bin", "/")
SKIPPED = {"__pycache__", ".git", ".hg", ".svn", ".venv"}


def folder_items(folder):
    """The files of a folder, with names relative to the folder's parent: the folder itself is copied."""
    folder = Path(folder)
    for path in sorted(folder.rglob("*")):
        relative = path.relative_to(folder.parent)
        if path.is_file() and not any(part in SKIPPED or part.startswith(".") for part in path.relative_to(folder).parts):
            yield path, relative.as_posix()


def run_line(text):
    """What to type at the board's prompt: a file of the board runs from its folder, as __main__; anything else is code."""
    text = text.strip()
    if text.endswith(".py") and "(" not in text and " " not in text:
        path = text if text.startswith("/") else "/" + text
        folder, name = path.rsplit("/", 1)
        return f"import os; os.chdir({folder or '/'!r}); exec(open({name!r}).read(), {{'__name__': '__main__', '__file__': {path!r}}})"
    return text


def protected_targets(items, destination):
    """The files that would replace what a board runs at power-on: boot.py anywhere, main.py at the top."""
    found = []
    for _local, name in items:
        target = ("/" + destination.strip("/") + "/" + name).replace("//", "/")
        parts = target.strip("/").split("/")
        if parts[-1] == "boot.py" or (parts[-1] == "main.py" and len(parts) <= 2):
            found.append(target)
    return found


def shadowed_modules(items, entries):
    """Names that would be both a folder and a module (.py or .mpy) in the destination, because of this upload.

    entries: the destination as list_dir gives it. MicroPython's import finds the folder first, as a
    package, so `import name` would no longer find the module.
    """
    folders = {entry["name"] for entry in entries if entry["dir"]}
    modules = {entry["name"].rsplit(".", 1)[0] for entry in entries if not entry["dir"] and entry["name"].endswith((".py", ".mpy"))}
    new = set()
    for _local, name in items:
        parts = name.strip("/").split("/")
        if len(parts) > 1:
            folders.add(parts[0])
            new.add(parts[0])
        elif parts[0].endswith((".py", ".mpy")):
            modules.add(parts[0].rsplit(".", 1)[0])
            new.add(parts[0].rsplit(".", 1)[0])
    return sorted(name for name in folders & modules if name in new)


class UploadFilesDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle(tr("Upload Files"))
        self.resize(560, 420)
        self.items = []
        self.list = QListWidget()
        self.list.setSelectionMode(QListWidget.ExtendedSelection)
        add_files = QPushButton(tr("Add Files…"))
        add_folder = QPushButton(tr("Add Folder…"))
        remove = QPushButton(tr("Remove"))
        add_files.clicked.connect(self.add_files)
        add_folder.clicked.connect(self.add_folder)
        remove.clicked.connect(self.remove_selected)
        buttons_row = QHBoxLayout()
        for button in (add_files, add_folder, remove):
            buttons_row.addWidget(button)
        buttons_row.addStretch(1)
        self.destination = QComboBox()
        self.destination.setEditable(True)
        self.destination.addItems(DESTINATIONS)
        self.destination.setCurrentText(settings.value("device/uploadFiles/destination", "/flash"))
        self.compile = QCheckBox(tr("Compile Python files to bytecode (.mpy)"))
        self.compile.setToolTip(tr("Faster to start and smaller. main.py and boot.py stay as source, and so must the programs that a shell runs from /bin or that an editor opens."))
        self.compile.setChecked(settings.value("device/uploadFiles/compile", False, type=bool))
        form = QFormLayout()
        form.addRow(tr("Folder on the board"), self.destination)
        form.addRow("", self.compile)
        note = QLabel(tr("Files with the same name are replaced; nothing else on the board changes. Binary files are copied as they are."))
        note.setWordWrap(True)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.button(QDialogButtonBox.Ok).setText(tr("Upload"))
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout = QVBoxLayout(self)
        layout.addWidget(self.list, 1)
        layout.addLayout(buttons_row)
        layout.addLayout(form)
        layout.addWidget(note)
        layout.addWidget(self.buttons)
        self._refresh()

    def _start(self):
        return self.settings.value("device/uploadFiles/folder", str(Path.home()))

    def add_items(self, items):
        known = {name for _local, name in self.items}
        for local, name in items:
            if name not in known:
                self.items.append((Path(local), name))
                known.add(name)
        self._refresh()

    def add_files(self):
        paths, _filter = QFileDialog.getOpenFileNames(self, tr("Add Files…"), self._start())
        if paths:
            self.settings.setValue("device/uploadFiles/folder", str(Path(paths[0]).parent))
            self.add_items((path, Path(path).name) for path in paths)

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, tr("Add Folder…"), self._start())
        if folder:
            self.settings.setValue("device/uploadFiles/folder", str(Path(folder).parent))
            self.add_items(folder_items(folder))

    def remove_selected(self):
        names = {item.data(Qt.UserRole) for item in self.list.selectedItems()}
        self.items = [entry for entry in self.items if entry[1] not in names]
        self._refresh()

    def _refresh(self):
        self.list.clear()
        for local, name in self.items:
            item = QListWidgetItem(f"{name}    ({local.stat().st_size if local.exists() else 0} B)")
            item.setData(Qt.UserRole, name)
            item.setToolTip(str(local))
            self.list.addItem(item)
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(bool(self.items))

    def accept(self):
        self.settings.setValue("device/uploadFiles/destination", self.destination.currentText().strip() or "/")
        self.settings.setValue("device/uploadFiles/compile", self.compile.isChecked())
        super().accept()

    def choice(self):
        return list(self.items), self.destination.currentText().strip() or "/", self.compile.isChecked()
