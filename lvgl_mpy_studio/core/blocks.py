"""Blocks: non-visual components described by a folder, with MicroPython code for the board.

A block is a folder with `block.json` and the modules it names. The IDE only reads these files:
the code of a block runs on the board or in the simulator, never inside the IDE. A folder that
cannot be read is reported and skipped; it never stops the IDE."""

import ast
import json
import re
import shutil
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from lvgl_mpy_studio.platform import config_dir

SCHEMA_VERSION = 1
MANIFEST = "block.json"
NOTICE = "# SPDX-License-Identifier: MIT\n# Copyright (c) 2026 Nunzio Raciti\n"  # of the code the IDE writes itself
ID = re.compile(r"[a-z][a-z0-9_]{0,30}")
NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
FILE = re.compile(r"[A-Za-z0-9_]+\.py")
PROPERTY_TYPES = ("number", "string", "boolean", "select", "color", "pin")
PROPERTY_VALUES = {"number": (int, float), "string": str, "boolean": bool, "select": str, "color": str, "pin": (int, str)}
CONSTANT_TYPES = {"integer": int, "number": (int, float), "string": str, "boolean": bool}
INSTANCES = ("one", "many")
EXTRAS = ("LICENSE", "LICENSE.txt", "README.md")
MODULE_PREFIX = "lms_"  # reserved: no user module can take the name of a block module
PIN_MAX = 255
PIN_NAME = re.compile(r"[A-Za-z][A-Za-z0-9_]{0,15}")  # as the firmware names it: PA5, GP25, LED


def parse_pin(text):
    """A pin as typed: a number, a name such as PA5, or nothing. ValueError for anything else.

    MicroPython takes a number on some ports and a name on others; the block gets what was typed."""
    text = str(text).strip()
    if not text:
        return None
    if text.isdigit():
        if int(text) > PIN_MAX:
            raise ValueError(text)
        return int(text)
    if not PIN_NAME.fullmatch(text):
        raise ValueError(text)
    return text


def is_pin(value):
    """True for a value a pin property may hold."""
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return 0 <= value <= PIN_MAX
    return value is None or isinstance(value, str) and bool(PIN_NAME.fullmatch(value))


class BlockError(ValueError):
    """A block that cannot be used; the message says what is wrong with it."""


