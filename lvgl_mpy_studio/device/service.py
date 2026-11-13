import codecs
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time

from lvgl_mpy_studio.core.boards import compatible, portable_profile, profile_fonts, validate_profile
from lvgl_mpy_studio.core.i18n import tr
from lvgl_mpy_studio.gen.board_gen import BoardSyntaxError, generate_board, precompile_board
from lvgl_mpy_studio.platform import CREATE_NO_WINDOW, IS_WINDOWS
from lvgl_mpy_studio.gen.fonts import font_memory_warning
from lvgl_mpy_studio.gen.live import LIVE_OK
from lvgl_mpy_studio.gen.project_gen import legacy_data
from .autostart import AUTOSTART_MARKER_V2, OLD_AUTOSTART_MARKERS, AutostartMixin  # noqa: F401  (imported from here by callers)
from .common import DeviceError, marked_json
from .uart import UartError, UartTransport

CONSOLE_CHUNK = 64  # bytes written at a time to the console: a long paste must not overflow the board's buffer


class SerialConsole:
    """The serial port of a board reached through mpremote, opened as mpremote opens it.

    mpremote's own SerialTransport knows the quirks of the USB adapters (the CP210x on Windows, the
    lines that reset an ESP32), so the console takes and gives back the port exactly as mpremote does."""

    def __init__(self, port):
        from mpremote.transport import TransportError
        from mpremote.transport_serial import SerialTransport

        try:
            self._transport = SerialTransport(port, baudrate=115200, timeout=0.1)
        except TransportError as exc:
            raise OSError(str(exc)) from exc
        self.serial = self._transport.serial

    def read_some(self):
        return self.serial.read(self.serial.in_waiting or 1)

    def write(self, data):
        self.serial.write(data)

    def close(self):
        self._transport.close()


APP_ROOT = "/lms_apps"



RAW_REPL_FAILED = "could not enter raw repl"


def break_in(port, sleep=time.sleep):
    """Repeated Ctrl+C with a pause: they also interrupt what the first one does not stop.

    mpremote sends only one before the raw REPL. A shell in the firmware, like that of some
    ESP32 boards ("Ctrl-C again leaves the shell"), needs two; at the >>> prompt the extra ones
    do nothing. Opening the port this way does not reset the board, as mpremote does not.
    """
    import serial
    try:
        with serial.Serial(port, 115200, timeout=0.2) as link:
            for key in (b"\r\x03", b"\x03", b"\x03"):
                link.write(key)
                link.flush()
                sleep(0.3)
            link.read(65536)
    except (OSError, ValueError, serial.SerialException):
        pass  # the port does not open: mpremote will say so when it retries


default_interrupt = break_in  # tests replace it: they must never write to a real port


def mpremote_command():
    override = os.environ.get("LVGL_MPY_STUDIO_MPREMOTE")
    if override:
        return [override]
    if getattr(sys, "frozen", False):
        return [sys.executable, "_mpremote"]
    return [sys.executable, "-m", "mpremote"]


def _version(value):
    if isinstance(value, (list, tuple)):
        value = ".".join(str(part) for part in value)
    match = re.match(r"^v?(\d+)\.(\d+)(?:\.(\d+))?", str(value or "").strip())
    return tuple(int(part or 0) for part in match.groups()) if match else None


PORT_ERRORS = (
    ("device.permissions", ("permission denied", "access is denied", "access denied")),
    ("device.busy", ("device or resource busy", "resource busy", "port is already in use", "could not exclusively lock")),
    ("device.absent", ("no device found", "failed to access", "no such file or directory", "could not open port", "filenotfounderror")),
)


def _port_error(output):
    """The error code, from the phrases mpremote and pyserial use about the port.

    A traceback of the code on the board passes through here: it must not become "port busy" only
    because it contains a word such as resource or not found.
    """
    if "Traceback (most recent call last)" in output and "mpremote" not in output:
        return "device.command"
    lowered = output.lower()
    return next((code for code, phrases in PORT_ERRORS if any(phrase in lowered for phrase in phrases)), "device.command")


def _remove_tree_script(path):
    return f"""def remove_tree(path):
 try:
  for name in os.listdir(path):
   child=path+'/'+name
   try:
    os.listdir(child);remove_tree(child)
   except OSError:
    os.remove(child)
  os.rmdir(path)
 except OSError:
  pass
remove_tree({path!r})"""


