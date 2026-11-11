import json
from pathlib import Path

import pytest

from lvgl_mpy_studio.gen.gen_python import generate_python

CORPUS = Path(__file__).parents[1] / "reference" / "corpus"
CASES = sorted(CORPUS.glob("*.json"))


@pytest.mark.parametrize("path", CASES, ids=lambda path: path.stem)
def test_corpus_generates_valid_python(path):
    case = json.loads(path.read_text(encoding="utf-8"))
    compile(generate_python(case["project"], case["generatedDate"]), path.name, "exec")


def test_reference_corpus_is_complete():
    assert len(CASES) == 232
