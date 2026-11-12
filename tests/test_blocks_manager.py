import json

import pytest
from PySide6.QtWidgets import QMessageBox

from lvgl_mpy_studio.core import blocks, components
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.ui.blocks_manager import BlocksDialog
from lvgl_mpy_studio.ui.designer.scene import Toolbox
from lvgl_mpy_studio.ui.main_window import MainWindow

RELAY = {
    "schemaVersion": 1, "id": "relay", "version": "1.0.0", "name": "Relay", "description": "A relay.", "author": "Someone", "license": "MIT",
    "instances": "many", "properties": [{"name": "pin", "type": "pin", "label": "Pin"}], "methods": [{"name": "close", "arguments": ""}], "events": [],
    "board": [{"file": "board.py"}],
}


def source_folder(tmp_path, name="download", manifest=RELAY):
    folder = tmp_path / name
    folder.mkdir()
    (folder / "block.json").write_text(json.dumps(manifest), encoding="utf-8")
    (folder / "board.py").write_text("class Block:\n    def __init__(self, **options):\n        pass\n\n    def close(self):\n        pass\n", encoding="utf-8")
    (folder / "LICENSE").write_text("MIT, Someone", encoding="utf-8")
    (folder / "secret.txt").write_text("not part of the block", encoding="utf-8")
    return folder


@pytest.fixture
def user_folder(tmp_path, monkeypatch):
    """An empty blocks folder for the test; the registry is put back as it was afterwards."""
    monkeypatch.setattr(blocks, "config_dir", lambda: tmp_path / "config")
    components.reload_blocks()
    yield tmp_path / "config" / "blocks"
    monkeypatch.undo()
    components.reload_blocks()


def names(dialog):
    return [dialog.tree.topLevelItem(row).text(0) for row in range(dialog.tree.topLevelItemCount())]


def select(dialog, name):
    dialog.tree.setCurrentItem(next(dialog.tree.topLevelItem(row) for row in range(dialog.tree.topLevelItemCount()) if dialog.tree.topLevelItem(row).text(0) == name))


def test_install_copies_only_the_block_and_remove_deletes_it(tmp_path, user_folder):
    installed = blocks.install_block(source_folder(tmp_path))
    assert installed.folder == str(user_folder / "relay") and installed.origin == "user"
    assert sorted(path.name for path in (user_folder / "relay").iterdir()) == ["LICENSE", "block.json", "board.py"]
    assert blocks.install_block(source_folder(tmp_path, "newer", {**RELAY, "version": "2.0.0"})).manifest["version"] == "2.0.0"  # replaces the old one
    assert not list(user_folder.glob(".*"))  # nothing left half written
    assert blocks.remove_block("relay") and not (user_folder / "relay").exists()
    assert not blocks.remove_block("relay") and not blocks.remove_block("../config")


def test_manager_lists_adds_and_removes_and_the_toolbox_follows(qtbot, tmp_path, user_folder, monkeypatch):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.blocks_action in [action for menu in window.menuBar().actions() for action in menu.menu().actions()]
    dialog = BlocksDialog(window.document, window)
    qtbot.addWidget(dialog)
    dialog.blocksChanged.connect(window._blocks_changed)
    assert names(dialog) == ["Buzzer", "Digital Input", "Digital Output"]
    assert not dialog.remove_button.isEnabled()  # a block shipped with the IDE cannot be removed
    select(dialog, "Digital Input")
    assert "simulate(value)" in dialog.details.toPlainText() and "its own module" in dialog.details.toPlainText()

    assert dialog.install_folder(str(source_folder(tmp_path)))
    assert names(dialog) == ["Buzzer", "Digital Input", "Digital Output", "Relay"] and dialog.selected().id == "relay"
    assert dialog.remove_button.isEnabled() and "a stand-in" in dialog.details.toPlainText()
    toolbox = window.findChild(Toolbox)
    assert "relay" in [item.toolTip() for item in toolbox.widget_items()]
    window.document.execute("add", lambda project: project.add_widget(project.pages[0], "relay", {"pin": 3}, "k1"))
    window.properties.set_selection(["k1"])
    assert window.properties.definitions["relay"]["properties"][0]["name"] == "pin"

    answers = []
    monkeypatch.setattr(QMessageBox, "warning", lambda *arguments: answers.append(arguments[2]))
    assert not dialog.install_folder(str(tmp_path))  # no block.json there
    assert "not a block that can be used" in answers[-1]
    monkeypatch.setattr(QMessageBox, "question", lambda *arguments: answers.append(arguments[2]) or QMessageBox.No)
    assert not dialog.install_folder(str(source_folder(tmp_path, "again", {**RELAY, "version": "3.0.0"})))
    assert "already there" in answers[-1] and components.BLOCKS["relay"].manifest["version"] == "1.0.0"

    dialog.populate("relay")
    assert dialog.tree.currentItem().text(5) == "k1"
    assert not dialog.remove_selected() and (user_folder / "relay").exists()  # answered No
    monkeypatch.setattr(QMessageBox, "question", lambda *arguments: answers.append(arguments[2]) or QMessageBox.Yes)
    assert dialog.remove_selected()
    assert "keeps working with the copy inside the project" in answers[-1] and not (user_folder / "relay").exists()
    assert components.BLOCKS["relay"].origin == "project"  # the open project still needs it
    select(dialog, "Relay")
    assert dialog.install_button.isEnabled() and not dialog.remove_button.isEnabled()
    assert dialog.install_selected() and components.BLOCKS["relay"].origin == "user" and (user_folder / "relay/board.py").exists()
    window.document.undo_stack.setClean()


def test_a_saved_project_carries_the_block_as_installed_now(tmp_path, user_folder):
    blocks.install_block(source_folder(tmp_path))
    components.reload_blocks()
    project = Project("Carry")
    project.add_widget(project.pages[0], "relay", {"pin": 3}, "k1")
    assert project.to_dict()["assets"]["blocks"]["relay"]["manifest"]["version"] == "1.0.0"
    assert project.to_dict()["assets"]["blocks"]["relay"]["extras"] == {"LICENSE": "MIT, Someone"}
    blocks.install_block(source_folder(tmp_path, "newer", {**RELAY, "version": "2.0.0"}))
    components.reload_blocks()
    assert project.to_dict()["assets"]["blocks"]["relay"]["manifest"]["version"] == "2.0.0"  # the copy follows what generates the code


def test_reload_reports_folders_that_are_not_blocks(qtbot, tmp_path, user_folder):
    (user_folder / "half").mkdir(parents=True)
    (user_folder / "half" / "block.json").write_text("{", encoding="utf-8")
    window = MainWindow()
    qtbot.addWidget(window)
    dialog = BlocksDialog(window.document, window)
    qtbot.addWidget(dialog)
    dialog.reload()
    assert dialog.problems.isVisibleTo(dialog) and "half" in dialog.problems.text() and "not valid JSON" in dialog.problems.text()
    assert names(dialog) == ["Buzzer", "Digital Input", "Digital Output"]
