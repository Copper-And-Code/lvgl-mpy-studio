"""How much a project weighs: exact flash size and RAM measured in the simulator."""

import copy
import os
from pathlib import Path
import re
import subprocess
import tempfile

from lvgl_mpy_studio.build.compiler import CompileError, compile_python
from lvgl_mpy_studio.core.boards import compatible, portable_profile
from lvgl_mpy_studio.gen.board_gen import BoardSyntaxError, generate_board, precompile_board
from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.platform import CREATE_NO_WINDOW, RUNTIME_ENTRY, run_background, runtime_environment, runtime_path

MARKER = "\x1bLVIDE_BUDGET"
SETTLE_LOOPS = 15   # turns of the LVGL loop: enough for SCREEN_LOADED and the first timers
RUN_TIMEOUT = 5


def _instrument(source):
    """Measure the RAM of the app, without the video buffers the firmware has already allocated."""
    source = source.replace("import display_driver\n", "import display_driver\nimport gc\ngc.collect()\n_base = gc.mem_alloc()\n", 1)
    source, displays = re.subn(r"^( +)(display_driver\.init\([^\n]*\))$", r"\1_before = gc.mem_alloc()\n\1\2\n\1_display = gc.mem_alloc() - _before\n\1_loops = 0", source, count=1, flags=re.MULTILINE)
    probe = (
        "        _loops += 1\n"
        f"        if _loops >= {SETTLE_LOOPS}:\n"
        "            gc.collect()\n"
        f'            print("{MARKER.encode("unicode_escape").decode()}", gc.mem_alloc() - _base - _display)\n'
        "            raise SystemExit\n"
    )
    source, loops = re.subn(r"^        lv\.timer_handler\(\)\n", lambda match: match.group(0) + probe, source, count=1, flags=re.MULTILINE)
    return source if displays and loops else None


def _measure_ram(directory):
    main = directory / "main.py"
    source = _instrument(main.read_text(encoding="utf-8"))
    if source is None or not runtime_path().exists():
        return None
    main.write_text(source, encoding="utf-8", newline="\n")
    environment = runtime_environment(LVSIM_HEADLESS="1", LVSIM_TICK_MS="5")
    try:
        result = run_background([str(runtime_path()), *RUNTIME_ENTRY], RUN_TIMEOUT, cwd=directory, env=environment, text=True, encoding="utf-8", errors="replace", creationflags=CREATE_NO_WINDOW)
    except (OSError, subprocess.TimeoutExpired):
        return None
    match = re.search(re.escape(MARKER) + r" (-?\d+)", result.stdout)
    return max(0, int(match.group(1))) if match else None


def _measure_flash(project, simulator_dir, directory, board_mpy):
    if project.board and compatible(project, project.board):
        profile = portable_profile(project.board)
        generated = precompile_board(generate_board(project, profile, directory), directory, board_mpy)
        return sum((directory / name).stat().st_size for name in generated["files"])
    return sum(path.stat().st_size for path in simulator_dir.glob("*.mpy"))


def measure_budget(project, board_mpy=None):
    """Return {"flash": bytes, "ram": bytes or None}; None if the project does not compile."""
    with tempfile.TemporaryDirectory(prefix="lvgl-mpy-studio-budget-", ignore_cleanup_errors=True) as temporary:
        simulator = Path(temporary) / "simulator"
        try:
            generate_project(project, simulator)
            compile_python(simulator)
            local_mpy = (simulator / "ui.mpy").read_bytes()[1]
            flash = _measure_flash(project, simulator, Path(temporary) / "board", board_mpy if board_mpy is not None else local_mpy)
        except (CompileError, BoardSyntaxError, OSError, ValueError):
            return None
        # As before for ui and app_events; user modules go to the board as bytecode.
        for name in ["ui.py", "app_events.py", *(f"{module.name}.py" for module in project.modules)]:
            (simulator / name).unlink()
        return {"flash": flash, "ram": _measure_ram(simulator)}
