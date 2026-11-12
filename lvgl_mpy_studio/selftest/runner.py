"""Runs the scenarios and writes the report."""

import os
import platform
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path


def isolate_settings(directory):
    """Keep the run away from the user's settings, recent files and board profiles.

    It must happen before Qt reads any setting."""
    os.environ["XDG_CONFIG_HOME"] = str(directory)
    from PySide6.QtCore import QSettings

    QSettings.setDefaultFormat(QSettings.IniFormat)  # on Windows the native format is the registry
    QSettings.setPath(QSettings.IniFormat, QSettings.UserScope, str(directory))


def main(names=(), show=False, slow_ms=0, output=None, list_only=False, echo=print):
    from .scenarios import SCENARIOS

    if list_only:
        for name, (title, _function) in SCENARIOS.items():
            echo(f"{name:<10} {title}")
        return 0
    unknown = [name for name in names if name not in SCENARIOS]
    if unknown:
        echo("Unknown scenario: " + ", ".join(unknown) + ". Use --list.")
        return 2
    if not show:
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
    settings = Path(tempfile.mkdtemp(prefix="lvgl-mpy-studio-selftest-"))
    isolate_settings(settings)

    from PySide6.QtCore import Qt, qInstallMessageHandler, qVersion
    from PySide6.QtWidgets import QApplication

    from lvgl_mpy_studio import __version__
    from lvgl_mpy_studio.core.i18n import set_language

    from .driver import Ide, ScenarioStopped
    from .report import Report

    # Two lines Qt prints for every window when nothing is shown: they hide the report and say nothing of the IDE.
    noise = ("This plugin does not support propagateSizeHints()", "QFontDatabase: Cannot find font directory", "Note that Qt no longer ships fonts")
    previous = qInstallMessageHandler(None)
    qInstallMessageHandler(lambda kind, context, message: None if message.startswith(noise) else (previous(kind, context, message) if previous else print(message, file=sys.stderr)))
    QApplication.setAttribute(Qt.AA_DontUseNativeDialogs)  # the system's own dialogs cannot be answered from here
    app = QApplication.instance() or QApplication(sys.argv[:1])
    set_language("en")
    directory = Path(output) if output else Path.cwd() / "lvgl-mpy-studio-selftest" / datetime.now().strftime("%Y%m%d-%H%M%S")
    report = Report(directory, echo)
    header = [
        f"LVGL MPY Studio {__version__} self-test, {datetime.now().isoformat(timespec='seconds')}",
        f"{platform.platform()}, Python {platform.python_version()}, Qt {qVersion()}, " + ("on screen" if show else "hidden") + (f", slowed by {slow_ms} ms" if slow_ms else ""),
    ]
    for line in header:
        echo(line)
    try:
        for name in names or SCENARIOS:
            title, function = SCENARIOS[name]
            report.scenario(title)
            work = directory / "work" / name
            work.mkdir(parents=True, exist_ok=True)
            ide = Ide(report, title, work, slow_ms)
            try:
                function(ide)
            except ScenarioStopped:
                ide.skipped()
            finally:
                ide.close()
        return 0 if report.finish(header) else 1
    finally:
        app.processEvents()
        shutil.rmtree(settings, ignore_errors=True)
