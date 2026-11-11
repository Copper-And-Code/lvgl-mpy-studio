# Board MicroPython

[English](boards.md)

### Prerequisiti e primo avvio

Il primo profilo è **Waveshare RP2350-Touch-LCD-4**: pannello ST7701S 480×480, UI LVGL 240×240 RGB565, touch GT911 e scala hardware 2×. Serve un firmware MicroPython con LVGL e i moduli `display_driver`, `rgbpanel` e `gt911` già installati. Copiare i file su una MicroPython generica non installa LVGL o i driver. L'IDE non aggiorna né sostituisce il firmware e non modifica `boot.py`.

1. Nel selettore accanto ad **Avvia** scegli la board. Il profilo e la risoluzione 240×240 vengono applicati al progetto in un'unica operazione annullabile; posizioni, dimensioni e font dei widget si adattano alla nuova risoluzione, ogni asse per conto suo, e vengono segnalati i widget che restano fuori area. I punti del widget Line non vengono scalati.
2. Premi **Avvia** (F5): se c'è una sola porta seriale viene usata, altrimenti ti viene chiesta una volta. La scelta è una preferenza locale per ogni board e non viene salvata nel progetto; **Cambia porta…** la modifica. Il codice C si ottiene da **Progetto → Esporta codice C…** e non si può caricare su una board.
3. La connessione si apre da sola e resta aperta per console e REPL. **Disconnetti** nella barra di stato libera la porta per altri strumenti.
4. **Dispositivo → Connetti** e **Informazioni dispositivo** servono a verificare firmware, LVGL, memoria, buffer, touch e compatibilità senza avviare nulla. Il controllo importa `display_driver` e può inizializzare il display; non avviene durante la semplice enumerazione delle porte.
5. **Carica progetto** copia senza avviare; **Carica ed esegui** copia e avvia. F5 usa la voce scelta nel selettore, Shift+F5 la ferma.

Il componente **Buzzer** usa il pin della chiave `buzzer` del profilo board: GPIO1 sulla Waveshare RP2350 e l'altoparlante tramite `audio.py` sulla ESP32-4848S040. Se il profilo non la indica, come sulla STM32H7, le chiamate non fanno nulla e l'IDE lo segnala. Un progetto il cui profilo salvato è precedente a questa chiave usa quella del profilo incluso con lo stesso id.

La scelta del selettore e il profilo board vengono salvati nel progetto (`runTarget`, `board`) e viaggiano con il file; la porta seriale no, perché dipende dal computer. **Usa come predefinito per i nuovi progetti**, nello stesso selettore, salva destinazione, board e risoluzione nelle preferenze locali; **Rimuovi predefinito** torna al comportamento iniziale.

L'applicazione viene generata in `build/board/<id-profilo>/` e trasferita in `/lms_apps/app_<hash>/`. L'hash deriva dal `projectId` salvato nel progetto, quindi progetti con lo stesso nome non si sostituiscono a vicenda; **Salva con nome** crea un nuovo id. I progetti creati prima dell'id lo ricevono al salvataggio successivo nell'IDE, e la loro vecchia cartella resta sulla board. La CLI non salva, quindi per quei file continua a usare la cartella basata sul nome. Prima del reset e del trasferimento tutti i sorgenti vengono compilati; gli errori sono ricollegati al gestore e alla riga originale e non attivano la nuova versione. Il probe verifica le versioni minime di MicroPython/LVGL, i moduli, le API, la risoluzione e il touch richiesti dal profilo del progetto. L'upload usa una directory temporanea, verifica le dimensioni dei file e conserva la versione precedente in `.previous`. Non cancella altre directory o file utente. Dopo un trasferimento interrotto ripeti l'upload: la directory temporanea viene ricreata e l'ultima versione attiva non viene sostituita fino alla verifica.

