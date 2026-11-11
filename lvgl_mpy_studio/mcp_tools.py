"""The tools of the MCP server as data: for each name its description, its arguments and the required ones.

mcp_server pairs every entry with the function of the same name.
"""

PROJECT = {"type": "string", "description": "Path of the project .json file"}
PORT = {"type": "string", "description": "Serial port, from device_list_ports"}
PROPS = {"type": "object", "description": "Property values, as listed by list_widget_types"}
MODULE = {"type": "string", "description": "Name of a Python module of the project, as imported by the code (utils for utils.py)"}
REVISION = {"type": "string", "description": "Revision returned by project_info or get_code. If the file is no longer that revision, nothing changes and the result is a revision_conflict error"}

SPECS = {
    "create_project": (
        "Create a new empty project file. Give width and height, or board to take resolution and board from a profile of list_boards; without them the project is 800x480.",
        {
            "path": {"type": "string"},
            "name": {"type": "string"},
            "width": {"type": "integer"},
            "height": {"type": "integer"},
            "board": {"type": "string"},
        },
        ["path"],
    ),
    "project_info": (
        "Read pages, widgets, properties, code and the list of images of a project.",
        {
            "project": PROJECT,
        },
        ["project"],
    ),
    "list_widget_types": (
        "List widget types with their properties, default values and events. The whole list is long: pass names_only to get just the type names, then types for the ones you need.",
        {
            "types": {"type": "array", "items": {"type": "string"}, "description": "Only these types"},
            "names_only": {"type": "boolean"},
        },
        [],
    ),
    "suggest_code": (
        "List ready-made LVGL calls for a widget, for use in handlers.",
        {
            "project": PROJECT,
            "widget": {"type": "string"},
        },
        ["project", "widget"],
    ),
    "add_page": (
        "Add a page.",
        {
            "project": PROJECT,
            "name": {"type": "string"},
        },
        ["project", "name"],
    ),
    "rename_page": (
        "Rename a page and its handlers. Warns about code that still uses the old PAGE_ constant.",
        {
            "project": PROJECT,
            "name": {"type": "string"},
            "new_name": {"type": "string"},
        },
        ["project", "name", "new_name"],
    ),
    "remove_page": (
        "Remove a page and its widgets. Their handlers stay in the project, as when deleting in the IDE.",
        {
            "project": PROJECT,
            "name": {"type": "string"},
        },
        ["project", "name"],
    ),
    "add_widgets": (
        "Add many widgets in one call. Either all of them are added or none. A parent can be a widget earlier in the same list.",
        {
            "project": PROJECT,
            "page": {"type": "string"},
            "widgets": {"type": "array", "description": "Each item takes the arguments of add_widget: type, name, props, parent, page", "items": {"type": "object"}},
        },
        ["project", "widgets"],
    ),
    "move_widget": (
        "Change the parent or draw order of a widget. A new parent keeps it where it is on screen. Later widgets draw on top.",
        {
            "project": PROJECT,
            "name": {"type": "string"},
            "parent": {"type": ["string", "null"], "description": "New parent; null for the page itself"},
            "order": {"type": ["string", "integer"], "description": "front, back or an index"},
            "before": {"type": "string", "description": "Place it just under this widget"},
        },
        ["project", "name"],
    ),
    "get_code": (
        "Read the shared code with the handler and module names, or the body of one handler, or the source of one Python module, without the whole project. Returns the file revision.",
        {
            "project": PROJECT,
            "handler": {"type": "string"},
            "module": MODULE,
        },
        ["project"],
    ),
    "patch_code": (
        "Replace a piece of the shared code, of one handler or of one Python module, without sending all of it. The old text must occur once unless all is set. The result must compile.",
        {
            "project": PROJECT,
            "old": {"type": "string"},
            "new": {"type": "string"},
            "handler": {"type": "string"},
            "module": MODULE,
            "all": {"type": "boolean"},
        },
        ["project", "old", "new"],
    ),
    "list_modules": (
        "List the Python modules of the project: files the handlers, the shared code and other modules import by name.",
        {
            "project": PROJECT,
        },
        ["project"],
    ),
    "create_module": (
        "Create a Python module of the project, imported by its name. The name is lower case letters, digits and _, and cannot be a MicroPython module, a file the IDE generates or a handler. The source must compile.",
        {
            "project": PROJECT,
            "name": MODULE,
            "source": {"type": "string"},
        },
        ["project", "name"],
    ),
    "rename_module": (
        "Rename a Python module. Code importing the old name is not rewritten: references lists where it is still imported.",
        {
            "project": PROJECT,
            "name": MODULE,
            "new_name": {"type": "string"},
        },
        ["project", "name", "new_name"],
    ),
    "delete_module": (
        "Delete a Python module. references lists code that still imports it.",
        {
            "project": PROJECT,
            "name": MODULE,
        },
        ["project", "name"],
    ),
    "add_image": (
        "Add a PNG picture to the project, from a file on this machine, to show it with an image widget: set the widget's src to the returned name. The picture is stored inside the project file and goes to the simulator, the board and every build. At most 512 kB; keep pictures small, a board needs about 4 bytes of RAM per pixel while one is shown.",
        {
            "project": PROJECT,
            "file": {"type": "string", "description": "Path of a .png file"},
            "name": {"type": "string", "description": "Name in the project; default: the file name"},
            "replace": {"type": "boolean", "description": "Replace an image with the same name"},
        },
        ["project", "file"],
    ),
    "remove_image": (
        "Remove a picture from the project. stillUsedBy lists the widgets that showed it.",
        {
            "project": PROJECT,
            "name": {"type": "string"},
        },
        ["project", "name"],
    ),
    "add_font": (
        "Add a TrueType or OpenType font to the project, from a file on this machine. A widget uses it when its font property is the returned name; fontSize can then be any size. The font is converted for each size in use, with printable ASCII and the characters of the widgets that use it; text set from code can use those characters.",
        {
            "project": PROJECT,
            "file": {"type": "string", "description": "Path of a .ttf or .otf file"},
            "name": {"type": "string"},
            "replace": {"type": "boolean"},
        },
        ["project", "file"],
    ),
    "remove_font": (
        "Remove a font from the project. stillUsedBy lists the widgets that asked for it.",
        {
            "project": PROJECT,
            "name": {"type": "string"},
        },
        ["project", "name"],
    ),
    "add_widget": (
        "Add a widget to a page, optionally inside a parent widget.",
        {
            "project": PROJECT,
            "type": {"type": "string"},
            "name": {"type": "string"},
            "page": {"type": "string"},
            "parent": {"type": "string"},
            "props": PROPS,
        },
        ["project", "type"],
    ),
    "update_widget": (
        "Change properties of a widget, or rename it.",
        {
            "project": PROJECT,
            "name": {"type": "string"},
            "new_name": {"type": "string"},
            "props": PROPS,
        },
        ["project", "name"],
    ),
    "remove_widget": (
        "Remove a widget, with the widgets it contains. Their handlers stay in the project.",
        {
            "project": PROJECT,
            "name": {"type": "string"},
        },
        ["project", "name"],
    ),
    "set_handler": (
        "Write the MicroPython body of an event handler. The body gets the event as e; use ui.<widget> and lv.",
        {
            "project": PROJECT,
            "widget": {"type": "string", "description": "Widget or page name"},
            "event": {"type": "string", "description": "Default: the main event of the widget type, SCREEN_LOADED for a page"},
            "body": {"type": "string"},
        },
        ["project", "widget", "body"],
    ),
    "set_module_code": (
        "Replace the shared MicroPython code placed before the handlers.",
        {
            "project": PROJECT,
            "code": {"type": "string"},
        },
        ["project", "code"],
    ),
    "set_resolution": (
        "Change the resolution. mode stretch (default) scales each axis on its own; adapt keeps proportions and follows edges, centre and groups; keep leaves widgets where they are, so each page can be adapted later with adapt_page.",
        {
            "project": PROJECT,
            "width": {"type": "integer"},
            "height": {"type": "integer"},
            "mode": {"type": "string", "enum": ["stretch", "adapt", "keep"]},
        },
        ["project", "width", "height"],
    ),
    "adapt_page": (
        "Bring a page left at another resolution by set_resolution keep to the current one, with mode adapt (default) or stretch.",
        {
            "project": PROJECT,
            "page": {"type": "string"},
            "mode": {"type": "string", "enum": ["adapt", "stretch"]},
        },
        ["project"],
    ),
    "validate": (
        "Validate a project and report widgets outside the screen.",
        {
            "project": PROJECT,
        },
        ["project"],
    ),
    "simulate": (
        "Run the project in the real LVGL simulator and play a script of touch input. With the default virtual clock, time advances in fixed 10 ms steps only while the script waits, so a run is repeatable, faster than real time and can last up to 600 simulated seconds; time.ticks_ms() in the game follows it. clock real runs in real time like the IDE panel, up to 30 s, for a feel of the frame rate. seed seeds random. Returns a JSON report (passed, failure, values, console, Python tracebacks, buzzer tones, frame count, whether the app is still running) redraw statistics, followed by one PNG per screenshot step and a final one.",
        {
            "project": PROJECT,
            "page": {"type": "string"},
            "design_only": {"type": "boolean"},
            "clock": {"type": "string", "enum": ["virtual", "real"]},
            "seed": {"type": "integer"},
            "steps": {"type": "array", "description": "Played in order, at most 600 s of waiting in total with the virtual clock, 30 s with the real one. Each step has an action: tap, press, move, release (x and y, or widget for the centre of a widget laid out at fixed coordinates), drag (also x_to and y_to or widget_to, and ms), wait (ms), key (code), screenshot (optional label), repeat (times, at most 10000, and nested steps), reset_redraw (start measuring redraw here, to skip the start-up frames). Steps that look inside the app, between two frames, in the namespace of the module code: eval (expr, optional label; the value goes to values), exec (code, to set up a state such as a level), assert (expr, or page for the active page; a false one stops the script and fills failure), wait_until (expr or page, ms timeout, default 5000). Expressions can also call page() and objects(), the number of LVGL objects on the active screen.", "items": {"type": "object"}},
        },
        ["project"],
    ),
    "render_page": (
        "Return a PNG of a page drawn by the real LVGL runtime, with the project code running unless design_only is set.",
        {
            "project": PROJECT,
            "page": {"type": "string"},
            "design_only": {"type": "boolean"},
        },
        ["project"],
    ),
    "visual_test": (
        "Compare pages and scenarios with their PNG baselines, or rewrite them with update. pages or scenarios limit the run to those names.",
        {
            "project": PROJECT,
            "update": {"type": "boolean"},
            "design_only": {"type": "boolean"},
            "pages": {"type": "array", "items": {"type": "string"}},
            "scenarios": {"type": "array", "items": {"type": "string"}},
        },
        ["project"],
    ),
    "save_scenario": (
        "Save a visual test scenario for the current resolution: the same steps as simulate, played on the virtual clock with a fixed seed. Each screenshot step and the final screen become baselines. A failed assert or a Python traceback fails the test.",
        {
            "project": PROJECT,
            "name": {"type": "string"},
            "page": {"type": "string"},
            "seed": {"type": "integer"},
            "steps": {"type": "array", "items": {"type": "object"}},
        },
        ["project", "name", "steps"],
    ),
    "measure": (
        "Measure flash and RAM use by running the project.",
        {
            "project": PROJECT,
        },
        ["project"],
    ),
    "generate_code": (
        "Generate sources: micropython for the simulator, board for the project's board (to copy onto it), or portable c.",
        {
            "project": PROJECT,
            "target": {"type": "string", "enum": ["micropython", "board", "c"]},
            "output": {"type": "string"},
            "board": {"type": "string", "description": "With target board: use this board id instead of the project's, without saving it"},
            "overwrite": {"type": "boolean", "description": "With target board: replace files changed after the last export"},
        },
        ["project"],
    ),
    "build": (
        "Build a standalone executable.",
        {
            "project": PROJECT,
            "target": {"type": "string", "enum": ["micropython", "c"]},
            "profile": {"type": "string", "enum": ["debug", "release"]},
            "output": {"type": "string"},
        },
        ["project"],
    ),
    "list_boards": (
        "List the board profiles, with the resolution and the Montserrat font sizes of each. A project without a board has sizes 14, 16, 24, 32 and 40; text in another size is drawn in the nearest one.",
        {},
        [],
    ),
    "set_board": (
        "Assign a board profile to the project, scaling its widgets to the board.",
        {
            "project": PROJECT,
            "board": {"type": "string"},
        },
        ["project", "board"],
    ),
    "device_list_ports": (
        "List serial ports.",
        {},
        [],
    ),
    "device_connect": (
        "Connect to a board, with the profile of a project or a board id.",
        {
            "port": PORT,
            "project": PROJECT,
            "board": {"type": "string"},
        },
        ["port"],
    ),
    "device_disconnect": (
        "Release the serial port.",
        {},
        [],
    ),
    "device_info": (
        "Read firmware, LVGL, memory and compatibility of the connected board.",
        {},
        [],
    ),
    "device_upload": (
        "Upload the project to the board, and start it with run.",
        {
            "project": PROJECT,
            "run": {"type": "boolean"},
        },
        ["project"],
    ),
    "device_stop": (
        "Stop the application on the board.",
        {},
        [],
    ),
    "device_reset": (
        "Soft reset the board.",
        {},
        [],
    ),
    "device_exec": (
        "Run MicroPython code on the board and return its output.",
        {
            "code": {"type": "string"},
        },
        ["code"],
    ),
    "device_read_console": (
        "Read the board console for some seconds, at most 30.",
        {
            "seconds": {"type": "number"},
        },
        [],
    ),
    "device_live_update": (
        "Send design changes to the running application with no restart. Code changes need device_upload.",
        {
            "project": PROJECT,
            "page": {"type": "string"},
        },
        ["project"],
    ),
    "device_autostart_install": (
        "Make the project start when the board boots.",
        {
            "project": PROJECT,
        },
        ["project"],
    ),
    "device_autostart_remove": (
        "Remove the project autostart.",
        {
            "project": PROJECT,
        },
        ["project"],
    ),
}

# The tools that write the project file accept expected_revision.
WRITES_PROJECT = (
    "add_page", "rename_page", "remove_page", "add_widget", "add_widgets", "move_widget", "update_widget", "remove_widget",
    "set_handler", "set_module_code", "patch_code", "set_resolution", "adapt_page", "set_board",
    "create_module", "rename_module", "delete_module", "add_image", "remove_image", "add_font", "remove_font",
)
for _name in WRITES_PROJECT:
    SPECS[_name][1]["expected_revision"] = REVISION
