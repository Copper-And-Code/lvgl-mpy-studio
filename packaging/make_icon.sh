#!/usr/bin/env bash
# Rebuilds lvgl_mpy_studio/icon.ico from the SVG. Run it after changing the drawing.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
QT_QPA_PLATFORM=offscreen "${PYTHON:-$ROOT/.venv/bin/python}" - "$ROOT/packaging/lvgl-mpy-studio.svg" "$WORK" <<'PY'
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QImage, QPainter
from PySide6.QtSvg import QSvgRenderer

app = QGuiApplication([])
renderer = QSvgRenderer(sys.argv[1])
for size in (16, 24, 32, 48, 64, 128, 256):
    image = QImage(size, size, QImage.Format_ARGB32)
    image.fill(Qt.transparent)
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()
    image.save(f"{sys.argv[2]}/{size:03}.png")
PY
convert "$WORK"/*.png "$ROOT/lvgl_mpy_studio/icon.ico"
