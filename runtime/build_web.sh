#!/usr/bin/env bash
# Runtime for the browser: MicroPython in WebAssembly with LVGL and lvsim on Emscripten's SDL2.
# The same for every game: the page passes it the compiled modules of the project.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEPS="$ROOT/.reference"
OUT="$ROOT/runtime/out-web"
JOBS=${JOBS:-4}
EMSDK=${EMSDK:-"$ROOT/cache/emsdk"}
if ! command -v emcc >/dev/null 2>&1; then
    # shellcheck disable=SC1091
    . "$EMSDK/emsdk_env.sh" > /dev/null
fi
make -C "$DEPS/micropython/ports/webassembly" -j"$JOBS" \
    BUILD="$OUT/build" \
    USER_C_MODULES="$ROOT/runtime/modules" \
    BINDINGS_DIR="$DEPS/lvgl-bindings" \
    SDL2_CFLAGS="-sUSE_SDL=2" \
    SDL2_LIBS="-sUSE_SDL=2 -sALLOW_MEMORY_GROWTH=1 -sASYNCIFY_STACK_SIZE=1048576"
cp "$OUT/build/micropython.mjs" "$OUT/build/micropython.wasm" "$OUT/"
ls -la "$OUT/micropython.mjs" "$OUT/micropython.wasm"
