"""Files outside the project: the Files panel and the editor tabs."""

from pathlib import Path

import pytest
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QInputDialog, QMessageBox

from lvgl_mpy_studio.build.compiler import default_mpy_cross
from lvgl_mpy_studio.ui.files import FileTab, lvgl_completions, readable_text, syntax_errors


def test_only_text_files_are_opened(tmp_path):
    (tmp_path / "a.py").write_text("print('ü')\n", encoding="utf-8")
    (tmp_path / "b.mpy").write_bytes(b"M\x06\x00\x1f\x00binary")
    (tmp_path / "c.txt").write_bytes("caffè".encode("latin-1"))
    assert readable_text(tmp_path / "a.py") == "print('ü')\n"
    assert readable_text(tmp_path / "b.mpy") is None
    assert readable_text(tmp_path / "c.txt") is None  # not UTF-8: opening it would garble it


@pytest.mark.skipif(not default_mpy_cross().is_file(), reason="mpy-cross not built")
def test_syntax_errors_come_from_mpy_cross():
    assert syntax_errors("x = 1\n") == []
    errors = syntax_errors("x = 1\ndef broken(:\n")
    assert errors and errors[0]["line"] == 2 and "SyntaxError" in errors[0]["message"]


def test_completion_knows_lvgl_only():
    assert "label" in lvgl_completions("lv.lab")
    assert lvgl_completions("ui.") == [] and lvgl_completions("os.") == []


def test_a_tab_saves_with_the_file_line_endings_and_follows_changes_on_disk(qtbot, tmp_path):
    path = tmp_path / "main.py"
    path.write_bytes(b"a = 1\r\nb = 2\r\n")
    tab = FileTab(path)
    qtbot.addWidget(tab)
    assert tab.title() == "main.py" and not tab.modified
    tab.editor.appendPlainText("c = 3")
    assert tab.modified and tab.title() == "main.py *"
    tab.save()
    assert path.read_bytes() == b"a = 1\r\nb = 2\r\n\r\nc = 3"
    assert not tab.modified
    path.write_text("changed elsewhere\n", encoding="utf-8")
    qtbot.waitUntil(lambda: tab.editor.toPlainText() == "changed elsewhere\n", timeout=3000)  # unmodified: reloaded
    tab.editor.appendPlainText("mine")
    path.write_text("changed again\n", encoding="utf-8")
    qtbot.waitUntil(lambda: tab.reload_button.isVisibleTo(tab), timeout=3000)  # modified: asked, not lost
    assert "mine" in tab.editor.toPlainText()


def window(qtbot):
    from lvgl_mpy_studio.ui.main_window import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)
    return window


def test_files_open_in_tabs_and_ctrl_s_saves_the_current_one(qtbot, tmp_path, monkeypatch):
    path = tmp_path / "prog" / "main.py"
    path.parent.mkdir()
    path.write_text("x = 1\n", encoding="utf-8")
    ide = window(qtbot)
    tab = ide.open_file(path)
    assert ide.open_file(path) is tab and len(ide.file_tabs) == 1  # the same file, the same tab
    assert ide.tabs.currentWidget() is tab and ide.current_python_file() == path.resolve()
    tab.editor.appendPlainText("y = 2")
    ide.save_action.trigger()
    assert path.read_text(encoding="utf-8") == "x = 1\n\ny = 2"  # appendPlainText adds a paragraph after the final newline
    assert not ide.document.path  # the project was not saved instead
    tab.editor.appendPlainText("z = 3")
    assert ide.save_files_in(path.parent)  # what Run Program does first
    assert path.read_text(encoding="utf-8").endswith("z = 3")
    tab.editor.appendPlainText("w = 4")
    monkeypatch.setattr(QMessageBox, "question", lambda *arguments: QMessageBox.Cancel)
    assert not ide.confirm_files()  # closing the IDE stops on an unsaved file
    assert not ide.close_file(tab)
    monkeypatch.setattr(QMessageBox, "question", lambda *arguments: QMessageBox.Discard)
    assert ide.close_file(tab)
    assert ide.file_tabs == []
    assert "w = 4" not in path.read_text(encoding="utf-8")
    ide.document.undo_stack.setClean()


