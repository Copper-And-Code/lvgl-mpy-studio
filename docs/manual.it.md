# Manuale di LVGL MPY Studio

LVGL MPY Studio è un ambiente visuale per creare interfacce grafiche con [LVGL](https://lvgl.io) e MicroPython, nello stile di Visual Basic: disegni le pagine trascinando i controlli, scrivi poche righe di Python per i loro eventi e provi tutto in un simulatore che usa lo stesso LVGL della board. Quando sei pronto carichi l'app su una board, ne crei un eseguibile da mandare agli altri o ne esporti il codice.

Questo manuale descrive la versione 0.4 ed è disponibile anche [in inglese](manual.md). Per i dettagli sulle board vedi la [guida alle board](boards.it.md), per gli agenti AI la [guida al server MCP](mcp.md).

## Indice

1. [Installazione e avvio](#1-installazione-e-avvio)
2. [Il primo progetto in cinque minuti](#2-il-primo-progetto-in-cinque-minuti)
3. [La finestra](#3-la-finestra)
4. [Pagine](#4-pagine)
5. [Widget e componenti](#5-widget-e-componenti)
6. [Disegnare la pagina](#6-disegnare-la-pagina)
7. [Risoluzione](#7-risoluzione)
8. [Scrivere il codice](#8-scrivere-il-codice)
9. [Il simulatore](#9-il-simulatore)
10. [Lavorare con una board](#10-lavorare-con-una-board)
11. [Memoria: flash e RAM](#11-memoria-flash-e-ram)
12. [Distribuire ed esportare](#12-distribuire-ed-esportare)
13. [Test visivi](#13-test-visivi)
14. [Riga di comando](#14-riga-di-comando)
15. [Agenti AI](#15-agenti-ai)
16. [Scorciatoie da tastiera](#16-scorciatoie-da-tastiera)
17. [Problemi comuni](#17-problemi-comuni)

## 1. Installazione e avvio

### Linux

Scarica `LVGL_MPY_STUDIO-x86_64.AppImage`, rendilo eseguibile e avvialo:

```bash
chmod +x LVGL_MPY_STUDIO-x86_64.AppImage
./LVGL_MPY_STUDIO-x86_64.AppImage
```

Non serve installare altro: Python, Qt, il simulatore e il compilatore di MicroPython sono dentro il file.

### Windows

Estrai **tutta** la cartella `LVGL_MPY_STUDIO-<versione>-portable-win64.zip` e apri `LVGL_MPY_STUDIO.exe`. Python non va installato. Se l'IDE non parte, `LVGL_MPY_STUDIO_console.bat` lo avvia con una console che mostra gli errori.

Gli eseguibili non sono firmati: al primo avvio Windows SmartScreen può mostrare un avviso. Scegli **Ulteriori informazioni → Esegui comunque**.

Esiste anche un installer (`LVGL_MPY_STUDIO-<versione>-Setup-win64.exe`) che installa in `%LOCALAPPDATA%` senza permessi di amministratore.

### Lingua e tema

L'IDE parte in inglese ed è disponibile anche in italiano: **Settings → Language**, poi **Impostazioni → Lingua**. Il tema segue quello del sistema, chiaro o scuro.

## 2. Il primo progetto in cinque minuti

Costruiamo una pagina con un pulsante che conta i tocchi.

1. **File → Nuovo** (Ctrl+N). Il progetto parte con una pagina vuota chiamata `main`.
2. Nella **Toolbox** a sinistra trascina un **Label** sulla pagina e poi un **Button**. Mentre trascini vedi il controllo sulla pagina, già allineato alla griglia.
3. Seleziona l'etichetta: nel pannello **Proprietà** a destra cambia `text` in `Tocchi: 0`. Il nome dell'etichetta è `label1`, quello del pulsante `button1`.
4. Fai **doppio clic sul pulsante**. Si apre la scheda **Codice** sul gestore del suo evento principale, `button1_clicked`, come in Visual Basic.
5. Scrivi:

   ```python
   global tocchi
   tocchi += 1
   ui.label1.set_text("Tocchi: %d" % tocchi)
   ```

6. In alto nella scheda **Codice** scegli **(Generale)** e scrivi `tocchi = 0`: è il codice del modulo, eseguito una volta all'avvio.
7. Premi **F5**. Si apre la scheda **Simulatore**: clicca il pulsante e il numero sale.
8. **File → Salva** (Ctrl+S). Il progetto è un unico file `.json`.

Se non ricordi come si cambia un testo o si legge un valore, guarda il riquadro **Cosa vuoi fare?** accanto all'editor: con un doppio clic inserisce il codice giusto. Ne parliamo nella [sezione 8](#8-scrivere-il-codice).

## 3. La finestra

| Zona | Cosa contiene |
|---|---|
| **Barra degli strumenti** | Nuovo, Apri, Salva, Annulla, Ripeti, Griglia, zoom, il pulsante della **risoluzione** (per esempio `480×480`), il selettore della **destinazione** (Simulatore o una board), **Avvia** e **Interrompi** |
| **Toolbox** (a sinistra in alto) | I widget da trascinare sulla pagina, divisi per categoria, con una casella di ricerca |
| **Progetto** (a sinistra in basso) | Le pagine e, sotto ognuna, i suoi widget e componenti. Il menu col tasto destro gestisce le pagine |
| **Area centrale** | Una scheda per ogni pagina, la scheda **Codice** e la scheda **Simulatore** |
| **Proprietà** (a destra) | Le proprietà del widget selezionato, **Per categoria** o in ordine alfabetico, e la scheda **Eventi** |
| **Pannelli in basso** | **Output** (messaggi), **Errori** (con doppio clic porta alla riga del codice), **Componenti** (Buzzer e Timer della pagina) e **Console dispositivo** (REPL della board) |
| **Barra di stato** | Messaggi, il **budget** di flash e RAM e, se una board è connessa, il suo stato con il pulsante **Disconnetti** |

I pannelli si spostano e si staccano; **Visualizza** li fa ricomparire se li chiudi.

## 4. Pagine

Un progetto ha una o più pagine, come i form di Visual Basic. Le gestisci dal menu **Progetto** o con il tasto destro su una pagina nell'albero **Progetto**:

- **Aggiungi pagina**, **Rinomina pagina**, **Elimina pagina**.
- **Imposta pagina iniziale**: quella che compare all'avvio dell'app.

Nel codice ogni pagina ha una costante: la pagina `Gioco` è `ui.PAGE_GIOCO`. Per passare a un'altra pagina:

```python
ui.load_page(ui.PAGE_GIOCO)
```

Rinominando una pagina, i suoi gestori la seguono; se il codice usa ancora la vecchia costante `PAGE_…`, l'IDE te lo segnala nell'output.

Ogni pagina ha l'evento **SCREEN_LOADED**, che scatta quando la pagina compare: è il posto giusto per preparare lo stato, per esempio per azzerare una partita. Lo trovi nella scheda **Codice** scegliendo la pagina come oggetto.

## 5. Widget e componenti

### Widget

| Categoria | Widget |
|---|---|
| **Basic** | Button, Label, Panel |
| **Input** | Slider, Switch, Checkbox, Text Area, Dropdown, Roller, Spinbox, Keyboard |
| **Display** | Arc, Bar, LED, Spinner |
| **Data** | Chart, Scale, Table |
| **Media** | Image, Image Button |
| **Container** | Button Matrix, Calendar, Line, List, Message Box, Span |
| **Navigation** | Menu, Tab View, Tile View, Window |

Ogni widget ha un nome unico nel progetto, per esempio `button1`, che usi nel codice come `ui.button1`. Il nome si cambia dal pannello **Proprietà**; i gestori lo seguono, e se il codice usa ancora il vecchio nome l'IDE ti dice dove.

Un widget può stare dentro un altro, come in un **Panel**: trascinalo sopra il contenitore. Le sue coordinate diventano relative al contenitore. Eliminando, copiando o duplicando un contenitore si prendono anche i widget che contiene.

### Immagini

Per mostrare un'immagine, trascina un **Image** sulla pagina e, in **Proprietà**, premi il pulsante **…** accanto a `src` e scegli un file. L'immagine entra nel progetto:

- viene convertita in PNG, e rimpicciolita se è più grande dello schermo;
- viene salvata dentro il file del progetto, che resta un solo file da copiare o inviare;
- va ovunque vada il progetto: simulatore, board, eseguibili, versione per il browser ed esportazione C.

L'immagine ha un nome, per esempio `logo.png`, mostrato in `src`: scrivi lo stesso nome in un altro Image per mostrarla di nuovo. Un solo Annulla toglie sia la scelta sia l'immagine.

Su una board un'immagine costa memoria: i byte del PNG, più circa 4 byte per pixel mentre è sullo schermo. Un'icona 100×100 chiede circa 40 kB; uno sfondo intero 480×480 circa 900 kB, più di quanto molte board hanno libero. L'output elenca le immagini pesanti e gli Image la cui immagine non è nel progetto.

### Font

Il testo è disegnato con Montserrat, il font incluso in LVGL, nelle misure che la destinazione ha (vedi [Risoluzione](#7-risoluzione) e la guida alle board). Per usare un altro font, o una misura che la board non ha, aggiungi un font al progetto: in **Proprietà**, premi **…** accanto a `font` e scegli un file `.ttf` o `.otf`. Poi imposta `fontSize` alla misura che vuoi.

- Il file del font viene salvato dentro il file del progetto. Scrivi il suo nome nel `font` di un altro widget per usarlo di nuovo.
- Quando si genera il codice il font viene convertito per ogni misura in uso, con i caratteri ASCII stampabili e quelli dei widget che lo usano. Il testo impostato dal codice può usare quei caratteri; un carattere che il font non ha viene elencato nell'output.
- I glifi sono gli stessi che produrrebbe il convertitore di LVGL. Viene convertito anche il kerning, cioè la spaziatura fine tra particolari coppie di lettere come «AV».
- Su una board ogni misura convertita costa memoria, circa due volte e mezza il suo peso: circa 30 kB per l'ASCII a 24 pixel. Al caricamento l'IDE avvisa quando i font occuperebbero più di metà della RAM libera della board. L'esportazione C comprende i font del progetto e li carica dalla memoria: serve `LV_USE_FS_MEMFS` in `lv_conf.h`.

### Componenti

I componenti non si vedono sulla pagina: compaiono nel pannello **Componenti** in basso.

- **Buzzer**: suona sulla board e nel simulatore, con l'altoparlante del computer.
  - `ui.buzzer1.beep(880, 60)` suona 880 Hz per 60 millisecondi.
  - `ui.buzzer1.tone(440)` suona finché non chiami `ui.buzzer1.off()`.
  - Su una board il suono va dove indica il profilo: un pin, oppure un altoparlante. Se il profilo non ha un buzzer, le chiamate non fanno nulla.
- **Timer**: chiama il suo evento **TICK** ogni `period` millisecondi.
  - Proprietà `period` e `enabled` (se parte da solo).
  - Nel codice: `ui.timer1.pause()`, `ui.timer1.resume()`, `ui.timer1.set_period(500)`.
  - È il modo giusto per animazioni e giochi: un ciclo `while` nel codice bloccherebbe l'interfaccia.
- **Digital Output** (sotto **Hardware**): un pin della board acceso o spento, per un LED o un relè.
  - Proprietà `pin`, `active_low` (l'uscita è accesa quando il pin è basso) e `initial` (accesa all'avvio).
  - Nel codice: `ui.digital_output1.on()`, `.off()`, `.toggle()`, `.set(True)`, `.value()`.
  - Nel simulatore non c'è un pin: ogni cambiamento viene scritto nel pannello Output.
- **Digital Input** (sotto **Hardware**): un pin che viene letto, per un pulsante o un interruttore.
  - Proprietà `pin`, `pull` (la resistenza interna), `active_low` e `debounce` in millisecondi.
  - Eventi **PRESSED**, **RELEASED** e **CHANGED**; nel gestore `e` è l'ingresso stesso: `e.value()`.
  - Nel simulatore l'ingresso cambia solo quando il codice chiama `ui.digital_input1.simulate(True)`.

Il pin è come MicroPython lo chiama su quella board: un numero, come `25`, oppure un nome, come `PA5` sulle board STM32. L'IDE non sa quali pin usa il display: scegline uno libero.

### Blocchi

Buzzer, Digital Output e Digital Input sono *blocchi*: cartelle con una descrizione (`block.json`) e moduli MicroPython. Altre persone possono scrivere blocchi, e tu puoi aggiungerli:

- **Impostazioni → Gestione blocchi…** elenca i blocchi, da dove viene ciascuno, autore e licenza, e quali componenti del progetto aperto lo usano.
- **Aggiungi da cartella…** installa il blocco di una cartella che hai scaricato; **Rimuovi** elimina uno che hai installato; **Ricarica** rilegge la cartella dei blocchi; **Apri cartella dei blocchi** la mostra.
- Un progetto conserva una copia dei blocchi che usa e che non sono forniti con l'IDE, così si apre anche su un computer che non li ha. **Installa dal progetto** installa un blocco di questo tipo su questo computer.
- Il simulatore esegue il codice di un blocco sul tuo computer, come esegue il codice di un progetto: installa blocchi di persone di cui ti fidi.

`docs/blocks.md` spiega come scriverne uno, con `examples/blocks/blinker` come esempio.

## 6. Disegnare la pagina

- **Aggiungere**: trascina un widget dalla Toolbox sulla pagina. La griglia (**Visualizza → Griglia**) lo allinea.
- **Spostare e ridimensionare**: trascina il widget o le sue maniglie. Per valori precisi usa `x`, `y`, `width` e `height` nel pannello **Proprietà**.
- **Selezione multipla**: trascina un rettangolo sulla pagina vuota, oppure tieni premuto Ctrl mentre clicchi.
- **Copiare**: Taglia, Copia, Incolla, **Duplica** (Ctrl+D) ed Elimina, anche dal menu col tasto destro.
- **Disponi**: con due o più widget selezionati puoi allinearli a sinistra, al centro, a destra, in alto, al centro verticale o in basso, e distribuirli in orizzontale o in verticale.
- **Ordine di disegno**: **Porta in primo piano** (Ctrl+]) e **Porta in fondo** (Ctrl+[). I widget disegnati dopo coprono quelli prima.
- **Anteprima LVGL reale** (**Visualizza**): la pagina viene disegnata dal vero LVGL, con i font e gli stili che vedrai sulla board, invece che dall'approssimazione del designer.
- **Zoom**: Ctrl++ e Ctrl+−; **Adatta alla finestra** con Ctrl+0.
- **Annulla e Ripeti** valgono per ogni modifica, anche del codice.

## 7. Risoluzione

La risoluzione è quella dello schermo per cui disegni, ed è la stessa del simulatore. Dopo un cambio la pagina viene di nuovo adattata alla finestra. La cambi con un clic dal pulsante nella barra degli strumenti, per esempio **480×480**:

- **Board**: le risoluzioni delle board conosciute, con il loro nome.
- **Comuni**: 240×240, 480×480, 1024×600 e 1024×1024.
- **Ruota**: scambia larghezza e altezza.
- **Personalizzata…**: larghezza e altezza a scelta.

Quando la risoluzione cambia, l'IDE chiede cosa fare dei widget. Niente si sposta da solo:

- **Adatta** mantiene le proporzioni: cerchi e quadrati restano tali. Ogni widget segue ciò a cui sta vicino: un bordo, il centro, il widget su cui è disegnato o il gruppo di cui fa parte, come una griglia di pulsanti. I widget che occupano quasi tutta la larghezza, come uno sfondo, si allargano con lo schermo; le etichette crescono se il loro font non può rimpicciolire. Funziona verso schermi più grandi e più piccoli.
- **Stira** scala ogni asse per conto suo: la pagina resta piena, ma le forme si deformano.
- **Lascia dove sono** cambia solo lo schermo. Ogni pagina ricorda per quale risoluzione era disegnata, e più tardi **Disponi → Adatta pagina alla risoluzione…** la adatta, una pagina alla volta.

La scelta viene ricordata per la volta successiva, e Ctrl+Z annulla tutto in un colpo. Su una pagina piccola e piena qualcosa può sovrapporsi: i widget che finiscono fuori schermo vengono elencati nell'output.

Se il progetto è legato a una board di un'altra risoluzione, la board viene scollegata e si torna al simulatore; la finestra te lo dice prima.

**Progetto → Impostazioni progetto…** offre le stesse risoluzioni, più il profilo board.

Il codice può leggere la risoluzione reale, utile per adattare un gioco a ogni schermo:

```python
larghezza = lv.display_get_default().get_horizontal_resolution()
altezza = lv.display_get_default().get_vertical_resolution()
```

## 8. Scrivere il codice

### Come funziona

Come in Visual Basic, ogni evento di un widget ha un **gestore**: una funzione Python che scatta quando l'evento avviene. Nella scheda **Codice**:

- a sinistra scegli l'**Oggetto**: un widget, una pagina, un componente, oppure **(Generale)**;
- a destra la **Procedura**, cioè l'evento: `CLICKED`, `VALUE_CHANGED`, `PRESSED`, `RELEASED`, `LONG_PRESSED`, `SCREEN_LOADED`, `TICK` e altri.

Scegliendo un evento che non ha ancora codice, l'IDE crea il gestore. Il doppio clic su un widget nel designer apre direttamente il suo evento principale: `CLICKED` per un pulsante, `VALUE_CHANGED` per uno slider o uno switch, `TICK` per un timer.

Scrivi solo il **corpo** del gestore: l'IDE ci mette intorno `def button1_clicked(e):`. Il parametro `e` è l'evento LVGL, se ti serve.

### (Generale)

Il codice di **(Generale)** è il modulo: viene eseguito una volta, all'avvio, prima che compaia la prima pagina. Ci metti le variabili condivise, le costanti e le tue funzioni. Dentro un gestore, per cambiare una variabile del modulo serve `global`, come in ogni programma Python:

```python
# (Generale)
punteggio = 0

def aggiungi(punti):
    global punteggio
    punteggio += punti
    ui.punti.set_text(str(punteggio))
```

### Moduli Python

Quando il codice cresce, puoi dividerlo in **moduli**: file `.py` del progetto, che i gestori, il codice di **(Generale)** e gli altri moduli usano con `import`.

1. Nel pannello **Progetto**, fai clic destro su **Moduli Python** e scegli **Nuovo modulo Python…**.
2. Dai un nome, per esempio `gioco`: lettere minuscole, cifre e `_`. Non si possono usare i nomi dei moduli di MicroPython, come `time` o `json`, né quelli dei file che crea l'IDE, come `ui` o `main`, né il nome di un gestore. Se il nome non va bene, l'IDE spiega perché e lo ripropone.
3. Il modulo si apre nell'editor del codice, già con `import lvgl as lv` e `import ui`. Un modulo è un file a sé: `ui` e `lv` non arrivano da soli come nei gestori, e va importato tutto ciò che usa.

```python
# gioco.py
import lvgl as lv
import ui


def mostra(testo):
    ui.label1.set_text(testo)
```

Poi, in un gestore o in **(Generale)**:

```python
import gioco
gioco.mostra("Ciao dal modulo")
```

Il doppio clic su un modulo nell'albero lo apre; il clic destro lo **rinomina** o lo **elimina**. L'IDE non riscrive mai gli `import`: se il codice importa ancora il modulo, prima di rinominarlo o eliminarlo ti avvisa che quegli import si fermeranno con `ImportError` ed elenca dove sono. Annulla modifica (Ctrl+Z) riporta tutto com'era.

I moduli vanno ovunque vada il progetto: nel simulatore, sulla board in bytecode, negli eseguibili e nella versione per il browser. L'esportazione C non li comprende, e lo segnala.

### Usare i widget

Ogni widget è `ui.<nome>`, e i suoi metodi sono quelli di LVGL. Alcuni esempi:

```python
ui.label1.set_text("Ciao")                         # cambia il testo di un'etichetta
ui.button1.get_child(0).set_text("OK")             # cambia il testo di un pulsante
valore = ui.slider1.get_value()                    # legge uno slider
acceso = ui.switch1.has_state(lv.STATE.CHECKED)    # legge uno switch
ui.label1.add_flag(lv.obj.FLAG.HIDDEN)             # nasconde un widget
ui.label1.remove_flag(lv.obj.FLAG.HIDDEN)          # lo mostra
ui.button1.add_state(lv.STATE.DISABLED)            # lo disabilita
```

### Cosa vuoi fare?

Non serve ricordare l'API di LVGL. Accanto all'editor il riquadro **Cosa vuoi fare?** elenca, per ogni widget, le azioni più comuni: cambia il testo, leggi il valore, nascondi, disabilita, apri questa pagina, leggi la larghezza dello schermo e così via. Cerca un oggetto o un'azione nella casella in alto e fai doppio clic: il codice giusto viene inserito nell'editor, con il cursore sul valore da cambiare. Anche i moduli compaiono qui, come i componenti: **Importa il modulo**, le sue funzioni, le classi e le costanti in maiuscolo. Nel modulo aperto il gruppo **Questo modulo** elenca le sue funzioni, da chiamare senza il nome davanti.

Nell'editor, dopo `ui.` o `ui.label1.`, **Ctrl+Spazio** mostra i suggerimenti.

### Errori

Gli errori di sintassi compaiono nel pannello **Errori** quando avvii l'app, e sotto l'editor mentre scrivi; un errore durante l'esecuzione compare con l'eccezione, e passando sopra la riga si vede il traceback intero. Il doppio clic porta al gestore o al modulo e alla riga giusti, che viene evidenziata, anche se l'errore è avvenuto sulla board.

Se l'errore nasce in un modulo, la prima riga è quella del modulo; il gestore che l'ha chiamato segue, marcato **chiamato da qui**.

### Stampa

**File → Stampa sorgenti…** (Ctrl+P) stampa il sorgente aperto nell'editor, oppure tutti i sorgenti del progetto: il codice generale, i gestori scritti come le funzioni che diventano, e ogni modulo, ciascuno da una pagina nuova. Le pagine riportano il nome del progetto e del sorgente, la data e il numero di pagine; le righe sono numerate e colorate come nell'editor, e una riga lunga va a capo invece di essere tagliata. **Anteprima…** mostra prima le pagine. Per avere un PDF, scegli la stampa su file nella finestra di stampa del sistema.

## 9. Il simulatore

- **F5** (**Esegui → Avvia**) avvia l'app nella scheda **Simulatore**, con il vero LVGL e il vero MicroPython.
- **Shift+F5** la ferma, **Esegui → Riavvia** la fa ripartire.
- Il mouse fa da dito, la tastiera funziona e il Buzzer suona dall'altoparlante del computer.
- I `print` del tuo codice compaiono nel pannello **Output**.

Mentre il simulatore è avviato il progetto è in sola lettura: una barra sopra l'editor lo ricorda, e il pulsante **Ferma e modifica** ferma l'app. Un errore in un gestore non ferma l'app, quindi dopo un errore il simulatore di solito è ancora avviato.

## 10. Lavorare con una board

La [guida alle board](boards.it.md) spiega tutto nel dettaglio; qui il percorso essenziale.

1. Collega la board via USB. Serve un firmware MicroPython con LVGL e il driver del display; i requisiti di ogni board sono nella guida.
2. Nel selettore accanto ad **Avvia** scegli la board. La risoluzione del progetto diventa quella della board, e l'IDE chiede come adattare i widget, come in [sezione 7](#7-risoluzione).
3. Premi **F5**: se c'è una sola porta seriale viene usata, altrimenti te la chiede una volta. L'app viene caricata ed eseguita; ciò che la board stampa compare in **Console dispositivo**.
4. **Shift+F5** ferma l'app. **Disconnetti** nella barra di stato libera la porta per altri programmi.

**Console dispositivo** è un terminale collegato alla board ogni volta che è connessa e l'IDE non sta usando la porta. Ogni tasto arriva alla board appena lo premi, come in PuTTY o picocom: al prompt `>>>` le frecce richiamano le righe precedenti e Tab completa, e un programma che legge la tastiera, come una shell o un editor, riceve ogni tasto. Colori e movimenti del cursore delle sequenze ANSI vengono mostrati.

- Ctrl+C e gli altri tasti Ctrl vanno alla board. Copia e incolla sono su **Ctrl+Maiusc+C** e **Ctrl+Maiusc+V**, e nel menu del tasto destro. Un testo incollato viene scritto riga per riga.
- Il pulsante **Ctrl-C** ferma il programma in esecuzione; **Ctrl-D** al prompt fa un soft reset.
- Mentre l'IDE carica, ferma o interroga la board, il terminale aspetta e lo dice in alto. Queste operazioni interrompono il programma che gira sulla board.
- Le righe grigie sono messaggi dell'IDE, non della board.

Altre voci del menu **Dispositivo**:

- **Modifica dal vivo**: con l'app avviata sulla board, ogni modifica alla pagina compare sulla board in meno di un secondo, senza ricaricare tutto. Le modifiche al codice richiedono F5.
- **Carica progetto** copia l'app senza avviarla; **Carica ed esegui** la copia e la avvia.
- **Informazioni dispositivo**: firmware, versione di LVGL, memoria, touch e compatibilità con il profilo.
- **Installa avvio automatico…**: l'app parte da sola all'accensione della board. **Rimuovi avvio automatico…** ripristina il lanciatore di prima, salvato dall'IDE.
- **Gestisci profili board…**: i profili descrivono display, touch, buzzer e requisiti di ogni board.

Ogni progetto ha un identificativo suo, quindi sulla board finisce in una cartella separata e non sovrascrive altre app, anche se hanno lo stesso nome.

Nel selettore della destinazione, **Usa come predefinito per i nuovi progetti** fa partire i nuovi progetti già con quella board e la sua risoluzione.

## 11. Memoria: flash e RAM

Nella barra di stato l'IDE mostra quanta **flash** occupa l'app compilata e quanta **RAM** usa all'avvio, aggiornati mentre lavori. Con una board scelta, i valori diventano gialli o rossi quando ti avvicini ai suoi limiti.

La RAM è misurata nel simulatore, che è a 64 bit: sulle board a 32 bit l'uso reale è più basso.

## 12. Distribuire ed esportare

### Eseguibile a cartella

**Esegui → Crea eseguibile…** crea in `dist/<progetto>-x86_64/` (o `-win64` su Windows) una cartella con il gioco, il runtime e le licenze. Su Linux si avvia con `run.sh`, su Windows con il `.exe`.

### Eseguibile a file unico

**Esegui → Crea eseguibile a file unico…** crea **un solo file**, di circa 5 MB, da mandare a chi deve solo usare l'app: `dist/<progetto>` su Linux, `dist/<progetto>.exe` su Windows. Si apre con un doppio clic, senza installare nulla.

- Su Linux parte su Ubuntu 22.04, Debian 12, Fedora 35, Mint 21 e successive.
- Su Windows usa solo le librerie di sistema. Non ha console: messaggi ed errori vanno in `<progetto>.log`, accanto al gioco.
- `--licenses` mostra le licenze dei componenti inclusi, `--selftest` disegna un frame senza aprire la finestra.
- Dalla riga di comando puoi creare il file per l'altro sistema: `--for windows` crea il `.exe` da Linux, `--for linux` crea il file Linux da Windows. Da Windows il file Linux arriva come `<progetto>.tar.gz`, perché Windows non conosce il permesso di esecuzione: estrailo e avvialo.

### Versione per il browser

**Esegui → Apri nel browser** crea la versione web del gioco in `dist/<progetto>-web/` e la apre nel browser. È la stessa app, con il vero LVGL e il vero MicroPython compilati in WebAssembly: si gioca con mouse o dito, e il Buzzer suona dal browser dopo il primo tocco, perché i browser non lasciano suonare una pagina prima di un gesto.

Per condividere il gioco con un link, copia tutta la cartella su un hosting, per esempio Hostinger, GitHub Pages o Netlify: la guida [Pubblicare i giochi sul web](publish-web.it.md) spiega i passi, anche per più giochi insieme. La pagina non funziona aperta direttamente come file, con doppio clic su `index.html`: il browser vuole un indirizzo web. Per questo l'IDE la apre con un piccolo server locale, attivo finché l'IDE resta aperto.

### Codice MicroPython per una board

**Progetto → Esporta codice MicroPython…** scrive in `export_py/`, accanto al progetto, i file per la board del progetto, da copiare a mano o da integrare in un altro progetto. Se il progetto non ha una board, l'IDE chiede quale usare. Se hai modificato un file esportato, l'IDE chiede conferma prima di sovrascriverlo.

### Codice C

**Progetto → Esporta codice C…** scrive in `export_c/` i file `ui.c`, `ui.h`, `ui_events.c` e `ui_events.h`, che dipendono solo da `lvgl.h` e si usano in qualsiasi progetto LVGL in C. I gestori sono funzioni vuote con il tuo Python come commento: il codice C lo scrivi tu in `ui_events.c`, e l'IDE lo conserva alle esportazioni successive.

## 13. Test visivi

I test visivi controllano che le pagine restino uguali mentre il progetto cambia.

```bash
lvgl-mpy-studio test project.json --update   # la prima volta: scrive le immagini di riferimento
lvgl-mpy-studio test project.json            # le volte dopo: confronta pixel per pixel
```

Le immagini di riferimento stanno in `visual/<larghezza>x<altezza>/` accanto al progetto. Se una pagina cambia, il comando fallisce e scrive `<pagina>.diff.png` con i pixel cambiati in rosso.

Per provare anche i tocchi, aggiungi degli **scenari** in `visual/<larghezza>x<altezza>/scenarios.json`:

```json
{"scenarios": [{"name": "lancio", "page": "main", "seed": 3, "steps": [
  {"action": "tap", "x": 512, "y": 300},
  {"action": "wait", "ms": 1500},
  {"action": "screenshot", "label": "palla"},
  {"action": "assert", "expr": "vite == 3"}]}]}
```

Uno scenario gira con un orologio simulato, quindi ogni esecuzione è identica, date comprese. Ogni `screenshot` e la schermata finale diventano immagini di riferimento; un `assert` falso o un errore Python fanno fallire il test. I passi disponibili sono gli stessi dello strumento `simulate` degli agenti AI, descritti nella [guida al server MCP](mcp.md).

## 14. Riga di comando

L'IDE ha anche una riga di comando, `lvgl-mpy-studio` (con l'AppImage: `./LVGL_MPY_STUDIO-x86_64.AppImage <comando>`).

| Comando | Cosa fa |
|---|---|
| `lvgl-mpy-studio` | apre l'IDE; il progetto si apre poi da **File → Apri** o da **File → File recenti** |
| `lvgl-mpy-studio run project.json` | avvia il progetto nel simulatore |
| `lvgl-mpy-studio generate project.json` | genera il codice (`--target micropython`, `c` o `board`) |
| `lvgl-mpy-studio build project.json` | crea l'eseguibile; `--profile release --single-file` per il file unico, `--for windows` o `--for linux` per l'altro sistema, `--web` per la versione per il browser |
| `lvgl-mpy-studio web project.json` | crea la versione per il browser, la serve e la apre; Ctrl+C la ferma |
| `lvgl-mpy-studio test project.json` | test visivi; `--update`, `--page`, `--scenario`, `--threshold` |
| `lvgl-mpy-studio device list` | elenca le board collegate; `info`, `upload`, `run`, `stop`, `reset`, `repl`, `autostart-install`, `autostart-remove` operano su una board con `--port` |
| `lvgl-mpy-studio mcp` | avvia il server per gli agenti AI |
| `lvgl-mpy-studio selftest` | l'IDE si usa da solo e riferisce cosa funziona; vedi sotto |
| `lvgl-mpy-studio --version` | mostra la versione |

### Collaudo automatico

`lvgl-mpy-studio selftest` apre l'IDE e lo usa come farebbe una persona: crea un progetto, prende i widget dalla casella, ne imposta le proprietà nel pannello, scrive un gestore, salva, avvia il simulatore e tocca lo schermo. Altri scenari coprono pagine, risoluzione, immagini e font, moduli Python, Timer e Buzzer, ed errori. Ogni passo è verificato e scritto come `PASSED` o `FAILED`; l'ultima riga è `RESULT: PASSED` o `RESULT: FAILED`, e il comando termina con 0 o 1. Il rapporto è in inglese.

- Senza opzioni l'IDE resta nascosto e servono pochi secondi. `--show` lo mostra al lavoro, rallentato; `--slow 800` imposta la pausa dopo ogni azione, in millisecondi.
- Il rapporto va in `lvgl-mpy-studio-selftest/<data-ora>/` nella cartella corrente, o nella cartella indicata con `--output`: `report.txt`, `report.json`, i progetti salvati in `work/`, e per ogni passo fallito un'immagine dell'IDE e del simulatore.
- `--list` elenca gli scenari; indicandone uno o più si eseguono solo quelli.
- Impostazioni, file recenti e profili delle board non vengono toccati. Non usare mouse e tastiera sulla finestra dell'IDE mentre gira con `--show`.

Verifica che le cose funzionino, non il loro aspetto, e non usa le board.

## 15. Agenti AI

LVGL MPY Studio può essere usato da un agente AI, come Claude o Kimi, tramite il **Model Context Protocol** (MCP). L'agente crea progetti, disegna pagine, scrive il codice, prova il gioco nel simulatore toccando lo schermo, misura la memoria e, con te presente, lavora sulla board.

Il server è spento finché non lo accendi da **Impostazioni → Server MCP per agenti AI**. La [guida al server MCP](mcp.md) spiega come collegarlo al tuo agente e cosa può fare. Due regole pratiche:

- se il progetto è aperto anche nell'IDE, l'IDE si accorge delle modifiche dell'agente quando salvi, e chiede se **ricaricare** il file, **salvare una copia**, **sovrascrivere** o annullare: niente viene scritto senza una scelta. Le modifiche fatte nell'IDE non compaiono all'agente finché non salvi;
- prima di far usare la board all'agente, disconnettila dall'IDE.

Lo stesso controllo vale per ogni programma che scrive il file del progetto, compresa la riga di comando. Se il file è stato eliminato, l'IDE propone di ricrearlo o di salvarlo altrove. **Salva con nome** chiede conferma prima di sostituire un altro file.

## 16. Scorciatoie da tastiera

| Tasti | Azione |
|---|---|
| Ctrl+N, Ctrl+O, Ctrl+S, Ctrl+Shift+S | Nuovo, Apri, Salva, Salva con nome |
| Ctrl+P | Stampa sorgenti |
| Ctrl+Z, Ctrl+Shift+Z | Annulla, Ripeti |
| Ctrl+X, Ctrl+C, Ctrl+V, Canc | Taglia, Copia, Incolla, Elimina |
| Ctrl+D | Duplica |
| Ctrl+A | Seleziona tutto |
| Ctrl+], Ctrl+[ | Porta in primo piano, Porta in fondo |
| Ctrl++, Ctrl+−, Ctrl+0 | Aumenta zoom, Riduci zoom, Adatta alla finestra |
| F5, Shift+F5 | Avvia, Interrompi |
| Ctrl+Spazio | Suggerimenti nell'editor |
| Ctrl+Q | Esci |

## 17. Problemi comuni

**Il simulatore non parte o si chiude subito.** Guarda i pannelli **Errori** e **Output**: un errore nel codice del modulo, o di un gestore `SCREEN_LOADED`, ferma l'app all'avvio. Il doppio clic sull'errore porta alla riga.

**Il progetto non si modifica.** Mentre il simulatore o un'app sulla board sono avviati il progetto è in sola lettura: premi **Ferma e modifica** sopra l'editor, o Shift+F5.

**`NameError: name 'ui' isn't defined` in un modulo.** Un modulo non riceve `ui` e `lv` come i gestori: aggiungi in cima `import ui` e `import lvgl as lv`.

**`ImportError` dopo aver rinominato o eliminato un modulo.** Il codice importa ancora il vecchio nome: aggiorna gli `import` che l'IDE ha elencato in **Output**, o annulla con Ctrl+Z.

**La board non risponde: `could not enter raw repl`.** Sulla board c'è un programma che non si ferma con Ctrl+C. L'IDE insiste con più Ctrl+C, e basta per le shell che ne chiedono due, come quella di alcuni firmware dell'ESP32-4848S040. Se non basta, chiudi gli altri programmi che usano la porta, premi il tasto di reset della board e riprova.

**Sulla board non si sente il Buzzer.** Il profilo della board deve indicare un pin o un altoparlante; i profili inclusi lo fanno dove la board ha un buzzer. Nel dubbio guarda **Dispositivo → Gestisci profili board…**.

**La porta seriale è occupata.** Un solo programma alla volta può usarla: chiudi altri terminali seriali, o disconnetti l'IDE se la deve usare un agente AI o `mpremote`.

**Ho cambiato risoluzione e qualcosa si sovrappone.** Ctrl+Z annulla, poi prova l'altra scelta, oppure sistema a mano i widget elencati nell'output come fuori area.

**L'eseguibile a file unico non parte su un Linux vecchio.** Serve glibc 2.34 o successiva, cioè Ubuntu 22.04, Debian 12 o più recenti. Su Windows, se non parte, guarda `<progetto>.log` accanto al file.

**Windows dice che l'app non è sicura.** Gli eseguibili non sono firmati: **Ulteriori informazioni → Esegui comunque**.
