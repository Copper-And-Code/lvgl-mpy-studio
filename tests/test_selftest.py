import json
import subprocess
import sys

from lvgl_mpy_studio.selftest.report import FAILED, PASSED, SKIPPED, Report


def test_report_counts_and_fails_when_a_step_failed(tmp_path):
    lines = []
    report = Report(tmp_path / "ok", lines.append)
    report.scenario("One")
    report.add("One", "first", PASSED, 0.5)
    assert report.finish(["header"])
    assert "RESULT: PASSED" in lines and (tmp_path / "ok/report.txt").read_text().startswith("header\n")

    report = Report(tmp_path / "bad", lines.append)
    assert not report.succeeded  # a run without steps proved nothing
    report.add("One", "first", PASSED)
    report.add("One", "second", FAILED, 1, "expected 1, found 2", ["one-02-ide.png"])
    report.add("One", "the rest of this scenario", SKIPPED)
    assert not report.finish([])
    text = (tmp_path / "bad/report.txt").read_text()
    assert "FAILED    1.00 s  second" in text and "expected 1, found 2" in text and "picture: one-02-ide.png" in text
    assert "1 passed, 1 failed, 1 skipped" in text and "RESULT: FAILED" in text
    stored = json.loads((tmp_path / "bad/report.json").read_text())
    assert stored["result"] == FAILED and [step["outcome"] for step in stored["steps"]] == [PASSED, FAILED, SKIPPED]


def run(tmp_path, *arguments):
    return subprocess.run([sys.executable, "-m", "lvgl_mpy_studio", "selftest", *arguments], cwd=tmp_path, capture_output=True, text=True, timeout=180)


def test_selftest_lists_and_refuses_unknown_scenarios(tmp_path):
    listed = run(tmp_path, "--list")
    assert listed.returncode == 0
    assert [line.split()[0] for line in listed.stdout.splitlines()] == ["tour", "save", "pages", "resolution", "assets", "modules", "components", "errors"]
    unknown = run(tmp_path, "nothing")
    assert unknown.returncode == 2 and "Unknown scenario: nothing" in unknown.stdout
    assert not list(tmp_path.iterdir())  # neither wrote a report


def test_selftest_runs_every_scenario_in_the_real_ide(tmp_path):
    result = run(tmp_path, "--output", str(tmp_path / "report"))
    text = (tmp_path / "report/report.txt").read_text()
    assert result.returncode == 0, result.stdout + result.stderr
    assert "RESULT: PASSED" in text and "0 failed, 0 skipped" in text
    assert "Touch the button in the simulator: the handler runs and the screen changes" in text
    assert text.count("\n== ") == 8  # every scenario ran
    assert (tmp_path / "report/work/save/saved.json").exists()
    assert not list((tmp_path / "report").glob("*.png"))  # pictures are taken only of what failed
