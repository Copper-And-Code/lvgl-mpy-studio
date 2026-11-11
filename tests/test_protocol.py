from hypothesis import given, strategies as st

from lvgl_mpy_studio.sim.protocol import Decoder, MessageType, encode_hello, encode_key, encode_pointer, encode_present, encode_quit, encode_rect, encode_stop, encode_wheel


def round_trip(kind, payload):
    decoder = Decoder()
    data = kind(*payload)
    messages = []
    for byte in data:
        messages.extend(decoder.feed(bytes([byte])))
    assert len(messages) == 1
    return messages[0]


def test_hello_and_control_messages():
    token = bytes(range(16))
    assert round_trip(encode_hello, (800, 480, token))[1] == {"width": 800, "height": 480, "format": 1, "version": 2, "token": token}
    assert round_trip(encode_pointer, (12, 34, True))[1]["pressed"] is True
    assert round_trip(encode_key, (65, False))[1]["code"] == 65
    assert round_trip(encode_wheel, (-3,))[1]["delta"] == -3
    assert round_trip(encode_present, ())[0] == MessageType.PRESENT
    assert round_trip(encode_quit, ())[0] == MessageType.QUIT
    assert round_trip(encode_stop, ())[0] == MessageType.STOP


@given(st.integers(-100, 100), st.integers(-100, 100), st.integers(1, 20), st.integers(1, 20), st.binary())
def test_rect_round_trip(x, y, width, height, extra):
    extra = extra or b"\0"
    pixels = (extra * ((width * height * 2 // len(extra)) + 1))[:width * height * 2]
    _kind, values = round_trip(encode_rect, (x, y, width, height, pixels))
    assert values["pixels"] == pixels
    assert (values["x"], values["y"], values["width"], values["height"]) == (x, y, width, height)
