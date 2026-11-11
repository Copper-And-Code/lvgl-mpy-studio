#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEPS="$ROOT/.reference"
OUT="$ROOT/runtime/out-win64"
LVGL_DIR="$DEPS/lvgl-bindings/lvgl"
CONF_DIR="$DEPS/lvgl-bindings"
OBJECTS="$OUT/c-objects"
CROSS_COMPILE=${CROSS_COMPILE:-x86_64-w64-mingw32-}
if ! command -v "${CROSS_COMPILE}gcc" >/dev/null 2>&1; then
    export PATH="$ROOT/cache/w0-mingw/sysroot/usr/bin:$PATH"
fi
CC=${CC:-${CROSS_COMPILE}gcc}
AR=${AR:-${CROSS_COMPILE}ar}
mkdir -p "$OBJECTS"

flags=(-O2 -std=c11 -Wall -Wextra -Werror -DLV_CPYTHON_BUILD -DLV_CONF_INCLUDE_SIMPLE -I"$CONF_DIR" -I"$LVGL_DIR")
objects=()
while IFS= read -r -d '' source; do
    relative=${source#"$LVGL_DIR/src/"}
    object="$OBJECTS/${relative%.c}.o"
    mkdir -p "$(dirname "$object")"
    if [ ! -f "$object" ] || [ "$source" -nt "$object" ] || [ "$CONF_DIR/lv_conf.h" -nt "$object" ]; then
        "$CC" "${flags[@]}" -c "$source" -o "$object"
    fi
    objects+=("$object")
done < <(find "$LVGL_DIR/src" -name '*.c' -not -path '*/drivers/*' -not -name 'lv_gltf_view_shader.c' -print0)
"$AR" rcs "$OUT/liblvgl.a" "${objects[@]}"
printf 'Windows C library: %s\n' "$OUT/liblvgl.a"
