import copy
import functools
import json
import os
from pathlib import Path
import tempfile
from uuid import uuid4

from lvgl_mpy_studio.platform import config_dir

ADAPTERS = {
    "waveshare_rgbpanel": {
        "colorFormats": {"RGB565"},
        "modules": ["lvgl", "display_driver", "rgbpanel", "gt911"],
        "eventLoop": "driver",
    },
    "stm32h7_uart": {
        "colorFormats": {"RGB565"},
        "modules": ["lvgl", "display_driver", "gt911", "st_ltdc"],
        "eventLoop": "driver",
    },
    "esp32_4848s040": {
        "colorFormats": {"RGB565"},
        "modules": ["lvgl", "display_driver", "gt911"],
        "eventLoop": "driver",
    },
}


@functools.lru_cache(maxsize=None)
def _builtin_profiles():
    directory = Path(__file__).parents[1] / "boards"
    profiles = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(directory.glob("*.json"))]
    return tuple(sorted(profiles, key=lambda profile: profile["id"] != "waveshare_rp2350_touch_lcd_4_240"))


def builtin_profiles():
    """A copy: whoever gets it can change it without touching the built-in profiles."""
    return copy.deepcopy(list(_builtin_profiles()))


SIMULATOR_FONTS = (14, 16, 24, 32, 40)  # Montserrat sizes of the pinned simulator runtime (runtime/lv_conf.h)
DEFAULT_BOARD_FONTS = (14, 16, 24)      # what a profile without a fonts list is taken to have


def profile_fonts(profile):
    """Montserrat sizes to draw with: those of the board profile, or of the simulator without a board.

    Text asked in a size the target lacks is drawn in the nearest one, so designer, simulator and
    generated code must agree on this list.
    """
    if not profile:
        return list(SIMULATOR_FONTS)
    fonts = profile.get("fonts")
    return sorted(fonts) if _valid_fonts(fonts) else list(DEFAULT_BOARD_FONTS)


def _valid_fonts(fonts):
    return isinstance(fonts, list) and bool(fonts) and all(isinstance(size, int) and not isinstance(size, bool) and 4 <= size <= 200 for size in fonts)


def portable_profile(profile):
    """A copy of the profile as a project or a board session keeps it: without origin, which only the catalog uses."""
    if profile is None:
        return None
    result = copy.deepcopy(profile)
    result.pop("origin", None)
    return result


def profile_diagnostics(profile):
    errors = []
    if not isinstance(profile, dict):
        return [{"code": "profile.object", "path": "", "params": {}}]
    for field in ("id", "name", "adapter", "colorFormat"):
        if not isinstance(profile.get(field), str) or not profile[field]:
            errors.append({"code": "profile.required", "path": field, "params": {}})
    if profile.get("schemaVersion") != 1:
        errors.append({"code": "profile.schema", "path": "schemaVersion", "params": {}})
    if not isinstance(profile.get("revision"), int) or isinstance(profile.get("revision"), bool) or profile.get("revision", 0) < 1:
        errors.append({"code": "profile.revision", "path": "revision", "params": {}})
    if profile.get("adapter") not in ADAPTERS:
        errors.append({"code": "profile.adapter", "path": "adapter", "params": {"adapter": str(profile.get("adapter"))}})
    for field in ("physicalWidth", "physicalHeight", "logicalWidth", "logicalHeight", "scale"):
        value = profile.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < 1 or value > 10000:
            errors.append({"code": "profile.dimension", "path": field, "params": {}})
    if profile.get("colorFormat") != "RGB565":
        errors.append({"code": "profile.color", "path": "colorFormat", "params": {}})
    if profile.get("orientations") != [0]:
        errors.append({"code": "profile.orientation", "path": "orientations", "params": {}})
    firmware = profile.get("firmware")
    if not isinstance(firmware, dict) or not isinstance(firmware.get("modules"), list) or not all(isinstance(name, str) and name for name in firmware.get("modules", [])):
        errors.append({"code": "profile.firmware", "path": "firmware.modules", "params": {}})
    if "fonts" in profile and not _valid_fonts(profile["fonts"]):
        errors.append({"code": "profile.fonts", "path": "fonts", "params": {}})
    config = profile.get("config")
    if not isinstance(config, dict) or config.get("driver") != "display_driver" or config.get("eventLoop") != "driver" or config.get("buffers") != "driver":
        errors.append({"code": "profile.driver", "path": "config", "params": {}})
    dimensions = [profile.get(field) for field in ("physicalWidth", "physicalHeight", "logicalWidth", "logicalHeight", "scale")]
    if all(isinstance(value, int) and not isinstance(value, bool) and value > 0 for value in dimensions):
        physical_width, physical_height, logical_width, logical_height, scale = dimensions
        if (physical_width, physical_height) != (logical_width * scale, logical_height * scale):
            errors.append({"code": "profile.scale", "path": "scale", "params": {}})
    return errors


