"""The garbage collector runs only in the main thread.

Python runs it in the thread that is allocating: a Qt object in a reference cycle would be
destroyed by the worker thread, with rare crashes in the event loop. Background measures use
Python threads, so automatic collection stays off and a timer of the main thread does it,
with the same thresholds.
"""

import gc

from PySide6.QtCore import QCoreApplication, QTimer

INTERVAL_MS = 500
_timer = None


def _collect():
    counts, thresholds = gc.get_count(), gc.get_threshold()
    for generation in (2, 1, 0):
        if thresholds[generation] and counts[generation] > thresholds[generation]:
            gc.collect(generation)
            return


def install():
    global _timer
    if _timer is not None:
        return
    gc.disable()
    _timer = QTimer(QCoreApplication.instance())
    _timer.timeout.connect(_collect)
    _timer.start(INTERVAL_MS)
