# W0 — Spike MicroPython/LVGL per Windows

Data: 2026-10-30.

## Esito

**W0 verde e chiuso: cross-build, riferimento Linux, Wine e smoke test su Windows reale riusciti.**

Non sono stati modificati MicroPython, PyDevices o i binding. Non sono state necessarie variant o flag aggiuntivi.

## Sorgenti verificati

- MicroPython: `v1.29.0`, commit `0fd6c573ea815774668bbb16b8e197c8822368b2`.
- PyDevices/lvgl-micropython: `58d18ce5b48cd7acce609317991627a046f998f8`.
- lvgl-bindings: `7740c2fae0daa10992f5f8fe54acf670a70e2d3b`.
- LVGL nel submodule: `85aa60d18b3d5e5588d7b247abf90198f07c8a63`.

I tre repository erano puliti prima e dopo la build.

## Toolchain

L'installazione di sistema prevista dal piano non era disponibile perché `sudo` richiede una password. I pacchetti Ubuntu originali sono quindi stati scaricati ed estratti senza privilegi in `cache/w0-mingw/sysroot`.

- GCC: `13.2.0-6ubuntu1+26.1`, target `x86_64-w64-mingw32`.
- Thread model: `posix`.
- Binutils: `2.41.90.20240122-1ubuntu1+11.4`.
- MinGW-w64: `11.0.1-3build1`.
- Wine: `10.0~repack-6ubuntu1+zorin5`, usato soltanto per la prova preliminare.

Pacchetti estratti:

```bash
apt-get download \
  gcc-mingw-w64-x86-64-posix \
  gcc-mingw-w64-x86-64-posix-runtime \
  gcc-mingw-w64-base \
  binutils-mingw-w64-x86-64 \
  mingw-w64-common \
  mingw-w64-x86-64-dev
for package in ./*.deb; do dpkg-deb -x "$package" ../sysroot; done
```

I nomi standard normalmente gestiti da `update-alternatives` sono stati ricreati come symlink locali (`gcc`, `cpp`, `gcc-ar`, `gcc-nm`, `gcc-ranlib`) verso gli eseguibili con suffisso `-posix`.

## Build

Dalla radice del progetto:

```bash
export PATH="$PWD/cache/w0-mingw/sysroot/usr/bin:$PATH"
make -C .reference/micropython/mpy-cross -j8
make -C .reference/micropython/ports/windows -j8 \
  CROSS_COMPILE=x86_64-w64-mingw32- \
  USER_C_MODULES="$PWD/.reference/lvgl-micropython" \
  BINDINGS_DIR="$PWD/.reference/lvgl-bindings" \
  BUILD="$PWD/runtime/out-w0-spike/build"
```

Log completi:

- `runtime/out-w0-spike/build-host-mpy-cross.log`
- `runtime/out-w0-spike/build-windows.log`

Risultato: `runtime/out-w0-spike/micropython.exe`, PE32+ console x86-64, **1.810.432 byte**.

SHA-256:

```text
fe385d5d198cf3b7eb7708c4105d499d579a5cc1b00c95c7957cc9f863d805fc  micropython.exe
078a66859155acf1ce0fe95e94fc12363de967193e2f926c90ff74f9cfb3b1b0  smoke.py
```

## DLL importate

Comando:

```bash
x86_64-w64-mingw32-objdump -p micropython.exe
```

Import rilevati:

```text
bcrypt.dll
KERNEL32.dll
msvcrt.dll
```

Sono tutte DLL di sistema. Non risultano dipendenze da `libgcc` o `libwinpthread`, quindi non serve modificare il link.

## Smoke test Linux di riferimento

```bash
runtime/out/lvsim-runtime runtime/out-w0-spike/smoke.py
```

Output, salvato in `runtime/out-w0-spike/smoke-linux.log`:

```text
clicked
Hello from LVGL - drew 240 px wide
```

## Smoke test preliminare con Wine

```bash
cd runtime/out-w0-spike
WINEDEBUG=-all wine build/micropython.exe smoke.py
```

Output, salvato in `runtime/out-w0-spike/smoke-wine.log`:

```text
clicked
Hello from LVGL - drew 240 px wide
```

## Checkpoint obbligatorio su Windows reale

**Superato il 2026-10-30.** Nunzio ha estratto il pacchetto in `C:\Users\racitin\Downloads\upython` ed eseguito da `cmd`:

```bat
micropython.exe smoke.py
```

Output reale riportato:

```text
clicked
Hello from LVGL - drew 240 px wide
```

**W0 è verde e chiuso.** Il risultato coincide con il riferimento Linux e autorizza il proseguimento con W1.
