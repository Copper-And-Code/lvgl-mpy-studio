import json
from pathlib import Path

LANGUAGES = {"it": "Italiano", "en": "English"}
DEFAULT_LANGUAGE = "en"
_language = DEFAULT_LANGUAGE
_catalogs = {}


def set_language(language):
    global _language
    _language = language if language in LANGUAGES else DEFAULT_LANGUAGE
    return _language


def language():
    return _language


def catalog(language):
    """Texts of the language, from the English of the code: {English text: translation}. English has none."""
    if language not in _catalogs:
        path = Path(__file__).parents[1] / "translations" / f"{language}.json"
        _catalogs[language] = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    return _catalogs[language]


def _sources():
    """From a translated text to the English one: a widget created in Italian is translated again from there."""
    if "sources" not in _catalogs:
        _catalogs["sources"] = {value: source for name in LANGUAGES if name != "en" for source, value in catalog(name).items()}
    return _catalogs["sources"]


def tr(text, **params):
    """The text in the chosen language. Takes the English text of the code or one already translated."""
    # An English text of the code stays itself, also when it equals the translation of another one:
    # "File" is a source, and also the Italian of "Files".
    english = any(text in catalog(name) for name in LANGUAGES if name != "en")
    source = text if english else _sources().get(text, text)
    translated = source if _language == "en" else catalog(_language).get(source, source)
    return translated.format(**params) if params else translated


def device_error_text(code, output=""):
    messages = {
        "device.syntax": "The code contains syntax errors; the active version and launcher were not changed.",
        "device.prerequisites": "The firmware does not meet the profile requirements; check versions, modules, APIs, resolution, and touch.",
        "device.profile.required": "Select a board profile in the project before deploying.",
        "device.resolution": "The project resolution does not match the board profile resolution.",
        "device.timeout": "The device did not respond within the time limit.",
        "device.cancelled": "Device operation cancelled.",
        "device.permissions": "Insufficient permissions to open the serial port.",
        "device.busy": "The serial port is occupied by another process.",
        "device.absent": "The device or mpremote backend is unavailable.",
        "device.live": "Live update failed: press F5 to reload the app.",
        "device.identity.unavailable": "The board does not expose a unique hardware identifier; autostart backup is not allowed.",
        "device.autostart.no-app": "Upload the app to the board before installing autostart.",
        "device.autostart.not-owned": "The current launcher does not match the selected transaction or belongs to another app; no files were changed.",
        "device.autostart.ambiguous": "An IDE launcher exists without a verifiable local transaction; automatic restore is not allowed.",
        "device.autostart.backup": "The previous backup is missing or corrupt; no files were restored.",
        "device.autostart.manifest": "The autostart transaction manifest is missing or invalid.",
        "device.autostart.verify": "Launcher verification after writing failed.",
        "device.transfer.incomplete": "The transfer is incomplete; the previous version was not activated.",
        "device.console": "Unable to start the continuous device console.",
        "device.space": "Not enough free space on the board for these files; none was copied.",
    }
    explanation = tr(messages.get(code, "The device operation failed."))
    detail = f"\n[{code}] {output.strip()}" if output and output.strip() else f"\n[{code}]"
    return explanation + detail
