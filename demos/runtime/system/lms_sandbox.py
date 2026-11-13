# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Nunzio Raciti
"""A folder of the PC as the root filesystem of a simulated board.

os.VfsPosix(folder) alone lets "/.." out of the folder. This one resolves every path itself,
so that "..", absolute paths and `rm -r /` stay inside: a program sees only its flash.
"""
import os


def normalize(path, cwd="/"):
    """The absolute form of path inside the root: '..' stops at '/'."""
    parts = [] if path.startswith("/") else [part for part in cwd.split("/") if part]
    for part in path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
        else:
            parts.append(part)
    return "/" + "/".join(parts)


class SandboxVfs:
    def __init__(self, folder):
        self._fs = os.VfsPosix(folder)
        self._cwd = "/"

    def _path(self, path):
        return normalize(path, self._cwd)

    def mount(self, readonly, mkfs):
        pass

    def umount(self):
        pass

    def ilistdir(self, path):
        return self._fs.ilistdir(self._path(path))

    def chdir(self, path):
        target = self._path(path)
        if not self._fs.stat(target)[0] & 0x4000:
            raise OSError(20)  # ENOTDIR
        self._cwd = target

    def getcwd(self):
        return self._cwd

    def mkdir(self, path):
        self._fs.mkdir(self._path(path))

    def remove(self, path):
        self._fs.remove(self._path(path))

    def rename(self, old, new):
        self._fs.rename(self._path(old), self._path(new))

    def rmdir(self, path):
        target = self._path(path)
        if target == "/":
            raise OSError(16)  # EBUSY: the root of the flash stays
        self._fs.rmdir(target)

    def stat(self, path):
        return self._fs.stat(self._path(path))

    def statvfs(self, path):
        return self._fs.statvfs(self._path(path))

    def open(self, path, mode):
        return self._fs.open(self._path(path), mode)
