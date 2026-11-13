# Decision log

- New IDE in Python 3.11+ and PySide6 6.12.0 (LGPL), separate from `lvgl-mpy-builder`.
- The core (`core`, `gen`, `build`, `sim`) does not import Qt and is available from the CLI.
- The TypeScript generator was ported to Python, verified with byte-for-byte golden files at commit `5c217fa1536d4c78b01d07a2dbfcc9055fb59cdc`.
- Native Linux x86-64 target; MicroPython 1.29.0, PyDevices `58d18ce`, bindings `7740c2fae0daa10992f5f8fe54acf670a70e2d3b` (LVGL 9.5.0).
- The v2 JSON project keeps the user's Python code; the C target generates stubs and reference comments.
- A single MicroPython unix runtime supports the IDE, SDL and headless backends through `lvsim_io`.
- RGB565 rendering, 800×480 by default; one resolution per project.
- The C target uses the same `lv_conf.h` with `LV_CPYTHON_BUILD`, which selects `LV_STDLIB_CLIB`; the LVGL cache includes the configuration hash. Unused LVGL drivers and C++ shaders are excluded from the build without changing upstream.
- The C spinner uses the same animated arc as the MicroPython generator, not `lv_spinner_create`: this makes rendering identical on the first tick.
- Headless parity tests use `LVSIM_TICK_MS=0`; normal behavior keeps the monotonic clock.
- The MicroPython release profile uses `FROZEN_MANIFEST` and a build cache based on the hash of the generated sources, with no patch to the unix port.
- Packaging uses PyInstaller onedir and AppImage; Qt stays in separate shared libraries. The container test needs access to the Docker socket, and the test on a clean Zorin install is manual.
- Native Windows x86-64 is v1.1 of the IDE and simulator; v1 stays Linux only so it is not slowed down.
- The Windows toolchain is MinGW-w64 cross-compiled from Linux, without MSVC: same GCC family and no toolchain needed on the development PC.
- The simulator transport is TCP on `127.0.0.1` with a session token on both systems, avoiding the divergence between Unix sockets and named pipes.
- User code is stopped with the protocol's `STOP` message and `KeyboardInterrupt`, not POSIX signals.
- The LVGL tick uses the monotonic `lvsim.ticks_ms()` (`CLOCK_MONOTONIC`/`QueryPerformanceCounter`), not the Windows port's system clock.
- Python platform differences are centralized in `lvgl_mpy_studio/platform.py`; the core forbids POSIX APIs and writes UTF-8 text with explicit LF newlines.
- Standalone Windows apps do not open a console: GUI PE subsystem, with stdout and stderr in `<project>.log`.
- For the C target on Windows, only existing MSYS2/w64devkit installations are detected; no portable toolchain is included or installed automatically, and a guide is shown if it is missing.
- The Windows distribution includes both a portable ZIP and a per-user Inno Setup installer in `%LOCALAPPDATA%`; there is no code signing in v1.1.

## Reference divergence

As of 2026-10-28, the public commit above still declares LVGL 9.3 for MicroPython and does not contain the 30/30 runner cited as a prerequisite. The port's golden files therefore describe that generator, not proven 9.5 compatibility. The v2 path uses the APIs at the pin and requires separate runtime checks.

## Compact MicroPython generator (2026-11-06)

- The requirement for output byte-identical to the TypeScript generator is dropped: it verified the port and was not a product requirement. `reference/corpus` remains as a set of projects to generate; the text comparison is replaced by compiling the result and by behavior and pixel parity tests.
- `ui.py` exposes as attributes only the widgets used by user code (`ui.name`) or that own a handler. If the code uses `ui` in any form other than `ui.something`, for example `getattr(ui, ...)`, all of them stay exposed.
- `objects` and `globals()` are gone. Empty handlers generate no code or callback unless code calls them. `load_page`, `load_page_anim`, `get_current_page` and the `PAGE_<NAME>` constants have stable names and are generated only when used; the old names with the project prefix no longer exist.
- Groups of identical constant styles on several objects become shared `lv_style_t` objects, which reduces bytecode and RAM. `add_style` costs more than a single `set_style` during creation, but overall startup improves because there is less source to compile. Suspending refresh with `enable_style_refresh` was tried and rejected: the final recalculation cancels the gain.
- The C generator does not change.

