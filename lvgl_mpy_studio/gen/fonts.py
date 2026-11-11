"""Fonts of the project in the generated code: which ones are used, and their conversion.

A widget names a font of the project in its font property. The generator asks for each font at
each size it is used in, with the characters of the widgets that use it plus printable ASCII, so
text set from code can use at least those. The conversion to LVGL's format needs a rasteriser,
which is Qt: this package stays free of it and calls lvgl_mpy_studio.fontconv only when needed.
"""

import base64

from lvgl_mpy_studio.core.i18n import tr

from .gen_python import build_project_code

_cache = {}
RAM_FACTOR = 2.5  # on a board a font is held as text in the module and as LVGL's own copy: 2.3 times, measured


def _convert(data, size, characters):
    try:
        from lvgl_mpy_studio.fontconv import convert  # Qt: imported only when a project has its own fonts
    except ImportError as exc:
        return {"error": f"fonts cannot be converted without Qt ({exc})"}
    return convert(data, size, characters)


def convert_fonts(data):
    """{key: result} for every font the project data uses, in the form generate_python expects."""
    requests = build_project_code(data)["fontRequests"]
    results = {}
    for request in requests:
        try:
            font = base64.b64decode(str(request["data"]).split(",", 1)[-1], validate=True)
        except ValueError:
            results[request["key"]] = {"error": "the font data in the project is damaged"}
            continue
        cache_key = (request["data"], request["size"], request["characters"])
        if cache_key not in _cache:  # the same font is asked for at every keystroke by the checks of the editor
            if len(_cache) > 32:
                _cache.clear()
            _cache[cache_key] = _convert(font, request["size"], request["characters"])
        results[request["key"]] = _cache[cache_key]
    return results


def font_warnings(data):
    """What went wrong converting the fonts of the project, in words for the user."""
    warnings = []
    for request in build_project_code(data)["fontRequests"]:
        result = convert_fonts(data).get(request["key"]) or {}
        if result.get("error"):
            warnings.append(f"{request['name']} {request['size']} px: {result['error']}; Montserrat is used instead")
        elif result.get("missing"):
            warnings.append(f"{request['name']} {request['size']} px has no glyph for: " + " ".join(f"{char} (U+{ord(char):04X})" for char in result["missing"][:12]))
    return warnings


def font_memory_warning(data, free):
    """A warning if the fonts of the project take more than half the free RAM of the board, else None."""
    need = int(RAM_FACTOR * sum(len(result["output"]) for result in convert_fonts(data).values() if result.get("output")))
    if need and free and need > free // 2:
        return tr("The fonts of the project need about {need} kB of RAM and the board has {free} kB free: use fewer sizes, or the built-in fonts.", need=-(-need // 1000), free=free // 1000)
    return None
