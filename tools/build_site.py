#!/usr/bin/env python3
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage

from lvgl_mpy_studio.build.budget import measure_budget
from lvgl_mpy_studio.build.preview import render_with_log
from lvgl_mpy_studio.build.release import THIRD_PARTY_LICENSES
from lvgl_mpy_studio.build.visual import rgb565_to_rgb, write_png
from lvgl_mpy_studio.build.program import prepare_program, program_board
from lvgl_mpy_studio.build.web import RUNTIME_FILES, build_web, copy_program_files, copy_program_runtime, web_runtime, web_template
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.platform import runtime_path

ROOT = Path(__file__).parents[1]
REPOSITORY = "https://github.com/Copper-And-Code/lvgl-mpy-studio"
FIELDS = {"id", "name", "description", "kind", "page", "prompt", "prompt_note", "order"}
PROGRAM_FIELDS = FIELDS | {"entry"}  # a program without pages: the file to run, in the same folder


class ProgramDemo:
    """What the gallery needs of a program without pages: its name and the size of its screen."""

    def __init__(self, entry):
        self.entry = entry
        self.projectName = entry.parent.name
        board, width, height = program_board()
        self.board = board
        self.display = type("Display", (), {"width": width, "height": height})()


def load_demos(root=ROOT):
    demos = []
    for metadata_path in sorted((root / "examples").glob("*/demo.json")):
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        expected = PROGRAM_FIELDS if metadata.get("kind") == "program" else FIELDS
        if set(metadata) != expected:
            raise ValueError(f"{metadata_path}: expected fields {sorted(expected)}")
        if metadata["id"] != metadata_path.parent.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata["id"]):
            raise ValueError(f"{metadata_path}: id must be a URL-safe name matching its folder")
        for field in ("name", "description"):
            if not isinstance(metadata[field], str) or not metadata[field].strip():
                raise ValueError(f"{metadata_path}: {field} must be a non-empty string")
        if metadata["kind"] not in ("game", "application", "program"):
            raise ValueError(f"{metadata_path}: kind must be game, application or program")
        if not isinstance(metadata["order"], int) or isinstance(metadata["order"], bool):
            raise ValueError(f"{metadata_path}: order must be an integer")
        if metadata["prompt"] is not None and not isinstance(metadata["prompt"], str):
            raise ValueError(f"{metadata_path}: prompt must be a string or null")
        if metadata["prompt_note"] is not None and not isinstance(metadata["prompt_note"], str):
            raise ValueError(f"{metadata_path}: prompt_note must be a string or null")
        if metadata["prompt"] is None and not metadata["prompt_note"]:
            raise ValueError(f"{metadata_path}: a missing prompt needs prompt_note")
        if metadata["kind"] == "program":
            entry = metadata_path.parent / str(metadata["entry"])
            if Path(str(metadata["entry"])).name != metadata["entry"] or entry.suffix != ".py" or not entry.is_file():
                raise ValueError(f"{metadata_path}: entry must be a .py file of the folder")
            if metadata["page"] is not None:
                raise ValueError(f"{metadata_path}: a program has no pages: page must be null")
            demos.append((metadata, ProgramDemo(entry)))
            continue
        project = Project.load(metadata_path.with_name("project.json"))
        names = [page.name for page in project.pages]
        if metadata["page"] is not None and metadata["page"] not in names:
            raise ValueError(f"{metadata_path}: page must be null or one of {names}")
        demos.append((metadata, project))
    orders = [metadata["order"] for metadata, _project in demos]
    if len(orders) != len(set(orders)):
        raise ValueError("Demo order values must be unique")
    return sorted(demos, key=lambda item: item[0]["order"])


def write_thumbnail(project, page_index, path):
    pixels, log = render_with_log(project, page_index, design_only=False)
    if pixels is None:
        raise RuntimeError(f"Could not render {project.projectName}: {log.strip()}")
    save_thumbnail(rgb565_to_rgb(pixels), project.display.width, project.display.height, path)
    return log


