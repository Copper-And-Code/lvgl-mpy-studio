
import pytest
from PySide6.QtCore import QPoint, Qt
from PySide6.QtNetwork import QHostAddress, QTcpSocket
from PySide6.QtTest import QTest

from lvgl_mpy_studio.build.compiler import compile_python
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.platform import runtime_path
from lvgl_mpy_studio.sim.protocol import encode_hello
from lvgl_mpy_studio.ui.document import ProjectDocument
from lvgl_mpy_studio.ui.sim_panel import SimPanel, SimScreen

pytestmark = pytest.mark.skipif(not runtime_path().exists(), reason="native runtime not built")


def test_start_frame_click_and_stop(qtbot, tmp_path):
    project = Project("sim_panel")
    project.add_widget(project.pages[0], "button", name="button1")
    project.add_widget(project.pages[0], "label", {"x": 30, "y": 120}, "label1")
    _name, handler = project.ensure_handler("button1")
    handler.body = 'ui.label1.set_text("Cliccato")\nprint("CLICK_OK")'
    output = tmp_path / "generated"
    generate_project(project, output)
    compile_python(output)
    document = ProjectDocument(project)
    panel = SimPanel(document)
    qtbot.addWidget(panel)
    panel.resize(800, 540)
    panel.show()
    messages = []
    errors = []
    panel.output.connect(lambda text, error: messages.append(text))
    panel.error.connect(errors.append)
    try:
        panel.start(output)
        assert document.read_only
        with qtbot.waitSignal(panel.frameReady, timeout=5000, raising=True):
            pass
        assert panel.first_frame_ms is not None, (errors, messages)
        assert panel.framebuffer.width() == 800
        assert panel.framebuffer.height() == 480
        target = panel.screen._target()
        x = target.x() + 70 * target.width() / 800
        y = target.y() + 70 * target.height() / 480
        point = QPoint(int(x), int(y))
        QTest.mousePress(panel.screen, Qt.LeftButton, Qt.NoModifier, point)
        qtbot.wait(100)
        QTest.mouseRelease(panel.screen, Qt.LeftButton, Qt.NoModifier, point)
        qtbot.waitUntil(lambda: "CLICK_OK" in "".join(messages), timeout=5000)
        panel.stop()
        with qtbot.waitSignal(panel.stopped, timeout=5000, raising=True):
            pass
        assert not panel.running
        assert not document.read_only
    finally:
        panel.shutdown()
    assert panel.process.state() == panel.process.ProcessState.NotRunning


def connect_unauthenticated(qtbot, panel):
    panel._token = bytes(range(16))
    assert panel.server.listen(QHostAddress.LocalHost, 0)
    client = QTcpSocket(panel)
    with qtbot.waitSignal(panel.server.newConnection, timeout=1000, raising=True):
        client.connectToHost(QHostAddress.LocalHost, panel.server.serverPort())
    # The server sees newConnection before the client is connected: writing now would lose the data.
    qtbot.waitUntil(lambda: client.state() == QTcpSocket.SocketState.ConnectedState, timeout=1000)
    return client


def test_rejects_wrong_hello_token(qtbot):
    panel = SimPanel()
    qtbot.addWidget(panel)
    errors = []
    panel.error.connect(errors.append)
    client = connect_unauthenticated(qtbot, panel)
    client.write(encode_hello(800, 480, bytes(16)))
    client.flush()
    qtbot.waitUntil(lambda: bool(errors), timeout=1000)
    assert "token" in errors[0]
    assert not panel._authenticated
    assert panel.socket is None


def test_rejects_missing_hello_after_timeout(qtbot):
    panel = SimPanel()
    qtbot.addWidget(panel)
    errors = []
    panel.error.connect(errors.append)
    connect_unauthenticated(qtbot, panel)
    qtbot.waitUntil(lambda: bool(errors), timeout=3000)
    assert "HELLO" in errors[0]
    assert not panel._authenticated
    assert panel.socket is None


def test_physical_pixel_scaling_uses_device_pixel_ratio(qtbot):
    class HiDpiScreen(SimScreen):
        def devicePixelRatioF(self):
            return 2.0

    screen = HiDpiScreen()
    qtbot.addWidget(screen)
    screen.resize(2000, 1200)
    screen.set_physical_pixels(True)
    target = screen._target()
    assert target.width() == 400
    assert target.height() == 240
    assert screen._coordinates(target.center()) == (400, 240)
    screen.toggle_zoom()
    target = screen._target()
    assert target.width() == 800
    assert target.height() == 480


def test_unicode_project_path_start_and_stop(qtbot, tmp_path):
    project = Project("Progetto è")
    project.add_widget(project.pages[0], "button", name="button1")
    output = tmp_path / "Nunzio Raciti" / "Progetto è" / "build py"
    generate_project(project, output)
    compile_python(output)
    panel = SimPanel()
    qtbot.addWidget(panel)
    errors = []
    panel.error.connect(errors.append)
    try:
        panel.start(output)
        with qtbot.waitSignal(panel.frameReady, timeout=5000, raising=True):
            pass
        assert not errors
        panel.stop()
        with qtbot.waitSignal(panel.stopped, timeout=5000, raising=True):
            pass
    finally:
        panel.shutdown()
    assert not panel.running
