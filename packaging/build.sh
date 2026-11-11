#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PYTHON=${PYTHON:-"$ROOT/.venv/bin/python"}
JOBS=${JOBS:-4}
test -x "$ROOT/runtime/out/lvsim-runtime"
test -x "$ROOT/runtime/out/mpy-cross"
test -x "$ROOT/runtime/out/lvsim-onefile"
test -f "$ROOT/runtime/out-win64/lvsim-onefile.exe" || { echo "The Windows launcher is missing: run runtime/build_onefile_windows.sh" >&2; exit 1; }
test -f "$ROOT/runtime/out-web/micropython.wasm" || { echo "The browser runtime is missing: run runtime/build_web.sh" >&2; exit 1; }
ONEFILE_GLIBC=$(objdump -T "$ROOT/runtime/out/lvsim-onefile" | grep -o 'GLIBC_[0-9.]*' | sort -Vu | tail -1)
if [ "$(printf '%s\n' "$ONEFILE_GLIBC" GLIBC_2.34 | sort -V | tail -1)" != GLIBC_2.34 ]; then
    echo "Warning: single-file games will need $ONEFILE_GLIBC. To ship them to older systems too, run runtime/build_onefile_portable.sh." >&2
fi
"$PYTHON" -m PyInstaller --noconfirm --clean --distpath "$ROOT/dist" --workpath "$ROOT/build/pyinstaller" "$ROOT/packaging/lvgl-mpy-studio.spec"
APPDIR="$ROOT/build/AppDir"
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/applications" "$APPDIR/usr/share/icons/hicolor/scalable/apps"
cp -a "$ROOT/dist/lvgl-mpy-studio" "$APPDIR/usr/bin/"
cp "$ROOT/packaging/AppRun" "$APPDIR/AppRun"
chmod +x "$APPDIR/AppRun"
cp "$ROOT/packaging/lvgl-mpy-studio.desktop" "$APPDIR/lvgl-mpy-studio.desktop"
cp "$ROOT/packaging/lvgl-mpy-studio.desktop" "$APPDIR/usr/share/applications/"
cp "$ROOT/packaging/lvgl-mpy-studio.svg" "$APPDIR/lvgl-mpy-studio.svg"
cp "$ROOT/packaging/lvgl-mpy-studio.svg" "$APPDIR/usr/share/icons/hicolor/scalable/apps/"
if command -v appimagetool >/dev/null; then
    TOOL=$(command -v appimagetool)
else
    TOOL="$ROOT/cache/appimagetool-x86_64.AppImage"
    if [ ! -x "$TOOL" ]; then
        mkdir -p "$ROOT/cache"
        curl -fL "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage" -o "$TOOL"
        chmod +x "$TOOL"
    fi
fi
ARCH=x86_64 "$TOOL" --appimage-extract-and-run "$APPDIR" "$ROOT/dist/LVGL_MPY_STUDIO-x86_64.AppImage"
