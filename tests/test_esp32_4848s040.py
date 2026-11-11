import copy

from lvgl_mpy_studio.core.boards import ADAPTERS, builtin_profiles, validate_profile
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.gen.board_gen import generate_board


def esp32_profile():
    return next(profile for profile in builtin_profiles() if profile["id"] == "esp32_4848s040_480")


def test_esp32_4848s040_profile_generates_native_480x480(tmp_path):
    profile = validate_profile(esp32_profile())
    assert (profile["physicalWidth"], profile["physicalHeight"]) == (480, 480)
    assert (profile["logicalWidth"], profile["logicalHeight"]) == (480, 480)
    assert profile["scale"] == 1
    assert profile["adapter"] in ADAPTERS
    assert "rgbpanel" not in profile["firmware"]["modules"]

    project = Project("esp32demo")
    project.set_display_size(480, 480)
    project.board = copy.deepcopy(profile)
    project.add_widget(project.pages[0], "button")
    result = generate_board(project, profile, tmp_path)

    assert result["manifest"]["profileId"] == profile["id"]
    assert "(480, 480)" in (tmp_path / "app_main.py").read_text()
    assert "ADAPTER = 'esp32_4848s040'" in (tmp_path / "board_adapter.py").read_text()
