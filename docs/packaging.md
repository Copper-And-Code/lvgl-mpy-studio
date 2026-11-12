# Building the packages

How to build the AppImage for Linux and the portable package for Windows, both from a Linux
computer. Packages are built by hand: the continuous integration runs the tests and builds no
package, because a package needs runtimes it does not compile.

## In short

With the runtimes already built, as on a computer where packages were made before:

```bash
./packaging/build.sh                     # dist/LVGL_MPY_STUDIO-x86_64.AppImage
./packaging/build_windows_portable.sh    # dist/LVGL_MPY_STUDIO-<version>-portable-win64.zip
```

Then check them, see [Checking a package](#checking-a-package).

## What a package contains

The IDE, Python and Qt, and the **runtimes**: the programs that run a project outside the IDE.
They are compiled once and only again when their sources change (`native/`, `runtime/`, the
pinned versions of MicroPython and LVGL).

| Runtime | Built by | Used for | Output |
|---|---|---|---|
| Simulator for Linux | `runtime/build.sh` | the simulator panel, previews, visual tests | `runtime/out/lvsim-runtime`, `mpy-cross` |
| Launcher of single-file games, Linux | `runtime/build_onefile_portable.sh` | **Build Single-File Executable** | `runtime/out/lvsim-onefile` |
| Simulator for Windows | `runtime/build_windows.sh` | the same as the first, on Windows | `runtime/out-win64/*.exe`, `SDL2.dll` |
| Launcher of single-file games, Windows | `runtime/build_onefile_windows.sh` | single-file games for Windows, also built from Linux | `runtime/out-win64/lvsim-onefile.exe` |
| Runtime for the browser | `runtime/build_web.sh` | **Open in Browser** | `runtime/out-web/micropython.mjs`, `.wasm` |

Both packages carry all of them, because the IDE on one system builds games for the other.

## Prerequisites

Once for the computer:

```bash
sudo apt-get install build-essential pkg-config cmake libffi-dev libsdl2-dev xvfb \
    gcc-mingw-w64-x86-64 cabextract unzip curl
python3 -m venv .venv
.venv/bin/pip install -e '.[dev,packaging]'
```

- **Docker**, for the Linux launcher of single-file games. It is built in an Ubuntu 22.04
  container so that the games also start on systems with an older C library.
- **Emscripten**, for the browser runtime. `runtime/build_web.sh` looks for `emcc` on the
  `PATH`, or for an emsdk in `cache/emsdk`; the runtime in use was built with Emscripten 7.0.0:

  ```bash
  git clone https://github.com/emscripten-core/emsdk cache/emsdk
  cache/emsdk/emsdk install 7.0.0 && cache/emsdk/emsdk activate 7.0.0
  ```

- Without MinGW installed from packages, a toolchain unpacked under `cache/w0-mingw` is used
  if present; `docs/windows-notes.md` says how it was made.

## Building the runtimes

In this order; each script fetches the pinned sources it needs under `.reference/`.

```bash
./runtime/build.sh                          # simulator for Linux, a few minutes the first time
sudo ./runtime/build_onefile_portable.sh    # Linux launcher, in Docker
./runtime/build_windows.sh                  # simulator for Windows
./runtime/build_onefile_windows.sh          # Windows launcher; after the previous one
./runtime/build_web.sh                      # runtime for the browser
```

`sudo` is needed only where Docker is not usable by your user; the files produced go back to
you. `runtime/build_onefile.sh` builds the Linux launcher without Docker: it is quicker, but
the games then need the C library of the computer that built it. `packaging/build.sh` prints
a warning when that is the case; the launcher of a package to be given out must be the one
from Docker.

To see which C library the launcher needs:

```bash
objdump -T runtime/out/lvsim-onefile | grep -o 'GLIBC_[0-9.]*' | sort -Vu | tail -1    # GLIBC_2.34
```

## The AppImage for Linux

```bash
./packaging/build.sh
```

About half a minute. It runs PyInstaller with `packaging/lvgl-mpy-studio.spec`, assembles
the AppDir and calls `appimagetool`, downloaded to `cache/` the first time. It stops with a
message if a runtime is missing. Output: `dist/LVGL_MPY_STUDIO-x86_64.AppImage`, about 95 MB.

## The portable package for Windows

```bash
./packaging/build_windows_portable.sh
```

Under a minute after the first time, when it downloads to `cache/windows-portable/` the
embeddable Python 3.12.10, the Windows wheels of the pinned dependencies and Microsoft's
Visual C++ runtime. It compiles `LVGL_MPY_STUDIO.exe`, a small launcher with the icon, with
MinGW. Output: `dist/LVGL_MPY_STUDIO-<version>-portable-win64.zip`, about 280 MB.

The archive is extracted whole and started with `LVGL_MPY_STUDIO.exe`; Python need not be
installed. `LVGL_MPY_STUDIO_console.bat` starts the same program with a console, for the
command line and for diagnostics.

**Do not add ICU to this package.** Qt uses the `icuuc.dll` of Windows; a copy next to Qt hides
it and Qt does not load. Version 0.4 had this fault, and tests under Wine did not show it.

### The installer for Windows

`packaging/build_windows.ps1` builds, on Windows, a PyInstaller folder, a zip and an Inno
Setup installer. It has not been run since 0.4 and is not part of the packages given out
today. From PowerShell, with Python and Inno Setup 6:

```powershell
python -m pip install -e '.[packaging]'
powershell -ExecutionPolicy Bypass -File packaging/build_windows.ps1
```

## Checking a package

A package is not done until it has run.

**Linux.** From an empty folder, so that nothing comes from the sources:

```bash
dist/LVGL_MPY_STUDIO-x86_64.AppImage --version
dist/LVGL_MPY_STUDIO-x86_64.AppImage selftest          # RESULT: PASSED, 82 steps
```

**Windows.** Wine is not a check: it starts a program whose libraries lack functions, and
has hidden real faults. On a real Windows, after extracting the archive:

```
LVGL_MPY_STUDIO_console.bat --version
LVGL_MPY_STUDIO_console.bat selftest
```

then start `LVGL_MPY_STUDIO.exe` by double click: the IDE opens, the file and the taskbar show
the icon, and no console window flashes while working.

What to look at before giving a package out:

| Check | How |
|---|---|
| The version is the one meant | `--version` |
| The self-test passes | `selftest`, on both systems |
| The Linux launcher is the portable one | the `objdump` line above, on `runtime/out/lvsim-onefile` |
| No ICU in the Windows archive | `unzip -l dist/*.zip \| grep -ci 'icu.*dll'` gives 0 |
| A game built by the package starts | `build project.json --profile release --single-file`, then the game with `--selftest` |
| The checksum is recorded | `sha256sum dist/LVGL_MPY_STUDIO-*` |

Record in [the status page](status.md) what was checked and on which system.

## What is not done

- Binaries are not signed: Windows SmartScreen asks for **More info → Run anyway**.
- Releases are made by hand: no workflow builds or uploads the packages. The two files and their
  checksums are attached to a GitHub release with `gh release create`.
- The AppImage has been run only on the computer that built it.

Licences and sources of what a package contains are in `packaging/NOTICE.txt` and
`THIRD_PARTY.md`. Pinned versions: MicroPython 1.29.0, LVGL 9.5.0, PySide6 6.12.0; see
`docs/target.md`.
