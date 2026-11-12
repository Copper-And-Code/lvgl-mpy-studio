# Plan: plugins

Status: phases 1 and 2 done on 2026-11-12, in version 0.6.0, with the Block Manager of phase 3; the rest is not started. Written on 2026-11-12.

## Goal

Let people other than the authors add features to LVGL MPY Studio. The first need is hardware:
blocks that make SPI, UART, PWM, I2C and similar MicroPython peripherals as easy to use as a
widget. Later the same mechanism must be able to carry other kinds of extension.

## Decisions taken

1. **Two kinds of plugin, one at a time.** A *block* is data plus MicroPython code that runs on
   the board. An *IDE extension* is Python code that runs inside the IDE. This plan delivers
   blocks; IDE extensions are only prepared for (see "Left for later").
2. **Installing is copying a folder.** No online catalogue, no installer, no downloads.
3. **The IDE ships with a set of standard blocks**, written in the same format a contributor
   uses. They prove the format and are the example to copy.

## What a block is

A block is a non-visual component, like Buzzer and Timer today: it appears in the toolbox, is
dropped on a page, has a name and properties, and the code reaches it as `ui.<name>`. It
creates no LVGL object.

Buzzer and Timer are written by hand in `core/components.py`, `gen/components.py` and
`gen/output/buzzer.py`, and eleven other files know them by name. The work of this plan is to
turn that special case into a general mechanism, and then express Buzzer as an ordinary block.
Timer stays built in: it is an `lv.timer`, not a module.

### Folder layout

```
i2c_bus/
  block.json        description: read by the IDE, never executed
  board.py          the module for a real board; a block can have several, see "Board variants"
  simulator.py      the module for the simulators (desktop and web); optional
  LICENSE           required for a block that is shared
  README.md         optional, shown in the IDE
```

### `block.json`

```json
{
  "schemaVersion": 1,
  "id": "i2c_bus",
  "version": "1.0.0",
  "name": "I2C Bus",
  "description": "An I2C bus in controller mode.",
  "author": "LVGL MPY Studio",
  "license": "MIT",
  "icon": "mdi6.chip",
  "category": "Hardware",
  "requires": {"modules": ["machine"]},
  "properties": [
    {"name": "bus", "type": "number", "label": "Bus", "default": 0, "min": 0, "max": 3},
    {"name": "scl", "type": "pin", "label": "SCL pin", "role": "i2c.scl"},
    {"name": "sda", "type": "pin", "label": "SDA pin", "role": "i2c.sda"},
    {"name": "freq", "type": "number", "label": "Frequency (Hz)", "default": 400000}
  ],
  "methods": [
    {"name": "scan", "arguments": "", "help": "Addresses of the devices that answer."},
    {"name": "read", "arguments": "address, count", "help": "Read count bytes."},
    {"name": "write", "arguments": "address, data", "help": "Write bytes."}
  ],
  "events": [],
  "instances": "many",
  "simulator": "simulator.py",
  "board": [{"file": "board.py"}]
}
```

Points of the format:

- `properties` use the property types the panel already has, plus the new type `pin`.
- `methods` feed code completion and the **What do you want to do?** panel, as
  `BUZZER_METHODS` does today.
- `events` names the handlers a block can call (for example `received` for a UART). The IDE
  generates the handler stub and wires it, as it does for the Timer.
- `instances` is `many` (a class, one object per component) or `one` (a module, as the buzzer).
- `requires.modules` is checked against what the board reports on connection; a missing module
  is a warning before upload, not a traceback after.
- `schemaVersion` lets the format change without breaking old blocks.
- `kind` is optional and only accepts `block`: it is the place where IDE extensions will be told apart.

### Board variants

`board` is a list, tried in order: the first variant that applies gives the module. A variant
applies when its `when.profile` value exists in the board profile and each of its `constants`
is found there with the right type. The constants are written as `NAME = value` lines above the
module. The Buzzer uses both:

```json
"board": [
  {"file": "board_audio.py", "when": {"profile": "buzzer.audio"}},
  {"file": "board_pwm.py", "constants": {"PIN": {"profile": "buzzer.pin", "type": "integer"}}}
],
"unavailable": "This board has no buzzer: calls to the component will do nothing."
```

