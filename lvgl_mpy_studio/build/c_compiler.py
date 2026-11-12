import os
from pathlib import Path
import re
import shutil
import subprocess

from lvgl_mpy_studio.platform import CREATE_NO_WINDOW, IS_WINDOWS, exe_name
from .compiler import CompileError

TOOLCHAIN_HELP = "Windows C toolchain not found. Install MSYS2 MinGW64 or w64devkit and add gcc, ar and make to PATH; see https://github.com/skeeto/w64devkit and https://www.msys2.org/"


def parse_c_errors(output, directory=None):
    directory = Path(directory) if directory else None
    errors = []
    for line in output.splitlines():
        match = re.match(r"(.+?\.(?:c|h)):(\d+)(?::(\d+))?:\s+(?:error|warning):\s+(.*)", line)
        if not match:
            continue
        path = Path(match.group(1))
        if directory and not path.is_absolute():
            path = directory / path
        errors.append({"file": str(path), "line": int(match.group(2)), "column": int(match.group(3) or 1), "message": match.group(4)})
    if not errors and output.strip():
        errors.append({"file": None, "line": 1, "column": 1, "message": output.strip()})
    return errors


def windows_toolchain():
    directories = []
    configured = os.environ.get("LVGL_MPY_STUDIO_TOOLCHAIN")
    if configured:
        root = Path(configured)
        directories.extend((root, root / "bin"))
    directories.extend((Path(r"C:\msys64\mingw64\bin"), Path(r"C:\msys64\ucrt64\bin")))
    for directory in directories:
        if not directory.is_dir():
            continue
        tools = {name: directory / ("mingw32-make.exe" if name == "make" and (directory / "mingw32-make.exe").exists() else f"{name}.exe") for name in ("gcc", "ar", "make")}
        if all(tool.exists() for tool in tools.values()):
            return tools, str(directory)
    tools = {}
    for name in ("gcc", "ar", "make"):
        executable = shutil.which(name)
        if executable is None and name == "make":
            executable = shutil.which("mingw32-make")
        if executable is None:
            raise FileNotFoundError(TOOLCHAIN_HELP)
        tools[name] = Path(executable)
    return tools, None


def compile_c(directory, jobs=None):
    directory = Path(directory).resolve()
    command = ["make", "-C", str(directory), f"-j{jobs or os.cpu_count() or 2}"]
    environment = None
    if IS_WINDOWS:
        tools, toolchain_bin = windows_toolchain()
        command = [str(tools["make"]), "-C", str(directory), f"-j{jobs or os.cpu_count() or 2}", f"CC={tools['gcc'].as_posix()}", f"AR={tools['ar'].as_posix()}"]
        environment = os.environ.copy()
        if toolchain_bin:
            environment["PATH"] = toolchain_bin + os.pathsep + environment.get("PATH", "")
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment, creationflags=CREATE_NO_WINDOW)
    if result.returncode:
        raise CompileError(parse_c_errors(result.stderr + result.stdout, directory))
    return directory / exe_name("app")
