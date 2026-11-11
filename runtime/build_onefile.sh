#!/usr/bin/env bash
# Launcher of the single-file executable for Linux: the same for every game, which the IDE appends to it.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEPS="$ROOT/.reference"
OUT="$ROOT/runtime/out"
BUILD=$(realpath -m "${ONEFILE_BUILD:-$OUT/build-onefile}")
JOBS=${JOBS:-4}
export SDL_OUT=$(realpath -m "${SDL_OUT:-$OUT/sdl2-static}")
SDL="$SDL_OUT/bin/sdl2-config"
test -x "$SDL" || "$ROOT/runtime/build_sdl_static.sh"
mkdir -p "$BUILD/frozen"
cp "$ROOT/runtime/onefile/lvgl_ide_boot.py" "$ROOT/runtime/onefile/manifest.py" "$BUILD/frozen/"
python3 - "$ROOT/lvgl_mpy_studio/gen/output/licenses" "$BUILD/frozen/lvgl_ide_licenses.py" <<'PY'
import pathlib, sys
texts = [f"===== {path.stem} =====\n{path.read_text(encoding='utf-8')}" for path in sorted(pathlib.Path(sys.argv[1]).glob("*.txt"))]
pathlib.Path(sys.argv[2]).write_text(f"print({chr(10).join(texts)!r})\n", encoding="utf-8")
PY
CROSS=()
if [ -n "${MPY_CROSS:-}" ]; then  # an mpy-cross built for this system, not the shared one in .reference
    MPY_CROSS=$(realpath -m "$MPY_CROSS")
    CROSS=(MICROPY_MPYCROSS="$MPY_CROSS" MICROPY_MPYCROSS_DEPENDENCY="$MPY_CROSS")
fi
make -C "$DEPS/micropython/ports/unix" -j"$JOBS" "${CROSS[@]}" \
    USER_C_MODULES="$ROOT/runtime/modules" \
    BINDINGS_DIR="$DEPS/lvgl-bindings" \
    BUILD="$BUILD" \
    FROZEN_MANIFEST="$BUILD/frozen/manifest.py" \
    LVSIM_STANDALONE="$ROOT/runtime/variant-win64/lvsim_standalone.c" \
    CFLAGS_EXTRA="-Dmain=micropython_main -DLVSIM_STANDALONE=1 -DLVSIM_ONEFILE=1" \
    SDL2_CFLAGS="$("$SDL" --cflags)" \
    SDL2_LIBS="$("$SDL" --static-libs)" \
    MICROPY_PY_FFI=0
cp "$BUILD/micropython" "$OUT/lvsim-onefile"
strip "$OUT/lvsim-onefile"
"$OUT/lvsim-onefile" --licenses | grep -q "===== SDL2 ====="
