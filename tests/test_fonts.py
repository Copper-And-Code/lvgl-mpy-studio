"""Fonts of a project: converted to LVGL's format with Qt and drawn by the real runtime.

The reference is LVGL itself: its built-in Montserrat was made by lv_font_conv from the same
TrueType file, so a font converted here must give the same glyphs.
"""

import json
import re
import subprocess
from pathlib import Path

import pytest

from lvgl_mpy_studio import mcp_server
from lvgl_mpy_studio.build.preview import render_with_log
from lvgl_mpy_studio.core import assets
from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.fontconv import convert, rasterise
from lvgl_mpy_studio.gen.binfont import write_binfont
from lvgl_mpy_studio.gen.board_gen import generate_board
from lvgl_mpy_studio.gen.gen_c import generate_c
from lvgl_mpy_studio.gen.project_gen import design_warnings, generate_project
from lvgl_mpy_studio.platform import runtime_environment, runtime_path

LVGL = Path(__file__).parents[1] / ".reference" / "lvgl-bindings" / "lvgl"
MONTSERRAT = LVGL / "scripts" / "built_in_font" / "Montserrat-Medium.ttf"
ASCII = "".join(chr(code) for code in range(32, 127))

pytestmark = pytest.mark.skipif(not MONTSERRAT.exists(), reason="LVGL sources not available")
needs_runtime = pytest.mark.skipif(not runtime_path().exists(), reason="runtime not built")


