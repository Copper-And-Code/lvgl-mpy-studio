# W6 — Target C su Windows

Data: 2026-10-30.

## Stato

Implementazione locale completata. Le prove con Wine sono preliminari; il gate richiede l'esecuzione della stessa matrice su `windows-latest` con MSYS2 MinGW64.

## Implementazione

- Il `main.c` generato usa `lvsim_time_ms()` e `lvsim_wait(5)` su entrambe le piattaforme; niente `clock_gettime`, `nanosleep` o `setenv` nel ramo Windows.
- Il Makefile seleziona `lvsim_net_win32.c`, `lvsim_time_win32.c`, Winsock e `winmm` con `OS=Windows_NT`; su Linux conserva la build LVGL incrementale.
- `runtime/build_c_windows.sh` produce `runtime/out-win64/liblvgl.a` con LVGL 9.5.0, gli stessi flag e lo stesso `lv_conf.h` del target Linux.
- Header e import library SDL2 sono inclusi negli artefatti; le app compilano soltanto `ui.c`, `ui_events.c`, `main.c` e il backend `lvsim`.
- `compile_c` rileva GCC, AR e Make dal `PATH`, da MSYS2 oppure da `LVGL_IDE_TOOLCHAIN`. Se mancano, mostra i collegamenti a `docs/windows-c.md`, MSYS2 e w64devkit. Nessuna toolchain viene scaricata automaticamente.
- Gli errori `C:\…\file.c:riga:colonna` sono riconosciuti dal parser.
- Il pacchetto C Windows contiene `<progetto>.exe`, SDL2 e ZIP; subsystem GUI, directory di lavoro e log sono coerenti con il target MicroPython.

## Verifiche locali

- Selftest C Windows con Wine in `Nunzio Raciti/Progetto è/build c`: frame RGB565 da 768.000 byte e log creato.
- Pacchetti C/MicroPython e test mirati: superati.
- Matrice `tests/test_windows_c.py -k parity`: **30 passed**, tutti i frame C Windows, MicroPython Windows e MicroPython Linux identici byte per byte. Durata: 299,16 secondi.

## CI

Il job Windows installa MSYS2 MinGW64 tramite `msys2/setup-msys2`, scarica runtime, `liblvgl.a` e SDL2 dal job Linux, quindi esegue selftest e parità. L'esito reale della CI resta in sospeso finché il repository non viene pubblicato.
