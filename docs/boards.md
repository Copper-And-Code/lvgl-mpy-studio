# MicroPython boards

[Italiano](https://github.com/Copper-And-Code/lvgl-mpy-studio/blob/main/docs/boards.it.md)

### Requirements and first run

The first profile is **Waveshare RP2350-Touch-LCD-4**: 480×480 ST7701S panel, 240×240 RGB565 LVGL UI, GT911 touch and 2× hardware scaling. You need a MicroPython firmware with LVGL and the `display_driver`, `rgbpanel` and `gt911` modules already installed. Copying files to generic MicroPython does not install LVGL or its drivers. The IDE does not flash firmware or modify `boot.py`.

1. Pick the board in the selector next to **Run**. Its profile and the 240×240 resolution are applied to the project as one undoable operation; widget positions, sizes and fonts scale to the new resolution, each axis on its own, and widgets that remain out of bounds are reported. The points of a Line widget do not scale.
2. Press **Run** (F5): a single serial port is used automatically, otherwise you are asked once. The choice is a local per-board preference and is not saved in the project; **Change Port…** updates it. C code is available through **Project → Export C Code…** and cannot be uploaded to a board.
3. The connection opens by itself and stays open for the console and REPL. **Disconnect** in the status bar releases the port for other tools.
4. **Device → Connect** and **Device Information** check firmware, LVGL, memory, buffers, touch and compatibility without starting anything. This check imports `display_driver` and may initialize the display; port enumeration alone does not do it.
5. **Upload Project** copies without running; **Upload and Run** copies and starts. F5 uses the entry chosen in the selector and Shift+F5 stops it.

The **Buzzer** component uses the pin from the `buzzer` key of the board profile: GPIO1 on the Waveshare RP2350 and the speaker through `audio.py` on the ESP32-4848S040. When the profile has no such key, as on the STM32H7, calls do nothing and the IDE reports it. A project whose saved profile predates this key uses the one from the built-in profile with the same id.

The selector choice and the board profile are saved in the project (`runTarget`, `board`) and travel with the file; the serial port does not, because it depends on the computer. **Use as default for new projects**, in the same selector, stores run target, board and resolution in local preferences; **Remove default** restores the initial behavior.

The application is generated in `build/board/<profile-id>/` and installed under `/lms_apps/app_<hash>/`. The hash comes from the `projectId` saved in the project, so projects with the same name do not replace each other; **Save As** creates a new id. Projects created before the id receive one the next time they are saved in the IDE, and their old directory stays on the board. The CLI does not save, so it keeps using the name-based directory for those files. All sources are compiled before reset and transfer; errors are mapped to the original handler and line and do not activate the new version. The probe checks minimum MicroPython/LVGL versions, modules, APIs, resolution and touch against the project profile. Upload uses a staging directory, verifies file sizes and keeps the previous version in `.previous`. It does not delete unrelated directories or user files. After an interrupted upload, retry: staging is recreated and the active version is not replaced until verification succeeds.

The firmware driver owns the framebuffers, touch and LVGL timer. Generated code does not import `lvsim`, allocate another framebuffer or create a second event loop. The application remains active through the driver timer after bootstrap finishes.

### STM32H7_CORE V1.3

The **STM32H7_CORE V1.3 (1024×600)** profile uses the 1024×600 RGB565 LTDC IPS panel, GT911 touch and 1× scaling. It requires MicroPython 1.29 or later, LVGL 9.5 or later, and the `display_driver`, `gt911` and `st_ltdc` modules. Pick the board in the selector next to **Run**; the logical resolution is 1024×600.

The connection uses UART1 through a CH340 adapter at **115200 8N1**, normally `/dev/ttyUSB0` on Linux. Native USB is not used. The IDE sets DTR=1 and RTS=0 before opening the port, waits 3 seconds for boot and keeps the same port open for probing, upload, execution and console. Do not use `mpremote` or another program on the same port: RTS=1 holds the board in reset and every reopening causes a hard reset. **Restart** uses a soft reset without reopening the port. Applications are installed under `/flash/lms_apps/`; autostart only affects `/flash/main.py` and does not modify `display_config.py` or other user files.

### ESP32-4848S040

The **ESP32-4848S040 (480×480)** profile uses native 480×480 RGB565 resolution, GT911 touch and 1× scaling. It requires MicroPython 1.29 or later, LVGL 9.5 or later, and the `display_driver` and `gt911` modules. Panel support is integrated into the display driver: a separate `rgbpanel` module is not required. The USB serial connection uses `mpremote`, normally on `/dev/ttyUSB0`; applications are installed under `/lms_apps/` without modifying `boot.py` or `main.py`.

### Live editing

While an application started from the IDE is running, **Device → Live Editing** sends design changes to the board about half a second after the last edit, with no restart. It rebuilds all pages off screen, shows the page open in the designer, and then deletes the old ones. Python module state survives, but widget state such as a typed text or a slider position returns to the design values. Code, Buzzer or Timer changes are not sent: the status bar asks you to press F5.

### Console, Stop and autostart

The **Device Console** incrementally shows output and tracebacks produced after bootstrap and accepts REPL commands while the session is ready. The continuous reader pauses during commands that need the port, ensuring a single serial owner. **Cancel operation** interrupts a blocked command. **Stop** in the Device menu always targets the board, even when the simulator is selected; F5 and Shift+F5 use the selected destination. Stop removes application modules from the import cache and calls `display_driver.stop()`. The last image may remain visible because scan-out continues after the timer stops. Every new run performs a soft reset to avoid stale timers and modules.

**Install Autostart…** is separate from F5. It replaces `/main.py` with a recognizable launcher and backs up an existing `main.py` under `~/.config/lvgl-mpy-studio/autostart-backups/<board-id>/<app>/<transaction>/` (or `XDG_CONFIG_HOME`). Identity uses `machine.unique_id()`, not the USB port. Every transaction verifies launcher and backup hashes; manual edits, invalid manifests or missing backups block restoration without overwriting files. **Remove Autostart…** only acts on the current transaction launcher for the selected app.

If an autostart application becomes unresponsive, use the safe/recovery mode provided by the board firmware, or power it down, open another MicroPython tool and remove only the recognizable `/main.py` launcher. Do not format the filesystem: application files remain under `/lms_apps/`.

### CLI

```bash
lvgl-mpy-studio --language en device list
lvgl-mpy-studio --language en device info --port /dev/ttyACM0
lvgl-mpy-studio device upload project.json --port /dev/ttyACM0
lvgl-mpy-studio device run project.json --port /dev/ttyACM0
lvgl-mpy-studio device stop --port /dev/ttyACM0
lvgl-mpy-studio device reset --port /dev/ttyACM0
lvgl-mpy-studio device repl --port /dev/ttyACM0
lvgl-mpy-studio device autostart-install project.json --port /dev/ttyACM0
lvgl-mpy-studio device autostart-remove project.json --port /dev/ttyACM0
```

Subcommand and option names are always in English. If a project has no embedded profile, add `--board-profile <id>`. `upload` and `run` accept `--output <directory>`. Projects contain a portable profile copy and can be opened without the corresponding local catalog entry.

Ctrl+C returns status 130 for non-interactive commands. In the interactive REPL it interrupts the remote program; leave the REPL with Ctrl+] as documented by `mpremote`. The port is released when the command exits. Do not open the IDE, a REPL and another serial monitor on the same port at once.