Il driver del firmware possiede framebuffer, touch e timer LVGL. Il codice generato non importa `lvsim`, non alloca un altro framebuffer e non crea un secondo event loop. Al termine del bootstrap l'app resta attiva grazie al timer del driver.

### STM32H7_CORE V1.3

Il profilo **STM32H7_CORE V1.3 (1024×600)** usa il pannello IPS LTDC 1024×600 RGB565, touch GT911 e scala 1×. Richiede MicroPython 1.29 o successivo, LVGL 9.5 o successivo e i moduli `display_driver`, `gt911` e `st_ltdc`. Selezionare la board nel selettore accanto ad **Avvia**: la risoluzione logica è 1024×600.

Il collegamento avviene tramite UART1 e convertitore CH340 a **115200 8N1**, normalmente `/dev/ttyUSB0` su Linux. La USB nativa non viene usata. L'IDE imposta DTR=1 e RTS=0 prima dell'apertura, attende 3 secondi per il boot e mantiene la stessa porta aperta per probe, upload, esecuzione e console. Non usare `mpremote` o un altro programma sulla stessa porta: RTS=1 tiene la scheda in reset e ogni riapertura provoca un hard reset. Il comando **Riavvia** usa il soft reset senza riaprire la porta. Le app vengono installate in `/flash/lms_apps/`; l'avvio automatico riguarda soltanto `/flash/main.py` e non modifica `display_config.py` né gli altri file utente.

### ESP32-4848S040

Il profilo **ESP32-4848S040 (480×480)** usa la risoluzione nativa 480×480 RGB565, touch GT911 e scala 1×. Richiede MicroPython 1.29 o successivo, LVGL 9.5 o successivo e i moduli `display_driver` e `gt911`. Il driver del display integra il supporto al pannello: il modulo separato `rgbpanel` non è richiesto. La connessione USB seriale usa `mpremote`, normalmente su `/dev/ttyUSB0`; le app vengono installate in `/lms_apps/` senza modificare `boot.py` o `main.py`.

### Modifica dal vivo

Mentre un'applicazione avviata dall'IDE è in esecuzione, **Dispositivo → Modifica dal vivo** invia le modifiche grafiche alla board circa mezzo secondo dopo l'ultima modifica, senza riavviare. Ricrea tutte le pagine fuori schermo, mostra la pagina aperta nel designer e poi elimina le vecchie. Lo stato dei moduli Python resta, ma quello dei widget, come un testo digitato o la posizione di uno slider, torna ai valori del progetto. Le modifiche a codice, Buzzer o Timer non vengono inviate: la barra di stato chiede di premere F5.

### Console, Stop e avvio automatico

La **Console dispositivo** mostra incrementalmente anche stampe e traceback prodotti dopo il bootstrap e accetta comandi REPL quando la sessione è pronta. Il lettore continuo viene sospeso durante i comandi che richiedono la porta, così esiste un solo proprietario della seriale. **Annulla operazione** interrompe un comando bloccato. **Interrompi** nel menu Dispositivo ferma sempre la board, anche quando è selezionato il simulatore; F5 e Shift+F5 usano invece la destinazione selezionata. Stop rimuove i moduli dell'app dalla cache e chiama `display_driver.stop()`. L'ultima immagine può restare sul display: lo scan-out continua anche quando il timer è fermo. Ogni nuova esecuzione effettua un soft reset per evitare timer e moduli obsoleti.

**Installa avvio automatico…** è un'azione separata da F5. Sostituisce `/main.py` con un launcher riconoscibile e salva un eventuale `main.py` precedente in `~/.config/lvgl-mpy-studio/autostart-backups/<id-board>/<app>/<transazione>/` (o sotto `XDG_CONFIG_HOME`). L'identità usa `machine.unique_id()`, non la porta USB. Ogni transazione verifica hash del launcher e backup; una modifica manuale, un manifest invalido o un backup mancante blocca il ripristino senza sovrascrivere file. **Rimuovi avvio automatico…** agisce solo sul launcher della transazione corrente e dell'app selezionata.

