# Status: what is verified, and how

Version 0.6.0 is in development and has not been released. This page separates what has been
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
| Upload progress window | yes | | RP2350: the figures it shows | the window itself, watched by a person |
| Buzzer | yes | yes, in the simulator | | on a board |
| Block: Digital Output | yes, with a fake `machine` | yes, in the simulator | STM32H7_CORE: the two LEDs of the board on pins `B0` and `B1`, driven from a Timer, the pin levels read back and the LEDs seen by the author | other boards |
| Block: Digital Input | yes, with a fake `machine` | yes, in the simulator | | on any board |
| Block Manager, blocks from other people | yes | | | used by a person; a block written by someone else |
| Browser version (WebAssembly) | yes | | Chromium, two resolutions | Firefox, Safari, phones |
| Single-file executables | yes, on Linux and under Wine | | Linux | Windows, natively |
| Windows | yes, under Wine | | | **natively, see below** |
| MCP server | yes, and a recorded session | | | the board tools, on hardware |
| Visual tests | yes | | used on the EIM-01 example | |
| Print Sources | yes | | a PDF, read | a real printer |
| Self-test, visible mode (`--show`) | | | | never run |
| AppImage for Linux | | yes, run from inside the package | built from the sources of 0.6.0 on the author's computer: self-test, visual tests of EIM-01, board and C generation, single-file games for Linux (needing glibc 2.34 or later) and Windows, browser version | on another Linux system |
| Portable Windows package | | | built for 0.6.0; its contents inspected: no bundled ICU, the icon in the program file, the blocks | **started on a real Windows** |

"Author's use" means the author uses it while developing; it is not a test plan.

## Known defects and open points

- **Windows.** The portable package of 0.4 did not start on a real Windows: it bundled a copy
  of ICU that hid the system's. The packaging was corrected in 0.5.1 and a package of 0.6.0
  was built without it, but nobody has started it on Windows yet. Tests under Wine did not
  show the fault and cannot be trusted for this.
- **The IDE does not know the pins of a board.** A block takes the pin the user types, a
  number or a name such as `PA5`, and nothing warns when it is one the display or the memory
  already uses.
- **The RAM budget** shown in the status bar is measured in the 64-bit simulator and is an
  overestimate for 32-bit boards.
- **Renaming a Python module** does not rewrite the code that imports it; the IDE warns.
- **Reference images that hold a changing value** fail when the generator changes: the EIM-01
  example shows the free memory on a page, and its image had to be regenerated for 0.6.
- **Continuous integration is off** while the repository is private. The suite is run locally
  before each commit; the two slowest files are not always among the tests run.
- **An upload sends every file again**, also those that did not change: a project with fonts
  takes tens of seconds on a slow link each time.

## What is not there

- C on boards: only MicroPython is uploaded. The C export is source code for another project.
- An online catalogue of blocks, and blocks that depend on other blocks.
- Extensions that run inside the IDE: blocks are data and MicroPython code, nothing more.
- Blocks for PWM, ADC, I2C, SPI and UART: planned in [the plan](plugins-plan.md), not written.
- A debugger. Errors are reported with file and line; there are no breakpoints.
- macOS.

## How to check for yourself

```bash
.venv/bin/python -m pytest -q        # the whole suite, about ten minutes
.venv/bin/lvgl-mpy-studio selftest   # the IDE uses itself, about twenty seconds
```

The self-test writes `report.txt` with one line for each step. A step that fails is a defect
worth reporting.
