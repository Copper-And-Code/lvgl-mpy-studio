"""Autostart: the app starts when the board powers up, and the main.py that was there can be restored.

Every installation is a transaction kept on the PC, under the hardware id of the board: the
launcher written, the main.py it replaced and their hashes. Nothing on the board is removed or
restored unless it is still exactly what the IDE wrote.
"""

import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from uuid import uuid4

from lvgl_mpy_studio.core.boards import portable_profile
from lvgl_mpy_studio.platform import config_dir
from .common import DeviceError, marked, marked_json, write_json_atomic

AUTOSTART_MARKER_V2 = "# LMS_AUTOSTART_V2"
# Launchers written up to 0.4, still recognised on a board so that they are not taken for the user's main.py.
OLD_AUTOSTART_MARKERS = ("# LVGL_IDE_AUTOSTART_V1", "# LVGL_IDE_AUTOSTART_V2")


class AutostartMixin:
    """The autostart operations of a DeviceSession, which provides the connection and the app paths."""

    def _device_identity(self):
        if self.device_id:
            return self.device_id
        probe = """import machine,binascii,json
try:
 print('LVGL_MPY_STUDIO_IDENTITY='+binascii.hexlify(machine.unique_id()).decode())
except Exception:
 print('LVGL_MPY_STUDIO_IDENTITY=')"""
        output = self._exec(probe, 15)
        identity = (marked(output, "LVGL_MPY_STUDIO_IDENTITY") or "").strip()
        if not identity or not re.fullmatch(r"[0-9A-Fa-f]+", identity):
            raise DeviceError("device.identity.unavailable")
        self.device_id = identity.lower()
        return self.device_id

    def _autostart_root(self):
        identity = self._device_identity()
        return config_dir() / "autostart-backups" / identity

    @staticmethod
    def _launcher(current, transaction):
        return f"{AUTOSTART_MARKER_V2}\n# transaction: {transaction}\nimport sys\nif {current!r} not in sys.path:\n sys.path.insert(0, {current!r})\nimport app_main\n"

    @staticmethod
    def _read_json(path, code):
        try:
            value = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise DeviceError(code, str(exc)) from exc
        if not isinstance(value, dict):
            raise DeviceError(code, str(path))
        return value

    def _current_transaction(self, root):
        pointer_path = root / "current.json"
        if not pointer_path.exists():
            return None
        pointer = self._read_json(pointer_path, "device.autostart.manifest")
        app_id, transaction = pointer.get("appId"), pointer.get("transaction")
        if not isinstance(app_id, str) or not re.fullmatch(r"app_[0-9a-f]{12}", app_id) or not isinstance(transaction, str) or not re.fullmatch(r"[0-9a-f]{32}", transaction):
            raise DeviceError("device.autostart.manifest")
        directory = root / app_id / transaction
        manifest = self._read_json(directory / "manifest.json", "device.autostart.manifest")
        if manifest.get("schemaVersion") != 2 or manifest.get("deviceId") != root.name or manifest.get("appId") != app_id or manifest.get("transaction") != transaction or not isinstance(manifest.get("appPath"), str) or not isinstance(manifest.get("hadMain"), bool):
            raise DeviceError("device.autostart.manifest")
        launcher = self._launcher(manifest["appPath"], transaction)
        if manifest.get("launcherSha256") != hashlib.sha256(launcher.encode("utf-8")).hexdigest():
            raise DeviceError("device.autostart.manifest")
        return directory, manifest, launcher

    def _read_remote_text(self, path):
        output = self._exec(f"import json\ntry:\n print('LVGL_MPY_STUDIO_FILE='+json.dumps(open({path!r}).read()))\nexcept OSError:\n print('LVGL_MPY_STUDIO_FILE=null')", 15)
        return marked_json(output, "LVGL_MPY_STUDIO_FILE")

    def _write_remote_text(self, path, content):
        with tempfile.TemporaryDirectory(prefix="lvgl-mpy-studio-launcher-") as directory:
            local = Path(directory) / Path(path).name
            local.write_text(content, encoding="utf-8")
            self._execute(["connect", self.port, "fs", "cp", str(local), f":{path}"], timeout=20)
        if self._read_remote_text(path) != content:
            raise DeviceError("device.autostart.verify")

    def install_autostart(self, project):
        self._require()
        with self._operation:
            if project.board is None:
                raise DeviceError("device.profile.required")
            profile = portable_profile(project.board)
            app_id = self._app_id(project, profile)
            current = f"{self._app_root(profile)}/{app_id}"
            main_path = self._main_path(profile)
            if not self._remote_exists(f"{current}/app_main.py"):
                raise DeviceError("device.autostart.no-app")
            root = self._autostart_root()
            remote = self._read_remote_text(main_path)
            previous = self._current_transaction(root)
            transaction = uuid4().hex
            directory = root / app_id / transaction
            directory.mkdir(parents=True, exist_ok=False)
            try:
                if previous:
                    _old_directory, old_manifest, old_launcher = previous
                    if remote != old_launcher:
                        raise DeviceError("device.autostart.not-owned")
                    had_main = old_manifest["hadMain"]
                    previous_transaction = old_manifest["transaction"]
                    if had_main:
                        old_backup = _old_directory / "main.py"
                        if not old_backup.is_file() or hashlib.sha256(old_backup.read_bytes()).hexdigest() != old_manifest.get("backupSha256"):
                            raise DeviceError("device.autostart.backup")
                        shutil.copyfile(old_backup, directory / "main.py")
                elif isinstance(remote, str) and remote.startswith((AUTOSTART_MARKER_V2, *OLD_AUTOSTART_MARKERS)):
                    raise DeviceError("device.autostart.ambiguous")
                else:
                    had_main = remote is not None
                    previous_transaction = None
                    if had_main:
                        self._execute(["connect", self.port, "fs", "cp", f":{main_path}", str(directory / "main.py")], timeout=15)
                        if not (directory / "main.py").is_file() or (directory / "main.py").read_text(encoding="utf-8") != remote:
                            raise DeviceError("device.autostart.backup")
                launcher = self._launcher(current, transaction)
                manifest = {"schemaVersion": 2, "deviceId": root.name, "appId": app_id, "appPath": current, "transaction": transaction, "previousTransaction": previous_transaction, "hadMain": had_main, "launcherSha256": hashlib.sha256(launcher.encode("utf-8")).hexdigest()}
                if had_main:
                    manifest["backupSha256"] = hashlib.sha256((directory / "main.py").read_bytes()).hexdigest()
                write_json_atomic(directory / "manifest.json", manifest)
                self._write_remote_text(main_path, launcher)
                write_json_atomic(root / "current.json", {"schemaVersion": 2, "appId": app_id, "transaction": transaction})
            except Exception:
                shutil.rmtree(directory, ignore_errors=True)  # a failed transaction does not leave its folder
                raise
            return {"backup": str(directory), "appPath": current, "transaction": transaction}

    def _remote_exists(self, path):
        output = self._exec(f"import os\ntry:\n os.stat({path!r});print('YES')\nexcept OSError:\n print('NO')", 15)
        return any(line.strip() == "YES" for line in output.splitlines())

    def remove_autostart(self, project):
        self._require()
        with self._operation:
            if project.board is None:
                raise DeviceError("device.profile.required")
            profile = portable_profile(project.board)
            main_path = self._main_path(profile)
            root = self._autostart_root()
            current_transaction = self._current_transaction(root)
            if not current_transaction:
                raise DeviceError("device.autostart.manifest")
            directory, manifest, launcher = current_transaction
            # An autostart installed before the id has the project name in its path.
            owned = {f"{self._app_root(profile)}/{app}" for app in (self._app_id(project, profile), self._hashed_app_id(project.projectName, profile))}
            if manifest["appPath"] not in owned or self._read_remote_text(main_path) != launcher:
                raise DeviceError("device.autostart.not-owned")
            if manifest["hadMain"]:
                backup = directory / "main.py"
                if not backup.is_file():
                    raise DeviceError("device.autostart.backup")
                content = backup.read_bytes()
                if hashlib.sha256(content).hexdigest() != manifest.get("backupSha256"):
                    raise DeviceError("device.autostart.backup")
                try:
                    text = content.decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise DeviceError("device.autostart.backup", str(exc)) from exc
                self._write_remote_text(main_path, text)
            else:
                self._exec(f"import os\nos.remove({main_path!r})", 15)
                if self._read_remote_text(main_path) is not None:
                    raise DeviceError("device.autostart.verify")
            try:
                (root / "current.json").unlink()
            except OSError as exc:
                raise DeviceError("device.autostart.manifest", str(exc)) from exc
            return True