@dataclass(frozen=True)
class Block:
    manifest: dict
    files: dict = field(default_factory=dict)  # file name -> text, only the modules the manifest names
    origin: str = "standard"
    extras: dict = field(default_factory=dict, compare=False)  # LICENSE and README, as text
    folder: str = field(default="", compare=False)  # where it was read from; empty for one stored in a project

    @property
    def id(self):
        return self.manifest["id"]

    @property
    def methods(self):
        return tuple(method["name"] for method in self.manifest["methods"])

    @property
    def events(self):
        return tuple(event["name"] for event in self.manifest["events"])

    @property
    def many(self):
        """True for a class with one object per component, False for a module shared by all."""
        return self.manifest["instances"] == "many"

    @property
    def module(self):
        """The name of the module in the generated application."""
        return MODULE_PREFIX + self.id

    def definition(self):
        """The block as the toolbox, the Properties panel and validation know a component."""
        properties = []
        for item in self.manifest["properties"]:
            entry = {key: value for key, value in item.items() if key != "default"}
            if entry["type"] == "pin":  # a number or a name, typed; the list of the pins of the board comes later
                entry["pin"] = True
            properties.append(entry)
        defaults = {item["name"]: item["default"] for item in self.manifest["properties"] if "default" in item}
        return {"type": self.id, "name": self.manifest["name"], "icon": self.manifest.get("icon", ""), "category": self.manifest.get("category", "Components"), "defaultProps": defaults, "properties": properties}

    def to_dict(self):
        """The copy a project keeps, so that it opens where the block is not installed."""
        return {"manifest": self.manifest, "files": self.files} | ({"extras": self.extras} if self.extras else {})

    @classmethod
    def from_dict(cls, data, origin="project"):
        """The block stored in a project; BlockError if it is not a usable one."""
        manifest, files = (data or {}).get("manifest"), (data or {}).get("files")
        if not isinstance(files, dict) or not all(isinstance(name, str) and isinstance(text, str) for name, text in files.items()):
            raise BlockError("the files of the block are missing")
        errors = validate(manifest, set(files))
        if errors:
            raise BlockError("; ".join(errors))
        extras = data.get("extras") if isinstance(data.get("extras"), dict) else {}
        return cls(manifest, dict(files), origin, {name: text for name, text in extras.items() if name in EXTRAS and isinstance(text, str)})

    def simulator_source(self):
        """The module for the simulators, or None when the block has none."""
        name = self.manifest.get("simulator")
        return self.files[name] if name else None

    def board_source(self, profile):
        """The module for a board with that profile: the first variant that applies, or None."""
        for variant in self.manifest["board"]:
            when = (variant.get("when") or {}).get("profile")
            if when and lookup(profile, when) in (None, False):
                continue
            constants = {}
            for name, source in (variant.get("constants") or {}).items():
                value = lookup(profile, source["profile"])
                expected = CONSTANT_TYPES[source.get("type", "integer")]
                if not isinstance(value, expected) or (isinstance(value, bool) and expected is not bool):
                    break
                constants[name] = value
            else:
                return with_constants(self.files[variant["file"]], constants)
        return None

    def silent_source(self):
        """A module with every method of the block that does nothing: for a board that lacks the hardware."""
        return self._stand_in(lambda method: ["pass"])

    def unsimulated_source(self):
        """The module for the simulator of a block that has none: the methods exist and say, once, that they do nothing."""
        name = self.manifest["name"]
        head = f"_told = set()\n\n\ndef _tell(method):\n    if method not in _told:\n        _told.add(method)\n        print({name + ': '!r} + method + {'() does nothing in the simulator'!r})\n\n\n"
        return self._stand_in(lambda method: [f"_tell({method['name']!r})"], head)

    def _stand_in(self, body, head=""):
        methods = self.manifest["methods"]
        if not self.many:
            return NOTICE + head + "\n\n".join(f"def {method['name']}({method.get('arguments', '')}):\n" + "".join(f"    {line}\n" for line in body(method)) for method in methods)
        lines = ["class Block:", "    def __init__(self, name=\"\", **options):", "        self.name = name", "        self.options = options"]
        for method in methods:
            arguments = method.get("arguments", "")
            lines += ["", f"    def {method['name']}(self{', ' + arguments if arguments else ''}):", *(f"        {line}" for line in body(method))]
        return NOTICE + head + "\n".join(lines) + "\n"


def lookup(data, path):
    """The value at a dotted path inside a profile, or None."""
    for key in path.split("."):
        if not isinstance(data, dict) or key not in data:
            return None
        data = data[key]
    return data


def with_constants(source, constants):
    """The module with NAME = value lines after its leading comments."""
    if not constants:
        return source
    lines = source.splitlines(keepends=True)
    head = next((index for index, line in enumerate(lines) if not line.startswith("#")), len(lines))
    return "".join(lines[:head]) + "".join(f"{name} = {value!r}\n" for name, value in constants.items()) + "".join(lines[head:])


def _is_argument_list(text):
    """True for what can stand between the brackets of a def, and nothing more: it is written into generated code."""
    if not isinstance(text, str) or "\n" in text or "\r" in text:
        return False
    try:
        tree = ast.parse(f"def _({text}): pass")
    except (SyntaxError, ValueError):
        return False
    return len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef) and len(tree.body[0].body) == 1 and isinstance(tree.body[0].body[0], ast.Pass)


def _texts(manifest, keys, where, errors):
    for key in keys:
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            errors.append(f"{where}: “{key}” must be a text")


