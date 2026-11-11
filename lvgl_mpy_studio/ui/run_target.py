from dataclasses import dataclass

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import QMenu, QToolButton

from lvgl_mpy_studio.core.i18n import tr


@dataclass(frozen=True)
class RunTarget:
    kind: str = "simulator"
    profile_id: str | None = None

    @property
    def is_board(self):
        return self.kind == "board"


SIMULATOR_MICROPYTHON = RunTarget()


def board_target(profile_id):
    return RunTarget("board", profile_id)


class RunTargetSelector(QToolButton):
    """The one place to choose where to run: language, board and port."""

    targetSelected = Signal(object)
    changePortRequested = Signal()
    manageProfilesRequested = Signal()
    saveDefaultRequested = Signal()
    clearDefaultRequested = Signal()

    def __init__(self, entries, current, has_default, parent=None):
        super().__init__(parent)
        self._entries = entries
        self._current = current
        self._has_default = has_default
        self.setObjectName("runTargetSelector")
        self.setPopupMode(QToolButton.InstantPopup)
        self.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.setMenu(QMenu(self))
        self.menu().aboutToShow.connect(self.rebuild)
        self.rebuild()

    def rebuild(self):
        menu = self.menu()
        menu.clear()
        group = QActionGroup(menu)
        self._add_target(menu, group, tr("Simulator"), SIMULATOR_MICROPYTHON)
        menu.addSection(tr("Board"))
        for profile_id, name, port in self._entries():
            self._add_target(menu, group, f"{name} · {port or tr('no port')}", board_target(profile_id))
        menu.addSeparator()
        change_port = menu.addAction(tr("Change Port…"), lambda: self.changePortRequested.emit())
        change_port.setEnabled(self._current().is_board)
        menu.addAction(tr("Manage Board Profiles…"), lambda: self.manageProfilesRequested.emit())
        menu.addSeparator()
        menu.addAction(tr("Use as default for new projects"), lambda: self.saveDefaultRequested.emit())
        clear_default = menu.addAction(tr("Remove default"), lambda: self.clearDefaultRequested.emit())
        clear_default.setEnabled(self._has_default())
        self.setText(self.label())

    def _add_target(self, menu, group, text, target):
        action = QAction(text, menu, checkable=True, checked=target == self._current())
        action.setData(target)
        action.triggered.connect(lambda _checked=False, value=target: self.targetSelected.emit(value))
        group.addAction(action)
        menu.addAction(action)

    def target_actions(self):
        return [action for action in self.menu().actions() if isinstance(action.data(), RunTarget)]

    def label(self):
        current = self._current()
        if current.is_board:
            return next((f"{name} · {port or tr('no port')}" for profile_id, name, port in self._entries() if profile_id == current.profile_id), current.profile_id)
        return tr("Simulator")