## Non-visual components (2026-11-06)

- Buzzer and Timer live in `lvgl_mpy_studio/core/components.py`, outside `widgets.json`: they are not LVGL objects and the C generator ignores them with a warning.
- `ui.buzzer1` is the `lms_buzzer` module, generated only when the component is present, so there are no extra classes or objects. `ui.timer1` is an `lv.timer`, created only if it has a handler or code uses it; its handler receives the timer as the `e` argument.
- In the simulator the buzzer writes a line `ESC LVSIM_TONE frequency milliseconds` to stdout, which the IDE intercepts and plays: this avoids changing the native protocol and rebuilding the runtimes. Outside the IDE the module stays silent.
- The pin is in the optional `buzzer` key of the board profile (`pin` or `audio`). QtMultimedia is loaded only on the first sound.

## RAM and flash budget (2026-11-06)

- Flash is the sum of the files that would go on the board. RAM is measured by running the project in the headless runtime for 15 iterations of the LVGL loop, so it includes objects created by code, and excludes video buffers.
- The runtime is 64-bit and the boards are 32-bit: RAM is an overestimate, stated in the tooltip and not corrected with unmeasured coefficients.
- Profiles contain no invented capacities: the comparison uses `memoryFree` and `filesystemFree` read at connection and saved in local preferences.

## Editor help and C target (2026-11-06)

- C leaves the selector: it does not run handlers and serves for exporting, so it becomes **Project → Export C Code…**. The export writes only the four portable files to `export_c/` next to the project; `main.c` and `Makefile` are tied to the simulator and are needed only to compile. A project saved with a C destination opens on the Simulator; the CLI keeps `--target c`.
- Suggestions are a child widget of the editor, not a popup: on Wayland the `QCompleter` popup is rejected and does not appear.
- The suggested actions live in `lvgl_mpy_studio/core/actions.py`, and `tests/test_actions.py` runs them all on the real runtime, so the IDE cannot suggest calls that do not exist.

## LVGL preview in the designer (2026-11-06)

- The canvas shows a frame from the headless runtime (`LVSIM_DUMP`), about 15 ms per page, on a copy of the project without user code: a broken handler does not affect the designer.
- `WidgetItem` objects stay above the frame for selection and dragging. While dragging, the frame is re-rendered with the pending geometry, so the real widget follows the cursor with no duplicate; the project changes only on release. The Toolbox drop preview is always drawn by Qt because it is not in the frame yet. Without a frame the IDE uses Qt drawing.
- The frame is recomputed only when the visible project changes, not the code. The option is in the View menu and is on by default.

## Garbage collector in the main thread (2026-11-06)

- Budget and preview work in Python threads, and the garbage collector runs in the thread that allocates: a Qt object in a reference cycle could be destroyed outside the main thread, causing rare segfaults in the event loop. `lvgl_mpy_studio/ui/gc_guard.py` turns off automatic collection and runs it from a main-thread timer.

## Licenses (2026-11-06)

- The IDE is GPL-3.0-or-later, copyright Nunzio Raciti. Generated code is MIT, so users' products do not inherit the GPL.
- The parts that end up in projects or executables are also MIT: `lvgl_mpy_studio/gen/output/`, `native/lvsim/` and `runtime/display_driver.py`. A dependency with a more restrictive license must not enter these parts. See `LICENSING.md`.

## Interface (2026-11-06)

- The IDE keeps PySide6 with the Fusion style and follows the system color scheme. Icons are Material Design Icons through QtAwesome, as the only runtime addition.
- `theme.icon` loads only the `mdi6` font and the packages include only that font: the other fonts bundled with QtAwesome have different licenses and are unused.
- On Wayland the Adwaita decoration plugin draws no border on the sides and bottom, so the window paints one in a 1 px margin. X11 and Windows draw their own.
- The dock layout has a version: a saved layout from an older version is ignored once.

