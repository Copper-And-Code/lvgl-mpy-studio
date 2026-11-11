import ast
import os
from pathlib import Path

from lvgl_mpy_studio import platform


ROOT = Path(__file__).parents[1]
CORE_DIRS = ("core", "gen", "build", "sim")
FORBIDDEN_IMPORTS = {"signal", "fcntl", "termios", "pty", "resource"}


def call_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = call_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def keyword(node, name):
    return next((item.value for item in node.keywords if item.arg == name), None)


def is_binary_mode(node):
    mode = node.args[1] if len(node.args) > 1 else keyword(node, "mode")
    return isinstance(mode, ast.Constant) and isinstance(mode.value, str) and "b" in mode.value


def portability_errors():
    errors = []
    for directory in CORE_DIRS:
        for path in sorted((ROOT / "lvgl_mpy_studio" / directory).rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                location = f"{path.relative_to(ROOT)}:{getattr(node, 'lineno', 1)}"
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.split(".")[0] in FORBIDDEN_IMPORTS:
                            errors.append(f"{location}: import vietato {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] in FORBIDDEN_IMPORTS:
                    errors.append(f"{location}: import vietato {node.module}")
                elif isinstance(node, ast.Call):
                    name = call_name(node.func)
                    if name == "os.fork":
                        errors.append(f"{location}: os.fork is not portable")
                    if keyword(node, "shell") is not None and isinstance(keyword(node, "shell"), ast.Constant) and keyword(node, "shell").value is True:
                        errors.append(f"{location}: shell=True vietato")
                    if name in {"open", "Path.open"} and not is_binary_mode(node) and keyword(node, "encoding") is None:
                        errors.append(f"{location}: text open without encoding")
                    if name in {"write_text", "Path.write_text", "tempfile.NamedTemporaryFile", "NamedTemporaryFile"}:
                        if keyword(node, "encoding") is None:
                            errors.append(f"{location}: text write without encoding")
                        if keyword(node, "newline") is None:
                            errors.append(f"{location}: text write without an explicit newline")
    return errors


def test_core_avoids_posix_apis_and_implicit_text_encodings():
    assert portability_errors() == []


def test_platform_executable_names(monkeypatch):
    monkeypatch.setattr(platform, "IS_WINDOWS", False)
    assert platform.exe_name("lvsim-runtime") == "lvsim-runtime"
    monkeypatch.setattr(platform, "IS_WINDOWS", True)
    assert platform.exe_name("lvsim-runtime") == "lvsim-runtime.exe"
    assert platform.exe_name("mpy-cross.exe") == "mpy-cross.exe"


def test_runtime_paths_use_windows_artifact_directory(monkeypatch, tmp_path):
    monkeypatch.setattr(platform, "IS_WINDOWS", True)
    assert platform.runtime_path(tmp_path) == tmp_path / "runtime/out-win64/lvsim-runtime.exe"
    assert platform.mpy_cross_path(tmp_path) == tmp_path / "runtime/out-win64/mpy-cross.exe"
    monkeypatch.setattr(platform, "IS_WINDOWS", False)
    assert platform.runtime_path(tmp_path) == tmp_path / "runtime/out/lvsim-runtime"
    assert platform.mpy_cross_path(tmp_path) == tmp_path / "runtime/out/mpy-cross"


def test_micropython_path_uses_platform_separator():
    assert platform.micropython_path("one", "two") == f"one{os.pathsep}two"
