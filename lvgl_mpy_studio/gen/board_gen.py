import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from lvgl_mpy_studio.build.compiler import default_mpy_cross
from lvgl_mpy_studio.core.boards import ADAPTERS, compatible, portable_profile, profile_fonts, validate_profile
from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.core.modules import module_files
from lvgl_mpy_studio.core.validation import validate_project
from .gen_python import build_project_code
from .components import BUZZER_MODULE, block_files
from .project_gen import design_warnings, generate_app_events, legacy_data, screen_statements, ui_source


PRECOMPILED = ("ui.py", "app_events.py", f"{BUZZER_MODULE}.py")


def _board_main(project, model, profile):
    initial = project.initial_page_index()
    lines = [
        "import sys",
        "import display_driver",
        "import lvgl as lv",
        f"if (display_driver.WIDTH, display_driver.HEIGHT) != ({profile['logicalWidth']}, {profile['logicalHeight']}):",
        f"    raise RuntimeError('UI requires {profile['logicalWidth']}x{profile['logicalHeight']}')",
        "APP_DIR = __file__.rsplit('/', 1)[0] if '/' in __file__ else '.'",
        "if APP_DIR not in sys.path:",
        "    sys.path.insert(0, APP_DIR)",
        "import ui",
        "import app_events",
        "",
    ]
    lines.extend(screen_statements(project, model))
    lines.extend([
        f"lv.screen_load(ui.screens[{initial}])",
        f"ui.current_screen = {initial}",
        "display_driver.start()",
        "print('LVGL_MPY_STUDIO_APP_READY buffers=%s touch=%s' % (display_driver.BUFFERS, display_driver.indev is not None))",
        "",
    ])
    return "\n".join(lines)


def _memory_warnings(project):
    warnings = []
    for widget in project.widgets:
        keys = set(widget.props) | set(widget.customStyles)
        if any(any(token in key.lower() for token in ("transform", "blend")) for key in keys):
            warnings.append(tr("Warning: {warning}", warning=tr("{name}: transforms/blending may allocate large ARGB8888 layers on the board", name=widget.name)))
        for key in keys:
            if "opa" in key.lower() and key.lower() not in {"opacity"}:
                value = widget.props.get(key, widget.customStyles.get(key))
                if isinstance(value, (int, float)) and value < 255:
                    warnings.append(tr("Warning: {warning}", warning=tr("{name}: opacity may allocate an ARGB8888 layer on the board", name=widget.name)))
    return warnings


class BoardSyntaxError(ValueError):
    def __init__(self, errors):
        super().__init__("device.syntax")
        self.code = "device.syntax"
        self.errors = errors


