"""Convert a TrueType or OpenType font to LVGL's binary format, with Qt as the rasteriser.

It does the job of lv_font_conv without Node.js. Compared with LVGL's own Montserrat, which that
tool made, metrics are the same and pixels differ by at most one level of sixteen on fewer than
one in a thousand, and kerning is the same wherever that font has it. This module needs Qt, so it
lives outside the Qt-free packages; lvgl_mpy_studio.gen.fonts calls it when a project uses its own
fonts.
"""

import math

from PySide6.QtCore import QByteArray
from PySide6.QtGui import QFont, QFontDatabase, QGuiApplication, QImage, QRawFont, QTextLayout

from lvgl_mpy_studio.gen.binfont import write_binfont

_application = None
KERNING_LIMIT = 400  # above this many characters only Latin, Greek and Cyrillic are kerned


def _qt():
    """Fonts need a Qt application; the command line and the MCP server have none of their own.

    A full QApplication, not the lighter QGuiApplication: the same process may open windows later,
    and Qt aborts if widgets are created on an application that is not one.
    """
    global _application
    if QGuiApplication.instance() is None:
        import os

        from PySide6.QtWidgets import QApplication

        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        _application = QApplication([])


def kerning(data, size, characters):
    """{(code, next code): change of the advance in 1/16 pixel} for the pairs of characters the font kerns.

    Qt gives kerning only through text layout, which reads it from the font as a browser would. Each
    character is laid out followed by every other one, at one pixel per font unit and without
    hinting, so the distances are the values the font holds; ligatures are off, to keep one glyph
    per character. A font that cannot be laid out reliably gets no kerning rather than a wrong one.
    """
    _qt()
    characters = [char for char in dict.fromkeys(characters) if len(char) == 1]
    if len(characters) > KERNING_LIMIT:  # every character against every other one: kept to the scripts that kern
        characters = [char for char in characters if ord(char) < 0x0530]
    identifier = QFontDatabase.addApplicationFontFromData(QByteArray(bytes(data)))
    families = QFontDatabase.applicationFontFamilies(identifier) if identifier >= 0 else []
    if not families or not hasattr(QFont, "setFeature"):
        return {}
    try:
        units = QRawFont(QByteArray(bytes(data)), 64, QFont.PreferNoHinting).unitsPerEm()
        raw = QRawFont(QByteArray(bytes(data)), units, QFont.PreferNoHinting)
        font = QFont(families[0])
        styles = QFontDatabase.styles(families[0])
        if styles:
            font.setStyleName(styles[0])
        font.setPixelSize(round(units))
        font.setHintingPreference(QFont.PreferNoHinting)
        for feature in ("liga", "clig", "dlig", "calt"):
            font.setFeature(QFont.Tag(feature), 0)
        glyph = {char: indexes[0] for char in characters if (indexes := raw.glyphIndexesForString(char)) and indexes[0]}
        advance = {char: raw.advancesForGlyphIndexes([index])[0].x() for char, index in glyph.items()}
        pairs = {}
        for left in glyph:
            text = "".join(left + right for right in glyph)
            layout = QTextLayout(text, font)
            layout.beginLayout()
            layout.createLine().setLineWidth(1e9)
            layout.endLayout()
            runs = layout.glyphRuns()
            indexes = [index for run in runs for index in run.glyphIndexes()]
            positions = [point.x() for run in runs for point in run.positions()]
            expected = [glyph[char] for char in text]
            if indexes != expected or any(run.rawFont().fontTable("head") != raw.fontTable("head") for run in runs):
                continue  # another font answered, or the layout merged glyphs: no kerning for this character
            for number, right in enumerate(glyph):
                value = round((positions[2 * number + 1] - positions[2 * number] - advance[left]) * size / units * 16)
                if value:
                    pairs[ord(left), ord(right)] = value
        return pairs
    finally:
        QFontDatabase.removeApplicationFont(identifier)


def rasterise(data, size, characters):
    """Glyphs of the characters at size pixels: (font description for write_binfont, characters without a glyph)."""
    _qt()
    raw = QRawFont(QByteArray(bytes(data)), size, QFont.PreferDefaultHinting)
    if not raw.isValid():
        raise ValueError("not a TrueType or OpenType font this program can read")
    units = raw.unitsPerEm()
    design = QRawFont(QByteArray(bytes(data)), units, QFont.PreferNoHinting)  # one pixel per font unit: advances as the font holds them
    glyphs, missing = [], []
    for char in dict.fromkeys(characters):
        if len(char) != 1:
            continue
        indexes = raw.glyphIndexesForString(char)
        if not indexes or indexes[0] == 0:
            missing.append(char)
            continue
        index = indexes[0]
        advance = math.floor(design.advancesForGlyphIndexes([index])[0].x() * size / units * 16 + 0.5)
        image = raw.alphaMapForGlyph(index, QRawFont.PixelAntialiasing)
        if image.isNull() or image.width() == 0 or image.height() == 0:
            glyphs.append({"code": ord(char), "advance": advance, "width": 0, "height": 0, "ofs_x": 0, "ofs_y": 0, "pixels": b""})
            continue
        image = image.convertToFormat(QImage.Format_Alpha8)
        rect = raw.boundingRect(index)
        width, height, stride = image.width(), image.height(), image.bytesPerLine()
        bits = bytes(image.constBits())
        pixels = bytes(bits[row * stride + column] >> 4 for row in range(height) for column in range(width))
        top = math.floor(rect.top())
        glyphs.append({"code": ord(char), "advance": advance, "width": width, "height": height, "ofs_x": math.floor(rect.left()), "ofs_y": -(top + height), "pixels": pixels})
    font = {"size": size, "underline_position": -round(raw.underlinePosition()), "underline_thickness": max(1, round(raw.lineThickness())), "glyphs": glyphs, "kerning": kerning(data, size, [chr(glyph["code"]) for glyph in glyphs])}
    return font, missing


def convert(data, size, characters):
    """{"output": bytes of the LVGL font, "missing": characters the font has no glyph for} or {"error": text}."""
    try:
        font, missing = rasterise(data, size, characters)
        if not font["glyphs"]:
            return {"error": "the font has none of the characters used"}
        return {"output": write_binfont(font), "missing": "".join(missing)}
    except ValueError as exc:
        return {"error": str(exc)}
