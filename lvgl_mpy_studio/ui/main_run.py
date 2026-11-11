import json
import re
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDockWidget, QTreeWidgetItem

from lvgl_mpy_studio.build.compiler import CompileError, compile_python, map_error, traceback_errors
from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.gen.project_gen import generate_project


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
        self.sim_panel.shutdown()
        return self.run_project()

    def _running_changed(self, running):
        self.properties.setEnabled(not running)
        self.code_panel.set_running(running)
        for _index, view in self.designers.values():
            view.setEnabled(not running)
        self._update_device_actions()

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
