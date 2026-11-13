"""Files outside the project: a panel with a folder of the PC and editor tabs for its files, as in Thonny.

The Code tab belongs to the project with pages; these tabs edit files on disk, with the same
editor widget: highlighting, line numbers, completion of `lv.`, a syntax check with mpy-cross.
"""

import json
from pathlib import Path
import subprocess
import tempfile

from PySide6.QtCore import QDir, QFileSystemWatcher, QSortFilterProxyModel, Qt, QTimer, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QFileSystemModel, QHBoxLayout, QInputDialog, QLabel, QMenu, QMessageBox, QPushButton, QSplitter, QTreeView, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget,
)

from lvgl_mpy_studio.build.compiler import default_mpy_cross, parse_compiler_errors
from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.platform import CREATE_NO_WINDOW
from lvgl_mpy_studio.ui.code.editor import CodeEditor

MAX_BYTES = 2 * 1024 * 1024  # a text file larger than this is not opened in the editor
TEXT_SUFFIXES = {".py", ".txt", ".md", ".json", ".csv", ".ini", ".cfg", ".toml", ".yaml", ".yml", ".html", ".css", ".js", ""}


def readable_text(path):
    """The text of path, or None when it is too large or not text (binary data, an image, a .mpy)."""
    path = Path(path)
    if path.stat().st_size > MAX_BYTES:
        return None
    data = path.read_bytes()
    if b"\0" in data[:8192]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def syntax_errors(text, name="file.py"):
    """mpy-cross's opinion of the text: [{"line", "message"}], empty when it compiles or mpy-cross is missing."""
    compiler = default_mpy_cross()
    if not compiler.is_file():
        return []
    with tempfile.TemporaryDirectory(prefix="lvgl-mpy-studio-file-") as directory:
        source = Path(directory) / Path(name).name
        source.write_text(text, encoding="utf-8", newline="\n")
        result = subprocess.run([str(compiler), "-o", str(source.with_suffix(".mpy")), source.name], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=directory, creationflags=CREATE_NO_WINDOW)
        if result.returncode == 0:
            return []
        return [{"line": error["line"], "message": error.get("detail") or error["message"]} for error in parse_compiler_errors(result.stderr + result.stdout, directory)]


_API = None


def lvgl_completions(qualified):
    """Completion for files: the names of `lv.`, which do not depend on a project."""
    global _API
    parts = qualified.split(".")
    if parts[0] != "lv" or len(parts) != 2:
        return []
    if _API is None:
        _API = json.loads((Path(__file__).parents[1] / "gen" / "completion.json").read_text(encoding="utf-8"))
    return sorted({*_API["constants"], *_API["functions"], *_API["objects"]})


