"""Python modules in the interface: project tree, code editor, errors and simulator."""

import json
from pathlib import Path

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QDockWidget, QInputDialog, QMessageBox

from lvgl_mpy_studio.build.compiler import default_mpy_cross
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.core.modules import create_module
from lvgl_mpy_studio.platform import runtime_path
from lvgl_mpy_studio.ui.main_tree import NEW_MODULE_SOURCE
from lvgl_mpy_studio.ui.main_window import MainWindow

ROOT = Path(__file__).parents[1]
needs_runtime = pytest.mark.skipif(not runtime_path().exists(), reason="runtime not built")
needs_mpy_cross = pytest.mark.skipif(not default_mpy_cross().exists(), reason="mpy-cross not built")


class Answers:
    """Answers prepared for the dialogs, in the order the window opens them."""

    def __init__(self, monkeypatch):
        self.names, self.questions, self.warnings = [], [], []
        self.reply = QMessageBox.Yes
        monkeypatch.setattr(QInputDialog, "getText", self._text)
        monkeypatch.setattr(QMessageBox, "question", self._question)
        monkeypatch.setattr(QMessageBox, "warning", self._warning)

    def _text(self, _parent, title, label, *args, text="", **kwargs):
        self.questions.append((title, label, text))
        return self.names.pop(0) if self.names else ("", False)

    def _question(self, _parent, title, text, *args, **kwargs):
        self.questions.append((title, text))
        return self.reply

    def _warning(self, _parent, title, text, buttons=None, *args, **kwargs):
        self.warnings.append(text)
        return self.reply if buttons is not None else QMessageBox.Ok  # with Yes/No it is a question


@pytest.fixture
def answers(monkeypatch):
    return Answers(monkeypatch)


def window_with(qtbot, tmp_path, project=None):
    project = project or Project("moduli_gui")
    path = tmp_path / "progetto.json"
    project.save(path)
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.open_project(path)
    return window, path


def close(window):
    window.document.undo_stack.setClean()  # no save dialog on closing


def modules_node(window):
    tree = window.project_tree
    node = tree.topLevelItem(tree.topLevelItemCount() - 1)
    assert node.data(0, Qt.UserRole) == ("modules", None)
    return node


def tree_modules(window):
    node = modules_node(window)
    return [node.child(index).text(0) for index in range(node.childCount())]


def module_item(window, name):
    node = modules_node(window)
    return next(node.child(index) for index in range(node.childCount()) if node.child(index).text(0) == f"{name}.py")


def type_into_editor(window, text):
    """As if the user typed: it goes through textChanged, so through the document and undo."""
    window.code_panel.editor.selectAll()
    window.code_panel.editor.insertPlainText(text)


def source(window, name):
    return next(module.source for module in window.document.project.modules if module.name == name)


def test_create_a_module_from_the_tree_and_open_it(qtbot, tmp_path, answers):
    window, _path = window_with(qtbot, tmp_path)
    assert tree_modules(window) == []
    answers.names = [("utils", True)]
    window.new_module_action.trigger()
    assert [module.name for module in window.document.project.modules] == ["utils"]
    assert tree_modules(window) == ["utils.py"]
    # The new module opens in the code editor, the same as handlers.
    assert window.tabs.currentWidget() is window.code_panel
    assert window.code_panel.current[0] == "pymodule" and window.code_panel.module().name == "utils"
    assert "import utils" in window.code_panel.signature.text()
    assert window.code_panel.object_combo.currentText() == "Module: utils.py"
    assert window.document.undo_stack.undoText() == "New Module"
    # The same editor as the general code, with the same syntax colouring.
    editor = window.code_panel.editor
    assert editor.highlighter.document() is editor.document()
    type_into_editor(window, "def f():\n    return 'testo'  # commento\n")
    formats = editor.document().firstBlock().layout().formats()
    assert formats, "the def keyword is not coloured"
    close(window)


