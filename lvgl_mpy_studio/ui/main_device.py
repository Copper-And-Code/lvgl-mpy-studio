import copy
import json
import threading

from PySide6.QtWidgets import QDialog, QMessageBox

from lvgl_mpy_studio.build.compiler import traceback_errors
from lvgl_mpy_studio.core.boards import portable_profile
from lvgl_mpy_studio.core.i18n import device_error_text, tr
from lvgl_mpy_studio.device.service import DeviceError
from lvgl_mpy_studio.gen import live
from lvgl_mpy_studio.ui.device_panel import DeviceWorker, SelectDeviceDialog, UploadProgress


LIVE_DELAY_MS = 500


class DeviceMixin:
    """Board: connection, upload, console, live update and autostart. A part of MainWindow."""

    def _toggle_live(self, enabled):
        self.settings.setValue("device/live", enabled)
        self._schedule_live()

    def _remember_live_page(self):
        view = self._active_designer()
        if view is not None:  # from Code or Simulator the last open page stays
            self._live_page_id = view.designer_scene.page.id

    def _schedule_live(self, *_ignored):
        self._remember_live_page()
        if self.live_action.isChecked() and self.device_app_active and self._live_upload_key is not None:
            self._live_timer.start()

    def _live_page(self):
        self._remember_live_page()
        pages = self.document.project.pages
        ids = [page.id for page in pages]
        page_id = self._live_page_id if self._live_page_id in ids else self.document.project.currentPageId
        return ids.index(page_id) if page_id in ids else 0

    def _send_live(self):
        if not self.live_action.isChecked() or not self.device_app_active or self._live_upload_key is None:
            return
        if self._worker is not None:
            self._live_timer.start()
            return
        project = copy.deepcopy(self.document.project)
        if live.upload_key(project) != self._live_upload_key:
            self.statusBar().showMessage(tr("The code changed: press F5 to send it to the board."), 5000)
            return
        page = self._live_page()
        key = live.design_key(project, page)
        if key == self._live_design_key:
            return
        operation = lambda: self.device.live_update(live.live_script(project, page), cancel=self._device_cancel)
        def completed(_output):
            self._live_design_key = key
            self.statusBar().showMessage(tr("Board updated."), 3000)
        self._device_task(operation, completed)

    def _device_output(self, text):
        self.device_console.append(text)
        self._device_trace = (self._device_trace + text)[-20000:]
        if not self._device_sourcemap:
            return
        for mapped in self._trace_rows(traceback_errors(self._device_trace, self._device_sourcemap, {module.name for module in self.document.project.modules})):
            key = (mapped["file"], mapped["line"])
            if key in self._device_mapped_traces:
                continue
            self._device_mapped_traces.add(key)
            self._add_error_row(mapped)

    def _board_entries(self):
        profiles = self.profile_store.profiles()
        board = self.document.project.board
        if board and all(profile["id"] != board["id"] for profile in profiles):
            profiles.insert(0, board)
        return [(profile["id"], profile["name"], self._port_for(profile["id"])) for profile in profiles]

    def _port_for(self, profile_id):
        if profile_id not in self._ports:
            self._ports[profile_id] = self.settings.value(f"device/ports/{profile_id}", "")
        return self._ports[profile_id]

    @property
    def selected_port(self):
        board = self.document.project.board
        return self._port_for(board["id"]) if board else ""

    @selected_port.setter
    def selected_port(self, port):
        self._ports[self.document.project.board["id"]] = port

    def _remember_port(self, port):
        self.selected_port = port
        self.settings.setValue(f"device/ports/{self.document.project.board['id']}", port)

    def _sync_device_session(self):
        """A session is valid only for the profile it was opened with."""
        if self._worker is None and self.device.port and self.device.profile is not None and self.device.profile != self._board_profile():
            self.device.disconnect()
            self.device_app_active = False
            self._device_info = None

    def _board_profile(self):
        return portable_profile(self.document.project.board)

    def _update_device_actions(self):
        if not hasattr(self, "run_selector"):
            return
        busy = self._worker is not None
        connected = bool(self.device.port)
        board = self.run_target.is_board
        running = self.sim_panel.running
        self.run_selector.setText(self.run_selector.label())
        self.run_action.setEnabled(not busy and not running)
        self.run_action.setToolTip(tr("Run on: {target}", target=self.run_selector.label()))
        self.stop_action.setEnabled(not busy and (running if not board else connected and self.device_app_active))
        self.board_stop_action.setEnabled(not busy and connected and self.device_app_active)
        self.restart_action.setEnabled(not board and not busy)
        self.run_program_action.setEnabled(not running)
        self.upload_action.setEnabled(not busy and board)
        self.upload_run_action.setEnabled(not busy and board)
        self.device_info_action.setEnabled(not busy and connected)
        self.device_restart_action.setEnabled(not busy and connected)
        self.autostart_install_action.setEnabled(not busy and connected)
        self.autostart_remove_action.setEnabled(not busy and connected)
        self.select_device_action.setEnabled(not busy and board)
        self.connect_action.setText(tr("Disconnect") if connected else tr("Connect"))
        self.connect_action.setEnabled(not busy and (connected or board))
        self.project_settings_action.setEnabled(not running and not self.device_app_active and not busy)
        current = self.document.project.board
        catalog = self.profile_store.get(current["id"]) if current else None
        self.update_profile_action.setEnabled(bool(current and catalog and not busy))
        live = connected and not busy and self.device.console_live
        reason = "" if live else tr("IDE operation in progress…") if busy else self._console_problem or tr("Console not available.") if connected else tr("Board not connected")
        self.device_console.set_ready(live, reason)
        self.device_console.set_busy(busy)
        self.disconnect_button.setVisible(connected or board)
        if connected:
            self.device_status.setText(tr("Connected to {port}", port=self.device.port) + (" · " + tr("app active") if self.device_app_active else ""))
        else:
            self.device_status.setText(tr("Board not connected") if board else "")

    def _device_task(self, operation, success=None):
        if self._worker is not None:
            return False
        self._device_cancel = threading.Event()
        worker = DeviceWorker(operation, self)
        self._worker = worker
        worker.succeeded.connect(lambda result: self._device_succeeded(result, success))
        worker.failed.connect(self._device_failed)
        worker.progress.connect(self._upload_reported)
        worker.finished.connect(self._device_finished)
        worker.finished.connect(worker.deleteLater)
        self._update_device_actions()
        worker.start()
        return True

    def _upload_reported(self, sent, total, name, size):
        if self._upload_progress is not None:
            self._upload_progress.report(sent, total, name, size)

    def _close_upload_progress(self):
        dialog, self._upload_progress = self._upload_progress, None
        if dialog is not None:
            dialog.finish()

    def _device_succeeded(self, result, callback):
        if callback:
            callback(result)

    def _device_failed(self, error):
        self._device_next = None
        text = device_error_text(error.code, error.output) if isinstance(error, DeviceError) else str(error)
        self.device_console.message(text)
        self._show_warnings(getattr(error, "warnings", []))
        if isinstance(error, DeviceError) and error.errors:
            for mapped in error.errors:
                self._add_error_row(mapped)
        else:
            self.append_error(tr("Device Error") + ": " + text)
        self.statusBar().showMessage(tr("Device Error"), 5000)

    def _device_finished(self):
        worker = self.sender()
        if worker is not self._worker:
            return
        self._close_upload_progress()
        self._device_cancel = None
        self._worker = None
        following, self._device_next = self._device_next, None
        self._sync_device_session()
        if not following:
            self._start_device_console()
        self._update_device_actions()
        if following:
            following()

    def cancel_device_operation(self):
        if self._device_cancel:
            self._device_cancel.set()
            self.statusBar().showMessage(tr("Cancelling after the current command…"))

    def _choose_port(self, ports, continuation=None):
        dialog = SelectDeviceDialog(ports, self.selected_port, self)
        if dialog.exec() != QDialog.Accepted or not dialog.selected_port():
            return
        port = dialog.selected_port()
        if self.device.port and self.device.port != port:
            self.device.disconnect()
            self.device_app_active = False
            self._device_info = None
        self._remember_port(port)
        self._update_device_actions()
        if continuation:
            self._device_next = continuation

    def select_device(self):
        if not self.document.project.board:
            return False
        return self._device_task(self.device.list_ports, self._choose_port)

    def _with_connection(self, action):
        """Run action on the board, opening the connection first if it is missing."""
        if self.device.port:
            return action()
        if not self._board_profile():
            self.append_error(tr("Select a board profile in the project settings."))
            return False
        if self.selected_port:
            return self._connect(action)
        def found(ports):
            if len(ports) == 1:
                self._remember_port(ports[0]["port"])
                self._update_device_actions()
                self._device_next = lambda: self._connect(action)
            else:
                self._choose_port(ports, lambda: self._connect(action))
        return self._device_task(self.device.list_ports, found)

    def _connect(self, action):
        profile = self._board_profile()
        port = self.selected_port
        def connected(info):
            self.device_app_active = False
            self._device_info = info
            self._remember_board_memory(info)
            self._show_budget()
            self.device_console.message(json.dumps(info, ensure_ascii=False, indent=2))
            if info.get("compatible"):
                self._device_next = action
            else:
                self.append_error(tr("Firmware or resolution is incompatible with the profile."))
        return self._device_task(lambda: self.device.connect(port, profile), connected)

    def connect_disconnect(self):
        if self.device.port:
            self.device.disconnect()
            self.device_app_active = False
            self._device_info = None
            self._update_device_actions()
            return True
        return self._with_connection(lambda: True)

    def show_device_info(self):
        def completed(info):
            self._device_info = info
            self._remember_board_memory(info)
            self._show_budget()
            self.device_console.message(json.dumps(info, ensure_ascii=False, indent=2))
        return self._device_task(self.device.info, completed)

    def upload_board(self, run=False):
        if not self.run_target.is_board or not self.save_project():
            return False
        return self._with_connection(lambda: self._upload(run))

    def _upload(self, run):
        project = copy.deepcopy(self.document.project)
        base = self._project_dir()
        output = base / "build" / "board" / project.board["id"]
        self.errors.clear()
        self.statusBar().showMessage(tr("Uploading…"))
        operation = lambda: self.device.upload(project, output, run=run, progress=self._worker.progress.emit, cancel=self._device_cancel)
        def completed(result):
            self._show_warnings(result.get("warnings", []))
            if self._upload_progress is not None:  # the next upload to this board starts from the speed seen now
                self.settings.setValue(self._upload_rate_key, self._upload_progress.rate)
            self._device_sourcemap = result.get("sourcemap")
            self._device_trace = ""
            self._device_mapped_traces.clear()
            self._device_output(result.get("output", ""))
            self.device_app_active = bool(run and result.get("active"))
            self._live_upload_key = live.upload_key(project) if self.device_app_active else None
            self._live_design_key = live.design_key(project, next((index for index, page in enumerate(project.pages) if page.id == project.currentPageId), 0)) if self.device_app_active else None
            message = tr("Board application started; the LVGL timer remains active after bootstrap.") if run else tr("Upload completed")
            self.statusBar().showMessage(message, 5000)
            self.device_console.message(message)
        if not self._device_task(operation, completed):
            return False
        self._upload_rate_key = f"device/uploadRate/{project.board['id']}"
        self._upload_progress = UploadProgress(self, rate=self.settings.value(self._upload_rate_key, 0, type=float))
        self._upload_progress.cancelRequested.connect(self.cancel_device_operation)
        return True

    def _start_device_console(self):
        """The console follows the board whenever it is connected and the IDE is not using it."""
        if not self.device.port or self._worker is not None:
            return False
        self._console_problem = ""
        try:
            return self.device.start_console(self.deviceOutput.emit, interactive=True, on_closed=self.consoleClosed.emit)
        except DeviceError as exc:
            self._console_problem = tr("Console not available: {error}", error=device_error_text(exc.code, exc.output))
            return False

    def console_write(self, data):
        try:
            self.device.write(data)
        except DeviceError as exc:
            self.device_console.message(device_error_text(exc.code, exc.output))
            self._update_device_actions()

    def stop_board(self):
        def stopped(output):
            self.device_app_active = False
            self.device_console.append(output)
            self.statusBar().showMessage(tr("Board stopped; the last image may remain visible."), 5000)
        return self._device_task(self.device.stop, stopped)

    def restart_device(self):
        self.device_app_active = False
        return self._device_task(self.device.restart, lambda output: self.device_console.append(output))

    def install_autostart(self):
        project = copy.deepcopy(self.document.project)
        answer = QMessageBox.question(self, tr("Install Autostart…"), tr("/main.py on the board will be replaced. An existing main.py will be backed up locally; boot.py will not be changed. Continue?"))
        if answer != QMessageBox.Yes:
            return False
        return self._device_task(lambda: self.device.install_autostart(project), lambda result: self.statusBar().showMessage(tr("Autostart installed"), 5000))

    def remove_autostart(self):
        project = copy.deepcopy(self.document.project)
        answer = QMessageBox.question(self, tr("Remove Autostart…"), tr("Remove only the recognizable IDE launcher and restore any previous main.py?"))
        if answer != QMessageBox.Yes:
            return False
        return self._device_task(lambda: self.device.remove_autostart(project), lambda result: self.statusBar().showMessage(tr("Autostart removed"), 5000))
