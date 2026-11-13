import glob
import os
from pathlib import Path
import subprocess
import sys

import pytest

from lvgl_mpy_studio.build.web import serve
from lvgl_mpy_studio.gen.project_gen import generate_project
from tools.build_site import check_internal_links, load_demos

ROOT = Path(__file__).parents[1]
CHROME = sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell")))
needs_browser = pytest.mark.skipif(not CHROME or not (ROOT / "runtime/out-web/micropython.wasm").exists(), reason="browser runtime or headless Chromium not available")


def test_demo_metadata_is_valid_and_projects_generate(tmp_path):
    demos = load_demos(ROOT)
    assert {"fifteen", "breakout", "simon", "eim-01"} <= {metadata["id"] for metadata, _project in demos}
    for metadata, project in demos:
        if metadata["kind"] == "program":  # no pages to generate: the program runs as it is
            assert project.entry.is_file() and (project.display.width, project.display.height) == (1024, 600)
            continue
        assert metadata["id"] == project.projectName.lower() or metadata["id"] in {"eim-01", "meteo", "weather"}
        target = tmp_path / metadata["id"]
        generate_project(project, target)
        assert (target / "main.py").is_file()


def test_link_checker_rejects_missing_and_absolute_targets(tmp_path):
    (tmp_path / "index.html").write_text('<a href="missing/">Missing</a><img src="/absolute.png">', encoding="utf-8")
    with pytest.raises(RuntimeError) as error:
        check_internal_links(tmp_path)
    assert "missing/" in str(error.value) and "absolute path" in str(error.value)


@pytest.fixture(scope="session")
def built_site():
    environment = os.environ.copy()
    environment["NO_MKDOCS_2_WARNING"] = "1"
    subprocess.run([sys.executable, str(ROOT / "tools/build_site.py")], cwd=ROOT, env=environment, check=True, timeout=300)
    return ROOT / "build/site"


@needs_browser
def test_gallery_and_demos_in_chromium_under_a_subpath(built_site, tmp_path):
    sync_playwright = pytest.importorskip("playwright.sync_api").sync_playwright
    (tmp_path / "lvgl-mpy-studio").symlink_to(built_site, target_is_directory=True)
    server, server_url = serve(tmp_path)
    base_url = server_url + "lvgl-mpy-studio/"
    external_requests = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=CHROME[-1], headless=True, args=["--no-sandbox"])
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.on("request", lambda request: external_requests.append(request.url) if not request.url.startswith(server_url) else None)
            page.goto(base_url + "demos/", wait_until="networkidle")
            demos = load_demos(ROOT)
            assert page.locator(".demo-card").count() == len(demos)
            for metadata, _project in demos:
                card = page.locator(f"#{metadata['id']}")
                assert card.locator("img").evaluate("image => image.complete && image.naturalWidth > 0")
                response = page.request.get(base_url + f"demos/{metadata['id']}/")
                assert response.ok
            screenshots = ROOT / "build/site-screenshots"
            screenshots.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshots / "gallery-desktop.png"), full_page=True)
            page.set_viewport_size({"width": 390, "height": 844})
            page.screenshot(path=str(screenshots / "gallery-mobile.png"), full_page=True)
            page.set_viewport_size({"width": 1280, "height": 900})

            for metadata, _project in demos:
                page.goto(base_url + f"demos/{metadata['id']}/", wait_until="networkidle")
                page.wait_for_function("window.lms && window.lms.running", timeout=60000)
                if metadata["kind"] == "program":  # it answers what is typed, and fills the screen
                    page.wait_for_timeout(1500)
                    page.locator("#canvas").click()
                    page.keyboard.type("help")
                    page.keyboard.press("Enter")
                    page.wait_for_function("window.lms.output.join('\\n').includes('rmdir')", timeout=20000)
                from PySide6.QtGui import QImage

                image = QImage.fromData(page.locator("#canvas").screenshot())
                assert not image.isNull()
                step = 3 if metadata["kind"] == "program" else None  # thin text on black: a sparse grid misses it
                non_black = sum(
                    1
                    for x in range(0, image.width(), step or max(1, image.width() // 64))
                    for y in range(0, image.height() // (3 if step else 1), step or max(1, image.height() // 64))
                    if sum(image.pixelColor(x, y).getRgb()[:3]) > 72
                )
                assert non_black > 20, f"{metadata['id']}: canvas is black"
                assert "failed" not in (page.locator("#status").get_attribute("class") or "")
                if metadata["id"] == "eim-01":
                    page.screenshot(path=str(screenshots / "demo-desktop.png"), full_page=True)
                    page.set_viewport_size({"width": 390, "height": 844})
                    page.screenshot(path=str(screenshots / "demo-mobile.png"), full_page=True)
                    page.set_viewport_size({"width": 1280, "height": 900})

            page.goto(base_url + "demos/fifteen/", wait_until="networkidle")
            page.wait_for_function("window.lms && window.lms.running", timeout=60000)
            canvas = page.locator("#canvas")
            before = canvas.screenshot()
            canvas.click(position={"x": 240, "y": 318}, delay=150)
            page.wait_for_timeout(1500)
            assert canvas.screenshot() != before, "a touch on Play did not change the screen"
            assert not external_requests, f"external network requests: {external_requests}"
            browser.close()
    finally:
        server.shutdown()