## Live editing on the board (2026-11-06)

- The script re-executes `ui.py` in the namespace of the running module, rebuilds all pages off screen, loads one, and deletes the old ones. It is general: added, removed and moved widgets need no per-property code, at the cost of resetting widget state. The old page stays visible if the build fails.
- Only the design is sent. `upload_key` covers code, Buzzer, Timer, display and board; if it differs from the last upload, the IDE asks for F5, because the board has neither the handlers nor the modules.
- The LVGL tick runs through `micropython.schedule`, so it interleaves between bytecodes in the same thread, not during a C call.
- Measured on the ESP32-4848S040 with a two-widget page: 0.39 s per update, free memory stable over repeated updates.

## Examples at any resolution (2026-11-06)

- The games read the real size with `lv.display_get_default()` when the page loads and place every widget from there, with a unit of 1/240 of the short side. The IDE needs no special mode: picking a board already sets the resolution. The designer still shows the original layout.
- The size cannot be read at module level: in the simulator `app_events` is imported before the display exists.
- The initialization functions clear their lists of LVGL objects, because a live update deletes the old pages and fires `SCREEN_LOADED` again.

## Project id (2026-11-06)

- The app directory on the board was derived from the project name and board, so two projects named the same replaced each other. It now uses `projectId`, a UUID saved in the project. **Save As** to another path creates a new one; a file copied by hand keeps its id and still shares the directory.
- Files without an id keep the name-based directory until the next save, so an unsaved reload does not create a new directory each time. Removing an autostart also accepts the old name-based path.
- Old directories are not deleted: the IDE cannot know whether another project still uses them.

## Scaling to the chosen profile (2026-11-07)

- Changing resolution, by picking a board, updating the profile or in the project settings, scales the project in one undoable step. Each axis scales on its own so the page stays full; shapes can stretch. Spacing props use the smaller factor, and fonts snap to the available sizes.
- Scaling rewrites the saved values, so going to a small screen and back loses precision and font sizes. Undo restores them exactly.
- The points of a Line widget are not scaled.

## LVGL sources in the packages (2026-11-07)

- Packages include only `src/`, the top-level headers, `LICENCE.txt` and `COPYRIGHTS.md` of LVGL: this is what the C target compiles. Tests, demos, documentation and scripts added 150 MB and fonts that the IDE does not use.

## Visual tests (2026-11-07)

- `lvgl-mpy-studio test` uses the same headless render as the designer preview, but runs the project code by default: the screen a user sees also depends on it. A Python traceback is an error even if a frame was drawn.
- Baselines are PNG files, readable in any viewer and in Git, written by a small encoder in `lvgl_mpy_studio/build/visual.py` so the core does not import Qt. The reader accepts only that format.
- Outside `--update`, a missing baseline fails, so a passing run always means a real comparison. `--update` renders twice and refuses unstable pages.
- Version 1 captured each page once after loading. Scenarios with touch input came once the virtual clock made runs identical: see below.

## MCP server (2026-11-07)

- `lvgl-mpy-studio mcp` is a separate stdio process with hand-written JSON-RPC, tested with the official Python client. The tool subset is small and the SDK would add many packages to the executables. The IDE gains only a menu switch, so the server costs nothing while it is unused.
- By the owner's decision the agent has no limits compared to the IDE, board and autostart included, because a person supervises it. The only gate is the menu switch, off by default and read on every call. An unreadable setting counts as off.
- `simulate` drives the runtime over the existing lvsim protocol, acting as a small headless IDE in `lvgl_mpy_studio/sim/session.py`. The runtime needs no change, and the app behaves as it does in the IDE panel. The clock was real at first; it is virtual by default since the next entry, and real only with `clock: "real"`.
- The server works on files, not on the open IDE, so version 1 has no shared undo and needs the project closed in the IDE.

## MicroPython export (2026-11-07)

