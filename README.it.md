# LVGL MPY Studio

[English](README.md)

IDE desktop per Linux e Windows x86-64 per progettare interfacce LVGL 9.5 in stile Visual Basic, eseguirle nel simulatore integrato e sulle board MicroPython, e generare codice MicroPython compatto o C portabile.

## Funzioni

- Designer con trascinamento che mostra il rendering LVGL reale.
- Gestori di evento in Python, con azioni in chiaro che inseriscono la chiamata LVGL esatta.
- Moduli Python tuoi, importati dai gestori e tra loro, nel simulatore, sulle board e in ogni build.
- Simulatore integrato con touch, tastiera e suono del buzzer.
- Un solo selettore per simulatore o board, con connessione automatica.
- Modifica dal vivo: le modifiche grafiche appaiono sulla board in esecuzione poco dopo averle fatte, senza riavviare.
- Budget di RAM e flash nella barra di stato.
- Eseguibili a file unico per Linux e Windows, e giochi che si giocano nel browser.
- Protezione dalle modifiche fatte fuori dall'IDE: salvare non sostituisce mai in silenzio ciò che ha scritto un agente o un altro programma.
- Test visivi e un [server MCP](docs/mcp.md) opzionale, con cui un agente AI lavora su progetti e board.
- Componenti Buzzer e Timer, senza alcun costo per i progetti che non li usano.
- Codice generato compatto: solo ciò che il progetto usa, con stili condivisi.
- Caricamento in bytecode sulle board con firmware compatibile.
- Esportazione dei sorgenti C portabili e dei sorgenti MicroPython per una board.

## Avvio

