import threading

from PySide6.QtCore import QTimer

POLL_MS = 50


def run_in_background(parent, work, done):
    """Run work in a thread and call done(ok, result) in the main thread.

    The thread touches no Qt objects: a timer of the main thread collects the result.
    """
    box = []

    def runner():
        try:
            box.append((True, work()))
        except Exception as exc:
            box.append((False, exc))

    timer = QTimer(parent)
    timer.setInterval(POLL_MS)

    def check():
        if box:
            timer.stop()
            timer.deleteLater()
            done(*box[0])

    timer.timeout.connect(check)
    threading.Thread(target=runner, daemon=True).start()
    timer.start()
