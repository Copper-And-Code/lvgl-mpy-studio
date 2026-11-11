# MCP server for AI agents

`lvgl-mpy-studio mcp` lets an AI agent work on LVGL MPY Studio projects through the Model Context Protocol, over stdio. The agent can create and edit projects, see pages rendered by the real LVGL runtime, run tests, build, and work on a connected board.

[From a prompt to an app](mcp-demo.md) shows a complete recorded session: an agent builds a weather station in 24 calls.

## Turning it on

The server is off by default. Turn it on under **Settings → MCP Server for AI Agents**. While it is off, `lvgl-mpy-studio mcp` refuses to start, and a running server answers every tool call with an error. The choice is stored in `lvgl-mpy-studio/mcp.json` in your configuration folder.

This switch controls the MCP server only. It does not restrict the CLI.

## What the agent can do

There are no limits compared to the IDE. With the server on, an agent can run project code on your computer, upload and run code on a board, execute MicroPython on it and install autostart. Stay in control of the session, especially with projects you did not write: text inside a project can try to steer an agent.

| Area | Tools |
|---|---|
| Project | `create_project`, `project_info`, `validate`, `set_resolution`, `adapt_page`, `list_boards`, `set_board` |
| Images and fonts | `add_image`, `remove_image`, `add_font`, `remove_font`; `project_info` lists them |
| Design | `list_widget_types`, `add_page`, `rename_page`, `remove_page`, `add_widget`, `add_widgets`, `update_widget`, `move_widget`, `remove_widget` |
| Code | `get_code`, `patch_code`, `set_handler`, `set_module_code`, `suggest_code` |
| Python modules | `list_modules`, `create_module`, `rename_module`, `delete_module` |
| Checks | `render_page`, `simulate`, `visual_test`, `save_scenario`, `measure` |
| Output | `generate_code`, `build` |
| Board | `device_list_ports`, `device_connect`, `device_disconnect`, `device_info`, `device_upload`, `device_stop`, `device_reset`, `device_exec`, `device_read_console`, `device_live_update`, `device_autostart_install`, `device_autostart_remove` |

`list_widget_types` returns every type with its properties, default values and events; the list is long, so `names_only` returns just the names and `types` the details of the ones asked for. `list_boards` gives the resolution and the Montserrat font sizes of each board. Text asked in a size the target lacks, or with a character outside the built-in font, is reported in the `warnings` of the call that sets it and by `validate`.

`create_project` takes `width` and `height`, or `board` for the resolution and board of a profile from `list_boards`; without them a project is 800×480. `set_resolution` takes `mode`: `stretch`, the default, `adapt`, which keeps proportions as in the IDE, or `keep`, which leaves the widgets alone so that `adapt_page` can adapt one page at a time.

Python modules are `.py` files of the project that handlers, the shared code and other modules import by name: `import utils`. `create_module` takes `name` and optional `source`; the name uses lower case letters, digits and `_`, and cannot be a MicroPython module such as `time`, a file the IDE generates such as `ui`, or a handler. `get_code` and `patch_code` take `module` instead of `handler` to read or change one. `rename_module` and `delete_module` never rewrite code: `references` lists the imports still using the old name. A module is a file of its own: `ui` and `lv` are not defined in it as in handlers, so its source imports them (`import ui`, `import lvgl as lv`). Unlike the editor, `create_module` does not add those lines.

`project_info`, `get_code` and `list_modules` return `revision`, a SHA-256 of the project file. Pass it as `expected_revision` to any tool that changes the project: if the file is no longer that revision, because the IDE or another agent saved it, nothing is written and the result is an error like this one, also in `structuredContent`:

```json
{
  "error": "revision_conflict",
  "message": "The project file is not the revision expected: nothing was changed. Read it again with project_info or get_code, then repeat the change if it still applies.",
  "project": "/home/me/game/project.json",
  "expected_revision": "6f1c…",
  "current_revision": "a93e…"
}
```

Tools that change the project return the new `revision`, valid for the next call. Without `expected_revision` the tools work as before, and still refuse to write if the file changed while the tool was running. The check is not a lock: a program writing at the very moment of the save can still be overwritten.

`render_page` returns a PNG and runs the project code unless `design_only` is set.

`simulate` runs the app in the real simulator and plays a script of steps: `tap`, `press`, `move`, `release`, `drag`, `key`, `wait`, `screenshot`, `repeat` and `reset_redraw`. It answers with the console, any Python traceback, the buzzer tones, the frame count, whether the app is still running, redraw statistics, and one PNG per screenshot plus a final one. This lets an agent play a game or try a handler without a board. Each run starts the app from scratch.

By default the clock is virtual: the game advances in fixed 10 ms steps only while the script waits, and stops in between. A run is repeatable, screenshots included, and much faster than real time: a two-minute game takes a few seconds. `time.ticks_ms()`, `ticks_us()`, the sleeps, `time()`, `time_ns()`, `localtime()` and `gmtime()` follow the simulated time, which always starts on 1 January 2026 at midnight, with local time in UTC, so dates and times on screen repeat on every computer, and `seed` seeds `random`. A script can wait 600 simulated seconds at most. `clock: "real"` runs in real time like the IDE panel, up to 30 seconds, and gives a feel of the frame rate.

Four steps look inside the running app, between two frames, in the namespace of the module code:

- `eval` reads an expression, such as `lives` or `(score, wave)`, into `values`.
- `exec` runs code to reach a state quickly, such as `wave = 8` followed by the function that prepares a wave.
- `assert` checks an expression, or `{"page": "Fine"}` for the active page. A false one stops the script and fills `failure`.
- `wait_until` waits for an expression or a page, up to `ms` milliseconds, 5000 by default, and also counts towards the time limit.

Expressions can call `page()` for the name of the active page and `objects()` for the number of LVGL objects on it. `passed` is true when no step failed, every `eval` worked, no traceback was printed and the app is still running. A failed `eval` does not stop the script, so later steps still run. If the app stops answering, the script ends there. This code is added only to the copy of the project that runs in the simulator, never to the board or to exported files.

`save_scenario` stores a `simulate` script as a visual test scenario for the current resolution, and `visual_test` with `update` writes its baselines. From then on the same touches must give the same pixels.

The redraw statistics say how many pixels the app redraws per frame and per second. A step `reset_redraw` starts the count later, to skip the start-up frames. They show the relative cost of a design, not the frame rate of a board, because a board can redraw differently.

Points come from `x` and `y`, or from `widget` for the centre of a widget. `widget` uses the project coordinates, so it is wrong for widgets that the code moves at runtime, as the adaptive examples do. Use a screenshot and `x`, `y` for those.

## Client configuration

Most clients accept this form. Use the path of your installed `lvgl-mpy-studio` or AppImage:

```json
{
  "mcpServers": {
    "lvgl-mpy-studio": {
      "command": "/path/to/lvgl-mpy-studio",
      "args": ["mcp"]
    }
  }
}
```

## Limits

- The server edits project files. If the same project is open in the IDE, the IDE notices the agent's changes when it saves and asks whether to reload, save a copy or overwrite; it does not watch the file, so it shows them only after a reload. The server itself refuses to write over a save it has not read, except in the brief race described above.
- Only one program can hold a serial port: disconnect in the IDE before using the `device_` tools.
- Agent changes do not enter the IDE's undo history. Use Git to review or revert them.
- With the virtual clock, code that measures real time, such as a benchmark, sees simulated time instead. The redraw statistics then describe simulated seconds: use `clock: "real"` for a feel of the frame rate on a PC, which still says nothing precise about a board.
- Long board operations block the server until they finish, and some clients stop waiting after a timeout.
