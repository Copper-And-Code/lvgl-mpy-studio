"""Support code of the components, included only in projects that use them."""

from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.components import is_component

from lvgl_mpy_studio.core.blocks import standard_blocks

BUZZER_MODULE = "lms_buzzer"


def buzzer_block():
    return standard_blocks()["buzzer"]


def board_buzzer(profile):
    """The buzzer module for that board, or None when the board has no buzzer."""
    # A project can hold a copy of the profile made before the buzzer existed.
    builtin = next((item for item in builtin_profiles() if item["id"] == profile.get("id")), {})
    return buzzer_block().board_source({**profile, "buzzer": profile.get("buzzer") or builtin.get("buzzer") or {}})


def project_components(data):
    return [widget for page in data.get("pages") or [] for widget in page.get("widgets") or [] if is_component(widget.get("type"))]


def has_buzzer(data):
    return any(widget["type"] == "buzzer" for widget in project_components(data))


def ui_imports(data):
    return "".join(f"import {BUZZER_MODULE} as {widget['name']}\n" for widget in project_components(data) if widget["type"] == "buzzer")


def timer_lines(data, callbacks, exposed):
    """Create the timers after the UI: without a handler or a use in code they are not needed."""
    lines = []
    for widget in project_components(data):
        if widget["type"] != "timer":
            continue
        name, props = widget["name"], widget.get("props") or {}
        callback = callbacks.get(name)
        if callback is None and exposed is not None and name not in exposed:
            continue
        lines.append(f"ui.{name} = lv.timer_create({callback or 'lambda _timer: None'}, {int(props.get('period', 1000))}, None)")
        if not props.get("enabled", True):
            lines.append(f"ui.{name}.pause()")
    return lines
