import glob
import os
from pathlib import Path
import subprocess
import urllib.request

import pytest

from lvgl_mpy_studio.build import web
from lvgl_mpy_studio.cli import main
from lvgl_mpy_studio.core.model import Project

ROOT = Path(__file__).parents[1]
needs_web_runtime = pytest.mark.skipif(not (ROOT / "runtime/out-web/micropython.wasm").exists(), reason="browser runtime not built: runtime/build_web.sh")
CHROME = sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell")))


def project(name="Gioco <bello>"):
    result = Project(name)
    result.set_display_size(320, 240)
    result.add_widget(result.pages[0], "panel", {"x": 0, "y": 0, "width": 320, "height": 240, "bgColor": "#FF0000"}, name="sfondo")
    return result


@needs_web_runtime
def test_web_folder_has_the_page_runtime_and_game(tmp_path):
    folder = web.build_web(project(), tmp_path)
    assert folder.name == "Gioco-bello-web"
    names = {path.name for path in folder.iterdir()}
    assert {"index.html", "lms_web.js", "micropython.mjs", "micropython.wasm", "game", "licenses"} <= names
    page = (folder / "index.html").read_text(encoding="utf-8")
    assert "<title>Gioco &lt;bello&gt;</title>" in page and 'width="320" height="240"' in page and "{" + "width}" not in page
    game = sorted(path.name for path in (folder / "game").iterdir())
    assert "main.mpy" in game and "display_driver.mpy" in game and "files.json" in game
    assert not list(tmp_path.glob(".*"))
    htaccess = (folder / ".htaccess").read_text(encoding="utf-8")
    assert "AddType application/wasm .wasm" in htaccess and "AddType text/javascript .js .mjs" in htaccess


@needs_web_runtime
def test_web_build_replaces_only_its_own_folder(tmp_path):
    folder = web.build_web(project(), tmp_path)
    (folder / "vecchio.txt").write_text("x", encoding="utf-8")
    assert not (web.build_web(project(), tmp_path) / "vecchio.txt").exists()
    other = tmp_path / "Altro-web"
    other.mkdir()
    with pytest.raises(ValueError, match="Altro-web"):
        web.build_web(project("Altro"), tmp_path)


def test_web_build_without_runtime_says_how_to_get_it(tmp_path, monkeypatch):
    monkeypatch.setattr(web, "web_runtime", lambda: tmp_path / "missing")
    with pytest.raises(FileNotFoundError, match="build_web.sh"):
        web.build_web(project(), tmp_path)


def test_server_gives_webassembly_its_type(tmp_path):
    (tmp_path / "a.wasm").write_bytes(b"\0asm")
    (tmp_path / "b.mjs").write_text("export {}", encoding="utf-8")
    server, url = web.serve(tmp_path)
    try:
        with urllib.request.urlopen(url + "a.wasm") as response:
            assert response.headers["Content-Type"] == "application/wasm"
        with urllib.request.urlopen(url + "b.mjs") as response:
            assert response.headers["Content-Type"].startswith("text/javascript")
    finally:
        server.shutdown()


@needs_web_runtime
def test_cli_builds_the_web_version(tmp_path, capsys):
    path = tmp_path / "progetto.json"
    project("Cli").save(path)
    assert main(["build", str(path), "--web", "--output", str(tmp_path / "dist")]) == 0
    assert (tmp_path / "dist" / "Cli-web" / "index.html").exists()
    assert capsys.readouterr().out.strip().endswith("index.html")


@needs_web_runtime
@pytest.mark.skipif(not CHROME, reason="headless Chromium not available")
def test_game_draws_in_a_real_browser(tmp_path):
    from PySide6.QtGui import QImage

    folder = web.build_web(project(), tmp_path)
    server, url = web.serve(folder)
    try:
        shot = tmp_path / "shot.png"
        subprocess.run([CHROME[-1], "--no-sandbox", "--window-size=400,320", "--virtual-time-budget=8000", f"--screenshot={shot}", url], capture_output=True, timeout=120)
    finally:
        server.shutdown()
    image = QImage(str(shot))
    assert not image.isNull()
    red = sum(1 for x in range(0, image.width(), 4) for y in range(0, image.height(), 4) if image.pixelColor(x, y).red() > 200 and image.pixelColor(x, y).green() < 60)
    assert red > 500, "the canvas does not show the red background of the game"