class FileTab(QWidget):
    """One file of the PC in the editor; the tab shows its name, with * while it has unsaved changes."""

    titleChanged = Signal()

    def __init__(self, path, parent=None, remote=None):
        super().__init__(parent)
        self.path = Path(path).resolve()
        self.remote = remote  # the path on the board, for a file opened from the board: path is its local copy
        self.editor = CodeEditor()
        self.editor.completion_provider = lvgl_completions if self.path.suffix == ".py" else (lambda _text: [])
        self.notice = QLabel()
        self.notice.setWordWrap(True)
        self.notice.setVisible(False)
        self.reload_button = QPushButton(tr("Reload"))
        self.reload_button.clicked.connect(self.reload)
        self.reload_button.setVisible(False)
        notice_row = QHBoxLayout()
        notice_row.addWidget(self.notice, 1)
        notice_row.addWidget(self.reload_button)
        self.error = QLabel()
        self.error.setWordWrap(True)
        self.error.setVisible(False)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(notice_row)
        layout.addWidget(self.editor, 1)
        layout.addWidget(self.error)
        self._newline = "\n"
        self._check = QTimer(self, singleShot=True, interval=800, timeout=self.check_syntax)
        self._watcher = QFileSystemWatcher(self)
        self._watcher.fileChanged.connect(self._changed_on_disk)
        self.load()
        self.editor.document().modificationChanged.connect(lambda _modified: self.titleChanged.emit())
        if self.path.suffix == ".py":
            self.editor.textChanged.connect(self._check.start)
            self._check.start()

    @property
    def modified(self):
        return self.editor.document().isModified()

    def title(self):
        name = self.path.name + (" [board]" if self.remote else "")
        return name + (" *" if self.modified else "")

    def load(self):
        text = readable_text(self.path)
        if text is None:
            raise ValueError(tr("{name} is not a text file the editor can open.", name=self.path.name))
        self._newline = "\r\n" if "\r\n" in text else "\n"
        self.editor.setPlainText(text.replace("\r\n", "\n"))
        self.editor.document().setModified(False)
        self._mtime = self.path.stat().st_mtime_ns
        if str(self.path) not in self._watcher.files():
            self._watcher.addPath(str(self.path))
        self._show_notice("")

    def reload(self):
        self.load()
        self.titleChanged.emit()

    def save(self):
        self._watcher.removePath(str(self.path))  # our own write is not an outside change
        try:
            with open(self.path, "w", encoding="utf-8", newline="") as stream:
                stream.write(self.editor.toPlainText().replace("\n", self._newline))
        finally:
            self._watcher.addPath(str(self.path))
        self._mtime = self.path.stat().st_mtime_ns
        self.editor.document().setModified(False)
        self._show_notice("")
        return True

    def _changed_on_disk(self, _path):
        if not self.path.exists():
            self._show_notice(tr("The file was deleted on disk: Save writes it again."))
            return
        if str(self.path) not in self._watcher.files():
            self._watcher.addPath(str(self.path))  # some editors replace the file, and the watch goes
        if self.path.stat().st_mtime_ns == self._mtime:
            return
        if self.modified:
            self._show_notice(tr("The file changed on disk. Reload loses your changes; Save replaces the other version."), reload=True)
        else:
            self.reload()

    def _show_notice(self, text, reload=False):
        self.notice.setText(text)
        self.notice.setVisible(bool(text))
        self.reload_button.setVisible(reload)

    def check_syntax(self):
        errors = syntax_errors(self.editor.toPlainText(), self.path.name)
        self.editor.show_errors([error["line"] for error in errors])
        self.error.setText("\n".join(f"{tr('Line')} {error['line']}: {error['message']}" for error in errors))
        self.error.setVisible(bool(errors))
        return errors


HIDDEN = {"__pycache__"}  # and names starting with a dot


class _Visible(QSortFilterProxyModel):
    """The folder without caches and hidden files."""

    def filterAcceptsRow(self, row, parent):
        name = self.sourceModel().fileName(self.sourceModel().index(row, 0, parent))
        return name not in HIDDEN and not name.startswith(".")


