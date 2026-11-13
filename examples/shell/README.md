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

Keep the folder apart from a `shell.py` in the same place: MicroPython's `import shell` finds the
folder `shell/` first, and a `main.py` that imports the shell then fails. The IDE asks before
such an upload. On the RP2350 without PSRAM the shell does not fit as source. Upload it with
**Compile Python files to bytecode (.mpy)**, and leave out `main.py` and `boot.py`, which stay `.py`.

Tried on 13 November 2026 on the STM32H7_CORE V1.3 and the ESP32-4848S040: upload, start,
`pwd`, `ls`, `uname -a`, `cd`, `exit`. The editors were tried in the simulator only.

## Origin and licences

Copied from `examples/shell` of
[mpy-lvgl-boards](https://github.com/Copper-And-Code/mpy-lvgl-boards), commit `375cdd6` of
13 November 2026. With firmware v0.1.7, which has `display_driver.CONTRACT`, `ansiterm.py` only
calls `display_driver.start()`. With older firmware it falls back to the driver's internal
names, as before.

The code is MIT, Copyright (c) 2026 Nunzio Raciti. The font in `ansifont.py` is the ASCII part
of Terminus Font, Copyright (C) 2020 Dimitar Toshkov Zhekov, under the SIL Open Font License 1.1
in `OFL.txt`; only that file is not MIT.
