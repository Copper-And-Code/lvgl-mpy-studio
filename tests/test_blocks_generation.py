"""Blocks in the generated application: modules, objects, handlers, and the copy inside the project."""

import json
import sys
import types

import pytest

from lvgl_mpy_studio.core import components
from lvgl_mpy_studio.core.blocks import Block
from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.events import EVENTS, events_for
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.core.validation import validate_project
from lvgl_mpy_studio.gen.board_gen import generate_board
from lvgl_mpy_studio.gen.components import block_files
from lvgl_mpy_studio.gen.live import upload_key
from lvgl_mpy_studio.gen.project_gen import generate_project

RELAY = {
    "schemaVersion": 1, "id": "relay", "version": "1.0.0", "name": "Relay", "description": "A relay.", "author": "Someone", "license": "MIT",
    "instances": "many", "properties": [{"name": "pin", "type": "pin", "label": "Pin"}, {"name": "label", "type": "string", "label": "Label", "default": "K1"}],
    "methods": [{"name": "close", "arguments": ""}, {"name": "pulse", "arguments": "ms=100"}], "events": [{"name": "TRIPPED", "help": "The relay opened by itself"}],
    "board": [{"file": "board.py", "when": {"profile": "relay.fitted"}}], "unavailable": "This board has no relay.",
}


@pytest.fixture
def relay():
    """A user block, as if copied into the blocks folder; forgotten again after the test."""
    block = Block(RELAY, {"board.py": "class Block:\n    def __init__(self, **options):\n        self.options = options\n"}, "user")
    components.register(block)
    yield block
    forget("relay")


def forget(block_id):
    components.BLOCKS.pop(block_id, None)
    components.COMPONENTS.pop(block_id, None)


def project():
    result = Project("Blocks")
    page = result.pages[0]
    result.add_widget(page, "digital_output", {"pin": 25}, "led")
    result.add_widget(page, "digital_input", {"pin": 14, "debounce": 50}, "key")
    result.add_widget(page, "digital_output", {"pin": 26, "active_low": True}, "spare")
    result.add_widget(page, "buzzer", None, "buzzer1")
    result.ensure_handler("key", "PRESSED")
    result.code.handlers["key_pressed"].body = "ui.led.toggle()"
    result.ensure_handler("key", "CHANGED")  # left empty: no code is generated for it
    return result


def test_simulator_application_creates_the_objects_of_the_blocks_in_use(tmp_path):
    generated = generate_project(project(), tmp_path)
    assert {"lms_digital_output.py", "lms_digital_input.py", "lms_buzzer.py"} <= set(generated["files"])
    assert {"lms_digital_output", "lms_digital_input", "lms_buzzer"} <= set(generated["modules"])  # the packagers copy what is listed
    main = (tmp_path / "main.py").read_text()
    assert "    import lms_digital_output\n    ui.led = lms_digital_output.Block(name='led', pin=25, active_low=False, initial=False)\n" in main
    assert "    import lms_digital_input\n    ui.key = lms_digital_input.Block(name='key', pin=14, pull='up', active_low=True, debounce=50, on_pressed=app_events.key_pressed)\n" in main
    assert "spare" not in main and main.count("import lms_digital_output") == 1  # no handler and no use in code: not created
    assert "add_event_cb(app_events.key_pressed" not in main  # the event of a block is not an LVGL event
    assert (tmp_path / "ui.py").read_text().endswith("import lms_buzzer as buzzer1\n")
    assert "machine" not in (tmp_path / "lms_digital_output.py").read_text()  # the module of the simulator, not of the board
    for name in generated["files"]:
        if name.endswith(".py"):
            compile((tmp_path / name).read_text(), name, "exec")
    assert generate_project(project(), tmp_path / "all", expose_all=True) and "ui.spare = lms_digital_output.Block(name='spare', pin=26, active_low=True, initial=False)" in (tmp_path / "all/main.py").read_text()


def test_board_application_gets_the_board_modules_precompiled(tmp_path):
    current = project()
    current.board = builtin_profiles()[0]
    current.set_display_size(current.board["logicalWidth"], current.board["logicalHeight"])
    generated = generate_board(current, current.board, tmp_path)
    assert "from machine import Pin" in (tmp_path / "lms_digital_output.py").read_text()
    assert "lv.timer_create(self._poll" in (tmp_path / "lms_digital_input.py").read_text()
    assert {"lms_digital_output.py", "lms_digital_input.py", "lms_buzzer.py"} <= set(generated["precompile"]) <= set(generated["files"])
    main = (tmp_path / "app_main.py").read_text()
    assert "\nimport lms_digital_input\nui.key = lms_digital_input.Block(name='key', pin=14" in main
    assert set(generated["manifest"]["files"]) >= {"lms_digital_output.py", "lms_digital_input.py"}


