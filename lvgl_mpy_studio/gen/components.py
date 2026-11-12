"""Support code of the components, included only in projects that use them."""

from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.components import block_for, is_component
from lvgl_mpy_studio.core.i18n import tr

BUZZER_MODULE = "lms_buzzer"


def project_components(data):
    return [widget for page in data.get("pages") or [] for widget in page.get("widgets") or [] if is_component(widget.get("type"))]


def project_blocks(data):
    """The blocks the project uses, each once, in the order their first component appears."""
    found = {}
    for widget in project_components(data):
        block = block_for(widget["type"])
        if block is not None:
            found.setdefault(block.id, block)
    return list(found.values())


def has_buzzer(data):
    return any(widget["type"] == "buzzer" for widget in project_components(data))


def ui_imports(data):
    """A block that is a module is imported by ui under the name of each of its components."""
    lines = []
    for widget in project_components(data):
        block = block_for(widget["type"])
        if block is not None and not block.many:
            lines.append(f"import {block.module} as {widget['name']}\n")
    return "".join(lines)


def _effective_profile(profile):
    # A project can hold a copy of the profile made before the buzzer existed.
    builtin = next((item for item in builtin_profiles() if item["id"] == profile.get("id")), {})
    return {**profile, "buzzer": profile.get("buzzer") or builtin.get("buzzer") or {}}


def block_files(data, profile=None):
    """The module of each block in use, as ({file: source}, warnings).

    With a profile the modules are those for that board; without, those for the simulators."""
    files, warnings = {}, []
    for block in project_blocks(data):
        if profile is None:
            source = block.simulator_source() or block.unsimulated_source()
        else:
            source = block.board_source(_effective_profile(profile))
            if source is None:
                source = block.silent_source()
                warnings.append(tr(block.manifest.get("unavailable") or "This board cannot run the block {name}: calls to it will do nothing.", name=block.manifest["name"]))
        files[f"{block.module}.py"] = source
    return files, warnings


def property_values(widget, block):
    """The properties of a component as the keyword arguments of its block, in the order of the block."""
    props = widget.get("props") or {}
    return [(item["name"], props.get(item["name"], item.get("default"))) for item in block.manifest["properties"]]


def block_lines(data, callbacks, exposed):
    """Create the objects of the blocks that are classes, after the UI.

    callbacks: {(component, event): expression}. As for timers, an object nobody uses is not made.
    Each object gets its name, for its messages, then its properties and its handlers."""
    lines, imported = [], set()
    for widget in project_components(data):
        block = block_for(widget["type"])
        if block is None or not block.many:
            continue
        name = widget["name"]
        handlers = [(event, callbacks[(name, event)]) for event in block.events if (name, event) in callbacks]
        if not handlers and exposed is not None and name not in exposed:
            continue
        if block.module not in imported:
            imported.add(block.module)
            lines.append(f"import {block.module}")
        arguments = [f"name={name!r}"] + [f"{key}={value!r}" for key, value in property_values(widget, block)] + [f"on_{event.lower()}={callback}" for event, callback in handlers]
        lines.append(f"ui.{name} = {block.module}.Block({', '.join(arguments)})")
    return lines


def timer_lines(data, callbacks, exposed):
    """Create the timers after the UI: without a handler or a use in code they are not needed."""
    lines = []
    for widget in project_components(data):
        if widget["type"] != "timer":
            continue
        name, props = widget["name"], widget.get("props") or {}
        callback = callbacks.get((name, "TICK"))
        if callback is None and exposed is not None and name not in exposed:
            continue
        lines.append(f"ui.{name} = lv.timer_create({callback or 'lambda _timer: None'}, {int(props.get('period', 1000))}, None)")
        if not props.get("enabled", True):
            lines.append(f"ui.{name}.pause()")
    return lines


def component_lines(data, callbacks, exposed):
    """Blocks first: the handler of a timer may use them at its first tick."""
    return block_lines(data, callbacks, exposed) + timer_lines(data, callbacks, exposed)
