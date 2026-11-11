#!/usr/bin/env bash
# Single-file launcher built in Ubuntu 22.04, so it also starts where glibc is older
# than on this computer: from glibc 2.35 up (Ubuntu 22.04, Debian 12, Mint 21, Zorin 17).
# Needs Docker; with sudo the files produced still go back to the user.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
IMAGE=${IMAGE:-ubuntu:22.04}
OWNER="${SUDO_UID:-$(id -u)}:${SUDO_GID:-$(id -g)}"
docker run --rm -v "$ROOT:$ROOT" -w "$ROOT" -e OWNER="$OWNER" -e JOBS="${JOBS:-4}" "$IMAGE" bash -euc '
    trap "chown -R \"\$OWNER\" runtime/out .reference" EXIT
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -yqq --no-install-recommends build-essential cmake git pkg-config python3 ca-certificates \
        libsdl2-dev libpipewire-0.3-dev libdecor-0-dev wayland-protocols > /dev/null
    git config --global --add safe.directory "*"
    # the shared mpy-cross in .reference is built for this computer and would not start in the container
    make -C .reference/micropython/mpy-cross -j"$JOBS" BUILD="$PWD/runtime/out/portable/mpy-cross" > /dev/null
    MPY_CROSS=runtime/out/portable/mpy-cross/mpy-cross SDL_OUT=runtime/out/portable/sdl2-static ONEFILE_BUILD=runtime/out/portable/build-onefile ./runtime/build_onefile.sh
'
echo "glibc required: $(objdump -T "$ROOT/runtime/out/lvsim-onefile" | grep -o 'GLIBC_[0-9.]*' | sort -Vu | tail -1)"
