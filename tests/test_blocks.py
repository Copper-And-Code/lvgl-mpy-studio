import copy
import json
from pathlib import Path

import pytest

from lvgl_mpy_studio.core import blocks
from lvgl_mpy_studio.core.blocks import Block, BlockError, discover, load_block, standard_blocks, validate, with_constants
from lvgl_mpy_studio.core.components import BUZZER_METHODS, COMPONENTS

MANIFEST = {
    "schemaVersion": 1, "id": "relay", "version": "1.0.0", "name": "Relay", "description": "A pin driven high or low.", "author": "Someone", "license": "MIT",
    "instances": "many",
    "properties": [{"name": "pin", "type": "pin", "label": "Pin"}, {"name": "active_low", "type": "boolean", "label": "Active low", "default": False}],
    "methods": [{"name": "on", "arguments": ""}, {"name": "set", "arguments": "value, *, force=False"}],
    "events": [{"name": "CHANGED"}],
    "simulator": "simulator.py",
    "board": [{"file": "board.py"}],
}


def folder(tmp_path, manifest=MANIFEST, name="relay", files=("board.py", "simulator.py")):
    directory = tmp_path / name
    directory.mkdir(parents=True)
    (directory / "block.json").write_text(manifest if isinstance(manifest, str) else json.dumps(manifest), encoding="utf-8")
    for file in files:
        (directory / file).write_text(f"# {file}\nVALUE = 1\n", encoding="utf-8")
    return directory


def test_the_buzzer_is_a_block_and_the_components_are_unchanged():
    buzzer = standard_blocks()["buzzer"]
    assert buzzer.origin == "standard" and buzzer.manifest["instances"] == "one"
    assert COMPONENTS["buzzer"] == {"type": "buzzer", "name": "Buzzer", "icon": "🔔", "category": "Components", "defaultProps": {}, "properties": []}
    assert list(COMPONENTS) == ["buzzer", "digital_input", "digital_output", "timer"] and BUZZER_METHODS == ("beep", "off", "tone")
    assert validate(buzzer.manifest, set(buzzer.files)) == []


def test_the_buzzer_module_follows_the_board():
    buzzer = standard_blocks()["buzzer"]
    pwm = buzzer.board_source({"buzzer": {"pin": 7}})
    assert pwm.startswith("# SPDX-License-Identifier: MIT\n# Copyright (c) 2026 Nunzio Raciti\nPIN = 7\n_pwm = None\n") and "PWM(Pin(PIN)" in pwm
    assert "PIN = 0\n" in buzzer.board_source({"buzzer": {"pin": 0}})  # pin 0 is a pin
    assert buzzer.board_source({"buzzer": {"audio": True, "pin": 7}}).endswith("def beep(freq, ms=40):\n    audio.beep(int(freq), ms)\n")
    for profile in ({}, {"buzzer": {}}, {"buzzer": {"pin": "A1"}}, {"buzzer": {"pin": True}}, {"buzzer": {"audio": False}}):
        assert buzzer.board_source(profile) is None, profile
    silent = buzzer.silent_source()
    assert silent.endswith("def tone(freq):\n    pass\n\n\ndef beep(freq, ms=40):\n    pass\n\n\ndef off():\n    pass\n")
    compile(silent, "silent", "exec")
    assert "LVSIM_TONE" in buzzer.simulator_source()


def test_a_block_folder_is_read_without_running_it(tmp_path):
    directory = folder(tmp_path)
    (directory / "board.py").write_text("raise SystemExit('a block must never run inside the IDE')\n", encoding="utf-8")
    (directory / "notes.py").write_text("not named by the manifest", encoding="utf-8")
    block = load_block(directory)
    assert (block.id, block.origin, block.methods) == ("relay", "user", ("on", "set"))
    assert set(block.files) == {"board.py", "simulator.py"}
    assert block.definition() == {"type": "relay", "name": "Relay", "icon": "", "category": "Components", "defaultProps": {"active_low": False}, "properties": [{"name": "pin", "type": "pin", "label": "Pin", "pin": True}, {"name": "active_low", "type": "boolean", "label": "Active low"}]}
    assert block.board_source({}).startswith("raise SystemExit")
    assert block.silent_source().endswith('class Block:\n    def __init__(self, name="", **options):\n        self.name = name\n        self.options = options\n\n    def on(self):\n        pass\n\n    def set(self, value, *, force=False):\n        pass\n')


