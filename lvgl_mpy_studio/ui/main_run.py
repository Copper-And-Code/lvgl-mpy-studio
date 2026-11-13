import json
import re
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QDockWidget, QFileDialog, QMessageBox, QTreeWidgetItem

from lvgl_mpy_studio.build.compiler import CompileError, compile_python, map_error, traceback_errors
from lvgl_mpy_studio.build.program import flash_dir, prepare_program, program_board, reset_flash
from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.platform import IS_WINDOWS


# A complete traceback: the frame lines, indented, then the exception line.
TRACEBACK_BLOCK = re.compile(r"Traceback \(most recent call last\):\n(?:[ \t].*\n)+(\S.*)\n")


class RunMixin:
    """Running in the simulator and showing errors. A part of MainWindow."""

    def _project_dir(self):
        """Where builds and exports go: next to the project, or the current folder before the first save."""
        return self.document.path.parent if self.document.path else Path.cwd()

    def _build_dir(self):
        return self._project_dir() / "build" / "py"

    def run_project(self):
        if self.run_target.is_board:
            return self.upload_board(True)
        if self.sim_panel.running or not self.save_project():
            return False
        output = self._build_dir()
        self.errors.clear()
        self._sim_trace = ""
        self.output.appendPlainText(tr("Generating in {output}", output=output))
        try:
            generated = generate_project(self.document.project, output)
            compile_python(output)
            self._show_warnings(generated["warnings"])
        except CompileError as exc:
            self._show_compile_errors(exc, output)
            return False
        except (OSError, ValueError) as exc:
            self.append_error(str(exc))
            return False
        self.output.appendPlainText(tr("{target} compilation completed", target="MicroPython"))
        self.tabs.setCurrentWidget(self.sim_panel)
        try:
            self.sim_panel.start(output)
        except (OSError, RuntimeError) as exc:
            self.append_error(str(exc))
            return False
        return True

    def stop_simulation(self):
        if self.run_target.is_board:
            return self.stop_board()
        self.sim_panel.stop()
        return True

    def restart_project(self):
        program = self.sim_panel.program
        self.sim_panel.shutdown()
        return self.run_program(self._program_entry) if program and self._program_entry else self.run_project()

    def _running_changed(self, running):
        locked = running and not self.sim_panel.program  # a program is not the open project, which stays editable
        self.properties.setEnabled(not locked)
        self.code_panel.set_running(locked)
        for _index, view in self.designers.values():
            view.setEnabled(not locked)
        self._update_device_actions()

    # ---- Programs without pages ----

    def _last_program(self):
        path = self.settings.value("simulator/program", "")
        return Path(path) if path else None

    def run_program(self, entry=None):
        """Run a .py file and its folder in the simulator as on a board: no pages, a terminal for the keys."""
        if IS_WINDOWS:
            self.append_error(tr("Programs without pages run only in the Linux simulator for now."))
            return False
        if self.sim_panel.running:
            self.statusBar().showMessage(tr("Stop the simulator first."), 5000)
            return False
        if entry is None:
            last = self.current_python_file() or self._last_program()
            path, _filter = QFileDialog.getOpenFileName(self, tr("Run Program"), str(last or ""), tr("MicroPython program (*.py)"))
            if not path:
                return False
            entry = path
        entry = Path(entry)
        if not self.save_files_in(entry.parent):
            return False
        self.files_panel.set_folder(entry.parent)
        board, width, height = program_board()
        try:
            prepared = prepare_program(entry, width, height, board)
        except (OSError, ValueError) as exc:
            self.append_error(str(exc))
            return False
        self.settings.setValue("simulator/program", str(entry))
        self._program_entry = entry
        self.output.appendPlainText(tr("Program {name}, {width}×{height}; its flash is {flash}", name=entry.name, width=width, height=height, flash=prepared["flash"]))
        self.tabs.setCurrentWidget(self.sim_panel)
        try:
            self.sim_panel.start(prepared["boot"], prepared["arguments"], prepared["environment"])
        except (OSError, RuntimeError) as exc:
            self.append_error(str(exc))
            return False
        self.sim_panel.terminal.setFocus()
        return True

    def _program_restart(self):
        """machine.reset() in the program: start it again with its flash as it is."""
        if self._program_entry:
            self.run_program(self._program_entry)

    def open_program_flash(self):
        last = self._last_program()
        if last is None:
            self.statusBar().showMessage(tr("Run a program first: Run → Run Program…"), 5000)
            return False
        folder = flash_dir(last.parent)
        folder.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))
        return True

    def erase_program_flash(self):
        last = self._last_program()
        if last is None:
            self.statusBar().showMessage(tr("Run a program first: Run → Run Program…"), 5000)
            return False
        if self.sim_panel.running and self.sim_panel.program:
            self.statusBar().showMessage(tr("Stop the simulator first."), 5000)
            return False
        answer = QMessageBox.question(self, tr("Erase Program Flash…"), tr("Erase the simulated flash of {folder}? The files the program wrote are lost; your folder is not touched.", folder=last.parent))
        if answer != QMessageBox.Yes:
            return False
        reset_flash(last.parent)
        self.statusBar().showMessage(tr("Program flash erased."), 5000)
        return True

    def _first_frame(self):
        if self.sim_panel.first_frame_ms is not None:
            self.statusBar().showMessage(tr("First frame: {milliseconds} ms", milliseconds=f"{self.sim_panel.first_frame_ms:.0f}"), 2000)

    def _sim_output(self, text, _error=False):
        """The simulator writes tracebacks to stdout, in pieces: they are read when a block is complete."""
        self.output.appendPlainText(text.rstrip())
        self._sim_trace += text.replace("\r\n", "\n")
        blocks = list(TRACEBACK_BLOCK.finditer(self._sim_trace))
        rest = self._sim_trace[blocks[-1].end():] if blocks else self._sim_trace
        start = rest.rfind("Traceback (most recent call last)")
        self._sim_trace = rest[start:][-20000:] if start >= 0 else rest[-40:]  # half a traceback waits for the next piece
        if not blocks:
            return
        try:
            sourcemap = json.loads((self._build_dir() / "sourcemap.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            sourcemap = None
        modules = {module.name for module in self.document.project.modules}
        added = False
        for block in blocks:
            exception = block.group(1).strip()
            for mapped in self._trace_rows(traceback_errors(block.group(0), sourcemap, modules)):
                mapped["message"] = exception if mapped["origin"] else tr("called from here") + " — " + exception
                self._add_error_row(mapped, block.group(0).strip())
                added = True
        if added:  # the Errors panel is behind Output: the lines to click must be visible
            self.findChild(QDockWidget, "errorsDock").raise_()

    @staticmethod
    def _trace_rows(errors):
        """First the line where the error happened, then the calls: an error in a module does not go to the handler that uses it."""
        return sorted(errors, key=lambda error: not error.get("origin"))

    def _show_compile_errors(self, error, output):
        modules = {module.name for module in self.document.project.modules}
        for item in error.errors:
            sourcemap = output / "sourcemap.json"
            mapped = map_error(item, sourcemap, modules) if sourcemap.exists() else item
            self._add_error_row(mapped)
            self.output.appendPlainText(mapped["message"])

    def _error_activated(self, item):
        error = item.data(0, Qt.UserRole)
        if not error:
            return
        line = error.get("sourceLine", error.get("line", 1))
        if error.get("module"):
            self.open_module(error["module"], line)
        elif error.get("handler"):
            self.tabs.setCurrentWidget(self.code_panel)
            self.code_panel.open_source(error["handler"], line)
        else:
            return
        self.code_panel.mark_line(line)

    def _add_error_row(self, mapped, tooltip=""):
        """A line of the Errors panel that a double click can open: file, line in the user's code, message."""
        name = Path(mapped["file"]).name if mapped.get("file") else tr("Compiler")
        row = QTreeWidgetItem((name, str(mapped.get("sourceLine", mapped["line"])), mapped["message"]))
        row.setData(0, Qt.UserRole, mapped)
        if tooltip:
            row.setToolTip(2, tooltip)
        self.errors.addTopLevelItem(row)

    def _show_warnings(self, warnings):
        for warning in warnings:
            self.output.appendPlainText(tr("Warning: {warning}", warning=warning))

    def append_error(self, text):
        self.output.appendPlainText(text)
        self.errors.addTopLevelItem(QTreeWidgetItem(("IDE", "", text)))
