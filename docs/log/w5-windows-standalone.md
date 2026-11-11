# W5 — Eseguibile autonomo MicroPython per Windows

Data: 2026-10-30.

## Stato

Implementazione e prove locali completate. Il gate su `windows-latest` e il doppio clic sul PC Windows restano da verificare; Wine non chiude questi gate.

## Implementazione

- `runtime/build_windows.sh` produce anche `lvsim-standalone.exe`, separato dal runtime usato dall'IDE.
- `runtime/variant-win64/lvsim_standalone.c` avvia `import main; main.main()` senza argomenti, gestisce `--selftest`, ripulisce `LVSIM_*`, usa la cartella dell'eseguibile come directory di lavoro e scrive stdout/stderr in `<progetto>.log`.
- Il wrapper vive nella variant out-of-tree; nessuna patch a MicroPython, SDL o PyDevices.
- `lvgl_ide/build/release.py` crea `dist/<progetto>-win64/` con `<progetto>.exe`, `SDL2.dll`, quattro `.mpy` e `project.json`, quindi genera il file `<progetto>-win64.zip`.
- L'eseguibile distribuito usa il subsystem PE GUI (2), senza finestra console. Il profilo Release Windows comunica che richiede la toolchain; Debug resta il profilo predefinito.
- Su Windows i percorsi predefiniti di runtime e `mpy-cross` usano `runtime/out-win64`.

## Verifiche

Comando:

```bash
QT_QPA_PLATFORM=offscreen .venv/bin/pytest -q \
  tests/test_windows_release.py tests/test_portability.py tests/test_release.py --maxfail=1
```

Risultato iniziale dopo l'implementazione: 13 test superati. La prova reale del pacchetto è stata successivamente estesa per usare i file estratti dallo ZIP.

La prova con Wine copre:

- avvio senza argomenti da una directory corrente diversa e scrittura di `NO_ARGS_OK` nel log;
- `--selftest` senza variabili `LVSIM_*` esterne e dump RGB565 da 800×480×2 byte;
- subsystem PE modificato da console (3) a GUI (2);
- contenuto della cartella e dello ZIP, percorsi Unicode e nomi sanificati;
- rifiuto di un PE non valido e messaggio esplicito per Release senza toolchain.

## Prova su Windows reale

Dopo aver estratto lo ZIP, da `cmd`:

```bat
<progetto>.exe --selftest
```

Atteso: codice di uscita 0, `selftest.raw` di 768.000 byte e `<progetto>.log` accanto all'eseguibile. Il doppio clic su `<progetto>.exe` deve aprire la finestra SDL senza console.
