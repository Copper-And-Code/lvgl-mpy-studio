# Status: what is verified, and how

Version 0.6.1 is published as a GitHub release, with an AppImage for Linux and a portable package for
Windows. This page separates what has been
checked from what has only been written.

## Read this first

The project was built broad on purpose: features expected to be useful were included from the
start, so that the design would not need to be reopened later. The automated tests are many.
**Human testing is scarce**: few people have used the IDE, and much of what is listed below has
never been tried by a person on a real task. Expect rough edges, and treat every "not tried"
below as an open question, not as a formality.

## How each area was checked

- **Tests**: covered by the automated suite, more than 1250 tests.
- **Self-test**: exercised in the real IDE window by `lvgl-mpy-studio selftest`.
- **Board**: tried on real hardware, with the board named.
- **Not tried**: written and tested by machine only, or not at all.

| Area | Tests | Self-test | Board or real use | Not tried |
|---|---|---|---|---|
| Designer, properties, undo | yes | yes | author's use | other users |
| Code editor, handlers, Python modules | yes | yes | ESP32-4848S040 (modules) | |
| Simulator on the PC | yes | yes | author's use | |
| MicroPython generation, upload as bytecode | yes | | ESP32-4848S040, STM32H7_CORE, Waveshare RP2350 | |
| Live editing on a board | yes | | ESP32-4848S040 | the other boards |
| Pictures in a project | yes | yes | STM32H7_CORE (seen on the display) | RP2350, ESP32-S3 |
| Fonts of a project, kerning | yes, against LVGL's Montserrat | yes | STM32H7_CORE (seen), RP2350 (loaded) | ESP32-S3 |
| Font memory warning | yes | | Waveshare RP2350 | |
| C export | yes, pixel parity with MicroPython in the simulator | | | in a real C project; fonts in C on a board |
| Device Console as a terminal (keys as typed, ANSI colours and cursor) | yes: the VT100 sequences cell by cell, the keys, the port taken and given back | | STM32H7_CORE V1.3 and ESP32-4848S040, 13 November 2026, driven by a script through the IDE's code: the shell typed to and read back, the console stopped and started again three times | typed by a person; full-screen editors on a board; Windows |
| Programs without pages in the simulator (Run Program) | yes: the service while waiting for a key, Ctrl-C, the flash that cannot be left, reset, the IDE | | the shell of `mpy-lvgl-boards` with `edit` and `vi`, driven by the tests of this work, not yet used by a person | used by a person; Windows, not available |
| Upload Files, Run File on Board | yes, with a board simulated in memory and a fake serial port | | STM32H7_CORE V1.3 (over its USB) and ESP32-4848S040, 13 November 2026: the shell of `examples/shell` copied (6 files, 110 kB, about 32 s) and started, `pwd`, `ls`, `uname -a`, `cd`, `exit` | the editors on a board; the RP2350; used by a person |
| Programs without pages in the browser (the shell demo) | yes: the page in headless Chromium, `help` answered; the build of the page | | | Firefox, Safari, a phone with its on-screen keyboard; used by a person |
| Upload progress window | yes | | RP2350: the figures it shows | the window itself, watched by a person |
| Buzzer | yes | yes, in the simulator | | on a board |
| Block: Digital Output | yes, with a fake `machine` | yes, in the simulator | STM32H7_CORE: the two LEDs of the board on pins `B0` and `B1`, driven from a Timer, the pin levels read back and the LEDs seen by the author | other boards |
| Block: Digital Input | yes, with a fake `machine` | yes, in the simulator | STM32H7_CORE: the two keys of the board on pins `A0` and `A1`; the author saw the LEDs follow the keys | other boards; the debounce, which was not measured |
| Block Manager, blocks from other people | yes | | | used by a person; a block written by someone else |
| Browser version (WebAssembly) | yes | | Chromium, two resolutions | Firefox, Safari, phones |
| Single-file executables | yes, on Linux and under Wine | | Linux | Windows, natively |
| Windows | yes, under Wine, and natively in continuous integration | yes, on Windows 11 from the portable package and in continuous integration | the portable package of 0.6.0 started by the author on Windows 11 | boards and builds on Windows |
| MCP server | yes, and a recorded session | | | the board tools, on hardware |
| Visual tests | yes | | used on the EIM-01 example | |
| Print Sources | yes | | a PDF, read | a real printer |
| Self-test, visible mode (`--show`) | | | | never run |
| AppImage for Linux | | yes, run from inside the package | the package of 0.6.1, released: self-test, 82 steps passed. The package of 0.6.0, on the author's computer: self-test, visual tests of EIM-01, board and C generation, single-file games for Linux (needing glibc 2.34 or later) and Windows, browser version | on another Linux system |
| Portable Windows package | | | the package of 0.6.0: contents inspected (no bundled ICU, the icon in the program file, the blocks) and started by the author on a real Windows. The package of 0.6.1, released: contents inspected, started by the author on Windows, no console windows flashing | the installer, never built |

