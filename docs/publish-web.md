# Publishing games on the web

[Italiano](publish-web.it.md)

This guide explains how to put online one or more games made with LVGL MPY Studio, so that anyone can play them in the browser from a link, also on a phone. The example uses **Hostinger**, but the steps apply to any web host: it is only a matter of copying files.

No special server or database is needed: the web version of a game is a folder of static files.

## 1. Building the web version

For each game:

1. Open the project in the IDE.
2. Choose **Run → Open in Browser**. The IDE creates the folder `dist/<game>-web/` next to the project and opens it in the browser: try it there before publishing.

Or, from a terminal:

```bash
lvgl-mpy-studio build project.json --web
```

The folder holds:

| File | What it is for |
|---|---|
| `index.html` | the page of the game |
| `lms_web.js` | starts the game and plays the Buzzer |
| `micropython.mjs`, `micropython.wasm` | MicroPython and LVGL compiled for the browser, about 6 MB, the same for every game |
| `game/` | the compiled game |
| `licenses/` | the licence notices of the included components |
| `.htaccess` | tells the server what kind of files `.wasm` and `.mjs` are |

The `.htaccess` file starts with a dot, so many programs hide it: it is there, and it is needed. See [section 5](#5-if-the-game-does-not-start).

Build the folder again every time you change the game: the IDE replaces it.

## 2. Organising one or more games

Each game goes in its own folder. For simple addresses, rename it in lower case and without spaces. A convenient layout:

```text
public_html/
└── games/
    ├── index.html         ← list of games, optional (section 4)
    ├── breakout/          ← the content of dist/Breakout-web/
    │   ├── index.html
    │   ├── .htaccess
    │   └── …
    └── orbit/             ← the content of dist/Orbit-web/
        ├── index.html
        └── …
```

The addresses become `https://yourdomain.com/games/breakout/` and `https://yourdomain.com/games/orbit/`.

Each folder holds a copy of the 6 MB runtime. With a few games this is not a problem, and the browser downloads the runtime only once per game.

## 3. Uploading the files to Hostinger

### With the File Manager, the simplest way

1. On your computer, compress each folder into a ZIP. On Linux, from the `dist` folder:

   ```bash
   cd dist
   cp -r Breakout-web breakout && zip -r breakout.zip breakout && rm -r breakout
   ```

   On Windows: right-click the folder → **Compress to ZIP file**, after renaming it to `breakout`. The ZIP keeps the `.htaccess` file too.
2. Go to **hPanel**, open the site and go to **Files → File Manager**.
3. Enter `public_html` and create the folder `games`: `public_html` is the folder of your site, and what is in it shows at `https://yourdomain.com/`.
4. Enter `games`, upload `breakout.zip` with the upload button, then right-click the file → **Extract**. The folder `breakout` must appear with `index.html` inside.
5. Delete the ZIP.
6. Repeat for the other games.

### With FTP, convenient if you update often

1. In **hPanel → Files → FTP Accounts** you find server, user and password, and can create one.
2. Connect with an FTP program, for example FileZilla, using those details.
3. Drag the game folders into `public_html/games/`.
4. In FileZilla, to see and upload `.htaccess` too, turn on **Server → Force showing hidden files**.

### Trying it

Open `https://yourdomain.com/games/breakout/` in the browser. "Loading…" appears, then the game. The first time loading takes a few seconds, to download the runtime; afterwards the browser keeps it in its cache. Sound starts after the first touch or click on the page, because browsers do not let a page play sound before a gesture.

## 4. A page listing the games

Optional, but convenient to share: one link for all the games. Save this file as `index.html` inside `public_html/games/` and adapt the list:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>My games</title>
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
<h1>My games</h1>
<ul>
  <li><a href="breakout/">Breakout<small>Drag the paddle, break the bricks</small></a></li>
  <li><a href="orbit/">Orbit<small>Defend the ring from the swarm</small></a></li>
</ul>
</body>
</html>
```

Each entry points to the folder of the game, with the trailing slash.

## 5. If the game does not start

Open the developer tools of the browser (F12), **Console** tab.

**"Failed to load module script… MIME type"** or **"Incorrect response MIME type. Expected 'application/wasm'"**
The server does not know what kind of files `.mjs` and `.wasm` are. Check that `.htaccess` is in the folder of the game. If you do not see it in the File Manager, look in its settings for the option to show hidden files. If it is really missing, upload it again, or create it with this content:

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

You can check the result in the **Network** tab: clicking `micropython.wasm`, the `Content-Type` header must be `application/wasm`. If `.htaccess` is there but nothing changes, ask Hostinger support to enable those MIME types for the site.

**"404" on `game/files.json` or on a `.mpy` file**
The `game` folder was not uploaded, or ended up in the wrong place. It must be next to `index.html`.

**The page stays blank or on "Loading…" when opened as a file**
You opened `index.html` with a double click from your computer. The browser wants a web address: use the address of the site, or **Run → Open in Browser** from the IDE.

**The game works but there is no sound**
Touch or click the page once: sound starts only after a gesture. Also check that the browser tab is not muted.

**The game is slow on an old phone**
MicroPython and LVGL run in the browser, so on a weak phone a game with many moving objects can slow down. The [Memory section](manual.md#11-memory-flash-and-ram) of the manual and the redraw statistics of `simulate` help to see how much work the game does at each frame.

## 6. Other hosts

The same steps apply elsewhere:

- **Other hosts with Apache or LiteSpeed**, such as SiteGround or OVH: copy the folders with the File Manager or FTP. The included `.htaccess` should work; if the game does not start, check the MIME types as in section 5.
- **GitHub Pages, Netlify, Cloudflare Pages**: they already know `.wasm` and `.mjs`, and the `.htaccess` file is ignored. Just upload the folders, or drag them onto the Netlify upload page.
- **Nginx on your own server**: `.htaccess` does not count. Check that `/etc/nginx/mime.types` holds `application/wasm wasm;` and `text/javascript js mjs;`.
