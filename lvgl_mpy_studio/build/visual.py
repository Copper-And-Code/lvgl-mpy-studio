"""Visual tests: each page, drawn by the real runtime, against a reference PNG."""

from dataclasses import dataclass
import json
from pathlib import Path
import re
import struct
import zlib

from .preview import render_with_log

SIGNATURE = b"\x89PNG\r\n\x1a\n"
PASSED, FAILED, MISSING, UPDATED, ERROR = "passed", "failed", "missing", "updated", "error"


class PngError(ValueError):
    pass


@dataclass
class PageResult:
    page: str
    status: str
    different: int = 0
    box: tuple[int, int, int, int] | None = None
    message: str = ""


def rgb565_to_rgb(pixels):
    result = bytearray(len(pixels) // 2 * 3)
    for index in range(len(pixels) // 2):
        low, high = pixels[index * 2], pixels[index * 2 + 1]
        value = high << 8 | low
        red, green, blue = value >> 11, value >> 5 & 0x3F, value & 0x1F
        target = index * 3
        result[target] = red << 3 | red >> 2
        result[target + 1] = green << 2 | green >> 4
        result[target + 2] = blue << 3 | blue >> 2
    return bytes(result)


def _chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))


def encode_png(rgb, width, height):
    rows = b"".join(b"\0" + rgb[row * width * 3:(row + 1) * width * 3] for row in range(height))
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return SIGNATURE + _chunk(b"IHDR", header) + _chunk(b"IDAT", zlib.compress(rows, 9)) + _chunk(b"IEND", b"")


def write_png(path, rgb, width, height):
    Path(path).write_bytes(encode_png(rgb, width, height))


def read_png(path):
    """Read the PNGs written by write_png: 8-bit RGB without filters."""
    data = Path(path).read_bytes()
    if not data.startswith(SIGNATURE):
        raise PngError(f"{path}: not a PNG file")
    offset, width, height, compressed = len(SIGNATURE), 0, 0, b""
    while offset + 8 <= len(data):
        length, kind = struct.unpack(">I4s", data[offset:offset + 8])
        body = data[offset + 8:offset + 8 + length]
        offset += 12 + length
        if kind == b"IHDR":
            width, height, depth, color, _compression, _filter, interlace = struct.unpack(">IIBBBBB", body)
            if (depth, color, interlace) != (8, 2, 0):
                raise PngError(f"{path}: only 8-bit RGB images written by lvgl-mpy-studio are supported")
        elif kind == b"IDAT":
            compressed += body
    try:
        rows = zlib.decompress(compressed)
    except zlib.error as exc:
        raise PngError(f"{path}: {exc}") from exc
    stride = width * 3 + 1
    if not width or len(rows) != stride * height or any(rows[row * stride] for row in range(height)):
        raise PngError(f"{path}: only images written by lvgl-mpy-studio are supported")
    return b"".join(rows[row * stride + 1:(row + 1) * stride] for row in range(height)), width, height


def compare(expected, actual, width, height):
    """Return how many pixels differ, their bounding box and the map of the differences."""
    if expected == actual:
        return 0, None, None
    different, left, top, right, bottom = 0, width, height, -1, -1
    image = bytearray(len(actual))
    for row in range(height):
        for column in range(width):
            start = (row * width + column) * 3
            if expected[start:start + 3] != actual[start:start + 3]:
                different += 1
                left, top = min(left, column), min(top, row)
                right, bottom = max(right, column), max(bottom, row)
                image[start] = 255
            else:  # the rest of the page stays recognisable, but faded
                for channel in range(3):
                    image[start + channel] = 160 + actual[start + channel] // 3
    return different, (left, top, right, bottom), bytes(image)


def baseline_dir(project_path, project):
    return Path(project_path).parent / "visual" / f"{project.display.width}x{project.display.height}"


def _file_name(page):
    return re.sub(r"[^A-Za-z0-9_-]", "_", page.name)


def _render(project, index, design_only):
    pixels, log = render_with_log(project, index, design_only=design_only)
    if pixels is None:
        lines = [line for line in log.splitlines() if line.strip()]
        return None, lines[-1] if lines else "no frame from the runtime"
    return rgb565_to_rgb(pixels), None


def _check_page(project, index, directory, update, threshold, design_only):
    page = project.pages[index]
    actual, problem = _render(project, index, design_only)
    if actual is None:
        return PageResult(page.name, ERROR, message=problem)
    if update:
        again, problem = _render(project, index, design_only)
        if again != actual:  # an unstable reference would fail every later run
            return PageResult(page.name, ERROR, message=problem or "the page changes between two runs: baseline not written")
    return _check_image(page.name, directory / _file_name(page), actual, project, update, threshold)


