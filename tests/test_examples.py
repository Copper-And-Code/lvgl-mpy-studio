import json
import os
from pathlib import Path
import subprocess

import pytest

from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.gen.live import LIVE_OK, live_script
from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.platform import RUNTIME_ENTRY, runtime_path

ROOT = Path(__file__).parents[1] / "examples"
GAMES = ("tictactoe", "simon", "snake", "breakout")
SIZES = ((240, 240), (480, 480), (800, 480), (1024, 600))

pytestmark = pytest.mark.skipif(not runtime_path().exists(), reason="runtime not built")


def load(name, size):
    project = Project.from_dict(json.loads((ROOT / name / "project.json").read_text(encoding="utf-8")))
    project.set_display_size(*size)
    return project


def play(directory, frames=1):
    environment = {**os.environ, "MICROPYPATH": ".", "LVSIM_HEADLESS": "1", "LVSIM_FRAMES": str(frames), "LVSIM_TICK_MS": "20", "LVSIM_DUMP": "frame.raw"}
    for name in ("LVSIM_CONNECT", "LVSIM_TOKEN", "LVSIM_SOCKET"):
        environment.pop(name, None)
    done = subprocess.run([str(runtime_path()), *RUNTIME_ENTRY], cwd=directory, env=environment, capture_output=True, text=True, timeout=15)
    assert done.returncode == 0, done.stdout + done.stderr
    return done.stdout + done.stderr, (directory / "frame.raw").read_bytes()


@pytest.mark.parametrize("size", SIZES)
@pytest.mark.parametrize("name", GAMES)
def test_game_runs_at_any_resolution(tmp_path, name, size):
    generate_project(load(name, size), tmp_path)
    output, frame = play(tmp_path)
    assert "Traceback" not in output, output
    assert len(frame) == size[0] * size[1] * 2


@pytest.mark.parametrize("name", GAMES)
def test_game_survives_a_live_update(tmp_path, name):
    project = load(name, (480, 480))
    generate_project(project, tmp_path)
    (tmp_path / "live.py").write_text(live_script(project, 0), encoding="utf-8")
    main = tmp_path / "main.py"
    source = main.read_text(encoding="utf-8")
    marker = "\n    while display_driver.poll():"
    assert marker in source
    main.write_text(source.replace(marker, "\n    lv.timer_handler()\n    exec(open('live.py').read(), {})" + marker), encoding="utf-8")
    output, _frame = play(tmp_path, frames=2)
    assert LIVE_OK in output, output
    assert "Traceback" not in output, output
