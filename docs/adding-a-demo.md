# Adding a demo

## 1. Create and check the project

Create `examples/<id>/project.json` by hand, in the IDE, or through the MCP server. Use a lower-case folder name made of letters, numbers, and hyphens; it becomes the public URL.

The demo must be original: do not copy the name, characters, graphics, or levels of an existing game. All visible text, widget names, and comments must be in English. Open the project in the simulator and check that it starts without errors or unexpected warnings.

## 2. Describe the demo

Create `examples/<id>/demo.json` next to the project:

```json
{
  "id": "example",
  "name": "Example",
  "description": "One or two sentences that say what the visitor can do.",
  "kind": "game",
  "page": null,
  "prompt": "The original prompt, if an AI agent created this demo.",
  "prompt_note": null,
  "order": 60
}
```

- `id` must match the folder name.
- `kind` is `game`, `application` or `program`.
- `page` is the page used for the thumbnail, or `null` for the initial page.
- `order` is a unique integer that controls the gallery order.
- If no prompt exists, set `prompt` to `null` and explain that in `prompt_note`. Never reconstruct or invent one.
- If the demo was changed after the prompt produced it, keep the prompt and say what changed, and who changed it, in `prompt_note`.

### A program without pages

A program such as `examples/shell` has no `project.json`. Its `demo.json` has `"kind": "program"`, `"page": null`, and one more field, `"entry"`, the `.py` file to run, in the same folder. The whole folder is copied into the flash of the program, in the browser's memory. It runs as the STM32H7_CORE V1.3, 1024×600; the keyboard of the page is its serial port. The thumbnail is the screen of the Linux simulator after the program has started and `ls` was typed, and the gallery shows the size of the files as Flash and no RAM figure.

In the browser there are no timer interrupts and no native code: LVGL is served only while the program waits for a key, sleeps or polls, and `@micropython.viper` or `@micropython.native` functions do not compile. `examples/shell/ansiterm.py` shows the way out: its viper functions are compiled from a string inside `try`, and `framebuf` does the same drawing where they fail.

**When an agent creates a demo from a prompt, save that prompt in `demo.json` at the same time.** Preserving the connection between prompt and result is the purpose of the gallery.

## 3. Build and try the site

Install the site and development dependencies, then build:

```bash
.venv/bin/pip install -e '.[site,dev]'
.venv/bin/python tools/build_site.py
.venv/bin/python -m pytest -q tests/test_site.py
```

The build requires the simulator and the browser runtime. If the latter is missing, build it separately with `runtime/build_web.sh`; the site build never downloads or builds it automatically.

Serve `build/site/` below a subpath such as `/lvgl-mpy-studio/` and try the gallery and the new demo at desktop and phone widths. The browser tests check this layout, every demo, one interaction, internal links, and the absence of external network requests. They need the Playwright Chromium browser.

## 4. Ask before publishing

Show the result to the project owner. Ask separately for any commit, for `tools/publish_site.sh`, for every push of `gh-pages`, and for enabling or changing GitHub Pages. The build and test commands do not send anything or change Git history.
