#!/usr/bin/env python3
"""Write the names the code editor completes after lv. and ui.<widget>., from the pinned binding.

The binding describes its whole API in generated/api.json (about 5 MB). The editor needs only the
names of constants, functions and objects, and the methods and parent of each object, so the IDE
ships this short extract. Run it again after changing the binding pin:

    python runtime/update_completion.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".reference" / "lvgl-bindings" / "generated" / "api.json"
TARGET = ROOT / "lvgl_mpy_studio" / "gen" / "completion.json"


def extract(api):
    return {
        "api_hash": api["api_hash"],
        "constants": sorted(item["python_name"] for item in api["constants"]),
        "functions": sorted({item["python_name"] for item in api["functions"]}),
        "objects": {item["python_name"]: {"parent": item.get("parent"), "methods": item.get("methods") or []} for item in api["objects"]},
    }


if __name__ == "__main__":
    data = extract(json.loads(SOURCE.read_text(encoding="utf-8")))
    TARGET.write_text(json.dumps(data, separators=(",", ":"), sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"{TARGET.relative_to(ROOT)}: {TARGET.stat().st_size} bytes")