- The export writes the board files, not the simulator ones: the simulator `display_driver.py` talks to the IDE and cannot run on hardware. In the IDE, a project without a board asks for one, among those of the same resolution, and the choice is not saved in the project. The CLI and the MCP tool cannot ask, so they take a board id and otherwise refuse.
- `export_py/` holds `.py` sources and JSON metadata, no `.mpy` files. MicroPython imports a `.py` before a `.mpy` of the same name, so bytecode next to the sources would be ignored, and its format depends on a firmware the IDE may never have seen. Uploading from the IDE still precompiles.
- Export overwrites its files, unlike the C export, because there is no handler stub to keep. The manifest stores their hashes, so the IDE asks before overwriting a file you changed, the CLI and the MCP tool refuse without an explicit flag, and all of them remove the files the project no longer needs.

## Single-file executable (2026-11-07)

- For sending games on Linux, one file: a prebuilt launcher with the app appended as a ROMFS image, the format MicroPython mounts with `vfs.VfsRom`, followed by its size and a magic. The launcher is the same for every game, so building takes under a second and needs no compiler. Freezing the app into a new MicroPython build was tried first: it works, but needs the MicroPython sources and GCC on the user's computer, which the AppImage cannot ship.
- The launcher reuses the Windows `lvsim_standalone.c` entry point and links a static SDL2 built from source with every backend loaded at runtime. The distribution `libSDL2.a` links about twenty libraries directly, `libdecor` among them, and a missing one would stop the game from starting.
- The entry point sets `sys.executable` from `/proc/self/exe`, so a game started from `PATH` still finds itself, and limits `sys.path` to the app and `.frozen`: MicroPython always puts the current folder first, and a stray `main.py` next to the game would replace it.
- License notices are frozen into the launcher and print with `--licenses`.
- Self-extracting archives were rejected: they start slowly, write temporary files and, on Windows, often trigger antivirus warnings. Windows can follow with the same launcher design.

## Looking inside the simulated app (2026-11-07)

- `simulate` can read and change the app state. The session adds a small module to its own copy of the project and calls it once per main loop iteration, after `lv.timer_handler()`. It reads JSON requests from standard input and answers on standard output with marked lines, which the session removes from the console. The runtime and the lvsim protocol do not change, and neither the board files nor the exports ever contain it.
- Requests run between two frames, in the namespace of the module code, so `lives` or `prepara_ondata()` mean what they mean in the game. `eval` gets `page()` and `objects()` as extra names, without adding them to the module.
- `assert` and `wait_until` stop the script at the first failure, so an agent reads one clear reason instead of a cascade.

## Simulated clock (2026-11-07)

- `simulate` uses a virtual clock by default. The session copy of the app replaces `tick` and `wait` in `display_driver` with a fixed 10 ms step and no sleep, and pauses after each loop iteration until the session asks for more time. Touch input goes through the same channel and lands at an exact simulated time, so a run is repeatable down to the pixel.
- The game code sees the same time: `sys.modules["time"]` becomes a small clock that answers the ticks, the sleeps, `time()` and `time_ns()` with simulated time and passes the rest, such as `localtime()`, to the real module. The step is added in `tick()`, before `lv.timer_handler()`, so callbacks and LVGL see the same instant. `seed` calls `random.seed`.
- No native change was needed: the time source and the touch state both live in the Python `display_driver`, and the session already uses its own copy.
- The real clock stays available for a feel of the frame rate. The limit is 600 simulated seconds against 30 real ones, because the virtual run of a two-minute game takes a few seconds.

## Changing the resolution (2026-11-08)

- A toolbar button changes the resolution in one click. Its menu lists the sizes of the known boards with their names, then common sizes, rotation and a custom size. The project settings dialog stays for the rarer cases. A board of another size is unlinked, with a note in the dialog.
- Nothing moves on its own: every change asks for adapt, stretch or keep, and remembers the last answer. Keep stores `designSize` in each page, only while it differs from the display, so a page can be adapted later from the **Arrange** menu.
- Adapt infers an anchor for each widget, like the Anchor property of Visual Basic, without asking for one. A widget that fills most of its container stretches with it; a small one near an edge stays at that edge; a large block or a widget in the middle keeps its centre in proportion. Sizes and fonts use one factor, so shapes keep their proportions, except on the axis where a widget stretches. Line points scale with their box in both modes. Two refinements came from rendering the examples: a widget drawn on a larger one follows it, as the dot on the Orbita ring, and close siblings move as one group, as the tic-tac-toe grid. Labels grow when their font is clamped to the smallest available size; buttons do not, or they would overlap.
- An editable Anchor property can come later, if inferred anchors turn out not to be enough. The MCP keeps stretch as the default of `set_resolution`, so existing agent scripts do not change.

