import copy
import threading

from PySide6.QtCore import QObject, QTimer, Signal

from lvgl_mpy_studio.build.budget import measure_budget
from lvgl_mpy_studio.core.i18n import tr

DELAY_MS = 1500
WARNING_RATIO = 0.8


def format_size(size):
    return f"{size / 1024:.0f} KB" if size < 1024 * 1024 else f"{size / (1024 * 1024):.1f} MB"


def budget_level(budget, limits):
    """0 normal, 1 near the limit, 2 over the limit."""
    ratios = [budget[key] / limits[key] for key in ("flash", "ram") if budget.get(key) is not None and limits.get(key)]
    worst = max(ratios, default=0)
    return 2 if worst > 1 else 1 if worst >= WARNING_RATIO else 0


def budget_text(budget, limits):
    if budget is None:
        return tr("Flash — · RAM —")
    def part(key):
        value = budget.get(key)
        if value is None:
            return "—"
        text = format_size(value)
        return f"{text} / {format_size(limits[key])}" if limits.get(key) else text
    return tr("Flash {flash} · RAM ~{ram}", flash=part("flash"), ram=part("ram"))


class BudgetMonitor(QObject):
    """Recompute the budget in the background, after a pause in the changes."""

    updated = Signal(object)

    def __init__(self, measure=measure_budget, delay=DELAY_MS, parent=None):
        super().__init__(parent)
        self._measure = measure
        self._project = None
        self._board_mpy = None
        self._running = False
        self._dirty = False
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(delay)
        self._timer.timeout.connect(self._start)
        self.updated.connect(self._completed)

    def schedule(self, project, board_mpy=None):
        self._project, self._board_mpy = project, board_mpy
        self._timer.start()

    def stop(self):
        self._timer.stop()
        self._dirty = False

    def _start(self):
        if self._running:
            self._dirty = True
            return
        self._running = True
        project = copy.deepcopy(self._project)
        threading.Thread(target=self._work, args=(project, self._board_mpy), daemon=True).start()

    def _work(self, project, board_mpy):
        try:
            result = self._measure(project, board_mpy)
        except Exception:
            result = None
        try:
            self.updated.emit(result)
        except RuntimeError:
            pass    # window already closed

    def _completed(self, _result):
        self._running = False
        if self._dirty:
            self._dirty = False
            self._timer.start()
