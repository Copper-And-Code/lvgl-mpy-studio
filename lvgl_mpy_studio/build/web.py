"""Web version of a game: a folder to open in the browser or publish on static hosting."""

from functools import partial
import html
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import threading

from lvgl_mpy_studio.gen.project_gen import app_modules, generate_project
from .compiler import compile_python, root_dir
from .release import THIRD_PARTY_LICENSES, project_name

RUNTIME_FILES = ("micropython.mjs", "micropython.wasm")
MARKER = ".lvgl-mpy-studio-web"  # only a folder created here can be replaced
# For hosting on Apache or LiteSpeed, such as Hostinger: without the right types the browser
# refuses the JavaScript module and the WebAssembly. Elsewhere the file is ignored.
HTACCESS = """<IfModule mod_mime.c>
    AddType application/wasm .wasm
    AddType text/javascript .js .mjs
    AddType application/octet-stream .mpy
</IfModule>
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE application/wasm text/javascript application/json
</IfModule>
"""


def web_runtime():
    return root_dir() / "runtime" / "out-web"


def web_template():
    return root_dir() / "runtime" / "web"


def build_web(project, dist_root=None):
    """Create dist/<project>-web/ with the page, the WebAssembly runtime and the compiled game."""
    runtime = web_runtime()
    missing = [name for name in RUNTIME_FILES if not (runtime / name).exists()]
    if missing:
        raise FileNotFoundError("Browser runtime not found: run runtime/build_web.sh")
    dist_root = Path(dist_root) if dist_root else root_dir() / "dist"
    target = dist_root / f"{project_name(project)}-web"
    if target.exists() and not (target / MARKER).exists():
        raise ValueError(f"{target} already exists and is not a web build made by this IDE: move or rename it")
    staging = dist_root / f".{target.name}.tmp"
    generated = dist_root / f".{target.name}-generated"
    shutil.rmtree(staging, ignore_errors=True)
    try:
        generate_project(project, generated)
        compile_python(generated)
        game = staging / "game"
        game.mkdir(parents=True)
        names = []
        for name in app_modules(generated):  # the same list as the single file, user modules included
            path = generated / f"{name}.mpy"
            shutil.copy2(path, game / path.name)
            names.append(path.name)
        (game / "files.json").write_text(json.dumps(names) + "\n", encoding="utf-8", newline="\n")
        template = web_template()
        page = (template / "index.html").read_text(encoding="utf-8")
        page = page.replace("{title}", html.escape(project.projectName)).replace("{width}", str(project.display.width)).replace("{height}", str(project.display.height))
        (staging / "index.html").write_text(page, encoding="utf-8", newline="\n")
        shutil.copy2(template / "lms_web.js", staging)
        for name in RUNTIME_FILES:
            shutil.copy2(runtime / name, staging)
        shutil.copytree(THIRD_PARTY_LICENSES, staging / "licenses")
        (staging / MARKER).write_text("", encoding="utf-8", newline="\n")
        (staging / ".htaccess").write_text(HTACCESS, encoding="utf-8", newline="\n")
        if target.exists():
            shutil.rmtree(target)
        staging.rename(target)
    finally:
        shutil.rmtree(generated, ignore_errors=True)
        shutil.rmtree(staging, ignore_errors=True)
    return target


class _QuietHandler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, ".mjs": "text/javascript", ".wasm": "application/wasm", ".mpy": "application/octet-stream"}

    def log_message(self, *_arguments):
        pass


def serve(directory, port=0):
    """Serve the folder on 127.0.0.1: JavaScript modules do not load from file://. Return (server, url)."""
    server = ThreadingHTTPServer(("127.0.0.1", port), partial(_QuietHandler, directory=str(directory)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/"
