"""Writer of LVGL's binary font format, the one lv.binfont_create_from_buffer loads.

The layout follows lv_binfont_loader.c of the pinned LVGL: four-byte-aligned tables, each starting
with its length and a label. head describes the font and how glyph fields are packed; cmap maps
character codes to glyph ids; loca gives the offset of each glyph in glyf; glyf holds, for every
glyph, its metrics and its pixels as one bit stream; kern, written only when the font has kerning,
adjusts the advance of a glyph by the one that follows. Glyph id 0 is reserved.
"""

import struct

BITS_PER_PIXEL = 4
CMAP_FORMAT0_TINY = 2   # a run of consecutive codes: glyph id = first id + (code - first code)
CMAP_SPARSE_TINY = 3    # a sorted list of code offsets: glyph id = first id + position in the list
RUN = 4                 # consecutive codes from this many on get a table of their own


class _Bits:
    """Bit stream, most significant bit first."""

    def __init__(self):
        self.data = bytearray()
        self.used = 0

    def write(self, value, count):
        for position in range(count - 1, -1, -1):
            if self.used % 8 == 0:
                self.data.append(0)
            if (value >> position) & 1:
                self.data[-1] |= 0x80 >> (self.used % 8)
            self.used += 1


def _unsigned_bits(value):
    return max(1, int(value).bit_length())


def _signed_bits(values):
    return max(_unsigned_bits(value if value >= 0 else -value - 1) + 1 for value in values)


def _table(label, body):
    body = bytes(body) + b"\0" * (-(len(body) + 8) % 4)
    return struct.pack("<I4s", len(body) + 8, label) + body


def _segments(codes):
    """Split sorted codes into slices that one cmap subtable can describe: (kind, codes)."""
    runs = []
    for code in codes:
        if runs and code == runs[-1][-1] + 1:
            runs[-1].append(code)
        else:
            runs.append([code])
    segments = []
    for run in runs:
        if len(run) >= RUN:
            segments.append((CMAP_FORMAT0_TINY, run))
        elif segments and segments[-1][0] == CMAP_SPARSE_TINY and run[-1] - segments[-1][1][0] <= 0xFFFF:
            segments[-1][1].extend(run)
        else:
            segments.append((CMAP_SPARSE_TINY, list(run)))
    return segments