## Scenarios in visual tests (2026-11-08)

- A scenario is a script of `simulate` steps with a name, a page and a seed, played on the virtual clock. Its screenshots and final screen are compared like pages. The step runner moved from the MCP server to `lvgl_mpy_studio/sim/script.py`, so the test command and the agent share it.
- Scenarios live in `scenarios.json` next to the baselines of each resolution, because touch coordinates depend on it. The MCP `save_scenario` tool writes that file, so an agent can turn a tried `simulate` run into a test.
- `--update` plays a scenario twice and refuses it if the two runs differ, as for pages. Simulated time starts on a fixed date, 1 January 2026, and `localtime()` follows it in UTC, so a clock on screen does not break a baseline, whatever the time zone of the computer. Steps are checked for shape before a scenario is saved or run.

## Portable single-file launcher (2026-11-08)

- Built on Ubuntu 24.04 the launcher needed glibc 2.38, and dozens of its symbols come from 2.34 or later, starting with the threads that moved into libc. Pinning symbol versions was not practical, so `runtime/build_onefile_portable.sh` builds it in an Ubuntu 22.04 container. The result needs glibc 2.34.
- The container builds its own `mpy-cross` in `runtime/out/portable`: the one in `.reference` belongs to the host and would not start inside. Intermediate paths are configurable for the same reason, so the container never mixes its objects with the host build. The final `runtime/out/lvsim-onefile` is replaced on purpose: the portable launcher also runs on the host.
- `runtime/build.sh` still builds the launcher for the host, which is enough to develop. `packaging/build.sh` warns when the launcher would need a newer glibc, so a release does not ship it by mistake.

## Single-file executable for Windows (2026-11-08)

- The Windows launcher reuses the Linux design: the same entry code and boot module, SDL2 linked statically from the MinGW development archive, ROMFS enabled with `MICROPY_VFS_ROM`, and `-static` so that only system DLLs remain. The IDE marks the copy as a GUI program before appending the app.
- The launcher passes its own path in `LVSIM_SELF`, from `GetModuleFileNameA` on Windows and `/proc/self/exe` on Linux, so the boot module finds the appended app in the same way on both. The boot module falls back to `sys.executable`, so a launcher built before this change still works.
- Bytecode does not depend on the system, so `--for windows` builds a Windows game on Linux and `--for linux` the other way round. The Windows build was verified under Wine: the frame matches the IDE render and a stray `main.py` next to the game does not replace it.

## Games in the browser (2026-11-08)

- The MicroPython WebAssembly port builds unchanged with our user C modules: the PyDevices LVGL 9.5 bindings, which were the main risk, compiled with Emscripten 7.0 at the first try, and `lvsim` draws through the Emscripten SDL2 on a canvas. Bytecode is the same format as on the desktop, so the game is the `.mpy` files the IDE already compiles, loaded into the in-memory file system.
- The port already builds with ASYNCIFY. `lvsim_sleep_ms` calls `emscripten_sleep`, and the page starts the game with an asynchronous `ccall`, so the unchanged `while display_driver.poll()` loop gives the browser back control between frames. The default ASYNCIFY stack of 4 KB was too small for an LVGL game; it is 1 MB.
- `display_driver.py` and the simulator buzzer tolerate the missing `os.getenv`. The buzzer prints its tone markers on WebAssembly too, and the page plays them with Web Audio after the first gesture, which browsers require.
- The page needs an HTTP server because browsers do not load JavaScript modules from `file://`. The IDE serves the folder on 127.0.0.1 while it is open; `lvgl-mpy-studio web` does the same from the command line.
- The runtime is about 6 MB and shared by every game. It is built by `runtime/build_web.sh` and not by `runtime/build.sh`, because it needs the Emscripten SDK, about 1 GB, which the CI does not install.

