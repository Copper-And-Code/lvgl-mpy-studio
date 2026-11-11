import copy

from PySide6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel, QSpinBox, QVBoxLayout

from lvgl_mpy_studio.core.boards import portable_profile
from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.ui.resolution import COMMON_SIZES, board_name


class ProjectSettingsDialog(QDialog):
    def __init__(self, project, profiles, parent=None):
        super().__init__(parent)
        self.project = project
        self.setWindowTitle(tr("Project Settings"))
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.preset = QComboBox()
        self.preset.addItem(tr("Custom"), None)
        boards = {}
        for profile in profiles:
            boards.setdefault((profile["logicalWidth"], profile["logicalHeight"]), []).append(board_name(profile))
        for size in sorted(set(COMMON_SIZES) | set(boards)):  # common sizes and those of the known boards
            label = f"{size[0]}×{size[1]}" + (f" — {', '.join(boards[size])}" if size in boards else "")
            self.preset.addItem(label, size)
        self.preset.activated.connect(self._preset_selected)
        form.addRow(tr("Preset"), self.preset)
        self.width = QSpinBox(minimum=1, maximum=10000, value=project.display.width)
        self.height = QSpinBox(minimum=1, maximum=10000, value=project.display.height)
        dimensions = QHBoxLayout()
        dimensions.addWidget(self.width)
        dimensions.addWidget(self.height)
        form.addRow(tr("Resolution"), dimensions)
        self.profile = QComboBox()
        self.profile.setProperty("_lvgl_dynamic_items", True)
        self.profile.addItem(tr("No Profile"), None)
        current = copy.deepcopy(project.board)
        if current:
            current["origin"] = "project"
            self.profile.addItem(current["name"], current)
            self.profile.setCurrentIndex(self.profile.count() - 1)
        for profile in profiles:
            self.profile.addItem(profile["name"], profile)
        self.profile.activated.connect(self._profile_selected)
        form.addRow(tr("Board Profile"), self.profile)
        layout.addLayout(form)
        self.info = QLabel()
        self.info.setWordWrap(True)
        layout.addWidget(self.info)
        diagnostics = project.resolution_diagnostics()
        if diagnostics:
            self.info.setText("\n".join(diagnostics))
        self.buttons = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        self.buttons.button(QDialogButtonBox.Apply).setText(tr("Apply"))
        self.buttons.button(QDialogButtonBox.Cancel).setText(tr("Cancel"))
        self.buttons.button(QDialogButtonBox.Apply).clicked.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        self._sync_resolution()

    def _sync_resolution(self):
        profile = self.profile.currentData()
        for editor in (self.preset, self.width, self.height):
            editor.setEnabled(profile is None)
        if profile:
            self.width.setValue(profile["logicalWidth"])
            self.height.setValue(profile["logicalHeight"])

    def _preset_selected(self):
        size = self.preset.currentData()
        if size:
            self.width.setValue(size[0])
            self.height.setValue(size[1])

    def _profile_selected(self):
        profile = self.profile.currentData()
        self._sync_resolution()
        if profile:
            self.info.setText(tr("Physical display: {physical} — UI resolution: {logical} — Hardware scale: {scale}×", physical=f"{profile['physicalWidth']}×{profile['physicalHeight']}", logical=f"{profile['logicalWidth']}×{profile['logicalHeight']}", scale=profile["scale"]))

    def values(self):
        return self.width.value(), self.height.value(), portable_profile(self.profile.currentData())
