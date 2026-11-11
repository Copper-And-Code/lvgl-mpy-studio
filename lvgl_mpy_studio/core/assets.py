"""Images and fonts of a project, kept inside the project file and used by widgets by name.

Images are PNG files shown by image widgets; fonts are TrueType or OpenType files that any widget
with text can name in its font property, converted to LVGL's format when the code is generated.

The project stays a single file, and an image goes wherever the project goes: simulator, board,
executables, browser and C export, embedded in the generated code. The price is memory on the
board: the PNG bytes, and the decoded picture while it is on screen. Hence the limits here.
"""

import base64
import re

from .i18n import tr

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_IMAGE_BYTES = 512 * 1024   # a larger file is refused: it would not fit a microcontroller anyway
LARGE_IMAGE_BYTES = 64 * 1024  # from here a warning says what it costs
IMAGE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,59}\.png")


MAX_FONT_BYTES = 2 * 1024 * 1024
FONT_SIGNATURES = (b"\x00\x01\x00\x00", b"OTTO", b"true", b"ttcf")
FONT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,59}\.(?:ttf|otf)")
BUILTIN_FONT = re.compile(r"(?:lv_font_)?montserrat_\d+")  # the names the font property offers for the built-in font


class AssetError(ValueError):
    pass


def font_name(name):
    """A file name fit for a font asset, keeping .ttf or .otf."""
    base = str(name).replace("\\", "/").rsplit("/", 1)[-1]
    ending = ".otf" if base.lower().endswith(".otf") else ".ttf"
    stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", re.sub(r"\.[A-Za-z0-9]+$", "", base)).strip("._-") or "font"
    return stem[:56] + ending


def _font_entries(project):
    fonts = project.assets.get("fonts") if isinstance(project.assets, dict) else None
    return fonts if isinstance(fonts, list) else []