## Changes made outside the IDE (2026-11-10)

- The MCP server and the CLI work on the project file, not on the open IDE. Before this, saving in the IDE silently replaced what an agent had written meanwhile. Now `ProjectDocument` keeps the SHA-256 of the bytes it last read or wrote. `Project.save` returns it and `Project.load_with_revision` computes it from the bytes it parses, so a save by the IDE itself is never taken for an external one.
- Before writing the open file, `save` compares that revision with the file on disk. If they differ, it refuses with `ExternalChangeError`, and the window asks: reload the disk version, save a copy elsewhere, overwrite, or cancel. Cancel is the default; nothing is written without a choice. Overwriting means `save(overwrite_external=True)`.
- A deleted or moved file is a conflict too: saving would bring it back against the wishes of whoever removed it. The window then offers to recreate it or save a copy, with no reload. A file rewritten with the same bytes is not a conflict.
- Save As, and therefore Save a copy, asks before replacing an existing file in the IDE itself, with `QFileDialog.DontConfirmOverwrite`, so the confirmation does not depend on the platform's native dialog. The copy is offered under a free name.
- A reload clears the undo history, as opening a file does. A malformed file on disk fails the reload and leaves the document, its changes and its history untouched.
- This is a check, not a transaction. A program that writes between the check and the atomic `os.replace` is still overwritten; the window is a few milliseconds. No lock files: they stay behind after a crash and behave differently on Windows. No file watcher yet: the IDE notices a change only when saving. A watcher and the `expected_revision` argument for MCP tools are the next steps in `docs/architecture-evolution-v0.4.md`.

## Project format for user modules (2026-11-10)

- User modules are stored in the project file, under a top-level `modules` list of `{id, name, source}`. One file keeps undo, MCP, atomic saving and external-change detection working unchanged. `core/modules.py` `module_files()` is the only reader the pipelines will use, so separate `.py` files can come later behind it.
- A project with modules is written as `schemaVersion: 3`; one without stays at version 2, byte for byte. This was tested on IDE 0.3.0, both the AppImage built on 2026-11-08 through its MCP server and the GUI from `main` (`f0932d8`):
  - version 2 with a `modules` key: 0.3 opens it, edits it, undoes and saves it, and keeps the key intact; but it generates no module file, so the app stops at start-up with `ImportError: no module named 'utils'`;
  - version 3: 0.3 refuses it at once, in the GUI, the CLI and every MCP tool, with "Versione progetto non supportata: 3".
  A clear refusal is better than a project that opens and then fails at run time, and keeping version 2 for projects without modules means 0.3 users lose nothing they could open before. A `requiredFeatures` key would not have helped: 0.3 does not read it.
- Module names are the import name and the file name: lowercase letters, digits and `_`, at most 31 characters, at the root of the app only. That rules out paths, `..` and names that differ only by case, which collide on FAT, the file system of some boards (MicroPython documentation, not tested on our boards). The 31-character limit is a deliberate margin, not a measured file-system limit.
- Refused names: files the IDE generates, anything starting with `lvgl_mpy_studio`, MicroPython modules with their `u` aliases, Python keywords and the names the IDE already reserves, `__` names and handler names. On the simulator runtime, a `time.py`, `json.py`, `random.py`, `asyncio.py` or `machine.py` next to the app replaces the built-in module, while `lvgl` cannot be replaced (tested). A module named after a built-in would break the clock or the game.
- Renaming or deleting a module never rewrites code. It returns the imports still using the old name, as renaming a widget does.

## User modules in every pipeline (2026-11-10)

