import time

import pytest

from lvgl_mpy_studio.core.vt import DEFAULT_BG, DEFAULT_FG, Screen


def rows(screen):
    return ["".join(cell[0] for cell in row) for row in screen.lines]


def screen_with(text, cols=10, rows_=4):
    screen = Screen(cols, rows_)
    screen.feed(text)
    return screen


def test_text_wraps_and_scrolls_into_the_history():
    screen = screen_with("0123456789AB\r\nline2\r\nline3\r\nline4")
    assert rows(screen) == ["AB        ", "line2     ", "line3     ", "line4     "]
    assert screen.text() == "0123456789\nAB\nline2\nline3\nline4\n"
    assert len(screen.history) == 1


def test_wrap_is_pending_until_the_next_character():
    screen = screen_with("0123456789")
    assert (screen.x, screen.y) == (9, 0) and screen.pending_wrap
    screen.feed("\r\n")
    assert (screen.x, screen.y) == (0, 1)  # no empty line in between


@pytest.mark.parametrize("sequence, position", [
    ("\x1b[3;5H", (4, 2)), ("\x1b[2d", (0, 1)), ("\x1b[7G", (6, 0)),
    ("\x1b[3;3H\x1b[2A", (2, 0)), ("\x1b[B\x1b[3C", (3, 1)), ("\x1b[4;9H\x1b[2D", (6, 3)),
    ("\x1b[3;3H\x1b[E", (0, 3)), ("\x1b[3;3H\x1b[F", (0, 1)), ("\x1b[99;99H", (9, 3)),
    ("\x1b[2;2H\x1b7\x1b[H\x1b8", (1, 1)), ("\x1b[2;2H\x1b[s\x1b[H\x1b[u", (1, 1)),
])
def test_cursor_moves(sequence, position):
    screen = screen_with(sequence)
    assert (screen.x, screen.y) == position


def test_erase_in_display_and_line():
    full = "\r\n".join(["aaaaaaaaaa", "bbbbbbbbbb", "cccccccccc", "dddddddddd"])
    assert rows(screen_with(full + "\x1b[2;5H\x1b[J")) == ["aaaaaaaaaa", "bbbb      ", "          ", "          "]
    assert rows(screen_with(full + "\x1b[2;5H\x1b[1J")) == ["          ", "     bbbbb", "cccccccccc", "dddddddddd"]
    assert rows(screen_with(full + "\x1b[2J")) == [" " * 10] * 4
    assert rows(screen_with(full + "\x1b[2;5H\x1b[K"))[1] == "bbbb      "
    assert rows(screen_with(full + "\x1b[2;5H\x1b[1K"))[1] == "     bbbbb"
    assert rows(screen_with(full + "\x1b[2;5H\x1b[2K"))[1] == " " * 10
    assert rows(screen_with(full + "\x1b[2;5H\x1b[3X"))[1] == "bbbb   bbb"


def test_insert_and_delete_characters_and_lines():
    assert rows(screen_with("abcdef\x1b[1;3H\x1b[2@"))[0] == "ab  cdef  "
    assert rows(screen_with("abcdef\x1b[1;3H\x1b[2P"))[0] == "abef      "
    lines = "1\r\n2\r\n3\r\n4"
    assert [row[0] for row in rows(screen_with(lines + "\x1b[2;1H\x1b[L"))] == ["1", " ", "2", "3"]
    assert [row[0] for row in rows(screen_with(lines + "\x1b[2;1H\x1b[M"))] == ["1", "3", "4", " "]


def test_scroll_region_keeps_the_lines_outside():
    screen = screen_with("top\r\n1\r\n2\r\nbottom\x1b[2;3r\x1b[3;1H\n")
    assert [row.rstrip() for row in rows(screen)] == ["top", "2", "", "bottom"]
    assert not screen.history  # a region that does not start at the top keeps no history
    screen.feed("\x1b[2;1H\x1bM")
    assert [row.rstrip() for row in rows(screen)] == ["top", "", "2", "bottom"]
    screen.feed("\x1b[r\x1b[S")
    assert [row.rstrip() for row in rows(screen)] == ["", "2", "bottom", ""]
    screen.feed("\x1b[T")
    assert [row.rstrip() for row in rows(screen)] == ["", "", "2", "bottom"]


def test_colours_bold_and_reverse():
    screen = screen_with("\x1b[31ma\x1b[1mb\x1b[0;44mc\x1b[38;5;200;48;5;17md\x1b[0;7me\x1b[0m\x1b[92mf")
    cells = screen.lines[0]
    assert cells[0][1:] == (1, DEFAULT_BG, False)
    assert cells[1][1:] == (9, DEFAULT_BG, True)  # bold brightens the eight basic colours, as ansiterm
    assert cells[2][1:] == (DEFAULT_FG, 4, False)
    assert cells[3][1:] == (200, 17, False)
    assert cells[4][1:] == (DEFAULT_BG, DEFAULT_FG, False)
    assert cells[5][1] == 10


