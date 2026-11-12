import hashlib
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess

from lvgl_mpy_studio.platform import CREATE_NO_WINDOW, IS_WINDOWS, exe_name, runtime_path
from .c_compiler import compile_c
from .compiler import cache_root, compile_python, default_mpy_cross, root_dir
from lvgl_mpy_studio.gen.gen_c import generate_c
from lvgl_mpy_studio.gen.project_gen import app_modules, generate_project

THIRD_PARTY_LICENSES = Path(__file__).parents[1] / "gen" / "output" / "licenses"


RUN_SH = '''#!/bin/sh
set -eu
cd "$(dirname "$0")"
unset LVSIM_SOCKET LVSIM_CONNECT LVSIM_TOKEN LVSIM_HEADLESS LVSIM_DUMP LVSIM_FRAMES LVSIM_TICK_MS
if [ "${1:-}" = "--selftest" ]; then
    LVSIM_HEADLESS=1
    LVSIM_FRAMES=1
    LVSIM_DUMP=selftest.raw
    export LVSIM_HEADLESS LVSIM_FRAMES LVSIM_DUMP
fi
exec "$@"
'''


def project_name(project):
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", project.projectName).strip("-.") or "project"


def output_name(project):
    suffix = "win64" if IS_WINDOWS else "x86_64"
    return f"{project_name(project)}-{suffix}"


def make_windows_gui(executable):
    path = Path(executable)
    data = bytearray(path.read_bytes())
    if len(data) < 64:
        raise ValueError(f"Invalid PE executable: {path}")
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    if pe + 26 > len(data) or data[pe:pe + 4] != b"PE\0\0":
        raise ValueError(f"Invalid PE header: {path}")
    optional = pe + 24
    if optional + 70 > len(data) or struct.unpack_from("<H", data, optional)[0] not in (0x10B, 0x20B):
        raise ValueError(f"Invalid PE optional header: {path}")
    subsystem = optional + 68
    if struct.unpack_from("<H", data, subsystem)[0] != 3:
        raise ValueError(f"The Windows runtime does not use the console subsystem: {path}")
    struct.pack_into("<H", data, subsystem, 2)
    path.write_bytes(data)


def _write_runner(directory, command):
    path = directory / "run.sh"
    path.write_text(RUN_SH.replace('exec "$@"', f"exec {command}"), encoding="utf-8", newline="\n")
    path.chmod(0o755)


def _frozen_runtime(generated):
    root = root_dir()
    sources = tuple(f"{name}.py" for name in app_modules(generated))
    digest = hashlib.sha256()
    for name in sources:
        digest.update((generated / name).read_bytes())
    build = cache_root() / "frozen" / digest.hexdigest()[:16]
    executable = build / exe_name("micropython")
    if not executable.exists():
        missing = [name for name in ("lvsim", "lvgl-bindings", "lvgl-micropython") if not (root / "runtime/modules" / name).exists()]
        if missing:
            raise RuntimeError(f"Runtime modules not found: {', '.join(missing)}. Run runtime/build.sh")
        manifest = generated / "manifest.py"
        manifest.write_text("freeze(\".\", (" + ", ".join(repr(name) for name in sources) + "))\n", encoding="utf-8", newline="\n")
        command = [
            "make", "-C", str(root / ".reference/micropython/ports/unix"), f"-j{os.cpu_count() or 2}",
            f"USER_C_MODULES={root / 'runtime/modules'}", f"BINDINGS_DIR={root / '.reference/lvgl-bindings'}",
            f"BUILD={build}", f"FROZEN_MANIFEST={manifest}",
        ]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=CREATE_NO_WINDOW)
        if result.returncode:
            raise RuntimeError(result.stderr[-12000:] or result.stdout[-12000:])
    return executable


ONEFILE_MAGIC = b"LMSAPP01"  # the launcher in runtime/onefile/lms_boot.py looks for the same


def onefile_runtime(windows=IS_WINDOWS):
    if windows:
        return root_dir() / "runtime" / "out-win64" / "lvsim-onefile.exe"
    return root_dir() / "runtime" / "out" / "lvsim-onefile"


def _app_image(generated):
    """Compiled modules in a ROMFS image, the format MicroPython mounts with vfs.VfsRom."""
    from mpremote.romfs import VfsRomWriter
    image = VfsRomWriter()
    for name in app_modules(generated):
        path = generated / f"{name}.mpy"
        image.mkfile(path.name, path.read_bytes())
    return image.finalise()


