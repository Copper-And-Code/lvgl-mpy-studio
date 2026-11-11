import ast
import json
from pathlib import Path

from hypothesis import HealthCheck, given, settings, strategies as st

from lvgl_mpy_studio.gen.gen_python import generate_python

DEFINITIONS = json.loads((Path(__file__).parents[1] / "lvgl_mpy_studio/gen/widgets.json").read_text(encoding="utf-8"))
TEXT = st.text(max_size=80)
PROPS = st.fixed_dictionaries({
    "x": st.integers(-1000, 1000), "y": st.integers(-1000, 1000),
    "width": st.integers(1, 1000), "height": st.integers(1, 1000),
    "text": TEXT, "options": TEXT, "items": TEXT, "spans": TEXT,
    "bgColor": st.one_of(st.from_regex(r"#[0-9a-fA-F]{6}", fullmatch=True), TEXT),
})
WIDGETS = st.builds(
    lambda kind, name, props: {"id": name, "name": name, "type": kind, "props": props, "events": [], "animations": []},
    st.sampled_from(list(DEFINITIONS)), st.from_regex(r"w[0-9]{1,4}", fullmatch=True), PROPS,
)


@settings(max_examples=1000, deadline=None, suppress_health_check=(HealthCheck.too_slow,), derandomize=True)
@given(st.lists(WIDGETS, max_size=6))
def test_generated_python_is_syntactically_valid(widgets):
    project = {"projectName": "fuzz", "pages": [{"name": "main", "canvasSize": {"width": 800, "height": 480}, "widgets": widgets}]}
    ast.parse(generate_python(project, "2026-01-01T00:00:00.000Z"))