When no variant applies the block gets a module whose methods do nothing, and the text of
`unavailable` is shown as a warning.

### The module contract

`board.py` and `simulator.py` define the same thing, so that project code does not change
between the simulator and the board:

- `instances: many` — a class named `Block`; the generator writes
  `ui.<name> = <module>.Block(name='<name>', bus=0, scl=5, sda=4, freq=400000)`: the name of the
  component, for its messages, then the properties as keyword arguments. A handler the user
  wrote for an event arrives as `on_<event>=`, for example `on_pressed=`; the block calls it
  with itself as the only argument. The object is created after the pages, and only if the
  code uses it or it has a handler.
- `instances: one` — module-level functions; the generator writes `import <module> as <name>`.
  Such a block is shared by all its components, so it has no properties and no events.

The module is named `lms_<id>` in the generated application.

A block without `simulator.py` gets a generated stand-in: every method listed in `block.json`
exists, does nothing, returns `None` and prints one line in the simulator console the first
time it is called. The project still runs in the simulator; it does not fail on `import machine`.

## Where blocks live

1. **Standard blocks**: inside the package, `lvgl_mpy_studio/blocks/<id>/`.
2. **User blocks**: `<config folder>/blocks/<id>/`, next to the board profiles. **Tools →
   Open the blocks folder** opens it; blocks are read again when the IDE starts and from
   **Tools → Reload blocks**.
3. **In the project**: a project keeps a copy of each block it uses, as it does for fonts,
   pictures and the board profile. A project opens and runs on a computer that lacks the block.

When the installed block and the copy in the project differ in version, the project keeps its
copy and the IDE offers **Update block**, as it does for the board profile. A user block with
the `id` of a standard one replaces it, with a line in the Output panel saying so.

## Pins

Hardware blocks are only easy if the IDE knows the pins.

- The board profile gains an optional `pins` section: the pins the user can reach, the
  roles each supports, and the ones taken by the display, the touch panel and the buzzer.
- The property type `pin` shows a list instead of a number when the profile has that section,
  filtered by `role`.
- Validation reports two components on one pin, and a component on a reserved pin. These are
  warnings: the profile may be incomplete, and the user knows their wiring.
- A profile without `pins` keeps working: the property is a plain number.

The three built-in profiles get their `pins` section from the schematics; values that cannot
be confirmed on the real board are left out rather than guessed.

## Standard blocks

| Block | Purpose | In the simulator |
|---|---|---|
| Digital output | A pin driven high or low: LED, relay | Keeps its state; printed on change |
| Digital input | A pin read, with an event on change and debounce | Value settable from scenario scripts |
| PWM | Frequency and duty on a pin | Keeps its values |
| ADC | Analogue reading, raw and in volts | Value settable from scenario scripts |
| I2C bus | Scan, read, write | No devices answer |
| SPI bus | Read, write, transfer | Reads return zeros |
| UART | Write, read, event on received line | Reads return nothing |
| Buzzer | The component of today, as a block | Sound, as today |

"Settable from scenario scripts" means a `simulate` scenario can set the value of an input, so
that behaviour depending on a button or a sensor can be tested without a board.

## What changes in the code

- **`core/blocks.py`** (new): find, read and validate blocks from the three places; the
  registry of definitions. Reading never imports or runs block code.
- **`core/components.py`**: `COMPONENTS` becomes the registry: Timer plus the blocks.
  `is_component` stays, so its eleven callers do not change.
- **`core/model.py`**: `assets["blocks"]` holds the copies; schema version 4 only for projects
  that use a block, as version 3 is only for projects with modules.
- **`core/validation.py`**: property checks for blocks, pin conflicts, missing firmware modules.
- **`gen/components.py`**, **`gen/project_gen.py`**, **`gen/board_gen.py`**: write the module of
  each block in use (`simulator.py` or the stand-in for the simulators, `board.py` for boards),
  the imports and the constructor calls. Block modules are precompiled like `ui.py`.
- **`gen/gen_c.py`**: blocks are ignored with a warning, as Buzzer and Timer are today.
- **`gen/live.py`**: a changed block property restarts the application instead of patching it.
- **`ui/designer/scene.py`**, **`ui/properties/panel.py`**, toolbox: read the registry; the
  `pin` editor; a category per `category` value.
