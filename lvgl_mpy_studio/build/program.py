"""Programs without pages in the simulator: a folder of .py files run as on a board.

The folder of the chosen file is copied into a flash of its own, kept between runs as a board
keeps its files, and the simulator starts from a separate folder with the board-like modules of
runtime/program. Projects with pages never come here.
"""

import hashlib
from pathlib import Path
import shutil

from lvgl_mpy_studio.platform import config_dir, root_dir

# The heap of the unix port is 2 MB by default; boards with a display have far more (28 MB on the STM32H7_CORE),
# and a terminal on the display keeps copies of the framebuffer.
HEAP = "32M"
PROGRAM_ENTRY = ["-X", f"heapsize={HEAP}", "-c", "import lms_program_boot"]
RESET_EXIT_CODE = 75  # machine.reset() in the simulator: see runtime/program/machine.py
SKIPPED = {"__pycache__", ".git", ".hg", ".svn", ".venv", "node_modules"}
MAX_BYTES = 64 * 1024 * 1024  # a folder larger than this is not a program for a board
PROGRAM_BOARD = "stm32h7_core_v1_3_1024x600"  # every program runs as this board, whatever project is open


def program_board():
    """The board a program runs as: (id, width, height)."""
    from lvgl_mpy_studio.core.boards import builtin_profiles

    board = next(profile for profile in builtin_profiles() if profile["id"] == PROGRAM_BOARD)
    return board["id"], board["logicalWidth"], board["logicalHeight"]


def program_dir(folder):
    """Where the simulator keeps what belongs to the program of this folder."""
    key = hashlib.sha256(str(Path(folder).resolve()).encode("utf-8")).hexdigest()[:12]
    return config_dir() / "simulator" / key


def flash_dir(folder):
    return program_dir(folder) / "flash"


def _files(folder):
    for path in sorted(Path(folder).rglob("*")):
        relative = path.relative_to(folder)
        if any(part in SKIPPED or part.startswith(".") for part in relative.parts):
            continue
        if path.is_file():
            yield path, relative


def copy_program(folder, flash):
    """The files of the folder into the flash, as an upload: they replace those of the same name, the others stay."""
    files = list(_files(folder))
    size = sum(path.stat().st_size for path, _relative in files)
    if size > MAX_BYTES:
        raise ValueError(f"The folder holds {size // (1024 * 1024)} MB: a program for a board is smaller. Choose the folder of the program alone.")
    for path, relative in files:
        target = flash / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    return [str(relative) for _path, relative in files]


def prepare_program(entry, width, height, board="simulator", runtime_dir=None):
    """Prepare a run of entry, a .py file: returns the folder to start from and the environment."""
    entry = Path(entry).resolve()
    if entry.suffix != ".py" or not entry.is_file():
        raise ValueError(f"Not a Python file: {entry}")
    folder = entry.parent
    base = program_dir(folder)
    boot, flash = base / "boot", base / "flash"
    shutil.rmtree(boot, ignore_errors=True)
    boot.mkdir(parents=True)
    flash.mkdir(parents=True, exist_ok=True)
    (base / "source.txt").write_text(str(folder) + "\n", encoding="utf-8", newline="\n")
    source = Path(runtime_dir) if runtime_dir else root_dir() / "runtime" / "program"
    for module in sorted(source.glob("*.py")):
        shutil.copyfile(module, boot / module.name)
    copy_program(folder, flash)
    environment = {
        "LVSIM_WIDTH": str(width),
        "LVSIM_HEIGHT": str(height),
        "LMS_FLASH": str(flash),
        "LMS_ENTRY": entry.name,
        "LMS_BOARD": board or "simulator",
    }
    return {"boot": boot, "flash": flash, "environment": environment, "arguments": PROGRAM_ENTRY}


def reset_flash(folder):
    """Empty the flash of the program of this folder, as erasing a board."""
    shutil.rmtree(flash_dir(folder), ignore_errors=True)