"Author's use" means the author uses it while developing; it is not a test plan.

## Project website

The English documentation and five browser demos are published at
<https://copper-and-code.github.io/lvgl-mpy-studio/> from the `gh-pages` branch. On 12 November
2026, the public home, manual, gallery, and all five demos were checked in Chromium. Each demo
reported a running WebAssembly application and a non-black canvas; a simulated touch changed the
Fifteen screen, and no requests went to external domains. The IDE test for **Help → Online
Documentation** also passed and opens the same public address.

Firefox, Safari, and a real phone with touch and sound have not been tried.

## Known defects and open points

- **Windows.** The portable package of 0.4 did not start on a real Windows: it bundled a copy
  of ICU that hid the system's. The package of 0.6.0 is built without it and starts on
  Windows 11. The self-test run there passed 76 steps of 78. The step that failed was a
  mistake of the self-test, which compared a path written with `\` with the same path written
  with `/`; the step after it was skipped. The run also showed a real defect: when the program
  ended while a measurement was running, a simulator process stayed alive and its temporary
  folder could not be removed. Both are corrected, and the author ran the corrected package on Windows 11 without that
  error. Tests under Wine had shown neither. A third defect, reported by the author, is
  corrected: started from the program file, a console window flashed four times at almost
  every operation. On 13 November 2026 the author saw no such window with the package of 0.6.1.
- **The IDE does not know the pins of a board.** A block takes the pin the user types, a
  number or a name such as `PA5`, and nothing warns when it is one the display or the memory
  already uses.
- **The RAM budget** shown in the status bar is measured in the 64-bit simulator and is an
  overestimate for 32-bit boards.
- **Renaming a Python module** does not rewrite the code that imports it; the IDE warns.
- **Reference images that hold a changing value** fail when the generator changes: the EIM-01
  example shows the free memory on a page, and its image had to be regenerated for 0.6.
- **Continuous integration covers tests, not packages.** Since the repository became public,
  each push runs the whole suite and the self-test on Linux, and on Windows the tests of the
  core, of the runtime and of the IDE, and the self-test. On the Linux machine 72 tests are
  skipped, because they need what is not built there: the launchers of single-file games, the
  WebAssembly runtime, Wine, a browser. Packages are built and checked by hand.
- **An upload sends every file again**, also those that did not change: a project with fonts
  takes tens of seconds on a slow link each time.

## What is not there

- C on boards: only MicroPython is uploaded. The C export is source code for another project.
- An online catalogue of blocks, and blocks that depend on other blocks.
- Extensions that run inside the IDE: blocks are data and MicroPython code, nothing more.
- Blocks for PWM, ADC, I2C, SPI and UART: planned in [the plan](https://github.com/Copper-And-Code/lvgl-mpy-studio/blob/main/docs/plugins-plan.md), not written.
- A debugger. Errors are reported with file and line; there are no breakpoints.
- macOS.

## How to check for yourself

```bash
.venv/bin/python -m pytest -q        # the whole suite, about ten minutes
.venv/bin/lvgl-mpy-studio selftest   # the IDE uses itself, about twenty seconds
```

The self-test writes `report.txt` with one line for each step. A step that fails is a defect
worth reporting.
