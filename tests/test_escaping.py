import ast

from hypothesis import example, given, strategies as st

from lvgl_mpy_studio.gen.escaping import c_comment_lines, python_string


@given(st.text())
def test_python_strings_round_trip(text):
    assert ast.literal_eval(python_string(text)) == text


@given(st.text(alphabet=st.characters(blacklist_categories=("Cs",))))
@example("/*")
@example("//*")
def test_c_comments_stay_on_one_logical_line(text):
    rendered = c_comment_lines(text)
    assert "/*" not in rendered
    assert not any(line.endswith("\\") for line in rendered.splitlines())