def validate_profile(profile):
    errors = profile_diagnostics(profile)
    if errors:
        raise ValueError("; ".join(f"{item['code']}:{item['path']}" for item in errors))
    return profile


class ProfileStore:
    def __init__(self, path=None):
        self.path = Path(path) if path else config_dir() / "board-profiles.json"
        self.custom = {}
        self.hidden = []
        self.load_error = None
        if self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if data.get("schemaVersion") != 1:
                raise ValueError("profile.store.schema")
            self.custom = data.get("custom") or {}
            self.hidden = data.get("hidden") or []
        for profile in self.custom.values():
            validate_profile(profile)

    @classmethod
    def tolerant(cls, path=None):
        """The catalog, even if the file of custom profiles is broken: the built-in profiles remain.

        load_error says what is wrong; while it is set, save refuses to overwrite the file, which
        can still be repaired by hand.
        """
        try:
            return cls(path)
        except (OSError, ValueError, AttributeError, TypeError) as exc:
            store = cls.__new__(cls)
            store.path = Path(path) if path else config_dir() / "board-profiles.json"
            store.custom, store.hidden, store.load_error = {}, [], f"{store.path}: {exc}"
            return store

    def snapshot(self):
        return copy.deepcopy({"custom": self.custom, "hidden": self.hidden})

    def restore(self, snapshot):
        self.custom = copy.deepcopy(snapshot["custom"])
        self.hidden = list(snapshot["hidden"])

    def profiles(self):
        result = []
        for profile in builtin_profiles():
            if profile["id"] in self.hidden:
                continue
            selected = self.custom.get(profile["id"], profile)
            result.append({**copy.deepcopy(selected), "origin": "custom" if profile["id"] in self.custom else "builtin"})
        builtin_ids = {profile["id"] for profile in builtin_profiles()}
        result.extend({**copy.deepcopy(profile), "origin": "custom"} for profile_id, profile in self.custom.items() if profile_id not in builtin_ids)
        return result

    def get(self, profile_id):
        return next((profile for profile in self.profiles() if profile["id"] == profile_id), None)

    def save_profile(self, profile):
        validate_profile(profile)
        profile = portable_profile(profile)
        self.custom[profile["id"]] = profile
        self.hidden = [item for item in self.hidden if item != profile["id"]]
        return profile

    def new_profile(self, source=None):
        profile = portable_profile(source or builtin_profiles()[0])
        profile["id"] = f"custom_{uuid4().hex}"
        profile["revision"] = 1
        profile["name"] = f"{profile['name']} custom"
        return profile

    def delete(self, profile_id):
        builtin_ids = {profile["id"] for profile in builtin_profiles()}
        if profile_id in builtin_ids:
            if profile_id not in self.hidden:
                self.hidden.append(profile_id)
            self.custom.pop(profile_id, None)
        else:
            self.custom.pop(profile_id, None)

    def restore_default(self, profile_id):
        self.custom.pop(profile_id, None)
        self.hidden = [item for item in self.hidden if item != profile_id]

    def restore_hidden(self):
        self.hidden = []

    def save(self):
        if self.load_error:
            raise OSError(f"profile.store.unreadable: {self.load_error}")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps({"schemaVersion": 1, "custom": self.custom, "hidden": self.hidden}, ensure_ascii=False, indent=2) + "\n"
        temporary = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", dir=self.path.parent, prefix=".board-profiles.", suffix=".tmp", delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
        except Exception:
            if temporary:
                temporary.unlink(missing_ok=True)
            raise


def compatible(project, profile):
    validate_profile(profile)
    return project.display.width == profile["logicalWidth"] and project.display.height == profile["logicalHeight"]
