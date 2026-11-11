from pathlib import Path

import pytest

from lvgl_mpy_studio.build.visual import ERROR, FAILED, MISSING, PASSED, UPDATED, PngError, compare, load_scenarios, read_png, rgb565_to_rgb, run_visual_tests, save_scenario, write_png
from lvgl_mpy_studio.cli import main
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.platform import runtime_path

needs_runtime = pytest.mark.skipif(not runtime_path().exists(), reason="runtime not built")


def small_project(text="Ciao"):
    project = Project()
    project.set_display_size(120, 80)
    project.add_widget(project.pages[0], "label", {"x": 10, "y": 10, "text": text}, "label1")
    return project


def test_png_round_trip(tmp_path):
    rgb = bytes(range(256)) * 3
    rgb = rgb[:4 * 3 * 3]
    write_png(tmp_path / "a.png", rgb, 4, 3)
    assert read_png(tmp_path / "a.png") == (rgb, 4, 3)


def test_png_file_is_valid_for_other_tools(tmp_path):
    from PySide6.QtGui import QImage

    write_png(tmp_path / "a.png", bytes((255, 0, 0)) * 6, 3, 2)
    image = QImage(str(tmp_path / "a.png"))
    assert (image.width(), image.height()) == (3, 2)
    assert image.pixelColor(2, 1).name() == "#ff0000"


def test_a_foreign_file_is_refused(tmp_path):
    (tmp_path / "a.png").write_bytes(b"non un png")
    with pytest.raises(PngError):
        read_png(tmp_path / "a.png")


def test_white_and_black_convert_exactly():
    assert rgb565_to_rgb(b"\xff\xff\x00\x00") == bytes((255, 255, 255, 0, 0, 0))


def test_compare_reports_count_and_box():
    first = bytes(3 * 12)
    second = bytearray(first)
    second[(1 * 4 + 2) * 3] = 9
    second[(2 * 4 + 3) * 3] = 9
    different, box, image = compare(first, bytes(second), 4, 3)
    assert (different, box) == (2, (2, 1, 3, 2))
    assert image[(1 * 4 + 2) * 3] == 255


def test_equal_images_have_no_diff():
    assert compare(b"\0\0\0", b"\0\0\0", 1, 1) == (0, None, None)


@needs_runtime
def test_missing_baseline_fails_until_it_is_written(tmp_path):
    project = small_project()
    assert run_visual_tests(project, tmp_path)[0].status == MISSING
    assert run_visual_tests(project, tmp_path, update=True)[0].status == UPDATED
    assert run_visual_tests(project, tmp_path)[0].status == PASSED


@needs_runtime
def test_change_is_reported_with_images_and_cleared_when_fixed(tmp_path):
    run_visual_tests(small_project(), tmp_path, update=True)
    result = run_visual_tests(small_project("Altro testo"), tmp_path)[0]
    assert result.status == FAILED and result.different > 0
    assert (tmp_path / "main.actual.png").exists() and (tmp_path / "main.diff.png").exists()
    assert run_visual_tests(small_project(), tmp_path)[0].status == PASSED
    assert not (tmp_path / "main.actual.png").exists() and not (tmp_path / "main.diff.png").exists()


@needs_runtime
def test_threshold_tolerates_small_changes(tmp_path):
    run_visual_tests(small_project(), tmp_path, update=True)
    different = run_visual_tests(small_project("Altro testo"), tmp_path)[0].different
    assert run_visual_tests(small_project("Altro testo"), tmp_path, threshold=different)[0].status == PASSED


@needs_runtime
def test_every_page_gets_its_own_baseline(tmp_path):
    project = small_project()
    project.pages.append(project.new_page("seconda"))
    assert [result.page for result in run_visual_tests(project, tmp_path, update=True)] == ["main", "seconda"]
    assert (tmp_path / "seconda.png").exists()
    assert [result.page for result in run_visual_tests(project, tmp_path, pages=["seconda"])] == ["seconda"]


def test_negative_threshold_is_refused(tmp_path):
    with pytest.raises(ValueError):
        run_visual_tests(small_project(), tmp_path, threshold=-1)


def test_unknown_page_is_an_error(tmp_path):
    with pytest.raises(ValueError):
        run_visual_tests(small_project(), tmp_path, pages=["nessuna"])


@needs_runtime
def test_project_code_runs_unless_design_only(tmp_path):
    project = small_project("Prima")
    project.ensure_handler("main", "SCREEN_LOADED")[1].body = "ui.label1.set_text('Dopo il codice')"
    run_visual_tests(small_project("Prima"), tmp_path, update=True)
    assert run_visual_tests(project, tmp_path)[0].status == FAILED
    assert run_visual_tests(project, tmp_path, design_only=True)[0].status == PASSED


@needs_runtime
def test_broken_project_code_is_an_error(tmp_path):
    project = small_project()
    project.ensure_handler("main", "SCREEN_LOADED")[1].body = "ui.label1.non_esiste()"
    result = run_visual_tests(project, tmp_path, update=True)[0]
    assert result.status == ERROR and "non_esiste" in result.message
    assert not (tmp_path / "main.png").exists()


@needs_runtime
def test_baseline_of_another_size_is_an_error(tmp_path):
    run_visual_tests(small_project(), tmp_path, update=True)
    project = small_project()
    project.set_display_size(100, 80)
    assert run_visual_tests(project, tmp_path)[0].status == ERROR


