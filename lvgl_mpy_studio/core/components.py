"""Non-visual components: they are in the project but create no LVGL objects.

The Timer is built in, because it is an lv.timer and not a module. The others are blocks, read
from their folders by core.blocks; for now only those shipped with the IDE."""

from .blocks import standard_blocks

COMPONENTS = {
    **{block.id: block.definition() for block in standard_blocks().values()},
    "timer": {
        "type": "timer",
        "name": "Timer",
        "icon": "⏱️",
        "category": "Components",
        "defaultProps": {"period": 1000, "enabled": True},
        "properties": [
            {"name": "period", "type": "number", "label": "Period (ms)", "min": 1, "max": 3600000},
            {"name": "enabled", "type": "boolean", "label": "Enabled"},
        ],
    },
}

BUZZER_METHODS = tuple(sorted(standard_blocks()["buzzer"].methods))
TIMER_METHODS = ("delete", "get_paused", "pause", "ready", "reset", "resume", "set_period", "set_repeat_count")


def is_component(widget_type):
    return widget_type in COMPONENTS