class FilesPanel(QWidget):
    """A folder of the PC: double click opens a file; the menu runs, creates, renames and deletes."""

    openRequested = Signal(str)
    runRequested = Signal(str)  # a .py file, in the simulator
    browserRequested = Signal(str)  # a .py file, in the browser
    uploadRequested = Signal(str, str)  # a file or folder of the PC, a folder of the board
    boardRunRequested = Signal(str)  # a .py file: its folder is uploaded to the board, then it runs there

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.model = QFileSystemModel(self)
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.proxy = _Visible(self)
        self.proxy.setSourceModel(self.model)
        # The model reads folders in a thread: until it has, the proxy has no row for the folder.
        self.model.directoryLoaded.connect(self._root_loaded)
        self.tree = QTreeView()
        self.tree.setModel(self.proxy)
        for column in (1, 2, 3):
            self.tree.hideColumn(column)
        self.tree.setHeaderHidden(True)
        self.tree.doubleClicked.connect(self._activated)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._menu)
        self.folder_label = QLabel()
        self.folder_label.setWordWrap(True)
        choose = QPushButton(tr("Open Folder…"))
        choose.clicked.connect(self.choose_folder)
        top = QHBoxLayout()
        top.addWidget(self.folder_label, 1)
        top.addWidget(choose)
        local = QWidget()
        local_layout = QVBoxLayout(local)
        local_layout.setContentsMargins(0, 0, 0, 0)
        local_layout.addLayout(top)
        local_layout.addWidget(self.tree, 1)
        self.board = BoardFilesView()
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(local)
        splitter.addWidget(self.board)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter, 1)
        self.folder = None
        saved = settings.value("files/folder", "")
        if saved and Path(saved).is_dir():
            self.set_folder(saved)
        else:
            self.folder_label.setText(tr("No folder: open one, or run a program."))
            self.tree.setVisible(False)  # without a root it would show the whole disk

    def set_folder(self, folder):
        self.folder = Path(folder).resolve()
        self.settings.setValue("files/folder", str(self.folder))
        self.folder_label.setText(self.folder.name or str(self.folder))  # the whole path is in the tooltip
        self.folder_label.setToolTip(str(self.folder))
        self.model.setRootPath(str(self.folder))
        self._root_loaded(str(self.folder))
        self.tree.setVisible(True)

    def _root_loaded(self, path):
        if self.folder is not None and Path(path) == self.folder:
            self.tree.setRootIndex(self.proxy.mapFromSource(self.model.index(str(self.folder))))

    def choose_folder(self):
        from PySide6.QtWidgets import QFileDialog

        folder = QFileDialog.getExistingDirectory(self, tr("Open Folder…"), str(self.folder or Path.home()))
        if folder:
            self.set_folder(folder)
        return bool(folder)

    def path_at(self, index):
        return Path(self.model.filePath(self.proxy.mapToSource(index))) if index.isValid() else None

    def _activated(self, index):
        path = self.path_at(index)
        if path and path.is_file():
            self.openRequested.emit(str(path))

    def _target_folder(self, path):
        if path is None:
            return self.folder
        return path if path.is_dir() else path.parent

    def _menu(self, position):
        if self.folder is None:
            return
        path = self.path_at(self.tree.indexAt(position))
        menu = QMenu(self)
        if path and path.is_file():
            menu.addAction(tr("Open"), lambda: self.openRequested.emit(str(path)))
            if path.suffix == ".py":
                menu.addAction(tr("Run Program"), lambda: self.runRequested.emit(str(path)))
                menu.addAction(tr("Run in the Browser"), lambda: self.browserRequested.emit(str(path)))
                menu.addAction(tr("Run on the Board"), lambda: self.boardRunRequested.emit(str(path)))
        if path is not None and self.board.connected:
            menu.addAction(tr("Upload to {folder} on the Board", folder=self.board.current_folder()), lambda: self.uploadRequested.emit(str(path), self.board.current_folder()))
        if path is not None:
            menu.addSeparator()
        folder = self._target_folder(path)
        menu.addAction(tr("New File…"), lambda: self.new_file(folder))
        menu.addAction(tr("New Folder…"), lambda: self.new_folder(folder))
        if path is not None:
            menu.addAction(tr("Rename…"), lambda: self.rename(path))
            menu.addAction(tr("Delete…"), lambda: self.delete(path))
        menu.addSeparator()
        menu.addAction(tr("Show in File Manager"), lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder))))
        menu.exec(self.tree.viewport().mapToGlobal(position))

    def _ask_name(self, title, text=""):
        name, accepted = QInputDialog.getText(self, title, tr("Name:"), text=text)
        name = name.strip()
        if not accepted or not name:
            return None
        if "/" in name or "\\" in name or name in (".", ".."):
            QMessageBox.warning(self, title, tr("A name without / or \\, please."))
            return None
        return name

    def new_file(self, folder):
        name = self._ask_name(tr("New File…"), "main.py")
        if name is None:
            return None
        path = folder / name
        if path.exists():
            QMessageBox.warning(self, tr("New File…"), tr("{name} already exists.", name=name))
            return None
        path.write_text("", encoding="utf-8")
        self.openRequested.emit(str(path))
        return path

    def new_folder(self, folder):
        name = self._ask_name(tr("New Folder…"))
        if name is None:
            return None
        path = folder / name
        try:
            path.mkdir()
        except OSError as exc:
            QMessageBox.warning(self, tr("New Folder…"), str(exc))
            return None
        return path

    def rename(self, path):
        name = self._ask_name(tr("Rename…"), path.name)
        if name is None or name == path.name:
            return None
        target = path.with_name(name)
        if target.exists():
            QMessageBox.warning(self, tr("Rename…"), tr("{name} already exists.", name=name))
            return None
        path.rename(target)
        return target

    def delete(self, path):
        answer = QMessageBox.question(self, tr("Delete…"), tr("Move {name} to the trash?", name=path.name))
        if answer != QMessageBox.Yes:
            return False
        from PySide6.QtCore import QFile

        if not QFile.moveToTrash(str(path)):
            QMessageBox.warning(self, tr("Delete…"), tr("{name} could not be moved to the trash.", name=path.name))
            return False
        return True

    def select(self, path):
        index = self.proxy.mapFromSource(self.model.index(str(path)))
        if index.isValid():
            self.tree.setCurrentIndex(index)


