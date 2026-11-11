import os
from pathlib import Path
import shutil
import subprocess

import pytest

from lvgl_mpy_studio.build.release import build_c_release, build_micropython_release
from lvgl_mpy_studio.cli import main
from lvgl_mpy_studio.core.model import Project

ROOT = Path(__file__).parents[1]
pytestmark = pytest.mark.skipif(not (ROOT / "runtime/out/lvsim-runtime").exists(), reason="native runtime not built")


def project():
    result = Project("release_test")
    result.add_widget(result.pages[0], "button")
    return result


@pytest.mark.parametrize("target,builder", [("micropython", build_micropython_release), ("c", build_c_release)])
def test_standalone_release_selftest(tmp_path, target, builder):
    runner = builder(project(), tmp_path / "dist")
    assert runner.parent.name == "release_test-x86_64"
    result = subprocess.run([str(runner), "--selftest"], cwd=runner.parent, capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, result.stderr
    assert (runner.parent / "selftest.raw").stat().st_size == 800 * 480 * 2
    assert (runner.parent / "licenses" / "LVGL.txt").exists()
    assert (runner.parent / "licenses" / "MicroPython.txt").exists()
    assert not (runner.parent / "generated").exists()


def test_cli_generate_and_build(tmp_path):
    path = tmp_path / "project.json"
    project().save(path)
    output = tmp_path / "generated"
    assert main(["generate", str(path), "--target", "c", "--output", str(output)]) == 0
    assert (output / "app").exists()
    dist = tmp_path / "dist"
    assert main(["build", str(path), "--target", "c", "--output", str(dist)]) == 0
    assert (dist / "release_test-x86_64/run.sh").exists()


def test_frozen_release_selftest(tmp_path):
    runner = build_micropython_release(project(), tmp_path / "dist", profile="release")
    assert not list(runner.parent.glob("*.mpy"))
    result = subprocess.run([str(runner), "--selftest"], cwd=runner.parent, capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, result.stderr
    assert (runner.parent / "selftest.raw").stat().st_size == 800 * 480 * 2


def test_frozen_build_refuses_missing_runtime_modules(tmp_path, monkeypatch):
    from lvgl_mpy_studio.build import release

    monkeypatch.setattr(release, "root_dir", lambda: tmp_path)
    monkeypatch.setattr(release, "cache_root", lambda: tmp_path / "cache")
    for name in ("main.py", "ui.py", "app_events.py", "display_driver.py"):
        (tmp_path / name).write_text("", encoding="utf-8")
    # The list of modules to freeze comes from the manifest generate_project writes.
    (tmp_path / "manifest.json").write_text('{"modules": ["main", "ui", "app_events", "display_driver"], "files": {}}', encoding="utf-8")
    with pytest.raises(RuntimeError, match="lvsim"):
        release._frozen_runtime(tmp_path)



needs_onefile = pytest.mark.skipif(not (ROOT / "runtime/out/lvsim-onefile").exists(), reason="single-file launcher not built: runtime/build_onefile.sh")


def test_single_file_needs_release_and_micropython(tmp_path):
    from lvgl_mpy_studio.build.release import build_release

    with pytest.raises(ValueError, match="Release"):
        build_release(project(), "micropython", tmp_path, "debug", single_file=True)
    with pytest.raises(ValueError, match="MicroPython"):
        build_release(project(), "c", tmp_path, "release", single_file=True)


def test_single_file_without_launcher_says_how_to_get_it(tmp_path, monkeypatch):
    from lvgl_mpy_studio.build import release

    monkeypatch.setattr(release, "onefile_runtime", lambda windows: tmp_path / "missing")
    with pytest.raises(FileNotFoundError, match="build_onefile.sh"):
        release.build_single_file(project(), tmp_path / "dist", windows=False)
    with pytest.raises(FileNotFoundError, match="build_onefile_windows.sh"):
        release.build_single_file(project(), tmp_path / "dist", windows=True)


@needs_onefile
def test_single_file_does_not_replace_a_folder(tmp_path):
    from lvgl_mpy_studio.build.release import build_single_file

    (tmp_path / "dist" / "release_test").mkdir(parents=True)
    with pytest.raises(ValueError, match="release_test"):
        build_single_file(project(), tmp_path / "dist")
    assert [item.name for item in (tmp_path / "dist").iterdir()] == ["release_test"]


@needs_onefile
def test_single_file_runs_alone(tmp_path):
    path = tmp_path / "project.json"
    project().save(path)
    assert main(["build", str(path), "--profile", "release", "--single-file", "--output", str(tmp_path / "dist")]) == 0
    executable = tmp_path / "dist" / "release_test"
    assert [item.name for item in (tmp_path / "dist").iterdir()] == ["release_test"]
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    for name in ("main.py", "lvgl_ide_boot.py"):
        (elsewhere / name).write_text("print('FAKE')\nraise SystemExit(3)\n", encoding="utf-8")
    result = subprocess.run([str(executable), "--selftest"], cwd=elsewhere, capture_output=True, text=True, timeout=20)
    assert result.returncode == 0 and "FAKE" not in result.stdout, result.stdout + result.stderr
    assert (elsewhere / "selftest.raw").stat().st_size == 800 * 480 * 2
    licenses = subprocess.run([str(executable), "--licenses"], capture_output=True, text=True, timeout=20).stdout
    assert "===== SDL2 =====" in licenses and "===== LVGL =====" in licenses
    libraries = subprocess.run(["ldd", str(executable)], capture_output=True, text=True).stdout
    assert "libSDL2" not in libraries and "libffi" not in libraries


@needs_onefile
def test_single_file_starts_from_the_path(tmp_path):
    path = tmp_path / "project.json"
    project().save(path)
    assert main(["build", str(path), "--profile", "release", "--single-file", "--output", str(tmp_path / "bin")]) == 0
    environment = {**os.environ, "PATH": f"{tmp_path / 'bin'}{os.pathsep}{os.environ['PATH']}"}
    result = subprocess.run(["release_test", "--selftest"], cwd=tmp_path, env=environment, capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, result.stdout + result.stderr


@needs_onefile
def test_launcher_alone_explains_itself(tmp_path):
    result = subprocess.run([str(ROOT / "runtime/out/lvsim-onefile")], cwd=tmp_path, capture_output=True, text=True, timeout=20)
    assert result.returncode != 0 and "No app attached" in result.stdout + result.stderr


needs_windows_onefile = pytest.mark.skipif(not (ROOT / "runtime/out-win64/lvsim-onefile.exe").exists() or shutil.which("wine") is None, reason="lanciatore Windows a file unico o Wine mancanti")


def test_windows_single_file_has_its_own_name_and_no_console(tmp_path, monkeypatch):
    from lvgl_mpy_studio.build import release

    stub = tmp_path / "stub.exe"
    stub.write_bytes(windows_stub())
    monkeypatch.setattr(release, "onefile_runtime", lambda windows: stub if windows else tmp_path / "missing")
    executable = release.build_single_file(project(), tmp_path / "dist", windows=True)
    assert executable.name == "release_test.exe"
    data = executable.read_bytes()
    pe = int.from_bytes(data[0x3C:0x40], "little")
    assert int.from_bytes(data[pe + 24 + 68:pe + 24 + 70], "little") == 2  # graphical subsystem
    assert data.endswith(release.ONEFILE_MAGIC)


def windows_stub():
    """A minimal PE, enough for the subsystem change."""
    data = bytearray(512)
    data[0:2] = b"MZ"
    data[0x3C:0x40] = (64).to_bytes(4, "little")
    data[64:68] = b"PE\0\0"
    data[64 + 24:64 + 26] = (0x20B).to_bytes(2, "little")
    data[64 + 24 + 68:64 + 24 + 70] = (3).to_bytes(2, "little")
    return bytes(data)


@needs_windows_onefile
def test_windows_single_file_runs_under_wine(tmp_path):
    path = tmp_path / "project.json"
    project().save(path)
    assert main(["build", str(path), "--profile", "release", "--single-file", "--for", "windows", "--output", str(tmp_path / "dist")]) == 0
    executable = tmp_path / "dist" / "release_test.exe"
    (executable.parent / "main.py").write_text("print('FAKE')\nraise SystemExit(3)\n", encoding="utf-8")
    result = subprocess.run(["wine", str(executable), "--selftest"], cwd=tmp_path, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr
    assert (executable.parent / "selftest.raw").stat().st_size == 800 * 480 * 2
    assert "FAKE" not in (executable.parent / "release_test.log").read_text(encoding="utf-8", errors="replace")


def test_a_linux_game_built_on_windows_keeps_its_execute_permission(tmp_path, monkeypatch):
    import tarfile
    from lvgl_mpy_studio.build import release

    stub = tmp_path / "stub"
    stub.write_bytes(b"\x7fELF stub")
    monkeypatch.setattr(release, "IS_WINDOWS", True)
    monkeypatch.setattr(release, "onefile_runtime", lambda windows: stub)
    archive = release.build_single_file(project(), tmp_path / "dist", windows=False)
    assert archive.name == "release_test.tar.gz"
    with tarfile.open(archive) as bundle:
        [member] = bundle.getmembers()
    assert member.name == "release_test" and member.mode & 0o111
    assert [path.name for path in (tmp_path / "dist").iterdir()] == ["release_test.tar.gz"]