def stop_script(app_root):
    """Stop the app and forget its modules, user modules included: they all live under app_root."""
    return (
        "import sys\n"
        "for name in ('app_main','app_events','ui'):\n sys.modules.pop(name,None)\n"
        f"for name,module in list(sys.modules.items()):\n if str(getattr(module,'__file__','')).startswith({app_root + '/'!r}):\n  sys.modules.pop(name,None)\n"
        "import display_driver\ndisplay_driver.stop()\nprint('LVGL_MPY_STUDIO_STOPPED')"
    )


class DeviceSession(AutostartMixin):
    def __init__(self, runner=None, process_factory=None, uart_factory=None, interrupt=None, console_factory=None):
        self._break_in = interrupt or default_interrupt
        self.port = None
        self.state = "disconnected"
        self.profile = None
        self.device_id = None
        self._runner = runner or self._run_process
        self._custom_runner = runner is not None
        self._process_factory = process_factory or subprocess.Popen
        self._custom_process_factory = process_factory is not None
        self._uart_factory = uart_factory or UartTransport
        self._uart = None
        self._console_factory = console_factory or SerialConsole
        self._console = None
        self._console_thread = None
        self._lock = threading.RLock()
        self._operation = threading.RLock()

    def _run_process(self, command, timeout, cancel=None):
        try:
            process = self._process_factory(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", creationflags=CREATE_NO_WINDOW)
            started = time.monotonic()
            while True:
                try:
                    stdout, stderr = process.communicate(timeout=0.1)
                    break
                except subprocess.TimeoutExpired:
                    if cancel is not None and cancel.is_set():
                        if IS_WINDOWS:
                            process.terminate()
                        else:
                            process.send_signal(signal.SIGINT)
                        try:
                            process.communicate(timeout=0.5)
                        except subprocess.TimeoutExpired:
                            process.kill()
                            process.communicate()
                        raise DeviceError("device.cancelled")
                    if time.monotonic() - started >= timeout:
                        process.kill()
                        stdout, stderr = process.communicate()
                        raise DeviceError("device.timeout", (stdout or "") + (stderr or ""))
        except DeviceError:
            raise
        except PermissionError as exc:
            raise DeviceError("device.permissions", str(exc)) from exc
        except FileNotFoundError as exc:
            raise DeviceError("device.absent", str(exc)) from exc
        output = (stdout or "") + (stderr or "")
        if process.returncode:
            raise DeviceError(_port_error(output), output)
        return output

    def _execute_uart(self, args, timeout, cancel):
        try:
            if "exec" in args:
                return self._uart.execute(args[args.index("exec") + 1], timeout, cancel)
            if "soft-reset" in args:
                return self._uart.soft_reset(cancel)
            if args[-4:-2] == ["fs", "cp"]:
                source, destination = args[-2:]
                if source.startswith(":"):
                    return self._uart.get(source[1:], destination, timeout, cancel)
                if destination.startswith(":"):
                    return self._uart.put(source, destination[1:], timeout, cancel)
            raise DeviceError("device.command", " ".join(args))
        except UartError as exc:
            raise DeviceError(exc.code, exc.output) from exc

    def _execute(self, args, timeout=20, cancel=None):
        self.stop_console()
        self._check_cancel(cancel)
        with self._lock:
            if self._uart is not None:
                output = self._execute_uart(args, timeout, cancel)
            else:
                output = self._run_mpremote(args, timeout, cancel)
        self._check_cancel(cancel)
        return output

    def _put(self, source, destination, cancel=None, written=None):
        """Copy a file to the board. Over the serial adapter `written` follows the bytes; mpremote says nothing until the end."""
        if self._uart is None or written is None:
            return self._execute(["connect", self.port, "fs", "cp", str(source), f":{destination}"], timeout=30)
        self.stop_console()
        with self._lock:
            try:
                return self._uart.put(str(source), destination, 30, cancel, written)
            except UartError as exc:
                raise DeviceError(exc.code, exc.output) from exc

    def _exec(self, source, timeout=20, cancel=None):
        """Run MicroPython source on the board without resetting it, and return what it printed."""
        options = {"cancel": cancel} if cancel is not None else {}
        return self._execute(["connect", self.port, "resume", "exec", source], timeout=timeout, **options)

    def _run_mpremote(self, args, timeout, cancel):
        def run():
            if self._custom_runner:
                return self._runner(mpremote_command() + args, timeout)
            return self._runner(mpremote_command() + args, timeout, cancel)
        try:
            return run()
        except DeviceError as exc:
            if RAW_REPL_FAILED not in (exc.output or "") or "connect" not in args:
                raise
            # Something on the board took the first Ctrl+C without stopping: insist once only.
            self._break_in(args[args.index("connect") + 1])
            self._check_cancel(cancel)
            return run()

    def start_console(self, on_output, interactive=False, on_closed=None):
        """Read what the board prints and pass it to on_output, until stop_console.

        interactive also leaves the raw REPL that the IDE's commands use, so that what is typed
        reaches the board's prompt or the running program."""
        self._require()
        self.stop_console()
        if self._uart is not None:
            console = self._uart
            if interactive:
                try:
                    console.leave_raw()
                except UartError as exc:
                    raise DeviceError(exc.code, exc.output) from exc
        else:
            try:
                console = self._console_factory(self.port)
            except (OSError, PermissionError) as exc:
                raise DeviceError("device.console", str(exc)) from exc
        self._console = console

        def read_output():
            decoder = codecs.getincrementaldecoder("utf-8")("replace")
            while self._console is console:
                try:
                    data = console.read_some() if hasattr(console, "read_some") else console.read(1)
                except (OSError, UartError, ValueError):
                    break
                if not data:  # nothing within the timeout: the port goes away only with an error
                    continue
                text = decoder.decode(data)
                if text:
                    on_output(text)
            remaining = decoder.decode(b"", final=True)
            if remaining:
                on_output(remaining)
            if self._console is console:  # the port went away, nobody stopped it
                self._console = None
                if console is not self._uart:
                    try:
                        console.close()
                    except (OSError, ValueError):
                        pass
                if on_closed:
                    on_closed()

        self._console_thread = threading.Thread(target=read_output, name="lvgl-mpy-studio-console", daemon=True)
        self._console_thread.start()
        return True

    @property
    def console_live(self):
        return self._console is not None

    def write(self, data):
        """Send typed bytes to the board's console, a few at a time."""
        console = self._console
        if console is None:
            raise DeviceError("device.console", tr("The console is not active."))
        try:
            for offset in range(0, len(data), CONSOLE_CHUNK):
                if offset:
                    time.sleep(0.005)
                console.write(data[offset:offset + CONSOLE_CHUNK])
        except (OSError, UartError, ValueError) as exc:
            raise DeviceError("device.console", str(exc)) from exc

    def stop_console(self):
        console, self._console = self._console, None
        if console is not None and console is not self._uart:
            try:
                console.close()
            except (OSError, ValueError):
                pass
        thread = self._console_thread
        self._console_thread = None
        if thread and thread is not threading.current_thread():
            thread.join(timeout=1)

    def list_ports(self):
        output = self._execute(["devs"], timeout=5)
        ports = []
        for line in output.splitlines():
            match = re.match(r"^(\S+)\s+(\S+)\s+(\S+)\s*(.*)$", line.strip())
            if match:
                ports.append({"port": match.group(1), "id": match.group(2), "usb": match.group(3), "description": match.group(4)})
        return ports

    def connect(self, port, profile):
        if not port:
            raise DeviceError("device.port.required")
        validate_profile(profile)
        with self._operation:
            self.state = "connecting"
            self.port = port
            self.device_id = None
            self.profile = portable_profile(profile)
            try:
                if self.profile["adapter"] == "stm32h7_uart":
                    self._uart = self._uart_factory(port)
                else:
                    # On connecting, a firmware shell is almost always there: interrupting it at once
                    # avoids the 10 s mpremote waits before giving up.
                    self._break_in(port)
                info = self.info()
            except Exception as exc:
                if self._uart is not None:
                    self._uart.close()
                    self._uart = None
                self.port = None
                self.profile = None
                self.device_id = None
                self.state = "error"
                if isinstance(exc, UartError):
                    raise DeviceError(exc.code, exc.output) from exc
                raise
            self.state = "ready"
            return info

    def disconnect(self):
        self.stop_console()
        with self._operation:
            if self._uart is not None:
                self._uart.close()
                self._uart = None
            self.port = None
            self.profile = None
            self.device_id = None
            self.state = "disconnected"

    def _require(self):
        if not self.port:
            raise DeviceError("device.not.connected")

    def info(self):
        with self._operation:
            return self._info()

    def _info(self, profile=None):
        self._require()
        active_profile = profile or self.profile
        required_modules = active_profile.get("firmware", {}).get("modules", []) if active_profile else ["lvgl", "rgbpanel", "gt911"]
        modules = list(dict.fromkeys(name for name in required_modules if name != "display_driver"))
        probe = r'''import sys,json,gc,os
r={'implementation':sys.implementation.name,'implementationVersion':list(sys.implementation.version),'version':sys.version,'modules':{},'apis':{},'memoryFreeBefore':gc.mem_free()}
r['mpy']=getattr(sys.implementation,'_mpy',None)
try:
 import machine,binascii
 r['deviceId']=binascii.hexlify(machine.unique_id()).decode()
except Exception:pass
for name in @MODULES@:
 try:
  module=__import__(name);r['modules'][name]=True
  if name=='lvgl':
   r['apis']['lvgl']={n:hasattr(module,n) for n in ('obj','screen_load','EVENT','timer_handler')}
   r['binfont']=hasattr(module,'binfont_create_from_buffer')
   r['fonts']=[s for s in (8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48) if hasattr(module,'font_montserrat_%d'%s)]
   try:
    values=module.version_info()
    if not values:values=(module.version_major(),module.version_minor(),module.version_patch())
    r['lvglVersion']='.'.join(str(v) for v in values)
   except Exception as e:r.setdefault('errors',{})['lvglVersion']=str(e)
 except Exception as e:
  r['modules'][name]=False;r.setdefault('errors',{})[name]=str(e)
try:
 import display_driver
 r['modules']['display_driver']=True;r['width']=display_driver.WIDTH;r['height']=display_driver.HEIGHT;r['buffers']=display_driver.BUFFERS;r['touch']=display_driver.indev is not None
 r['apis']['display_driver']={n:hasattr(display_driver,n) for n in ('start','stop','WIDTH','HEIGHT','BUFFERS','indev')}
except Exception as e:
 r['modules']['display_driver']=False;r.setdefault('errors',{})['display_driver']=str(e)
gc.collect();r['memoryFree']=gc.mem_free()
try:
 s=os.statvfs(@ROOT@);r['filesystemFree']=s[0]*s[3]
except Exception as e:r['filesystemError']=str(e)
print('LVGL_MPY_STUDIO_INFO='+json.dumps(r))'''.replace("@MODULES@", repr(modules)).replace("@ROOT@", repr(self._app_root(self.profile or {}).rsplit("/", 1)[0] or "/"))  # the filesystem apps are written to
        output = self._exec(probe, 25)
        info = marked_json(output, "LVGL_MPY_STUDIO_INFO")
        profile = copy.deepcopy(profile or self.profile)
        required = profile.get("firmware", {}).get("modules", []) if profile else []
        missing = [name for name in required if not info.get("modules", {}).get(name)]
        info["missingModules"] = missing
        if info.get("deviceId"):
            self.device_id = str(info["deviceId"]).lower()
        if profile:
            missing_apis = [f"{module}.{name}" for module, names in info.get("apis", {}).items() for name, present in names.items() if not present]
            for module, names in (("lvgl", ("obj", "screen_load", "EVENT")), ("display_driver", ("start", "stop", "WIDTH", "HEIGHT", "BUFFERS", "indev"))):
                if info.get("modules", {}).get(module) and module not in info.get("apis", {}):
                    missing_apis.extend(f"{module}.{name}" for name in names)
            firmware = profile["firmware"]
            micro_actual, micro_required = _version(info.get("implementationVersion")), _version(firmware.get("microPython"))
            lvgl_actual, lvgl_required = _version(info.get("lvglVersion")), _version(firmware.get("lvgl"))
            size_ok = (info.get("width"), info.get("height")) == (profile["logicalWidth"], profile["logicalHeight"])
            touch_ok = not profile.get("config", {}).get("touch") or info.get("touch") is True
            reasons = list(missing) + missing_apis
            incomplete = []
            if info.get("implementation") != "micropython":
                reasons.append("implementation")
            if micro_actual is None or lvgl_actual is None:
                incomplete.extend(name for name, value in (("microPython", micro_actual), ("lvgl", lvgl_actual)) if value is None)
            else:
                if micro_required and micro_actual < micro_required:  # a profile without a minimum accepts any version
                    reasons.append("microPython")
                if lvgl_required and lvgl_actual < lvgl_required:
                    reasons.append("lvgl")
            if not size_ok:
                reasons.append("resolution")
            if not touch_ok:
                reasons.append("touch")
            info.update(missingApis=missing_apis, missingRequirements=reasons + incomplete, compatibilityStatus="incomplete" if incomplete and not reasons else "incompatible" if reasons else "compatible", compatible=not reasons and not incomplete, sizeCompatible=size_ok, touchCompatible=touch_ok, microPythonCompatible=micro_actual is not None and (not micro_required or micro_actual >= micro_required), lvglCompatible=lvgl_actual is not None and (not lvgl_required or lvgl_actual >= lvgl_required))
        return info

    @staticmethod
    def _hashed_app_id(identity, profile):
        digest = hashlib.sha256(f"{identity}\0{profile['id']}".encode("utf-8")).hexdigest()[:12]
        return f"app_{digest}"

    def _app_id(self, project, profile):
        return self._hashed_app_id(project.projectId or project.projectName, profile)

    @staticmethod
    def _app_root(profile):
        return profile.get("config", {}).get("appRoot", APP_ROOT)

    @staticmethod
    def _main_path(profile):
        return profile.get("config", {}).get("mainPath", "/main.py")

    def _reset(self):
        self._require()
        output = self._execute(["connect", self.port, "soft-reset"], timeout=15)
        time.sleep(0.5)
        return output

    @staticmethod
    def _check_cancel(cancel):
        if cancel is not None and cancel.is_set():
            raise DeviceError("device.cancelled")

    def upload(self, project, output_dir=None, run=False, progress=None, cancel=None):
        self._require()
        with self._operation:
            if self.state == "transferring":
                raise DeviceError("device.session.busy")
            project = copy.deepcopy(project)
            if project.board is None:
                raise DeviceError("device.profile.required")
            profile = portable_profile(project.board)
            validate_profile(profile)
            if not compatible(project, profile):
                raise DeviceError("device.resolution", f"{profile['logicalWidth']}x{profile['logicalHeight']}")
            temporary = tempfile.TemporaryDirectory(prefix="lvgl-mpy-studio-board-")
            try:
                output = Path(output_dir) if output_dir else Path(temporary.name)
                try:
                    generated = generate_board(project, profile, output)
                except BoardSyntaxError as exc:
                    raise DeviceError("device.syntax", json.dumps(exc.errors, ensure_ascii=False), exc.errors) from exc
                info = self._info(profile)
                if not info.get("compatible"):
                    raise DeviceError("device.prerequisites", ",".join(info.get("missingRequirements") or [info.get("compatibilityStatus", "unknown")]))
                self._check_cancel(cancel)
                fonts = info.get("fonts")
                if fonts and sorted(fonts) != profile_fonts(profile):
                    # The firmware decides: text in a size it lacks would stop the app at start-up.
                    generated = generate_board(project, profile, output, fonts=sorted(fonts))
                    generated["warnings"].append(tr("The board has Montserrat fonts {board}, the profile lists {profile}: the code uses those of the board, so text can differ from the preview. Set them in the board profile.", board=", ".join(str(size) for size in sorted(fonts)), profile=", ".join(str(size) for size in profile_fonts(profile))))
                if (project.assets or {}).get("fonts") and info.get("binfont") is False:
                    generated["warnings"].append(tr("This firmware cannot load fonts at run time: the fonts of the project are replaced by the built-in font."))
                generated = precompile_board(generated, output, info.get("mpy"))
                self.state = "transferring"
                app_id = self._app_id(project, profile)
                app_root = self._app_root(profile)
                current = f"{app_root}/{app_id}"
                staging = f"{current}.uploading"
                backup = f"{current}.previous"
                self._check_cancel(cancel)
                self._reset()
                if (project.assets or {}).get("fonts") and info.get("binfont") is not False:
                    # Asked again now: before the reset the application already on the board held its own
                    # memory. The probe loads the display driver, as the application will, so what it
                    # reports is what the application finds; the second reset gives a clean start.
                    warning = font_memory_warning(legacy_data(project), self._info(profile).get("memoryFree"))
                    self._reset()
                    if warning:
                        generated["warnings"].append(warning)
                prepare = f"import os\ntry:\n os.mkdir({app_root!r})\nexcept OSError:\n pass\n{_remove_tree_script(staging)}"
                self._exec(prepare, 20)
                self._exec(f"import os\nos.mkdir({staging!r})", 20)
                checks = {name: (output / name).stat().st_size for name in generated["files"]}
                total, sent = sum(checks.values()), 0
                for name, size in checks.items():
                    self._check_cancel(cancel)
                    if progress:  # sent bytes, all bytes, the file being written and its size
                        progress(sent, total, name, size)
                    self._put(output / name, f"{staging}/{name}", cancel, (lambda done, sent=sent, name=name, size=size: progress(sent + done, total, name, size)) if progress else None)
                    sent += size
                if progress:
                    progress(total, total, "", 0)
                script = "import os,json\nr={}\nfor n in %r:\n try:r[n]=os.stat('%s/'+n)[6]\n except OSError:r[n]=-1\nprint('LVGL_MPY_STUDIO_SIZES='+json.dumps(r))" % (list(checks), staging)
                result = self._exec(script, 20)
                actual = marked_json(result, "LVGL_MPY_STUDIO_SIZES", missing={})
                if actual != checks:
                    raise DeviceError("device.transfer.incomplete", json.dumps({"expected": checks, "actual": actual}))
                self._check_cancel(cancel)
                activate = f"""import os
{_remove_tree_script(backup)}
try:
 os.rename({current!r},{backup!r})
except OSError:
 pass
try:
 os.rename({staging!r},{current!r})
except OSError:
 try:
  os.rename({backup!r},{current!r})
 except OSError:
  pass
 raise"""
                self._exec(activate, 20)
                self.state = "ready"
                if run:
                    try:
                        return self.run(project, output_dir=output, _uploaded=True, _generated=generated)
                    except DeviceError as exc:
                        exc.warnings = generated["warnings"]  # they often say why it did not start
                        raise
                return {"appPath": current, **generated}
            except Exception:  # an unexpected error too must leave the session usable
                self.state = "error"
                raise
            finally:
                temporary.cleanup()

    def run(self, project=None, output_dir=None, _uploaded=False, progress=None, cancel=None, _generated=None):
        self._require()
        if not _uploaded:
            return self.upload(project, output_dir, run=True, progress=progress, cancel=cancel)
        if project is None or project.board is None:
            raise DeviceError("device.profile.required")
        profile = portable_profile(project.board)
        current = f"{self._app_root(profile)}/{self._app_id(project, profile)}"
        self.state = "running"
        try:
            output = self._exec(f"import sys\nif {current!r} not in sys.path:\n sys.path.insert(0,{current!r})\nimport app_main", 30)
            self.state = "ready"
            return {"output": output, "appPath": current, "active": True, **(_generated or {})}
        except DeviceError:
            self.state = "error"
            raise

    def stop(self):
        self._require()
        with self._operation:
            self.state = "stopping"
            output = self._exec(stop_script(self._app_root(self.profile or {})), 20)
            if "LVGL_MPY_STUDIO_STOPPED" not in output:
                raise DeviceError("device.protocol", output)
            self.state = "ready"
            return output

    def restart(self):
        with self._operation:
            output = self._reset()
            self.state = "ready"
            return output

    def evaluate(self, source, cancel=None):
        self._require()
        if not source.strip():
            return ""
        with self._operation:
            return self._exec(source, 30, cancel)

    def live_update(self, script, cancel=None):
        """Update the UI of the running app. The app and its Python state stay alive."""
        self._require()
        with self._operation:
            if self._uart is not None or self._custom_runner:
                output = self._exec(script, 30, cancel)
            else:
                # On Windows a command line cannot hold a large UI.
                with tempfile.TemporaryDirectory(prefix="lvgl-mpy-studio-live-") as temporary:
                    path = Path(temporary) / "live.py"
                    path.write_text(script, encoding="utf-8", newline="\n")
                    output = self._execute(["connect", self.port, "resume", "run", str(path)], timeout=30, cancel=cancel)
        if LIVE_OK not in output:
            raise DeviceError("device.live", output)
        return output

    def repl(self):
        self._require()
        with self._operation:
            try:
                if self._uart is not None:
                    return self._uart.repl()
                return subprocess.call(mpremote_command() + ["connect", self.port, "repl"])
            except KeyboardInterrupt:
                return 130
            except PermissionError as exc:
                raise DeviceError("device.permissions", str(exc)) from exc
            except FileNotFoundError as exc:
                raise DeviceError("device.absent", str(exc)) from exc