class BoardFilesView(QWidget):
    """The files of the connected board. Folders are read when opened: a board answers slowly.

    The window does the work with the board and answers with show_listing(); this view only asks."""

    listRequested = Signal(str)
    openRequested = Signal(str)
    downloadRequested = Signal(str)
    uploadRequested = Signal(str)  # a folder of the board: files of the PC go there
    mkdirRequested = Signal(str)
    renameRequested = Signal(str)
    deleteRequested = Signal(str, bool)
    runRequested = Signal(str)

    PATH, FOLDER, LOADED = Qt.UserRole, Qt.UserRole + 1, Qt.UserRole + 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self.connected = False
        # Set by the window from its dock: for docks grouped in tabs, isVisible() is true also behind the other tab.
        self.shown = False
        self.title = QLabel(tr("Board"))
        self.refresh_button = QPushButton(tr("Refresh"))
        self.refresh_button.clicked.connect(self.refresh)
        top = QHBoxLayout()
        top.addWidget(self.title, 1)
        top.addWidget(self.refresh_button)
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemExpanded.connect(self._expanded)
        self.tree.itemDoubleClicked.connect(self._activated)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._menu)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(top)
        layout.addWidget(self.tree, 1)
        self.set_connected(False)

    def set_connected(self, connected, port=""):
        changed = connected != self.connected
        self.connected = connected
        self.title.setText(tr("Board on {port}", port=port) if connected else tr("Board: not connected"))
        self.refresh_button.setEnabled(connected)
        self.tree.setEnabled(connected)
        if changed:
            self.tree.clear()

    def ensure_listed(self):
        """Read the board when the view is seen, not at every connection: reading occupies the board, and
        an upload or a start asked meanwhile would be refused."""
        if self.connected and self.shown and self.tree.topLevelItemCount() == 0:
            self.refresh()

    def refresh(self):
        """Read the top folder again; open folders are read again when opened."""
        if self.connected:
            self.tree.clear()
            self.listRequested.emit("/")

    def _item(self, path):
        if path == "/":
            return self.tree.invisibleRootItem()
        pending = [self.tree.invisibleRootItem()]
        while pending:
            item = pending.pop()
            for index in range(item.childCount()):
                child = item.child(index)
                if child.data(0, self.PATH) == path:
                    return child
                pending.append(child)
        return None

    def show_listing(self, path, entries):
        item = self._item(path)
        if item is None:
            return
        item.takeChildren()
        for entry in entries:
            child_path = (path.rstrip("/") + "/" + entry["name"])
            child = QTreeWidgetItem([entry["name"] + ("/" if entry["dir"] else "")])
            child.setData(0, self.PATH, child_path)
            child.setData(0, self.FOLDER, entry["dir"])
            if entry["dir"]:
                child.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            elif entry["size"] >= 0:
                child.setToolTip(0, f"{child_path} — {entry['size']} B")
            item.addChild(child)
        if item is not self.tree.invisibleRootItem():
            item.setData(0, self.LOADED, True)

    def _expanded(self, item):
        if item.data(0, self.FOLDER):
            self.listRequested.emit(item.data(0, self.PATH))

    def _activated(self, item):
        if not item.data(0, self.FOLDER):
            self.openRequested.emit(item.data(0, self.PATH))

    def current_folder(self):
        """The folder selected, or the folder of the file selected; "/" without a selection."""
        item = self.tree.currentItem()
        if item is None:
            return "/"
        path = item.data(0, self.PATH)
        return path if item.data(0, self.FOLDER) else (path.rsplit("/", 1)[0] or "/")

    def reload_folder(self, path):
        """After a change: read the folder again, or the top one."""
        self.listRequested.emit(path if path == "/" or self._item(path) is not None else "/")

    def _menu(self, position):
        if not self.connected:
            return
        item = self.tree.itemAt(position)
        path = item.data(0, self.PATH) if item else None
        folder = item.data(0, self.FOLDER) if item else True
        target = (path if folder else path.rsplit("/", 1)[0] or "/") if path else "/"
        menu = QMenu(self)
        if path and not folder:
            menu.addAction(tr("Open"), lambda: self.openRequested.emit(path))
            if path.endswith(".py"):
                menu.addAction(tr("Run on the Board"), lambda: self.runRequested.emit(path))
            menu.addAction(tr("Download to the Computer"), lambda: self.downloadRequested.emit(path))
            menu.addSeparator()
        menu.addAction(tr("Upload Files Here…"), lambda: self.uploadRequested.emit(target))
        menu.addAction(tr("New Folder…"), lambda: self.mkdirRequested.emit(target))
        if path:
            menu.addAction(tr("Rename…"), lambda: self.renameRequested.emit(path))
            menu.addAction(tr("Delete…"), lambda: self.deleteRequested.emit(path, bool(folder)))
        menu.addSeparator()
        menu.addAction(tr("Refresh"), self.refresh)
        menu.exec(self.tree.viewport().mapToGlobal(position))
