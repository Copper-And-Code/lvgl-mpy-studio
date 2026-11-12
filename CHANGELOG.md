# Changelog

## 0.5.1 — 2026-11-12

### Added

- **Self-test.** `lvgl-mpy-studio selftest` uses the IDE as a person would — toolbox, page, Properties panel, code editor, Save As, simulator and touch — and writes a report with `PASSED` or `FAILED` for each step, with pictures of what failed. `--show` shows the IDE at work. Eight scenarios: the full tour, save and open again, pages, resolution, pictures and fonts, Python modules, Timer and Buzzer, and errors.
- **Print Sources.** **File → Print Sources…** (Ctrl+P) prints the source open in the editor or all the sources of the project, with line numbers, the colours of the editor, wrapped long lines, and a header and footer on each page. It has a preview, and a PDF comes from the system print dialog.

### Changed

- **Upload progress.** Sending an application to a board opens a small window with a bar that follows the bytes sent, the file being written, the time elapsed and an estimate of the time left, and a Cancel button. On boards reached through mpremote the bar moves inside a file by estimate, from the speed of the last upload to that board. It appears when the upload lasts more than a moment. Until now the only sign was a file count in the status bar, which stood still for most of a long upload.
- Changing the resolution, or the board of the project, fits the page to the window again, as **View → Fit to Window** does. Each page is fitted when it is shown; other changes keep the zoom.

### Fixed

- A widget chosen with a double click in the toolbox was placed twice in a project with several pages: once where you clicked, and again at the first click on another page. Found by the self-test.
- The warning about fonts and free RAM appeared by mistake from the second upload on: the memory was read while the previous application was still running. It is now read after the reset, with the display driver loaded.
- When the application did not start after an upload, the warnings found before were lost; they are now shown with the error, in the IDE, on the command line and through MCP.
- The portable Windows package did not start on Windows: it carried a copy of ICU 72 next to Qt, which hid the `icuuc.dll` of the system and lacks the functions Qt asks for. The package no longer includes ICU. Wine did not show the fault, because it starts a program even when imported functions are missing.
- The Windows packages had no icon: the program file, the taskbar and the windows showed a generic one. The windows have the icon on Linux too.

## 0.5.0 — not released

### Added

- **Images.** A picture chosen for an Image widget is converted to PNG, made no larger than the screen and stored inside the project file. It is drawn in the simulator, on boards, in executables, in the browser version and in the C export. MCP tools `add_image` and `remove_image`; `project_info` lists the images. Pictures that cost much memory, and image widgets whose picture is missing, are reported as warnings. Until now a chosen file path was written into the generated code and never drawn, and a project with assets could not be uploaded to a board.
- **Fonts.** A TrueType or OpenType file chosen for the `font` property is stored in the project and converted to LVGL's format for each size in use, by a converter written for the IDE on top of Qt: no Node.js or other tool is needed. Compared with LVGL's built-in Montserrat, made by the official converter from the same file, the metrics are the same and fewer than two pixels in a thousand differ, by one level of sixteen. Kerning is converted too, with the same values wherever the built-in font has it. On upload a warning says when the fonts would take more than half the free RAM of the board. MCP tools `add_font` and `remove_font`. The C export includes them too, loaded from memory, which needs `LV_USE_FS_MEMFS`.
- **From a prompt to an app.** `examples/weather` is a weather station built by an AI agent through the MCP server, with the recorded session of its 24 tool calls; `docs/mcp-demo.md` describes it and a test replays it.
- MCP: `list_widget_types` takes `names_only` and `types` and returns the default values; `list_boards` returns the font sizes of each board.
- A font size the target lacks and characters outside the built-in font are reported as warnings, by the MCP tools and when generating.

### Changed

