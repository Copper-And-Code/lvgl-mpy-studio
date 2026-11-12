# Writing a block

A block adds a component to LVGL MPY Studio: something the application uses from code and that
is not drawn on the page, such as an output pin, a sensor or a bus. This guide builds one from
nothing. The finished example is in `examples/blocks/blinker`.

You need a text editor and some MicroPython. The IDE itself needs no change.

## What a block is

A folder, named as the block:

```
blinker/
  block.json      what the block is: read by the IDE, never run
  board.py        the code for a real board
  simulator.py    the code for the simulators; optional
  LICENSE         the licence, if you share the block
  README.md       optional
```

The IDE reads `block.json` and shows the block in the toolbox. When a project that uses it is
started, the IDE copies `simulator.py` into the application for the simulator, or `board.py`
for a board, under the name `lms_blinker.py`.

**The code of a block runs on the user's computer, inside the simulator**, with the same
access to files as the code of a project. People will install your block only if they trust
you: keep it short and readable, and say what it does.

## Step 1: the description

`block.json` for a pin that blinks by itself:

```json
{
  "schemaVersion": 1,
  "id": "blinker",
  "version": "1.0.0",
  "name": "Blinker",
  "description": "A pin that blinks by itself: a status LED that needs no code to keep going.",
  "author": "Your Name",
  "license": "MIT",
  "icon": "mdi6.alarm-light-outline",
  "category": "Hardware",
  "instances": "many",
  "properties": [
    {"name": "pin", "type": "pin", "label": "Pin"},
    {"name": "period", "type": "number", "label": "Period (ms)", "default": 500, "min": 20, "max": 60000},
    {"name": "running", "type": "boolean", "label": "Blink at Start", "default": true}
  ],
  "methods": [
    {"name": "start", "arguments": "", "help": "Start blinking."},
    {"name": "stop", "arguments": "", "help": "Stop blinking and leave the pin off."},
    {"name": "set_period", "arguments": "ms", "help": "Change how long the pin stays on and off, in milliseconds."},
    {"name": "is_running", "arguments": "", "help": "True while it blinks."}
  ],
  "events": [
    {"name": "BLINKED", "help": "The pin went on"}
  ],
  "simulator": "simulator.py",
  "board": [{"file": "board.py"}]
}
```

| Field | Meaning |
|---|---|
| `schemaVersion` | Always `1`. |
| `id` | Lower-case letters, digits and `_`, starting with a letter. It is the name of the folder, the type of the component and part of the module name. `timer` is taken. |
| `version`, `name`, `description`, `author`, `license` | Shown in **Settings → Manage Blocks…**. |
| `icon` | An icon of Material Design Icons 6, as `mdi6.<name>`. Without it the block gets a chip. |
| `category` | The heading in the toolbox. `Hardware` is where the standard blocks are. |
| `instances` | `many`: a class, one object for each component. `one`: a module shared by all components, without properties and events. |
| `properties` | What the user sets in the Properties panel. |
| `methods` | What the code can call: they feed completion and **What do you want to do?**. `arguments` is what stands between the brackets; `help` is the sentence the user reads. |
| `events` | What the block tells the application. Names are upper-case. |
| `simulator` | The module for the simulators. Leave the field out if there is none. |
| `board` | The module for boards: a list, see "More than one board". |

### Property types

| `type` | Value in code | In the panel |
|---|---|---|
| `number` | `int` | a number field; `min` and `max` are optional |
| `string` | `str` | a text field |
| `boolean` | `bool` | a check box |
| `select` | one of `options`, a list of texts | a list |
| `color` | `"#RRGGBB"` | a colour chooser |
| `pin` | `int` or `str`, or `None` when not set | a field for a number, such as `25`, or a name, such as `PA5` |

A property without `default` starts empty. A `pin` should have none: a wrong pin can drive
hardware it should not, so the user must choose it. An unset pin reaches your code as `None`.
A pin is what the user typed, a number or a name, because MicroPython wants one or the other
depending on the port: pass it to `machine.Pin` as it is.

## Step 2: the code for the board

The contract is short. For `"instances": "many"` the module defines a class named `Block`:

```python
import lvgl as lv
from machine import Pin


class Block:
    def __init__(self, name="", pin=None, period=500, running=True, on_blinked=None):
        if pin is None:
            raise ValueError(name + ": set the Pin property")
        self._pin = Pin(pin, Pin.OUT, value=0)
        self._on = False
        self._handler = on_blinked
        self._timer = lv.timer_create(self._tick, max(1, int(period) // 2), None)
        if not running:
            self._timer.pause()
        self._running = bool(running)

    def _tick(self, timer):
        self._on = not self._on
        self._pin.value(int(self._on))
        if self._on and self._handler is not None:
            self._handler(self)

    def start(self):
        self._running = True
        self._timer.resume()

    def stop(self):
        self._running = False
        self._timer.pause()
        self._on = False
        self._pin.value(0)

    def set_period(self, ms):
        self._timer.set_period(max(1, int(ms) // 2))

    def is_running(self):
        return self._running
```

The IDE writes the line that creates the object, after the pages exist:

```python
ui.blinker1 = lms_blinker.Block(name='blinker1', pin=25, period=500, running=True, on_blinked=app_events.blinker1_blinked)
```

- `name` is the name of the component: use it in error messages.
- Each property arrives as a keyword argument with its name. Give every argument a default, so
  that a later version of the block with one more property still loads.
- An event arrives as `on_<event in lower case>`, only when the user wrote a handler for it.
  Call the handler with the block as its only argument: the user reads it as `e`.
- Every method in `block.json` must exist, with those arguments.
- An object nobody uses is not created: no handler and no `ui.blinker1` in the code.

**Do not call handlers from an interrupt.** A handler usually changes the screen, and LVGL must
not be touched from an interrupt. Use `lv.timer_create`, as here: its callback runs where LVGL
runs. To watch a pin, read it from a timer, as the Digital Input block does.

For `"instances": "one"` the module defines functions instead of a class, and the IDE writes
`import lms_<id> as <name>`. The Buzzer is made this way.

## Step 3: the code for the simulator

In the simulator there is no `machine`. `simulator.py` has the same class, the same methods and
the same events, without the hardware:

```python
import lvgl as lv


class Block:
    def __init__(self, name="", pin=None, period=500, running=True, on_blinked=None):
        self._on = False
        self._handler = on_blinked
        self._timer = lv.timer_create(self._tick, max(1, int(period) // 2), None)
        if not running:
            self._timer.pause()
        self._running = bool(running)

    def _tick(self, timer):
        self._on = not self._on
        if self._on and self._handler is not None:
            self._handler(self)
    ...
```

Make it behave as the board does wherever the application can tell the difference: here the
event still fires, so a project that counts blinks works on the PC. For an input, give the
block a method that pretends the input changed, as `simulate()` of the Digital Input.

Without `simulator.py` the IDE writes a stand-in: every method exists and does nothing, and says
so once in the Output panel. The project still starts in the simulator.

## Step 4: try it

1. **Settings → Manage Blocks… → Add from Folder…** and choose the folder. A block with a
   mistake is refused with a sentence that says what is wrong.
2. The block is in the toolbox, under its category. Add it to a project, set its properties,
   write a handler for its event from the **Events** tab.
3. Press F5: the simulator runs `simulator.py`.
4. After changing the files, install the folder again: the manager asks to replace the block.
   **Reload** is enough when you edit the files inside the blocks folder itself.

`lvgl-mpy-studio selftest` does not cover your block; try it on the board too.

## More than one board

`board` is a list of variants, tried in order. The first that applies gives the module:

```json
"board": [
  {"file": "board_audio.py", "when": {"profile": "buzzer.audio"}},
  {"file": "board_pwm.py", "constants": {"PIN": {"profile": "buzzer.pin", "type": "integer"}}}
],
"unavailable": "This board has no buzzer: calls to the component will do nothing."
```

- `when.profile` names a value of the board profile, with dots for nested values. The variant
  applies when the value is there and is not `false`.
- `constants` takes values from the profile and writes them above the module as `NAME = value`.
  The variant applies only if every constant is found, with its `type`: `integer`, `number`,
  `string` or `boolean`.
- When no variant applies the application gets a module whose methods do nothing, and the
  user sees the text of `unavailable` as a warning.

A block with one module for every board needs only `[{"file": "board.py"}]`.

## What the user's project keeps

A project that uses your block stores a copy of it, so it opens on a computer where the block
is not installed, and can be installed from there with **Install from Project**. The copy is
the block as installed when the project was last saved. Such a project is saved as version 4,
which IDEs older than 0.6 refuse to open.

## Limits today

- The IDE does not know which pins a board has free, and does not warn about two blocks on one pin.
- Blocks are MicroPython only: the C export leaves components out, with a warning.
- A block cannot depend on another block, for example a sensor on an I2C bus block.
- Texts of a block are shown as written: the IDE translates only those of its own blocks.

`docs/plugins-plan.md` says what is planned for each.