- **`ui/code/editor.py`**: completion from `methods` instead of the two fixed tuples.
- **`mcp_server.py`**: `list_widget_types` already merges components; add `list_blocks`, and
  report blocks in `project_info`.
- **Module names**: a block module is `lms_<id>`; the prefix is already reserved.

## Compatibility

- Projects with a Buzzer open unchanged: the type name `buzzer` and `ui.<name>.beep()` stay.
- The `buzzer` section of a board profile stays, and becomes the default pin of the block.
- An IDE older than this refuses a project that uses blocks, with the message it already gives
  for a newer schema version.

## Risks

- **A block breaks the application on the board.** It is the user's own risk, as with their
  own code; the IDE shows the author and the licence.
- **Block code runs on the PC inside the simulator.** The IDE itself never runs block code,
  but the simulator runs `simulator.py` as it runs the code of the project, with the same
  access to files. A block from someone else deserves the trust given to a project from
  someone else, and so does a project that carries a block inside.
- **Memory.** Each block is a module on a board with little RAM. The size budget already shown
  for the project counts block modules.
- **The format is hard to change once published.** Hence `schemaVersion`, and the standard
  blocks written first: eight real uses before anyone else depends on it.
- **Pin data in profiles can be wrong.** Hence warnings rather than errors, and no guessed values.

## Phases

Each phase ends with the test suite passing and can be released on its own.

1. **Registry and format.** Done. `core/blocks.py`, `block.json` validation, discovery among the
   standard blocks and in the user folder, Buzzer rewritten as a block with unchanged behaviour:
   the generated files are the same byte for byte. No visible change. User blocks are read and
   checked but not offered, because generation only knows the Buzzer; the copy inside the
   project comes with phase 2.
2. **Generation.** Done. Classes with properties and events, simulator stand-in, copy in the
   project (for blocks that are not standard), project file version 4, precompilation, C
   warning. Digital Output and Digital Input are the first new blocks, tried in the simulator
   and with a fake `machine` in the tests, not yet on a board. User blocks are offered in the
   toolbox when the IDE starts. Left out: setting an input from `simulate` scenarios; for now
   the code calls `simulate(value)` on the input.
3. **IDE.** Partly done: toolbox category, properties, completion and **What do you want to
   do?** from the methods of the block, and **Settings → Manage Blocks…**, which lists the
   blocks with their origin, adds one from a folder, removes it, reloads, opens the blocks
   folder and installs on this computer a block that only the open project carries. **Update
   block** is not needed: a project is saved with the blocks as they are installed now. Still
   to do: the MCP tool `list_blocks`, blocks in `project_info`, translations of the texts of
   the standard blocks, and `docs/blocks.md`.
4. **Pins.** `pins` in profiles, the `pin` editor, conflict warnings.
5. **The remaining standard blocks**: PWM, ADC, I2C, SPI, UART, each tried on a real board.
6. **Documentation.** `docs/blocks.md`: how to write a block, with one block built step by
   step; a chapter in the manual.

Hardware checks needed: every standard block on at least one of the three boards, with a
wiring note in the test log. Phase 5 cannot be closed in the simulator alone.

## Left for later

- **IDE extensions.** Python code running inside the IDE: menus, panels, exporters,
  importers. The open questions are trust (the code has the user's permissions), a stable
  interface to program against, and dependencies inside the AppImage and the Windows package.
  What this plan prepares: the plugin folder, the manifest with `schemaVersion`, and a `kind`
  field that today only accepts `block`.
- **An online catalogue**, with whatever review it needs.
- **Blocks in the C export.**
- **Visual blocks**: a plugin that adds an LVGL widget. It touches `widgets.json`, the
  renderer and both generators, and is a different piece of work.

## Open questions

1. Should a block be allowed to depend on another, for example a temperature sensor on an I2C
   bus block? It is the natural next step for sensors, and it changes the format: a property of
   type `block`. Proposed: accept it in the format from the start, implement it in phase 5.
2. Blocks are placed on a page today because components are. A bus belongs to the whole
   application rather than to a page. Proposed: keep the current rule for now and revisit it
   when the project tree gains a place for application-wide items.