def test_a_new_module_starts_with_the_imports_and_the_editor_explains_them(qtbot, tmp_path, answers):
    project = Project("suggerimento")
    button = project.add_widget(project.pages[0], "button")
    window, _path = window_with(qtbot, tmp_path, project)
    answers.names = [("utils", True)]
    window.new_module()
    assert source(window, "utils") == "import lvgl as lv\nimport ui\n\n\n"
    assert window.code_panel.editor.toPlainText() == source(window, "utils")
    hint = window.code_panel.module_hint
    assert not hint.isHidden() and "import ui" in hint.text() and "import lvgl as lv" in hint.text()
    window.open_handler(button.name)  # handlers and general code already get ui and lv
    assert hint.isHidden()
    window.code_panel.open_source("module")
    assert hint.isHidden()
    window.open_module("utils")
    assert not hint.isHidden()
    close(window)


@needs_runtime
def test_a_function_of_a_new_module_can_use_ui(qtbot, tmp_path, answers):
    """The reported case: a module that writes to a label, called by the handler of a button."""
    from lvgl_mpy_studio.sim.script import play

    project = Project("ui_nel_modulo")
    button = project.add_widget(project.pages[0], "button", {"x": 20, "y": 20, "width": 120, "height": 50})
    label = project.add_widget(project.pages[0], "label", {"x": 20, "y": 100, "text": "Prima"})
    window, _path = window_with(qtbot, tmp_path, project)
    answers.names = [("test", True)]
    window.new_module()
    editor = window.code_panel.editor
    editor.moveCursor(QTextCursor.End)
    editor.insertPlainText(f"def module_my():\n    ui.{label.name}.set_text('Ciao dal modulo')\n")
    window.code_panel.open_source("module")
    type_into_editor(window, "import test\n")
    window.open_handler(button.name)
    type_into_editor(window, "test.module_my()")
    report = play(window.document.project, 0, [{"action": "wait", "ms": 100}, {"action": "tap", "widget": button.name}, {"action": "wait", "ms": 100}, {"action": "eval", "expr": f"ui.{label.name}.get_text()"}])
    assert not report["traceback"], report["console"]
    assert report["values"][0]["value"] == "Ciao dal modulo"
    close(window)


def test_context_menu_offers_module_actions_on_the_modules_node(qtbot, tmp_path):
    project = Project("menu")
    create_module(project, "utils")
    window, _path = window_with(qtbot, tmp_path, project)
    tree = window.project_tree
    shown = []
    for item in (modules_node(window), module_item(window, "utils"), tree.topLevelItem(0)):
        shown.append([action.text() for action in window._project_menu(item).actions() if action.text()])
    assert shown[0] == ["New Python Module…"]
    assert shown[1] == ["New Python Module…", "Open Module", "Rename Module…", "Delete Module"]
    assert "Add Page" in shown[2] and "New Python Module…" not in shown[2]
    # Open Module acts on the module chosen in the tree.
    tree.setCurrentItem(module_item(window, "utils"))
    window.open_module_action.trigger()
    assert window.tabs.currentWidget() is window.code_panel and window.code_panel.module().name == "utils"
    close(window)


def test_edit_save_close_and_reopen(qtbot, tmp_path, answers):
    window, path = window_with(qtbot, tmp_path)
    answers.names = [("utils", True)]
    window.new_module()
    type_into_editor(window, "def greet(name):\n    return 'ciao ' + name\n")
    assert source(window, "utils") == "def greet(name):\n    return 'ciao ' + name\n"
    assert window.document.modified
    assert window.save_project()
    assert not window.document.modified
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw["schemaVersion"] == 3 and raw["modules"][0]["name"] == "utils"
    assert raw["modules"][0]["source"] == "def greet(name):\n    return 'ciao ' + name\n"
    window.close()

    reopened, _path = MainWindow(), None
    qtbot.addWidget(reopened)
    assert reopened.open_project(path)
    assert tree_modules(reopened) == ["utils.py"]
    reopened._tree_activated(module_item(reopened, "utils"))  # double click
    assert reopened.tabs.currentWidget() is reopened.code_panel
    assert reopened.code_panel.editor.toPlainText() == "def greet(name):\n    return 'ciao ' + name\n"
    close(reopened)


def test_modules_are_listed_in_project_order_in_tree_and_editor(qtbot, tmp_path):
    project = Project("ordine")
    for name in ("zeta", "alfa", "media"):
        create_module(project, name)
    window, _path = window_with(qtbot, tmp_path, project)
    assert tree_modules(window) == ["zeta.py", "alfa.py", "media.py"]
    combo = window.code_panel.object_combo
    assert [combo.itemText(index) for index in range(1, 4)] == ["Module: zeta.py", "Module: alfa.py", "Module: media.py"]
    assert combo.itemText(0) == "(General)"
    close(window)