def test_a_block_property_needs_a_new_upload_and_an_unset_pin_is_reported():
    current = project()
    before = upload_key(current)
    current.find_widget("led").props["pin"] = 27
    assert upload_key(current) != before  # the object is created with its properties: live editing cannot patch it
    assert not [warning for warning in validate_project(current) if "is not set" in warning]
    current.find_widget("key").props.pop("pin")
    assert [warning for warning in validate_project(current) if warning.startswith("key: the property Pin is not set")]


def fake_board(monkeypatch, levels):
    """machine and lvgl as the board modules of the blocks use them; levels is {pin: level}."""
    timers = []

    class Pin:
        IN, OUT, PULL_UP, PULL_DOWN = "in", "out", "up", "down"

        def __init__(self, number, mode, pull=None, value=None):
            self.number, self.mode, self.pull = number, mode, pull
            if value is not None:
                levels[number] = value

        def value(self, level=None):
            if level is None:
                return levels[self.number]
            levels[self.number] = level

    monkeypatch.setitem(sys.modules, "machine", types.SimpleNamespace(Pin=Pin))
    monkeypatch.setitem(sys.modules, "lvgl", types.SimpleNamespace(timer_create=lambda callback, period, data: timers.append((callback, period)) or object()))
    return timers


def load(block_id, target):
    block = components.BLOCKS[block_id]
    namespace = {}
    exec(compile(block.board_source({}) if target == "board" else block.simulator_source(), f"{block.module}.py", "exec"), namespace)
    return namespace["Block"]


def test_digital_output_drives_the_pin_with_its_polarity(monkeypatch):
    levels = {}
    fake_board(monkeypatch, levels)
    output = load("digital_output", "board")
    led = output(name="led", pin=5, active_low=False, initial=True)
    assert levels[5] == 1 and led.value() is True
    led.toggle()
    assert levels[5] == 0 and led.value() is False
    relay = output(name="relay", pin=6, active_low=True)
    assert levels[6] == 1 and relay.value() is False  # off is the high level
    relay.on()
    assert levels[6] == 0 and relay.value() is True
    relay.set(0)
    assert levels[6] == 1
    with pytest.raises(ValueError, match="led: set the Pin property"):
        output(name="led")


def test_digital_input_debounces_and_calls_the_handlers_from_the_lvgl_timer(monkeypatch):
    levels = {7: 1}  # a button to ground with a pull-up: released
    timers = fake_board(monkeypatch, levels)
    calls = []
    key = load("digital_input", "board")(name="key", pin=7, debounce=30, on_changed=lambda block: calls.append(("changed", block.value())), on_pressed=lambda block: calls.append(("pressed", block.value())), on_released=lambda block: calls.append(("released", block.value())))
    (poll, period), = timers
    assert period == 10 and key.value() is False
    levels[7] = 0
    poll(None), poll(None)
    assert calls == []  # 20 ms: still bouncing
    levels[7] = 1
    poll(None)  # the bounce went back: the count starts again
    levels[7] = 0
    poll(None), poll(None)
    assert calls == []
    poll(None)
    assert calls == [("changed", True), ("pressed", True)] and key.value() is True
    levels[7] = 1
    poll(None), poll(None), poll(None)
    assert calls[2:] == [("changed", False), ("released", False)]
    key.simulate(True)
    assert calls[4:] == [("changed", True), ("pressed", True)]
    key.simulate(True)
    assert len(calls) == 6  # the same value again is not a change


def test_the_simulator_modules_behave_like_the_board_ones(capsys):
    led = load("digital_output", "simulator")(name="led", pin=5, initial=False)
    led.on(), led.on(), led.toggle()
    assert capsys.readouterr().out == "led: on\nled: off\n" and led.value() is False
    calls = []
    key = load("digital_input", "simulator")(name="key", on_released=lambda block: calls.append(block.value()))
    key.simulate(True), key.simulate(False)
    assert calls == [False]


