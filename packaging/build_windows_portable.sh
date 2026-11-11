#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
CACHE="$ROOT/cache/windows-portable"
WHEELS="$CACHE/wheels"
BUILD="$ROOT/build/windows-portable"
OUT="$BUILD/LVGL_MPY_STUDIO"
PYTHON_VERSION=3.12.10
PYTHON_ARCHIVE="$CACHE/python-$PYTHON_VERSION-embed-amd64.zip"
ICU_ARCHIVE="$CACHE/microsoft-icu-win64.zip"
ICU_URL="https://api.nuget.org/v3-flatcontainer/microsoft.icu.icu4c.runtime.win-x64/72.1.0.3/microsoft.icu.icu4c.runtime.win-x64.72.1.0.3.nupkg"
VC_REDIST="$CACHE/vc_redist.x64.exe"
VC_URL="https://aka.ms/vs/17/release/vc_redist.x64.exe"
HOST_PYTHON=${PYTHON:-"$ROOT/.venv/bin/python"}
IDE_VERSION=$("$HOST_PYTHON" -c 'from lvgl_mpy_studio import __version__; print(__version__)' | tail -n 1)

mkdir -p "$WHEELS"
if [ ! -f "$PYTHON_ARCHIVE" ]; then
    curl -fL --retry 3 "https://www.python.org/ftp/python/$PYTHON_VERSION/python-$PYTHON_VERSION-embed-amd64.zip" -o "$PYTHON_ARCHIVE"
fi
if [ ! -f "$ICU_ARCHIVE" ]; then
    curl -fL --retry 3 "$ICU_URL" -o "$ICU_ARCHIVE"
fi
if [ ! -f "$VC_REDIST" ]; then
    curl -fL --retry 3 "$VC_URL" -o "$VC_REDIST"
fi
if ! compgen -G "$WHEELS/qtawesome-*.whl" >/dev/null; then
    "$HOST_PYTHON" -m pip download --dest "$WHEELS" --only-binary=:all: --platform win_amd64 \
        --python-version 3.12 --implementation cp --abi cp312 PySide6==6.12.0 mpremote==1.29.0 pyserial==3.5 qtawesome==1.4.2
fi
if ! command -v x86_64-w64-mingw32-gcc >/dev/null 2>&1; then
    export PATH="$ROOT/cache/w0-mingw/sysroot/usr/bin:$PATH"
fi

