# W7 — Pacchetto IDE Windows e CI

Data: 2026-10-30.

## Stato

Configurazione implementata e controlli statici locali superati. PyInstaller, Inno Setup e il workflow non sono ancora stati eseguiti su Windows reale: il repository GitHub non è stato pubblicato.

## Artefatti previsti

- `LVGL_IDE-<versione>-win64.zip`: cartella PyInstaller onedir portabile.
- `LVGL_IDE-<versione>-Setup-win64.exe`: installer Inno Setup per utente in `%LOCALAPPDATA%\Programs\LVGL IDE`, senza privilegi di amministratore.

`packaging/build_windows.ps1` esegue PyInstaller su Windows, crea lo ZIP e compila l'installer. `-SkipInstaller` consente di creare soltanto lo ZIP durante lo sviluppo.

## Contenuto

- IDE con `console=False` e moduli Qt/PySide6 in DLL separate dentro `_internal`.
- `lvsim-runtime.exe`, `lvsim-standalone.exe`, `mpy-cross.exe`, SDL2 e `liblvgl.a`.
- Header/import library SDL2, sorgenti e configurazione LVGL necessari al target C.
- Guida toolchain `docs/windows-c.md`, `NOTICE.txt` e `THIRD_PARTY.md`.
- Nota SmartScreen nel README; nessuna firma del codice nella v1.1.

## CI

`package-windows` dipende dai test runtime/C e GUI Windows, scarica gli artefatti compilati su Linux, esegue `packaging/build_windows.ps1`, avvia `LVGL_IDE.exe --version` e pubblica ZIP e installer.

L'artefatto `lvgl-c-source` trasferisce `lv_conf.h` e i sorgenti LVGL dal job Linux ai runner Windows, perché `.reference` non è versionato.

## Verifica locale

`tests/test_windows_packaging.py`: 3 test superati per sintassi dello spec, onedir senza console, contenuti runtime, installer per utente e produzione ZIP/Inno. Restano da verificare installazione, avvio GUI e flusso completo su un PC Windows pulito.

Suite completa: **544 passed** in 547,98 secondi. Build Windows integrata ripetuta con successo, inclusa `liblvgl.a`. AppImage Linux ricostruita: `--version` restituisce `0.2.1` e l'avvio GUI offscreen supera lo smoke test.

## Portabile con Python incluso

`packaging/build_windows_portable.sh` assembla Python embeddable 3.12.10, le wheel Windows delle dipendenze pinnate, l'IDE e i runtime Windows, quindi produce `dist/LVGL_IDE-0.2.1-portable-win64.zip`. Include `LVGL_IDE.exe`, avviatore nativo senza console, e `LVGL_IDE_console.bat` per la diagnostica. ICU4C 72.1 e la relativa licenza sono inclusi per compatibilità anche con ambienti privi delle DLL di sistema.

Verifica effettuata dopo l'estrazione dello ZIP: `--version` restituisce `0.2.1` sia tramite Python incluso sia tramite l'avviatore; import Qt riuscito; build MicroPython Debug e `--selftest` riusciti, con framebuffer da 768.000 byte e log creato. La GUI Wine si arresta su `mscms.dll.WcsCreateIccProfile`, funzione non implementata da Wine ma disponibile su Windows: il checkpoint GUI su Windows reale resta aperto.
