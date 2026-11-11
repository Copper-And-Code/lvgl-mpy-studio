from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from lvgl_mpy_studio.ui.code.editor import CodePanel, PythonHighlighter
from lvgl_mpy_studio.ui.document import ProjectDocument


def make_panel(qtbot):
    document = ProjectDocument()
    document.project.add_widget(document.project.pages[0], "button")
    document.project.add_widget(document.project.pages[0], "label")
    panel = CodePanel(document)
    qtbot.addWidget(panel)
    return document, panel


def test_open_handler_edit_and_undo(qtbot):
    document, panel = make_panel(qtbot)
    panel.open_handler("button1")
    assert panel.current == ("handler", "button1_clicked")
    assert panel.signature.text() == "def button1_clicked(e):"
    panel.editor.setPlainText('ui.label1.set_text("Cliccato")')
    assert document.project.code.handlers["button1_clicked"].body == 'ui.label1.set_text("Cliccato")'
    document.undo_stack.undo()
    assert "button1_clicked" not in document.project.code.handlers
    assert panel.current == ("handler", "button1_clicked")
    assert panel.object_combo.currentData() == ("widget", "button1")
    assert panel.editor.toPlainText() == ""
    panel.check_syntax()
    assert panel._errors == []


def test_syntax_error_maps_to_original_line(qtbot):
    document, panel = make_panel(qtbot)
    panel.open_handler("button1")
    panel.editor.setPlainText("x = 1\ndef broken(")
    panel.check_syntax()
    assert any(error.get("handler") == "button1_clicked" and error.get("sourceLine") == 2 for error in panel._errors)


def test_completion_uses_project_and_pinned_api(qtbot):
    document, panel = make_panel(qtbot)
    assert {"button1", "label1"} <= set(panel._completions("ui."))
    assert "set_text" in panel._completions("ui.label1.")
    assert "EVENT" not in panel._completions("lv.")
    assert "obj" in panel._completions("lv.obj")
    assert panel._completions("lv.obj.") == []


def test_auto_indent_and_tabs(qtbot):
    _document, panel = make_panel(qtbot)
    panel.editor.setFocus()
    panel.editor.setPlainText("if True:")
    cursor = panel.editor.textCursor()
    cursor.movePosition(cursor.MoveOperation.End)
    panel.editor.setTextCursor(cursor)
    QTest.keyClick(panel.editor, Qt.Key_Return)
    QTest.keyClick(panel.editor, Qt.Key_A)
    assert panel.editor.toPlainText() == "if True:\n    a"


def test_triple_quoted_string_state(qtbot):
    from PySide6.QtGui import QTextDocument
    document = QTextDocument('"""\nabc\n"""')
    highlighter = PythonHighlighter(document)
    highlighter.rehighlight()
    assert document.findBlockByNumber(0).userState() == 1
    assert document.findBlockByNumber(1).userState() == 1
    assert document.findBlockByNumber(2).userState() == 0


def test_browsing_objects_does_not_touch_project(qtbot):
    document, panel = make_panel(qtbot)
    panel.object_combo.setCurrentIndex(panel._find_object(("widget", "button1")))
    panel.procedure_combo.setCurrentIndex(panel.procedure_combo.findText("PRESSED"))
    assert not document.project.code.handlers
    assert not document.undo_stack.count()
    assert not document.modified


def test_object_combo_selects_default_event(qtbot):
    document, panel = make_panel(qtbot)
    document.execute("Slider", lambda project: project.add_widget(project.pages[0], "slider", name="volume"))
    panel.object_combo.setCurrentIndex(panel._find_object(("widget", "volume")))
    assert panel.procedure_combo.currentText() == "VALUE_CHANGED"
    panel.editor.setPlainText("print(1)")
    assert document.project.code.handlers["volume_value_changed"].body == "print(1)"


def test_completion_offers_stable_page_helpers(qtbot):
    _document, panel = make_panel(qtbot)
    choices = panel._completions("ui.x")
    assert "load_page" in choices
    assert "PAGE_MAIN" in choices