Se un'app in avvio automatico non risponde, usa la modalità sicura/recupero prevista dal firmware della board oppure scollega l'alimentazione, apri un altro strumento MicroPython e rimuovi soltanto il launcher `/main.py` riconoscibile. Non formattare il filesystem: i file dell'app restano in `/lms_apps/`.

### CLI

```bash
lvgl-mpy-studio --language it device list
lvgl-mpy-studio --language it device info --port /dev/ttyACM0
lvgl-mpy-studio device upload progetto.json --port /dev/ttyACM0
lvgl-mpy-studio device run progetto.json --port /dev/ttyACM0
lvgl-mpy-studio device stop --port /dev/ttyACM0
lvgl-mpy-studio device reset --port /dev/ttyACM0
lvgl-mpy-studio device repl --port /dev/ttyACM0
lvgl-mpy-studio device autostart-install progetto.json --port /dev/ttyACM0
lvgl-mpy-studio device autostart-remove progetto.json --port /dev/ttyACM0
```

Per un progetto senza profilo incorporato, aggiungi `--board-profile <id>`. `upload` e `run` accettano `--output <directory>`. Il progetto salva una copia portabile del profilo, quindi resta apribile anche se quel profilo non è presente nel catalogo locale.

Ctrl+C durante un comando non interattivo restituisce il codice 130. Nella REPL interattiva, Ctrl+C interrompe il programma remoto; esci dalla REPL con Ctrl+] secondo `mpremote`. Alla chiusura del comando la porta viene rilasciata. Non aprire contemporaneamente IDE, REPL e altri programmi sulla stessa porta.

### Lingua e profili

**Impostazioni → Lingua** cambia immediatamente italiano/inglese e salva la preferenza senza modificare il progetto. **Dispositivo → Gestisci profili board…** permette nuovo, modifica, duplicazione, eliminazione e ripristino. Le modifiche diventano persistenti solo con **Applica**. Modificare un profilo incluso crea una personalizzazione nella configurazione utente; eliminarlo lo nasconde. I progetti mantengono la propria copia e vengono aggiornati solo tramite **Aggiorna profilo del progetto**, con undo.

### Font

Un profilo può elencare in `fonts` le misure di Montserrat del suo firmware, per esempio `"fonts": [14, 16, 24, 32, 40]`. Un testo chiesto in una misura che la board non ha viene disegnato nella più vicina, allo stesso modo nell'anteprima del designer, nel simulatore e sulla board. Un profilo senza elenco vale 14, 16 e 24; un progetto senza board usa le cinque misure del simulatore: 14, 16, 24, 32 e 40.

A ogni caricamento l'IDE legge i font che il firmware ha davvero. Se sono diversi da quelli del profilo, il codice viene generato per i font della board e un avviso lo dice: aggiungi l'elenco al profilo per vedere lo stesso testo nell'anteprima. **Dispositivo → Informazioni dispositivo** mostra l'elenco come `fonts`.

Errori comuni:

- `device.busy`: chiudi REPL, monitor seriali o altre IDE che usano la porta.
- `device.permissions`: verifica i permessi della porta seriale e le regole della distribuzione; non copiare file come root.
- `device.absent`: ricollega la board e seleziona di nuovo la porta dopo un reset o una disconnessione USB.
- `device.timeout`: controlla che la board risponda; interrompi eventuali programmi bloccati prima di riprovare.
- `device.prerequisites`: installa un firmware con i moduli richiesti oppure correggi risoluzione/touch del profilo.
- `device.resolution`: imposta il progetto sulle dimensioni logiche del profilo; per questa Waveshare 240×240, non 480×480.
- `device.transfer.incomplete`: ripeti l'upload e controlla spazio libero e collegamento USB.
- `device.autostart.not-owned`: `/main.py` non è un launcher riconoscibile dell'IDE e non viene rimosso.
