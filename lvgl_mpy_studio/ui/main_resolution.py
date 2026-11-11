import copy

from PySide6.QtWidgets import QDialog

from lvgl_mpy_studio.core.boards import portable_profile, validate_profile
from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.ui.profile_manager import ProfileManagerDialog
from lvgl_mpy_studio.ui.project_settings import ProjectSettingsDialog
from lvgl_mpy_studio.ui.resolution import MODE_KEY, CustomSizeDialog, ResizeDialog, board_name


class ResolutionMixin:
    """Display size and board profile of the project. A part of MainWindow."""

    def _resize_mode(self, new_size, allow_keep=True, note="", old_size=None):
        """Ask what to do with the widgets and remember the choice; None if the user cancels."""
        display = self.document.project.display
        old_size = old_size or (display.width, display.height)
        if tuple(new_size) == tuple(old_size):
            return "keep"
        saved = self.settings.value(MODE_KEY, "adapt")
        dialog = ResizeDialog(old_size, new_size, saved, allow_keep, note, self)
        if dialog.exec() != QDialog.Accepted:
            return None
        self.settings.setValue(MODE_KEY, dialog.mode())
        return dialog.mode()

    def _session_blocks_resize(self):
        if self.sim_panel.running or self.device_app_active:
            self.append_error(tr("Stop the session before changing the resolution or profile."))
            return True
        return False

    def change_resolution(self, width, height):
        project = self.document.project
        if (width, height) == (project.display.width, project.display.height) or self._session_blocks_resize():
            return False
        board = project.board
        unlink = bool(board) and (board["logicalWidth"], board["logicalHeight"]) != (width, height)
        note = tr("The project uses the board {name} ({size}): it will be unlinked and the simulator selected.", name=board_name(board), size=f"{board['logicalWidth']}×{board['logicalHeight']}") if unlink else ""
        mode = self._resize_mode((width, height), note=note)
        if mode is None:
            return False
        def mutate(project):
            project.resize(width, height, mode)
            if unlink:
                project.board = None
                project.runTarget = None
        self.document.execute(tr("Change Resolution"), mutate)
        self._report_outside(width, height)
        return True

    def _custom_resolution(self):
        display = self.document.project.display
        dialog = CustomSizeDialog((display.width, display.height), self)
        if dialog.exec() == QDialog.Accepted:
            self.change_resolution(*dialog.size())

    def _report_outside(self, width, height):
        outside = self.document.project.widgets_outside(width, height)
        if outside:
            self.output.appendPlainText(tr("Widgets outside canvas: {names}", names=", ".join(outside)))

    def _update_adapt_page_action(self):
        self.adapt_page_action.setEnabled(bool(self._selected_page().designSize))

    def adapt_current_page(self):
        page = self._selected_page()
        if not page.designSize or self._session_blocks_resize():
            return False
        display = self.document.project.display
        mode = self._resize_mode((display.width, display.height), allow_keep=False, old_size=page.designSize)
        if mode is None:
            return False
        self.document.execute(tr("Adapt Page to Resolution"), lambda project: project.adapt_page(next(item for item in project.pages if item.id == page.id), mode))
        self._report_outside(display.width, display.height)
        return True

    def open_project_settings(self):
        if self._session_blocks_resize():
            return False
        dialog = ProjectSettingsDialog(self.document.project, self.profile_store.profiles(), self)
        if dialog.exec() != QDialog.Accepted:
            return False
        width, height, profile = dialog.values()
        mode = self._resize_mode((width, height))
        if mode is None:
            return False
        def mutate(project):
            project.resize(width, height, mode)
            project.board = copy.deepcopy(profile)
        self.document.execute(tr("Change Project Settings"), mutate)
        self._report_outside(width, height)
        return True

    def update_project_profile(self):
        current = self.document.project.board
        profile = self.profile_store.get(current["id"]) if current else None
        if not current or not profile:
            self.append_error(tr("The profile is not in the catalog; the project's portable copy remains available."))
            return False
        try:
            validate_profile(profile)
        except ValueError as exc:
            self.append_error(str(exc))
            return False
        def mutate(project):
            project.board = portable_profile(profile)
            project.scale_to(profile["logicalWidth"], profile["logicalHeight"])
        self.document.execute(tr("Update Project Profile"), mutate)
        return True

    def manage_profiles(self):
        dialog = ProfileManagerDialog(self.profile_store, self)
        dialog.exec()
        self._update_device_actions()
