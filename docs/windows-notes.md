# Windows porting notes

## MinGW toolchain without administrator rights

**Context:** W0 requires MinGW-w64, but installing it with `sudo` was not possible because it asked for a password.

**Cause:** Ubuntu GCC packages with the POSIX thread model install executables with a `-posix` suffix; standard names such as `x86_64-w64-mingw32-gcc` are normally created by `update-alternatives`, which requires administrator rights.

**Solution:** download the Ubuntu packages with `apt-get download`, extract them with `dpkg-deb -x` into a local toolchain, and recreate the standard symlinks to the `-posix` binaries in its `usr/bin` directory. GCC 13.2.0 then correctly built a PE32+ and the whole MicroPython/LVGL runtime. Commands and versions are in `docs/log/w0-spike.md`.

## W0 spike runtime dependencies

The W0 binary imports only `bcrypt.dll`, `KERNEL32.dll` and `msvcrt.dll`. No further MinGW dependencies need to be distributed or linked statically.

## Simulator clock and wait

**Cause:** `mp_hal_ticks_ms()` in the Windows port uses `gettimeofday`, so it is not monotonic; waiting with `SleepEx` alone also delays the reaction to IDE messages.

**Solution:** `lvsim.ticks_ms()` uses `CLOCK_MONOTONIC` on POSIX and `QueryPerformanceCounter` on Windows. `lvsim.wait()` waits on the socket with `poll`/`WSAPoll`; the Windows backend enables a 1 ms timer granularity between open and close.

## Regenerating MicroPython QSTRs

**Context:** after adding the `lvsim.wait` binding, the incremental Linux build failed with a double declaration of `MP_QSTR_wait` in `frozen_content.c`.

**Cause:** generated QSTR indexes had not been rebuilt after the same identifier was added to both the C binding and the frozen module.

**Solution:** run `make clean` on the affected build only and rebuild. The following clean build succeeded; upstream sources were not changed.

## Standalone startup and CRT environment

**Context:** W5 requires the Windows app to start without arguments, and `--selftest` to configure the headless backend without inheriting variables from the IDE.

**Cause:** the Windows port uses `ports/unix/main.c`, which opens the REPL without arguments and offers no auto-start hook through a variant. Also, `SDL_main.h` redefines `main`, and `SetEnvironmentVariableA` does not reliably update the environment read by `getenv` in MSVCRT.

**Solution:** a second build of the same variant renames only the upstream `main` and adds `lvsim_standalone.c`; `SDL_MAIN_HANDLED` avoids the SDL redefinition. The wrapper imports `main` and calls `main.main()`, uses `_putenv_s` for the CRT environment, sets the working directory next to the executable and handles `--selftest`. Upstream sources were not changed. The package switches the PE subsystem from console to GUI and the wrapper redirects stdout and stderr to `<project>.log`.

## Accented project paths

**Cause:** when `main.py` is passed as a script, MicroPython puts the absolute directory in `sys.path`. On Windows that path arrives in the ANSI code page, which is not valid UTF-8, so imports fail with `UnicodeError` when the path has accents.

**Solution:** the IDE, the CLI, the budget and the preview start the runtime with `-c "import main; main.main()"`, so `sys.path` stays relative.

## Console window

The IDE does not need to hide the runtime console: `QProcess` already sets `CREATE_NO_WINDOW` when the parent process has no console.
