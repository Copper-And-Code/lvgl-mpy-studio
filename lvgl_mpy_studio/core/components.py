"""Non-visual components: they are in the project but create no LVGL objects."""

COMPONENTS = {
    "buzzer": {
        "type": "buzzer",
        "name": "Buzzer",
        "icon": "🔔",
        "category": "Components",
        "defaultProps": {},
        "properties": [],
    },
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

BUZZER_METHODS = ("beep", "off", "tone")
TIMER_METHODS = ("delete", "get_paused", "pause", "ready", "reset", "resume", "set_period", "set_repeat_count")


def is_component(widget_type):
    return widget_type in COMPONENTS
