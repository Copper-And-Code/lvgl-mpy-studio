# Pubblicare i giochi sul web

[English](publish-web.md)

Questa guida spiega come mettere online uno o più giochi creati con LVGL MPY Studio, in modo che chiunque possa giocarli dal browser con un link, anche da telefono. L'esempio usa **Hostinger**, ma i passi valgono per qualsiasi hosting web: si tratta solo di copiare file.

Non serve un server particolare né un database: la versione web di un gioco è una cartella di file statici.

## 1. Creare la versione web

Per ogni gioco:

1. Apri il progetto nell'IDE.
2. Scegli **Esegui → Apri nel browser**. L'IDE crea la cartella `dist/<gioco>-web/` accanto al progetto e la apre nel browser: provala lì prima di pubblicarla.

In alternativa, da terminale:

```bash
lvgl-mpy-studio build project.json --web
```

La cartella contiene:

| File | A cosa serve |
|---|---|
| `index.html` | la pagina del gioco |
| `lms_web.js` | avvia il gioco e suona il Buzzer |
| `micropython.mjs`, `micropython.wasm` | MicroPython e LVGL compilati per il browser, circa 6 MB, uguali per tutti i giochi |
| `game/` | il gioco compilato |
| `licenses/` | gli avvisi di licenza dei componenti inclusi |
| `.htaccess` | dice al server di che tipo sono i file `.wasm` e `.mjs` |

Il file `.htaccess` inizia con un punto, quindi molti programmi lo nascondono: c'è, e serve. Lo spiego alla [sezione 5](#5-se-il-gioco-non-parte).

Rigenera la cartella ogni volta che modifichi il gioco: l'IDE la sostituisce.

## 2. Organizzare uno o più giochi

Ogni gioco va in una sua cartella. Per avere indirizzi semplici, rinominala in minuscolo e senza spazi. Una struttura comoda:

```text
public_html/
└── giochi/
    ├── index.html         ← elenco dei giochi, facoltativo (sezione 4)
    ├── breakout/          ← il contenuto di dist/Breakout-web/
    │   ├── index.html
    │   ├── .htaccess
    │   └── …
    └── orbita/            ← il contenuto di dist/Orbita-web/
        ├── index.html
        └── …
```

Gli indirizzi diventano `https://tuodominio.it/giochi/breakout/` e `https://tuodominio.it/giochi/orbita/`.

Ogni cartella contiene una copia del runtime da 6 MB. Con pochi giochi non è un problema, e il browser scarica il runtime una sola volta per gioco.

## 3. Caricare i file su Hostinger

### Con il File Manager, il modo più semplice

1. Sul computer, comprimi ogni cartella in uno ZIP. Su Linux, dalla cartella `dist`:

   ```bash
   cd dist
   cp -r Breakout-web breakout && zip -r breakout.zip breakout && rm -r breakout
   ```

   Su Windows: tasto destro sulla cartella → **Comprimi in file ZIP**, dopo averla rinominata in `breakout`. Lo ZIP conserva anche il file `.htaccess`.
2. Entra in **hPanel**, apri il sito e vai su **File → File Manager**.
3. Entra in `public_html` e crea la cartella `giochi`: è la cartella del tuo sito, e ciò che sta qui dentro si vede su `https://tuodominio.it/`.
4. Entra in `giochi`, carica `breakout.zip` con il pulsante di upload, poi fai tasto destro sul file → **Estrai**. Deve comparire la cartella `breakout` con dentro `index.html`.
5. Cancella lo ZIP.
6. Ripeti per gli altri giochi.

### Con FTP, comodo se aggiorni spesso

1. In **hPanel → File → Account FTP** trovi server, utente e password, e puoi crearne una.
2. Collegati con un programma FTP, per esempio FileZilla, usando quei dati.
3. Trascina le cartelle dei giochi dentro `public_html/giochi/`.
4. In FileZilla, per vedere e caricare anche `.htaccess`, attiva **Server → Forza visualizzazione file nascosti**.

### Prova

Apri `https://tuodominio.it/giochi/breakout/` nel browser. Compare "Loading…", poi il gioco. La prima volta il caricamento richiede qualche secondo, per scaricare il runtime; le volte successive il browser lo tiene in memoria. Il suono parte dopo il primo tocco o clic sulla pagina, perché i browser non lasciano suonare una pagina prima di un gesto.

