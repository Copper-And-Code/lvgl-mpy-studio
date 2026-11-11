import os
import subprocess

import pytest

from lvgl_mpy_studio.core.actions import SCREEN_ACTIONS, COMMON, COMPONENT_ACTIONS, CURSOR, SPECIFIC, actions_for, method_entries, page_actions
from lvgl_mpy_studio.core.i18n import catalog, language, set_language
from lvgl_mpy_studio.core.model import Project, widget_definitions
from lvgl_mpy_studio.gen.gen_python import page_constant
from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.platform import runtime_path


@pytest.mark.skipif(not runtime_path().exists(), reason="native runtime not built")
def test_every_suggested_action_runs_on_the_real_runtime(tmp_path):
    project = Project("azioni")
    project.pages.append(project.new_page("seconda"))
    types = [*widget_definitions(), *COMPONENT_ACTIONS]
    calls = []
    for index, widget_type in enumerate(types):
        name = f"w{index}"
        project.add_widget(project.pages[0], widget_type, name=name)
        calls.extend(code.replace(CURSOR, "") for _label, code in actions_for(widget_type, name))
    calls.extend(code for _label, code in page_actions(page_constant("seconda")))
    calls.extend(code for _label, code in SCREEN_ACTIONS)
    body = []
    for call in calls:
        body += ["try:", f"    {call}", "except Exception as x:", f"    print('RIFIUTATA', {call!r}, x)"]
    project.ensure_handler("main", "SCREEN_LOADED")[1].body = "\n".join(body + ["print('FINE')", "import sys", "sys.exit(0)"]) + "\n"
    generate_project(project, tmp_path)
    environment = dict(os.environ, MICROPYPATH=".", LVSIM_HEADLESS="1", LVSIM_TICK_MS="5")
    process = subprocess.Popen([str(runtime_path()), "main.py"], cwd=tmp_path, env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    lines = []
    try:
        for line in process.stdout:
            lines.append(line)
            if line.startswith("FINE"):
                break
    finally:
        process.kill()
    assert any(line.startswith("FINE") for line in lines), "".join(lines)[-800:]
    assert not [line for line in lines if line.startswith("RIFIUTATA")]


def test_label_offers_text_first():
    assert actions_for("label", "label1")[0] == ("Change text", 'ui.label1.set_text("§")')


def test_button_text_goes_through_its_label():
    assert any("get_child(0).set_text" in code for _label, code in actions_for("button", "b"))


def test_method_entries_keep_description_and_tail():
    entries = dict(method_entries("label", "lab"))
    assert entries["set_text — Change text"] == 'set_text("§")'


def test_every_specific_type_exists():
    assert set(SPECIFIC) <= set(widget_definitions())


def test_every_action_has_an_english_label():
    groups = [COMMON, *SPECIFIC.values(), *COMPONENT_ACTIONS.values()]
    labels = {label for group in groups for label, _code in group} | {page_actions("PAGE_X")[0][0]}
    assert not labels - set(catalog("it"))


def test_suggestions_follow_the_language():
    previous = language()
    set_language("en")
    try:
        assert ("set_text — Change text", 'set_text("§")') in method_entries("label", "lab")
    finally:
        set_language(previous)


def test_helper_panel_is_translated(qtbot):
    from lvgl_mpy_studio.ui.code.editor import ActionHelper
    from lvgl_mpy_studio.ui.document import ProjectDocument

    previous = language()
    set_language("en")
    try:
        document = ProjectDocument()
        document.project.add_widget(document.project.pages[0], "label", name="lab")
        helper = ActionHelper(document)
        qtbot.addWidget(helper)
        helper.rebuild()
        assert helper.title.text() == "What do you want to do?"
        assert helper.tree.topLevelItem(0).child(0).text(0) == "Change text"
    finally:
        set_language(previous)
