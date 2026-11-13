#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEPS="$ROOT/.reference"
SRC="$ROOT/runtime/src"
OUT="$ROOT/runtime/out"
JOBS=${JOBS:-4}
mkdir -p "$DEPS" "$SRC" "$OUT" "$ROOT/runtime/modules"

fetch() {
    local name=$1 url=$2 revision=$3
    if [ ! -d "$DEPS/$name/.git" ]; then
        git init -q "$DEPS/$name"
        git -C "$DEPS/$name" remote add origin "$url"
    fi
    if ! git -C "$DEPS/$name" cat-file -e "$revision^{commit}" 2>/dev/null; then
        git -C "$DEPS/$name" fetch origin
    fi
    git -C "$DEPS/$name" checkout -q "$revision"
}

fetch micropython https://github.com/micropython/micropython.git v1.29.0
fetch lvgl-micropython https://github.com/PyDevices/lvgl-micropython.git 58d18ce5b48cd7acce609317991627a046f998f8
fetch lvgl-bindings https://github.com/PyDevices/lvgl-bindings.git 7740c2fae0daa10992f5f8fe54acf670a70e2d3b
make -C "$DEPS/micropython/ports/unix" submodules
git -C "$DEPS/lvgl-bindings" submodule update --init --depth=1
ln -srfn "$DEPS/lvgl-micropython" "$ROOT/runtime/modules/lvgl-micropython"
ln -srfn "$DEPS/lvgl-bindings" "$ROOT/runtime/modules/lvgl-bindings"
ln -srfn "$ROOT/native/lvsim" "$ROOT/runtime/modules/lvsim"
make -C "$DEPS/micropython/mpy-cross" -j"$JOBS"
# os.dupterm, which the unix port leaves out: a program without pages shows its output on the display
# as on a board (ansiterm.py of mpy-lvgl-boards). It changes the VM state: rebuild from clean when it changes.
make -C "$DEPS/micropython/ports/unix" -j"$JOBS" \
    USER_C_MODULES="$ROOT/runtime/modules" \
    BINDINGS_DIR="$DEPS/lvgl-bindings" \
    CFLAGS_EXTRA="-DMICROPY_PY_OS_DUPTERM=1" \
    BUILD="$OUT/build"
cp "$OUT/build/micropython" "$OUT/lvsim-runtime"
cp "$DEPS/micropython/mpy-cross/build/mpy-cross" "$OUT/mpy-cross" 2>/dev/null || make -C "$DEPS/micropython/mpy-cross" -j"$JOBS" && cp "$DEPS/micropython/mpy-cross/build/mpy-cross" "$OUT/mpy-cross"
"$OUT/lvsim-runtime" -c 'import lvgl, hello; print("lvgl", lvgl.version_info()); print("hello", hello.answer())'
JOBS="$JOBS" "$ROOT/runtime/build_onefile.sh"