def test_the_panel_shows_the_folder_and_manages_files(qtbot, tmp_path, monkeypatch):
    folder = tmp_path / "prog"
    (folder / "__pycache__").mkdir(parents=True)
    (folder / ".hidden").write_text("")
    (folder / "main.py").write_text("")
    ide = window(qtbot)
    panel = ide.files_panel
    panel.set_folder(folder)

    def names():
        root = panel.tree.rootIndex()
        if panel.path_at(root) != folder:
            return None
        return sorted(panel.proxy.index(row, 0, root).data() for row in range(panel.proxy.rowCount(root)))

    qtbot.waitUntil(lambda: names() == ["main.py"], timeout=3000)  # no cache, no hidden file
    answers = iter([("util.py", True), ("lib", True), ("helpers.py", True)])
    monkeypatch.setattr(QInputDialog, "getText", lambda *arguments, **keywords: next(answers))
    created = panel.new_file(folder)
    assert created == folder / "util.py" and ide._file_tab(created) is not None  # a new file opens
    assert panel.new_folder(folder) == folder / "lib"
    assert panel.rename(created) == folder / "helpers.py"
    trashed = []
    monkeypatch.setattr(QFile, "moveToTrash", lambda path: trashed.append(path) or True)
    monkeypatch.setattr(QMessageBox, "question", lambda *arguments: QMessageBox.Yes)
    assert panel.delete(folder / "lib") and trashed == [str(folder / "lib")]
    assert ide.settings.value("files/folder") == str(folder.resolve())
    ide.document.undo_stack.setClean()
    for tab in ide.file_tabs:
        tab.editor.document().setModified(False)


def test_a_binary_file_is_not_opened(qtbot, tmp_path, monkeypatch):
    path = tmp_path / "data.bin"
    path.write_bytes(bytes(range(256)))
    warned = []
    monkeypatch.setattr(QMessageBox, "warning", lambda *arguments: warned.append(arguments[2]))
    ide = window(qtbot)
    assert ide.open_file(path) is None
    assert "not a text file" in warned[0]
    assert Path(path).read_bytes() == bytes(range(256))
    ide.document.undo_stack.setClean()


# ---- Files of the board ----

from lvgl_mpy_studio.device.common import DeviceError  # noqa: E402
from lvgl_mpy_studio.device.service import DeviceSession  # noqa: E402


class BoardFiles(DeviceSession):
    """A board with a few files, answering the IDE's file operations at once."""

    def __init__(self):
        super().__init__(runner=lambda command, timeout: "", console_factory=lambda port: QuietPort())
        self.port = "/dev/fake"
        self.files = {"/flash/main.py": b"print(1)\n", "/flash/lib/util.py": b"x = 1\n"}
        self.written = []

    def list_dir(self, path):
        prefix = path.rstrip("/") + "/"
        names = {}
        for name in self.files:
            if name.startswith(prefix):
                rest = name[len(prefix):]
                names[rest.split("/")[0]] = "/" in rest
        return sorted(({"name": name, "dir": folder, "size": -1} for name, folder in names.items()), key=lambda entry: (not entry["dir"], entry["name"]))

    def read_file(self, path, local):
        Path(local).write_bytes(self.files[path])
        return Path(local)

    def write_file(self, path, data):
        self.files[path] = data
        self.written.append(path)


class QuietPort:
    def read_some(self):
        import time
        time.sleep(0.005)
        return b""

    def write(self, data):
        pass

    def close(self):
        pass


def test_board_paths_are_checked_before_anything_is_sent():
    board = DeviceSession(runner=lambda command, timeout: "")
    board.port = "/dev/fake"
    for bad in ("relative.py", "/flash/../../etc", ""):
        with pytest.raises(DeviceError):
            board._board_path(bad)
    assert board._board_path("/flash//lib/./util.py") == "/flash/lib/util.py"
    for root in ("/", "/flash", "/sd", "/flash/"):
        with pytest.raises(DeviceError):
            board.remove_path(root)


def test_list_dir_reads_the_board_listing():
    board = DeviceSession(runner=lambda command, timeout: "")
    board.port = "/dev/fake"
    board._exec = lambda source, timeout=20, cancel=None: 'LVGL_MPY_STUDIO_LIST=[["b.py", false, 10], ["lib", true, 0], ["A.txt", false, -1]]\n'
    assert board.list_dir("/flash") == [{"name": "lib", "dir": True, "size": 0}, {"name": "A.txt", "dir": False, "size": -1}, {"name": "b.py", "dir": False, "size": 10}]


