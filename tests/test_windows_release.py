import os
from pathlib import Path
import struct
import subprocess
import zipfile

import pytest

from lvgl_mpy_studio.build import release
from lvgl_mpy_studio.build.compiler import compile_python
from lvgl_mpy_studio.core.model import Project

ROOT = Path(__file__).parents[1]
STANDALONE = ROOT / "runtime/out-win64/lvsim-standalone.exe"


def project():
    result = Project("Progetto è")
    result.add_widget(result.pages[0], "button")
    return result


def pe_subsystem(executable):
    data = Path(executable).read_bytes()
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    assert data[pe:pe + 4] == b"PE\0\0"
    return struct.unpack_from("<H", data, pe + 24 + 68)[0]


def windows_package(tmp_path, monkeypatch, real=False):
    artifacts = ROOT / "runtime/out-win64"
    if not real:
        artifacts = tmp_path / "artifacts"
        artifacts.mkdir()
        for name in ("lvsim-runtime.exe", "lvsim-standalone.exe", "mpy-cross.exe", "SDL2.dll"):
            (artifacts / name).write_bytes(b"test artifact")
        monkeypatch.setattr(release, "make_windows_gui", lambda executable: None)

        def fake_compile(directory):
            for source in Path(directory).glob("*.py"):
                source.with_suffix(".mpy").write_bytes(b"test module")

        monkeypatch.setattr(release, "compile_python", fake_compile)
    else:
        compiler = artifacts / "mpy-cross.exe" if os.name == "nt" else ROOT / "runtime/out/mpy-cross"
        monkeypatch.setattr(release, "compile_python", lambda directory: compile_python(directory, compiler))
    monkeypatch.setattr(release, "IS_WINDOWS", True)
    monkeypatch.setattr(release, "exe_name", lambda name: name if str(name).lower().endswith(".exe") else f"{name}.exe")
    monkeypatch.setattr(release, "runtime_path", lambda: artifacts / "lvsim-runtime.exe")
    monkeypatch.setattr(release, "default_mpy_cross", lambda: artifacts / "mpy-cross.exe")
    return release.build_micropython_release(project(), tmp_path / "dist")


def test_windows_debug_package_layout_and_zip(tmp_path, monkeypatch):
    executable = windows_package(tmp_path, monkeypatch)
    output = executable.parent
    assert output.name == "Progetto-win64"
    assert executable.name == "Progetto.exe"
    assert (output / "SDL2.dll").exists()
    assert {path.name for path in output.glob("*.mpy")} == {"main.mpy", "ui.mpy", "app_events.mpy", "display_driver.mpy"}
    assert not (output / "run.sh").exists()
    assert not (output / "generated").exists()
    archive = output.with_suffix(".zip")
    with zipfile.ZipFile(archive) as package:
        names = package.namelist()
        assert f"{output.name}/{executable.name}" in names
        assert f"{output.name}/SDL2.dll" in names


def test_windows_release_requires_toolchain(tmp_path, monkeypatch):
    monkeypatch.setattr(release, "IS_WINDOWS", True)
    with pytest.raises(ValueError, match="MicroPython toolchain"):
        release.build_micropython_release(project(), tmp_path / "dist", profile="release")


def test_make_windows_gui_rejects_invalid_pe(tmp_path):
    executable = tmp_path / "invalid.exe"
    executable.write_bytes(b"not a PE file")
    with pytest.raises(ValueError, match="PE"):
        release.make_windows_gui(executable)


@pytest.mark.skipif(not (ROOT / "runtime/out-win64/lvsim-runtime.exe").exists(), reason="Windows runtime not built")
def test_windows_c_package_layout(tmp_path, monkeypatch):
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    (artifacts / "SDL2.dll").write_bytes(b"SDL2")
    runtime = ROOT / "runtime/out-win64/lvsim-runtime.exe"

    def fake_compile(directory):
        (Path(directory) / "app.exe").write_bytes(runtime.read_bytes())
        return Path(directory) / "app.exe"

    monkeypatch.setattr(release, "IS_WINDOWS", True)
    monkeypatch.setattr(release, "exe_name", lambda name: name if str(name).lower().endswith(".exe") else f"{name}.exe")
    monkeypatch.setattr(release, "runtime_path", lambda: artifacts / "lvsim-runtime.exe")
    monkeypatch.setattr(release, "compile_c", fake_compile)
    executable = release.build_c_release(project(), tmp_path / "dist")
    assert executable.name == "Progetto.exe"
    assert pe_subsystem(executable) == 2
    assert (executable.parent / "SDL2.dll").exists()
    assert executable.parent.with_suffix(".zip").exists()


@pytest.mark.skipif(not (ROOT / "runtime/out-win64/lvsim-runtime.exe").exists(), reason="Windows runtime not built")
def test_make_windows_gui_updates_pe_subsystem(tmp_path):
    executable = tmp_path / "app.exe"
    executable.write_bytes((ROOT / "runtime/out-win64/lvsim-runtime.exe").read_bytes())
    assert pe_subsystem(executable) == 3
    release.make_windows_gui(executable)
    assert pe_subsystem(executable) == 2


@pytest.mark.skipif(not STANDALONE.exists(), reason="Windows standalone runtime not built")
def test_windows_standalone_no_args_selftest_and_log(tmp_path, monkeypatch):
    executable = windows_package(tmp_path, monkeypatch, real=True)
    with zipfile.ZipFile(executable.parent.with_suffix(".zip")) as archive:
        archive.extractall(tmp_path / "extracted")
    output = tmp_path / "extracted" / executable.parent.name
    executable = output / executable.name
    command = [str(executable)] if os.name == "nt" else ["wine", str(executable)]
    env = os.environ.copy()
    for name in ("LVSIM_SOCKET", "LVSIM_CONNECT", "LVSIM_TOKEN", "LVSIM_HEADLESS", "LVSIM_DUMP", "LVSIM_FRAMES", "LVSIM_TICK_MS"):
        env.pop(name, None)
    env["WINEDEBUG"] = "-all"

    generated_main = (output / "main.mpy").read_bytes()
    (output / "main.py").write_text('def main():\n    print("NO_ARGS_OK")\n', encoding="utf-8", newline="\n")
    compiler = ROOT / "runtime/out-win64/mpy-cross.exe" if os.name == "nt" else ROOT / "runtime/out/mpy-cross"
    compile_python(output, compiler)
    result = subprocess.run(command, cwd=tmp_path, env=env, capture_output=True, encoding="utf-8", errors="replace", timeout=30)
    log = executable.with_suffix(".log")
    assert result.returncode == 0, result.stdout + result.stderr + (log.read_text(encoding="utf-8", errors="replace") if log.exists() else "")
    assert "NO_ARGS_OK" in log.read_text(encoding="utf-8", errors="replace")

    (output / "main.mpy").write_bytes(generated_main)
    (output / "main.py").unlink()
    result = subprocess.run(command + ["--selftest"], cwd=output, env=env, capture_output=True, encoding="utf-8", errors="replace", timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (output / "selftest.raw").stat().st_size == 800 * 480 * 2