def build_single_file(project, dist_root=None, windows=None):
    """One executable to send to players: a prebuilt launcher with the game appended.

    No compiler on the PC of whoever builds the file: only mpy-cross is needed, as for the Debug
    profile. windows chooses the target system; normally it is the one the IDE runs on. The
    bytecode is the same, so Linux can also build the .exe for Windows, and the other way round.
    """
    windows = IS_WINDOWS if windows is None else windows
    stub = onefile_runtime(windows)
    if not stub.exists():
        script = "runtime/build_onefile_windows.sh" if windows else "runtime/build_onefile.sh"
        raise FileNotFoundError(f"Single-file launcher not found: run {script}")
    dist_root = Path(dist_root) if dist_root else root_dir() / "dist"
    target = dist_root / (project_name(project) + (".exe" if windows else ""))
    if target.is_dir():
        raise ValueError(f"A folder {target} already exists: move or rename it")
    dist_root.mkdir(parents=True, exist_ok=True)
    generated = dist_root / f".{target.name}-generated"
    temporary = target.with_name(f".{target.name}.tmp")
    try:
        generate_project(project, generated)
        compile_python(generated)
        image = _app_image(generated)
        temporary.write_bytes(stub.read_bytes())
        if windows:
            make_windows_gui(temporary)  # no console window next to the game
        with open(temporary, "ab") as stream:
            stream.write(image)
            stream.write(struct.pack("<Q", len(image)) + ONEFILE_MAGIC)
        temporary.chmod(0o755)
        if IS_WINDOWS and not windows:
            return _linux_archive(temporary, target)
        os.replace(temporary, target)
    finally:
        shutil.rmtree(generated, ignore_errors=True)
        temporary.unlink(missing_ok=True)
    return target


def _linux_archive(executable, target):
    """Windows has no execute permission: a .tar.gz carries it to Linux."""
    import tarfile
    archive = target.with_name(target.name + ".tar.gz")
    partial = archive.with_name(f".{archive.name}.tmp")
    with tarfile.open(partial, "w:gz") as bundle:
        info = bundle.gettarinfo(str(executable), arcname=target.name)
        info.mode = 0o755
        with open(executable, "rb") as stream:
            bundle.addfile(info, stream)
    os.replace(partial, archive)
    return archive


def build_micropython_release(project, dist_root=None, profile="debug"):
    if profile not in ("debug", "release"):
        raise ValueError(f"Unknown build profile: {profile}")
    if IS_WINDOWS and profile == "release":
        raise ValueError("The Release profile on Windows needs the MicroPython toolchain; use Debug")
    dist_root = Path(dist_root) if dist_root else root_dir() / "dist"
    output = dist_root / output_name(project)
    output.mkdir(parents=True, exist_ok=True)
    generated = output / "generated"
    shutil.rmtree(generated, ignore_errors=True)  # leftovers of an interrupted build
    generate_project(project, generated)
    runtime = runtime_path()
    if IS_WINDOWS:
        runtime = runtime.with_name(exe_name("lvsim-standalone"))
    if not runtime.exists() or not default_mpy_cross().exists():
        raise FileNotFoundError("Build the lvsim runtime and mpy-cross first")
    # A .mpy of a removed module would hide the ImportError, in Debug as in Release.
    for stale in output.glob("*.mpy"):
        stale.unlink()
    if profile == "release":
        runtime = _frozen_runtime(generated)
    else:
        compile_python(generated)
    runtime_name = exe_name(project_name(project)) if IS_WINDOWS else exe_name("lvsim-runtime")
    shutil.copy2(runtime, output / runtime_name)
    if IS_WINDOWS:
        sdl = runtime.parent / "SDL2.dll"
        if not sdl.exists():
            raise FileNotFoundError(f"DLL SDL2 mancante: {sdl}")
        shutil.copy2(sdl, output / "SDL2.dll")
        make_windows_gui(output / runtime_name)
    if profile == "debug":
        for name in app_modules(generated):
            source = generated / f"{name}.mpy"
            if not source.exists():
                raise FileNotFoundError(f"Compiled module missing: {source}")
            shutil.copy2(source, output / source.name)
    shutil.rmtree(generated)
    shutil.copytree(THIRD_PARTY_LICENSES, output / "licenses", dirs_exist_ok=True)
    if IS_WINDOWS:
        executable = output / runtime_name
        shutil.make_archive(str(output), "zip", root_dir=output.parent, base_dir=output.name)
        return executable
    _write_runner(output, f'./{runtime_name} -c "import main; main.main()"')
    return output / "run.sh"


def build_c_release(project, dist_root=None):
    dist_root = Path(dist_root) if dist_root else root_dir() / "dist"
    output = dist_root / output_name(project)
    output.mkdir(parents=True, exist_ok=True)
    generated = output / "generated"
    generate_c(project, generated)
    executable = compile_c(generated)
    app_name = exe_name(project_name(project)) if IS_WINDOWS else exe_name("app")
    shutil.copy2(executable, output / app_name)
    if IS_WINDOWS:
        sdl = runtime_path().parent / "SDL2.dll"
        if not sdl.exists():
            raise FileNotFoundError(f"DLL SDL2 mancante: {sdl}")
        shutil.copy2(sdl, output / "SDL2.dll")
        make_windows_gui(output / app_name)
    shutil.rmtree(generated)
    shutil.copytree(THIRD_PARTY_LICENSES, output / "licenses", dirs_exist_ok=True)
    if IS_WINDOWS:
        result = output / app_name
        shutil.make_archive(str(output), "zip", root_dir=output.parent, base_dir=output.name)
        return result
    _write_runner(output, f'./{app_name} "$@"')
    return output / "run.sh"


def build_release(project, target="micropython", dist_root=None, profile="debug", single_file=False, windows=None):
    if single_file:
        if target != "micropython" or profile != "release":
            raise ValueError("A single file needs the MicroPython target and the Release profile")
        return build_single_file(project, dist_root, windows)
    if target == "c":
        return build_c_release(project, dist_root)
    return build_micropython_release(project, dist_root, profile)