Servono Python 3.11+, un compilatore C, `pkg-config`, CMake, SDL2 con i suoi header di sviluppo e, per le finestre SDL senza display, `xvfb`. CMake compila la SDL2 statica dell'[eseguibile a file unico](#un-gioco-in-un-solo-file); il primo `runtime/build.sh` scarica anche i sorgenti di SDL2.

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
./runtime/build.sh
.venv/bin/lvgl-mpy-studio
```

Il progetto JSON è la fonte di verità: salva pagine, widget, proprietà e codice Python, moduli compresi. Un progetto con moduli si salva con lo schema 3, che l'IDE 0.3 non apre; uno senza moduli resta allo schema 2. Designer, Proprietà, Eventi e Codice aggiornano lo stesso documento tramite undo e redo. F5 avvia la destinazione scelta nel selettore accanto ad **Avvia** e Shift+F5 la ferma. Scegliendo una board, profilo e risoluzione vengono applicati al progetto. La lingua si cambia in **Impostazioni → Lingua**.

Il pulsante della risoluzione nella barra, per esempio **480×480**, cambia la risoluzione con un clic: elenca le misure delle board conosciute con il loro nome, le misure comuni, **Ruota** e **Personalizzata…**. Niente si sposta da solo: a ogni cambio l'IDE chiede cosa fare dei widget.

- **Adatta** mantiene le proporzioni, così cerchi e quadrati restano tali, tranne i widget che occupano quasi tutto il loro contenitore, che si allargano con lui. Ogni widget segue ciò a cui sta vicino: un bordo, il centro, il widget su cui è disegnato o il gruppo di cui fa parte, come una griglia di pulsanti. I widget larghi crescono con lo schermo, e le etichette si allargano quando il loro font non può rimpicciolire.
- **Stira** scala ogni asse per conto suo: la pagina resta piena, ma le forme cambiano.
- **Lascia dove sono** cambia solo lo schermo. Ogni pagina ricorda la risoluzione per cui è disegnata, e **Disponi → Adatta pagina alla risoluzione…** la adatta dopo, una pagina alla volta.

L'adattamento funziona in entrambi i sensi, verso schermi più grandi e più piccoli, e Ctrl+Z lo annulla. Non può garantire un risultato perfetto: su una pagina piccola e piena qualcosa può sovrapporsi, e i widget che finiscono fuori schermo vengono elencati nell'output.

Il [manuale](docs/manual.it.md) descrive l'IDE passo per passo, dal primo progetto alla distribuzione. La [guida alle board](docs/boards.it.md) spiega porte, upload, console, avvio automatico e CLI delle board.

La documentazione tecnica in `docs/` è in inglese.

## Moduli Python

Sotto **Moduli Python** nell'albero del progetto, il menu contestuale crea, apre, rinomina ed elimina i moduli `.py` del progetto. Gestori, codice generale e altri moduli li usano con `import <nome>`. Un modulo è un file a sé, quindi importa ciò che usa: un modulo nuovo parte con `import lvgl as lv` e `import ui`. **Cosa vuoi fare?** elenca le funzioni di ogni modulo. Un errore in un modulo viene indicato con il file e la riga del modulo, e il doppio clic nel pannello Errori lo apre lì. Rinominare o eliminare un modulo non riscrive il codice che lo importa: l'IDE avvisa prima ed elenca quei punti. I moduli arrivano al simulatore, alle board in bytecode, a ogni build e alla versione per il browser; l'esportazione C li esclude e lo dice.

## Demo interattiva

```bash
.venv/bin/lvgl-mpy-studio build examples/demo.json --target micropython --output dist
dist/Demo_LVGL-x86_64/run.sh
```

Nella finestra SDL il pulsante aggiorna un contatore tramite un gestore Python. Per modificare la demo, apri `examples/demo.json` nell'IDE e fai doppio clic sul pulsante per vedere il codice.

## Un gioco in un solo file

Per mandare un gioco a qualcuno, **Esegui → Crea eseguibile a file unico…** oppure `lvgl-mpy-studio build project.json --profile release --single-file` crea `dist/<progetto>`, di circa 5 MB, oppure `dist/<progetto>.exe` su Windows: un solo file con l'app, il runtime e SDL, che parte con un doppio clic. `--for windows` o `--for linux` lo crea per l'altro sistema: l'app dentro è lo stesso bytecode, quindi un gioco per Windows si può creare da Linux e viceversa. Un gioco per Linux creato su Windows arriva come `<progetto>.tar.gz`, perché i file di Windows non hanno il permesso di esecuzione: estrailo e avvia il gioco. È un lanciatore precompilato con l'app compilata accodata, quindi la creazione richiede meno di un secondo e nessun compilatore, anche dall'AppImage. `--licenses` stampa gli avvisi di licenza di terze parti e `--selftest` disegna un frame senza finestra. Un gioco per Windows non ha console, quindi entrambi scrivono in `<progetto>.log` accanto al gioco, e lavora nella propria cartella, come l'eseguibile a cartella. Il suo lanciatore nasce da `runtime/build_onefile_windows.sh`, che `runtime/build_windows.sh` esegue, e usa solo le DLL fornite con Windows. Il lanciatore nasce da `runtime/build_onefile.sh`, che `runtime/build.sh` esegue, e richiede la glibc del computer che l'ha compilato. Per mandare giochi a sistemi più vecchi compilalo una volta con `runtime/build_onefile_portable.sh`, che usa un container Ubuntu 22.04 tramite Docker: i giochi richiedono allora glibc 2.34 o successiva, quindi partono su Ubuntu 22.04, Debian 12, Fedora 35, Linux Mint 21 e successive. `packaging/build.sh` avvisa se il lanciatore richiederebbe una glibc più recente.

## Giochi nel browser

**Esegui → Apri nel browser** crea `dist/<progetto>-web/` e la apre nel browser tramite un piccolo server locale. La cartella contiene la pagina, un runtime WebAssembly di circa 6 MB con MicroPython e LVGL e il gioco compilato: copiala su un qualsiasi hosting, come Hostinger o GitHub Pages, per condividere il gioco con un link: vedi [Pubblicare i giochi sul web](docs/publish-web.it.md). Funziona con mouse e tocco, anche sui telefoni, e il Buzzer suona dal browser dopo il primo tocco. Dalla riga di comando, `lvgl-mpy-studio build project.json --web` crea la cartella e `lvgl-mpy-studio web project.json` la serve e la apre. Il runtime nasce da `runtime/build_web.sh`, che richiede l'SDK di Emscripten; di norma lo cerca in `cache/emsdk`.

## Test visivi

`lvgl-mpy-studio test project.json` disegna ogni pagina con il runtime reale, compreso il codice del progetto, e la confronta pixel per pixel con un PNG di riferimento in `visual/<larghezza>x<altezza>/` accanto al progetto. La prima volta esegui il comando con `--update` per scrivere i riferimenti, poi committali.

Se una pagina è diversa, il comando esce con stato 1 e scrive `<pagina>.actual.png` e `<pagina>.diff.png`, con i pixel cambiati in rosso. Anche un riferimento mancante è un fallimento, così la CI non può passare per caso. `--threshold` tollera un certo numero di pixel diversi per pagina, `--page` sceglie le pagine, `--baseline` indica un'altra cartella e `--design-only` non esegue il codice del progetto. Aggiungi `*.actual.png` e `*.diff.png` a `.gitignore`.

Ogni pagina viene catturata una volta, subito dopo il caricamento. Per provare il tocco aggiungi degli scenari in `visual/<larghezza>x<altezza>/scenarios.json`, accanto ai riferimenti, perché le coordinate dipendono dalla risoluzione:

```json
{"scenarios": [{"name": "lancio", "page": "main", "seed": 3, "steps": [
  {"action": "tap", "x": 512, "y": 300}, {"action": "wait", "ms": 1500},
  {"action": "screenshot", "label": "palla"}, {"action": "assert", "expr": "lives == 3"}]}]}