def _validate_sources(files, sourcemap):
    errors = []
    entries = {entry["line"]: entry for entry in sourcemap["entries"]}
    for name, source in files.items():
        if not name.endswith(".py"):
            continue
        try:
            compile(source, name, "exec")
        except SyntaxError as exc:
            # Only app_events.py has a source map: a user module is written as it is.
            mapped = entries.get(exc.lineno, {}) if name == "app_events.py" else {"sourceLine": exc.lineno or 1, "module": name[:-3]}
            errors.append({"file": name, "line": exc.lineno or 1, "column": exc.offset or 1, "message": exc.msg, "handler": mapped.get("handler"), "module": mapped.get("module"), "sourceLine": mapped.get("sourceLine", exc.lineno or 1)})
    if errors:
        raise BoardSyntaxError(errors)
    compiler = default_mpy_cross()
    if not compiler.is_file():
        return
    with tempfile.TemporaryDirectory(prefix="lvgl-mpy-studio-syntax-") as directory:
        for name, source in files.items():
            if not name.endswith(".py"):
                continue
            path = Path(directory) / name
            path.write_text(source, encoding="utf-8", newline="\n")
            result = subprocess.run([str(compiler), "-o", str(Path(directory) / (name + ".mpy")), str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
            if result.returncode:
                output = (result.stderr + result.stdout).strip()
                match = re.search(r":(\d+):(\d+)", output)
                line, column = (int(match.group(1)), int(match.group(2))) if match else (1, 1)
                mapped = entries.get(line, {}) if name == "app_events.py" else {"sourceLine": line, "module": name[:-3]}
                raise BoardSyntaxError([{"file": name, "line": line, "column": column, "message": output, "handler": mapped.get("handler"), "module": mapped.get("module"), "sourceLine": mapped.get("sourceLine", line)}])


def _bytecode_file(source, target):
    """Compile source into target and return the bytes, or None if it cannot be done."""
    compiler = default_mpy_cross()
    if not compiler.is_file():
        return None
    result = subprocess.run([str(compiler), "-s", source.name, "-o", str(target), str(source)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return target.read_bytes() if result.returncode == 0 and target.is_file() else None


def precompile_board(generated, output_dir, board_mpy):
    """Replace the source with bytecode if the firmware accepts it.

    board_mpy is sys.implementation._mpy: the low byte is the format version,
    the only one that matters for pure bytecode. Without a match the source stays.
    """
    output = Path(output_dir)
    compiled = {}
    if isinstance(board_mpy, int):
        for name in (item for item in generated.get("precompile", PRECOMPILED) if item in generated["files"]):
            target = output / (name[:-3] + ".mpy")
            data = _bytecode_file(output / name, target)
            if not data or data[:1] != b"M" or data[1] != board_mpy & 0xFF:
                compiled = {}
                break
            compiled[name] = (target.name, data)
    if not compiled:
        return {**generated, "warnings": [*generated["warnings"], tr("Firmware without compatible bytecode: source uploaded, slower startup.")]}
    files = [compiled[name][0] if name in compiled else name for name in generated["files"]]
    manifest = {**generated["manifest"], "files": dict(generated["manifest"]["files"])}
    for name, (target, data) in compiled.items():
        del manifest["files"][name]
        manifest["files"][target] = hashlib.sha256(data).hexdigest()
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    return {**generated, "files": files, "manifest": manifest}


def _exported_files(directory):
    """Files listed by the previous export: {name: hash}. The manifest may have been edited by hand."""
    try:
        files = json.loads((Path(directory) / "manifest.json").read_text(encoding="utf-8"))["files"]
        return {name: digest for name, digest in files.items() if Path(name).name == name}
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return {}


def changed_exports(directory):
    """Files of a previous export that are no longer as they were generated."""
    output = Path(directory)
    return sorted(name for name, digest in _exported_files(directory).items() if (output / name).is_file() and hashlib.sha256((output / name).read_bytes()).hexdigest() != digest)


def export_board(project, profile, directory):
    """Sources for the board, in a stable folder. Files no longer needed are removed."""
    previous = _exported_files(directory)
    generated = generate_board(project, profile, directory)
    for name in set(previous) - set(generated["files"]):
        (Path(directory) / name).unlink(missing_ok=True)
    return generated


def generate_board(project, profile, output_dir, fonts=None):
    warnings = validate_project(project) + design_warnings(project)
    profile = portable_profile(profile)
    validate_profile(profile)
    if profile["adapter"] not in ADAPTERS:
        raise ValueError("device.adapter.unavailable")
    if not compatible(project, profile):
        raise ValueError(f"device.resolution:{profile['logicalWidth']}x{profile['logicalHeight']}")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    data = legacy_data(project)
    model = build_project_code(data)
    app_source, sourcemap = generate_app_events(project)
    files = {
        "ui.py": ui_source(data, project.to_dict(), fonts=fonts or profile_fonts(profile)),
        "app_events.py": app_source,
        "app_main.py": _board_main(project, model, profile),
        "sourcemap.json": json.dumps(sourcemap, indent=2) + "\n",
        "board_profile.json": json.dumps(profile, ensure_ascii=False, indent=2) + "\n",
        "board_adapter.py": f"ADAPTER = {profile['adapter']!r}\nLOGICAL_SIZE = ({profile['logicalWidth']}, {profile['logicalHeight']})\nPHYSICAL_SIZE = ({profile['physicalWidth']}, {profile['physicalHeight']})\nSCALE = {profile['scale']}\n",
    }
    block_modules, extra_warnings = block_files(project.to_dict(), profile)
    files.update(block_modules)
    user_modules = module_files(project)
    files.update(user_modules)
    _validate_sources(files, sourcemap)
    for name, source in files.items():
        (output / name).write_text(source, encoding="utf-8", newline="\n")
    manifest = {"schemaVersion": 1, "entryPoint": "app_main.py", "profileId": profile["id"], "profileRevision": profile["revision"], "files": {name: hashlib.sha256(source.encode("utf-8")).hexdigest() for name, source in files.items()}}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    precompile = [name for name in PRECOMPILED if name in files] + [name for name in block_modules if name not in PRECOMPILED] + list(user_modules)
    return {"files": list(files) + ["manifest.json"], "warnings": warnings + extra_warnings + _memory_warnings(project), "manifest": manifest, "sourcemap": sourcemap, "profile": profile, "precompile": precompile}
