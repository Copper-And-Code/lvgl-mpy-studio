from pathlib import Path
import re

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox, QTabBar, QToolButton

from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.platform import config_dir
from lvgl_mpy_studio.ui.device_files import folder_items
from lvgl_mpy_studio.ui.files import FileTab, FilesPanel


class EditorTabsMixin:
    """Files of the PC in tabs of their own, next to the pages, the Code and the Simulator. A part of MainWindow."""

    def _make_files_panel(self):
        self.files_panel = FilesPanel(self.settings)
        self.files_panel.openRequested.connect(self.open_file)
        self.files_panel.runRequested.connect(lambda path: self.run_program(path))
        self.files_panel.browserRequested.connect(lambda path: self.program_in_browser(path))
        self.files_panel.uploadRequested.connect(self._upload_local_to_board)
        self.files_panel.boardRunRequested.connect(self.run_program_on_board)
        board = self.files_panel.board
        board.listRequested.connect(self._board_list)
        board.openRequested.connect(self.open_board_file)
        board.downloadRequested.connect(self.download_board_file)
        board.uploadRequested.connect(self.upload_to_board_folder)
        board.mkdirRequested.connect(self.board_new_folder)
        board.renameRequested.connect(self.board_rename)
        board.deleteRequested.connect(self.board_delete)
        board.runRequested.connect(lambda path: self.run_file_on_board(path))
        self._board_pending = []
        return self.files_panel

    def _files_shown(self, visible):
        self.files_panel.board.shown = visible
        self.files_panel.board.ensure_listed()

    @property
    def file_tabs(self):
        return [self.tabs.widget(index) for index in range(self.tabs.count()) if isinstance(self.tabs.widget(index), FileTab)]

    def _file_tab(self, path):
        path = Path(path).resolve()
        return next((tab for tab in self.file_tabs if tab.path == path), None)

    def open_file(self, path, remote=None):
        """Open a file of the PC in a tab, or bring forward the tab that has it; remote: its path on the board."""
        tab = self._file_tab(path)
        if tab is None:
            try:
                tab = FileTab(path, remote=remote)
            except (OSError, ValueError) as exc:
                QMessageBox.warning(self, tr("Open"), str(exc))
                return None
            index = self.tabs.addTab(tab, tab.title())
            self.tabs.setTabToolTip(index, str(tab.path))
            close = QToolButton()
            close.setAutoRaise(True)
            close.setText("×")
            close.setToolTip(tr("Close"))
            close.clicked.connect(lambda: self.close_file(tab))
            self.tabs.tabBar().setTabButton(index, QTabBar.RightSide, close)
            tab.titleChanged.connect(lambda: self.tabs.setTabText(self.tabs.indexOf(tab), tab.title()))
        self.tabs.setCurrentWidget(tab)
        tab.editor.setFocus(Qt.OtherFocusReason)
        return tab

    def close_file(self, tab):
        if tab.modified:
            answer = QMessageBox.question(self, tr("Unsaved Changes"), tr("Save changes to {name}?", name=tab.path.name), QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return False
            if answer == QMessageBox.Save and not self._save_file(tab):
                return False
        self.tabs.removeTab(self.tabs.indexOf(tab))
        tab.deleteLater()
        return True

    def _save_file(self, tab):
        if tab.remote and not self.device.port:
            QMessageBox.warning(self, tr("Save"), tr("{name} is a file of the board: connect to the board to save it.", name=tab.path.name))
            return False
        try:
            tab.save()
        except OSError as exc:
            QMessageBox.warning(self, tr("Save"), str(exc))
            return False
        if tab.remote:
            # The local copy is written; the tab stays modified until the board has the file.
            tab.editor.document().setModified(True)
            data = tab.path.read_bytes()
            def saved(_result):
                tab.editor.document().setModified(False)
                self.statusBar().showMessage(tr("Saved {path} on the board", path=tab.remote), 3000)
            self._board_task(lambda: self.device.write_file(tab.remote, data), saved)
        return True

    def save_current(self):
        """Ctrl+S: the file of the current tab, or the project."""
        tab = self.tabs.currentWidget()
        if isinstance(tab, FileTab):
            saved = self._save_file(tab)
            if saved and not tab.remote:
                self.statusBar().showMessage(tr("Saved {path}", path=tab.path), 3000)
            return saved
        return self.save_project()

    def save_files_in(self, folder):
        """Before a program runs: its files modified in the editor go to disk, as F5 saves the project."""
        folder = Path(folder).resolve()
        for tab in self.file_tabs:
            if tab.modified and folder in tab.path.parents and not self._save_file(tab):
                return False
        return True

    def confirm_files(self):
        """When the window closes: each modified file is saved, discarded, or the closing stops."""
        for tab in self.file_tabs:
            if not tab.modified:
                continue
            self.tabs.setCurrentWidget(tab)
            answer = QMessageBox.question(self, tr("Unsaved Changes"), tr("Save changes to {name}?", name=tab.path.name), QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if answer == QMessageBox.Cancel or (answer == QMessageBox.Save and not self._save_file(tab)):
                return False
        return True

    def current_python_file(self):
        """The .py file of the current tab, if any: Run Program and Run in the Browser offer it first."""
        tab = self.tabs.currentWidget()
        return tab.path if isinstance(tab, FileTab) and tab.path.suffix == ".py" else None

    # ---- Files of the board ----

    def _board_task(self, operation, completed=None):
        """One operation on the board, now or as soon as the board is free: the IDE does one at a time."""
        if not self.device.port:
            self.statusBar().showMessage(tr("Board not connected"), 3000)
            return
        if self._worker is not None or not self._device_task(operation, completed, background=True):
            self._board_pending.append((operation, completed))

    def _run_board_pending(self):
        if self._board_pending and self._worker is None and self.device.port:
            operation, completed = self._board_pending.pop(0)
            self._device_task(operation, completed, background=True)
        elif not self.device.port:
            self._board_pending.clear()

    def _board_list(self, path):
        self._board_task(lambda: self.device.list_dir(path), lambda entries: self.files_panel.board.show_listing(path, entries))

    def _board_cache(self, remote):
        """Where a file of the board is copied to be edited: one folder per port, in the settings."""
        port = re.sub(r"[^A-Za-z0-9_.-]", "_", self.device.port or "board")
        return config_dir() / "board-files" / port / remote.lstrip("/")

    def open_board_file(self, remote):
        tab = next((tab for tab in self.file_tabs if tab.remote == remote), None)
        if tab is not None:
            self.tabs.setCurrentWidget(tab)
            return
        local = self._board_cache(remote)
        local.parent.mkdir(parents=True, exist_ok=True)
        self._board_task(lambda: self.device.read_file(remote, local), lambda _path: self.open_file(local, remote=remote))

    def download_board_file(self, remote):
        folder = self.files_panel.folder
        if folder is None:
            if not self.files_panel.choose_folder():
                return
            folder = self.files_panel.folder
        target = folder / remote.rsplit("/", 1)[-1]
        if target.exists():
            answer = QMessageBox.question(self, tr("Download to the Computer"), tr("{path} exists. Replace it?", path=target))
            if answer != QMessageBox.Yes:
                return
        self._board_task(lambda: self.device.read_file(remote, target), lambda _path: self.statusBar().showMessage(tr("Downloaded to {path}", path=target), 3000))

    def upload_to_board_folder(self, remote_folder):
        start = str(self.files_panel.folder or Path.home())
        paths, _filter = QFileDialog.getOpenFileNames(self, tr("Upload Files Here…"), start)
        if paths:
            self._confirm_and_upload_files([(path, Path(path).name) for path in paths], remote_folder)

    def _upload_local_to_board(self, local, remote_folder):
        local = Path(local)
        items = list(folder_items(local)) if local.is_dir() else [(local, local.name)]
        self._confirm_and_upload_files(items, remote_folder)

    def _ask_board_name(self, title, text=""):
        name, accepted = QInputDialog.getText(self, title, tr("Name:"), text=text)
        name = name.strip()
        if not accepted or not name:
            return None
        if "/" in name or name in (".", ".."):
            QMessageBox.warning(self, title, tr("A name without / or \\, please."))
            return None
        return name

    @staticmethod
    def _parent(remote):
        return remote.rsplit("/", 1)[0] or "/"

    def board_new_folder(self, remote_folder):
        name = self._ask_board_name(tr("New Folder…"))
        if name:
            path = remote_folder.rstrip("/") + "/" + name
            self._board_task(lambda: self.device.make_dir(path), lambda _result: self.files_panel.board.reload_folder(remote_folder))

    def board_rename(self, remote):
        name = self._ask_board_name(tr("Rename…"), remote.rsplit("/", 1)[-1])
        if name and name != remote.rsplit("/", 1)[-1]:
            target = self._parent(remote).rstrip("/") + "/" + name
            self._board_task(lambda: self.device.rename_path(remote, target), lambda _result: self.files_panel.board.reload_folder(self._parent(remote)))

    def board_delete(self, remote, folder):
        question = tr("Delete the folder {path} from the board, with everything in it?", path=remote) if folder else tr("Delete {path} from the board?", path=remote)
        if QMessageBox.question(self, tr("Delete…"), question) != QMessageBox.Yes:
            return
        self._board_task(lambda: self.device.remove_path(remote), lambda _result: self.files_panel.board.reload_folder(self._parent(remote)))

    def _board_program_root(self):
        """Where a program goes on the board when no folder is chosen: the flash of the STM32 boards, else the root."""
        board = self.document.project.board or {}
        return "/flash" if str(board.get("config", {}).get("appRoot", "")).startswith("/flash") else "/"

    def run_program_on_board(self, entry):
        """As Run Program, on the board: its folder is uploaded, then the file runs from the board's prompt."""
        entry = Path(entry).resolve()
        if not self.save_files_in(entry.parent):
            return False
        view = self.files_panel.board
        destination = view.current_folder() if view.connected and view.tree.currentItem() else self._board_program_root()
        remote = f"{destination.rstrip('/')}/{entry.parent.name}/{entry.name}"
        items = list(folder_items(entry.parent))
        self.statusBar().showMessage(tr("Uploading {folder} to {destination} on the board, then running {name}…", folder=entry.parent.name, destination=destination, name=entry.name))
        return self._confirm_and_upload_files(items, destination, then=lambda: self.run_file_on_board(remote))

    def ask_run_on_board(self):
        last = self.current_python_file() or self._last_program()
        path, _filter = QFileDialog.getOpenFileName(self, tr("Run on the Board"), str(last or ""), tr("MicroPython program (*.py)"))
        if not path:
            return False
        self.settings.setValue("simulator/program", path)
        self.files_panel.set_folder(Path(path).parent)
        return self.run_program_on_board(path)
