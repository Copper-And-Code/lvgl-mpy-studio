# W2–W3 — Runtime Windows

Data: 2026-10-30.

## Stato

Cross-build e verifiche locali completate. I gate che richiedono Windows reale restano in sospeso fino alla disponibilità della CI o di un run manuale; Wine non viene contato come prova di correttezza Windows.

## Build

Comando:

```bash
./runtime/build_windows.sh
```

- MinGW-w64 GCC 13.2.0 POSIX, MicroPython 1.29.0 e binding ai pin esistenti.
- SDL2 2.30.9, pacchetto MinGW ufficiale con SHA-256 verificato.
- Variante out-of-tree `runtime/variant-win64`, senza modifiche upstream.
- Informazioni `VERSIONINFO` con LVGL IDE 0.2.1 e commit `59c0f12`, verificate nel binario.

Artefatti:

| File | Byte | SHA-256 |
|---|---:|---|
| `lvsim-runtime.exe` | 1819648 | `a1f74f7e9b99727d1d2e221da27fdc4296f78b0fcacf77a6244b3f839a708b87` |
| `mpy-cross.exe` | 437760 | `f5ba92367f0c52170b84c73d239af8dd7c727b81f968a6155acdd8f3b4d5841b` |
| `SDL2.dll` | 2284544 | `b67bca20a0a35c0e0689495f9f3095526aa6575543c2678646c1593107410800` |

DLL importate dal runtime: `SDL2.dll`, `bcrypt.dll`, `KERNEL32.dll`, `msvcrt.dll`, `WINMM.dll`, `WS2_32.dll`. Nessuna dipendenza da `libgcc` o `libwinpthread`.

## Verifiche locali

- Test C client/server POSIX e Win32: `NET_OK` su Linux e Wine, compilazione con `-Wall -Wextra -Werror -pedantic`.
- Import del runtime Windows con Wine: riuscito.
- `mpy-cross.exe --version`: MicroPython 1.29.0, mpy 6.3.
- Parità preliminare Linux/Wine: 30/30 frame RGB565 identici byte per byte.
- Protocollo Windows con token, HELLO v2, RECT, clic, STOP/KeyboardInterrupt e QUIT: riuscito con Wine.
- Smoke test headless 240×120: `W3_SMOKE_OK`, frame di 57.600 byte non nero.

## Pacchetto provvisorio

`dist/LVGL_IDE-W3-runtime-win64.zip` contiene runtime, compilatore, SDL2, driver, smoke test e test C.

Da `cmd`, nella cartella estratta:

```bat
set MICROPYPATH=.
set LVSIM_HEADLESS=1
set LVSIM_DUMP=smoke.raw
lvsim-runtime.exe smoke.py
net-test.exe
```

Output atteso: `W3_SMOKE_OK` e `NET_OK`. Il file `smoke.raw` deve essere di 57.600 byte. Questo run manuale non è ancora stato eseguito su Windows reale.