def choices(panel, text):
    return panel._entries(text)


def test_typing_a_widget_name_finds_it_without_knowing_ui(qtbot):
    _document, panel = make_panel(qtbot)
    assert choices(panel, "lab") == [("label1", "ui.label1.")]
    assert choices(panel, "LAB") == [("label1", "ui.label1.")]
    assert choices(panel, "xyz") == []


def test_common_actions_come_first_with_a_description(qtbot):
    _document, panel = make_panel(qtbot)
    entries = choices(panel, "ui.label1.")
    assert entries[0] == ("set_text — Change text", 'set_text("§")')
    assert "cut_text" in entries
    assert len([entry for entry in entries if entry == "set_text"]) == 0


def test_completion_inserts_name_then_call_with_cursor_inside(qtbot):
    _document, panel = make_panel(qtbot)
    editor = panel.editor
    editor.insertPlainText("lab")
    editor.insert_completion("label1")
    assert editor.toPlainText() == "ui.label1."
    editor._insertions = {"set_text — Change text": 'set_text("§")'}
    editor.insert_completion("set_text — Change text")
    assert editor.toPlainText() == 'ui.label1.set_text("")'
    assert editor.textCursor().position() == len('ui.label1.set_text("')


def show_panel(qtbot, panel):
    panel.show()
    qtbot.waitExposed(panel)
    panel.editor.setFocus()


def suggestion_names(editor):
    return [editor.suggestions.item(index).text() for index in range(editor.suggestions.count())]


def test_suggestions_are_a_child_widget_not_a_window(qtbot):
    _document, panel = make_panel(qtbot)
    suggestions = panel.editor.suggestions
    assert not suggestions.isWindow()
    assert suggestions.parentWidget() is panel.editor.viewport()


def test_typing_the_whole_flow_with_the_keyboard(qtbot):
    document, panel = make_panel(qtbot)
    show_panel(qtbot, panel)
    panel.open_handler("button1")
    editor = panel.editor
    qtbot.keyClicks(editor, "lab")
    assert editor.suggestions.isVisible()
    assert suggestion_names(editor) == ["label1"]
    qtbot.keyClick(editor, Qt.Key_Return)
    assert editor.toPlainText() == "ui.label1."
    qtbot.waitUntil(editor.suggestions.isVisible, timeout=1000)
    assert suggestion_names(editor)[0] == "set_text — Change text"
    qtbot.keyClick(editor, Qt.Key_Return)
    qtbot.keyClicks(editor, "Ciao")
    assert document.project.code.handlers["button1_clicked"].body == 'ui.label1.set_text("Ciao")'
    assert not editor.suggestions.isVisible()


def test_suggestion_keys_move_escape_and_tab(qtbot):
    _document, panel = make_panel(qtbot)
    show_panel(qtbot, panel)
    editor = panel.editor
    qtbot.keyClicks(editor, "ui.label1.")
    qtbot.keyClick(editor, Qt.Key_Down)
    assert editor.suggestions.currentRow() == 1
    qtbot.keyClick(editor, Qt.Key_Up)
    assert editor.suggestions.currentRow() == 0
    qtbot.keyClick(editor, Qt.Key_Escape)
    assert not editor.suggestions.isVisible()
    assert editor.toPlainText() == "ui.label1."
    qtbot.keyClicks(editor, "set_st")
    assert all(name.startswith("set_st") for name in suggestion_names(editor))


def test_ctrl_space_lists_objects_on_an_empty_line(qtbot):
    _document, panel = make_panel(qtbot)
    show_panel(qtbot, panel)
    qtbot.keyClick(panel.editor, Qt.Key_Space, Qt.ControlModifier)
    assert {"button1", "label1"} <= set(suggestion_names(panel.editor))


def test_no_suggestions_inside_strings_or_comments(qtbot):
    _document, panel = make_panel(qtbot)
    panel.editor.insertPlainText('x = "label')
    assert not panel.editor.suggestions.isVisible()
    assert panel.editor._inside_text('x = "label')
    assert panel.editor._inside_text("# label")
    assert not panel.editor._inside_text("label")


