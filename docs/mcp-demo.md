# From a prompt to an app

This is a complete session of an AI agent building an app with LVGL MPY Studio through the [MCP server](mcp.md), starting from one sentence. It is recorded so that it can be replayed: the calls are in [`examples/weather/mcp-session.json`](https://github.com/Copper-And-Code/lvgl-mpy-studio/blob/main/examples/weather/mcp-session.json) and the result is [`examples/weather/project.json`](https://github.com/Copper-And-Code/lvgl-mpy-studio/blob/main/examples/weather/project.json). A test replays the session at every run of the suite and checks that it still builds the same app.

## The prompt

> Build a weather station for the ESP32-4848S040: the current temperature of a city, a five-day forecast, a button to change city, and a settings page to switch between Celsius and Fahrenheit. Check that it works before you finish.

## What the agent did

24 tool calls, in four steps. The agent read about 18,000 characters of answers in total.

| Step | Calls | What happened |
|---|---|---|
| **Look around** | `list_boards`, `create_project`, `list_widget_types` (names, then five types), `project_info` | The board is 480×480 and its profile listed fonts 14, 16 and 24 when the session was recorded, so the large temperature is asked at 24. The profile now lists 32 and 40 too, read from a real board. |
| **Draw** | `add_widgets` (23 widgets in one call), `add_page`, `add_widgets`, `render_page`, `validate` | Two pages. The five forecast cards are panels with two labels each, added with their parent in the same call. The agent looked at the rendering of the page. |
| **Write the code** | `create_module`, `set_module_code`, `set_handler` × 6 | A `forecast` module with the data and the unit conversion, a `refresh()` function in the shared code, and one short handler per event. |
| **Check** | `simulate`, `save_scenario`, `visual_test` × 2, `measure`, `project_info` | The simulator played taps on the buttons and the switch, with assertions on the texts. The same steps were saved as a scenario with reference images. |

The app worked at the first run of `simulate`: 24 °C for Catania, Milan after a tap, 53 °F after switching units on the settings page, and the "updated N s ago" line counting on the simulated clock.

`forecast.fetch()` returns fixed data, so the app runs the same in the simulator and in the tests. On the board, with Wi-Fi, it is the one function to replace with a call to a weather service.

## What the session changed in the server

Playing the agent showed four places where it had to guess or pay more than needed. They are fixed, and the recorded session uses the fixed tools:

- **Answers were indented JSON.** They are compact now: the whole session costs the agent about half the characters.
- **`list_widget_types` returned every type at once**, 34,000 characters. It now takes `names_only` and `types`, and also returns the default values of each type.
- **`list_boards` did not say which font sizes a board has.** It does now.
- **Text that cannot be drawn as asked was silent.** A font size the board lacks, or a character outside the built-in font such as `…`, is now reported in the warnings of the call that sets it and by `validate`.

## Replaying it

```bash
QT_QPA_PLATFORM=offscreen python -m pytest tests/test_mcp_demo.py
```

To open the result, load `examples/weather/project.json` in the IDE and press F5, or run:

```bash
lvgl-mpy-studio run examples/weather/project.json
lvgl-mpy-studio test examples/weather/project.json
```
