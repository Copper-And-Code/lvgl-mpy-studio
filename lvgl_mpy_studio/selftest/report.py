"""The report of a self-test run: one line for each step, and pictures of what failed."""

import json
import time
from pathlib import Path

PASSED, FAILED, SKIPPED = "PASSED", "FAILED", "SKIPPED"


class Report:
    def __init__(self, directory, echo=print):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.echo = echo
        self.entries = []  # dicts: scenario, step, outcome, seconds, detail, pictures
        self.started = time.monotonic()
        self._lines = []

    def line(self, text=""):
        self._lines.append(text)
        self.echo(text)

    def scenario(self, title):
        self.line()
        self.line(f"== {title}")

    def add(self, scenario, step, outcome, seconds=0.0, detail="", pictures=()):
        self.entries.append({"scenario": scenario, "step": step, "outcome": outcome, "seconds": round(seconds, 3), "detail": detail, "pictures": list(pictures)})
        self.line(f"{outcome:<7} {seconds:6.2f} s  {step}")
        for text in filter(None, [detail, *(f"picture: {name}" for name in pictures)]):
            for row in str(text).splitlines():
                self.line(f"            {row}")

    def count(self, outcome):
        return sum(entry["outcome"] == outcome for entry in self.entries)

    @property
    def succeeded(self):
        return bool(self.entries) and not self.count(FAILED) and not self.count(SKIPPED)

    def finish(self, header):
        self.line()
        self.line(f"{self.count(PASSED)} passed, {self.count(FAILED)} failed, {self.count(SKIPPED)} skipped in {time.monotonic() - self.started:.1f} s")
        self.line("RESULT: " + (PASSED if self.succeeded else FAILED))
        (self.directory / "report.txt").write_text("\n".join([*header, *self._lines]) + "\n", encoding="utf-8")
        (self.directory / "report.json").write_text(json.dumps({"result": PASSED if self.succeeded else FAILED, "steps": self.entries}, indent=2), encoding="utf-8")
        self.echo(f"Report: {self.directory / 'report.txt'}")
        return self.succeeded
