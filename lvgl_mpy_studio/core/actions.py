"""Common widget actions: the text for the user and the exact LVGL call.

CURSOR marks where to leave the cursor after inserting. Each action is tried
on the real runtime by tests/test_actions.py.
"""

import re

from lvgl_mpy_studio.core.i18n import tr

CURSOR = "§"

COMMON = (
    ("Hide", "ui.{name}.add_flag(lv.obj.FLAG.HIDDEN)"),
    ("Show", "ui.{name}.remove_flag(lv.obj.FLAG.HIDDEN)"),
    ("Move", "ui.{name}.set_pos(§0, 0)"),
    ("Resize", "ui.{name}.set_size(§100, 40)"),
    ("Change background color", "ui.{name}.set_style_bg_color(lv.color_hex(0x§2196F3), lv.PART.MAIN)"),
)
ENABLE = (
    ("Disable", "ui.{name}.add_state(lv.STATE.DISABLED)"),
    ("Enable", "ui.{name}.remove_state(lv.STATE.DISABLED)"),
)
TEXT = (
    ("Change text", 'ui.{name}.set_text("§")'),
    ("Read text", "ui.{name}.get_text()"),
)
TEXT_COLOR = (("Change text color", "ui.{name}.set_style_text_color(lv.color_hex(0x§FF0000), lv.PART.MAIN)"),)
CHECKED = (
    ("Is it on?", "ui.{name}.has_state(lv.STATE.CHECKED)"),
    ("Turn on", "ui.{name}.add_state(lv.STATE.CHECKED)"),
    ("Turn off", "ui.{name}.remove_state(lv.STATE.CHECKED)"),
)
ANIMATED_VALUE = (
    ("Read value", "ui.{name}.get_value()"),
    ("Change value", "ui.{name}.set_value(§50, False)"),
)
SIMPLE_VALUE = (
    ("Read value", "ui.{name}.get_value()"),
    ("Change value", "ui.{name}.set_value(§50)"),
)
SELECTED = (
    ("Read selected item", "ui.{name}.get_selected()"),
    ("Read selected item text", "ui.{name}.get_selected_str()"),
)

SPECIFIC = {
    "label": (*TEXT, *TEXT_COLOR),
    "button": (("Change text", 'ui.{name}.get_child(0).set_text("§")'), ("Read text", "ui.{name}.get_child(0).get_text()"), *ENABLE),
    "textarea": (*TEXT, ("Add text", 'ui.{name}.add_text("§")'), *ENABLE),
    "slider": (*ANIMATED_VALUE, *ENABLE),
    "bar": ANIMATED_VALUE,
    "arc": (*SIMPLE_VALUE, *ENABLE),
    "spinbox": (*SIMPLE_VALUE, *ENABLE),
    "switch": (*CHECKED, *ENABLE),
    "checkbox": (*CHECKED, ("Change text", 'ui.{name}.set_text("§")'), *ENABLE),
    "dropdown": (("Read selected item", "ui.{name}.get_selected()"), ("Select an item", "ui.{name}.set_selected(§0)"), *ENABLE),
    "roller": (("Read selected item", "ui.{name}.get_selected()"), ("Select an item", "ui.{name}.set_selected(§0, False)"), *ENABLE),
    "led": (("Switch on", "ui.{name}.on()"), ("Switch off", "ui.{name}.off()")),
    "imagebutton": ENABLE,
}

COMPONENT_ACTIONS = {
    "buzzer": (
        ("Beep", "ui.{name}.beep(§440, 30)"),
        ("Start sound", "ui.{name}.tone(§880)"),
        ("Stop sound", "ui.{name}.off()"),
    ),
    "timer": (
        ("Pause", "ui.{name}.pause()"),
        ("Resume", "ui.{name}.resume()"),
        ("Change interval (ms)", "ui.{name}.set_period(§500)"),
    ),
}


def actions_for(widget_type, name):
    """Actions of the widget, the most useful first: (description, code)."""
    actions = COMPONENT_ACTIONS.get(widget_type) or (*SPECIFIC.get(widget_type, ()), *COMMON)
    return [(label, code.format(name=name)) for label, code in actions]


SCREEN_ACTIONS = (
    ("Read the screen width", "lv.display_get_default().get_horizontal_resolution()"),
    ("Read the screen height", "lv.display_get_default().get_vertical_resolution()"),
)


def page_actions(constant):
    return [("Open this page", f"ui.load_page(ui.{constant})")]


def method_entries(widget_type, name):
    """For completion after ui.<name>.: (menu text, text to insert)."""
    prefix = f"ui.{name}."
    entries = []
    for label, code in actions_for(widget_type, name):
        if code.startswith(prefix):
            tail = code[len(prefix):]
            entries.append((f"{tail.split('(')[0]} — {tr(label)}", tail))
    return entries


def module_actions(module, own=False):
    """What a user module offers: importing it, its functions and classes, its upper-case constants.

    The source is read without running it. With a syntax error the top-level def lines remain, so
    the help does not vanish while typing. own: for the open module, where its functions are
    called without the module name in front and there is nothing to import.
    """
    import ast

    prefix = "" if own else f"{module.name}."
    actions = [] if own else [("Import the module", f"import {module.name}")]
    try:
        tree = ast.parse(module.source)
    except SyntaxError:
        for match in re.finditer(r"^def ([A-Za-z_][A-Za-z0-9_]*)\(", module.source, re.MULTILINE):
            if not match.group(1).startswith("_"):
                actions.append((f"{match.group(1)}()", f"{prefix}{match.group(1)}({CURSOR})"))
        return actions
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and not node.name.startswith("_"):
            if isinstance(node, ast.ClassDef):
                actions.append((f"{node.name}()", f"{prefix}{node.name}({CURSOR})"))
                continue
            arguments = [argument.arg for argument in node.args.posonlyargs + node.args.args]
            call = f"{prefix}{node.name}({CURSOR})" if arguments else f"{prefix}{node.name}()"
            actions.append((f"{node.name}({', '.join(arguments)})", call))
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper() and not target.id.startswith("_"):
                    actions.append((target.id, f"{prefix}{target.id}"))
    return actions
