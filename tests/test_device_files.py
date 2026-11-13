"""Device → Upload Files… and Run File on Board…: files and programs outside the project."""

import re
import time
from pathlib import Path

import pytest

from lvgl_mpy_studio.device.common import DeviceError
from lvgl_mpy_studio.device.service import DeviceSession
from lvgl_mpy_studio.gen.board_gen import _bytecode_file
from lvgl_mpy_studio.ui.device_files import folder_items, protected_targets, run_line, shadowed_modules


class FakeBoard(DeviceSession):
    """A board whose files live in a dict; it answers the scripts of upload_files as a real one would."""

    def __init__(self, free=10_000_000, mpy=None):
        super().__init__(runner=lambda command, timeout: "")
        self.port = "/dev/fake"
        self.profile = {"id": "fake"}
        self.files = {"/flash/notes.txt": b"mine"}
        self.folders = set()
        self.free = free
        self.mpy = mpy

    def _info(self, profile=None):
        return {"mpy": self.mpy}

    def _put(self, source, destination, cancel=None, written=None):
        data = Path(source).read_bytes()
        self.files[destination] = data
        if written:
            written(len(data))

    def _exec(self, source, timeout=20, cancel=None):
        if "LVGL_MPY_STUDIO_FREE" in source:
            self.folders.update(re.search(r"for d in (\[.*?\]):", source).group(1).strip("[]").replace("'", "").split(", "))
            return f"LVGL_MPY_STUDIO_FREE={self.free}\n"
        name = re.search(r"n='(.*?)'", source).group(1)
        size = int(re.search(r"\[6\]!=(\d+)", source).group(1))
        if len(self.files.get(name + ".lms-part", b"")) != size:
            raise DeviceError("device.command", "OSError: incomplete")
        self.files[name] = self.files.pop(name + ".lms-part")
        return "LVGL_MPY_STUDIO_DONE=1\n"


def program(tmp_path):
    folder = tmp_path / "shell"
    folder.mkdir()
    (folder / "shell.py").write_text("print('shell')\n", encoding="utf-8")
    (folder / "main.py").write_text("import shell\n", encoding="utf-8")
    (folder / "game.bin").write_bytes(bytes(range(256)) * 4)  # binary, with every byte value
    (folder / "__pycache__").mkdir()
    (folder / "__pycache__" / "shell.cpython-312.pyc").write_bytes(b"x")
    return folder


def test_a_folder_is_copied_as_it_is_and_nothing_else_changes(tmp_path):
    board = FakeBoard()
    items = list(folder_items(program(tmp_path)))
    assert [name for _local, name in items] == ["shell/game.bin", "shell/main.py", "shell/shell.py"]
    reports = []
    result = board.upload_files(items, "/flash/", progress=lambda *report: reports.append(report))
    assert result["destination"] == "/flash"
    assert result["files"] == ["/flash/shell/game.bin", "/flash/shell/main.py", "/flash/shell/shell.py"]
    assert board.files["/flash/shell/game.bin"] == bytes(range(256)) * 4
    assert board.files["/flash/notes.txt"] == b"mine"
    assert not any(name.endswith(".lms-part") for name in board.files)
    assert {"/flash", "/flash/shell"} <= board.folders
    sent = [report[0] for report in reports]
    assert sent == sorted(sent) and reports[-1][:2] == (result["bytes"], result["bytes"])


def test_python_becomes_bytecode_except_main_and_boot(tmp_path):
    folder = program(tmp_path)
    reference = _bytecode_file(folder / "shell.py", tmp_path / "probe.mpy")
    if reference is None:
        pytest.skip("mpy-cross not built")
    board = FakeBoard(mpy=reference[1])
    result = board.upload_files([(folder / "shell.py", "shell.py"), (folder / "main.py", "main.py")], "/flash", compile_python=True)
    assert result["files"] == ["/flash/shell.mpy", "/flash/main.py"]
    assert board.files["/flash/shell.mpy"][:1] == b"M"
    assert result["warnings"] == []
    other = FakeBoard(mpy=reference[1] + 1)  # a firmware of another bytecode version
    result = other.upload_files([(folder / "shell.py", "shell.py")], "/flash", compile_python=True)
    assert result["files"] == ["/flash/shell.py"]
    assert "uploaded as source" in result["warnings"][0]


def test_without_space_nothing_is_copied(tmp_path):
    board = FakeBoard(free=100)
    with pytest.raises(DeviceError) as error:
        board.upload_files(list(folder_items(program(tmp_path))), "/sd")
    assert error.value.code == "device.space"
    assert set(board.files) == {"/flash/notes.txt"}


