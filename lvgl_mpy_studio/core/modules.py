"""User Python modules: .py files of the project, importable from the code and from each other.

Pure functions on the model, without Qt: GUI, CLI and MCP use them the same way. The name of a
module is also the name of its file, so the rules mostly avoid paths and collisions: a simple
lower-case identifier at the root of the app.
"""

import keyword
import re

from .i18n import tr
from .names import RESERVED

MODULE_NAME_RE = re.compile(r"[a-z_][a-z0-9_]{0,30}")

# Files the IDE generates next to the modules, on the simulator, on the board or in packages.
GENERATED = frozenset((
    "ui", "main", "app_events", "app_main", "display_driver", "board_adapter", "board_profile",
    "manifest", "sourcemap", "boot",
))
# MicroPython modules. On the simulator runtime a file time.py, json.py, random.py,
# asyncio.py or machine.py takes the place of the real module (verified), so these names are
# not used. The list joins the modules of the unix runtime and those of the most common boards.
MICROPYTHON = frozenset((
    "array", "asyncio", "binascii", "bluetooth", "btree", "builtins", "cmath", "collections",
    "cryptolib", "deflate", "dht", "ds18x20", "errno", "esp", "esp32", "espnow", "ffi", "framebuf",
    "gc", "hashlib", "heapq", "io", "json", "lvgl", "lvgl_micropython", "lvsim", "lv", "machine",
    "math", "micropython", "mip", "neopixel", "network", "ntptime", "onewire", "os", "platform",
    "pyb", "random", "re", "requests", "rp2", "select", "socket", "ssl", "stm", "struct", "sys",
    "termios", "time", "tls", "uasyncio", "uctypes", "upip", "vfs", "webrepl", "websocket",
    "argparse", "_thread", "_asyncio",
))
# The old names with a leading u still exist on some firmware.
MICROPYTHON_ALIASES = frozenset("u" + name for name in (
    "array", "binascii", "collections", "errno", "hashlib", "heapq", "io", "json", "os", "random",
    "re", "select", "socket", "ssl", "struct", "sys", "time", "zlib",
))
IDE_PREFIXES = ("lms_", "lvgl_ide", "lvgl_mpy_studio")  # generated files, their names up to 0.4, and the package of the IDE


class ModuleError(ValueError):
    pass


def reserved_module_name(name):
    """Why the name cannot be used, or None."""
    if name in GENERATED or name.startswith(IDE_PREFIXES):
        return tr("name of a file the IDE generates")
    if name in MICROPYTHON or name in MICROPYTHON_ALIASES:
        return tr("name of a MicroPython module")
    if keyword.iskeyword(name) or name in RESERVED:
        # Importing it would bind the name in the app code: import print would hide print().
        return tr("name reserved by Python or the IDE")
    if name.startswith("__"):
        return tr("names with __ are reserved for Python")
    return None


def validate_module_name(name, project=None, exclude=None):
    """Error message, or None if the name is valid in the project. exclude: the module being renamed."""
    if not isinstance(name, str) or not MODULE_NAME_RE.fullmatch(name):
        return tr("a module name uses lower case letters, digits and _, starts with a letter or _, and has at most 31 characters")
    reason = reserved_module_name(name)
    if reason:
        return f"{name}: {reason}"
    if project is not None:
        if any(module.name == name and module is not exclude for module in project.modules):
            return tr("{name}: a module with this name already exists", name=name)
        if name in project.code.handlers:
            return tr("{name}: it is the name of a handler", name=name)
    return None


def find_module(project, name):
    module = next((module for module in project.modules if module.name == name), None)
    if module is None:
        raise ModuleError(tr("no such module: {name}", name=name))
    return module


def create_module(project, name, source=""):
    from .model import UserModule

    error = validate_module_name(name, project)
    if error:
        raise ModuleError(error)
    module = UserModule(name, _text(source))
    project.modules.append(module)
    return module


def rename_module(project, name, new_name):
    """Rename without rewriting code; return where the old name still appears."""
    module = find_module(project, name)
    if new_name == name:
        return []
    error = validate_module_name(new_name, project, exclude=module)
    if error:
        raise ModuleError(error)
    module.name = new_name
    return module_references(project, name)


def delete_module(project, name):
    """Delete the module; return the code that still imports it."""
    module = find_module(project, name)
    project.modules.remove(module)
    return module_references(project, name)


def set_module_source(project, name, source):
    find_module(project, name).source = _text(source)


def patch_module(project, name, old, new, replace_all=False):
    """Replace old with new in the module; old must occur once, unless replace_all."""
    module = find_module(project, name)
    count = module.source.count(old) if old else 0
    if count == 0:
        raise ModuleError(tr("text to replace not found"))
    if count > 1 and not replace_all:
        raise ModuleError(tr("the text to replace occurs {count} times: add context or replace them all", count=count))
    module.source = module.source.replace(old, _text(new))
    return count


def module_files(project):
    """{file name: source} of each module, in project order. The only place the pipelines read them from."""
    files = {}
    for module in project.modules:
        error = validate_module_name(module.name)
        if error:  # a hand-written file must not be able to leave the app folder
            raise ModuleError(error)
        files[f"{module.name}.py"] = module.source.replace("\r\n", "\n").replace("\r", "\n")
    return files


def module_references(project, name):
    """Where an import of the module appears: in the general code, in handlers and in other modules."""
    pattern = re.compile(rf"^\s*(?:import\s+[^#\n]*\b{re.escape(name)}\b|from\s+{re.escape(name)}\s+import\b)", re.MULTILINE)
    scopes = [(tr("(General)"), project.code.module)]
    scopes += [(handler, body.body) for handler, body in project.code.handlers.items()]
    scopes += [(f"{module.name}.py", module.source) for module in project.modules if module.name != name]
    return [tr("{scope}: still imports {name}", scope=scope, name=name) for scope, source in scopes if pattern.search(source)]


def _text(source):
    if not isinstance(source, str):
        raise ModuleError(tr("the source of a module must be text"))
    return source
