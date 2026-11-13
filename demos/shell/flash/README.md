# A Linux-like shell for MicroPython boards

A program without pages: a shell with `ls`, `cd`, `cp`, `rm`, `grep`, pipes, redirections,
history and Tab completion, an ANSI terminal drawn on the display, and two full-screen
editors, `edit` and `vi`. It runs on the boards of `mpy-lvgl-boards` and in the simulator of
LVGL MPY Studio.

| File | What it is |
|---|---|
| `shell.py` | the shell; `help` lists the commands |
| `ansiterm.py` | a VT100 terminal on an LVGL canvas, which receives what MicroPython prints through `os.dupterm` |
| `ansifont.py` | the 8×16 font of the terminal |
| `edit.py`, `vi.py` | the editors; the shell runs them as `edit` and `vi` once they are in `/bin` |

## In the simulator

**Run → Run Program…** and choose `shell.py`. The simulator runs it as an STM32H7_CORE V1.3,
1024×600: the screen shows the terminal of `ansiterm.py`, and the terminal under it is the
serial port, where you type. The program has a flash of its own and cannot leave it.

To use the editors by name, once: `mkdir /bin`, `cp edit.py /bin/edit.py`,
`cp vi.py /bin/vi.py`. The flash keeps them for the next runs.

## On a board

1. **Device → Upload Files… → Add Folder…**, this folder, destination `/flash` (STM32) or `/`
   (ESP32-S3, RP2350). The files go to `/flash/shell/` or `/shell/`.
2. **Device → Run File on Board…**, `/flash/shell/shell.py` or `/shell/shell.py`.
3. Use it from **Device Console**: every key reaches the shell as it is typed.

Tried on 13 November 2026 on the STM32H7_CORE V1.3 and the ESP32-4848S040: upload, start,
`pwd`, `ls`, `uname -a`, `cd`, `exit`. The editors were tried in the simulator only.

## Origin and licences

Copied on 13 November 2026 from `examples/shell` of
[mpy-lvgl-boards](https://github.com/Copper-And-Code/mpy-lvgl-boards) (commit `9a4c15a`), with
one change made the same day in both places: `ansiterm.py` calls `display_driver._arm()` only
when the driver has it, since the STM32 driver's timer is periodic and has none.

The code is MIT, Copyright (c) 2026 Nunzio Raciti. The font in `ansifont.py` is the ASCII part
of Terminus Font, Copyright (C) 2020 Dimitar Toshkov Zhekov, under the SIL Open Font License 1.1
in `OFL.txt`; only that file is not MIT.
