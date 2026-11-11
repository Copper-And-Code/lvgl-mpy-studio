#!/usr/bin/env bash
# Single-file launcher for Windows: SDL is inside the executable, so no SDL2.dll next to it.
# Needs MinGW-w64 and SDL2 for MinGW, like runtime/build_windows.sh, which must run first.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEPS="$ROOT/.reference"
OUT="$ROOT/runtime/out-win64"
BUILD="$OUT/build-onefile"
JOBS=${JOBS:-4}
SDL_DIR=${SDL2_DIR:-"$ROOT/cache/sdl2/SDL2-2.30.9/x86_64-w64-mingw32"}
if ! command -v x86_64-w64-mingw32-gcc >/dev/null 2>&1; then
    export PATH="$ROOT/cache/w0-mingw/sysroot/usr/bin:$PATH"
fi
test -f "$SDL_DIR/lib/libSDL2.a" || { echo "SDL2 for MinGW not found: run runtime/build_windows.sh" >&2; exit 1; }
mkdir -p "$BUILD/frozen"
cp "$ROOT/runtime/onefile/lvgl_ide_boot.py" "$ROOT/runtime/onefile/manifest.py" "$BUILD/frozen/"
python3 - "$ROOT/lvgl_mpy_studio/gen/output/licenses" "$BUILD/frozen/lvgl_ide_licenses.py" <<'PY'
import pathlib, sys
texts = [f"===== {path.stem} =====\n{path.read_text(encoding='utf-8')}" for path in sorted(pathlib.Path(sys.argv[1]).glob("*.txt"))]
pathlib.Path(sys.argv[2]).write_text(f"print({chr(10).join(texts)!r})\n", encoding="utf-8")
PY
# mpy-cross of the building system: frozen modules are compiled here, not on Windows.
make -C "$DEPS/micropython/mpy-cross" -j"$JOBS" BUILD="$BUILD/mpy-cross" > /dev/null
make -C "$DEPS/micropython/ports/windows" -j"$JOBS" \
    CROSS_COMPILE=x86_64-w64-mingw32- \
    MICROPY_MPYCROSS="$BUILD/mpy-cross/mpy-cross" MICROPY_MPYCROSS_DEPENDENCY="$BUILD/mpy-cross/mpy-cross" \
    USER_C_MODULES="$ROOT/runtime/modules" \
    BINDINGS_DIR="$DEPS/lvgl-bindings" \
    VARIANT_DIR="$ROOT/runtime/variant-win64" \
    FROZEN_MANIFEST="$BUILD/frozen/manifest.py" \
    SDL2_CFLAGS="-I$SDL_DIR/include/SDL2" \
    SDL2_LIBS="-L$SDL_DIR/lib -Wl,-Bstatic -lSDL2 -Wl,-Bdynamic -lm -lkernel32 -luser32 -lgdi32 -lwinmm -limm32 -lole32 -loleaut32 -lversion -luuid -ladvapi32 -lsetupapi -lshell32 -ldinput8" \
    CFLAGS_EXTRA="-Dmain=micropython_main -DLVSIM_STANDALONE=1 -DLVSIM_ONEFILE=1 -DSDL_MAIN_HANDLED -DMICROPY_VFS_ROM=1" \
    LDFLAGS_EXTRA="-static" \
    BUILD="$BUILD"
cp "$BUILD/micropython.exe" "$OUT/lvsim-onefile.exe"
x86_64-w64-mingw32-strip "$OUT/lvsim-onefile.exe"
x86_64-w64-mingw32-objdump -p "$OUT/lvsim-onefile.exe" | grep "DLL Name"