def test_rename_and_delete_warn_about_imports_left_behind(qtbot, tmp_path, answers):
    project = Project("rinomina")
    create_module(project, "helpers", "PREFIX = 'ciao '\n")
    create_module(project, "utils", "import helpers\n")
    project.code.module = "from helpers import PREFIX\n"
    window, _path = window_with(qtbot, tmp_path, project)
    window.project_tree.setCurrentItem(module_item(window, "helpers"))
    # The warning first: No leaves everything as it was.
    answers.names = [("common", True)]
    answers.reply = QMessageBox.No
    assert not window.rename_module()
    assert "ImportError" in answers.warnings[-1] and "(General): still imports helpers" in answers.warnings[-1] and "common" in answers.warnings[-1]
    assert tree_modules(window) == ["helpers.py", "utils.py"] and not window.document.modified
    answers.reply = QMessageBox.Yes
    answers.names = [("common", True)]
    assert window.rename_module()
    assert answers.questions[-1][2] == "helpers"  # the dialog proposes the current name
    assert tree_modules(window) == ["common.py", "utils.py"]
    output = window.output.toPlainText()
    assert "Warning: (General): still imports helpers" in output and "Warning: utils.py: still imports helpers" in output
    assert source(window, "utils") == "import helpers\n"  # imports are not rewritten
    # Deleting: the confirmation lists who imports it; No touches nothing.
    window.project_tree.setCurrentItem(module_item(window, "utils"))
    answers.reply = QMessageBox.No
    assert not window.delete_module()
    assert tree_modules(window) == ["common.py", "utils.py"]
    create_module_and_import = "import utils\n"
    window.code_panel.open_source("module")
    type_into_editor(window, create_module_and_import)
    window.project_tree.setCurrentItem(module_item(window, "utils"))
    answers.reply = QMessageBox.Yes
    assert window.delete_module()
    # A module still imported: a warning, not a plain question, and the risk is named.
    assert "(General): still imports utils" in answers.warnings[-1] and "ImportError" in answers.warnings[-1]
    assert tree_modules(window) == ["common.py"]
    assert "Warning: (General): still imports utils" in window.output.toPlainText()
    close(window)


def test_renaming_a_module_nothing_imports_asks_nothing_more(qtbot, tmp_path, answers):
    project = Project("libero")
    create_module(project, "utils")
    window, _path = window_with(qtbot, tmp_path, project)
    window.project_tree.setCurrentItem(module_item(window, "utils"))
    answers.names = [("tools", True)]
    assert window.rename_module()
    assert answers.warnings == [] and tree_modules(window) == ["tools.py"]
    close(window)


def test_undo_and_redo_follow_every_module_change(qtbot, tmp_path, answers):
    window, _path = window_with(qtbot, tmp_path)
    stack = window.document.undo_stack
    answers.names = [("utils", True)]
    window.new_module()
    type_into_editor(window, "A = 1\n")
    window.project_tree.setCurrentItem(module_item(window, "utils"))
    answers.names = [("tools", True)]
    window.rename_module()
    window.project_tree.setCurrentItem(module_item(window, "tools"))
    window.delete_module()
    assert tree_modules(window) == []
    stack.undo()  # delete
    assert tree_modules(window) == ["tools.py"] and source(window, "tools") == "A = 1\n"
    stack.undo()  # rename
    assert tree_modules(window) == ["utils.py"]
    window.open_module("utils")
    assert window.code_panel.editor.toPlainText() == "A = 1\n"
    stack.undo()  # text change: back to the text the module starts with
    assert source(window, "utils") == NEW_MODULE_SOURCE and window.code_panel.editor.toPlainText() == NEW_MODULE_SOURCE
    stack.undo()  # creation
    assert tree_modules(window) == [] and window.code_panel.current == ("module", "module")
    for _step in range(4):
        stack.redo()
    assert tree_modules(window) == []
    stack.undo()
    assert source(window, "tools") == "A = 1\n"
    close(window)