def test_helper_lists_objects_and_inserts_on_activation(qtbot):
    document, panel = make_panel(qtbot)
    panel.open_handler("button1")
    tree = panel.helper.tree
    groups = {tree.topLevelItem(index).text(0): tree.topLevelItem(index) for index in range(tree.topLevelItemCount())}
    label = groups["label1 (label)"]
    panel.helper._activated(label.child(0))
    assert panel.editor.toPlainText() == 'ui.label1.set_text("")'
    assert document.project.code.handlers["button1_clicked"].body == 'ui.label1.set_text("")'
    panel.helper._activated(label.child(1))
    assert panel.editor.toPlainText() == 'ui.label1.set_text("")\nui.label1.get_text()'


def helper_action(panel):
    tree = panel.helper.tree
    group = next(tree.topLevelItem(index) for index in range(tree.topLevelItemCount()) if tree.topLevelItem(index).text(0) == "label1 (label)")
    group.setExpanded(True)
    return group.child(0)


def test_real_double_click_inserts_the_action_once(qtbot):
    _document, panel = make_panel(qtbot)
    show_panel(qtbot, panel)
    panel.open_handler("button1")
    tree = panel.helper.tree
    position = tree.visualItemRect(helper_action(panel)).center()
    qtbot.mouseClick(tree.viewport(), Qt.LeftButton, pos=position)
    qtbot.mouseDClick(tree.viewport(), Qt.LeftButton, pos=position)
    assert panel.editor.toPlainText() == 'ui.label1.set_text("")'


def test_enter_inserts_the_action_once(qtbot):
    _document, panel = make_panel(qtbot)
    show_panel(qtbot, panel)
    panel.open_handler("button1")
    tree = panel.helper.tree
    tree.setCurrentItem(helper_action(panel))
    tree.setFocus()
    qtbot.keyClick(tree, Qt.Key_Return)
    assert panel.editor.toPlainText() == 'ui.label1.set_text("")'


def test_helper_search_filters_actions(qtbot):
    _document, panel = make_panel(qtbot)
    panel.helper.search.setText("text color")
    tree = panel.helper.tree
    visible = [tree.topLevelItem(index).text(0) for index in range(tree.topLevelItemCount()) if not tree.topLevelItem(index).isHidden()]
    assert visible == ["label1 (label)"]


def test_orphan_handler_remains_editable_through_undo_and_reload(qtbot, tmp_path):
    document, panel = make_panel(qtbot)
    panel.open_handler("button1")
    panel.editor.setPlainText('print("preserved")')
    document.execute("Elimina pulsante", lambda project: project.remove_widget("button1"))
    assert panel.current == ("handler", "button1_clicked")
    assert panel.object_combo.currentData() == ("orphan", "button1_clicked")
    assert panel.editor.toPlainText() == 'print("preserved")'
    assert len(document.project.code.handlers) == 1

    document.undo_stack.undo()
    assert document.project.find_widget("button1")
    assert panel.object_combo.currentData() == ("widget", "button1")
    assert panel.editor.toPlainText() == 'print("preserved")'
    document.undo_stack.redo()
    assert panel.object_combo.currentData() == ("orphan", "button1_clicked")

    panel.editor.setPlainText('print("updated")')
    path = tmp_path / "orphan.json"
    document.save(path)
    document.open(path)
    panel.open_source("button1_clicked")
    assert panel.current == ("handler", "button1_clicked")
    assert panel.object_combo.currentData() == ("orphan", "button1_clicked")
    assert panel.editor.toPlainText() == 'print("updated")'
    assert len(document.project.code.handlers) == 1


def test_monospace_font_has_windows_fallbacks(qtbot):
    _document, panel = make_panel(qtbot)
    assert panel.editor.font().families() == ["Cascadia Mono", "Consolas", "Monospace"]
    assert panel.signature.font().families() == ["Cascadia Mono", "Consolas", "Monospace"]
