"""What the parts of the device package share: the error type and the lines the board prints for the IDE."""

import json
import os
from pathlib import Path
from uuid import uuid4


class DeviceError(RuntimeError):
    def __init__(self, code, output="", errors=None):
        super().__init__(f"{code}: {output.strip()}" if output else code)
        self.code = code
        self.output = output
        self.errors = errors or []
        self.warnings = []  # found before the failure, e.g. fonts larger than the free memory


def write_json_atomic(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    try:
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


REQUIRED = object()


def marked(output, name):
    """The text after NAME= on the line the board printed for us, or None."""
    prefix = name + "="
    return next((line.removeprefix(prefix) for line in output.splitlines() if line.startswith(prefix)), None)


def marked_json(output, name, missing=REQUIRED):
    """The JSON value the board printed after NAME=; without the line, missing or a protocol error."""
    text = marked(output, name)
    if text is None:
        if missing is REQUIRED:
            raise DeviceError("device.protocol", output)
        return missing
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise DeviceError("device.protocol", output) from exc