def changed(**changes):
    manifest = copy.deepcopy(MANIFEST)
    manifest.update(changes)
    return manifest


@pytest.mark.parametrize("manifest, message", [
    ([], "must be an object"),
    (changed(schemaVersion=2), "this IDE reads version 1"),
    (changed(kind="extension"), "only “block” exists"),
    (changed(id="Relay"), "“id” must be lower-case"),
    (changed(id="../relay"), "“id” must be lower-case"),
    (changed(name=""), "“name” must be a text"),
    (changed(instances="two"), "“instances” must be"),
    (changed(properties={}), "“properties” must be a list"),
    (changed(properties=[{"name": "my pin", "type": "pin", "label": "Pin"}]), "properties[0]: “name” must be a Python name"),
    (changed(properties=[{"name": "pin", "type": "wire", "label": "Pin"}]), "properties[0]: “type” must be one of"),
    (changed(properties=[{"name": "pin", "type": "pin", "label": "Pin"}] * 2), "the name “pin” is used twice"),
    (changed(methods=[{"name": "_hidden"}]), "methods[0]: “name” must be a public Python name"),
    (changed(methods=[{"name": "on", "arguments": "value,, other"}]), "“arguments” is not a Python argument list"),
    (changed(methods=[{"name": "on", "arguments": "): import os\ndef x("}]), "“arguments” is not a Python argument list"),
    (changed(methods=[{"name": "on", "arguments": "): pass; import os; (lambda"}]), "“arguments” is not a Python argument list"),
    (changed(methods=[{"name": "on", "arguments": 3}]), "“arguments” is not a Python argument list"),
    (changed(events=[{"name": "changed"}]), "events[0]: “name” must be upper-case"),
    (changed(simulator="../simulator.py"), "simulator: a module is a file name"),
    (changed(simulator="other.py"), "simulator: the file other.py is missing"),
    (changed(board=[{"file": "sub/board.py"}]), "board[0]: a module is a file name"),
    (changed(board=[{"file": "board.py", "when": "buzzer"}]), "“when” must name a “profile” value"),
    (changed(board=[{"file": "board.py", "constants": {"pin": {"profile": "a.b"}}}]), "the constant “pin” must be upper-case"),
    (changed(board=[{"file": "board.py", "constants": {"PIN": {"profile": "a.b", "type": "list"}}}]), "the constant “PIN” must be upper-case"),
])
def test_a_wrong_block_says_what_is_wrong(manifest, message):
    errors = validate(manifest, {"board.py", "simulator.py"})
    assert errors and any(message in error for error in errors), errors


def test_a_valid_block_has_nothing_to_report():
    assert validate(MANIFEST, {"board.py", "simulator.py"}) == []


def test_broken_folders_are_reported_and_the_others_still_load(tmp_path):
    folder(tmp_path)
    folder(tmp_path, "{ not json", name="broken")
    folder(tmp_path, changed(id="renamed"), name="mismatch")
    folder(tmp_path, changed(id="incomplete"), name="incomplete", files=("board.py",))
    (tmp_path / "empty").mkdir()
    (tmp_path / ".hidden").mkdir()
    (tmp_path / "readme.txt").write_text("not a block", encoding="utf-8")
    found, problems = discover(tmp_path)
    assert list(found) == ["relay"]
    messages = {name.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]: message for name, message in problems}
    assert set(messages) == {"broken", "mismatch", "incomplete", "empty"}
    assert "not valid JSON" in messages["broken"] and "they must be the same" in messages["mismatch"]
    assert "simulator.py is missing" in messages["incomplete"] and "cannot be read" in messages["empty"]
    assert discover(tmp_path / "nowhere") == ({}, [])
    with pytest.raises(BlockError, match="not valid JSON"):
        load_block(tmp_path / "broken")


