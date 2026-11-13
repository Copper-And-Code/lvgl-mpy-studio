"""A VT100/xterm screen in plain Python: what the Device Console shows.

It understands the sequences that ansiterm.py of mpy-lvgl-boards draws on a board's display,
so a program written for that terminal looks the same here: cursor (A B C D E F G H d f s u,
ESC 7/8), erase (J K X), insert and delete (L M @ P), scroll region (r, S, T, ESC D/E/M),
colours (m: 16 colours, 256 with 38;5 and 48;5, bold, reverse), ?25 cursor, ?7 wrap,
?1049 alternate screen, and the reports 5n, 6n and c, whose answers wait in `replies`.

Unlike ansiterm it keeps the lines that scroll off the top, and shows any Unicode character.
"""

from collections import deque

DEFAULT_FG = -1  # the colour of the text in the theme
DEFAULT_BG = -2  # the background of the theme
SCROLLBACK = 10000


class Screen:
    def __init__(self, cols=80, rows=24, scrollback=SCROLLBACK):
        self.cols, self.rows = cols, rows
        self.history = deque(maxlen=scrollback)  # rows scrolled off the top: lists of cells
        self.replies = bytearray()
        self.reset()

    # A cell is (character, foreground, background, bold).

    def _blank(self):
        return (" ", self.fg, self.bg, False)

    def _row(self):
        return [self._blank() for _ in range(self.cols)]

    def reset(self):
        self.fg, self.bg = DEFAULT_FG, DEFAULT_BG
        self.base_fg, self.base_bg = DEFAULT_FG, DEFAULT_BG
        self.bold = self.reverse = False
        self.lines = [self._row() for _ in range(self.rows)]
        self.x = self.y = 0
        self.top, self.bottom = 0, self.rows - 1
        self.wrap = True
        self.pending_wrap = False
        self.cursor_on = True
        self.saved = (0, 0, DEFAULT_FG, DEFAULT_BG, DEFAULT_FG, DEFAULT_BG, False, False)
        self.alt = None
        self.state = 0
        self.params = ""

    def resize(self, cols, rows):
        cols, rows = max(1, cols), max(1, rows)
        if (cols, rows) == (self.cols, self.rows):
            return
        blank = (" ", DEFAULT_FG, DEFAULT_BG, False)
        lines = [row[:cols] + [blank] * (cols - len(row)) for row in self.lines]
        while len(lines) > rows:  # the rows above the cursor go to the history first
            if self.y > 0 and self.alt is None:
                self.history.append(lines.pop(0))
                self.y -= 1
            else:
                lines.pop()
        while len(lines) < rows:
            lines.append([blank] * cols)
        self.lines, self.cols, self.rows = lines, cols, rows
        self.top, self.bottom = 0, rows - 1
        self.x, self.y = min(self.x, cols - 1), min(self.y, rows - 1)
        self.pending_wrap = False

    def clear(self):
        self.history.clear()
        self.lines = [self._row() for _ in range(self.rows)]
        self.x = self.y = 0
        self.pending_wrap = False

    def text(self):
        """Everything shown, history included, as plain text."""
        rows = list(self.history) + self.lines
        lines = ["".join(cell[0] for cell in row).rstrip() for row in rows]
        while lines and not lines[-1]:
            lines.pop()
        return "\n".join(lines) + ("\n" if lines else "")

    def take_replies(self):
        data, self.replies = bytes(self.replies), bytearray()
        return data

    # ---- Drawing ----

    def _scroll(self, n, top=None):
        """n > 0: up, n < 0: down, between top and the bottom margin."""
        top = self.top if top is None else top
        size = self.bottom - top + 1
        count = min(abs(n), size)
        region = self.lines[top:self.bottom + 1]
        if n > 0:
            if top == 0 and self.alt is None:
                self.history.extend(region[:count])
            region = region[count:] + [self._row() for _ in range(count)]
        else:
            region = [self._row() for _ in range(count)] + region[:size - count]
        self.lines[top:self.bottom + 1] = region

    def _line_feed(self):
        if self.y == self.bottom:
            self._scroll(1)
        elif self.y < self.rows - 1:
            self.y += 1

    def _reverse_feed(self):
        if self.y == self.top:
            self._scroll(-1)
        elif self.y > 0:
            self.y -= 1

    def _put(self, char):
        if self.pending_wrap:
            self.pending_wrap = False
            self.x = 0
            self._line_feed()
        self.lines[self.y][self.x] = (char, self.fg, self.bg, self.bold)
        if self.x < self.cols - 1:
            self.x += 1
        elif self.wrap:
            self.pending_wrap = True

    def _erase(self, start, end):
        """Blanks the cells from start to end, counted row by row, with the current background."""
        for index in range(max(0, start), min(end, self.cols * self.rows)):
            y, x = divmod(index, self.cols)
            self.lines[y][x] = self._blank()

    def _goto(self, x, y):
        self.x = max(0, min(self.cols - 1, x))
        self.y = max(0, min(self.rows - 1, y))
        self.pending_wrap = False

    # ---- Parser ----

    def feed(self, text):
        for char in text:
            code = ord(char)
            if self.state == 0:
                if code == 27:
                    self.state = 1
                elif code < 32:
                    self._control(code)
                elif code != 127:
                    self._put(char)
            elif code in (24, 26):  # CAN, SUB
                self.state = 0
            elif self.state == 1:
                self._escape(char)
            elif self.state == 2:
                if 0x40 <= code <= 0x7E:
                    self.state = 0
                    self._csi(char)
                else:
                    self.params += char
            elif self.state == 3:  # OSC: until BEL or ESC \
                if code == 7:
                    self.state = 0
                elif code == 27:
                    self.state = 1
            else:  # the character set after ESC ( or ESC )
                self.state = 0

    def _control(self, code):
        wrapping, self.pending_wrap = self.pending_wrap, False
        if code == 13:
            self.x = 0
        elif code in (10, 11, 12):
            self._line_feed()
        elif code == 8:
            self.x = max(0, self.x - 1)
        elif code == 9:
            self.x = min(self.cols - 1, (self.x // 8 + 1) * 8)
        else:
            self.pending_wrap = wrapping

    def _escape(self, char):
        self.state = 0
        if char == "[":
            self.state = 2
            self.params = ""
        elif char == "]":
            self.state = 3
        elif char in "()":
            self.state = 4
        elif char == "7":
            self._save()
        elif char == "8":
            self._restore()
        elif char == "D":
            self._line_feed()
        elif char == "E":
            self.x = 0
            self._line_feed()
        elif char == "M":
            self._reverse_feed()
        elif char == "c":
            history = self.history
            self.reset()
            self.history = history

    def _save(self):
        self.saved = (self.x, self.y, self.fg, self.bg, self.base_fg, self.base_bg, self.bold, self.reverse)

    def _restore(self):
        self.x, self.y, self.fg, self.bg, self.base_fg, self.base_bg, self.bold, self.reverse = self.saved
        self.pending_wrap = False

    def _csi(self, final):
        private = self.params.startswith("?")
        text = self.params[1:] if private else self.params
        args = []
        for part in text.split(";"):
            try:
                args.append(int(part))
            except ValueError:
                args.append(0)
        n = args[0]
        count = max(1, n)
        second = args[1] if len(args) > 1 else 0
        if private:
            if final in "hl":
                self._mode(args, final == "h")
            return
        cols = self.cols
        pos = self.y * cols + self.x
        if final == "A":
            self._goto(self.x, max(self.y - count, self.top if self.y >= self.top else 0))
        elif final == "B":
            limit = self.bottom if self.y <= self.bottom else self.rows - 1
            self._goto(self.x, min(self.y + count, limit))
        elif final == "C":
            self._goto(self.x + count, self.y)
        elif final == "D":
            self._goto(self.x - count, self.y)
        elif final == "E":
            self._goto(0, self.y + count)
        elif final == "F":
            self._goto(0, self.y - count)
        elif final == "G":
            self._goto(count - 1, self.y)
        elif final == "d":
            self._goto(self.x, count - 1)
        elif final in "Hf":
            self._goto(max(1, second) - 1, count - 1)
        elif final == "J":
            start, end = ((pos, cols * self.rows), (0, pos + 1), (0, cols * self.rows))[min(n, 2)]
            self._erase(start, end)
        elif final == "K":
            row = self.y * cols
            start, end = ((pos, row + cols), (row, pos + 1), (row, row + cols))[min(n, 2)]
            self._erase(start, end)
        elif final == "X":
            self._erase(pos, min(pos + count, self.y * cols + cols))
        elif final == "m":
            self._sgr(args)
        elif final in "LM":
            if self.top <= self.y <= self.bottom:
                self._scroll(-count if final == "L" else count, self.y)
                self.x = 0
        elif final == "S":
            self._scroll(count)
        elif final == "T":
            self._scroll(-count)
        elif final in "@P":
            self._shift_cells(count, final == "@")
        elif final == "r":
            top, bottom = count - 1, (second or self.rows) - 1
            if top < bottom < self.rows:
                self.top, self.bottom = top, bottom
                self._goto(0, 0)
        elif final == "s":
            self._save()
        elif final == "u":
            self._restore()
        elif final == "n":
            if n == 5:
                self.replies += b"\x1b[0n"
            elif n == 6:
                self.replies += f"\x1b[{self.y + 1};{self.x + 1}R".encode()
        elif final == "c":
            self.replies += b"\x1b[?1;2c"

    def _shift_cells(self, n, right):
        """Insert or delete n cells at the cursor; the rest of the row moves."""
        row = self.lines[self.y]
        n = min(n, self.cols - self.x)
        blanks = [self._blank() for _ in range(n)]
        if right:
            row[self.x:] = blanks + row[self.x:self.cols - n]
        else:
            row[self.x:] = row[self.x + n:] + blanks

    def _sgr(self, args):
        index = 0
        while index < len(args):
            value = args[index]
            if value == 0:
                self.bold = self.reverse = False
                self.base_fg, self.base_bg = DEFAULT_FG, DEFAULT_BG
            elif value == 1:
                self.bold = True
            elif value == 22:
                self.bold = False
            elif value == 7:
                self.reverse = True
            elif value == 27:
                self.reverse = False
            elif 30 <= value <= 37:
                self.base_fg = value - 30
            elif value == 39:
                self.base_fg = DEFAULT_FG
            elif 40 <= value <= 47:
                self.base_bg = value - 40
            elif value == 49:
                self.base_bg = DEFAULT_BG
            elif 90 <= value <= 97:
                self.base_fg = value - 82
            elif 100 <= value <= 107:
                self.base_bg = value - 92
            elif value in (38, 48) and index + 2 < len(args) and args[index + 1] == 5:
                if value == 38:
                    self.base_fg = args[index + 2] & 255
                else:
                    self.base_bg = args[index + 2] & 255
                index += 2
            index += 1
        fg = self.base_fg
        if self.bold and 0 <= fg < 8:
            fg += 8
        self.fg, self.bg = (self.base_bg, fg) if self.reverse else (fg, self.base_bg)

    def _mode(self, args, on):
        for value in args:
            if value == 25:
                self.cursor_on = on
            elif value == 7:
                self.wrap = on
            elif value in (1049, 47, 1047):
                self._alternate(on)

    def _alternate(self, on):
        if on and self.alt is None:
            self.alt = ([list(row) for row in self.lines], self.x, self.y)
            self.lines = [self._row() for _ in range(self.rows)]
            self._goto(0, 0)
        elif not on and self.alt is not None:
            lines, x, y = self.alt
            self.alt = None
            self.lines = lines
            self._goto(x, y)


def palette():
    """The 256 xterm colours as 0xRRGGBB, with the 16 basic ones of ansiterm.py."""
    rgb = [
        0x000000, 0xCC3333, 0x33BB33, 0xCCAA22, 0x3366DD, 0xBB44BB, 0x22AAAA, 0xCCCCCC,
        0x666666, 0xFF6666, 0x66EE66, 0xFFEE66, 0x7799FF, 0xFF77FF, 0x66EEEE, 0xFFFFFF,
    ]
    levels = (0, 95, 135, 175, 215, 255)
    rgb += [r << 16 | g << 8 | b for r in levels for g in levels for b in levels]
    rgb += [(8 + i * 10) * 0x010101 for i in range(24)]
    return rgb
