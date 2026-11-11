from enum import IntEnum
import struct

HEADER = struct.Struct("<BI")
MAX_PAYLOAD = 64 * 1024 * 1024


class MessageType(IntEnum):
    HELLO = 1
    RECT = 2
    PRESENT = 3
    POINTER = 4
    KEY = 5
    WHEEL = 6
    QUIT = 7
    STOP = 8


def encode_message(kind, payload=b""):
    if len(payload) > MAX_PAYLOAD: raise ValueError("Message too large")
    return HEADER.pack(int(kind), len(payload)) + payload


def encode_hello(width, height, token, color_format=1, version=2):
    if not isinstance(token, bytes) or len(token) != 16: raise ValueError("Invalid HELLO token")
    return encode_message(MessageType.HELLO, struct.pack("<HHBB", width, height, color_format, version) + token)


def encode_rect(x, y, width, height, pixels):
    return encode_message(MessageType.RECT, struct.pack("<hhhh", x, y, width, height) + pixels)


def encode_present():
    return encode_message(MessageType.PRESENT)


def encode_pointer(x, y, pressed):
    return encode_message(MessageType.POINTER, struct.pack("<hhB", x, y, bool(pressed)))


def encode_key(code, pressed):
    return encode_message(MessageType.KEY, struct.pack("<IB", code, bool(pressed)))


def encode_wheel(delta):
    return encode_message(MessageType.WHEEL, struct.pack("<h", delta))


def encode_quit():
    return encode_message(MessageType.QUIT)


def encode_stop():
    return encode_message(MessageType.STOP)


def decode_payload(kind, payload):
    if kind == MessageType.HELLO:
        if len(payload) != 22: raise ValueError("Invalid HELLO")
        values = struct.unpack_from("<HHBB", payload)
        return {**dict(zip(("width", "height", "format", "version"), values)), "token": payload[6:]}
    if kind == MessageType.RECT:
        x, y, width, height = struct.unpack_from("<hhhh", payload)
        expected = width * height * 2
        if width < 0 or height < 0 or len(payload) != 8 + expected: raise ValueError("Invalid RECT")
        return {"x": x, "y": y, "width": width, "height": height, "pixels": memoryview(payload)[8:]}
    if kind == MessageType.POINTER:
        x, y, pressed = struct.unpack("<hhB", payload)
        return {"x": x, "y": y, "pressed": bool(pressed)}
    if kind == MessageType.KEY:
        code, pressed = struct.unpack("<IB", payload)
        return {"code": code, "pressed": bool(pressed)}
    if kind == MessageType.WHEEL: return {"delta": struct.unpack("<h", payload)[0]}
    if payload: raise ValueError("Unexpected payload")
    return {}


class Decoder:
    def __init__(self):
        self._buffer = bytearray()

    def feed(self, data):
        self._buffer.extend(data)
        messages = []
        while len(self._buffer) >= HEADER.size:
            kind, length = HEADER.unpack_from(self._buffer)
            if length > MAX_PAYLOAD: raise ValueError("Message too large")
            if len(self._buffer) < HEADER.size + length: break
            payload = bytes(self._buffer[HEADER.size:HEADER.size + length])
            del self._buffer[:HEADER.size + length]
            try: message_type = MessageType(kind)
            except ValueError as exc: raise ValueError(f"Unknown message type: {kind}") from exc
            messages.append((message_type, decode_payload(message_type, payload)))
        return messages