def fonts(project):
    """The fonts of the project: [{"name", "bytes"}], in project order."""
    return [{"name": entry.get("name"), "bytes": len(entry["data"].split(",", 1)[-1]) * 3 // 4} for entry in _font_entries(project) if isinstance(entry, dict) and isinstance(entry.get("data"), str)]


def add_font(project, name, data, replace=False):
    """Add a TrueType or OpenType file to the project under name; return the name used."""
    if not isinstance(data, (bytes, bytearray)) or bytes(data[:4]) not in FONT_SIGNATURES:
        raise AssetError(tr("only TrueType and OpenType fonts (.ttf, .otf) can be added"))
    if len(data) > MAX_FONT_BYTES:
        raise AssetError(tr("the font file is {size} kB: the limit is {limit} kB", size=len(data) // 1024, limit=MAX_FONT_BYTES // 1024))
    name = font_name(name)
    entries = [entry for entry in _font_entries(project) if isinstance(entry, dict)]
    existing = next((entry for entry in entries if entry.get("name") == name), None)
    if existing is not None and not replace:
        raise AssetError(tr("{name}: a font with this name already exists", name=name))
    entry = {"name": name, "data": "data:font/ttf;base64," + base64.b64encode(bytes(data)).decode("ascii")}
    if existing is not None:
        entries[entries.index(existing)] = entry
    else:
        entries.append(entry)
    project.assets = {**(project.assets if isinstance(project.assets, dict) else {}), "fonts": entries}
    return name


def remove_font(project, name):
    """Remove the font; return the names of the widgets that still ask for it."""
    entries = _font_entries(project)
    if not any(isinstance(entry, dict) and entry.get("name") == name for entry in entries):
        raise AssetError(tr("no such font: {name}", name=name))
    project.assets = {**project.assets, "fonts": [entry for entry in entries if not (isinstance(entry, dict) and entry.get("name") == name)]}
    return [widget.name for widget in project.widgets if widget.props.get("font") == name]


def uses_project_font(project, widget):
    """Whether the widget draws its text with a font of the project, not with the built-in one."""
    return widget.props.get("font") in {entry.get("name") for entry in _font_entries(project) if isinstance(entry, dict)}


def font_warnings(project):
    """Widgets that ask for a font the project does not have: they are drawn with the built-in one."""
    known = {entry.get("name") for entry in _font_entries(project) if isinstance(entry, dict)}
    warnings = []
    for widget in project.widgets:
        font = widget.props.get("font")
        if isinstance(font, str) and font and font not in known and not BUILTIN_FONT.fullmatch(font):
            warnings.append(tr("{name}: the font {font} is not in the project, so the built-in font is used. Add it to the project and choose it again", name=widget.name, font=font))
    return warnings


def png_size(data):
    """(width, height) of PNG bytes, or None if they are not a PNG."""
    if len(data) < 24 or not data.startswith(PNG_SIGNATURE):
        return None
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def image_name(name):
    """A file name fit for an asset: letters, digits, _ . - and the .png ending."""
    stem = re.sub(r"\.[A-Za-z0-9]+$", "", str(name).replace("\\", "/").rsplit("/", 1)[-1])
    stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", stem).strip("._-") or "image"
    return stem[:56] + ".png"


def _entries(project):
    images = project.assets.get("images") if isinstance(project.assets, dict) else None
    return images if isinstance(images, list) else []


def images(project):
    """The images of the project: [{"name", "bytes", "width", "height"}], in project order."""
    result = []
    for entry in _entries(project):
        if not isinstance(entry, dict) or not isinstance(entry.get("data"), str):
            continue
        try:
            data = base64.b64decode(entry["data"].split(",", 1)[-1], validate=True)
        except ValueError:
            continue
        size = png_size(data)
        if size:
            result.append({"name": entry.get("name"), "bytes": len(data), "width": size[0], "height": size[1]})
    return result


def add_image(project, name, data, replace=False):
    """Add PNG bytes to the project under name; return the name used."""
    if not isinstance(data, (bytes, bytearray)) or png_size(data) is None:
        raise AssetError(tr("only PNG images can be added: convert the picture to PNG first"))
    if len(data) > MAX_IMAGE_BYTES:
        raise AssetError(tr("the image is {size} kB: the limit is {limit} kB, make it smaller", size=len(data) // 1024, limit=MAX_IMAGE_BYTES // 1024))
    name = image_name(name)
    if not IMAGE_NAME.fullmatch(name):
        raise AssetError(tr("invalid image name: {name}", name=name))
    entries = [entry for entry in _entries(project) if isinstance(entry, dict)]
    existing = next((entry for entry in entries if entry.get("name") == name), None)
    if existing is not None and not replace:
        raise AssetError(tr("{name}: an image with this name already exists", name=name))
    entry = {"name": name, "data": "data:image/png;base64," + base64.b64encode(bytes(data)).decode("ascii")}
    if existing is not None:
        entries[entries.index(existing)] = entry
    else:
        entries.append(entry)
    project.assets = {**(project.assets if isinstance(project.assets, dict) else {}), "images": entries}
    return name


def free_image_name(project, name):
    """name, or name with a number, so that it does not replace an image already in the project."""
    used = {entry.get("name") for entry in _entries(project) if isinstance(entry, dict)}
    candidate, number = image_name(name), 2
    while candidate in used:
        candidate = image_name(name)[:-4] + f"_{number}.png"
        number += 1
    return candidate


def remove_image(project, name):
    """Remove the image; return the names of the widgets that still show it."""
    entries = _entries(project)
    if not any(isinstance(entry, dict) and entry.get("name") == name for entry in entries):
        raise AssetError(tr("no such image: {name}", name=name))
    project.assets = {**project.assets, "images": [entry for entry in entries if not (isinstance(entry, dict) and entry.get("name") == name)]}
    return [widget.name for widget in project.widgets if widget.props.get("src") == name]


def image_warnings(project):
    """Image widgets that will stay empty, and images that cost a lot of memory."""
    known = {item["name"]: item for item in images(project)}
    warnings = []
    for widget in project.widgets:
        source = widget.props.get("src")
        if widget.type in ("image", "imagebutton") and source and source not in known:
            warnings.append(tr("{name}: the image {image} is not in the project, so nothing is drawn. Add it to the project and choose it again", name=widget.name, image=source))
    for item in known.values():
        decoded = item["width"] * item["height"] * 4 // 1024
        if item["bytes"] >= LARGE_IMAGE_BYTES or decoded >= 512:
            warnings.append(tr("{image}: {size} kB of PNG, {width}×{height}: on a board it needs about {decoded} kB of RAM while it is shown", image=item["name"], size=item["bytes"] // 1024, width=item["width"], height=item["height"], decoded=decoded))
    return warnings