def test_paths_that_leave_the_folder_are_refused(tmp_path):
    board = FakeBoard()
    source = tmp_path / "a.txt"
    source.write_text("a")
    for items, destination in (([(source, "../a.txt")], "/flash"), ([(source, "a.txt")], "/flash/../etc")):
        with pytest.raises(DeviceError):
            board.upload_files(items, destination)
    assert set(board.files) == {"/flash/notes.txt"}


def test_files_a_board_runs_at_power_on_are_named():
    items = [(None, "boot.py"), (None, "main.py"), (None, "lib/main.py"), (None, "app/boot.py"), (None, "shell.py")]
    assert protected_targets(items, "/flash") == ["/flash/boot.py", "/flash/main.py", "/flash/app/boot.py"]
    assert protected_targets([(None, "main.py")], "/") == ["/main.py"]
    assert protected_targets([(None, "main.py")], "/sd/bin") == []


def test_a_folder_that_would_hide_a_module_is_named():
    board = [{"name": "shell.py", "dir": False, "size": 10}, {"name": "lib", "dir": True, "size": 0}, {"name": "vi.mpy", "dir": False, "size": 10}]
    shell = [(None, "shell/shell.py"), (None, "shell/demo.json")]
    assert shadowed_modules(shell, board) == ["shell"]  # /shell beside /shell.py: `import shell` finds the folder
    assert shadowed_modules([(None, "vi/vi.py")], board) == ["vi"]
    assert shadowed_modules([(None, "lib.py")], board) == ["lib"]
    assert shadowed_modules([(None, "tools/x.py"), (None, "tools.py")], []) == ["tools"]
    assert shadowed_modules([(None, "shell.py"), (None, "notes/a.txt"), (None, "lib/x.py")], board) == []  # what is there already is not this upload's doing


def test_run_line_runs_a_file_from_its_folder_or_types_code():
    assert run_line("/flash/shell.py") == "import os; os.chdir('/flash'); exec(open('shell.py').read(), {'__name__': '__main__', '__file__': '/flash/shell.py'})"
    assert run_line("main.py").startswith("import os; os.chdir('/');")
    assert run_line("import shell; shell.main()") == "import shell; shell.main()"


def test_run_file_on_board_types_at_the_prompt(qtbot, tmp_path):
    from lvgl_mpy_studio.ui.main_window import MainWindow

    class Port:
        def __init__(self):
            self.written = []
        def read_some(self):
            time.sleep(0.005)
            return b""
        def write(self, data):
            self.written.append(data)
        def close(self):
            pass

    window = MainWindow()
    qtbot.addWidget(window)
    port = Port()
    window.device = DeviceSession(console_factory=lambda name: port)
    window.device.port = "/dev/fake"
    assert window.run_file_on_board("/flash/shell.py")
    sent = b"".join(port.written)
    assert sent.startswith(b"\x03import os; os.chdir('/flash'); exec(open('shell.py').read()")
    assert sent.endswith(b"\r")
    assert window.device.console_live
    window.device.disconnect()
    window.document.undo_stack.setClean()


@pytest.mark.parametrize("answer", ["no", "yes"])
def test_the_upload_asks_before_a_folder_hides_a_module(qtbot, tmp_path, monkeypatch, answer):
    from PySide6.QtWidgets import QMessageBox
    from lvgl_mpy_studio.ui.main_window import MainWindow

    class Board(FakeBoard):
        def list_dir(self, path):
            return [{"name": name.rsplit("/", 1)[1], "dir": False, "size": len(data)} for name, data in self.files.items() if name.rsplit("/", 1)[0] == path]

    asked = []
    def question(_parent, _title, text, *args):
        asked.append(text)
        return QMessageBox.Yes if answer == "yes" else QMessageBox.No
    monkeypatch.setattr(QMessageBox, "question", question)
    window = MainWindow()
    qtbot.addWidget(window)
    window.device = Board()
    window.device.profile = window._board_profile()  # else the window closes a session of another board
    window.device.files["/flash/shell.py"] = b"print('old')"
    items = list(folder_items(program(tmp_path)))
    window._confirm_and_upload_files(items, "/flash")
    qtbot.waitUntil(lambda: bool(asked) and window._worker is None, timeout=5000)
    assert "shell/ — shell.py" in asked[0]
    if answer == "yes":
        qtbot.waitUntil(lambda: "/flash/shell/shell.py" in window.device.files and window._worker is None, timeout=5000)
    else:
        assert not any(name.startswith("/flash/shell/") for name in window.device.files)
    window.document.undo_stack.setClean()
