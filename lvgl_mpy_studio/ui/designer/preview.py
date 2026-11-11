import copy
import threading

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtGui import QImage

from lvgl_mpy_studio.build.preview import design_key, render_page

DELAY_MS = 60


def frame_image(pixels, width, height):
    return QImage(pixels, width, height, width * 2, QImage.Format_RGB16).copy()


class PreviewRenderer(QObject):
    """Render the page in the background; keeps only the last request."""

    rendered = Signal(str, object, int, int)

    def __init__(self, render=render_page, delay=DELAY_MS, parent=None):
        super().__init__(parent)
        self._render = render
        self._request = None
        self._running = False
        self._dirty = False
        self._delay = delay
        self._done = {}
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(delay)
        self._timer.timeout.connect(self._start)
        self.rendered.connect(self._completed)

    @property
    def busy(self):
        return self._running

    def request(self, project, page_id, page_index, immediate=False):
        key = design_key(project, page_index)
        if self._done.get(page_id) == key:
            return False
        self._request = (project, page_id, page_index, key)
        if immediate:
            self._timer.setInterval(0)
        self._timer.start()
        return True

    def stop(self):
        self._timer.stop()
        self._dirty = False

    def forget(self):
        self._done.clear()

    def _start(self):
        self._timer.setInterval(self._delay)
        if self._running:
            self._dirty = True
            return
        project, page_id, page_index, key = self._request
        self._running = True
        arguments = (copy.deepcopy(project), page_id, page_index, key)
        threading.Thread(target=self._work, args=arguments, daemon=True).start()

    def _work(self, project, page_id, page_index, key):
        try:
            pixels = self._render(project, page_index)
        except Exception:
            pixels = None
        if pixels is not None:
            self._done[page_id] = key
        try:
            self.rendered.emit(page_id, pixels, project.display.width, project.display.height)
        except RuntimeError:
            pass    # window already closed

    def _completed(self, *_result):
        self._running = False
        if self._dirty:
            self._dirty = False
            self._timer.start()
