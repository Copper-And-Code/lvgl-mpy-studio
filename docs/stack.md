# The stack, from the display controller to the agent

LVGL MPY Studio is the top of a stack that goes down to the registers of the display
controller. This page follows one frame from the silicon to the tool an AI agent calls, and
says in which repository each layer lives.

| Layer | What it does | Where |
|---|---|---|
| 7. Agents | An AI agent designs, runs and tests an application through 49 tools | this repository, `mcp_server.py` |
| 6. IDE | Designer, code editor, generators, board upload | this repository |
| 5. Simulator | The same MicroPython and LVGL on the PC, and in the browser as WebAssembly | this repository, `native/lvsim`, `runtime/` |
| 4. Contract | What an application may assume of a board: `display_driver`, the board profile | both repositories |
| 3. Binding | `import lvgl as lv` in MicroPython, generated from LVGL's headers | [omnipython-lvgl](https://github.com/PyDevices/omnipython-lvgl), by PyDevices, pinned and unchanged |
| 2. Firmware | MicroPython boards built out of tree, with frozen drivers | [mpy-lvgl-boards](https://github.com/Copper-And-Code/mpy-lvgl-boards) |
| 1. Display drivers | C modules that put pixels on an RGB panel | [mpy-lvgl-boards](https://github.com/Copper-And-Code/mpy-lvgl-boards), `modules/` |

## One engine, four places it runs

Nothing here is an emulation or a mock-up. The board, the simulator, the single-file
executables for Linux and Windows and the browser version all run **the real code, compiled**:
the MicroPython interpreter and the LVGL library in C, built from the same sources at the same
pinned versions (`docs/target.md`), for each processor. The application itself is the same
MicroPython code everywhere; for the board and the executables it is compiled to bytecode by the
same `mpy-cross`. The simulator is
MicroPython's own Unix and Windows ports with LVGL compiled in; an executable is that
simulator with the application packed inside; the browser version is the same code compiled to
WebAssembly. What differs is only the thin layer that reaches the screen and the input: a
display driver on the board, a window on the PC, a canvas in the browser.

The consequence matters more than the design: **every fix and every improvement that the
MicroPython and LVGL projects release reaches all four at once.** A faster renderer, a new
widget, a corrected font or a fixed garbage collector improves the application on the board,
what the developer sees in the simulator, the programs given to users and the demos on the web,
with no porting work in this repository. An application also draws and behaves the same everywhere,
because nothing in between reinterprets it. What does not carry over is the machine: a board
has less memory and a slower processor than a PC, so the IDE measures memory on the board itself
and the status page says which checks were made on hardware.

What it takes is to move the pin: rebuild the runtimes with the new versions, rebuild the board
firmware in [mpy-lvgl-boards](https://github.com/Copper-And-Code/mpy-lvgl-boards), and run the
tests, which compare the renderings pixel by pixel. That step is deliberate, so that an upstream
change is adopted when it has been checked, not when it happens to land.

## Layers 1 and 2: registers and firmware

The firmware is a separate repository, [mpy-lvgl-boards](https://github.com/Copper-And-Code/mpy-lvgl-boards),
by the same author. Its documents hold the measurements and the bench logs; what follows is a
summary of what is there.

- **STM32H743, `modules/st_ltdc`.** The LTDC and the DMA2D are programmed through their
  registers, without the HAL sources for those peripherals. Frame buffers live in a region of
  the SDRAM that is never freed, because the LTDC keeps reading it across a soft reset.
  Partial updates are copied into the shown buffer by the DMA2D. Frames and underruns are
  counted and can be read from Python.
- **RP2350, `modules/rgbpanel`.** The RGB panel is scanned out by a PIO program fed by DMA.
  The DMA block that ends a frame reads the list for the next one, in hardware, so no
  interrupt runs per frame.
- **ESP32-S3, `modules/esp_rgb`.** The RGB panel of the ESP32-4848S040 through ESP-IDF.
- **Boards out of tree.** No fork of MicroPython or of the binding: board definitions, user C
  modules and a `patches/` folder applied by the build script, on pinned sources.
- **Tests on the board.** `tests/hil/` runs on the hardware with `mpremote`: panel, touch,
  performance, a soak test, behaviour when LVGL runs out of memory.

The frame rates, the soak times and the state of each board are in that repository's README
and are not repeated here, so that they have one source.

### Where the STM32H743 drivers come from

They are older than this project. The author wrote the LTDC display driver, the GT911 touch
driver and the board definitions himself and proposed them upstream in March 2026:

- [lvgl/lv_binding_micropython #407](https://github.com/lvgl/lv_binding_micropython/pull/407),
  the LTDC display and GT911 touch drivers: about 2900 lines in 14 files, with the C module,
  the board support for three boards and the Python layer that selects board and panel;
- [lvgl/lv_micropython #104](https://github.com/lvgl/lv_micropython/pull/104) and
  [#105](https://github.com/lvgl/lv_micropython/pull/105), the STM32H743 board family.

Those pull requests are still open; the first has had no review from a maintainer. In May
2026 the author paused them, saying so in the pull request, and took the same work to the
lvgl_micropython project, asking its maintainer which architecture a contribution should
follow: [discussion #577](https://github.com/lvgl-micropython/lvgl_micropython/discussions/577),
which ran until August with 8 threads and 45 replies. That repository has had no commits
since June 2026, and the series was not submitted there.

In November 2026 the code was ported, with the help of AI agents, to a repository of its own
on top of omnipython-lvgl, a binding under active development. One change needed there went
upstream and was merged:
[PyDevices/omnipython-lvgl #6](https://github.com/PyDevices/omnipython-lvgl/pull/6), LVGL
memory pools on ports without `multi_heap`.

## Layer 4: the contract

The IDE does not know a board's pins. It relies on two things the firmware provides:

- a frozen module, `display_driver`, with `start()`, `stop()`, `running()`, `backlight()`,
  `WIDTH`, `HEIGHT`, `BUFFERS`, `PERIOD_MS` and `indev`; `import display_driver` is all a
  generated application needs. From firmware v0.1.7 this is contract 1, `CONTRACT = 1`,
  written down in `docs/display-driver.md` of mpy-lvgl-boards. It also promises that a Ctrl-C
  reaches the program and the screen goes on, on every board. The one case left out is a
  Ctrl-C that lands in a Python callback of the application, such as an `lv.timer`. That
  happened 2 times in 60 on the ESP32-S3 and never on the other boards. Each Ctrl-C costs
  about 30 ms of still screen. The simulator's driver for programs has the same names and
  behaves the same way;
- facts read from the running board on connection: MicroPython and LVGL versions, the
  bytecode version, the built-in font sizes, whether fonts can be loaded at run time, free
  RAM and free space.

A board profile, a JSON file in `lvgl_mpy_studio/boards/`, holds what cannot be read: the
name, the resolution, the adapter, the serial protocol. When the board and the profile
disagree, for example on the font sizes, the board wins and the IDE says so.

## Layers 5 and 6: this repository

Places worth reading first:

| File | Why |
|---|---|
| `lvgl_mpy_studio/device/uart.py` | A raw-REPL transport written for the STM32H7 boards, reached through a UART adapter: chunked writes that stay inside the raw REPL |
| `lvgl_mpy_studio/device/service.py` | Upload as a transaction: staging folder, size check, rename, rollback |
| `lvgl_mpy_studio/gen/binfont.py`, `fontconv.py` | A TrueType to LVGL binary font converter, kerning included, compared in the tests with LVGL's own Montserrat |
| `native/lvsim/` | The C side of the simulator and its protocol, shared by the MicroPython and the C targets |
| `lvgl_mpy_studio/gen/` | The generators: one project, MicroPython and C, compared pixel by pixel in the tests |
| `lvgl_mpy_studio/core/blocks.py` | Blocks: hardware components described by data, read without ever running their code |
| `lvgl_mpy_studio/selftest/` | The IDE driving itself with mouse and keyboard |

## Layer 7: agents

The [MCP server](mcp.md) exposes the same operations as the IDE: create a project, add and
change widgets, write handlers and modules, render a page with the real LVGL, play touch input
on a simulated clock, upload to a board and read its console. [From a prompt to an
app](mcp-demo.md) is a recorded session of 24 tool calls, replayed by a test.

The [case study](case-study-eim-01.md), an industrial monitor of 5 pages and 256 widgets, was
built this way from a prompt.

Two details matter more than the number of tools:

- **Revisions.** Every tool that changes a project can be given the revision the agent last
  read; a file changed in the meantime is reported as a conflict and left untouched. The IDE
  applies the same check when saving. An agent and a person can work on one file.
- **The same renderer.** What an agent sees from `render_page` is the frame the board draws,
  produced by the same MicroPython and LVGL, not a mock-up.

## What this stack does not show yet

A complete device going through all seven layers. The [case study](case-study-eim-01.md) stops
at layer 5: its data are simulated. The blocks for I2C and PWM, which would let it read a real
sensor and drive a real fan, are planned and not written.
