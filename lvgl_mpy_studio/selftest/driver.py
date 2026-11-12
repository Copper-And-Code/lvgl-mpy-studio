"""Uses the IDE as a person does: mouse on the toolbox, the page and the panels, keys in the editors.

Menu entries are triggered through their action, which is what choosing the entry does. Dialogs
are answered by a watcher, because a modal dialog stops the code that opened it."""

import time
from contextlib import contextmanager

from PySide6.QtCore import QEventLoop, QPoint, QPointF, Qt, QTimer
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QAbstractSpinBox, QApplication, QComboBox, QDialogButtonBox, QFileDialog, QLineEdit, QMessageBox

from lvgl_mpy_studio.core.events import handler_name
from lvgl_mpy_studio.ui.designer.scene import Toolbox
from lvgl_mpy_studio.ui.main_window import MainWindow
from lvgl_mpy_studio.ui.properties.panel import DESCRIPTOR_ROLE

from .report import FAILED, PASSED, SKIPPED


class StepFailed(Exception):
    """A check that did not hold: the message says what was expected and what was found."""


class ScenarioStopped(Exception):
    """A step failed: the steps after it would only fail because of it."""


def sleep(milliseconds):
    """Let the IDE work for a while. Not QTest.qWait: it keeps Python's lock, and the threads of the IDE (the page preview) would stand still."""
    loop = QEventLoop()
    QTimer.singleShot(max(0, milliseconds), loop.quit)
    loop.exec()


def describe(dialog):
    text = dialog.text() if isinstance(dialog, QMessageBox) else ""
    return f"{type(dialog).__name__} “{dialog.windowTitle()}”" + (f": {text}" if text else "")