@pytest.mark.parametrize("name, reason", [
    ("time", "MicroPython"), ("ui", "file the IDE generates"), ("Utils", "lower case"), ("../x", "lower case"),
    ("class", "reserved"), ("helpers", "already exists"),
])
def test_invalid_names_are_refused_and_asked_again(qtbot, tmp_path, answers, name, reason):
    project = Project("nomi")
    create_module(project, "helpers")
    window, path = window_with(qtbot, tmp_path, project)
    before = window.document.project.to_dict()
    answers.names = [(name, True), ("", False)]  # invalid name, then cancel
    assert not window.new_module()
    assert len(answers.warnings) == 1 and reason in answers.warnings[0]
    assert answers.questions[-1][2] == name  # the dialog proposes again the text to correct
    assert window.document.project.to_dict() == before and not window.document.modified
    assert reason in window.errors.topLevelItem(window.errors.topLevelItemCount() - 1).text(2)
    close(window)


def test_a_handler_name_is_refused(qtbot, tmp_path, answers):
    project = Project("gestore")
    button = project.add_widget(project.pages[0], "button")
    handler, _body = project.ensure_handler(button.name)
    window, _path = window_with(qtbot, tmp_path, project)
    answers.names = [(handler, True), ("valido", True)]
    assert window.new_module()
    assert "handler" in answers.warnings[0]
    assert [module.name for module in window.document.project.modules] == ["valido"]
    close(window)


@needs_mpy_cross
def test_syntax_error_in_a_module_names_the_module_and_the_line(qtbot, tmp_path, answers):
    project = Project("sintassi")
    button = project.add_widget(project.pages[0], "button")
    handler, body = project.ensure_handler(button.name)
    body.body = "import utils\nutils.go()"
    window, _path = window_with(qtbot, tmp_path, project)
    answers.names = [("utils", True)]
    window.new_module()
    type_into_editor(window, "X = 1\n\ndef go(:\n    pass\n")
    window.code_panel.check_syntax()
    panel = window.code_panel
    assert panel.error.isVisible() if panel.isVisible() else not panel.error.isHidden()
    assert panel.error.text() == "utils.py, line 3: SyntaxError: invalid syntax"
    assert [selection.cursor.blockNumber() for selection in panel.editor.extraSelections()] == [2]
    # The handler that imports the module does not get the error.
    panel.open_source(handler)
    panel.check_syntax()
    assert panel.error.isHidden() and panel.editor.extraSelections() == []
    close(window)


def traceback_project():
    project = Project("traceback")
    button = project.add_widget(project.pages[0], "button", {"x": 20, "y": 20, "width": 120, "height": 50})
    handler, body = project.ensure_handler(button.name)
    body.body = "import utils\nutils.boom()"
    create_module(project, "utils", "def boom():\n    x = 1\n    raise ValueError('rotto nel modulo')\n")
    return project, button.name, handler


@needs_runtime
def test_traceback_from_a_module_opens_the_module_at_its_line(qtbot, tmp_path):
    from lvgl_mpy_studio.gen.project_gen import generate_project
    from lvgl_mpy_studio.sim.script import play

    project, button, handler = traceback_project()
    window, path = window_with(qtbot, tmp_path, project)
    report = play(window.document.project, 0, [{"action": "wait", "ms": 100}, {"action": "tap", "widget": button}, {"action": "wait", "ms": 200}])
    assert report["traceback"] and "rotto nel modulo" in report["console"]
    generate_project(window.document.project, window._build_dir())  # the source map the panel reads
    window._sim_output(report["console"], True)
    rows = [window.errors.topLevelItem(index) for index in range(window.errors.topLevelItemCount())]
    first = rows[0].data(0, Qt.UserRole)
    assert (rows[0].text(0), rows[0].text(1)) == ("utils.py", "3") and first["module"] == "utils" and first["origin"]
    caller = next(row.data(0, Qt.UserRole) for row in rows if row.data(0, Qt.UserRole).get("handler"))
    assert caller["handler"] == handler and not caller["origin"] and caller["message"].startswith("called from here")
    window._error_activated(rows[0])
    panel = window.code_panel
    assert window.tabs.currentWidget() is panel and panel.module().name == "utils"
    assert panel.editor.textCursor().blockNumber() == 2
    # The handler line leads to the handler, not to the module.
    window._error_activated(next(row for row in rows if row.data(0, Qt.UserRole).get("handler")))
    assert panel.current == ("handler", handler)
    close(window)