def test_a_user_block_travels_inside_the_project(relay, tmp_path):
    current = Project("Carry")
    current.add_widget(current.pages[0], "relay", {"pin": 4}, "k1")
    current.add_widget(current.pages[0], "digital_output", {"pin": 5}, "led")
    assert events_for("relay") == ["TRIPPED"] and "TRIPPED" in EVENTS and "TRIPPED" not in events_for("button")
    data = current.to_dict()
    assert data["schemaVersion"] == 4
    assert set(data["assets"]["blocks"]) == {"relay"}  # the standard ones are in every IDE
    path = tmp_path / "carry.json"
    current.save(path)

    forget("relay")  # a computer without the block
    assert "relay" not in components.COMPONENTS
    opened = Project.load(path)
    assert components.BLOCKS["relay"].origin == "project" and opened.find_widget("k1").props == {"label": "K1", "pin": 4}
    generated = generate_project(opened, tmp_path / "sim", expose_all=True)
    assert "lms_relay.py" in generated["files"]
    assert "ui.k1 = lms_relay.Block(name='k1', pin=4, label='K1')" in (tmp_path / "sim/main.py").read_text()

    opened.remove_widget("k1")
    assert "blocks" not in opened.to_dict()["assets"] and opened.to_dict()["schemaVersion"] == 4  # the Digital Output still needs it
    opened.remove_widget("led")
    assert opened.to_dict()["schemaVersion"] == 2


def test_a_block_without_simulator_or_board_variant_gets_a_stand_in(relay, capsys):
    current = Project("Stand-in")
    current.add_widget(current.pages[0], "relay", {"pin": 4}, "k1")
    files, warnings = block_files(current.to_dict())
    assert warnings == []
    namespace = {}
    exec(files["lms_relay.py"], namespace)
    k1 = namespace["Block"](name="k1", pin=4, label="K1")
    k1.close(), k1.close(), k1.pulse(ms=5)
    assert capsys.readouterr().out == "Relay: close() does nothing in the simulator\nRelay: pulse() does nothing in the simulator\n"
    files, warnings = block_files(current.to_dict(), {"id": "x"})
    assert warnings == ["This board has no relay."] and "pass" in files["lms_relay.py"] and "_tell" not in files["lms_relay.py"]
    files, warnings = block_files(current.to_dict(), {"id": "x", "relay": {"fitted": True}})
    assert warnings == [] and files["lms_relay.py"] == relay.files["board.py"]


def test_a_broken_block_inside_a_project_is_reported_not_fatal(relay):
    current = Project("Broken")
    current.add_widget(current.pages[0], "relay", {"pin": 4}, "k1")
    data = json.loads(json.dumps(current.to_dict()))
    data["assets"]["blocks"]["ghost"] = {"manifest": {"schemaVersion": 1}, "files": {}}
    warnings = validate_project(data)
    assert [warning for warning in warnings if warning.startswith("assets.blocks.ghost:")]
    assert "ghost" not in components.COMPONENTS


def test_blocks_are_a_module_or_a_class_never_both():
    from lvgl_mpy_studio.core.blocks import validate

    errors = validate({**RELAY, "instances": "one"}, {"board.py"})
    assert any("cannot have properties or events" in error for error in errors)
    assert validate(RELAY, {"board.py"}) == []
    assert any("“default” is not a string" in error for error in validate({**RELAY, "properties": [{"name": "label", "type": "string", "label": "Label", "default": 3}]}, {"board.py"}))
    assert any("needs its “options”" in error for error in validate({**RELAY, "properties": [{"name": "mode", "type": "select", "label": "Mode"}]}, {"board.py"}))


def test_what_do_you_want_to_do_offers_the_methods_of_a_block_not_the_lvgl_ones(relay):
    from lvgl_mpy_studio.core.actions import COMMON, actions_for, method_entries

    offered = actions_for("digital_input", "key")
    assert offered == [("True while the input is active.", "ui.key.value()"), ("Behave as if the input had become active (True) or not (False): for the simulator and for tests.", "ui.key.simulate(§)")]
    graphic = {code.format(name="x") for _label, code in COMMON}
    for component in ("digital_input", "digital_output", "buzzer", "timer", "relay"):
        assert not graphic & {code for _label, code in actions_for(component, "x")}, component
    assert [code for _label, code in actions_for("digital_output", "led")] == ["ui.led.on()", "ui.led.off()", "ui.led.toggle()", "ui.led.set(§)", "ui.led.value()"]
    assert actions_for("relay", "k1") == [("close()", "ui.k1.close()"), ("pulse(ms=100)", "ui.k1.pulse(§)")]  # no help written: the call itself
    assert actions_for("buzzer", "b")[0] == ("Beep", "ui.b.beep(§440, 30)")  # the Buzzer keeps its translated texts
    assert [tail for _text, tail in method_entries("digital_output", "led")] == ["on()", "off()", "toggle()", "set(§)", "value()"]
    assert actions_for("label", "l")[-1][1] == "ui.l.set_style_bg_color(lv.color_hex(0x§2196F3), lv.PART.MAIN)"
