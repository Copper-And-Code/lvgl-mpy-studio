# Building, testing and packaging

Reference for whoever works on LVGL MPY Studio. The [user manual](manual.md) describes the IDE itself.

## From the sources

You need Python 3.11+, a C compiler, `pkg-config`, CMake, SDL2 with its development headers and, for SDL windows without a display, `xvfb`. CMake builds the static SDL2 of the single-file executable; the first `runtime/build.sh` also downloads the SDL2 sources.

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
./runtime/build.sh
.venv/bin/lvgl-mpy-studio
```

## CLI

```bash
lvgl-mpy-studio generate project.json --target micropython
lvgl-mpy-studio generate project.json --target c
lvgl-mpy-studio run project.json --target micropython
lvgl-mpy-studio run project.json --target c
lvgl-mpy-studio build project.json --target micropython --profile debug
lvgl-mpy-studio build project.json --target micropython --profile release
lvgl-mpy-studio build project.json --target c
lvgl-mpy-studio test project.json --update
lvgl-mpy-studio test project.json
```

On Linux, `build` creates `dist/<project>-x86_64/run.sh`. The MicroPython `debug` profile uses the runtime with `.mpy` modules, and `release` freezes the app with `FROZEN_MANIFEST`. The C target produces a native binary. On Windows, the Debug profile creates `dist/<project>-win64/<project>.exe` and a ZIP, with SDL2 included and no console; stdout and errors go to `<project>.log`. The C target requires an [MSYS2 or w64devkit toolchain](windows-c.md); MicroPython Debug does not. All launchers use SDL and support:

```bash
dist/<project>-x86_64/run.sh --selftest
```

The self-test draws a headless RGB565 frame to `selftest.raw` and exits. C builds need GCC, Make and the SDL2 headers; MicroPython debug builds need no toolchain to run.

To send a game to someone, **Run → Build Single-File Executable…** or `lvgl-mpy-studio build project.json --profile release --single-file` creates `dist/<project>`, about 5 MB, or `dist/<project>.exe` on Windows: one file with the app, the runtime and SDL, which starts with a double click. `--for windows` or `--for linux` builds for the other system: the app inside is the same bytecode, so a Windows game can be built on Linux and the other way round. A Linux game built on Windows comes as `<project>.tar.gz`, because Windows files have no execute permission: extract it and start the game. It is a prebuilt launcher with the compiled app appended, so building takes under a second and needs no compiler, in the AppImage too. SDL is linked statically and loads X11, Wayland and audio from the system when they are present. `--licenses` prints the third-party notices that the folder build keeps in `licenses/`, and `--selftest` works as above. A Windows game has no console, so both write to `<project>.log` next to it, and it works in its own folder, like the folder build. Its launcher comes from `runtime/build_onefile_windows.sh`, which `runtime/build_windows.sh` runs, and needs only the DLLs that ship with Windows. The launcher comes from `runtime/build_onefile.sh`, which `runtime/build.sh` runs, and needs the glibc of the computer that built it. To send games to older systems, build it once with `runtime/build_onefile_portable.sh`, which compiles in an Ubuntu 22.04 container through Docker: games then need glibc 2.34 or later, so they start on Ubuntu 22.04, Debian 12, Fedora 35, Linux Mint 21 and newer. `packaging/build.sh` warns when the launcher would need a newer glibc.

## Games in the browser

**Run → Open in Browser** builds `dist/<project>-web/` and opens it in the browser through a small local server. The folder holds the page, a WebAssembly runtime of about 6 MB with MicroPython and LVGL, and the compiled game: copy it to any static host, such as GitHub Pages, to share the game with a link. The [publishing guide](publish-web.md) explains the steps.

## Visual tests

`lvgl-mpy-studio test` draws every page with the real runtime, project code included, and compares it pixel by pixel with a PNG baseline in `visual/<width>x<height>/` next to the project. Run it once with `--update` to write the baselines and commit them.

When a page differs, the command exits with status 1 and writes `<page>.actual.png` and `<page>.diff.png`, with the changed pixels in red. A missing baseline is also a failure, so CI cannot pass by accident. `--threshold` allows a number of different pixels per page, `--page` selects pages, `--baseline` picks another folder, and `--design-only` skips the project code. Add `*.actual.png` and `*.diff.png` to `.gitignore`.

Each page is captured once, right after it loads. To test touch input, add scenarios to `visual/<width>x<height>/scenarios.json`, next to the baselines, because coordinates depend on the resolution:

```json
{"scenarios": [{"name": "launch", "page": "main", "seed": 3, "steps": [
  {"action": "tap", "x": 512, "y": 300}, {"action": "wait", "ms": 1500},
  {"action": "screenshot", "label": "ball"}, {"action": "assert", "expr": "lives == 3"}]}]}