```

Uno scenario esegue gli stessi passi dello strumento MCP `simulate` con l'orologio simulato, quindi ogni esecuzione è identica, anche nelle date e negli orari: il tempo simulato parte sempre dal 1° gennaio 2026. Ogni passo `screenshot` e la schermata finale diventano riferimenti chiamati `<scenario>@<etichetta>.png`. Un `assert` fallito o un traceback Python fanno fallire lo scenario. `--scenario` sceglie gli scenari; con solo `--page` o solo `--scenario` l'altro tipo viene saltato. `--update` rifiuta una pagina o uno scenario che cambia tra due esecuzioni.

## Codice C

**Progetto → Esporta codice C…** scrive `ui.c`, `ui.h`, `ui_events.c` e `ui_events.h` in `export_c/`, accanto al progetto. Dipendono solo da `lvgl.h`, quindi puoi copiarli in qualsiasi progetto LVGL. I gestori sono stub con il Python originale come commento: non esiste una traduzione automatica da Python a C. Il tuo codice in `ui_events.c` viene conservato nelle esportazioni successive.

**Progetto → Esporta codice MicroPython…** scrive i sorgenti per la board del progetto in `export_py/`, accanto al progetto, e nell'IDE chiede quale board usare se il progetto non ne ha una. I file del simulatore in `build/` su una board non girerebbero. Copia i file in una cartella della board e avvia `app_main.py`: il firmware deve fornire LVGL e `display_driver`. L'esportazione sovrascrive i file, e l'IDE chiede conferma se ne hai modificato qualcuno. `lvgl-mpy-studio generate --target board` è la forma da riga di comando: richiede una board nel progetto o `--board-profile`, e senza `--force` non sovrascrive i file modificati.

## Limiti

- Piattaforme: Linux e Windows 10 22H2/11 x86-64, RGB565.
- Il codice utente è Python. Le board con C non sono ancora supportate: sulle board si può caricare solo MicroPython.
- Il designer non esegue il tuo codice, quindi gli oggetti creati dal codice non compaiono sul canvas.
- Il budget di RAM è misurato nel simulatore a 64 bit, quindi è una stima per eccesso sulle board a 32 bit.

## Test e pacchetti

I comandi per test, CLI e pacchetti sono in [README.md](README.md).

## Licenza

L'IDE è distribuito sotto GPL-3.0-or-later. Il codice generato per i tuoi progetti e i componenti che l'IDE vi incorpora sono sotto MIT, quindi i tuoi prodotti non diventano GPL. I dettagli sono in [LICENSING.md](LICENSING.md).

LVGL MPY Studio è un progetto indipendente e non è affiliato a LVGL né approvato dai suoi autori. LVGL è un nome dei rispettivi titolari.