@needs_runtime
def test_a_module_imported_by_an_lvgl_handler_runs_on_a_tap(qtbot, tmp_path, answers):
    from lvgl_mpy_studio.sim.script import play

    project = Project("gestore_modulo")
    button = project.add_widget(project.pages[0], "button", {"x": 20, "y": 20, "width": 120, "height": 50})
    label = project.add_widget(project.pages[0], "label", {"x": 20, "y": 100, "text": "Prima"})
    window, _path = window_with(qtbot, tmp_path, project)
    answers.names = [("helpers", True)]
    window.new_module()
    type_into_editor(window, "PREFIX = 'ciao '\n")
    answers.names = [("utils", True)]
    window.new_module()
    type_into_editor(window, "import helpers\n\n\ndef greeting(name):\n    return helpers.PREFIX + name\n")
    window.open_handler(button.name)
    type_into_editor(window, f"import utils\nui.{label.name}.set_text(utils.greeting('Ada'))")
    report = play(window.document.project, 0, [{"action": "wait", "ms": 100}, {"action": "tap", "widget": button.name}, {"action": "wait", "ms": 100}, {"action": "eval", "expr": f"ui.{label.name}.get_text()"}])
    assert report["passed"] and not report["traceback"], report
    assert report["values"][0]["value"] == "ciao Ada"
    close(window)


@needs_runtime
def test_simulator_runs_the_modules_and_sees_each_change(qtbot, tmp_path, answers):
    project = Project("incrementale")
    project.add_widget(project.pages[0], "button")
    project.code.module = "import utils\nprint('VALORE', utils.VALUE)\n"
    create_module(project, "utils", "VALUE = 1\n")
    window, path = window_with(qtbot, tmp_path, project)
    window.show()
    seen = []
    window.sim_panel.output.connect(lambda text, _error: seen.append(text))
    for value in (1, 2, 3):
        if value > 1:
            window.open_module("utils")
            type_into_editor(window, f"VALUE = {value}\n")
        assert window.run_project()  # save, generate, compile and start, like F5
        qtbot.waitUntil(lambda: f"VALORE {value}" in "".join(seen), timeout=8000)
        window.stop_simulation()
        qtbot.waitUntil(lambda: not window.sim_panel.running, timeout=5000)
        assert Project.load(path).modules[0].source == f"VALUE = {value}\n"
    # A deleted module does not stay importable from the old build.
    window.project_tree.setCurrentItem(module_item(window, "utils"))
    window.delete_module()
    seen.clear()
    window.run_project()
    qtbot.waitUntil(lambda: "utils" in "".join(seen), timeout=8000)
    assert "ImportError" in "".join(seen) or "no module named" in "".join(seen)
    window.stop_simulation()
    qtbot.waitUntil(lambda: not window.sim_panel.running, timeout=5000)
    close(window)


@needs_runtime
def test_running_and_generating_never_rewrite_the_modules(qtbot, tmp_path, answers):
    project, button, _handler = traceback_project()
    window, path = window_with(qtbot, tmp_path, project)
    original = source(window, "utils")
    window.show()
    assert window.run_project()
    qtbot.waitUntil(lambda: window.sim_panel.running, timeout=5000)
    window.stop_simulation()
    qtbot.waitUntil(lambda: not window.sim_panel.running, timeout=5000)
    generated = window._build_dir() / "utils.py"
    generated.write_text("# modificato a mano nella cartella generata\n", encoding="utf-8")
    assert window.run_project()
    window.stop_simulation()
    qtbot.waitUntil(lambda: not window.sim_panel.running, timeout=5000)
    assert source(window, "utils") == original and Project.load(path).modules[0].source == original
    assert generated.read_text(encoding="utf-8") == original  # the generated folder follows the project
    # Renaming a widget warns about code in modules, without rewriting it.
    create_ui = "import ui\n\ndef boom():\n    ui.%s.set_x(1)\n" % button
    window.open_module("utils")
    type_into_editor(window, create_ui)
    warnings = []
    window.document.execute("Rinomina", lambda project: warnings.extend(project.rename_widget(button, "pulsante")))
    assert any("utils.py" in warning for warning in warnings)
    assert source(window, "utils") == create_ui
    close(window)


