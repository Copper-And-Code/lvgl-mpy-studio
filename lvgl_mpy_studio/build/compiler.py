import json
import os
from pathlib import Path
import re
import subprocess
import sys

from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.platform import CREATE_NO_WINDOW, mpy_cross_path, root_dir


def cache_root():
    if getattr(sys, "frozen", False):
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
        return base / "lvgl-mpy-studio"
    return root_dir() / "cache"


def default_mpy_cross():
    return mpy_cross_path()


def compile_python(directory, mpy_cross=None):
    directory = Path(directory).resolve()
    executable = Path(mpy_cross).resolve() if mpy_cross else default_mpy_cross()
    errors = []
    for path in sorted(directory.glob("*.py")):
        result = subprocess.run([str(executable), str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=directory, creationflags=CREATE_NO_WINDOW)
        if result.returncode:
            errors.extend(parse_compiler_errors(result.stderr + result.stdout, directory))
    if errors:
        raise CompileError(errors)
    return True


def parse_compiler_errors(output, directory=None):
    directory = Path(directory) if directory else None
    errors = []
    lines = output.splitlines()
    for index, line in enumerate(lines):
        match = re.search(r'(?:File ")?([^":\n]+\.py)"?, line (\d+)(?::(\d+))?', line)
        if match:
            path = Path(match.group(1))
            if directory and not path.is_absolute(): path = directory / path
            error = {"file": str(path), "line": int(match.group(2)), "column": int(match.group(3) or 1), "message": line}
            following = lines[index + 1].strip() if index + 1 < len(lines) else ""
            if re.match(r"[A-Za-z]*Error\b", following):  # SyntaxError: invalid syntax, on the next line
                error["detail"] = following
            errors.append(error)
    if not errors and output.strip(): errors.append({"file": None, "line": 1, "column": 1, "message": output.strip()})
    return errors


TRACE_FRAME = re.compile(r'File "([^"]*?([A-Za-z_][A-Za-z0-9_]*)\.py)", line (\d+)')


def _sourcemap_entry(entries, line):
    entry = next((entry for entry in entries if entry["line"] == line), None)
    if entry is None:
        previous = [entry for entry in entries if entry["line"] < line]
        entry = max(previous, key=lambda entry: entry["line"]) if previous else None
    return entry


def traceback_errors(text, sourcemap=None, modules=()):
    """The lines of a traceback that lead to user code, without repeats.

    app_events.py goes through the source map to a handler and a line; a user module is written
    as it is, so file and line are already those of the editor. Other generated files do not count.
    In each traceback the last user line is where the error happened: it has origin, the others
    are the calls that led there, such as the handler that imported or called the module.
    """
    errors, seen = [], set()
    entries = (sourcemap or {}).get("entries", [])
    for block in re.split(r"(?=Traceback \(most recent call last\))", text):
        frames = [match for match in TRACE_FRAME.finditer(block) if match.group(2) == "app_events" or match.group(2) in modules]
        origin = (frames[-1].group(1), int(frames[-1].group(3))) if frames else None  # even if already seen
        for match in frames:
            path, stem, line = match.group(1), match.group(2), int(match.group(3))
            if (path, line) in seen:
                continue
            seen.add((path, line))
            error = {"file": path, "line": line, "column": 1, "message": match.group(0), "origin": (path, line) == origin}
            if stem == "app_events":
                entry = _sourcemap_entry(entries, line) if entries else None
                error.update({"handler": entry["handler"], "sourceLine": entry["sourceLine"]} if entry else {})
            else:
                error.update({"module": stem, "sourceLine": line})
            errors.append(error)
    return errors


def map_error(error, sourcemap_path, modules=()):
    """Map an error in app_events.py back to its handler; one in a user module stays there, on the same line."""
    sourcemap = json.loads(Path(sourcemap_path).read_text(encoding="utf-8"))
    path = Path(error["file"]) if error.get("file") else None
    if path and path.suffix == ".py" and path.stem in modules:
        message = tr("{file}, line {line}: {detail}", file=path.name, line=error["line"], detail=error.get("detail") or tr("syntax error"))
        return {**error, "module": path.stem, "sourceLine": error["line"], "message": message}
    if not path or path.name != sourcemap["file"]: return error
    entry = next((entry for entry in sourcemap["entries"] if entry["line"] == error["line"]), None)
    if entry is None:
        previous = [entry for entry in sourcemap["entries"] if entry["line"] < error["line"]]
        entry = max(previous, key=lambda entry: entry["line"]) if previous else None
    return {**error, **({"handler": entry["handler"], "sourceLine": entry["sourceLine"]} if entry else {})}


class CompileError(Exception):
    def __init__(self, errors):
        super().__init__("\n".join(error["message"] for error in errors))
        self.errors = errors
