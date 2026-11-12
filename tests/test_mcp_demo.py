"""The "from a prompt to an app" demo: an agent's whole session, replayed against the server.

examples/weather/mcp-session.json holds the tool calls in order; examples/weather/mcp-result.json is
what they produce. examples/weather/project.json is that result reworked later, with icons. If a tool changes so that the session no longer builds the same app, this fails.
"""

import json
from pathlib import Path

import pytest

from lvgl_mpy_studio import mcp_server
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.platform import runtime_path

EXAMPLE = Path(__file__).parents[1] / "examples" / "weather"

pytestmark = pytest.mark.skipif(not runtime_path().exists(), reason="runtime not built")


def comparable(project):
    """The project without the ids, which are new at every run."""
    data = project.to_dict()
    for key in ("projectId", "currentPageId"):
        data.pop(key, None)
    for page in data["pages"]:
        page.pop("id")
        ids = {widget["id"]: widget["name"] for widget in page["widgets"]}
        for widget in page["widgets"]:
            widget.pop("id")
            if widget.get("parentId"):
                widget["parentId"] = ids[widget["parentId"]]
    for module in data.get("modules", []):
        module.pop("id")
    return data


def test_the_recorded_session_builds_the_weather_example(tmp_path, monkeypatch):
    monkeypatch.setattr(mcp_server, "is_enabled", lambda: True)
    path = tmp_path / "weather" / "project.json"
    calls = json.loads((EXAMPLE / "mcp-session.json").read_text(encoding="utf-8").replace("{project}", str(path)))
    answers = {}
    characters = 0
    for name, arguments in calls:
        result = mcp_server._call_tool({"name": name, "arguments": arguments})
        text = "".join(item.get("text", "") for item in result["content"])
        assert not result.get("isError"), f"{name}: {text}"
        characters += len(text)
        if text.startswith(("{", "[")):
            answers.setdefault(name, []).append(json.loads(text))
    assert answers["simulate"][0]["passed"]
    assert [item["passed"] for item in answers["visual_test"]] == [True, True]
    assert all(page["status"] == "passed" for page in answers["visual_test"][1]["pages"])
    assert answers["validate"][0] == {"warnings": [], "outOfBounds": []}
    assert comparable(Project.load(path)) == comparable(Project.load(EXAMPLE / "mcp-result.json"))
    assert characters < 25000  # what the agent has to read for the whole session


def test_the_weather_example_matches_its_reference_images():
    from lvgl_mpy_studio.build.visual import PASSED, baseline_dir, run_visual_tests

    project = Project.load(EXAMPLE / "project.json")
    results = run_visual_tests(project, baseline_dir((EXAMPLE / "project.json").resolve(), project))
    assert [result.page for result in results] == ["main", "settings", "tour: catania", "tour: final"]
    assert all(result.status == PASSED for result in results)


def test_text_that_cannot_be_drawn_as_asked_is_reported(tmp_path, monkeypatch):
    monkeypatch.setattr(mcp_server, "is_enabled", lambda: True)
    path = tmp_path / "p.json"
    for name, arguments in (
        ("create_project", {"path": str(path), "board": "esp32_4848s040_480"}),
        ("add_widget", {"project": str(path), "type": "label", "name": "big", "props": {"text": "Loading…", "fontSize": 60}}),
    ):
        result = mcp_server._call_tool({"name": name, "arguments": arguments})
    warnings = json.loads(result["content"][0]["text"])["warnings"]
    assert any("font size 60" in warning and "drawn at 40" in warning for warning in warnings)
    assert any("U+2026" in warning for warning in warnings)
    boards = json.loads(mcp_server._call_tool({"name": "list_boards", "arguments": {}})["content"][0]["text"])
    assert {board["id"]: board["fonts"] for board in boards}["esp32_4848s040_480"] == [14, 16, 24, 32, 40]
    types = json.loads(mcp_server._call_tool({"name": "list_widget_types", "arguments": {"types": ["label"]}})["content"][0]["text"])
    assert list(types) == ["label"] and "text" in types["label"]["defaults"]