def _check_image(name, base, actual, project, update, threshold):
    """Compare an image with its reference, or write the reference with update."""
    width, height = project.display.width, project.display.height
    directory = base.parent
    baseline, actual_file, diff_file = base.with_name(base.name + ".png"), base.with_name(base.name + ".actual.png"), base.with_name(base.name + ".diff.png")
    if update:
        directory.mkdir(parents=True, exist_ok=True)
        write_png(baseline, actual, width, height)
        actual_file.unlink(missing_ok=True)
        diff_file.unlink(missing_ok=True)
        return PageResult(name, UPDATED)
    if not baseline.exists():
        return PageResult(name, MISSING, message=str(baseline))
    try:
        expected, expected_width, expected_height = read_png(baseline)
    except PngError as exc:
        return PageResult(name, ERROR, message=str(exc))
    if (expected_width, expected_height) != (width, height):
        return PageResult(name, ERROR, message=f"baseline is {expected_width}x{expected_height}, page is {width}x{height}")
    different, box, image = compare(expected, actual, width, height)
    if different <= threshold:
        actual_file.unlink(missing_ok=True)
        diff_file.unlink(missing_ok=True)
        return PageResult(name, PASSED, different, box)
    write_png(actual_file, actual, width, height)
    write_png(diff_file, image, width, height)
    return PageResult(name, FAILED, different, box, str(diff_file))


SCENARIOS_FILE = "scenarios.json"


def load_scenarios(directory):
    """The scenarios of one resolution: touches depend on coordinates, so they sit next to the references."""
    path = Path(directory) / SCENARIOS_FILE
    if not path.exists():
        return []
    try:
        scenarios = json.loads(path.read_text(encoding="utf-8")).get("scenarios", [])
    except (OSError, ValueError, AttributeError) as exc:
        raise ValueError(f"visual.scenarios-invalid:{path}: {exc}") from exc
    if not isinstance(scenarios, list):
        raise ValueError(f"visual.scenarios-invalid:{path}: scenarios must be a list")
    names = [item.get("name") for item in scenarios if isinstance(item, dict)]
    if len(names) != len(scenarios) or not all(isinstance(name, str) and name for name in names) or len({_safe(name) for name in names}) != len(names):
        raise ValueError(f"visual.scenarios-invalid:{path}: every scenario needs a name that stays unique as a file name")
    return scenarios


def save_scenario(directory, scenario):
    """Add or replace a scenario by name."""
    path = Path(directory) / SCENARIOS_FILE
    others = [item for item in load_scenarios(directory) if item["name"] != scenario["name"]]
    if any(_safe(item["name"]) == _safe(scenario["name"]) for item in others):
        raise ValueError(f"visual.scenario-name-clash:{scenario['name']}: another scenario uses the same file names")
    scenarios = others + [scenario]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"scenarios": scenarios}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def _play(project, scenario):
    from lvgl_mpy_studio.sim.script import play
    from lvgl_mpy_studio.sim.session import SimulationError
    names = [page.name for page in project.pages]
    page = scenario.get("page") or names[0]
    if page not in names:
        raise ValueError(f"page {page!r} not found")
    try:
        result = play(project, names.index(page), scenario.get("steps", []), "virtual", scenario.get("seed", 0))
    except (SimulationError, TypeError, KeyError) as exc:
        raise ValueError(str(exc)) from exc
    if not result["passed"]:
        if result["failure"]:
            reason = result["failure"]["reason"]
        elif result["traceback"]:
            reason = [line for line in result["console"].splitlines() if line.strip()][-1]
        else:
            reason = "the app stopped" if not result["running"] else "an eval step failed"
        raise ValueError(str(reason).strip().splitlines()[-1] if str(reason).strip() else "failed")
    return [(label, rgb565_to_rgb(pixels)) for label, pixels in result["images"]]


def _check_scenario(project, scenario, directory, update, threshold):
    name = scenario["name"]
    try:
        images = _play(project, scenario)
        if update and _play(project, scenario) != images:  # with the simulated clock two runs must match
            return [PageResult(name, ERROR, message="the scenario changes between two runs: baseline not written")]
    except ValueError as exc:
        return [PageResult(name, ERROR, message=str(exc))]
    labels = [label for label, _image in images]
    if len(set(labels)) != len(labels):
        return [PageResult(name, ERROR, message="two screenshots have the same label")]
    return [_check_image(f"{name}: {label}", directory / f"{_safe(name)}@{_safe(label)}", image, project, update, threshold) for label, image in images]


def _safe(text):
    return re.sub(r"[^A-Za-z0-9_-]", "_", str(text))


def run_visual_tests(project, directory, update=False, threshold=0, pages=None, design_only=False, scenarios=None):
    """Pages and scenarios. Choosing only pages or only scenarios tests only those."""
    if threshold < 0:
        raise ValueError("visual.threshold-negative")
    directory = Path(directory)
    names = {page.name for page in project.pages}
    unknown = sorted(set(pages or ()) - names)
    if unknown:
        raise ValueError("visual.page-not-found:" + ",".join(unknown))
    if scenarios and design_only:
        raise ValueError("visual.scenario-design-only")  # a scenario without code would prove nothing
    available = load_scenarios(directory)
    missing = sorted(set(scenarios or ()) - {item["name"] for item in available})
    if missing:
        raise ValueError("visual.scenario-not-found:" + ",".join(missing))
    results = []
    if pages or not scenarios:
        results += [
            _check_page(project, index, directory, update, threshold, design_only)
            for index, page in enumerate(project.pages)
            if not pages or page.name in pages
        ]
    if (scenarios or not pages) and not design_only:  # a scenario without code would make no sense
        for scenario in available:
            if not scenarios or scenario["name"] in scenarios:
                results += _check_scenario(project, scenario, directory, update, threshold)
    return results
