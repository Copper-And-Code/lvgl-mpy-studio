"""Support code of the components, included only in projects that use them."""

from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.components import is_component

from .output.buzzer import AUDIO_BUZZER, NOTICE, PWM_BUZZER, SILENT_BUZZER, SIMULATOR_BUZZER  # noqa: F401  (the generators import them from here)

BUZZER_MODULE = "lms_buzzer"

def board_buzzer(profile):
    # A project can hold a copy of the profile made before the buzzer existed.
    builtin = next((item for item in builtin_profiles() if item["id"] == profile.get("id")), {})
    buzzer = profile.get("buzzer") or builtin.get("buzzer") or {}
    if buzzer.get("audio"):
        return NOTICE + AUDIO_BUZZER
    if isinstance(buzzer.get("pin"), int):
        return NOTICE + PWM_BUZZER.format(pin=buzzer["pin"])
    return None


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
