#!/usr/bin/env bash
# Static SDL2 for the single-file executable on Linux.
# X11, Wayland and audio are loaded at run time if present, so the binary does not need them to start.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEPS="$ROOT/.reference"
OUT=$(realpath -m "${SDL_OUT:-$ROOT/runtime/out/sdl2-static}")  # build_onefile_portable.sh uses its own
REVISION=release-2.30.9
JOBS=${JOBS:-4}
if [ ! -d "$DEPS/SDL/.git" ]; then
    git init -q "$DEPS/SDL"
    git -C "$DEPS/SDL" remote add origin https://github.com/libsdl-org/SDL.git
fi
if ! git -C "$DEPS/SDL" cat-file -e "$REVISION^{commit}" 2>/dev/null; then
    git -C "$DEPS/SDL" fetch -q --depth 1 origin tag "$REVISION"
fi
git -C "$DEPS/SDL" checkout -q "$REVISION"
cmake -S "$DEPS/SDL" -B "$OUT/build" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$OUT" \
    -DSDL_SHARED=OFF -DSDL_STATIC=ON -DSDL_STATIC_PIC=ON -DSDL_TEST=OFF \
    -DSDL_X11_SHARED=ON -DSDL_WAYLAND_SHARED=ON -DSDL_WAYLAND_LIBDECOR_SHARED=ON -DSDL_KMSDRM_SHARED=ON \
    -DSDL_PULSEAUDIO_SHARED=ON -DSDL_ALSA_SHARED=ON -DSDL_PIPEWIRE_SHARED=ON -DSDL_JACK=OFF -DSDL_SNDIO=OFF \
    -DSDL_LIBSAMPLERATE=OFF -DSDL_HIDAPI=OFF -DSDL_RPATH=OFF
cmake --build "$OUT/build" -j"$JOBS"
cmake --install "$OUT/build"
"$OUT/bin/sdl2-config" --static-libs
