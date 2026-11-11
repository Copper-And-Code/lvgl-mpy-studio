#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEPS="$ROOT/.reference"
OUT="$ROOT/runtime/out-win64"
JOBS=${JOBS:-4}
SDL_VERSION=2.30.9
SDL_SHA256=b188d165dc4a0372042bff3d0c18e9bb90772581e92a7b8b47b521b47714f75c
SDL_CACHE="$ROOT/cache/sdl2"
SDL_ARCHIVE="$SDL_CACHE/SDL2-devel-$SDL_VERSION-mingw.tar.gz"
SDL_DIR=${SDL2_DIR:-"$SDL_CACHE/SDL2-$SDL_VERSION/x86_64-w64-mingw32"}

if ! command -v x86_64-w64-mingw32-gcc >/dev/null 2>&1; then
    export PATH="$ROOT/cache/w0-mingw/sysroot/usr/bin:$PATH"
fi
command -v x86_64-w64-mingw32-gcc >/dev/null 2>&1 || {
    echo "Install MinGW-w64 x86-64 or set PATH" >&2
    exit 1
}
mkdir -p "$DEPS" "$OUT/build" "$SDL_CACHE" "$ROOT/runtime/modules"

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

if [ ! -f "$SDL_ARCHIVE" ]; then
    curl -fL --retry 3 "https://github.com/libsdl-org/SDL/releases/download/release-$SDL_VERSION/SDL2-devel-$SDL_VERSION-mingw.tar.gz" -o "$SDL_ARCHIVE.part"
    mv "$SDL_ARCHIVE.part" "$SDL_ARCHIVE"
fi
echo "$SDL_SHA256  $SDL_ARCHIVE" | sha256sum -c -
if [ ! -d "$SDL_DIR" ]; then
    tar -xzf "$SDL_ARCHIVE" -C "$SDL_CACHE"
fi

IDE_VERSION=$(python3 -c 'import re, pathlib, sys; print(re.search(r"__version__ = \"([^\"]+)", (pathlib.Path(sys.argv[1]) / "lvgl_mpy_studio/__init__.py").read_text(encoding="utf-8")).group(1))' "$ROOT")
IDE_COMMIT=$(git -C "$ROOT" rev-parse --short HEAD)
IDE_FILEVERSION=$(python3 -c 'import sys; print(",".join((sys.argv[1].split(".") + ["0", "0", "0"])[:4]))' "$IDE_VERSION")
sed -e "s/@IDE_VERSION@/$IDE_VERSION/g" -e "s/@IDE_COMMIT@/$IDE_COMMIT/g" -e "s/@IDE_FILEVERSION@/$IDE_FILEVERSION/g" \
    "$ROOT/runtime/variant-win64/lvsim_version.rc" > "$OUT/build/lvsim_version.rc"
x86_64-w64-mingw32-windres "$OUT/build/lvsim_version.rc" -O coff -o "$OUT/build/lvsim_version.res"

make -C "$DEPS/micropython/mpy-cross" -j"$JOBS"
make -C "$DEPS/micropython/mpy-cross" -j"$JOBS" \
    CROSS_COMPILE=x86_64-w64-mingw32- \
    BUILD="$OUT/build-mpy-cross" \
    LDFLAGS_EXTRA=-static-libgcc
make -C "$DEPS/micropython/ports/windows" -j"$JOBS" \
    CROSS_COMPILE=x86_64-w64-mingw32- \
    USER_C_MODULES="$ROOT/runtime/modules" \
    BINDINGS_DIR="$DEPS/lvgl-bindings" \
    VARIANT_DIR="$ROOT/runtime/variant-win64" \
    SDL2_CFLAGS="-I$SDL_DIR/include/SDL2" \
    SDL2_LIBS="-L$SDL_DIR/lib -lSDL2" \
    LDFLAGS_EXTRA="$OUT/build/lvsim_version.res -static-libgcc" \
    BUILD="$OUT/build"
make -C "$DEPS/micropython/ports/windows" -j"$JOBS" \
    CROSS_COMPILE=x86_64-w64-mingw32- \
    USER_C_MODULES="$ROOT/runtime/modules" \
    BINDINGS_DIR="$DEPS/lvgl-bindings" \
    VARIANT_DIR="$ROOT/runtime/variant-win64" \
    SDL2_CFLAGS="-I$SDL_DIR/include/SDL2" \
    SDL2_LIBS="-L$SDL_DIR/lib -lSDL2" \
    CFLAGS_EXTRA="-Dmain=micropython_main -DLVSIM_STANDALONE=1 -DSDL_MAIN_HANDLED" \
    LDFLAGS_EXTRA="$OUT/build/lvsim_version.res -static-libgcc" \
    BUILD="$OUT/build-standalone"

cp "$OUT/build/micropython.exe" "$OUT/lvsim-runtime.exe"
cp "$OUT/build-standalone/micropython.exe" "$OUT/lvsim-standalone.exe"
cp "$OUT/build-mpy-cross/mpy-cross.exe" "$OUT/mpy-cross.exe"
cp "$SDL_DIR/bin/SDL2.dll" "$OUT/SDL2.dll"
mkdir -p "$OUT/SDL2"
cp -a "$SDL_DIR/include" "$SDL_DIR/lib" "$OUT/SDL2/"
"$ROOT/runtime/build_c_windows.sh"
JOBS="$JOBS" "$ROOT/runtime/build_onefile_windows.sh"
x86_64-w64-mingw32-objdump -p "$OUT/lvsim-runtime.exe" | grep "DLL Name"
printf 'Windows runtime %s (%s): %s\n' "$IDE_VERSION" "$IDE_COMMIT" "$OUT/lvsim-runtime.exe"
