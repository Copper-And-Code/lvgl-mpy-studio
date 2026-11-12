"""Non-visual components: they are in the project but create no LVGL objects.

The Timer is built in, because it is an lv.timer and not a module. The others are blocks, read
from their folders by core.blocks: those shipped with the IDE, those the user copied into the
blocks folder, and those a project carries with it."""

from .blocks import Block, BlockError, standard_blocks, user_blocks
from .events import register_component_events

TIMER = {
    "type": "timer",
    "name": "Timer",
    "icon": "⏱️",
    "category": "Components",
    "defaultProps": {"period": 1000, "enabled": True},
    "properties": [
        {"name": "period", "type": "number", "label": "Period (ms)", "min": 1, "max": 3600000},
        {"name": "enabled", "type": "boolean", "label": "Enabled"},
    ],
}

COMPONENTS = {}  # type -> definition, as the toolbox and the Properties panel read it
BLOCKS = {}  # type -> Block, for the components that are blocks
PROBLEMS = []  # (folder, message) of the user blocks that could not be read

TIMER_METHODS = ("delete", "get_paused", "pause", "ready", "reset", "resume", "set_period", "set_repeat_count")


def register(block):
    BLOCKS[block.id] = block
    COMPONENTS[block.id] = block.definition()
    register_component_events(block.id, [(event["name"], event.get("help", "")) for event in block.manifest["events"]])


def reload_blocks():
    """Read the blocks again: the standard ones, then the user's, which replace a standard one with the same id."""
    timer = COMPONENTS.get("timer", TIMER)
    COMPONENTS.clear()
    BLOCKS.clear()
    found, problems = user_blocks()
    PROBLEMS[:] = problems
    standard = standard_blocks()
    for block in standard.values():
        register(block)
    COMPONENTS["timer"] = timer  # after the Buzzer, where it has always been in the toolbox
    for block in found.values():
        if block.id == "timer":
            PROBLEMS.append((block.id, "“timer” is the name of the built-in Timer"))
            continue
        if block.id in standard:
            PROBLEMS.append((block.id, f"replaces the block “{block.id}” shipped with the IDE"))
        register(block)


def register_project_blocks(data):
    """Make known the blocks a project carries and this IDE lacks; return what could not be read."""
    problems = []
    stored = (data.get("assets") or {}).get("blocks") if isinstance(data, dict) else None
    for block_id, entry in (stored.items() if isinstance(stored, dict) else ()):
        if block_id in BLOCKS:
            continue  # the installed one is used; updating the copy of the project comes with the IDE commands
        try:
            block = Block.from_dict(entry)
            if block.id != block_id:
                raise BlockError(f"it is stored as {block_id} and its id is {block.id}")
            register(block)
        except BlockError as exc:
            problems.append((block_id, str(exc)))
    return problems


def block_for(component_type):
    """The block behind a component type, or None for the Timer and for LVGL widgets."""
    return BLOCKS.get(component_type)


def methods_for(component_type):
    """The methods the code can call on a component, sorted, for completion."""
    if component_type == "timer":
        return TIMER_METHODS
    block = BLOCKS.get(component_type)
    return tuple(sorted(block.methods)) if block else ()


def is_component(widget_type):
    return widget_type in COMPONENTS


reload_blocks()
BUZZER_METHODS = methods_for("buzzer")