def program_thumbnail(program, path, keys=b"ls\r"):
    """The screen of a program in the simulator for Linux, after it has started and typed keys."""
    width, height = program.display.width, program.display.height
    with tempfile.TemporaryDirectory(prefix="site-program-") as temporary:
        temporary = Path(temporary)
        saved = os.environ.get("XDG_CONFIG_HOME")
        os.environ["XDG_CONFIG_HOME"] = str(temporary / "config")  # the flash of this run, not the user's
        try:
            prepared = prepare_program(program.entry, width, height, program.board)
        finally:
            if saved is None:
                os.environ.pop("XDG_CONFIG_HOME")
            else:
                os.environ["XDG_CONFIG_HOME"] = saved
        frame = temporary / "frame.raw"
        environment = {**os.environ, "MICROPYPATH": ".", "LVSIM_HEADLESS": "1", "LVSIM_DUMP": str(frame), **prepared["environment"]}
        for name in ("LVSIM_CONNECT", "LVSIM_TOKEN", "LVSIM_SOCKET"):
            environment.pop(name, None)
        process = subprocess.Popen([str(runtime_path()), *prepared["arguments"]], cwd=prepared["boot"], env=environment, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            time.sleep(2)
            process.stdin.write(keys)
            process.stdin.flush()
            time.sleep(1.5)
        finally:
            process.kill()
            process.wait()
        data = frame.read_bytes() if frame.exists() else b""
        if len(data) != width * height * 2:
            raise RuntimeError(f"Could not capture {program.projectName}: no frame from the simulator")
    save_thumbnail(rgb565_to_rgb(data), width, height, path)


def save_thumbnail(rgb, width, height, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if width <= 480:
        write_png(path, rgb, width, height)
    else:
        image = QImage(rgb, width, height, width * 3, QImage.Format.Format_RGB888).copy()
        image = image.scaled(480, max(1, round(height * 480 / width)), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        if not image.save(str(path)):
            raise RuntimeError(f"Could not write thumbnail {path}")


def size_text(value):
    return "Not measured" if value is None else f"{value / 1024:.1f} KiB"


def gallery(demos):
    cards = []
    for metadata, project, budget in demos:
        identifier = metadata["id"]
        prompt = metadata["prompt"] or metadata["prompt_note"]
        note = f'<p>{html.escape(metadata["prompt_note"])}</p>' if metadata["prompt"] and metadata["prompt_note"] else ""
        cards.append(f'''<article class="demo-card" id="{identifier}">
<a href="{identifier}/"><img class="demo-thumbnail" src="{identifier}/thumbnail.png" alt="{html.escape(metadata['name'], quote=True)} initial page"></a>
<h2>{html.escape(metadata["name"])}</h2>
<p>{html.escape(metadata["description"])}</p>
<dl class="demo-facts">
<dt>Type</dt><dd>{metadata["kind"].capitalize()}</dd>
<dt>Resolution</dt><dd>{project.display.width} × {project.display.height}</dd>
<dt>Flash</dt><dd>{size_text(budget["flash"])}</dd>
<dt>RAM</dt><dd>{size_text(budget["ram"])}</dd>
</dl>
<div class="demo-actions">
<a class="md-button md-button--primary" href="{identifier}/">Play</a>
<a class="md-button" href="{REPOSITORY}/tree/main/examples/{identifier}">Source project</a>
</div>
<details><summary>Creation prompt</summary><p class="demo-prompt">{html.escape(prompt)}</p>{note}</details>
</article>''')
    return "# Browser demos\n\nThese applications and games run locally in your browser on one shared WebAssembly runtime. The flash and RAM figures are measured by the IDE; RAM is a 64-bit simulator estimate and overestimates 32-bit boards.\n\n" + '<div class="demo-grid">\n' + "\n".join(cards) + "\n</div>\n"


def demo_page(metadata, project):
    if metadata["kind"] == "program":
        return program_demo_page(metadata, project)
    title = html.escape(metadata["name"])
    description = html.escape(metadata["description"])
    width, height = project.display.width, project.display.height
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — LVGL MPY Studio</title>
<style>
  :root {{ color-scheme: dark; }}
  html, body {{ margin: 0; min-height: 100%; background: #101318; color: #d8dde6; font: 14px system-ui, sans-serif; }}
  main {{ min-height: 100vh; display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 16px; box-sizing: border-box; }}
  header {{ width: min(100%, {width}px); display: flex; align-items: baseline; justify-content: space-between; gap: 16px; }}
  h1 {{ margin: 0; font-size: 20px; }}
  a {{ color: #79bbff; }}
  canvas {{ display: block; width: min(100%, {width}px); height: auto; max-height: calc(100vh - 130px); aspect-ratio: {width} / {height}; background: #000; touch-action: none; image-rendering: pixelated; }}
  #status {{ min-height: 1.2em; white-space: pre-wrap; text-align: center; }}
  #status.failed {{ color: #ff8a80; }}
  .description {{ max-width: 70ch; margin: 0; text-align: center; color: #aeb8c5; }}
</style>
</head>
<body>
<main>
<header><a href="../">← All demos</a><h1>{title}</h1></header>
<canvas id="canvas" width="{width}" height="{height}" oncontextmenu="event.preventDefault()"></canvas>
<div id="status">Loading…</div>
<p class="description">{description}</p>
</main>
<script type="module" src="../runtime/lms_web.js"></script>
</body>
</html>
'''


def program_demo_page(metadata, program):
    """A program without pages: the keyboard of the page is its serial port."""
    title = html.escape(metadata["name"])
    description = html.escape(metadata["description"])
    width, height = program.display.width, program.display.height
    data = f'data-flash="flash/" data-width="{width}" data-height="{height}" data-board="{html.escape(program.board, quote=True)}" data-entry="{html.escape(metadata["entry"], quote=True)}"'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — LVGL MPY Studio</title>
<style>
  :root {{ color-scheme: dark; }}
  html, body {{ margin: 0; min-height: 100%; background: #101318; color: #d8dde6; font: 14px system-ui, sans-serif; }}
  main {{ min-height: 100vh; display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 16px; box-sizing: border-box; }}
  header {{ width: min(100%, {width}px); display: flex; align-items: baseline; justify-content: space-between; gap: 16px; }}
  h1 {{ margin: 0; font-size: 20px; }}
  a {{ color: #79bbff; }}
  canvas {{ display: block; width: min(100%, {width}px); height: auto; max-height: calc(100vh - 150px); aspect-ratio: {width} / {height}; background: #000; touch-action: none; image-rendering: pixelated; }}
  #status {{ min-height: 1.2em; white-space: pre-wrap; text-align: center; }}
  #status.failed {{ color: #ff8a80; }}
  #typing {{ position: fixed; left: -1000px; top: 0; width: 1px; height: 1px; opacity: 0; }}
  .description {{ max-width: 70ch; margin: 0; text-align: center; color: #aeb8c5; }}
</style>
</head>
<body>
<main {data}>
<header><a href="../">← All demos</a><h1>{title}</h1></header>
<canvas id="canvas" width="{width}" height="{height}" oncontextmenu="event.preventDefault()"></canvas>
<div id="status">Loading…</div>
<textarea id="typing" autocapitalize="off" autocomplete="off" spellcheck="false" aria-label="Keyboard"></textarea>
<p class="description">{description}</p>
</main>
<script type="module" src="../runtime/lms_program.js"></script>
</body>
</html>
'''


def build_documentation(root, output, gallery_markdown):
    import yaml

    with tempfile.TemporaryDirectory(prefix="site-docs-", dir=root / "build") as temporary:
        temporary = Path(temporary)
        docs = temporary / "docs"
        shutil.copytree(root / "docs", docs)
        shutil.copy2(root / "CHANGELOG.md", temporary / "CHANGELOG.md")
        (docs / "demos.md").write_text(gallery_markdown, encoding="utf-8", newline="\n")
        config = yaml.safe_load((root / "mkdocs.yml").read_text(encoding="utf-8"))
        config["docs_dir"] = str(docs)
        config["site_dir"] = str(output)
        config_path = temporary / "mkdocs.yml"
        config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8", newline="\n")
        environment = os.environ.copy()
        environment["NO_MKDOCS_2_WARNING"] = "1"
        subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict", "--config-file", str(config_path)], cwd=root, env=environment, check=True)
    not_found = output / "404.html"
    not_found.write_text(not_found.read_text(encoding="utf-8").replace("/lvgl-mpy-studio/", "./"), encoding="utf-8", newline="\n")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, _tag, attrs):
        for name, value in attrs:
            if name in ("href", "src", "poster") and value:
                self.references.append(value)


def check_internal_links(output):
    problems = []
    for page in output.rglob("*.html"):
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8"))
        for reference in parser.references:
            target = urlsplit(reference)
            if target.scheme or target.netloc or not target.path:
                continue
            if target.path.startswith("/"):
                problems.append(f"{page.relative_to(output)}: absolute path {reference}")
                continue
            resolved = (page.parent / unquote(target.path)).resolve()
            try:
                resolved.relative_to(output.resolve())
            except ValueError:
                problems.append(f"{page.relative_to(output)}: path leaves the site: {reference}")
                continue
            if resolved.is_dir():
                resolved = resolved / "index.html"
            if not resolved.is_file():
                problems.append(f"{page.relative_to(output)}: missing target {reference}")
    if problems:
        raise RuntimeError("Broken internal links:\n" + "\n".join(problems))


def main():
    root = ROOT
    runtime = web_runtime()
    missing = [name for name in RUNTIME_FILES if not (runtime / name).exists()]
    if missing:
        raise SystemExit("Browser runtime not found: run runtime/build_web.sh before building the site")
    demos = load_demos(root)
    if not demos:
        raise SystemExit("No examples/*/demo.json files found")
    output = root / "build/site"
    staging = root / "build/site-demos"
    web_staging = root / "build/site-web"
    for directory in (output, staging, web_staging):
        shutil.rmtree(directory, ignore_errors=True)
    staging.mkdir(parents=True)
    web_staging.mkdir(parents=True)
    built = []
    warnings = []
    try:
        for metadata, project in demos:
            identifier = metadata["id"]
            print(f"Building {identifier}…", flush=True)
            if metadata["kind"] == "program":
                target = staging / "demos" / identifier
                names = copy_program_files(project.entry, target / "flash")
                (target / "index.html").write_text(demo_page(metadata, project), encoding="utf-8", newline="\n")
                program_thumbnail(project, target / "thumbnail.png")
                size = sum((target / "flash" / name).stat().st_size for name in names)
                built.append((metadata, project, {"flash": size, "ram": None}))
                continue
            exported = build_web(project, web_staging)
            target = staging / "demos" / identifier
            target.mkdir(parents=True)
            shutil.copytree(exported / "game", target / "game")
            (target / "index.html").write_text(demo_page(metadata, project), encoding="utf-8", newline="\n")
            page_index = 0 if metadata["page"] is None else [page.name for page in project.pages].index(metadata["page"])
            log = write_thumbnail(project, page_index, target / "thumbnail.png")
            if log.strip():
                warnings.append(f"{identifier}: {log.strip()}")
            budget = measure_budget(project)
            if budget is None:
                raise RuntimeError(f"Could not measure {identifier}")
            built.append((metadata, project, budget))
    finally:
        shutil.rmtree(web_staging, ignore_errors=True)
    runtime_target = staging / "demos/runtime"
    runtime_target.mkdir(parents=True)
    shutil.copy2(web_template() / "lms_web.js", runtime_target)
    copy_program_runtime(runtime_target)  # lms_program.js and system/ for the programs without pages
    for name in RUNTIME_FILES:
        shutil.copy2(runtime / name, runtime_target)
    shutil.copytree(THIRD_PARTY_LICENSES, staging / "demos/licenses")
    build_documentation(root, output, gallery(built))
    shutil.copytree(staging / "demos", output / "demos", dirs_exist_ok=True)
    (output / ".nojekyll").write_bytes(b"")
    check_internal_links(output)
    total = sum(path.stat().st_size for path in output.rglob("*") if path.is_file())
    print(f"Built {len(built)} demos: {', '.join(metadata['id'] for metadata, _project, _budget in built)}")
    print(f"Site: {output} ({total} bytes, {total / 1024 / 1024:.2f} MiB)")
    print("Warnings: " + ("; ".join(warnings) if warnings else "none"))


if __name__ == "__main__":
    main()