- `generate_project` writes the modules next to the generated files, verbatim except for line endings, so a traceback names the module's own file and line. It also writes a `manifest.json` with the file hashes and the ordered list of the app's Python modules. `app_modules(directory)` reads that list, and it is the only one: the single file (ROMFS), the frozen Release build, the Debug build and the web version all take their modules from it instead of keeping their own lists.
- The manifest also tells what the previous generation wrote. A module that was removed or renamed is deleted with its `.mpy`, so stale code cannot hide an `ImportError`; files the generator did not write are never touched. Debug builds now drop old `.mpy` files as Release builds already did.
- On the board, modules go into the package, the manifest and the bytecode precompilation, under the same all-or-nothing rule. A syntax error in a module names the module and its line instead of being mapped through the `app_events.py` source map. Stopping the app also forgets the modules loaded from the app folder.
- Live editing treats a module change like any code change: a full upload. The designer preview ignores modules and the schema version, so neither editing a module nor going from version 2 to 3 redraws the canvas.
- `code_usage` also scans the modules. `import ui` on its own line and `from ui import a, b` are understood; any other use of `ui` still exposes everything, the cautious choice. Projects without modules are analysed exactly as before.
- The RAM budget runs the modules as bytecode, as on the board. The C export warns that Python modules are not part of it.
- The simulator panel and the board console list traceback lines from modules with file and line, through `build.compiler.traceback_errors`, shared with the handler mapping.

## MCP tools for user modules, and file revisions (2026-11-10)

- `list_modules`, `create_module`, `rename_module` and `delete_module`, plus `module` on `get_code` and `patch_code` as an alternative to `handler`, call `core/modules.py` and nothing else: names, reserved words, duplicates, references and patching live there once, shared with the future editor. The server only adds what MCP needs, an English "Unknown module" error listing the modules and the syntax check that `set_handler` and `patch_code` already did. A module must compile to be saved.
- Existing tools keep their arguments, required lists and answers; new fields are only added. `get_code` without arguments still returns the shared code under `module`, now with `modules` and `revision` next to it.
- `project_info`, `get_code` and `list_modules` return `revision`, the SHA-256 of the file bytes, as computed by `Project.load_with_revision` (identical to the code in the `external-changes` branch, so both branches agree on the value). Each tool that writes the project file accepts `expected_revision` and returns the `revision` it wrote, so an agent can chain changes without reading again.
- A different revision is a `revision_conflict` error: `isError`, a JSON text and the same object in `structuredContent`, with `expected_revision` and `current_revision` (null for a deleted file). Nothing is written and nothing is retried: the agent reads again and decides.
- The same check also runs without `expected_revision`, between the tool's own read and write, so a save by the IDE during a tool call is never overwritten. Agents that do not know about revisions only see an error in that race, which before was a silent loss.
- It is not a transaction. Between the last check and `os.replace` another program can still write, and its change is lost; the window is the time of one atomic write. Without a lock, which we keep out for the reasons given for the IDE, it cannot be closed. Two MCP servers on the same file follow the same rule.
- `app_modules` now stops with `ManifestError` when the manifest is missing, unreadable, without a module list, names something that is not a plain identifier, or lists a file that is not there. A broken manifest from an older run still never blocks the next generation, which rewrites it.
- The MCP tests found that a version 3 file with widget events was read as if it were version 1, and failed to load: the check was `version == 2`. It is now `version != 1`, so version 3 reads events as version 2 does; the fix belongs with the version 3 format.

## Python modules in the editor (2026-11-10)

