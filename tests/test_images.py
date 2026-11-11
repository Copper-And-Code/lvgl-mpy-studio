"""Images of a project: stored in the project file, drawn by the real runtime, sent to every target."""

import json

import pytest
from PySide6.QtGui import QColor, QImage, QPainter

from lvgl_mpy_studio import mcp_server
from lvgl_mpy_studio.build.preview import render_with_log
from lvgl_mpy_studio.build.visual import rgb565_to_rgb
from lvgl_mpy_studio.core import assets
from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.gen.board_gen import generate_board
from lvgl_mpy_studio.gen.gen_c import generate_c
from lvgl_mpy_studio.gen.project_gen import generate_project
from lvgl_mpy_studio.platform import runtime_path
from helpers import find_item

needs_runtime = pytest.mark.skipif(not runtime_path().exists(), reason="runtime not built")
RED = (229, 57, 53)


def picture(path, width=64, height=48, kind="PNG"):
    """A red ellipse on a transparent background; returns the file."""
    image = QImage(width, height, QImage.Format_ARGB32)
    image.fill(QColor(0, 0, 0, 0))
    painter = QPainter(image)
    painter.setBrush(QColor(*RED))
    painter.setPen(QColor(*RED))
    painter.drawEllipse(2, 2, width - 4, height - 4)
    painter.end()
    assert (image if kind == "PNG" else image.convertToFormat(QImage.Format_RGB888)).save(str(path), kind)
    return path


def with_image(tmp_path):
    project = Project()
    project.set_display_size(240, 160)
    name = assets.add_image(project, "My Logo.png", picture(tmp_path / "logo.png").read_bytes())
    project.add_widget(project.pages[0], "image", {"x": 20, "y": 20, "width": 64, "height": 48, "src": name}, "pic")
    return project, name


def pixel(pixels, x, y, width=240):
    rgb = rgb565_to_rgb(pixels)
    return tuple(rgb[(y * width + x) * 3:(y * width + x) * 3 + 3])


def test_images_are_named_listed_and_removed(tmp_path):
    project, name = with_image(tmp_path)
    assert name == "My_Logo.png"
    assert assets.images(project) == [{"name": name, "bytes": (tmp_path / "logo.png").stat().st_size, "width": 64, "height": 48}]
    with pytest.raises(assets.AssetError, match="already exists"):
        assets.add_image(project, name, (tmp_path / "logo.png").read_bytes())
    assert assets.free_image_name(project, "My Logo.png") == "My_Logo_2.png"
    with pytest.raises(assets.AssetError, match="PNG"):
        assets.add_image(project, "x.png", picture(tmp_path / "photo.jpg", kind="JPG").read_bytes())
    with pytest.raises(assets.AssetError, match="limit"):
        assets.add_image(project, "big.png", assets.PNG_SIGNATURE + bytes(assets.MAX_IMAGE_BYTES))
    saved = tmp_path / "project.json"
    project.save(saved)
    assert assets.images(Project.load(saved)) == assets.images(project)
    assert assets.remove_image(project, name) == ["pic"]
    assert any("is not in the project" in warning for warning in project.text_warnings())


@needs_runtime
def test_the_runtime_draws_the_image(tmp_path):
    project, _name = with_image(tmp_path)
    pixels, log = render_with_log(project, 0, design_only=False)
    assert pixels, log
    red, green, blue = pixel(pixels, 20 + 32, 20 + 24)
    assert red > 200 and green < 90 and blue < 90  # the centre of the ellipse, through RGB565


def test_every_target_gets_the_image(tmp_path):
    project, name = with_image(tmp_path)
    generate_project(project, tmp_path / "py")
    assert "a2b_base64" in (tmp_path / "py" / "ui.py").read_text()
    profile = builtin_profiles()[0]
    project.board = profile
    project.resize(profile["logicalWidth"], profile["logicalHeight"], "keep")
    generated = generate_board(project, profile, tmp_path / "board")
    assert "a2b_base64" in (tmp_path / "board" / "ui.py").read_text() and "ui.py" in generated["files"]
    generate_c(project, tmp_path / "c", portable=True)
    assert "lv_image_dsc_t" in (tmp_path / "c" / "ui.c").read_text()


