# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
# Start of the single-file executable: the game is a ROMFS image appended to the binary.
import os
import sys
import vfs

MAGIC = b"LVGLIDE1"


def _image():
    with open(os.getenv("LVSIM_SELF") or sys.executable, "rb") as stream:
        stream.seek(-16, 2)
        trailer = stream.read(16)
        if trailer[8:] != MAGIC:
            raise SystemExit("No app attached to this runtime: build it with LVGL IDE")
        size = int.from_bytes(trailer[:8], "little")
        stream.seek(-16 - size, 2)
        return stream.read(size)


vfs.mount(vfs.VfsRom(_image()), "/app")
sys.path[:] = ["/app", ".frozen"]
import main  # noqa: E402

main.main()
