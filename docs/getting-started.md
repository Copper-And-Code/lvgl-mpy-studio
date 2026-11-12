# Getting started

## Install from the sources

On Linux you need Python 3.11 or later, a C compiler, CMake, `pkg-config`, SDL2 development headers, and `xvfb` for headless simulator windows. The first runtime build also downloads the pinned SDL2 sources.

```bash
git clone https://github.com/Copper-And-Code/lvgl-mpy-studio.git
cd lvgl-mpy-studio
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
./runtime/build.sh
.venv/bin/lvgl-mpy-studio
```

The full requirements and the Windows and packaging instructions are in [Building and testing](https://github.com/Copper-And-Code/lvgl-mpy-studio/blob/main/docs/development.md) on GitHub.

## Open a complete project

Choose **File → Open**, select `examples/eim-01/project.json`, and press **F5**. The simulator runs the industrial monitor with the real LVGL runtime, including touch input and sound.

## Create your first project

1. Choose **File → New**.
2. Drag a label and a button from the toolbox onto the page.
3. Double-click the button and add its Python event handler.
4. Press **F5** to try the page in the simulator.
5. Save the project as a single `.json` file.

The [first-project walkthrough](manual.md#2-your-first-project-in-five-minutes) includes the handler for a tap counter. Continue with the [user manual](manual.md), the [board guide](boards.md), or [Publishing on the web](publish-web.md).
