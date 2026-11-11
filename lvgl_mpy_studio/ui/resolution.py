"""Choosing the resolution from the toolbar, and what to do with the widgets when it changes."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLabel, QMenu, QRadioButton, QSpinBox, QToolButton, QVBoxLayout

from lvgl_mpy_studio.core.i18n import tr

COMMON_SIZES = ((240, 240), (480, 480), (1024, 600), (1024, 1024))
MODE_KEY = "resolution/mode"


def board_name(profile):
    """The name without the resolution, if it already holds it: next to the size it would be repeated."""
    size = f"({profile['logicalWidth']}×{profile['logicalHeight']})"
    return profile["name"].replace(size, "").strip() or profile["name"]


class ResizeDialog(QDialog):
    """Ask what to do with the widgets: nothing changes on its own."""

    def __init__(self, old_size, new_size, mode, allow_keep=True, note="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Change Resolution") if allow_keep else tr("Adapt Page to Resolution"))
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(tr("From {old} to {new}. What should happen to the widgets?", old=f"{old_size[0]}×{old_size[1]}", new=f"{new_size[0]}×{new_size[1]}")))
        self.options = {
            "adapt": QRadioButton(tr("Adapt: keep proportions, follow edges, centre and groups")),
            "stretch": QRadioButton(tr("Stretch: scale each axis on its own, the page stays full")),
        }
        if allow_keep:
            self.options["keep"] = QRadioButton(tr("Leave them where they are: adapt each page later"))
        for button in self.options.values():
            layout.addWidget(button)
        self.options.get(mode, self.options["adapt"]).setChecked(True)
        if note:
            warning = QLabel(note)
            warning.setWordWrap(True)
            layout.addWidget(warning)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText(tr("Apply"))
        buttons.button(QDialogButtonBox.Cancel).setText(tr("Cancel"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def mode(self):
        return next(name for name, button in self.options.items() if button.isChecked())


class CustomSizeDialog(QDialog):
    def __init__(self, size, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Custom Resolution"))
        form = QFormLayout(self)
        self.width = QSpinBox(minimum=1, maximum=10000, value=size[0])
        self.height = QSpinBox(minimum=1, maximum=10000, value=size[1])
        form.addRow(tr("Width"), self.width)
        form.addRow(tr("Height"), self.height)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def size(self):
        return self.width.value(), self.height.value()


class ResolutionSelector(QToolButton):
    """The resolution of the project, one click away: board sizes, common sizes, rotation."""

    sizeSelected = Signal(int, int)
    customRequested = Signal()

    def __init__(self, current, profiles, parent=None):
        super().__init__(parent)
        self._current = current
        self._profiles = profiles
        self.setObjectName("resolutionSelector")
        self.setPopupMode(QToolButton.InstantPopup)
        self.setToolButtonStyle(self.toolButtonStyle())
        self.setToolTip(tr("Project resolution"))
        self.setMenu(QMenu(self))
        self.menu().aboutToShow.connect(self.rebuild)
        self.rebuild()

    def rebuild(self):
        menu = self.menu()
        menu.clear()
        width, height = self._current()
        boards = {}
        for profile in self._profiles():
            size = (profile["logicalWidth"], profile["logicalHeight"])
            boards.setdefault(size, []).append(board_name(profile))
        if boards:
            menu.addSection(tr("Board"))
            for size in sorted(boards):
                self._add(menu, size, f"{size[0]}×{size[1]} — {', '.join(boards[size])}")
        menu.addSection(tr("Common"))
        for size in COMMON_SIZES:  # even if a board has the same size: here only the resolution is chosen
            self._add(menu, size, f"{size[0]}×{size[1]}")
        menu.addSeparator()
        rotate = menu.addAction(tr("Rotate ({size})", size=f"{height}×{width}"), lambda: self.sizeSelected.emit(height, width))
        rotate.setEnabled(width != height)
        menu.addAction(tr("Custom…"), lambda: self.customRequested.emit())  # a signal cannot be passed as an action
        self.setText(f"{width}×{height}")

    def _add(self, menu, size, text):
        action = menu.addAction(text, lambda: self.sizeSelected.emit(*size))
        action.setCheckable(True)
        action.setChecked(size == tuple(self._current()))
