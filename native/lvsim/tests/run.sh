#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
OUT="$ROOT/cache/lvsim-net-tests"
mkdir -p "$OUT"
CFLAGS="-std=c11 -Wall -Wextra -Werror -pedantic -I$ROOT/native/lvsim"

cc $CFLAGS -o "$OUT/net-test" \
    "$ROOT/native/lvsim/tests/net_test.c" \
    "$ROOT/native/lvsim/lvsim_net_posix.c" \
    "$ROOT/native/lvsim/lvsim_time_posix.c"
"$OUT/net-test"

if ! command -v x86_64-w64-mingw32-gcc >/dev/null 2>&1; then
    export PATH="$ROOT/cache/w0-mingw/sysroot/usr/bin:$PATH"
fi
if command -v x86_64-w64-mingw32-gcc >/dev/null 2>&1; then
    x86_64-w64-mingw32-gcc $CFLAGS -DWIN32_LEAN_AND_MEAN -o "$OUT/net-test.exe" \
        "$ROOT/native/lvsim/tests/net_test.c" \
        "$ROOT/native/lvsim/lvsim_net_win32.c" \
        "$ROOT/native/lvsim/lvsim_time_win32.c" \
        -lws2_32 -lwinmm -static-libgcc
    if command -v wine >/dev/null 2>&1; then
        WINEDEBUG=-all wine "$OUT/net-test.exe"
    fi
fi
