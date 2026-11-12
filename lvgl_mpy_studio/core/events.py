from dataclasses import dataclass


@dataclass(frozen=True)
class EventDefinition:
    name: str
    description: str


EVENTS = {
    item.name: item
    for item in [
        EventDefinition("CLICKED", "Widget activated by a click"),
        EventDefinition("VALUE_CHANGED", "Widget value changed"),
        EventDefinition("PRESSED", "Pointer pressed on the widget"),
        EventDefinition("RELEASED", "Pointer released"),
        EventDefinition("LONG_PRESSED", "Long press"),
        EventDefinition("FOCUSED", "Widget received focus"),
        EventDefinition("DEFOCUSED", "Widget lost focus"),
        EventDefinition("READY", "Operation completed"),
        EventDefinition("CANCEL", "Operation cancelled"),
        EventDefinition("SCREEN_LOADED", "Page loaded and displayed"),
        EventDefinition("GESTURE", "Gesture recognized"),
        EventDefinition("TICK", "Timer interval elapsed"),
    ]
}

DEFAULT_EVENTS = {
    "button": "CLICKED", "imagebutton": "CLICKED", "slider": "VALUE_CHANGED",
    "switch": "VALUE_CHANGED", "checkbox": "VALUE_CHANGED", "dropdown": "VALUE_CHANGED",
    "roller": "VALUE_CHANGED", "arc": "VALUE_CHANGED", "textarea": "VALUE_CHANGED",
    "page": "SCREEN_LOADED", "timer": "TICK",
}

PAGE_EVENTS = ("SCREEN_LOADED",)  # the events a page offers in the editor
COMPONENT_EVENTS = {"buzzer": (), "timer": ("TICK",)}


COMPONENT_ONLY = {"TICK"}  # events no LVGL widget has


def register_component_events(component_type, events):
    """The events of a block: events is a list of (name, description)."""
    COMPONENT_EVENTS[component_type] = tuple(name for name, _description in events)
    for name, description in events:
        if name not in EVENTS:
            EVENTS[name] = EventDefinition(name, description)
            COMPONENT_ONLY.add(name)
    if events:
        DEFAULT_EVENTS[component_type] = events[0][0]


def events_for(widget_type):
    if widget_type in COMPONENT_EVENTS:
        return list(COMPONENT_EVENTS[widget_type])
    return [name for name in EVENTS if name not in COMPONENT_ONLY]


def default_event(widget_type):
    return DEFAULT_EVENTS.get(widget_type, "CLICKED")


def handler_name(object_name, event):
    return f"{object_name}_{event.lower()}"