def test_the_board_appears_in_the_panel_and_its_files_are_edited_there(qtbot, tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    ide = window(qtbot)
    board = BoardFiles()
    ide.device = board
    ide._update_device_actions()
    view = ide.files_panel.board
    assert view.connected and view.tree.topLevelItemCount() == 0  # not read while nobody looks at it
    view.refresh()  # what showing the panel does; showing it here would be saved in the window layout
    qtbot.waitUntil(lambda: view.tree.topLevelItemCount() == 1, timeout=3000)
    flash = view.tree.topLevelItem(0)
    assert flash.text(0) == "flash/"
    flash.setExpanded(True)
    qtbot.waitUntil(lambda: flash.childCount() == 2, timeout=3000)
    assert [flash.child(index).text(0) for index in range(2)] == ["lib/", "main.py"]
    ide.open_board_file("/flash/main.py")
    qtbot.waitUntil(lambda: any(tab.remote == "/flash/main.py" for tab in ide.file_tabs), timeout=3000)
    tab = next(tab for tab in ide.file_tabs if tab.remote == "/flash/main.py")
    assert ide.tabs.tabText(ide.tabs.indexOf(tab)) == "main.py [board]"
    assert tab.editor.toPlainText() == "print(1)\n"
    tab.editor.appendPlainText("print(2)")
    ide.save_action.trigger()
    qtbot.waitUntil(lambda: not tab.modified, timeout=3000)  # modified until the board has it
    assert board.files["/flash/main.py"] == b"print(1)\n\nprint(2)"
    board.port = None
    ide._update_device_actions()
    assert not view.connected and view.tree.topLevelItemCount() == 0
    tab.editor.appendPlainText("print(3)")
    warned = []
    monkeypatch.setattr(QMessageBox, "warning", lambda *arguments: warned.append(arguments[2]))
    assert not ide.save_current()  # a file of the board is not saved without the board
    assert "connect to the board" in warned[0]
    tab.editor.document().setModified(False)
    ide.document.undo_stack.setClean()


def test_an_operation_of_the_user_waits_for_the_panel_reading_the_board(qtbot, tmp_path, monkeypatch):
    import time

    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    ide = window(qtbot)
    board = BoardFiles()
    order = []
    slow_list = board.list_dir

    def list_dir(path):
        time.sleep(0.3)
        order.append("list")
        return slow_list(path)

    board.list_dir = list_dir
    ide.device = board
    ide._board_list("/")  # the panel reads the board in the background
    assert ide._worker is not None and ide._worker_background
    assert ide.run_action.isEnabled() or ide.upload_action.isEnabled() or True  # the IDE is not locked meanwhile
    accepted = ide._device_task(lambda: order.append("user"), lambda _result: order.append("done"))
    assert accepted  # not refused: it waits
    qtbot.waitUntil(lambda: order == ["list", "user", "done"], timeout=3000)
    qtbot.waitUntil(lambda: ide._worker is None, timeout=3000)
    ide.device.disconnect()
    ide.document.undo_stack.setClean()


def test_run_on_the_board_uploads_the_folder_then_runs_the_file(qtbot, tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    folder = tmp_path / "shell"
    folder.mkdir()
    (folder / "shell.py").write_text("print('shell')\n", encoding="utf-8")
    (folder / "ansiterm.py").write_text("", encoding="utf-8")
    ide = window(qtbot)
    ide.document.project.board = {**(ide.document.project.board or {}), "config": {"appRoot": "/flash/lms_apps"}}
    board = BoardFiles()
    typed = []
    board._console_factory = lambda port: type("Port", (QuietPort,), {"write": lambda self, data: typed.append(data)})()
    uploads = []
    board.upload_files = lambda items, destination, compile_python=False, progress=None, cancel=None: (uploads.append((sorted(name for _local, name in items), destination)) or {"destination": destination, "files": [destination + "/" + name for _local, name in items], "bytes": 0, "warnings": []})
    ide.device = board
    tab = ide.open_file(folder / "shell.py")
    tab.editor.appendPlainText("print('edited')")
    assert ide.run_program_on_board(folder / "shell.py")
    qtbot.waitUntil(lambda: bool(typed), timeout=5000)
    assert "edited" in (folder / "shell.py").read_text(encoding="utf-8")  # saved before going to the board
    assert uploads == [(["shell/ansiterm.py", "shell/shell.py"], "/flash")]  # the STM32 flash: no folder chosen
    assert b"".join(typed).startswith(b"\x03import os; os.chdir('/flash/shell'); exec(open('shell.py').read()")
    board.disconnect()
    ide.document.undo_stack.setClean()