### Language and profiles

**Settings → Language** switches Italian/English immediately and saves the preference without changing the project. **Device → Manage Board Profiles…** provides create, edit, duplicate, delete and restore operations. Changes persist only with **Apply**. Editing a built-in profile creates a user customization; deleting it hides it. Projects retain their portable copy and are updated only through **Update Project Profile**, with undo.

### Fonts

A profile can list the Montserrat sizes of its firmware in `fonts`, for example `"fonts": [14, 16, 24, 32, 40]`. Text asked in a size the board lacks is drawn in the nearest one, in the designer preview, in the simulator and on the board alike. A profile without the list is taken to have 14, 16 and 24; a project without a board uses the five sizes of the simulator, 14, 16, 24, 32 and 40.

On every upload the IDE reads the fonts the firmware really has. If they differ from the profile, the code is generated for the fonts of the board and a notice says so: add the list to the profile to see the same text in the preview. **Device → Device Information** shows the list as `fonts`.

Common errors:

- `device.busy`: close REPLs, serial monitors or other IDEs using the port.
- `device.permissions`: check the serial port permissions and your distribution's rules; do not copy files as root.
- `device.absent`: reconnect the board and select the port again after a reset or USB disconnection.
- `device.timeout`: check that the board responds; interrupt any blocked program before retrying.
- `device.prerequisites`: install a firmware with the required modules, or fix the profile resolution or touch setting.
- `device.resolution`: set the project to the profile's logical size; 240×240 for this Waveshare, not 480×480.
- `device.transfer.incomplete`: repeat the upload and check free space and the USB connection.
- `device.autostart.not-owned`: `/main.py` is not a recognizable IDE launcher, so it is not removed.

Raw MicroPython tracebacks are preserved in the console.
