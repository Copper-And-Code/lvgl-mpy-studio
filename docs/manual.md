# LVGL MPY Studio manual

LVGL MPY Studio is a visual environment for building graphical interfaces with [LVGL](https://lvgl.io) and MicroPython, in the style of Visual Basic: you draw pages by dragging controls, write a few lines of Python for their events and try everything in a simulator that uses the same LVGL as the board. When you are ready you upload the app to a board, build an executable to send to others, or export the code.

This manual describes version 0.4. For details on boards see the [board guide](boards.md), for AI agents the [MCP server guide](mcp.md). The manual is also available [in Italian](manual.it.md).

## Contents

1. [Installing and starting](#1-installing-and-starting)
2. [Your first project in five minutes](#2-your-first-project-in-five-minutes)
3. [The window](#3-the-window)
4. [Pages](#4-pages)
5. [Widgets and components](#5-widgets-and-components)
6. [Drawing the page](#6-drawing-the-page)
7. [Resolution](#7-resolution)
8. [Writing code](#8-writing-code)
9. [The simulator](#9-the-simulator)
10. [Working with a board](#10-working-with-a-board)
11. [Memory: flash and RAM](#11-memory-flash-and-ram)
12. [Distributing and exporting](#12-distributing-and-exporting)
13. [Visual tests](#13-visual-tests)
14. [Command line](#14-command-line)
15. [AI agents](#15-ai-agents)
16. [Keyboard shortcuts](#16-keyboard-shortcuts)
17. [Common problems](#17-common-problems)

## 1. Installing and starting

### Linux

Download `LVGL_MPY_STUDIO-x86_64.AppImage`, make it executable and start it:

```bash
chmod +x LVGL_MPY_STUDIO-x86_64.AppImage
./LVGL_MPY_STUDIO-x86_64.AppImage
```

Nothing else needs installing: Python, Qt, the simulator and the MicroPython compiler are inside the file.

### Windows

Extract the **whole** folder `LVGL_MPY_STUDIO-<version>-portable-win64.zip` and open `LVGL_MPY_STUDIO.exe`. Python does not need installing. If the IDE does not start, `LVGL_MPY_STUDIO_console.bat` starts it with a console that shows the errors.

The executables are not signed: at the first start Windows SmartScreen may show a warning. Choose **More info → Run anyway**.

There is also an installer (`LVGL_MPY_STUDIO-<version>-Setup-win64.exe`) that installs to `%LOCALAPPDATA%` without administrator rights.

### Language and theme

The IDE starts in English and is also available in Italian: **Settings → Language**. The theme follows the system, light or dark.

## 2. Your first project in five minutes

Let us build a page with a button that counts taps.

1. **File → New** (Ctrl+N). The project starts with an empty page called `main`.
2. From the **Toolbox** on the left drag a **Label** onto the page, then a **Button**. While dragging you see the control on the page, already aligned to the grid.
3. Select the label: in the **Properties** panel on the right change `text` to `Taps: 0`. The label is named `label1`, the button `button1`.
4. **Double-click the button**. The **Code** tab opens on the handler of its main event, `button1_clicked`, as in Visual Basic.
5. Type:

   ```python
   global taps
   taps += 1
   ui.label1.set_text("Taps: %d" % taps)
   ```

6. At the top of the **Code** tab choose **(General)** and type `taps = 0`: this is the module code, run once at start-up.
7. Press **F5**. The **Simulator** tab opens: click the button and the number goes up.
8. **File → Save** (Ctrl+S). The project is a single `.json` file.

If you do not remember how to change a text or read a value, look at the **What do you want to do?** box next to the editor: a double click inserts the right code. See [section 8](#8-writing-code).

## 3. The window

| Area | What it holds |
|---|---|
| **Toolbar** | New, Open, Save, Undo, Redo, Grid, zoom, the **resolution** button (for example `480×480`), the **run target** selector (Simulator or a board), **Start** and **Stop** |
| **Toolbox** (top left) | The widgets to drag onto the page, by category, with a search box |
| **Project** (bottom left) | The pages and, under each, its widgets and components, then the **Python Modules**. The right-click menu manages pages and modules |
| **Central area** | One tab per page, the **Code** tab and the **Simulator** tab |
| **Properties** (right) | The properties of the selected widget, **By Category** or in alphabetical order, and the **Events** tab |
| **Bottom panels** | **Output** (messages), **Errors** (a double click goes to the line of code), **Components** (Buzzer and Timer of the page) and **Device Console** (REPL of the board) |
| **Status bar** | Messages, the flash and RAM **budget** and, if a board is connected, its state with the **Disconnect** button |

Panels can be moved and detached; **View** brings them back if you close them.

## 4. Pages

A project has one or more pages, like the forms of Visual Basic. You manage them from the **Project** menu or by right-clicking a page in the **Project** tree:

- **Add Page**, **Rename Page**, **Delete Page**.
- **Set Initial Page**: the one shown when the app starts.

In code each page has a constant: the page `Game` is `ui.PAGE_GAME`. To go to another page:

```python
ui.load_page(ui.PAGE_GAME)
```

When you rename a page its handlers follow it; if the code still uses the old `PAGE_…` constant, the IDE tells you in the output.

Every page has the **SCREEN_LOADED** event, raised when the page appears: it is the right place to prepare the state, for example to reset a game. You find it in the **Code** tab by choosing the page as the object.

## 5. Widgets and components

### Widgets

| Category | Widgets |
|---|---|
| **Basic** | Button, Label, Panel |
| **Input** | Slider, Switch, Checkbox, Text Area, Dropdown, Roller, Spinbox, Keyboard |
| **Display** | Arc, Bar, LED, Spinner |
| **Data** | Chart, Scale, Table |
| **Media** | Image, Image Button |
| **Container** | Button Matrix, Calendar, Line, List, Message Box, Span |
| **Navigation** | Menu, Tab View, Tile View, Window |

Each widget has a name that is unique in the project, for example `button1`, which you use in code as `ui.button1`. You change the name in the **Properties** panel; the handlers follow it, and if the code still uses the old name the IDE tells you where.

A widget can sit inside another, such as a **Panel**: drag it onto the container. Its coordinates become relative to the container. Deleting, copying or duplicating a container takes the widgets inside it too.

### Images

To show a picture, drag an **Image** onto the page and, in **Properties**, press the **…** button next to `src` and choose a file. The picture becomes part of the project:

- it is converted to PNG, and made smaller if it is larger than the screen;
- it is stored inside the project file, so the project is still one file to copy or send;
- it goes wherever the project goes: simulator, board, executables, browser version and C export.

The picture has a name, such as `logo.png`, shown in `src`: type the same name in another Image to show it again. One Undo takes back both the choice and the picture.

On a board a picture costs memory: its PNG bytes, plus about 4 bytes per pixel while it is on screen. A 100×100 icon needs about 40 kB; a full 480×480 background about 900 kB, more than many boards have free. The output lists the pictures that are heavy, and the image widgets whose picture is not in the project.

### Fonts

Text is drawn with Montserrat, the font built into LVGL, in the sizes the target has (see [Resolution](#7-resolution) and the board guide). To use another font, or a size the board lacks, add a font to the project: in **Properties**, press **…** next to `font` and choose a `.ttf` or `.otf` file. Then set `fontSize` to any size.

- The font file is stored inside the project file. Type its name in the `font` of another widget to use it again.
- When the code is generated the font is converted for each size in use, with the printable ASCII characters and the characters of the widgets that use it. Text set from code can use those characters; a character the font does not have is listed in the output.
- The glyphs are the same LVGL's own converter would make. Kerning, the fine spacing between particular pairs of letters such as “AV”, is converted too.
- On a board each converted size costs memory, roughly two and a half times its size: about 30 kB for ASCII at 24 pixels. On upload the IDE warns when the fonts would take more than half the free RAM of the board. The C export includes the fonts of the project and loads them from memory, which needs `LV_USE_FS_MEMFS` in `lv_conf.h`.

### Components

Components are not visible on the page: they appear in the **Components** panel at the bottom.

- **Buzzer**: it sounds on the board and in the simulator, through the computer speaker.
  - `ui.buzzer1.beep(880, 60)` plays 880 Hz for 60 milliseconds.
  - `ui.buzzer1.tone(440)` plays until you call `ui.buzzer1.off()`.
  - On a board the sound goes where the profile says: a pin, or a speaker. If the profile has no buzzer, the calls do nothing.
- **Timer**: it raises its **TICK** event every `period` milliseconds.
  - Properties `period` and `enabled` (whether it starts on its own).
  - In code: `ui.timer1.pause()`, `ui.timer1.resume()`, `ui.timer1.set_period(500)`.
  - It is the right way to do animations and games: a `while` loop in the code would block the interface.

## 6. Drawing the page

- **Adding**: drag a widget from the Toolbox onto the page. The grid (**View → Grid**) aligns it.
- **Moving and resizing**: drag the widget or its handles. For exact values use `x`, `y`, `width` and `height` in the **Properties** panel.
- **Selecting several**: drag a rectangle on the empty page, or hold Ctrl while clicking.
- **Copying**: Cut, Copy, Paste, **Duplicate** (Ctrl+D) and Delete, also from the right-click menu.
- **Arrange**: with two or more widgets selected you can align them left, centre, right, top, middle or bottom, and distribute them horizontally or vertically.
- **Drawing order**: **Bring to Front** (Ctrl+]) and **Send to Back** (Ctrl+[). Widgets drawn later cover the earlier ones.
- **Real LVGL Preview** (**View**): the page is drawn by the real LVGL, with the fonts and styles you will see on the board, instead of the designer's approximation.
- **Zoom**: Ctrl++ and Ctrl+−; **Fit to Window** with Ctrl+0.
- **Undo and Redo** apply to every change, code included.

## 7. Resolution

The resolution is that of the screen you draw for, and it is the same in the simulator. After a change the page is fitted to the window again. You change it with one click from the button in the toolbar, for example **480×480**:

- **Board**: the resolutions of the known boards, with their names.
- **Common**: 240×240, 480×480, 1024×600 and 1024×1024.
- **Rotate**: swaps width and height.
- **Custom…**: any width and height.

When the resolution changes, the IDE asks what to do with the widgets. Nothing moves on its own:

- **Adapt** keeps proportions: circles and squares stay so. Each widget follows what it sits near: an edge, the centre, the widget it is drawn on, or the group it belongs to, such as a grid of buttons. Widgets that fill almost the whole width, such as a background, grow with the screen; labels grow if their font cannot get smaller. It works towards larger and smaller screens.
- **Stretch** scales each axis on its own: the page stays full, but shapes are distorted.
- **Leave them where they are** changes only the screen. Each page remembers the resolution it was drawn for, and later **Arrange → Adapt Page to Resolution…** adapts it, one page at a time.

The choice is remembered for the next time, and Ctrl+Z undoes everything at once. On a small, crowded page something may overlap: widgets that end up outside the screen are listed in the output.

If the project is tied to a board with another resolution, the board is unlinked and the project goes back to the simulator; the dialog tells you first.

**Project → Project Settings…** offers the same resolutions, plus the board profile.

Code can read the real resolution, which helps a game fit any screen:

```python
width = lv.display_get_default().get_horizontal_resolution()
height = lv.display_get_default().get_vertical_resolution()
```

## 8. Writing code

### How it works

As in Visual Basic, each event of a widget has a **handler**: a Python function that runs when the event happens. In the **Code** tab:

- on the left you choose the **Object**: a widget, a page, a component, or **(General)**;
- on the right the **Procedure**, that is the event: `CLICKED`, `VALUE_CHANGED`, `PRESSED`, `RELEASED`, `LONG_PRESSED`, `SCREEN_LOADED`, `TICK` and others.

When you choose an event that has no code yet, the IDE creates the handler. A double click on a widget in the designer opens its main event directly: `CLICKED` for a button, `VALUE_CHANGED` for a slider or a switch, `TICK` for a timer.

You write only the **body** of the handler: the IDE wraps it in `def button1_clicked(e):`. The parameter `e` is the LVGL event, if you need it.

### (General)

The code of **(General)** is the module: it runs once, at start-up, before the first page appears. Put shared variables, constants and your functions there. Inside a handler, changing a module variable needs `global`, as in any Python program:

```python
# (General)
score = 0

def add(points):
    global score
    score += points
    ui.points.set_text(str(score))
```

### Python modules

When the code grows you can split it into **modules**: `.py` files of the project, which handlers, the **(General)** code and other modules use with `import`.

1. In the **Project** panel, right-click **Python Modules** and choose **New Python Module…**.
2. Give it a name, for example `game`: lower-case letters, digits and `_`. You cannot use the names of MicroPython modules, such as `time` or `json`, nor those of the files the IDE creates, such as `ui` or `main`, nor the name of a handler. If the name is not valid, the IDE explains why and proposes it again.
3. The module opens in the code editor, already with `import lvgl as lv` and `import ui`. A module is a file of its own: `ui` and `lv` do not arrive on their own as in handlers, and everything it uses must be imported.

```python
# game.py
import lvgl as lv
import ui


def show(text):
    ui.label1.set_text(text)
```

Then, in a handler or in **(General)**:

```python
import game
game.show("Hello from the module")
```

A double click on a module in the tree opens it; a right click **renames** or **deletes** it. The IDE never rewrites `import` lines: if the code still imports the module, before renaming or deleting it the IDE warns that those imports will stop with `ImportError` and lists where they are. Undo (Ctrl+Z) puts everything back.

Modules go wherever the project goes: to the simulator, to the board as bytecode, into executables and into the browser version. The C export does not include them, and says so.

### Using widgets

Each widget is `ui.<name>`, and its methods are those of LVGL. Some examples:

```python
ui.label1.set_text("Hello")                        # change the text of a label
ui.button1.get_child(0).set_text("OK")             # change the text of a button
value = ui.slider1.get_value()                     # read a slider
on = ui.switch1.has_state(lv.STATE.CHECKED)        # read a switch
ui.label1.add_flag(lv.obj.FLAG.HIDDEN)             # hide a widget
ui.label1.remove_flag(lv.obj.FLAG.HIDDEN)          # show it
ui.button1.add_state(lv.STATE.DISABLED)            # disable it
```

### What do you want to do?

You do not need to remember the LVGL API. Next to the editor the **What do you want to do?** box lists, for each widget, the most common actions: change the text, read the value, hide, disable, open this page, read the screen width and so on. Search for an object or an action in the box at the top and double-click: the right code is inserted in the editor, with the cursor on the value to change. Modules appear here too, like components: **Import the module**, its functions, classes and upper-case constants. In the open module the **This module** group lists its functions, to be called without the name in front.

In the editor, after `ui.` or `ui.label1.`, **Ctrl+Space** shows suggestions.

### Errors

Syntax errors appear in the **Errors** panel when you start the app, and under the editor while you type; an error while running appears with its exception, and hovering over the line shows the whole traceback. A double click goes to the right handler or module and line, which is highlighted, even if the error happened on the board.

If the error starts in a module, the first line is that of the module; the handler that called it follows, marked **called from here**.

### Printing

**File → Print Sources…** (Ctrl+P) prints the source open in the editor, or all the sources of the project: the general code, the handlers written as the functions they become, and each module, each starting on a new page. Pages carry the project and source names, the date and the page count; lines are numbered and coloured as in the editor, and a long line wraps instead of being cut. **Preview…** shows the pages first. To get a PDF, choose to print to a file in the system print dialog.

## 9. The simulator

- **F5** (**Run → Start**) starts the app in the **Simulator** tab, with the real LVGL and the real MicroPython.
- **Shift+F5** stops it, **Run → Restart** starts it again.
- The mouse acts as a finger, the keyboard works and the Buzzer sounds from the computer speaker.
- The `print` calls of your code appear in the **Output** panel.

While the simulator is running the project is read-only: a bar above the editor says so, and the **Stop and Edit** button stops the app. An error in a handler does not stop the app, so after an error the simulator is usually still running.

## 10. Working with a board

The [board guide](boards.md) explains everything in detail; here is the essential path.

1. Connect the board by USB. It needs a MicroPython firmware with LVGL and the display driver; the requirements of each board are in the guide.
2. In the selector next to **Start** choose the board. The project resolution becomes that of the board, and the IDE asks how to adapt the widgets, as in [section 7](#7-resolution).
3. Press **F5**: if there is only one serial port it is used, otherwise the IDE asks once. The app is uploaded and run; the board console appears in **Device Console**, where you can also type commands to the REPL.
4. **Shift+F5** stops the app. **Disconnect** in the status bar frees the port for other programs.

Other entries of the **Device** menu:

- **Live Editing**: with the app running on the board, every change to the page appears on the board in under a second, without uploading everything again. Code changes need F5.
- **Upload Project** copies the app without starting it; **Upload and Run** copies and starts it.
- **Device Information**: firmware, LVGL version, memory, touch and compatibility with the profile.
- **Install Autostart…**: the app starts on its own when the board powers up. **Remove Autostart…** restores the earlier launcher, saved by the IDE.
- **Manage Board Profiles…**: profiles describe display, touch, buzzer and requirements of each board.

Each project has its own identifier, so on the board it goes to a separate folder and does not overwrite other apps, even with the same name.

In the run target selector, **Use as default for new projects** makes new projects start with that board and its resolution.

## 11. Memory: flash and RAM

In the status bar the IDE shows how much **flash** the compiled app takes and how much **RAM** it uses at start-up, updated as you work. With a board chosen, the values turn yellow or red as you get near its limits.

RAM is measured in the simulator, which is 64-bit: on 32-bit boards real use is lower.

## 12. Distributing and exporting

### Folder executable

**Run → Build Executable…** creates in `dist/<project>-x86_64/` (or `-win64` on Windows) a folder with the game, the runtime and the licences. On Linux it starts with `run.sh`, on Windows with the `.exe`.

### Single-file executable

**Run → Build Single-File Executable…** creates **one file**, about 5 MB, to send to whoever only needs to use the app: `dist/<project>` on Linux, `dist/<project>.exe` on Windows. It opens with a double click, with nothing to install.

- On Linux it starts on Ubuntu 22.04, Debian 12, Fedora 35, Mint 21 and later.
- On Windows it uses only system libraries. It has no console: messages and errors go to `<project>.log`, next to the game.
- `--licenses` shows the licences of the included components, `--selftest` draws a frame without opening the window.
- From the command line you can build the file for the other system: `--for windows` builds the `.exe` on Linux, `--for linux` builds the Linux file on Windows. On Windows the Linux file comes as `<project>.tar.gz`, because Windows has no execute permission: extract it and start it.

### Browser version

**Run → Open in Browser** builds the web version of the game in `dist/<project>-web/` and opens it in the browser. It is the same app, with the real LVGL and the real MicroPython compiled to WebAssembly: you play with the mouse or a finger, and the Buzzer sounds from the browser after the first touch, because browsers do not let a page play sound before a gesture.

To share the game with a link, copy the whole folder to a host, for example Hostinger, GitHub Pages or Netlify: the guide [Publishing games on the web](publish-web.md) explains the steps, also for several games together. The page does not work when opened directly as a file, with a double click on `index.html`: the browser wants a web address. That is why the IDE opens it through a small local server, active while the IDE stays open.

### MicroPython code for a board

**Project → Export MicroPython Code…** writes to `export_py/`, next to the project, the files for the board of the project, to copy by hand or to integrate into another project. If the project has no board, the IDE asks which one to use. If you changed an exported file, the IDE asks before overwriting it.

### C code

**Project → Export C Code…** writes to `export_c/` the files `ui.c`, `ui.h`, `ui_events.c` and `ui_events.h`, which depend only on `lvgl.h` and work in any LVGL project in C. The handlers are empty functions with your Python as a comment: you write the C code in `ui_events.c`, and the IDE keeps it at later exports.

## 13. Visual tests

Visual tests check that pages stay the same while the project changes.

```bash
lvgl-mpy-studio test project.json --update   # the first time: writes the reference images
lvgl-mpy-studio test project.json            # afterwards: compares pixel by pixel
```

The reference images are in `visual/<width>x<height>/` next to the project. If a page changes, the command fails and writes `<page>.diff.png` with the changed pixels in red.

To test touches too, add **scenarios** in `visual/<width>x<height>/scenarios.json`:

```json
{"scenarios": [{"name": "launch", "page": "main", "seed": 3, "steps": [
  {"action": "tap", "x": 512, "y": 300},
  {"action": "wait", "ms": 1500},
  {"action": "screenshot", "label": "ball"},
  {"action": "assert", "expr": "lives == 3"}]}]}
```

A scenario runs on a simulated clock, so every run is identical, dates included. Each `screenshot` and the final screen become reference images; a false `assert` or a Python error fails the test. The steps available are the same as those of the `simulate` tool of AI agents, described in the [MCP server guide](mcp.md).

## 14. Command line

The IDE also has a command line, `lvgl-mpy-studio` (with the AppImage: `./LVGL_MPY_STUDIO-x86_64.AppImage <command>`). Messages are in English; `--language it` switches to Italian.

| Command | What it does |
|---|---|
| `lvgl-mpy-studio` | opens the IDE; the project is then opened from **File → Open** or **File → Recent Files** |
| `lvgl-mpy-studio run project.json` | starts the project in the simulator |
| `lvgl-mpy-studio generate project.json` | generates the code (`--target micropython`, `c` or `board`) |
| `lvgl-mpy-studio build project.json` | builds the executable in `dist/` next to the project; `--profile release --single-file` for the single file, `--for windows` or `--for linux` for the other system, `--web` for the browser version |
| `lvgl-mpy-studio web project.json` | builds the browser version, serves it and opens it; Ctrl+C stops it |
| `lvgl-mpy-studio test project.json` | visual tests; `--update`, `--page`, `--scenario`, `--threshold` |
| `lvgl-mpy-studio device list` | lists the connected boards; `info`, `upload`, `run`, `stop`, `reset`, `repl`, `autostart-install`, `autostart-remove` act on a board with `--port` |
| `lvgl-mpy-studio mcp` | starts the server for AI agents |
| `lvgl-mpy-studio selftest` | the IDE uses itself and reports what works; see below |
| `lvgl-mpy-studio --version` | shows the version |

### Self-test

`lvgl-mpy-studio selftest` opens the IDE and uses it as a person would: it creates a project, takes widgets from the toolbox, sets their properties in the panel, types a handler, saves, starts the simulator and touches the screen. Each step is checked and written as `PASSED` or `FAILED`; the last line is `RESULT: PASSED` or `RESULT: FAILED`, and the command ends with 0 or 1.

- Without options the IDE stays hidden and the run takes a few seconds. `--show` shows it at work, slowed down; `--slow 800` sets the pause after each action in milliseconds.
- The report goes to `lvgl-mpy-studio-selftest/<date-time>/` in the current folder, or to the folder given with `--output`: `report.txt`, `report.json`, the projects it saved under `work/`, and for each failed step a picture of the IDE and of the simulator.
- `--list` shows the scenarios; naming one or more runs only those.
- Your settings, recent files and board profiles are not touched. Do not use the mouse or the keyboard on the IDE's window while `--show` runs.

It checks that things work, not how they look, and it does not use boards.

## 15. AI agents

LVGL MPY Studio can be used by an AI agent, such as Claude or Kimi, through the **Model Context Protocol** (MCP). The agent creates projects, draws pages, writes the code, tries the game in the simulator by touching the screen, measures memory and, with you present, works on the board.

The server is off until you turn it on from **Settings → MCP Server for AI Agents**. The [MCP server guide](mcp.md) explains how to connect it to your agent and what it can do. Two practical rules:

- if the project is also open in the IDE, the IDE notices the agent's changes when you save, and asks whether to **reload** the file, **save a copy**, **overwrite** or cancel: nothing is written without a choice. Changes made in the IDE do not reach the agent until you save;
- before letting the agent use the board, disconnect it from the IDE.

The same check applies to any program that writes the project file, the command line included. If the file was deleted, the IDE offers to recreate it or to save it elsewhere. **Save As** asks before replacing another file.

## 16. Keyboard shortcuts

| Keys | Action |
|---|---|
| Ctrl+N, Ctrl+O, Ctrl+S, Ctrl+Shift+S | New, Open, Save, Save As |
| Ctrl+P | Print Sources |
| Ctrl+Z, Ctrl+Shift+Z | Undo, Redo |
| Ctrl+X, Ctrl+C, Ctrl+V, Del | Cut, Copy, Paste, Delete |
| Ctrl+D | Duplicate |
| Ctrl+A | Select all |
| Ctrl+], Ctrl+[ | Bring to Front, Send to Back |
| Ctrl++, Ctrl+−, Ctrl+0 | Zoom in, Zoom out, Fit to Window |
| F5, Shift+F5 | Start, Stop |
| Ctrl+Space | Suggestions in the editor |
| Ctrl+Q | Exit |

## 17. Common problems

**The simulator does not start or closes at once.** Look at the **Errors** and **Output** panels: an error in the module code, or in a `SCREEN_LOADED` handler, stops the app at start-up. A double click on the error goes to the line.

**The project cannot be changed.** While the simulator or an app on the board is running the project is read-only: press **Stop and Edit** above the editor, or Shift+F5.

**`NameError: name 'ui' isn't defined` in a module.** A module does not get `ui` and `lv` as handlers do: add `import ui` and `import lvgl as lv` at the top.

**`ImportError` after renaming or deleting a module.** The code still imports the old name: update the `import` lines the IDE listed in **Output**, or undo with Ctrl+Z.

**The board does not answer: `could not enter raw repl`.** A program on the board does not stop with Ctrl+C. The IDE insists with more Ctrl+C, which is enough for shells that ask for two, like that of some ESP32-4848S040 firmware. If it is not enough, close other programs that use the port, press the reset button of the board and try again.

**No sound from the Buzzer on the board.** The board profile must name a pin or a speaker; the built-in profiles do so where the board has a buzzer. If in doubt look at **Device → Manage Board Profiles…**.

**The serial port is busy.** Only one program at a time can use it: close other serial terminals, or disconnect the IDE if an AI agent or `mpremote` needs it.

**I changed the resolution and something overlaps.** Ctrl+Z undoes it, then try the other choice, or fix by hand the widgets the output lists as outside the screen.

**The single-file executable does not start on an old Linux.** It needs glibc 2.34 or later, that is Ubuntu 22.04, Debian 12 or newer. On Windows, if it does not start, look at `<project>.log` next to the file.

**Windows says the app is not safe.** The executables are not signed: **More info → Run anyway**.
