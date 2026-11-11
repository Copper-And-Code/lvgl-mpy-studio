import keyword
import re

from lvgl_mpy_studio.gen.identifiers import C_KEYWORDS, PYTHON_BUILTINS, TEMPLATE_NAMES

IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
RESERVED = C_KEYWORDS | PYTHON_BUILTINS | TEMPLATE_NAMES | set(keyword.kwlist)
RESERVED.update(("ui", "lv", "main", "app_events", "display_driver", "time", "self", "cls"))


def validate_name(name, existing=()):
    if not isinstance(name, str) or not IDENTIFIER_RE.fullmatch(name):
        return "The name must match [A-Za-z_][A-Za-z0-9_]*"
    if keyword.iskeyword(name) or name in C_KEYWORDS or name in RESERVED:
        return f"The name {name!r} is reserved"
    if name.startswith(("lv_", "LV_")):
        return "The lv_/LV_ prefix is reserved for LVGL"
    if name in set(existing):
        return f"The name {name!r} is already used"
    return None


def allocate_name(widget_type, existing):
    used = set(existing)
    base = re.sub(r"[^A-Za-z0-9_]", "_", widget_type).strip("_") or "widget"
    if base[0].isdigit() or validate_name(base):
        base = "widget"
    number = 1
    while f"{base}{number}" in used or validate_name(f"{base}{number}"):
        number += 1
    return f"{base}{number}"