```

A scenario plays the same steps as the MCP `simulate` tool on the virtual clock, so every run is identical, dates and times included: simulated time always starts on 1 January 2026. Each `screenshot` step and the final screen become baselines named `<scenario>@<label>.png`. A failed `assert` or a Python traceback fails the scenario. `--scenario` chooses scenarios; with only `--page` or only `--scenario`, the other kind is skipped. `--update` refuses a page or a scenario that changes between two runs.

## C code

**Project → Export C Code…** writes `ui.c`, `ui.h`, `ui_events.c` and `ui_events.h` to `export_c/` next to the project. They depend only on `lvgl.h`, so you can copy them into any LVGL project. Handlers are stubs with the original Python as a comment, and there is no automatic Python to C translation. Your code in `ui_events.c` is kept on later exports.

**Project → Export MicroPython Code…** writes the sources for the project's board to `export_py/` next to the project, and in the IDE asks for a board if the project has none. The simulator files in `build/` would not run on a board. Copy the files to a folder on the board and run `app_main.py`: the firmware must provide LVGL and `display_driver`. Export overwrites the files, and the IDE asks first if you changed any of them. `lvgl-mpy-studio generate --target board` is the command-line form: it needs a board in the project or `--board-profile`, and refuses to overwrite changed files without `--force`.

## Simulator

MicroPython and C share `lvsim_io`: loopback TCP with a token in the IDE panel, a standalone SDL window, or a headless dump. The framebuffer is RGB565 and the protocol is documented in `native/lvsim/PROTOCOL.md`. For deterministic headless comparisons, `LVSIM_TICK_MS=0` fixes the tick delta; normal use does not need it.

## Limits of the tool

- Supported platforms: Linux and Windows 10 22H2/11 x86-64, RGB565.
- User code is Python. C boards are not supported yet: only MicroPython can be uploaded to a board.
- The designer does not run your code, so objects created by code do not appear on the canvas.
- The RAM budget is measured in the 64-bit simulator, so it is an overestimate for 32-bit boards.
- Built-in Montserrat fonts: 14, 16, 24, 32 and 40 in the simulator and in C; on a board, those its firmware has. Any other size needs a font added to the project.
- Images from the filesystem require a dedicated LVGL driver.

## Tests

```bash
QT_QPA_PLATFORM=offscreen .venv/bin/pytest -q
```

The suite covers generation, fuzzing, the runtime, the GUI, the protocol, all 30 widgets and MicroPython/C pixel parity. The tests use a temporary configuration folder and never open serial ports. The whole suite takes about ten minutes; without `tests/test_windows_c.py` and `tests/test_parity.py`, about four. A CI workflow for Linux and Windows exists and is switched off while the repository is private.

```bash
.venv/bin/lvgl-mpy-studio selftest
```

The self-test opens the real IDE and drives it through nine scenarios; see the [manual](manual.md#self-test).

## Packages

Linux:

```bash
.venv/bin/pip install -e '.[packaging]'
./packaging/build.sh
```

This produces `dist/LVGL_MPY_STUDIO-x86_64.AppImage`. On Windows, from PowerShell with Python and Inno Setup 6:

```powershell
python -m pip install -e '.[packaging]'
powershell -ExecutionPolicy Bypass -File packaging/build_windows.ps1
```

This produces `LVGL_MPY_STUDIO-<version>-win64.zip` and `LVGL_MPY_STUDIO-<version>-Setup-win64.exe`. The installer uses `%LOCALAPPDATA%` and does not require administrator rights.

From Linux, after building the Windows runtimes, you can also build a package with embeddable Python 3.12.10:

```bash
./packaging/build_windows_portable.sh
```

This produces `dist/LVGL_MPY_STUDIO-<version>-portable-win64.zip`. Extract the whole archive and start `LVGL_MPY_STUDIO.exe`; Python does not need to be installed. `LVGL_MPY_STUDIO_console.bat` is available for diagnostics.

Qt stays in separate shared libraries. Licenses and sources are listed in `packaging/NOTICE.txt` and `THIRD_PARTY.md`.

Binaries are not signed: SmartScreen may ask for **More info → Run anyway**.

Pinned versions: MicroPython 1.29.0, LVGL 9.5.0, PySide6 6.12.0. See `docs/target.md` and `docs/decisions.md`.
