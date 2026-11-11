import math
import re

C_FONT_SIZES = [14, 16, 24, 32, 40]
MICROPYTHON_FONT_SIZES = [14, 16, 24]


def js_round(value):
    return math.floor(value + 0.5)


def to_int(value, fallback=0):
    if isinstance(value, str) and value.strip():
        try:
            value = float(value)
        except ValueError:
            return fallback
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        return fallback
    return js_round(value)


def parse_color(value):
    match = re.fullmatch(r"#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", str(value or "").strip())
    if not match:
        return None
    digits = match.group(1)
    if len(digits) == 3:
        digits = "".join(char * 2 for char in digits)
    return int(digits, 16)


def nearest_font_size(size, available):
    wanted = to_int(size, 14)
    best = available[0]
    for current in available[1:]:
        if abs(current - wanted) < abs(best - wanted):
            best = current
    return best


ANIM_PATHS = ["linear", "ease_in", "ease_out", "ease_in_out", "overshoot", "bounce", "step"]


class Values:
    @staticmethod
    def int(value, fallback=0):
        return {"k": "int", "value": to_int(value, fallback)}

    @staticmethod
    def str(value):
        return {"k": "str", "value": "" if value is None else str(value)}

    @staticmethod
    def bool(value):
        return {"k": "bool", "value": bool(value)}

    @staticmethod
    def color(value):
        color = parse_color(value)
        return None if color is None else {"k": "color", "value": color}

    @staticmethod
    def enum(enum_name, member):
        return {"k": "enum", "enumName": enum_name, "member": member}

    @staticmethod
    def sel(part="MAIN", state=None):
        return {"k": "sel", "part": part, "state": state}

    @staticmethod
    def font(size, symbol=None):
        return {"k": "font", "size": to_int(size, 14), "symbol": symbol}

    @staticmethod
    def ref(name):
        return {"k": "ref", "name": name}

    @staticmethod
    def null():
        return {"k": "null"}

    @staticmethod
    def pct(value):
        return {"k": "pct", "value": to_int(value, 100)}

    @staticmethod
    def constant(name):
        return {"k": "constant", "name": name}

    @staticmethod
    def anim_enable(on):
        return {"k": "animEnable", "value": bool(on)}

    @staticmethod
    def anim_path(path):
        name = re.sub(r"^lv_anim_path_", "", str(path or ""))
        return {"k": "animPath", "name": name if name in ANIM_PATHS else "linear"}

    @staticmethod
    def image(source, symbol=None):
        return {"k": "image", "source": str(source or ""), "symbol": symbol}


v = Values()


def enum_member(value, enum_name, members):
    if value is None:
        return None
    raw = str(value).strip()
    prefix = f"LV_{enum_name}_"
    member = raw[len(prefix):] if raw.startswith(prefix) else raw.upper()
    return member if member in members else None


def has(value):
    return value is not None and value != ""
