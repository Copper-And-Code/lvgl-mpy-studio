import base64
from pathlib import Path
import time

import serial


class UartError(RuntimeError):
    def __init__(self, code, output=""):
        super().__init__(f"{code}: {output.strip()}" if output else code)
        self.code = code
        self.output = output


PUT_CHUNK = 768  # bytes per command: in base64 they stay under the line buffer of the raw REPL


class UartTransport:
    def __init__(self, port, serial_factory=None, sleep=time.sleep):
        self.port = port
        self._sleep = sleep
        self.serial = (serial_factory or serial.Serial)()
        self.serial.port = port
        self.serial.baudrate = 115200
        self.serial.timeout = 0.1
        self.serial.dtr = True
        self.serial.rts = False
        try:
            self.serial.open()
        except PermissionError as exc:
            raise UartError("device.permissions", str(exc)) from exc
        except serial.SerialException as exc:
            text = str(exc)
            lowered = text.lower()
            code = "device.permissions" if "permission" in lowered or "access denied" in lowered else "device.busy" if "busy" in lowered or "resource" in lowered else "device.absent"
            raise UartError(code, text) from exc
        self._sleep(3)

    def close(self):
        if self.serial.is_open:
            self.serial.close()

    def read(self, size=1):
        try:
            return self.serial.read(size)
        except (OSError, serial.SerialException) as exc:
            raise UartError("device.console", str(exc)) from exc

    @staticmethod
    def _check_cancel(cancel):
        if cancel is not None and cancel.is_set():
            raise UartError("device.cancelled")

    def _read_until(self, marker, timeout, cancel=None):
        data = bytearray()
        deadline = time.monotonic() + timeout
        while marker not in data:
            self._check_cancel(cancel)
            if time.monotonic() >= deadline:
                raise UartError("device.timeout", bytes(data).decode("utf-8", "replace"))
            try:
                chunk = self.serial.read(4096)
            except (OSError, serial.SerialException) as exc:
                raise UartError("device.absent", str(exc)) from exc
            if chunk:
                data.extend(chunk)
        return bytes(data)

    def _enter_raw(self, cancel=None):
        self.serial.write(b"\r\x03\x03\x03")
        self._sleep(0.2)
        self.serial.reset_input_buffer()
        self.serial.write(b"\r\x01")
        self._read_until(b"raw REPL; CTRL-B to exit\r\n>", 5, cancel)

    def execute(self, source, timeout=20, cancel=None):
        try:
            self._enter_raw(cancel)
        except (OSError, serial.SerialException) as exc:
            raise UartError("device.absent", str(exc)) from exc
        return self._run_raw(source, timeout, cancel)

    def _run_raw(self, source, timeout=20, cancel=None):
        """Run source in the raw REPL already open, which stays open for the next command."""
        try:
            payload = source.encode("utf-8")
            for offset in range(0, len(payload), 256):
                self._check_cancel(cancel)
                self.serial.write(payload[offset:offset + 256])
                self._sleep(0.01)
            self.serial.write(b"\x04")
            response = self._read_until(b"\x04>", timeout, cancel)
        except (OSError, serial.SerialException) as exc:
            raise UartError("device.absent", str(exc)) from exc
        if b"OK" not in response:
            raise UartError("device.protocol", response.decode("utf-8", "replace"))
        parts = response.split(b"OK", 1)[1].split(b"\x04")
        if len(parts) < 3:
            raise UartError("device.protocol", response.decode("utf-8", "replace"))
        stdout, stderr = parts[0], parts[1]
        if stderr.strip():
            raise UartError("device.command", stderr.decode("utf-8", "replace"))
        return stdout.decode("utf-8", "replace")

    def soft_reset(self, cancel=None):
        self._enter_raw(cancel)
        self.serial.write(b"\x04")
        self._sleep(0.5)
        try:
            return self.serial.read(self.serial.in_waiting or 1).decode("utf-8", "replace")
        except (OSError, serial.SerialException) as exc:
            raise UartError("device.absent", str(exc)) from exc

    def put(self, local, remote, timeout=30, cancel=None):
        """Write the file in chunks without leaving the raw REPL: entering it for each chunk cost 0.2 s."""
        data = Path(local).read_bytes()
        self.execute(f"import binascii\nf=open({remote!r},'wb')", timeout, cancel)
        try:
            for offset in range(0, len(data), PUT_CHUNK):
                chunk = base64.b64encode(data[offset:offset + PUT_CHUNK]).decode("ascii")
                self._run_raw(f"f.write(binascii.a2b_base64({chunk!r}))", timeout, cancel)
        finally:
            self.execute("f.close()", timeout)  # enters the raw REPL again: this also works after an error half way

    def get(self, remote, local, timeout=30, cancel=None):
        output = self.execute(
            f"import binascii\nf=open({remote!r},'rb')\nwhile True:\n data=f.read(384)\n if not data:break\n print('LVGL_MPY_STUDIO_CHUNK='+binascii.b2a_base64(data,newline=False).decode())\nf.close()\nprint('LVGL_MPY_STUDIO_EOF=1')",
            timeout,
            cancel,
        )
        chunks = []
        complete = False
        for line in output.splitlines():
            if line.startswith("LVGL_MPY_STUDIO_CHUNK="):
                try:
                    chunks.append(base64.b64decode(line.removeprefix("LVGL_MPY_STUDIO_CHUNK="), validate=True))
                except ValueError as exc:
                    raise UartError("device.protocol", output) from exc
            elif line.strip() == "LVGL_MPY_STUDIO_EOF=1":
                complete = True
        if not complete:
            raise UartError("device.protocol", output)
        Path(local).write_bytes(b"".join(chunks))

    def repl(self):
        from serial.tools.miniterm import Miniterm

        self.serial.write(b"\x02")
        terminal = Miniterm(self.serial)
        terminal.exit_character = chr(0x1D)
        terminal.set_rx_encoding("utf-8", "replace")
        terminal.set_tx_encoding("utf-8", "replace")
        terminal.start()
        try:
            terminal.join(True)
        finally:
            terminal.close()
        return 0
