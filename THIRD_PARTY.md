# Third-party components

The notices distributed with the application are in `packaging/NOTICE.txt`.

- **Qt and PySide6**: LGPL-3.0-only for the modules used; separate DLLs in the `_internal` folder. Sources: <https://code.qt.io/cgit/qt/> and <https://code.qt.io/cgit/pyside/pyside-setup.git/>. LGPL text: <https://www.gnu.org/licenses/lgpl-3.0.txt>.
- **FFmpeg**: LGPL-2.1 or later, included with Qt Multimedia for simulator sound; separate libraries in the package. Sources: <https://ffmpeg.org>.
- **SDL2**: zlib, <https://www.libsdl.org>.
- **LVGL**: MIT, <https://github.com/lvgl/lvgl>.
- **MicroPython**: MIT, <https://github.com/micropython/micropython>.
- **PyDevices lvgl-micropython / lvgl-bindings**: MIT, <https://github.com/PyDevices/lvgl-micropython> and <https://github.com/PyDevices/lvgl-bindings>.
- **mpremote**: MIT, <https://github.com/micropython/micropython>.
- **pyserial**: BSD-3-Clause, <https://github.com/pyserial/pyserial>.
- **QtAwesome and QtPy**: MIT, <https://github.com/spyder-ide/qtawesome> and <https://github.com/spyder-ide/qtpy>.
- **Material Design Icons 6.9.96**: Apache-2.0, <https://pictogrammers.com/library/mdi/>; IDE only. Only this font is packaged, not the others shipped with QtAwesome.
- **MinGW-w64 / GCC runtime**: <https://mingw-w64.org> and GCC Runtime Library Exception, <https://gcc.gnu.org/onlinedocs/libstdc++/manual/license.html>.
- **Python**: PSF License, <https://docs.python.org/3/license.html>.
- **Microsoft Visual C++ 2015-2022 Redistributable**: app-local runtime in the portable package, <https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist>.

MSYS2 and w64devkit are detected but neither included nor installed automatically. Pinned versions are in `docs/target.md` and `pyproject.toml`.

Full texts are in `packaging/licenses/` and `lvgl_mpy_studio/gen/output/licenses/`. The latter are also copied into executables built with the IDE, because those contain LVGL, MicroPython and SDL2. A single-file executable links SDL2 statically and carries the same texts inside, printed by `--licenses`.