- The project tree ends with a **Python Modules** node, always shown so that a module can be created from its context menu: New, and on a module Open, Rename and Delete. Pages keep their positions in the tree. Modules are listed in project order, the order of the manifest, in the tree and in the code editor alike.
- There is still one editor. A module is one more entry of the code panel's object list, `Modulo: utils.py`, next to the general code and the handlers, so highlighting, completion, typing merged into one undo step and syntax checking work as they do for the rest of the code. The panel follows a module by id, so it stays on it across a rename, an undo or a reload.
- Every change goes through `ProjectDocument.execute` and the functions of `core/modules.py`: create, rename, delete and the text itself through `set_module_source`. The name dialog uses `validate_module_name`; an invalid name is explained and offered again for correction. Delete asks for confirmation and lists the code still importing the module; undo brings it back.
- Rename and delete never rewrite imports. When code still imports the module, both ask first with a warning that lists it and names the risk, ImportError, with No as the default; afterwards the references also go to Output, with a status bar message. Renaming a widget or a page now also warns about modules that use the old name, still without rewriting them.
- A syntax error in a module reads `utils.py, riga 3: SyntaxError: invalid syntax` and underlines the line; it never appears on the handler that imports the module. `parse_compiler_errors` now keeps the error line printed after the location as `detail`; handler messages are unchanged.
- In a traceback, the last frame in user code is where the error happened (`origin`): the Errors panel lists it first, and the frames that led there, such as the handler that called the module, are marked "called from here". Activating a module row opens the module at its line.
- The simulator prints tracebacks on stdout, not stderr, and a read can cut one in two. The window first parsed only stderr, so no row appeared and nothing could be clicked; the tests had fed the text in directly and missed it. Output is now buffered until a traceback is complete, whatever the stream, each row shows the exception and keeps the whole traceback as a tooltip, and the Errors panel comes to the front, since it sits behind Output.
- An error in a handler does not stop the app, so the code stays read-only while the simulator runs, as before. That looked like a broken editor, and read-only text draws no cursor, so a row opened from the Errors panel seemed to land nowhere. While the simulator runs, a bar above the editor now says so, with a Stop and Edit button. The line of an opened error is highlighted, which shows in read-only text too, and stays until the code is edited.
- **What do you want to do?** lists each module like a component: Import the module, its public functions with their arguments, classes and upper-case constants. They are read with `ast`, without running the module; with a syntax error the top-level `def` lines remain. Double-clicking inserts the call, with the cursor between the brackets when there are arguments. The open module shows its own group instead, expanded, as This module, with calls without the module prefix; leaving it out made a new module look as if the panel had not updated. While a module is edited, the list follows its functions after a short pause.
- Generation never writes back into the project: a file edited by hand in the generated folder is replaced by the module's source at the next run.
- A module is a file of its own, so `ui` and `lv` are not defined in it as they are in handlers, and the first user test stopped on `NameError: name 'ui' isn't defined`. A module created from the editor therefore starts with `import lvgl as lv` and `import ui`, the imports of the generated handlers, and a hint under the editor says so while a module is open. `create_module` in `core/modules.py` and over MCP still starts empty, so existing agents see no change.

## The Device Console as a terminal (2026-11-13)

- The console sends each key as it is typed, as a serial terminal does, instead of a line at a time. The first program that needed it is the Linux-like shell of `mpy-lvgl-boards/examples/shell`, with history, Tab completion and full-screen editors; the plain REPL gains its history and completion too.
- The screen is `core/vt.py`, written here in plain Python rather than taken from a library such as pyte. It follows `ansiterm.py`, the terminal that the same shell draws on a board's display, sequence by sequence, so a program looks the same on the board and in the IDE; it adds the history of the lines scrolled off and Unicode. No new dependency reaches the packages. Its tests compare the screen cell by cell.
- The console no longer runs `mpremote repl`. On Windows that command reads the keyboard of its own console window, which a GUI program does not have, so typed keys could not reach the board. The port is opened with mpremote's own `SerialTransport`, so the lines DTR and RTS behave as with every other mpremote command, quirks of the CP210x on Windows included. The STM32H7 boards keep their UART transport, which stays open; the console leaves the raw REPL with Ctrl-B only after an IDE command left it there.
- The console is live whenever the board is connected and the IDE is idle, not only while an app runs. Each IDE operation stops it first and it starts again afterwards, as the mpremote commands already took and gave back the port. An empty read is a read timeout, not the end: only an error of the port ends the console, and the window is told.
- Ctrl+C and the other Ctrl keys belong to the board, also over the menu shortcuts of the window; copy and paste are on Ctrl+Shift+C and Ctrl+Shift+V. Keys are written in pieces of 64 bytes with a short pause, so a long paste does not overflow the receive buffer of a board.
- Not changed: the IDE's commands over the raw REPL, the MCP tool `device_read_console`, which still reads without typing, and the traceback mapping, which reads the same text as before.