## 4. Una pagina con l'elenco dei giochi

Facoltativa, ma comoda da condividere: un solo link per tutti i giochi. Salva questo file come `index.html` dentro `public_html/giochi/` e adatta l'elenco:

```html
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>I miei giochi</title>
<style>
  body { margin: 0; padding: 24px; background: #101318; color: #d8dde6; font: 16px system-ui, sans-serif; }
  h1 { font-weight: 600; }
  ul { list-style: none; padding: 0; display: grid; gap: 12px; max-width: 480px; }
  a { display: block; padding: 16px 20px; border-radius: 10px; background: #1d2430; color: #fff; text-decoration: none; }
  a:hover { background: #2a3445; }
  small { display: block; color: #9aa4b2; margin-top: 4px; }
</style>
</head>
<body>
<h1>I miei giochi</h1>
<ul>
  <li><a href="breakout/">Breakout<small>Trascina la racchetta, rompi i mattoni</small></a></li>
  <li><a href="orbita/">Orbita<small>Difendi l'anello dallo sciame</small></a></li>
</ul>
</body>
</html>
```

Ogni voce punta alla cartella del gioco, con la barra finale.

## 5. Se il gioco non parte

Apri gli strumenti per sviluppatori del browser (F12), scheda **Console**.

**"Failed to load module script… MIME type"** oppure **"Incorrect response MIME type. Expected 'application/wasm'"**
Il server non sa che tipo di file sono `.mjs` e `.wasm`. Controlla che nella cartella del gioco ci sia `.htaccess`. Se nel File Manager non lo vedi, cerca nelle sue impostazioni l'opzione per mostrare i file nascosti. Se manca davvero, ricaricalo, oppure crealo con questo contenuto:

```apache
<IfModule mod_mime.c>
    AddType application/wasm .wasm
    AddType text/javascript .js .mjs
    AddType application/octet-stream .mpy
</IfModule>
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE application/wasm text/javascript application/json
</IfModule>
```

Puoi verificare il risultato nella scheda **Network**: cliccando su `micropython.wasm`, l'intestazione `Content-Type` deve essere `application/wasm`. Se `.htaccess` c'è ma non cambia nulla, chiedi al supporto di Hostinger di abilitare quei tipi MIME per il sito.

**"404" su `game/files.json` o su un file `.mpy`**
La cartella `game` non è stata caricata, o è finita al posto sbagliato. Deve stare accanto a `index.html`.

**La pagina resta bianca o su "Loading…" aperta come file**
Hai aperto `index.html` con un doppio clic dal computer. Il browser vuole un indirizzo web: usa l'indirizzo del sito, oppure **Esegui → Apri nel browser** dall'IDE.

**Il gioco funziona ma non si sente**
Tocca o clicca una volta sulla pagina: il suono parte solo dopo un gesto. Controlla anche che la scheda del browser non sia silenziata.

**Il gioco è lento su un telefono vecchio**
MicroPython e LVGL girano nel browser, quindi su un telefono poco potente un gioco con molti oggetti in movimento può rallentare. La [sezione Memoria](manual.it.md#11-memoria-flash-e-ram) del manuale e le statistiche di ridisegno di `simulate` aiutano a capire quanto lavoro fa il gioco a ogni frame.

## 6. Altri hosting

Gli stessi passi valgono altrove:

- **Altri hosting con Apache o LiteSpeed**, come Aruba, SiteGround o OVH: copia le cartelle via File Manager o FTP. Il `.htaccess` incluso dovrebbe funzionare; se il gioco non parte, controlla i tipi MIME come nella sezione 5.
- **GitHub Pages, Netlify, Cloudflare Pages**: riconoscono già `.wasm` e `.mjs`, e il file `.htaccess` viene ignorato. Basta caricare le cartelle, o trascinarle nella pagina di upload di Netlify.
- **Nginx su un tuo server**: `.htaccess` non conta. Controlla che `/etc/nginx/mime.types` contenga `application/wasm wasm;` e `text/javascript js mjs;`.