def test_alternate_screen_restores_what_was_there():
    screen = screen_with("shell$ vi\x1b[?1049h\x1b[Hediting")
    assert rows(screen)[0].rstrip() == "editing"
    screen.feed("\x1b[?1049l")
    assert rows(screen)[0].rstrip() == "shell$ vi"
    assert (screen.x, screen.y) == (9, 0)


def test_modes_cursor_and_wrap():
    screen = screen_with("\x1b[?25l\x1b[?7l0123456789XY")
    assert not screen.cursor_on
    assert rows(screen)[0] == "012345678Y"  # without wrap the last column is overwritten
    screen.feed("\x1b[?25h")
    assert screen.cursor_on


def test_reports_wait_as_replies():
    screen = screen_with("ab\x1b[6n\x1b[5n\x1b[c")
    assert screen.take_replies() == b"\x1b[1;3R\x1b[0n\x1b[?1;2c"
    assert screen.take_replies() == b""


def test_unicode_osc_and_cancelled_sequences():
    screen = screen_with("ü€\x1b]0;title\x07x\x1b[3\x18y\x1b(Bz")
    assert rows(screen)[0].rstrip() == "ü€xyz"


def test_resize_keeps_the_cursor_line():
    screen = screen_with("1\r\n2\r\n3\r\n4")
    screen.resize(5, 2)
    assert [row.rstrip() for row in rows(screen)] == ["3", "4"]
    assert (screen.x, screen.y) == (1, 1)
    assert screen.text() == "1\n2\n3\n4\n"
    screen.resize(12, 3)
    assert len(screen.lines) == 3 and len(screen.lines[0]) == 12


def test_full_reset_keeps_the_history():
    screen = screen_with("1\r\n2\r\n3\r\n4\r\n5\x1b[31m\x1bc")
    assert rows(screen) == [" " * 10] * 4
    assert screen.fg == DEFAULT_FG
    assert screen.text().startswith("1\n")


def test_a_long_output_is_fast():
    screen = Screen(80, 24)
    line = "\x1b[32mfile.py\x1b[0m   1234  \x1b[1mbold\x1b[0m text text text text\r\n"
    payload = line * (20000 // len(line))
    started = time.perf_counter()
    screen.feed(payload)
    assert time.perf_counter() - started < 1.0
    assert len(screen.history) > 300


# ---- The widget ----


def test_keys_become_the_bytes_of_xterm(qtbot):
    from PySide6.QtCore import Qt

    from lvgl_mpy_studio.ui.terminal import TerminalView

    view = TerminalView()
    qtbot.addWidget(view)
    view.input_enabled = True
    sent = []
    view.typed.connect(sent.append)
    view.show()
    view.setFocus()
    for key, modifiers in (
        (Qt.Key_Up, Qt.NoModifier), (Qt.Key_Left, Qt.NoModifier), (Qt.Key_Home, Qt.NoModifier),
        (Qt.Key_Delete, Qt.NoModifier), (Qt.Key_PageDown, Qt.NoModifier), (Qt.Key_Tab, Qt.NoModifier),
        (Qt.Key_Backspace, Qt.NoModifier), (Qt.Key_Return, Qt.NoModifier), (Qt.Key_Escape, Qt.NoModifier),
        (Qt.Key_A, Qt.ControlModifier), (Qt.Key_S, Qt.ControlModifier), (Qt.Key_BracketRight, Qt.ControlModifier),
    ):
        qtbot.keyClick(view, key, modifiers)
    from PySide6.QtCore import QEvent
    from PySide6.QtGui import QKeyEvent
    from PySide6.QtWidgets import QApplication

    QApplication.sendEvent(view, QKeyEvent(QEvent.KeyPress, Qt.Key_unknown, Qt.NoModifier, "è"))  # QTest cannot type it
    assert sent == [b"\x1b[A", b"\x1b[D", b"\x1b[H", b"\x1b[3~", b"\x1b[6~", b"\t", b"\x7f", b"\r", b"\x1b",
                    b"\x01", b"\x13", b"\x1d", "è".encode()]


def test_reports_are_answered_and_paste_ends_lines_with_enter(qtbot):
    from PySide6.QtGui import QGuiApplication

    from lvgl_mpy_studio.ui.terminal import TerminalView, paste_bytes

    view = TerminalView()
    qtbot.addWidget(view)
    sent = []
    view.typed.connect(sent.append)
    view.feed("\x1b[6n")
    assert sent == []  # nobody is listening: the answer would go nowhere
    view.input_enabled = True
    view.feed("\x1b[6n")
    assert sent == [b"\x1b[1;1R"]
    assert paste_bytes("a\r\nb\nc") == b"a\rb\rc"
    QGuiApplication.clipboard().setText("print(1)\n")
    view.paste()
    assert sent[-1] == b"print(1)\r"


def test_selection_is_copied_as_text(qtbot):
    from lvgl_mpy_studio.ui.terminal import TerminalView

    view = TerminalView()
    qtbot.addWidget(view)
    view.resize(400, 200)
    view.show()
    view.feed("first line\r\nsecond")
    view._selection = ((0, 6), (1, 2))
    assert view.selected_text() == "line\nsec"
    view.select_all()
    assert view.selected_text().startswith("first line\nsecond")
    view.clear()
    assert view.text() == ""