- **Shorter names on the board and in generated files.** Applications are installed under `/lms_apps` instead of `/lvgl_ide_apps`; the generated modules are `lms_buzzer` and `lms_probe`; the web page loads `lms_web.js`; the markers in exported C are `lms:new-handlers`. An autostart installed by 0.4 is still recognised, and C files exported by 0.4 keep working with their markers. Applications already on a board under the old folder are left there: remove the folder by hand. Module names starting with `lms_` are reserved.
- The ESP32-4848S040 and Waveshare RP2350 profiles list the Montserrat sizes read from the real boards: 14, 16, 24, 32 and 40.
- A new project is named “Untitled”.
- MCP answers are compact JSON instead of indented: an agent reads about half the characters.
- **The product is now LVGL MPY Studio.** The command is `lvgl-mpy-studio` (`lvgl-ide` still works), the Python package is `lvgl_mpy_studio`, and the packages are named `LVGL_MPY_STUDIO-…`. Settings and the `~/.config/lvgl-ide` folder of earlier versions are copied on first start.
- English is the language of the code: interface texts, comments, messages, examples and documents. The Italian interface is unchanged and the Italian documents remain next to the new English manual and web publishing guide.
- Three English interface texts changed: the F5 action is **Start**, the toolbar is **Run toolbar** and a custom board profile is **Custom profile**.
- The examples are `examples/<game>/project.json`, with English names and comments; `tris` is now `tictactoe`.
- The IDE, the command line and the MCP server start in English. Italian is still available under **Settings → Language** and with `--language it`.
- Deleting a container deletes the widgets inside it. Copy, cut and duplicate take them too, and they keep their place inside the copy.
- `lvgl-mpy-studio build` writes to `dist/` next to the project, as the IDE does, when `--output` is not given.
- App packages no longer contain `project.json`.
- A handler set on a page without an event is `SCREEN_LOADED`. An event the object does not have is refused.
- The MCP tool `remove_widget` returns the names of everything it removed.
- The IDE package is 4.7 MB smaller: it ships only the names the code editor completes instead of the whole binding API.
- The Simulator panel no longer has an unused path for running the C build.

### Fixed

- Choosing a picture that is still above 512 kB once converted to PNG raised an error inside the undo step instead of showing a message.
- The free space of an STM32H7 board was reported as zero: it was read from the root instead of the filesystem apps are written to.
- Text in sizes 32 and 40 was drawn at 24 in the simulator and on boards, although the runtime has those fonts. The sizes now come from the target: a board profile can list them in `fonts`, the upload reads them from the board, and a project without a board uses the five sizes of the simulator. The STM32H7_CORE profile lists the five its firmware has.
- The order of the widget declarations in the exported `ui.c` changed from one export to the next.
- Deleting a container left its children on the page at the wrong position.
- Widgets inside a container were checked against the screen with coordinates relative to the container, so `outOfBounds` and the "outside the screen" notice were wrong for them.
- The simulator always started from the first page, while boards started from the initial page of the project.
- `simulate` and visual scenarios could not read a widget the project code never names (`ui.<name>` raised `AttributeError`).
- About eighty error messages reached agents and the command line in Italian whatever the language.
- An unexpected error could end the MCP server.
- After an unexpected error during an upload, every later upload answered `device.session.busy`.
- A traceback of the app on the board containing words such as "resource" or "not found" was reported as a busy or missing serial port.
- A board profile without minimum firmware versions raised an error when the board answered.
- A broken custom board profile file stopped the IDE from starting.
- A simulated wait could block for a very long time when the app stopped answering.
- Uploads over UART are about 4.5 times faster: measured on the STM32H7 board, 100 kB take 22 s.

## 0.4.0 — 2026-11-10

### Added

- **Python modules.** A project can hold its own `.py` modules, which handlers, the general code and other modules import by name (`import utils`).
  - The project tree has a **Python Modules** node. Its context menu offers New, Open, Rename and Delete, and a double click opens a module.
  - Modules are edited in the existing code editor, with undo and redo, highlighting, completion and syntax checks.
  - Module names cannot be paths, MicroPython modules, files the IDE generates or handler names.
  - A module created in the editor starts with `import lvgl as lv` and `import ui`, and a hint explains why they are needed.
  - **What do you want to do?** lists each module like a component: import it, call its public functions, classes and upper-case constants. The open module shows its own functions.