VC_EXTRACT="$CACHE/vcredist-extract"
VC_RUNTIME="$CACHE/vc-runtime-x64"
rm -rf "$VC_EXTRACT" "$VC_RUNTIME"
mkdir -p "$VC_EXTRACT" "$VC_RUNTIME"
cabextract -q -d "$VC_EXTRACT" "$VC_REDIST"
for archive in "$VC_EXTRACT"/*; do
    contents=$(cabextract -l "$archive" 2>/dev/null || true)
    case "$contents" in
        *msvcp140.dll_amd64*)
            cabextract -q -d "$VC_RUNTIME" "$archive"
            break
            ;;
    esac
done
if [ ! -f "$VC_RUNTIME/msvcp140.dll_amd64" ]; then
    printf 'Visual C++ x64 runtime not found in %s\n' "$VC_REDIST" >&2
    exit 1
fi

rm -rf "$OUT"
mkdir -p "$OUT/python/Lib/site-packages" "$OUT/runtime/out-win64" "$OUT/docs" "$OUT/.reference/lvgl-bindings"
unzip -q "$PYTHON_ARCHIVE" -d "$OUT/python"
printf 'python312.zip\n.\n..\nLib\\site-packages\nimport site\n' > "$OUT/python/python312._pth"
for wheel in "$WHEELS"/*.whl; do
    unzip -q -o "$wheel" -d "$OUT/python/Lib/site-packages"
done
for path in "$VC_RUNTIME"/*.dll_amd64; do
    name=$(basename "$path" _amd64)
    cp "$path" "$OUT/python/$name"
done
# Only the font the IDE uses: the others in QtAwesome have different licences.
find "$OUT/python/Lib/site-packages/qtawesome/fonts" -type f ! -name 'materialdesignicons6*' -delete
QT_DIR="$OUT/python/Lib/site-packages/PySide6"
for name in icudt72.dll icuin72.dll icuuc72.dll; do
    unzip -p "$ICU_ARCHIVE" "runtimes/win-x64/native/$name" > "$QT_DIR/$name"
done
cp "$QT_DIR/icuuc72.dll" "$QT_DIR/icuuc.dll"
unzip -p "$ICU_ARCHIVE" LICENSE > "$OUT/ICU-LICENSE.txt"

tar -C "$ROOT" --exclude=__pycache__ --exclude='*.pyc' -cf - lvgl_mpy_studio | tar -xf - -C "$OUT"
cp "$ROOT/packaging/launcher.py" "$OUT/"
for name in lvsim-runtime.exe lvsim-standalone.exe lvsim-onefile.exe mpy-cross.exe SDL2.dll liblvgl.a; do
    cp "$ROOT/runtime/out-win64/$name" "$OUT/runtime/out-win64/"
done
cp -a "$ROOT/runtime/out-win64/SDL2" "$OUT/runtime/out-win64/"
mkdir -p "$OUT/runtime/out"
cp "$ROOT/runtime/out/lvsim-onefile" "$OUT/runtime/out/"  # games for Linux built on Windows
mkdir -p "$OUT/runtime/out-web"
cp "$ROOT/runtime/out-web/micropython.mjs" "$ROOT/runtime/out-web/micropython.wasm" "$OUT/runtime/out-web/"
cp -r "$ROOT/runtime/web" "$OUT/runtime/"
cp "$ROOT/runtime/display_driver.py" "$OUT/runtime/"
cp -a "$ROOT/native" "$OUT/"
# Only what is needed to build the C target.
mkdir -p "$OUT/.reference/lvgl-bindings/lvgl"
cp -a "$ROOT/.reference/lvgl-bindings/lvgl/src" "$OUT/.reference/lvgl-bindings/lvgl/"
for name in lvgl.h lvgl_private.h lv_version.h LICENCE.txt COPYRIGHTS.md; do
    cp "$ROOT/.reference/lvgl-bindings/lvgl/$name" "$OUT/.reference/lvgl-bindings/lvgl/"
done
cp "$ROOT/.reference/lvgl-bindings/lv_conf.h" "$OUT/.reference/lvgl-bindings/"
cp "$ROOT/docs/target.md" "$ROOT/docs/boards.md" "$ROOT/docs/boards.it.md" "$ROOT/docs/windows-c.md" "$OUT/docs/"
cp "$ROOT/packaging/NOTICE.txt" "$ROOT/THIRD_PARTY.md" "$ROOT/README.md" "$ROOT/LICENSE" "$ROOT/LICENSE-MIT.txt" "$ROOT/LICENSING.md" "$OUT/"
mkdir -p "$OUT/licenses"
cp "$ROOT"/packaging/licenses/* "$ROOT"/lvgl_mpy_studio/gen/output/licenses/* "$OUT/licenses/"

x86_64-w64-mingw32-gcc -O2 -Wall -Wextra -Werror -mwindows -municode -static-libgcc \
    "$ROOT/packaging/windows_launcher.c" -o "$OUT/LVGL_MPY_STUDIO.exe"
printf '@echo off\r\n"%%~dp0python\\python.exe" -m lvgl_mpy_studio %%*\r\n' > "$OUT/LVGL_MPY_STUDIO_console.bat"
printf '%s\r\n' 'LVGL MPY Studio - portable Windows x86-64 version' '' \
    'Start LVGL_MPY_STUDIO.exe. Do not move files out of this folder.' \
    'For terminal diagnostics use LVGL_MPY_STUDIO_console.bat.' \
    'The MicroPython Debug target needs no toolchain.' \
    'For the C target see docs/windows-c.md.' > "$OUT/README.txt"

mkdir -p "$ROOT/dist"
ARCHIVE="$ROOT/dist/LVGL_MPY_STUDIO-$IDE_VERSION-portable-win64"
rm -f "$ARCHIVE.zip"
"$HOST_PYTHON" -c 'import shutil, sys; shutil.make_archive(sys.argv[1], "zip", root_dir=sys.argv[2], base_dir="LVGL_MPY_STUDIO")' "$ARCHIVE" "$BUILD"
printf 'Portable package: %s.zip\n' "$ARCHIVE"
