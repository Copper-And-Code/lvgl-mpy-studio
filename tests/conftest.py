import atexit
import os
import shutil
import tempfile

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# Tests do not touch the configuration of whoever runs them: on Linux QSettings (recent files,
# language, layout), custom board profiles, MCP and autostart backups follow XDG_CONFIG_HOME.
# It must be set before Qt reads the path, that is before any QSettings. On Windows
# QSettings uses the registry and this is not enough.
_config = tempfile.mkdtemp(prefix="lvgl-mpy-studio-tests-config-")
os.environ["XDG_CONFIG_HOME"] = _config
atexit.register(shutil.rmtree, _config, ignore_errors=True)

from lvgl_mpy_studio.core.i18n import set_language  # noqa: E402

@pytest.fixture(autouse=True)
def no_real_serial_ports(monkeypatch):
    """This PC may have real boards attached: a test DeviceSession must never open their ports."""
    try:
        from lvgl_mpy_studio.device import service
    except ImportError:  # without pyserial nothing can open a port
        return
    monkeypatch.setattr(service, "default_interrupt", lambda port: None)


@pytest.fixture(autouse=True)
def default_language():
    """A test that switches language leaves English, the default, for the next one."""
    try:  # the tests of the core run also where Qt is not installed
        from PySide6.QtCore import QSettings
    except ImportError:
        pass
    else:
        QSettings("CopperAndCode", "LVGL MPY Studio").remove("language")
    set_language("en")


@pytest.fixture(autouse=True)
def no_blocking_question(monkeypatch):
    """A failed test can leave a window with unsaved changes: closing it must not wait for an answer."""
    try:
        from PySide6.QtWidgets import QMessageBox
    except ImportError:
        return
    monkeypatch.setattr(QMessageBox, "question", lambda *arguments, **options: QMessageBox.Discard)
