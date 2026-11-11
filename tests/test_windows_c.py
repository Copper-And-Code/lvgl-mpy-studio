import os
from pathlib import Path
import shutil
import subprocess

import pytest

from lvgl_mpy_studio import platform
from lvgl_mpy_studio.build import c_compiler
from lvgl_mpy_studio.build.c_compiler import compile_c, parse_c_errors
from lvgl_mpy_studio.build.compiler import compile_python
from lvgl_mpy_studio.core.model import Project, widget_definitions
from lvgl_mpy_studio.gen.gen_c import generate_c
from lvgl_mpy_studio.gen.project_gen import generate_project

ROOT = Path(__file__).parents[1]
CROSS_CC = shutil.which("x86_64-w64-mingw32-gcc") or ROOT / "cache/w0-mingw/sysroot/usr/bin/x86_64-w64-mingw32-gcc"
CROSS_AR = shutil.which("x86_64-w64-mingw32-ar") or ROOT / "cache/w0-mingw/sysroot/usr/bin/x86_64-w64-mingw32-ar"
LIBLVGL = ROOT / "runtime/out-win64/liblvgl.a"
RUNTIME = ROOT / "runtime/out-win64/lvsim-runtime.exe"


def make_project(kind="button"):
    project = Project(f"windows_c_{kind}")
    project.add_widget(project.pages[0], kind, name=f"{kind}1")
    return project


def windows_c_available():
    return LIBLVGL.exists() and RUNTIME.exists() and (os.name == "nt" or Path(CROSS_CC).exists() if not shutil.which("x86_64-w64-mingw32-gcc") else True)


def test_windows_c_makefile_and_main_are_portable(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "IS_WINDOWS", True)
    generate_c(make_project(), tmp_path)
    makefile = (tmp_path / "Makefile").read_text(encoding="utf-8")
    main = (tmp_path / "main.c").read_text(encoding="utf-8")
    assert "lvsim_net_win32.c" in makefile
    assert "lvsim_time_win32.c" in makefile
    assert "-lws2_32 -lwinmm" in makefile
    assert "lvsim_time_ms()" in main
    assert "lvsim_wait(5)" in main
    assert "clock_gettime" not in main
    assert "nanosleep" not in main


def test_windows_c_error_path_and_missing_toolchain(monkeypatch, tmp_path):
    error = parse_c_errors(r"C:\Users\Nunzio Raciti\Progetto è\main.c:12:4: error: prova")[0]
    assert error["line"] == 12
    assert error["column"] == 4
    assert error["file"].endswith("main.c")
    monkeypatch.setattr(c_compiler, "IS_WINDOWS", True)
    monkeypatch.setattr(c_compiler, "windows_toolchain", lambda: (_ for _ in ()).throw(FileNotFoundError(c_compiler.TOOLCHAIN_HELP)))
    with pytest.raises(FileNotFoundError, match="MSYS2"):
        compile_c(tmp_path)


def build_windows_c(directory, monkeypatch=None):
    if monkeypatch:
        monkeypatch.setattr(platform, "IS_WINDOWS", True)
    generate_c(make_project(), directory)
    if os.name == "nt":
        executable = compile_c(directory, jobs=4)
    else:
        environment = os.environ.copy()
        environment["PATH"] = str(ROOT / "cache/w0-mingw/sysroot/usr/bin") + os.pathsep + environment.get("PATH", "")
        result = subprocess.run(["make", "-C", str(directory), "-j4", "OS=Windows_NT", f"CC={CROSS_CC}", f"AR={CROSS_AR}"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment, timeout=120)
        assert result.returncode == 0, result.stdout + result.stderr
        executable = directory / "app.exe"
    shutil.copy2(ROOT / "runtime/out-win64/SDL2.dll", directory / "SDL2.dll")
    return executable


def render(command, directory, dump):
    env = os.environ.copy()
    env.update(LVSIM_HEADLESS="1", LVSIM_FRAMES="1", LVSIM_TICK_MS="0", LVSIM_DUMP=str(dump), MICROPYPATH=".", WINEDEBUG="-all")
    result = subprocess.run(command, cwd=directory, env=env, capture_output=True, encoding="utf-8", errors="replace", timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    return dump.read_bytes()


def windows_command(executable):
    return [str(executable)] if os.name == "nt" else ["wine", str(executable)]


@pytest.mark.skipif(not windows_c_available(), reason="runtime, liblvgl or Windows cross-compiler not available")
def test_windows_c_selftest_unicode_path(tmp_path, monkeypatch):
    output = tmp_path / "Nunzio Raciti" / "Progetto è" / "build c"
    executable = build_windows_c(output, monkeypatch)
    (output / "selftest.raw").unlink(missing_ok=True)
    result = subprocess.run(windows_command(executable) + ["--selftest"], cwd=output, env={**os.environ, "WINEDEBUG": "-all"}, capture_output=True, encoding="utf-8", errors="replace", timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (output / "selftest.raw").stat().st_size == 800 * 480 * 2
    assert executable.with_suffix(".log").exists()


@pytest.mark.skipif(not windows_c_available(), reason="runtime, liblvgl or Windows cross-compiler not available")
@pytest.mark.parametrize("kind", list(widget_definitions()))
def test_windows_c_python_and_linux_parity(tmp_path, monkeypatch, kind):
    project = make_project(kind)
    c_dir = tmp_path / "c"
    monkeypatch.setattr(platform, "IS_WINDOWS", True)
    generate_c(project, c_dir)
    if os.name == "nt":
        executable = compile_c(c_dir, jobs=4)
    else:
        environment = os.environ.copy()
        environment["PATH"] = str(ROOT / "cache/w0-mingw/sysroot/usr/bin") + os.pathsep + environment.get("PATH", "")
        result = subprocess.run(["make", "-C", str(c_dir), "-j4", "OS=Windows_NT", f"CC={CROSS_CC}", f"AR={CROSS_AR}"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment, timeout=120)
        assert result.returncode == 0, result.stdout + result.stderr
        executable = c_dir / "app.exe"
    shutil.copy2(ROOT / "runtime/out-win64/SDL2.dll", c_dir / "SDL2.dll")
    c_frame = render(windows_command(executable), c_dir, tmp_path / "c-windows.raw")

    python_dir = tmp_path / "py"
    generate_project(project, python_dir)
    compile_python(python_dir, ROOT / "runtime/out-win64/mpy-cross.exe" if os.name == "nt" else ROOT / "runtime/out/mpy-cross")
    windows_frame = render(windows_command(RUNTIME) + ["main.py"], python_dir, tmp_path / "python-windows.raw")
    assert c_frame == windows_frame
    if os.name != "nt":
        linux_frame = render([str(ROOT / "runtime/out/lvsim-runtime"), "main.py"], python_dir, tmp_path / "python-linux.raw")
        assert c_frame == linux_frame
