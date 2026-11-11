# Pinned targets

- MicroPython: `v1.29.0`, `unix` port on Linux x86-64 and `windows` port on Windows x86-64.
- PyDevices/lvgl-micropython: `58d18ce`.
- SDL2 MinGW: `2.30.9`, official package `SDL2-devel-2.30.9-mingw.tar.gz`, SHA-256 `b188d165dc4a0372042bff3d0c18e9bb90772581e92a7b8b47b521b47714f75c`.
- LVGL bindings: `7740c2fae0daa10992f5f8fe54acf670a70e2d3b`, LVGL 9.5.0.
- PySide6: `6.12.0`, found with `python3 -m pip index versions PySide6`.
- pyserial: `3.5`, for the STM32H7 UART transport.
- Default display: 800×480, RGB565.

## `lv_conf.h` verified at the pin

Source: `lvgl-bindings/lv_conf.h` at the bindings commit, copied unchanged to `runtime/lv_conf.h`.

- `LV_COLOR_DEPTH = 16`; IDE framebuffer in RGB565.
- Allocator: `LV_USE_STDLIB_MALLOC = LV_STDLIB_MICROPYTHON_OVERRIDE` in the MicroPython build (`LV_STDLIB_CLIB` outside MicroPython/CircuitPython); builtin strings.
- Render mode: not set by the configuration file; the Python driver uses `DISPLAY_RENDER_MODE.DIRECT` with a full-screen buffer.
- Enabled Montserrat fonts: 14, 16, 24, 32, 40. Default font: Montserrat 14.
- `LV_USE_FLOAT = 1`, `LV_USE_OS = LV_OS_NONE`.
- Logging: `LV_USE_LOG = 0`; in the inactive block the default level is `WARN`, `LV_LOG_PRINTF = 0`.
- Null and malloc asserts enabled; style, mem integrity and obj asserts disabled.
- `LV_USE_DRAW_SDL = 0`: SDL belongs to `lvsim_io`, not to the LVGL renderer.