def test_a_large_image_says_what_it_costs(tmp_path):
    project = Project()
    assets.add_image(project, "wide.png", picture(tmp_path / "wide.png", 480, 320).read_bytes())
    assert any("wide.png" in warning and "600 kB of RAM" in warning for warning in project.text_warnings())


def test_choosing_a_picture_in_the_properties_adds_it_to_the_project(qtbot, tmp_path):
    from lvgl_mpy_studio.ui.document import ProjectDocument
    from lvgl_mpy_studio.ui.properties.panel import PropertiesPanel

    project = Project()
    project.set_display_size(240, 160)
    project.add_widget(project.pages[0], "image", {"x": 0, "y": 0, "width": 64, "height": 48}, "pic")
    document = ProjectDocument(project)
    panel = PropertiesPanel(document)
    qtbot.addWidget(panel)
    panel.set_selection(["pic"])
    panel.rebuild()
    item = find_item(panel, "src")
    item.setText(str(picture(tmp_path / "photo.jpg", 960, 640, "JPG")))  # a JPEG larger than the screen
    widget = document.project.find_widget("pic")
    assert widget.props["src"] == "photo.png"
    assert assets.images(document.project)[0]["width"] == 240 and assets.images(document.project)[0]["height"] == 160
    document.undo_stack.undo()  # one step takes back both the property and the image
    assert document.project.find_widget("pic").props.get("src", "") == "" and not assets.images(document.project)
    item = find_item(panel, "src")
    item.setText(str(tmp_path / "missing.png"))  # not a file: kept as typed, and reported
    assert any("is not in the project" in warning for warning in document.project.text_warnings())
    document.undo_stack.setClean()


@needs_runtime
def test_an_agent_adds_an_image_and_sees_it(tmp_path, monkeypatch):
    monkeypatch.setattr(mcp_server, "is_enabled", lambda: True)
    path = tmp_path / "project.json"
    logo = picture(tmp_path / "logo.png")

    def call(tool, **arguments):
        result = mcp_server._call_tool({"name": tool, "arguments": arguments})
        text = result["content"][0].get("text", "")
        assert not result.get("isError"), text
        return json.loads(text) if text else result

    call("create_project", path=str(path), width=240, height=160)
    assert call("add_image", project=str(path), file=str(logo))["image"] == "logo.png"
    call("add_widget", project=str(path), type="image", name="pic", props={"x": 20, "y": 20, "width": 64, "height": 48, "src": "logo.png"})
    info = call("project_info", project=str(path))
    assert info["images"] == [{"name": "logo.png", "bytes": logo.stat().st_size, "width": 64, "height": 48}]
    assert "base64" not in json.dumps(info)  # the picture data never goes to the agent
    report = mcp_server._call_tool({"name": "simulate", "arguments": {"project": str(path), "steps": [{"action": "wait", "ms": 100}]}})
    assert json.loads(report["content"][0]["text"])["passed"]
    assert call("remove_image", project=str(path), name="logo.png")["stillUsedBy"] == ["pic"]
    assert any("is not in the project" in warning for warning in call("validate", project=str(path))["warnings"])
    error = mcp_server._call_tool({"name": "add_image", "arguments": {"project": str(path), "file": str(picture(tmp_path / "p.jpg", kind="JPG"))}})
    assert error["isError"] and "PNG" in error["content"][0]["text"]


def test_a_picture_too_heavy_as_png_is_refused_with_a_message(qtbot, tmp_path):
    """A photo the size of the screen stays above the limit once converted: nothing must change, and no exception escape."""
    import random

    from lvgl_mpy_studio.ui.document import ProjectDocument
    from lvgl_mpy_studio.ui.properties.panel import PropertiesPanel

    noise = QImage(bytes(random.Random(1).randbytes(800 * 480 * 4)), 800, 480, QImage.Format_RGBA8888)
    noise.save(str(tmp_path / "photo.png"))
    project = Project()
    project.add_widget(project.pages[0], "image", {"x": 0, "y": 0, "width": 64, "height": 48}, "pic")
    document = ProjectDocument(project)
    panel = PropertiesPanel(document)
    qtbot.addWidget(panel)
    panel.set_selection(["pic"])
    panel.rebuild()
    item = find_item(panel, "src")
    item.setText(str(tmp_path / "photo.png"))
    assert "limit is 512 kB" in panel.error.text() and not panel.error.isHidden()
    assert not assets.images(document.project) and document.project.find_widget("pic").props.get("src", "") == ""
