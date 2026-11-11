import base64
import binascii
import re
import struct

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SOF = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}


def parse_data_url(url):
    match = re.fullmatch(r"data:([^;,]+)(?:;[^,]*)?;base64,([A-Za-z0-9+/=\s]*)", str(url or ""))
    if not match:
        return None
    encoded = re.sub(r"\s+", "", match.group(2))
    try:
        data = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError):
        return None
    return {"mime": match.group(1).lower(), "base64": encoded, "bytes": data}


def image_info(data):
    if len(data) >= 24 and data.startswith(PNG_SIGNATURE):
        return {"format": "png", "width": struct.unpack_from(">I", data, 16)[0], "height": struct.unpack_from(">I", data, 20)[0]}
    if len(data) >= 4 and data[:2] == b"\xff\xd8":
        index = 2
        while index + 9 < len(data):
            if data[index] != 0xFF:
                return None
            marker = data[index + 1]
            if marker == 0xFF:
                index += 1
                continue
            if marker in JPEG_SOF:
                return {"format": "jpeg", "width": struct.unpack_from(">H", data, index + 7)[0], "height": struct.unpack_from(">H", data, index + 5)[0]}
            if marker in (0xDA, 0xD9):
                return None
            index += 2 + struct.unpack_from(">H", data, index + 2)[0]
    return None


def c_byte_lines(data, per_line=16):
    return [", ".join(f"0x{byte:02x}" for byte in data[start:start + per_line]) + "," for start in range(0, len(data), per_line)]
