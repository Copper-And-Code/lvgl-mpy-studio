import copy
import json
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox

from lvgl_mpy_studio.core.boards import compatible, portable_profile
from lvgl_mpy_studio.core.i18n import device_error_text, tr
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.device.service import DeviceError
from lvgl_mpy_studio.gen.board_gen import BoardSyntaxError, changed_exports, export_board
from lvgl_mpy_studio.ui.background import run_in_background
from lvgl_mpy_studio.ui.document import ExternalChangeError


DEFAULTS_KEY = "defaults/newProject"


class FilesMixin:
    """Project files: new, open, save, changes made by other programs, defaults, export and build. A part of MainWindow."""

    def new_project(self):
        if not self._confirm_discard():
            return
        self.document.new(self._default_project())
        self.tabs.setCurrentIndex(0)
        self.output.clear()
        self.errors.clear()

    def open_project_dialog(self):
        path, _filter = QFileDialog.getOpenFileName(self, tr("Open Project"), str(Path.home()), tr("LVGL Projects (*.json)"))
        if path:
            self.open_project(path)

    def open_project(self, path):
        if not self._confirm_discard():
            return False
        try:
            self.document.open(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            QMessageBox.critical(self, tr("Open Error"), str(exc))
            return False
        self._add_recent(path)
        self.tabs.setCurrentIndex(0)
        self.output.clear()
        self.errors.clear()
        return True

    def save_project(self, overwrite_external=False):
        if not self.document.path:
            return self.save_project_as()
        try:
            self.document.save(overwrite_external=overwrite_external)
        except ExternalChangeError as exc:
            return self._resolve_external_change(exc.deleted)
        except OSError as exc:
            QMessageBox.critical(self, tr("Save Error"), str(exc))
            return False
        self.statusBar().showMessage(tr("Saved: {path}", path=self.document.path), 3000)
        return True

    def _resolve_external_change(self, deleted=False):
        """The file was changed or removed from outside, for example by MCP: nothing is written without a choice."""
        choice = self._ask_external_change(deleted)
        if choice == "reload" and not deleted:
            return self.reload_project()
        if choice == "copy":
            return self.save_project_as(self._copy_name())
        if choice == "overwrite":
            return self.save_project(overwrite_external=True)
        return False

    def _copy_name(self):
        """A free name next to the file: the copy must not land on another project."""
        path = self.document.path
        candidate = path.with_name(f"{path.stem}-{tr('copy')}{path.suffix}")
        number = 2
        while candidate.exists():
            candidate = path.with_name(f"{path.stem}-{tr('copy')}-{number}{path.suffix}")
            number += 1
        return candidate

    def _ask_external_change(self, deleted=False):
        """reload, copy, overwrite or None to cancel. A removed file cannot be reloaded."""
        if deleted:
            box = QMessageBox(QMessageBox.Warning, tr("File deleted by another program"), tr("{name} was deleted or moved outside the IDE after it was opened.", name=self.document.path.name), parent=self)
            box.setInformativeText(tr("Recreate the file: saves it again where it was. Save a copy: saves the project in another file."))
            buttons = {
                box.addButton(tr("Recreate the file"), QMessageBox.AcceptRole): "overwrite",
                box.addButton(tr("Save a copy…"), QMessageBox.ActionRole): "copy",
            }
            box.addButton(QMessageBox.Cancel)
            box.setDefaultButton(box.button(QMessageBox.Cancel))
            box.exec()
            return buttons.get(box.clickedButton())
        box = QMessageBox(QMessageBox.Warning, tr("File changed by another program"), tr("{name} was changed outside the IDE after it was opened, for example by an MCP agent or from the command line. Saving now would lose those changes.", name=self.document.path.name), parent=self)
        if self.document.modified:
            box.setInformativeText(tr("Reload: opens the version on disk; the unsaved changes made here and the undo history are lost. Save a copy: keeps your changes in another file and leaves this one untouched. Overwrite: replaces the version on disk with yours."))
        else:
            box.setInformativeText(tr("Reload: opens the version on disk. Save a copy: keeps the IDE's version in another file. Overwrite: replaces the version on disk with the IDE's."))
        buttons = {
            box.addButton(tr("Reload"), QMessageBox.DestructiveRole if self.document.modified else QMessageBox.AcceptRole): "reload",
            box.addButton(tr("Save a copy…"), QMessageBox.ActionRole): "copy",
            box.addButton(tr("Overwrite"), QMessageBox.DestructiveRole): "overwrite",
        }
        box.addButton(QMessageBox.Cancel)
        box.setDefaultButton(box.button(QMessageBox.Cancel))
        box.exec()
        return buttons.get(box.clickedButton())

    def reload_project(self):
        try:
            self.document.reload()
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            # A broken outside file must not cost the changes made here.
            QMessageBox.critical(self, tr("Open Error"), tr("The version on disk cannot be opened; your changes stay in the IDE: {error}", error=exc))
            return False
        self.output.clear()
        self.errors.clear()
        self.statusBar().showMessage(tr("Reloaded: {path}", path=self.document.path), 3000)
        return True

    def save_project_as(self, suggested=None):
        # The IDE asks to confirm an existing file, the same on every system: a native dialog may not.
        path, _filter = QFileDialog.getSaveFileName(self, tr("Save Project"), str(suggested or self.document.path or Path.home() / "project.json"), tr("LVGL Projects (*.json)"), "", QFileDialog.DontConfirmOverwrite)
        if not path:
            return False
        target = Path(path)
        own_file = self.document.path is not None and target.resolve() == self.document.path.resolve()
        if target.exists() and not own_file:
            answer = QMessageBox.question(self, tr("Save Project"), tr("{name} already exists. Replace it with this project?", name=target.name), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if answer != QMessageBox.Yes:
                return False
        try:
            self.document.save(path)
        except ExternalChangeError as exc:
            return self._resolve_external_change(exc.deleted)  # the same file was chosen, changed from outside
        except OSError as exc:
            QMessageBox.critical(self, tr("Save Error"), str(exc))
            return False
        self._add_recent(path)
        return True

    def _confirm_discard(self):
        if not self.document.modified:
            return True
        answer = QMessageBox.question(self, tr("Unsaved Changes"), tr("Save changes?"), QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if answer == QMessageBox.Cancel:
            return False
        return self.save_project() if answer == QMessageBox.Save else True

    def _add_recent(self, path):
        recent = self.settings.value("recentFiles", [], list)
        path = str(Path(path).resolve())
        self.settings.setValue("recentFiles", [path] + [item for item in recent if item != path][:9])

    def _populate_recent(self):
        self.recent_menu.clear()
        for path in self.settings.value("recentFiles", [], list):
            self.recent_menu.addAction(path, lambda checked=False, value=path: self.open_project(value))

    def _update_title(self):
        marker = "*" if self.document.modified else ""
        name = self.document.path.name if self.document.path else self.document.project.projectName
        self.setWindowTitle(f"{marker}{name} — LVGL MPY Studio")

    def build_executable(self, single_file=False):
        if self._building or not self.save_project():
            return False
        from lvgl_mpy_studio.build.release import build_release
        base = self._project_dir()
        project = copy.deepcopy(self.document.project)
        self._building = True
        self.build_action.setEnabled(False)
        self.single_file_action.setEnabled(False)
        self.statusBar().showMessage(tr("Building the executable…"))
        def finished(succeeded, result):
            self._building = False
            self.build_action.setEnabled(True)
            self.single_file_action.setEnabled(True)
            if succeeded:
                self.output.appendPlainText(tr("Standalone executable created: {runner}", runner=result))
                self.statusBar().showMessage(tr("Build completed: {path}", path=result.parent), 5000)
            else:
                self.append_error(str(result))
                self.statusBar().showMessage(tr("Build failed"), 5000)
        if single_file:
            run_in_background(self, lambda: build_release(project, "micropython", base / "dist", "release", single_file=True), finished)
        else:
            run_in_background(self, lambda: build_release(project, "micropython", base / "dist"), finished)
        return True

    def build_single_file(self):
        return self.build_executable(single_file=True)

    def open_in_browser(self):
        """Create the web version in dist/<project>-web/ and open it: the folder can then be published as it is."""
        if self._building or not self.save_project():
            return False
        from lvgl_mpy_studio.build.web import build_web, serve
        base = self._project_dir()
        project = copy.deepcopy(self.document.project)
        self._building = True
        self.web_action.setEnabled(False)
        self.statusBar().showMessage(tr("Building the web version…"))
        def finished(succeeded, result):
            self._building = False
            self.web_action.setEnabled(True)
            if not succeeded:
                self.append_error(str(result))
                self.statusBar().showMessage(tr("Web version failed"), 5000)
                return
            if self._web_server is not None:
                self._web_server.shutdown()
            self._web_server, url = serve(result)
            self.output.appendPlainText(tr("Web version in {path}: to publish it, copy the folder to a static host.", path=result))
            self.statusBar().showMessage(tr("Open at {url}", url=url), 5000)
            QDesktopServices.openUrl(QUrl(url))
        run_in_background(self, lambda: build_web(project, base / "dist"), finished)
        return True

    def _default_project(self):
        project = Project()
        try:
            defaults = json.loads(self.settings.value(DEFAULTS_KEY, "") or "{}")
            profile = self.profile_store.get(defaults.get("board"))
            if profile:
                project.board = portable_profile(profile)
                project.set_display_size(profile["logicalWidth"], profile["logicalHeight"])
            elif defaults.get("width"):
                project.set_display_size(defaults["width"], defaults["height"])
            project.runTarget = defaults.get("runTarget")
        except (AttributeError, KeyError, TypeError, ValueError):
            return Project()
        return project

    def save_new_project_defaults(self):
        project = self.document.project
        self.settings.setValue(DEFAULTS_KEY, json.dumps({"board": project.board["id"] if project.board else None, "runTarget": project.runTarget, "width": project.display.width, "height": project.display.height}))
        self.statusBar().showMessage(tr("Default for new projects: {target}", target=self.run_selector.label()), 5000)

    def clear_new_project_defaults(self):
        self.settings.remove(DEFAULTS_KEY)
        self.statusBar().showMessage(tr("Default removed"), 5000)

    def _export_directory(self, name, title):
        if self.document.path:
            return self.document.path.parent / name
        chosen = QFileDialog.getExistingDirectory(self, title, str(Path.home()))
        return Path(chosen) if chosen else None

    def _show_export(self, title, message, detail, directory):
        self.output.appendPlainText(message)
        self.statusBar().showMessage(message, 5000)
        box = QMessageBox(QMessageBox.Information, title, message, QMessageBox.Close, self)
        box.setInformativeText(detail)
        open_folder = box.addButton(tr("Open Folder"), QMessageBox.ActionRole)
        box.exec()
        if box.clickedButton() is open_folder:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(directory)))

    def _export_profile(self):
        """The board of the project, or a choice among those with the same resolution."""
        profile = self._board_profile()
        if profile:
            return profile
        project = self.document.project
        boards = [item for item in self.profile_store.profiles() if compatible(project, item)]
        if not boards:
            self.append_error(tr("No board at {width}×{height}: change the project resolution.", width=project.display.width, height=project.display.height))
            return None
        names = [f"{item['name']} — {item['id']}" for item in boards]  # two profiles can have the same name
        name, accepted = QInputDialog.getItem(self, tr("Export MicroPython Code"), tr("The code depends on the board. Which board?"), names, 0, False)
        if not accepted:
            return None
        profile = portable_profile(boards[names.index(name)])
        return profile

    def export_python(self):
        profile = self._export_profile()
        if profile is None:
            return False
        directory = self._export_directory("export_py", tr("Choose the folder for the MicroPython code"))
        if directory is None:
            return False
        changed = changed_exports(directory)
        if changed:
            answer = QMessageBox.warning(self, tr("Export MicroPython Code"), tr("These files changed after the last export and will be overwritten:\n{files}", files="\n".join(changed)), QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
            if answer != QMessageBox.Yes:
                return False
        try:
            generated = export_board(self.document.project, profile, directory)
        except BoardSyntaxError as exc:
            self._device_failed(DeviceError(exc.code, json.dumps(exc.errors, ensure_ascii=False), exc.errors))
            return False
        except ValueError as exc:
            code, _separator, detail = str(exc).partition(":")
            self.append_error(device_error_text(code, detail))
            return False
        except OSError as exc:
            self.append_error(str(exc))
            return False
        self._show_warnings(generated["warnings"])
        message = tr("MicroPython code for {board} exported to {path}", board=profile["name"], path=directory)
        self._show_export(tr("Export MicroPython Code"), message, tr("Copy the files to a folder on the board and run app_main.py. The board needs the LVGL firmware with display_driver."), directory)
        return True

    def export_c(self):
        directory = self._export_directory("export_c", tr("Choose the folder for the C code"))
        if directory is None:
            return False
        from lvgl_mpy_studio.gen.gen_c import generate_c
        try:
            generated = generate_c(self.document.project, directory, portable=True)
        except (OSError, ValueError) as exc:
            self.append_error(str(exc))
            return False
        self._show_warnings(generated["warnings"])
        self._show_export(tr("Export C Code"), tr("C code exported to {path}", path=directory), tr("Write the handlers in ui_events.c: the Python code is there as a comment, and your code is kept on future exports."), directory)
        return True