def validate(manifest, files=()):
    """What is wrong with a block.json, as a list of sentences; empty when it can be used.

    files are the names of the files next to it."""
    if not isinstance(manifest, dict):
        return ["block.json must be an object"]
    errors = []
    if manifest.get("schemaVersion") != SCHEMA_VERSION:
        return [f"schemaVersion is {manifest.get('schemaVersion')!r}: this IDE reads version {SCHEMA_VERSION}"]
    if manifest.get("kind", "block") != "block":
        errors.append(f"kind is {manifest.get('kind')!r}: only “block” exists")
    if not isinstance(manifest.get("id"), str) or not ID.fullmatch(manifest["id"]):
        errors.append("“id” must be lower-case letters, digits and _, starting with a letter, at most 31 characters")
    _texts(manifest, ("version", "name", "description", "author", "license"), "block.json", errors)
    if manifest.get("instances") not in INSTANCES:
        errors.append("“instances” must be “one” or “many”")
    if manifest.get("instances") == "one" and (manifest.get("properties") or manifest.get("events")):
        errors.append("a block with “instances”: “one” is a module shared by all its components: it cannot have properties or events")
    for key in ("properties", "methods", "events", "board"):
        if not isinstance(manifest.get(key), list):
            errors.append(f"“{key}” must be a list")
            manifest = {**manifest, key: []}
    names = set()
    for index, item in enumerate(manifest["properties"]):
        where = f"properties[{index}]"
        if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not NAME.fullmatch(item["name"]):
            errors.append(f"{where}: “name” must be a Python name")
            continue
        if item["name"] in names:
            errors.append(f"{where}: the name “{item['name']}” is used twice")
        names.add(item["name"])
        if item.get("type") not in PROPERTY_TYPES:
            errors.append(f"{where}: “type” must be one of {', '.join(PROPERTY_TYPES)}")
        elif "default" in item and not isinstance(item["default"], PROPERTY_VALUES[item["type"]]) or isinstance(item.get("default"), bool) and item["type"] != "boolean" or item["type"] == "pin" and not is_pin(item.get("default")):
            errors.append(f"{where}: “default” is not a {item['type']}")
        if item.get("type") == "select" and not (isinstance(item.get("options"), list) and item["options"] and all(isinstance(option, str) for option in item["options"])):
            errors.append(f"{where}: a “select” needs its “options”, a list of texts")
        _texts(item, ("label",), where, errors)
    names = set()
    for index, item in enumerate(manifest["methods"]):
        where = f"methods[{index}]"
        if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not NAME.fullmatch(item["name"]) or item["name"].startswith("_"):
            errors.append(f"{where}: “name” must be a public Python name")
            continue
        if item["name"] in names:
            errors.append(f"{where}: the name “{item['name']}” is used twice")
        names.add(item["name"])
        if not _is_argument_list(item.get("arguments", "")):
            errors.append(f"{where}: “arguments” is not a Python argument list")
    for index, item in enumerate(manifest["events"]):
        if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not re.fullmatch(r"[A-Z][A-Z0-9_]*", item["name"]):
            errors.append(f"events[{index}]: “name” must be upper-case letters, digits and _")

    def module(name, where):
        if not isinstance(name, str) or not FILE.fullmatch(name):
            errors.append(f"{where}: a module is a file name ending in .py, without folders")
        elif files is not None and name not in files:
            errors.append(f"{where}: the file {name} is missing")

    if manifest.get("simulator") is not None:
        module(manifest["simulator"], "simulator")
    for index, variant in enumerate(manifest["board"]):
        where = f"board[{index}]"
        if not isinstance(variant, dict):
            errors.append(f"{where}: must be an object")
            continue
        module(variant.get("file"), where)
        when = variant.get("when")
        if when is not None and (not isinstance(when, dict) or not isinstance(when.get("profile"), str)):
            errors.append(f"{where}: “when” must name a “profile” value")
        constants = variant.get("constants") or {}
        if not isinstance(constants, dict):
            errors.append(f"{where}: “constants” must be an object")
            continue
        for name, source in constants.items():
            if not re.fullmatch(r"[A-Z][A-Z0-9_]*", name) or not isinstance(source, dict) or not isinstance(source.get("profile"), str) or source.get("type", "integer") not in CONSTANT_TYPES:
                errors.append(f"{where}: the constant “{name}” must be upper-case and name a “profile” value, with a “type” among {', '.join(CONSTANT_TYPES)}")
    if "unavailable" in manifest and not isinstance(manifest["unavailable"], str):
        errors.append("“unavailable” must be a text")
    return errors