- **Modules in every pipeline.** Modules are included in the simulator, the upload to boards (as bytecode, with precompilation) and the MicroPython export for a board. They are also included in Debug and Release folder builds, in the single-file executables for Linux and Windows, and in the browser version.
  - The generated folder has a `manifest.json` with the ordered list of modules. Every build takes its modules from it, and stops with a clear error if it is missing or inconsistent.
  - A module that was removed or renamed is deleted from the generated folder, together with its bytecode.
  - The C export warns that Python modules are not part of it.
- **MCP tools for modules.** The new tools are `list_modules`, `create_module`, `rename_module` and `delete_module`; `get_code` and `patch_code` take `module` as an alternative to `handler`. `project_info` lists the modules. Existing tools keep their arguments and answers.
- **Project revisions.**
  - `project_info`, `get_code` and `list_modules` return a SHA-256 revision of the project file.
  - Every MCP tool that writes the project accepts `expected_revision` and returns the revision it wrote. A file changed in the meantime is reported as a structured `revision_conflict` error, and nothing is written.
- **Changes made outside the IDE.**
  - Before saving, the IDE checks that the file on disk is still the one it opened or last saved, for example when an MCP agent or the command line wrote it meanwhile. If the file changed, the IDE asks whether to reload it, save a copy, overwrite it or cancel; Cancel is the default. A deleted file can be recreated or saved elsewhere.
  - **Save As** asks before replacing another file.
- **Single-file executable for Windows.** **Run → Build Single-File Executable…** now works on Windows too. The `--for windows` and `--for linux` options build for the other system. A Linux game built on Windows comes as a `.tar.gz`, to keep its execute permission.
- **Games in the browser.** **Run → Open in Browser**, `lvgl-mpy-studio build --web` and `lvgl-mpy-studio web` build a folder with the page, a WebAssembly runtime of MicroPython and LVGL, and the compiled game, ready for a static host. The folder includes an `.htaccess` for Apache and LiteSpeed hosts. The runtime is built by `runtime/build_web.sh`. A publishing guide is available in Italian.
- **Italian user manual,** `docs/manual.it.md`.
- **Project schema 3** for projects with modules. Projects without modules are still written as schema 2, byte for byte.

### Changed

- **Errors in modules.**
  - A syntax error names the module and its line, and is never reported on the handler that imports the module.
  - In a runtime traceback, the line where the error happened comes first in the Errors panel. The handler that led there is marked "called from here".
  - Double-clicking a row opens the module or handler at that line and highlights it.
- **Confirmations before risky module changes.** Renaming or deleting a module that code still imports asks first, with a warning that the old imports will stop with `ImportError`. Imports are never rewritten.
- **Read-only code while running.** While the simulator runs, a bar above the code editor explains why the code is read-only and offers **Stop and Edit**.
- **Resolution sizes.**
  - The resolution menu lists the common sizes 240×240, 480×480, 1024×600 and 1024×1024, even when a board has the same size.
  - Project settings list the common sizes and those of the known boards.

### Fixed

- Runtime errors in the simulator did not appear in the Errors panel. The simulator prints tracebacks on standard output, while the IDE read only standard error. This also affected handler errors in 0.3.
- **Custom…** in the resolution menu raised an error and did nothing.
- The **Change Port**, **Manage Board Profiles**, **Use as Default** and **Remove Default** entries of the destination menu did nothing.
- Boards whose firmware starts a MicroPython shell that needs a second Ctrl+C, such as some ESP32-4848S040 builds, failed every operation with `could not enter raw repl`. The IDE now sends repeated Ctrl+C when it connects, and retries once after that error.

### Known limitations

- **Modules.**
  - Renaming or deleting a module does not update the code that imports it; the IDE warns and lists those places.
  - Modules created through MCP start empty, without the imports the editor adds.
  - The C export does not include Python modules.
  - Projects with modules (schema 3) cannot be opened by 0.3, which refuses them clearly.
- **External changes.**
  - There is no file watcher: the IDE notices a change only when it saves.
  - The revision check is not a lock: a program writing at the very moment of the save can still be overwritten. The same applies to `expected_revision` over MCP.
- **Simulator.** The code is read-only while the simulator runs.
- **Browser version.** It has been checked in Chromium only.
- **Documentation.** The user manual and the web publishing guide are available in Italian only.
