import os
from pathlib import Path
import subprocess

import pytest

from lvgl_mpy_studio.build.c_compiler import compile_c
from lvgl_mpy_studio.build.compiler import compile_python
from lvgl_mpy_studio.core.model import Project, widget_definitions
from lvgl_mpy_studio.gen.gen_c import generate_c
from lvgl_mpy_studio.gen.project_gen import generate_project

ROOT = Path(__file__).parents[1]
RUNTIME = ROOT / "runtime/out/lvsim-runtime"
LVGL = ROOT / ".reference/lvgl-bindings/lvgl"
pytestmark = pytest.mark.skipif(not RUNTIME.exists() or not LVGL.exists(), reason="runtime or native LVGL not available")


def render(command, directory, dump):
    env = os.environ.copy()
    env.update(LVSIM_HEADLESS="1", LVSIM_FRAMES="1", LVSIM_TICK_MS="0", LVSIM_DUMP=str(dump), MICROPYPATH=".")
    result = subprocess.run(command, cwd=directory, env=env, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    return dump.read_bytes()


@pytest.mark.parametrize("kind", list(widget_definitions()))
def test_pixel_parity_for_every_widget(tmp_path, kind):
    project = Project(f"parity_{kind}")
    project.add_widget(project.pages[0], kind, name=f"{kind}1")
    python_dir, c_dir = tmp_path / "py", tmp_path / "c"
    generate_project(project, python_dir)
    compile_python(python_dir)
    generate_c(project, c_dir)
    executable = compile_c(c_dir, jobs=4)
    python_frame = render([str(RUNTIME), "main.py"], python_dir, tmp_path / "python.raw")
    c_frame = render([str(executable)], c_dir, tmp_path / "c.raw")
    assert len(python_frame) == len(c_frame) == 800 * 480 * 2
    assert c_frame == python_frame


def test_c_selftest_argument(tmp_path):
    project = Project("selftest")
    project.add_widget(project.pages[0], "button")
    generate_c(project, tmp_path)
    executable = compile_c(tmp_path, jobs=4)
    result = subprocess.run([str(executable), "--selftest"], cwd=tmp_path, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "selftest.raw").stat().st_size == 800 * 480 * 2