def test_projects_without_modules_look_and_save_as_before(qtbot, tmp_path):
    example = ROOT / "examples" / "breakout" / "project.json"
    data = json.loads(example.read_text(encoding="utf-8"))
    path = tmp_path / "progetto.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    original = Project.load(path)
    original.save(path)
    before = path.read_bytes()
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.open_project(path)
    pages = len(window.document.project.pages)
    assert window.project_tree.topLevelItemCount() == pages + 1 and tree_modules(window) == []
    combo = window.code_panel.object_combo
    assert not any(combo.itemData(index)[0] == "pymodule" for index in range(combo.count()))
    window.document.save()
    assert path.read_bytes() == before
    assert json.loads(before)["schemaVersion"] == 2
    close(window)


def test_the_tree_is_translated(qtbot, tmp_path):
    """Without change_language, which would save the language in the real settings of the user."""
    from lvgl_mpy_studio.core.i18n import set_language
    from lvgl_mpy_studio.ui.language import retranslate_widget

    window, _path = window_with(qtbot, tmp_path)
    try:
        set_language("en")
        retranslate_widget(window)
        window.rebuild_project_tree()
        assert modules_node(window).text(0) == "Python Modules"
        assert window.new_module_action.text() == "New Python Module…"
    finally:
        set_language("it")
        retranslate_widget(window)
        window.rebuild_project_tree()
        assert modules_node(window).text(0) == "Moduli Python"
    set_language("en")
    close(window)


TRACE = (
    'Traceback (most recent call last):\n'
    '  File "main.py", line 4, in <module>\n'
    '  File "app_events.py", line 9, in button1_clicked\n'
    '  File "test.py", line 6, in mod1\n'
    "NameError: name 'fff' isn't defined\n"
)


def test_a_traceback_on_stdout_split_in_pieces_still_becomes_rows(qtbot, tmp_path):
    """The simulator writes tracebacks to stdout, and reading can split them: earlier the IDE ignored them."""
    project = Project("pezzi")
    create_module(project, "test", "import ui\n\n\ndef mod1():\n    x = 1\n    fff\n")
    window, _path = window_with(qtbot, tmp_path, project)
    window._sim_output("ciao\n" + TRACE[:70], False)
    assert window.errors.topLevelItemCount() == 0  # half way: wait for the rest
    window._sim_output(TRACE[70:] + "altro output\n", False)
    rows = [window.errors.topLevelItem(index) for index in range(window.errors.topLevelItemCount())]
    assert [(row.text(0), row.text(1)) for row in rows][0] == ("test.py", "6")
    assert rows[0].text(2) == "NameError: name 'fff' isn't defined"
    assert "Traceback" in rows[0].toolTip(2)
    window._sim_output(TRACE, False)  # the same error a second time: lines already seen
    window._error_activated(rows[0])
    assert window.code_panel.module().name == "test" and window.code_panel.editor.textCursor().blockNumber() == 5
    close(window)


@needs_runtime
def test_a_real_run_lists_the_module_error_and_opens_its_line(qtbot, tmp_path):
    project = Project("errore_vero")
    project.add_widget(project.pages[0], "button")
    project.code.module = "import test\n"
    create_module(project, "test", "import ui\n\nX = 1\nfff\n")  # the error comes at import, as soon as the app starts
    window, _path = window_with(qtbot, tmp_path, project)
    window.show()
    assert window.run_project()
    qtbot.waitUntil(lambda: window.errors.topLevelItemCount() > 0, timeout=8000)
    first = window.errors.topLevelItem(0)
    assert (first.text(0), first.text(1)) == ("test.py", "4") and "NameError" in first.text(2)
    errors_dock = window.findChild(QDockWidget, "errorsDock")
    assert not errors_dock.visibleRegion().isEmpty() or errors_dock.isVisible()
    window._error_activated(first)
    assert window.tabs.currentWidget() is window.code_panel
    assert window.code_panel.module().name == "test" and window.code_panel.editor.textCursor().blockNumber() == 3
    window.stop_simulation()
    qtbot.waitUntil(lambda: not window.sim_panel.running, timeout=5000)
    close(window)


def helper_groups(window):
    tree = window.code_panel.helper.tree
    return {tree.topLevelItem(index).text(0): [tree.topLevelItem(index).child(child).text(0) for child in range(tree.topLevelItem(index).childCount())]
            for index in range(tree.topLevelItemCount())}