def test_user_blocks_live_next_to_the_board_profiles(tmp_path, monkeypatch):
    monkeypatch.setattr(blocks, "config_dir", lambda: tmp_path)
    assert blocks.user_dir() == tmp_path / "blocks"
    assert blocks.user_blocks() == ({}, [])  # the folder need not exist
    folder(tmp_path / "blocks")
    found, problems = blocks.user_blocks()
    assert list(found) == ["relay"] and found["relay"].origin == "user" and problems == []
    assert "relay" not in COMPONENTS  # read when the IDE starts, or when asked


def test_constants_go_after_the_leading_comments():
    assert with_constants("# a\n# b\nimport x\n", {"PIN": 3, "NAME": "led"}) == "# a\n# b\nPIN = 3\nNAME = 'led'\nimport x\n"
    assert with_constants("import x\n", {"PIN": 3}) == "PIN = 3\nimport x\n"
    assert with_constants("# only\n", {}) == "# only\n"
    block = Block({**MANIFEST, "board": [{"file": "board.py", "constants": {"RATE": {"profile": "uart.rate", "type": "number"}}}]}, {"board.py": "x = RATE\n"})
    assert block.board_source({"uart": {"rate": 9600}}) == "RATE = 9600\nx = RATE\n"
    assert block.board_source({"uart": {"rate": "fast"}}) is None and block.board_source({}) is None


def test_standard_blocks_have_italian_texts():
    """The texts of a block are shown through tr(): those of the blocks shipped with the IDE are translated."""
    catalog = json.loads(Path("lvgl_mpy_studio/translations/it.json").read_text(encoding="utf-8"))
    missing = []
    for block in standard_blocks().values():
        manifest = block.manifest
        texts = [manifest["name"], manifest["description"], *(item["label"] for item in manifest["properties"])]
        texts += [item["help"] for item in manifest["methods"]] + [item["help"] for item in manifest["events"]]
        missing += [f"{block.id}: {text}" for text in texts if text not in catalog and text != "Buzzer"]
    assert not missing


def test_the_example_of_the_guide_is_a_block_that_installs_and_generates(tmp_path, monkeypatch):
    from lvgl_mpy_studio.core import components
    from lvgl_mpy_studio.core.model import Project
    from lvgl_mpy_studio.gen.project_gen import generate_project

    monkeypatch.setattr(blocks, "config_dir", lambda: tmp_path / "config")
    installed = blocks.install_block("examples/blocks/blinker")
    assert sorted(path.name for path in (tmp_path / "config/blocks/blinker").iterdir()) == ["LICENSE", "README.md", "block.json", "board.py", "simulator.py"]
    components.register(installed)
    try:
        project = Project("Guide")
        project.add_widget(project.pages[0], "blinker", {"pin": 25}, "blinker1")
        project.ensure_handler("blinker1", "BLINKED")
        project.code.handlers["blinker1_blinked"].body = "print(e.is_running())"
        generate_project(project, tmp_path / "app")
        assert "ui.blinker1 = lms_blinker.Block(name='blinker1', pin=25, period=500, running=True, on_blinked=app_events.blinker1_blinked)" in (tmp_path / "app/main.py").read_text()
        guide = Path("docs/blocks.md").read_text(encoding="utf-8")
        assert "ui.blinker1 = lms_blinker.Block(name='blinker1', pin=25, period=500, running=True, on_blinked=app_events.blinker1_blinked)" in guide
        shown = json.loads(guide.split("```json\n", 1)[1].split("```", 1)[0])
        shipped = dict(installed.manifest, author=shown["author"])
        shipped.pop("kind")
        for item in shipped["properties"]:
            item.pop("role", None)
        assert shown == shipped  # the guide shows the example as it is
    finally:
        components.reload_blocks()