def _kern(pairs, count):
    """(kern table, scale) for pairs {(left id, right id): 1/16 pixel}, among count glyph ids.

    A value is stored in one signed byte as value * 16 / scale. Glyphs that kern alike share a
    class, and a table of left class by right class holds the values; a font with more than 255
    classes on a side gets the sorted list of pairs instead.
    """
    scale = max(16, -(-max(abs(value) for value in pairs.values()) * 16 // 127))
    pairs = {pair: round(value * 16 / scale) for pair, value in sorted(pairs.items())}
    pairs = {pair: value for pair, value in pairs.items() if value}
    sides = []
    for side in (0, 1):  # glyphs with the same values against every glyph of the other side form a class
        profiles = {}
        for pair, value in pairs.items():
            profiles.setdefault(pair[side], []).append((pair[1 - side], value))
        classes = {}
        sides.append({glyph: classes.setdefault(tuple(profile), len(classes) + 1) for glyph, profile in profiles.items()})
    rows, columns = (max(side.values(), default=0) for side in sides)
    if rows <= 255 and columns <= 255:
        values = bytearray(rows * columns)
        for (left, right), value in pairs.items():
            values[(sides[0][left] - 1) * columns + sides[1][right] - 1] = value & 0xFF
        mappings = b"".join(bytes(side.get(glyph, 0) for glyph in range(count)) for side in sides)
        return _table(b"kern", struct.pack("<B3xHBB", 3, count, rows, columns) + mappings + values), scale
    ids = b"".join(struct.pack("<HH" if count > 256 else "<BB", *pair) for pair in pairs)
    return _table(b"kern", struct.pack("<B3xI", 0, len(pairs)) + ids + bytes(value & 0xFF for value in pairs.values())), scale


def write_binfont(font):
    """Bytes of the font. font: size, underline_position, underline_thickness and glyphs, each with
    code, advance (in 1/16 pixel), width, height, ofs_x, ofs_y (bottom edge above the baseline) and
    pixels (one byte per pixel, 0 to 15, rows from the top); optionally kerning, {(code, next code):
    change of the advance in 1/16 pixel}."""
    glyphs = sorted(font["glyphs"], key=lambda glyph: glyph["code"])
    if not glyphs:
        raise ValueError("a font needs at least one glyph")
    ascent = max(glyph["ofs_y"] + glyph["height"] for glyph in glyphs)
    descent = min(glyph["ofs_y"] for glyph in glyphs)
    advance_bits = _unsigned_bits(max(glyph["advance"] for glyph in glyphs))
    xy_bits = _signed_bits([value for glyph in glyphs for value in (glyph["ofs_x"], glyph["ofs_y"])])
    wh_bits = _unsigned_bits(max(max(glyph["width"], glyph["height"]) for glyph in glyphs))

    offsets, body = [], bytearray()
    for glyph in [None, *glyphs]:  # id 0 is reserved: an empty record
        offsets.append(8 + len(body))
        bits = _Bits()
        advance, ofs_x, ofs_y, width, height, pixels = (glyph["advance"], glyph["ofs_x"], glyph["ofs_y"], glyph["width"], glyph["height"], glyph["pixels"]) if glyph else (0, 0, 0, 0, 0, b"")
        if len(pixels) != width * height:
            raise ValueError(f"glyph U+{glyph['code']:04X}: {len(pixels)} pixels for {width}x{height}")
        bits.write(advance, advance_bits)
        bits.write(ofs_x & ((1 << xy_bits) - 1), xy_bits)
        bits.write(ofs_y & ((1 << xy_bits) - 1), xy_bits)
        bits.write(width, wh_bits)
        bits.write(height, wh_bits)
        for value in pixels:
            bits.write(value, BITS_PER_PIXEL)
        body += bits.data
    glyf = _table(b"glyf", body)
    long_offsets = len(glyf) > 0xFFFF
    loca = _table(b"loca", struct.pack("<I", len(offsets)) + b"".join(struct.pack("<I" if long_offsets else "<H", offset) for offset in offsets))

    segments = _segments([glyph["code"] for glyph in glyphs])
    entries, lists = bytearray(), bytearray()
    lists_start = 8 + 4 + 16 * len(segments)
    glyph_id = 1
    for kind, codes in segments:
        count = len(codes) if kind == CMAP_SPARSE_TINY else 0
        entries += struct.pack("<IIHHHBB", lists_start + len(lists) if count else 0, codes[0], codes[-1] - codes[0] + 1, glyph_id, count, kind, 0)
        if count:
            lists += b"".join(struct.pack("<H", code - codes[0]) for code in codes)
        glyph_id += len(codes)
    cmap = _table(b"cmap", struct.pack("<I", len(segments)) + entries + lists)

    ids = {glyph["code"]: index for index, glyph in enumerate(glyphs, 1)}
    pairs = {(ids[left], ids[right]): value for (left, right), value in (font.get("kerning") or {}).items() if value and left in ids and right in ids}
    kern, scale = _kern(pairs, len(glyphs) + 1) if pairs else (b"", 0)

    head = _table(b"head", struct.pack(
        "<IHHHhHhHhhHH10BhH",
        1, 4 if kern else 3, font["size"], ascent, descent, ascent, descent, 0, descent, ascent, 0, scale,
        1 if long_offsets else 0, 1 if len(glyphs) + 1 > 256 else 0, 1, BITS_PER_PIXEL, xy_bits, wh_bits, advance_bits, 0, 0, 0,
        font.get("underline_position", 0), font.get("underline_thickness", 1),
    ))
    return head + cmap + loca + glyf + kern