def test_what_do_you_want_to_do_lists_the_modules_like_components(qtbot, tmp_path, answers):
    project = Project("aiuto")
    button = project.add_widget(project.pages[0], "button")
    create_module(project, "test", "import ui\n\nPREFIX = 'x'\n\n\ndef mod1():\n    pass\n\n\ndef greet(name, times=1):\n    return name\n\n\ndef _private():\n    pass\n\n\nclass Player:\n    pass\n")
    create_module(project, "helpers", "def h():\n    pass\n")
    window, _path = window_with(qtbot, tmp_path, project)
    window.open_handler(button.name)
    groups = helper_groups(window)
    assert groups["Module: test.py"] == ["Import the module", "PREFIX", "mod1()", "greet(name, times)", "Player()"]
    assert groups["Module: helpers.py"] == ["Import the module", "h()"]
    # Double click on a function: the call ends up in the handler.
    type_into_editor(window, "")
    group = next(window.code_panel.helper.tree.topLevelItem(index) for index in range(window.code_panel.helper.tree.topLevelItemCount()) if window.code_panel.helper.tree.topLevelItem(index).text(0) == "Module: test.py")
    window.code_panel.helper._activated(group.child(3))
    assert window.document.project.code.handlers[f"{button.name}_clicked"].body == "test.greet()"
    assert window.code_panel.editor.textCursor().positionInBlock() == len("test.greet(")  # the cursor between the brackets
    # The open module has its own group, expanded: functions are called without the name in front.
    window.open_module("test")
    groups = helper_groups(window)
    assert "Module: test.py" not in groups and "Module: helpers.py" in groups
    assert groups["This module: test.py"] == ["PREFIX", "mod1()", "greet(name, times)", "Player()"]
    tree = window.code_panel.helper.tree
    own = next(tree.topLevelItem(index) for index in range(tree.topLevelItemCount()) if tree.topLevelItem(index).text(0) == "This module: test.py")
    assert own.isExpanded() and own.child(1).data(0, Qt.UserRole) == "mod1()"
    # While typing, the list follows the new functions.
    window.code_panel.editor.moveCursor(QTextCursor.End)
    window.code_panel.editor.insertPlainText("\n\ndef nuova():\n    pass\n")
    qtbot.waitUntil(lambda: "nuova()" in helper_groups(window).get("This module: test.py", []), timeout=3000)
    window.open_handler(button.name)
    assert "nuova()" in helper_groups(window)["Module: test.py"]
    close(window)


@needs_runtime
def test_an_error_while_the_app_keeps_running_shows_its_line_and_offers_to_stop(qtbot, tmp_path):
    """The reported case: the error does not stop the app, so the code stays read-only."""
    project = Project("app_avviata")
    timer = project.add_widget(project.pages[0], "timer", {"period": 100, "enabled": True})
    handler, body = project.ensure_handler(timer.name, "TICK")
    body.body = "import test\ntest.mod1()"
    create_module(project, "test", "import ui\n\n\ndef mod1():\n    x = 1\n    fff\n")
    window, _path = window_with(qtbot, tmp_path, project)
    window.show()
    assert window.run_project()
    qtbot.waitUntil(lambda: window.errors.topLevelItemCount() > 0, timeout=8000)
    assert window.sim_panel.running  # the app is still running
    panel = window.code_panel
    assert panel.editor.isReadOnly() and not panel.running_bar.isHidden()
    first = window.errors.topLevelItem(0)
    assert (first.text(0), first.text(1)) == ("test.py", "6")
    window._error_activated(first)
    # The line shows even when read-only, where the cursor is not drawn.
    assert panel.module().name == "test" and panel.editor.textCursor().blockNumber() == 5
    assert [selection.cursor.blockNumber() for selection in panel.editor.extraSelections()] == [5]
    panel.stop_button.click()
    qtbot.waitUntil(lambda: not window.sim_panel.running, timeout=5000)
    assert not panel.editor.isReadOnly() and panel.running_bar.isHidden()
    assert [selection.cursor.blockNumber() for selection in panel.editor.extraSelections()] == [5]  # stays while typing
    panel.editor.setTextCursor(panel.editor.textCursor())
    panel.editor.insertPlainText("# corretto ")
    assert "# corretto" in source(window, "test")
    close(window)