def load_block(directory, origin="user", check_name=True):
    """Read the block in a folder; BlockError says why it cannot be used.

    check_name: the folder must be named as the id, as it must be once installed."""
    directory = Path(directory)
    try:
        manifest = json.loads((directory / MANIFEST).read_text(encoding="utf-8"))
    except OSError as exc:
        raise BlockError(f"{MANIFEST} cannot be read: {exc}") from exc
    except ValueError as exc:
        raise BlockError(f"{MANIFEST} is not valid JSON: {exc}") from exc
    present = {path.name for path in directory.iterdir() if path.is_file()}
    errors = validate(manifest, present)
    if not errors and check_name and manifest["id"] != directory.name:
        errors.append(f"the folder is named {directory.name} and the id is {manifest['id']}: they must be the same")
    if errors:
        raise BlockError("; ".join(errors))
    names = {variant["file"] for variant in manifest["board"]} | ({manifest["simulator"]} if manifest.get("simulator") else set())
    try:
        files = {name: (directory / name).read_text(encoding="utf-8") for name in sorted(names)}
    except (OSError, ValueError) as exc:
        raise BlockError(f"a module cannot be read: {exc}") from exc
    extras = {}
    for name in sorted(present & set(EXTRAS)):  # shown to the user and copied with the block, never used by the IDE
        try:
            extras[name] = (directory / name).read_text(encoding="utf-8")
        except (OSError, ValueError):
            pass
    return Block(manifest, files, origin, extras, str(directory))


def discover(directory, origin="user"):
    """The blocks in the folders of a directory, and what went wrong: ({id: Block}, [(folder, message)])."""
    directory = Path(directory)
    found, problems = {}, []
    if not directory.is_dir():
        return found, problems
    for folder in sorted(path for path in directory.iterdir() if path.is_dir() and not path.name.startswith((".", "_"))):
        try:
            block = load_block(folder, origin)
        except BlockError as exc:
            problems.append((str(folder), str(exc)))
        else:
            found[block.id] = block
    return found, problems


def standard_dir():
    return Path(__file__).resolve().parent.parent / "blocks"


def user_dir():
    return config_dir() / "blocks"


@lru_cache(maxsize=1)
def standard_blocks():
    """The blocks shipped with the IDE. One that cannot be read is a defect of the package: it raises."""
    found, problems = discover(standard_dir(), "standard")
    if problems:
        raise BlockError("; ".join(f"{folder}: {message}" for folder, message in problems))
    return found


def user_blocks():
    """The blocks the user copied into the blocks folder, and the folders that could not be read."""
    return discover(user_dir(), "user")


def write_block(block, directory=None):
    """Install a block: write its folder under the user's blocks folder, replacing one with the same id."""
    directory = Path(directory) if directory else user_dir()
    target = directory / block.id
    temporary = directory / f".{block.id}.installing"
    shutil.rmtree(temporary, ignore_errors=True)
    temporary.mkdir(parents=True)
    try:
        (temporary / MANIFEST).write_text(json.dumps(block.manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        for name, text in {**block.extras, **block.files}.items():
            (temporary / name).write_text(text, encoding="utf-8", newline="\n")
        shutil.rmtree(target, ignore_errors=True)
        temporary.rename(target)
    finally:
        shutil.rmtree(temporary, ignore_errors=True)
    return target


def install_block(source):
    """Copy the block in the folder source into the user's blocks folder; return it as installed.

    Only block.json, the modules it names, the licence and the README are copied."""
    block = load_block(source, "user", check_name=False)
    return load_block(write_block(block), "user")


def remove_block(block_id):
    """Delete a block of the user's blocks folder; False if it is not there."""
    target = user_dir() / block_id
    if not ID.fullmatch(block_id) or not target.is_dir():
        return False
    shutil.rmtree(target)
    return True