@needs_runtime
def test_command_line_exit_codes(tmp_path, capsys):
    path = tmp_path / "progetto.json"
    small_project().save(path)
    assert main(["--language", "en", "test", str(path)]) == 1
    assert "baseline missing" in capsys.readouterr().out
    assert main(["--language", "en", "test", str(path), "--update"]) == 0
    assert (tmp_path / "visual" / "120x80" / "main.png").exists()
    assert main(["--language", "en", "test", str(path)]) == 0
    small_project("Diverso").save(path)
    assert main(["--language", "en", "test", str(path)]) == 1
    assert "different" in capsys.readouterr().out


@needs_runtime
@pytest.mark.parametrize("name", ("tictactoe", "simon", "snake", "breakout"))
def test_examples_render_the_same_twice(tmp_path, name):
    root = Path(__file__).parents[1] / "examples" / name
    project = Project.load(root / "project.json")
    assert run_visual_tests(project, tmp_path, update=True)[0].status == UPDATED
    assert run_visual_tests(project, tmp_path)[0].status == PASSED


def tap_project():
    project = small_project()
    project.add_widget(project.pages[0], "button", {"x": 10, "y": 10, "width": 80, "height": 40}, name="pulsante")
    project.add_widget(project.pages[0], "label", {"x": 10, "y": 70, "text": "Prima"}, name="esito")
    project.ensure_handler("pulsante", "CLICKED")[1].body = "ui.esito.set_text('Dopo')\n"
    return project


def write_scenario(tmp_path, **scenario):
    save_scenario(tmp_path, {"name": "tocco", "steps": [{"action": "screenshot", "label": "prima"}, {"action": "tap", "widget": "pulsante"}, {"action": "wait", "ms": 200}, {"action": "assert", "expr": "True"}], **scenario})


@needs_runtime
def test_scenario_baselines_are_written_and_then_pass(tmp_path):
    project = tap_project()
    write_scenario(tmp_path)
    results = run_visual_tests(project, tmp_path, update=True, scenarios=["tocco"])
    assert [(result.page, result.status) for result in results] == [("tocco: prima", UPDATED), ("tocco: final", UPDATED)]
    assert read_png(tmp_path / "tocco@prima.png")[0] != read_png(tmp_path / "tocco@final.png")[0]
    assert [result.status for result in run_visual_tests(project, tmp_path)] == [MISSING, PASSED, PASSED]  # the page has no reference yet
    run_visual_tests(project, tmp_path, update=True)
    assert all(result.status == PASSED for result in run_visual_tests(project, tmp_path))


@needs_runtime
def test_scenario_notices_a_changed_handler(tmp_path):
    project = tap_project()
    write_scenario(tmp_path)
    run_visual_tests(project, tmp_path, update=True, scenarios=["tocco"])
    project.code.handlers[next(iter(project.code.handlers))].body = "ui.esito.set_text('Altro')\n"
    statuses = {result.page: result.status for result in run_visual_tests(project, tmp_path, scenarios=["tocco"])}
    assert statuses == {"tocco: prima": PASSED, "tocco: final": FAILED}


@needs_runtime
def test_a_failed_assert_fails_the_scenario(tmp_path):
    project = tap_project()
    save_scenario(tmp_path, {"name": "falso", "steps": [{"action": "assert", "expr": "1 == 2"}]})
    [result] = run_visual_tests(project, tmp_path, scenarios=["falso"])
    assert result.status == ERROR and "1 == 2" in result.message


def test_scenarios_file_problems_are_reported(tmp_path):
    (tmp_path / "scenarios.json").write_text('{"scenarios": [{"steps": []}]}', encoding="utf-8")
    with pytest.raises(ValueError, match="unique"):
        run_visual_tests(small_project(), tmp_path)
    (tmp_path / "scenarios.json").write_text('{"scenarios": []}', encoding="utf-8")
    with pytest.raises(ValueError, match="scenario-not-found"):
        run_visual_tests(small_project(), tmp_path, scenarios=["nessuno"])


def test_saving_a_scenario_replaces_one_with_the_same_name(tmp_path):
    save_scenario(tmp_path, {"name": "uno", "steps": []})
    save_scenario(tmp_path, {"name": "due", "steps": []})
    save_scenario(tmp_path, {"name": "uno", "steps": [{"action": "wait", "ms": 10}]})
    scenarios = load_scenarios(tmp_path)
    assert [item["name"] for item in scenarios] == ["due", "uno"] and scenarios[1]["steps"]


def test_scenario_names_must_stay_distinct_as_files(tmp_path):
    save_scenario(tmp_path, {"name": "A/B", "steps": []})
    with pytest.raises(ValueError, match="clash"):
        save_scenario(tmp_path, {"name": "A?B", "steps": []})


def test_scenarios_cannot_run_without_code(tmp_path):
    save_scenario(tmp_path, {"name": "uno", "steps": []})
    with pytest.raises(ValueError, match="design-only"):
        run_visual_tests(small_project(), tmp_path, scenarios=["uno"], design_only=True)


def test_malformed_steps_are_an_error_result(tmp_path):
    (tmp_path / "scenarios.json").write_text('{"scenarios": [{"name": "rotto", "steps": ["tap"]}]}', encoding="utf-8")
    [result] = run_visual_tests(small_project(), tmp_path, scenarios=["rotto"])
    assert result.status == ERROR and "object" in result.message