def builtin(size):
    """Glyphs of LVGL's built-in Montserrat: {code: (advance, width, height, ofs_x, ofs_y, pixels)}."""
    source = (LVGL / "src" / "font" / f"lv_font_montserrat_{size}.c").read_text()
    records = [tuple(int(value) for value in match) for match in re.findall(r"\{\.bitmap_index = (\d+), \.adv_w = (\d+), \.box_w = (\d+), \.box_h = (\d+), \.ofs_x = (-?\d+), \.ofs_y = (-?\d+)\}", source)]
    start = source.index("glyph_bitmap[] = {")
    data = bytes(int(value, 16) for value in re.findall(r"0x([0-9a-fA-F]{1,2})", re.sub(r"/\*.*?\*/", "", source[start:source.index("};", start)])))
    glyphs = {}
    for code in range(32, 127):
        index, advance, width, height, ofs_x, ofs_y = records[code - 31]
        nibbles = [value for byte in data[index:index + (width * height + 1) // 2] for value in (byte >> 4, byte & 15)]
        glyphs[code] = (advance, width, height, ofs_x, ofs_y, bytes(nibbles[:width * height]))
    return glyphs


@pytest.mark.parametrize("size", (14, 24, 40))
def test_glyphs_match_the_font_lvgl_ships(size):
    font, missing = rasterise(MONTSERRAT.read_bytes(), size, ASCII)
    assert not missing
    reference = builtin(size)
    pixels = different = 0
    for glyph in font["glyphs"]:
        advance, width, height, ofs_x, ofs_y, expected = reference[glyph["code"]]
        assert (glyph["advance"], glyph["width"], glyph["height"], glyph["ofs_x"], glyph["ofs_y"]) == (advance, width, height, ofs_x, ofs_y), chr(glyph["code"])
        assert all(abs(mine - theirs) <= 1 for mine, theirs in zip(glyph["pixels"], expected)), chr(glyph["code"])
        pixels += len(expected)
        different += sum(mine != theirs for mine, theirs in zip(glyph["pixels"], expected))
    assert different < pixels / 500  # one level of sixteen, on fewer than two pixels in a thousand


def builtin_kerning(size):
    """Kerning of LVGL's built-in Montserrat among ASCII characters: {(code, next code): 1/16 pixel}."""
    source = (LVGL / "src" / "font" / f"lv_font_montserrat_{size}.c").read_text()

    def array(name):
        return [int(value) for value in re.findall(r"-?\d+", re.sub(r"/\*.*?\*/", "", re.search(name + r"\[\] =\s*\{(.*?)\};", source, re.S).group(1), flags=re.S))]

    left, right, values = array("kern_left_class_mapping"), array("kern_right_class_mapping"), array("kern_class_values")
    columns = max(right)
    pairs = {(a, b): values[(left[a - 31] - 1) * columns + right[b - 31] - 1] for a in range(32, 127) for b in range(32, 127) if left[a - 31] and right[b - 31]}
    return {pair: value for pair, value in pairs.items() if value}


def run_in_runtime(script, folder):
    done = subprocess.run([str(runtime_path()), "-c", script], cwd=folder, env=runtime_environment(LVSIM_HEADLESS="1"), capture_output=True, text=True, timeout=120)
    assert done.returncode == 0, done.stdout + done.stderr
    return done.stdout


@pytest.mark.parametrize("size", (14, 24, 40))
def test_kerning_matches_the_font_lvgl_ships(size):
    """Every pair LVGL's font kerns has the same value here. This converter reads the font through
    HarfBuzz and finds some more pairs, which lv_font_conv left out."""
    font, _missing = rasterise(MONTSERRAT.read_bytes(), size, ASCII)
    reference = builtin_kerning(size)
    assert len(reference) > 2000
    assert {pair: font["kerning"].get(pair) for pair in reference} == reference
    assert len(font["kerning"]) - len(reference) < 400


@needs_runtime
def test_the_runtime_spaces_pairs_like_the_builtin_font(tmp_path):
    (tmp_path / "font.bin").write_bytes(convert(MONTSERRAT.read_bytes(), 24, ASCII)["output"])
    output = run_in_runtime("""
import lvgl as lv
lv.init()
data = open("font.bin", "rb").read()
mine = lv.binfont_create_from_buffer(data, len(data))
print([(a, b) for a in range(32, 127) for b in range(32, 127) if mine.get_glyph_width(a, b) != lv.font_montserrat_24.get_glyph_width(a, b)])
""", tmp_path)
    different = {tuple(pair) for pair in json.loads(output.replace("(", "[").replace(")", "]"))}
    reference = builtin_kerning(24)
    assert not different & set(reference)  # the only pairs spaced differently are those the built-in font does not kern
    assert reference[ord("A"), ord("V")] < 0 and len(different) < 400


@needs_runtime
def test_the_runtime_reads_kerning_stored_as_a_list_of_pairs(tmp_path):
    """300 glyphs that all kern differently do not fit in classes; values above 127 need a coarser scale."""
    glyphs = [{"code": 0x100 + index, "advance": 1600, "width": 1, "height": 1, "ofs_x": 0, "ofs_y": 0, "pixels": b"\x0f"} for index in range(300)]
    kerning = {(0x100 + index, 0x100 + (index * 7 + 1) % 300): (index % 40 - 20) * 16 or 16 for index in range(300)}
    kerning[0x100, 0x101] = -400
    data = write_binfont({"size": 10, "glyphs": glyphs, "kerning": kerning})
    assert data[data.index(b"kern") + 4] == 0  # the list of pairs
    (tmp_path / "font.bin").write_bytes(data)
    output = run_in_runtime("""
import lvgl as lv
lv.init()
data = open("font.bin", "rb").read()
font = lv.binfont_create_from_buffer(data, len(data))
print([font.get_glyph_width(0x100 + i, 0x100 + (i * 7 + 1) % 300) for i in range(300)], font.get_glyph_width(0x100, 0x105))
""", tmp_path)
    widths, plain = output.rsplit("]", 1)
    widths = json.loads(widths + "]")
    assert int(plain) == 100
    assert all(abs(width - (100 + kerning[0x100 + index, 0x100 + (index * 7 + 1) % 300] / 16)) <= 0.6 for index, width in enumerate(widths))


def test_a_font_without_kerning_has_no_kern_table():
    glyphs = [{"code": 65, "advance": 160, "width": 1, "height": 1, "ofs_x": 0, "ofs_y": 0, "pixels": b"\x0f"}]
    assert b"kern" not in write_binfont({"size": 10, "glyphs": glyphs}) and write_binfont({"size": 10, "glyphs": glyphs})[12] == 3  # the count of tables


def test_the_converter_reports_what_it_cannot_do():
    assert "error" in convert(b"not a font", 24, "A")
    result = convert(MONTSERRAT.read_bytes(), 24, "A中")
    assert result["missing"] == "中" and result["output"][4:8] == b"head"


def with_font(size=24, text="0123456789"):
    project = Project()
    project.set_display_size(320, 120)
    name = assets.add_font(project, "Montserrat Medium.ttf", MONTSERRAT.read_bytes())
    project.add_widget(project.pages[0], "panel", {"x": 0, "y": 0, "width": 320, "height": 120, "bgColor": "#000000", "radius": 0, "borderWidth": 0}, "back")
    project.add_widget(project.pages[0], "label", {"x": 10, "y": 20, "width": 300, "height": 60, "text": text, "textColor": "#FFFFFF", "fontSize": size, "font": name, "textAlign": "LV_TEXT_ALIGN_LEFT"}, "text")
    return project, name


@needs_runtime
def test_the_runtime_draws_text_with_the_project_font_like_the_builtin_one():
    for char in ("8", "y", "@", "AVATAR"):
        project, _name = with_font(text=char)
        custom, log = render_with_log(project, 0, design_only=False)
        assert custom, log
        project.find_widget("text").props["font"] = ""
        plain, log = render_with_log(project, 0, design_only=False)
        assert plain, log
        rows = lambda frame: [frame[row * 640:(row + 1) * 640] for row in range(120)]
        lit = sum(1 for index in range(0, len(plain), 2) if plain[index:index + 2] != b"\0\0")
        best = min(sum(a != b for a, b in zip(rows(plain)[2:-2], rows(custom)[2 + shift:118 + shift])) for shift in (-1, 0, 1))
        assert lit > 30 and best <= 2, char  # at most the line height differs, by one pixel


@needs_runtime
def test_a_size_the_board_lacks_is_drawn_with_the_project_font(tmp_path):
    profile = next(item for item in builtin_profiles() if item["id"] == "esp32_4848s040_480")
    project, name = with_font(size=31)
    project.board = profile
    project.resize(480, 480, "keep")
    assert design_warnings(project) == []  # no "drawn at 24": the project font has every size
    generated = generate_board(project, profile, tmp_path / "board")
    source = (tmp_path / "board" / "ui.py").read_text()
    assert "binfont_create_from_buffer" in source and "font_montserrat_medium_31" in source and generated["warnings"] == []
    generate_project(project, tmp_path / "sim")
    done = subprocess.run([str(runtime_path()), "-c", "import lvgl as lv; lv.init(); import ui; print(ui.font_montserrat_medium_31.get_line_height())"], cwd=tmp_path / "sim", env=runtime_environment(LVSIM_HEADLESS="1"), capture_output=True, text=True, timeout=30)
    assert done.stdout.strip().isdigit() and 28 <= int(done.stdout) <= 40, done.stdout + done.stderr


def test_fonts_are_listed_removed_and_reported(tmp_path):
    project, name = with_font()
    assert name == "Montserrat_Medium.ttf" and assets.fonts(project)[0]["name"] == name
    with pytest.raises(assets.AssetError, match="TrueType"):
        assets.add_font(project, "x.ttf", b"PNG\0not a font")
    saved = tmp_path / "project.json"
    project.save(saved)
    assert assets.fonts(Project.load(saved)) == assets.fonts(project)
    project.find_widget("text").props["text"] = "中"
    assert any("no glyph for" in warning and "U+4E2D" in warning for warning in design_warnings(project))
    assert assets.remove_font(project, name) == ["text"]
    assert any("is not in the project" in warning for warning in project.text_warnings())


def test_choosing_a_font_file_in_the_properties_adds_it(qtbot):
    from lvgl_mpy_studio.ui.document import ProjectDocument
    from lvgl_mpy_studio.ui.properties.panel import PropertiesPanel
    from test_images import find_item

    project = Project()
    project.add_widget(project.pages[0], "label", {"x": 0, "y": 0, "width": 100, "height": 30, "text": "Hi"}, "text")
    document = ProjectDocument(project)
    panel = PropertiesPanel(document)
    qtbot.addWidget(panel)
    panel.set_selection(["text"])
    panel.rebuild()
    find_item(panel, "font").setText(str(MONTSERRAT))
    assert document.project.find_widget("text").props["font"] == "Montserrat-Medium.ttf"
    assert [item["name"] for item in assets.fonts(document.project)] == ["Montserrat-Medium.ttf"]
    document.undo_stack.undo()
    assert not assets.fonts(document.project)
    document.undo_stack.setClean()


@needs_runtime
def test_an_agent_adds_a_font_and_uses_it(tmp_path, monkeypatch):
    monkeypatch.setattr(mcp_server, "is_enabled", lambda: True)
    path = tmp_path / "project.json"

    def call(tool, **arguments):
        result = mcp_server._call_tool({"name": tool, "arguments": arguments})
        text = result["content"][0].get("text", "")
        assert not result.get("isError"), text
        return json.loads(text) if text else result

    call("create_project", path=str(path), board="esp32_4848s040_480")
    assert call("add_font", project=str(path), file=str(MONTSERRAT))["font"] == "Montserrat-Medium.ttf"
    added = call("add_widget", project=str(path), type="label", name="big", props={"text": "21°", "fontSize": 60, "font": "Montserrat-Medium.ttf"})
    assert added["warnings"] == []
    info = call("project_info", project=str(path))
    assert info["fonts"][0]["name"] == "Montserrat-Medium.ttf" and "base64" not in json.dumps(info)
    report = json.loads(mcp_server._call_tool({"name": "simulate", "arguments": {"project": str(path), "steps": [{"action": "eval", "expr": "ui.big.get_style_text_font(lv.PART.MAIN).get_line_height()"}]}})["content"][0]["text"])
    assert report["passed"] and report["values"][0]["value"] > 50  # taller than any built-in font of this board
    assert call("remove_font", project=str(path), name="Montserrat-Medium.ttf")["stillUsedBy"] == ["big"]


@needs_runtime
def test_the_c_export_draws_the_project_font_like_python(tmp_path):
    from lvgl_mpy_studio.build.c_compiler import compile_c
    from lvgl_mpy_studio.build.compiler import compile_python

    project, _name = with_font(size=31, text="AVATAR Type 21")
    project.set_display_size(800, 480)
    python_dir, c_dir = tmp_path / "py", tmp_path / "c"
    generate_project(project, python_dir)
    compile_python(python_dir)
    generated = generate_c(project, c_dir)
    source = (c_dir / "ui.c").read_text()
    assert generated["warnings"] == [] and "lv_binfont_create_from_buffer" in source and "font_montserrat_medium_31_data" in source
    frames = []
    for command, folder in (([str(runtime_path()), "main.py"], python_dir), ([str(compile_c(c_dir, jobs=4))], c_dir)):
        dump = folder / "frame.raw"
        done = subprocess.run(command, cwd=folder, env=runtime_environment(LVSIM_HEADLESS="1", LVSIM_FRAMES="1", LVSIM_TICK_MS="0", LVSIM_DUMP=str(dump), MICROPYPATH="."), capture_output=True, text=True, timeout=30)
        assert done.returncode == 0, done.stderr
        frames.append(dump.read_bytes())
    assert len(frames[0]) == 800 * 480 * 2 and frames[0] == frames[1]
    assert frames[0].count(b"\xff\xff") > 200  # white text was drawn


def test_fonts_too_heavy_for_the_board_are_reported():
    from lvgl_mpy_studio.gen.fonts import font_memory_warning
    from lvgl_mpy_studio.gen.project_gen import legacy_data

    project, _name = with_font(size=60)
    data = legacy_data(project)
    assert font_memory_warning(data, 28_000_000) is None  # the STM32H7
    warning = font_memory_warning(data, 192_000)          # the RP2350
    assert warning and "192 kB free" in warning and "need about 1" in warning  # some 60 kB of font, two and a half times over
    project.find_widget("text").props["font"] = ""
    assert font_memory_warning(legacy_data(project), 192_000) is None


def test_memory_is_measured_after_the_reset_and_the_warning_survives_a_failed_start(tmp_path):
    from test_device import FakeRunner

    from lvgl_mpy_studio.core.boards import builtin_profiles
    from lvgl_mpy_studio.device.service import DeviceError, DeviceSession

    class Runner(FakeRunner):
        free = 0
        fails = False

        def __call__(self, command, timeout):
            script = command[-1] if command else ""
            # while the previous application runs the board has little free; once it is reset, its real room
            self.info["memoryFree"] = self.free if self.resets else 47_000
            if self.fails and "import app_main" in script:
                raise DeviceError("device.command", "MemoryError: memory allocation failed")
            return super().__call__(command, timeout)

    def upload(free, fails=False, size=60):
        project, _name = with_font(size=size)
        project.board = next(profile for profile in builtin_profiles() if "rp2350" in profile["id"])
        project.set_display_size(project.board["logicalWidth"], project.board["logicalHeight"])
        runner = Runner()
        runner.free, runner.fails = free, fails
        session = DeviceSession(runner=runner)
        session.connect("/dev/fake", project.board)
        try:
            return session.upload(project, tmp_path / f"{free}-{fails}", run=True)
        finally:
            assert runner.resets == 2  # one to free the memory to measure, one to start clean

    assert not [warning for warning in upload(28_000_000)["warnings"] if "RAM" in warning]
    assert [warning for warning in upload(192_000)["warnings"] if "192 kB free" in warning]
    with pytest.raises(DeviceError) as failure:
        upload(192_000, fails=True)
    assert [warning for warning in failure.value.warnings if "192 kB free" in warning]