class Ide:
    def __init__(self, report, scenario, directory, slow_ms=0):
        self.report = report
        self.scenario = scenario
        self.directory = directory
        self.slow_ms = slow_ms
        self._number = 0
        self._dialog_handlers = []
        self._unexpected = []
        self._answered, self._patience = None, 0
        self.window = MainWindow()
        self.window.resize(1280, 800)
        self.window.show()
        QTest.qWaitForWindowExposed(self.window)
        self._watcher = QTimer()
        self._watcher.timeout.connect(self._watch_dialogs)
        self._watcher.start(max(100, slow_ms))
        self.pause()

    # --- steps and checks

    @contextmanager
    def step(self, title):
        self._number += 1
        started = time.monotonic()
        try:
            yield
            sleep(0)
            if self._unexpected:
                raise StepFailed("a dialog nobody expected appeared: " + "; ".join(self._unexpected))
            if self._dialog_handlers:
                raise StepFailed("a dialog was expected and did not appear")
        except Exception as exc:  # a defect of the IDE must be reported as a failed step, not stop the run
            detail = str(exc) if isinstance(exc, StepFailed) else f"{type(exc).__name__}: {exc}"
            pictures = self.pictures(f"{self._slug()}-{self._number:02}")
            self._unexpected.clear()
            self._dialog_handlers.clear()
            self.report.add(self.scenario, title, FAILED, time.monotonic() - started, detail, pictures)
            raise ScenarioStopped from exc
        self.report.add(self.scenario, title, PASSED, time.monotonic() - started)

    def skipped(self):
        self.report.add(self.scenario, "the rest of this scenario", SKIPPED, detail="not run: it depends on the step that failed")

    def check(self, condition, message):
        if not condition:
            raise StepFailed(message)

    def equal(self, found, expected, what):
        self.check(found == expected, f"{what}: expected {expected!r}, found {found!r}")

    def wait(self, condition, what, timeout_ms=5000):
        deadline = time.monotonic() + timeout_ms / 1000
        while not condition():
            if time.monotonic() > deadline:
                raise StepFailed(f"waited {timeout_ms / 1000:.0f} s for: {what}")
            sleep(20)

    def pause(self, factor=1):
        sleep(int(self.slow_ms * factor) if self.slow_ms else 0)

    def _slug(self):
        return "".join(character if character.isalnum() else "-" for character in self.scenario.lower()).strip("-")[:40]

    def pictures(self, name):
        """What the IDE and the simulator show now, saved next to the report."""
        saved = []
        if self.window.grab().save(str(self.report.directory / f"{name}-ide.png")):
            saved.append(f"{name}-ide.png")
        panel = self.window.sim_panel
        if panel.running and panel.framebuffer.save(str(self.report.directory / f"{name}-simulator.png")):
            saved.append(f"{name}-simulator.png")
        return saved

    # --- dialogs

    def _watch_dialogs(self):
        dialog = QApplication.activeModalWidget()
        if dialog is None or dialog is self.window:
            self._answered = None
            return
        if dialog is self._answered:  # answered at the last look: it is closing
            self._patience -= 1
            if self._patience > 0:
                return
        elif self._dialog_handlers:
            self._answered, self._patience = dialog, 10
            self._dialog_handlers.pop(0)(dialog)
            return
        self._unexpected.append(describe(dialog))
        dialog.grab().save(str(self.report.directory / f"{self._slug()}-{self._number:02}-dialog.png"))
        dialog.reject() if hasattr(dialog, "reject") else dialog.close()

    def answer_next_dialog(self, handler):
        """The next modal dialog is given to handler(dialog), which must close it."""
        self._dialog_handlers.append(handler)

    def answer_message(self, button):
        def handler(dialog):
            if not isinstance(dialog, QMessageBox) or dialog.button(button) is None:
                self._unexpected.append(describe(dialog))
                dialog.reject()
                return
            QTest.mouseClick(dialog.button(button), Qt.LeftButton)

        self.answer_next_dialog(handler)

    def answer_file_dialog(self, path):
        def handler(dialog):
            if not isinstance(dialog, QFileDialog):
                self._unexpected.append(describe(dialog))
                dialog.reject()
                return
            # The name is set in one go: typed key by key, the dialog follows each folder of the path.
            dialog.findChild(QLineEdit, "fileNameEdit").setText(str(path))
            buttons = dialog.findChild(QDialogButtonBox)
            QTest.mouseClick(buttons.button(QDialogButtonBox.Save) or buttons.button(QDialogButtonBox.Open), Qt.LeftButton)

        self.answer_next_dialog(handler)

    # --- the IDE

    @property
    def project(self):
        return self.window.document.project

    def choose(self, action):
        """Choose a menu entry or a toolbar button."""
        self.check(action.isEnabled(), f"the action “{action.text()}” is disabled")
        action.trigger()
        self.pause()

    def designer(self):
        view = self.window.current_designer()
        self.check(view is not None, "no page is open in the designer")
        return view

    def add_widget(self, widget_type, x, y):
        """Double-click the widget in the toolbox, then click the page where it goes; return its name."""
        toolbox = self.window.findChild(Toolbox)
        item = next((entry for entry in toolbox.widget_items() if entry.data(Qt.UserRole) == widget_type), None)
        self.check(item is not None, f"the toolbox has no widget “{widget_type}”")
        toolbox.scrollToItem(item)
        centre = toolbox.visualItemRect(item).center()
        QTest.mouseClick(toolbox.viewport(), Qt.LeftButton, pos=centre)
        QTest.mouseDClick(toolbox.viewport(), Qt.LeftButton, pos=centre)
        view = self.designer()
        self.equal(view.pending_type, widget_type, "widget armed by the double click")
        self.pause()
        before = {widget.name for widget in view.designer_scene.page.widgets}
        QTest.mouseClick(view.viewport(), Qt.LeftButton, pos=view.mapFromScene(QPointF(x, y)))
        added = [widget.name for widget in view.designer_scene.page.widgets if widget.name not in before]
        self.equal(len(added), 1, f"widgets added by the click for “{widget_type}”")
        self.pause()
        return added[0]

    def drawn(self, name):
        """The item that draws the widget on the open page, or None."""
        widget = self.project.find_widget(name)
        return self.designer().designer_scene.widget_items.get(widget.id) if widget else None

    def select(self, name):
        """Click the widget on the page."""
        view = self.designer()
        item = self.drawn(name)
        self.check(item is not None, f"the page has no widget “{name}”")
        view.designer_scene.clearSelection()
        QTest.mouseClick(view.viewport(), Qt.LeftButton, pos=view.mapFromScene(item.sceneBoundingRect().center()))
        self.equal(view.designer_scene.selected_names(), [name], "selection after the click")
        self.pause()

    def _property_item(self, name):
        def visit(parent):
            for row in range(parent.rowCount()):
                label, value = parent.child(row, 0), parent.child(row, 1)
                if value is not None and (value.data(DESCRIPTOR_ROLE) or {}).get("name") == name:
                    return value
                found = visit(label) if label is not None else None
                if found is not None:
                    return found
            return None

        return visit(self.window.properties.model.invisibleRootItem())

    def set_property(self, name, value):
        """Click the value in the Properties panel, type the new one and press Enter."""
        panel = self.window.properties
        sleep(30)  # the panel is rebuilt after a selection or a change
        self.check(self._property_item(name) is not None, f"the Properties panel has no “{name}” for {panel.names}")
        widget_name = panel.names[0]

        def open_editor():
            item = self._property_item(name)  # looked up again: a rebuild replaces the items
            panel.view.expandAll()
            panel.view.scrollTo(item.index())
            QTest.mouseClick(panel.view.viewport(), Qt.LeftButton, pos=panel.view.visualRect(item.index()).center())
            # Looked for among the children: after another window was in front, Qt reports no focus widget.
            editors = [child for kind in (QAbstractSpinBox, QComboBox, QLineEdit) for child in panel.view.viewport().findChildren(kind) if child.isVisible()]
            found = editors[0] if editors else None
            return found.lineEdit() if isinstance(found, QComboBox) else found

        editor = open_editor() or open_editor()  # the first click may only give the panel the focus
        self.check(editor is not None, f"clicking “{name}” opened no editor")
        editor.selectAll()
        QTest.keyClicks(editor, str(value))
        self.pause()
        QTest.keyClick(editor, Qt.Key_Return)
        self.wait(lambda: self.project.find_widget(widget_name).props.get(name) == value, f"{widget_name}.{name} to become {value!r} (it is {self.project.find_widget(widget_name).props.get(name)!r})", 2000)
        self.pause()

    def open_handler(self, event):
        """Open the Events tab of the Properties panel and double-click the event."""
        panel = self.window.properties
        bar = panel.tabs.tabBar()
        QTest.mouseClick(bar, Qt.LeftButton, pos=bar.tabRect(1).center())
        sleep(0)
        model = panel.events_model
        row = next((row for row in range(model.rowCount()) if model.item(row, 0).text() == event), None)
        self.check(row is not None, f"the Events tab has no “{event}” for {panel.names}")
        index = model.index(row, 0)
        panel.events_view.scrollTo(index)
        centre = panel.events_view.visualRect(index).center()
        QTest.mouseClick(panel.events_view.viewport(), Qt.LeftButton, pos=centre)
        QTest.mouseDClick(panel.events_view.viewport(), Qt.LeftButton, pos=centre)
        handler = handler_name(panel.names[0], event)
        self.wait(lambda: self.window.code_panel.current == ("handler", handler), f"the editor to open {handler}", 2000)
        self.check(self.window.tabs.currentWidget() is self.window.code_panel, "the Code tab did not come to the front")
        QTest.mouseClick(bar, Qt.LeftButton, pos=bar.tabRect(0).center())
        self.pause()
        return handler

    def type_code(self, text):
        """Type in the code editor, key by key."""
        editor = self.window.code_panel.editor
        editor.setFocus()
        for index, line in enumerate(text.split("\n")):
            if index:
                QTest.keyClick(editor, Qt.Key_Return)
            QTest.keyClicks(editor, line)
            QTest.keyClick(editor, Qt.Key_Escape)  # closes the suggestions, which Enter would accept
        self.pause()

    def save_as(self, path):
        self.answer_file_dialog(path)
        self.choose(self.window.save_as_action)
        self.equal(str(self.window.document.path), str(path), "path of the project after Save As")
        self.check(path.exists(), f"{path} was not written")

    def run(self):
        """Press Start and wait for the first picture of the simulator."""
        panel = self.window.sim_panel
        self.choose(self.window.run_action)
        errors = self.window.errors
        self.wait(lambda: panel.first_frame_ms is not None or errors.topLevelItemCount(), "the first frame of the simulator", 20000)
        self.check(not errors.topLevelItemCount(), "the Errors panel says: " + "; ".join(errors.topLevelItem(row).text(2) for row in range(errors.topLevelItemCount())))
        self.check(self.window.tabs.currentWidget() is panel, "the Simulator tab did not come to the front")
        sleep(300)  # the first frames draw the page
        self.pause(2)

    def tap(self, x, y):
        """Press and release the mouse on the simulator at the screen coordinates x, y."""
        screen = self.window.sim_panel.screen
        target = screen._target()
        point = QPoint(int(target.x() + (x + 0.5) * target.width() / screen.image.width()), int(target.y() + (y + 0.5) * target.height() / screen.image.height()))
        QTest.mousePress(screen, Qt.LeftButton, pos=point)
        sleep(150)
        QTest.mouseRelease(screen, Qt.LeftButton, pos=point)
        sleep(250)
        self.pause()

    def wait_preview(self):
        """Wait until the page shows the real LVGL picture of the project as it is now."""
        from lvgl_mpy_studio.build.preview import design_key

        view, renderer = self.designer(), self.window.preview_renderer
        page_id = view.designer_scene.page_id
        index = next(position for position, page in enumerate(self.project.pages) if page.id == page_id)
        self.wait(lambda: not renderer.busy and renderer._done.get(page_id) == design_key(self.project, index), "the page to show the LVGL picture of the last change", 5000)
        sleep(0)
        image = view.designer_scene.preview_image
        self.check(image is not None and view.designer_scene.show_preview, "the page shows no LVGL picture")
        return image.copy()

    def frame(self):
        return self.window.sim_panel.framebuffer.copy()

    def output(self):
        return self.window.output.toPlainText()

    def stop(self):
        self.choose(self.window.stop_action)
        self.wait(lambda: not self.window.sim_panel.running, "the simulator to stop")

    def close(self):
        """Close the window, whatever state a failed step left it in."""
        try:
            if self.window.sim_panel.running:
                self.window.sim_panel.shutdown()
            if self.window.document.modified:
                self.answer_message(QMessageBox.Discard)
            self.window.close()
            sleep(50)
        finally:
            self._watcher.stop()
            self.window.deleteLater()
            sleep(0)
