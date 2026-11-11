import os
from pathlib import Path
import subprocess
import tempfile

from hypothesis import given, settings, strategies as st

from lvgl_mpy_studio.build.c_compiler import compile_c
from lvgl_mpy_studio.core.model import Project, widget_definitions
from lvgl_mpy_studio.gen.gen_c import NEW_HANDLERS_BEGIN, NEW_HANDLERS_END, generate_c


def make_project(kind="button"):
    project = Project(f"c_{kind}")
    project.add_widget(project.pages[0], kind, name=f"{kind}1")
    return project


def test_c_golden_button(tmp_path):
    generate_c(make_project(), tmp_path)
    golden = Path(__file__).parent / "golden/c-button-ui.c"
    assert (tmp_path / "ui.c").read_text() == golden.read_text()


def test_user_handlers_are_preserved_and_missing_added(tmp_path):
    project = make_project()
    name, handler = project.ensure_handler("button1")
    handler.body = 'print("ciao")'
    generate_c(project, tmp_path)
    events = tmp_path / "ui_events.c"
    original = events.read_text().replace("LV_UNUSED(e);", "LV_UNUSED(e); /* modifica utente */")
    events.write_text(original)
    project.add_widget(project.pages[0], "label", name="label1")
    project.ensure_handler("label1", "FOCUSED")
    generate_c(project, tmp_path)
    updated = events.read_text()
    assert "/* modifica utente */" in updated
    assert updated.count(f"void {name}(lv_event_t * e)") == 1
    assert "void label1_focused(lv_event_t * e)" in updated
    assert NEW_HANDLERS_BEGIN in updated and NEW_HANDLERS_END in updated
    assert '// print("ciao")' in updated


def test_c_generation_covers_all_widget_types(tmp_path):
    for kind in widget_definitions():
        output = tmp_path / kind
        generate_c(make_project(kind), output)
        source = (output / "ui.c").read_text()
        assert f"ui_{kind}1 = lv_" in source
        assert (output / "Makefile").read_text().count("-std=c11") == 1


def test_cache_depends_on_configuration(tmp_path, monkeypatch):
    root = tmp_path / "root"
    conf = root / ".reference/lvgl-bindings"
    conf.mkdir(parents=True)
    (conf / "lv_conf.h").write_text("first")
    generate_c(make_project(), tmp_path / "one", root)
    first = (tmp_path / "one/Makefile").read_text()
    (conf / "lv_conf.h").write_text("second")
    generate_c(make_project(), tmp_path / "two", root)
    second = (tmp_path / "two/Makefile").read_text()
    assert first != second


def test_camelcase_widget_names_and_event_link(tmp_path):
    project = Project("camelcase")
    project.add_widget(project.pages[0], "button", name="counterButton")
    project.ensure_handler("counterButton")
    generate_c(project, tmp_path)
    assert "extern lv_obj_t * ui_counterButton;" in (tmp_path / "ui.h").read_text()
    assert "#define ui_counterButton" not in (tmp_path / "ui.h").read_text()
    assert "lv_obj_add_event_cb(ui_counterButton, counterButton_clicked" in (tmp_path / "ui.c").read_text()


def run_c_fixture(tmp_path, project, fixture):
    generate_c(project, tmp_path)
    (tmp_path / "fixture.c").write_text(fixture)
    root = Path(__file__).parents[1]
    result = subprocess.run([
        "make", "-C", str(tmp_path), "-j2",
        f"APP_SOURCES=ui.c fixture.c {root / 'native/lvsim/lvsim_io.c'} {root / 'native/lvsim/lvsim_net_posix.c'} {root / 'native/lvsim/lvsim_time_posix.c'}",
    ], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
    result = subprocess.run([str(tmp_path / "app")], cwd=tmp_path, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stdout + result.stderr


FIXTURE_PREAMBLE = r'''#include <stdio.h>
#include "ui.h"
#include "ui_events.h"

#define CHECK(condition) do { if (!(condition)) { fprintf(stderr, "check failed at line %d\n", __LINE__); return 1; } } while (0)

static void flush_cb(lv_display_t * display, const lv_area_t * area, uint8_t * pixels)
{
    LV_UNUSED(area);
    LV_UNUSED(pixels);
    lv_display_flush_ready(display);
}

static void init_display(void)
{
    static uint8_t buffer[800 * 10 * 2];
    lv_display_t * display = lv_display_create(800, 480);
    lv_display_set_buffers(display, buffer, NULL, sizeof(buffer), LV_DISPLAY_RENDER_MODE_PARTIAL);
    lv_display_set_flush_cb(display, flush_cb);
}
'''


def test_public_widget_names_remain_distinct_at_runtime(tmp_path):
    project = Project("collisions")
    long_name = "widget_" + "a" * 60
    names = ("MyButton", "mybutton", "mybutton_2", long_name, long_name + "_other")
    for index, name in enumerate(names):
        project.add_widget(project.pages[0], "button", {"x": 10 + index * 100, "width": 100 + index * 10}, name)
        project.ensure_handler(name)
    counters = "\n".join(f"static int count_{index};" for index in range(len(names)))
    handlers = "\n".join(f"void {name}_clicked(lv_event_t * e) {{ LV_UNUSED(e); count_{index}++; }}" for index, name in enumerate(names))
    checks = "\n".join([
        "    CHECK(ui_MyButton != ui_mybutton && ui_mybutton != ui_mybutton_2);",
        "    CHECK(lv_obj_get_width(ui_MyButton) == 100 && lv_obj_get_width(ui_mybutton) == 110);",
        "    CHECK(lv_obj_get_width(ui_mybutton_2) == 120);",
        f"    CHECK(lv_obj_get_width(ui_{long_name}) == 130 && lv_obj_get_width(ui_{long_name}_other) == 140);",
        *[line for current, name in enumerate(names) for line in [
            f"    lv_obj_send_event(ui_{name}, LV_EVENT_CLICKED, NULL);",
            *[f"    CHECK(count_{index} == {1 if index <= current else 0});" for index in range(len(names))],
        ]],
    ])
    fixture = FIXTURE_PREAMBLE + counters + "\n" + handlers + "\nint main(void)\n{\n    lv_init();\n    init_display();\n    ui_create();\n    lv_obj_update_layout(lv_screen_active());\n" + checks + "\n    return 0;\n}\n"
    run_c_fixture(tmp_path, project, fixture)


def test_deferred_page_callbacks_and_screen_loaded_at_runtime(tmp_path):
    from lvgl_mpy_studio.core.model import Page

    project = Project("pages")
    project.pages.append(Page("second"))
    project.add_widget(project.pages[1], "button", name="secondButton")
    project.ensure_handler("main", "SCREEN_LOADED")
    project.ensure_handler("second", "SCREEN_LOADED")
    project.ensure_handler("secondButton", "CLICKED")
    fixture = FIXTURE_PREAMBLE + r'''
static int main_loaded;
static int second_loaded;
static int second_clicked;
void main_screen_loaded(lv_event_t * e) { LV_UNUSED(e); main_loaded++; }
void second_screen_loaded(lv_event_t * e) { LV_UNUSED(e); second_loaded++; }
void secondButton_clicked(lv_event_t * e) { LV_UNUSED(e); second_clicked++; }
int main(void)
{
    lv_init();
    init_display();
    ui_create();
    CHECK(main_loaded == 1 && second_loaded == 0);
    pages_load_page(1);
    CHECK(second_loaded == 1);
    lv_obj_send_event(ui_secondButton, LV_EVENT_CLICKED, NULL);
    CHECK(second_clicked == 1);
    pages_load_page(0);
    pages_load_page(1);
    CHECK(main_loaded == 2 && second_loaded == 2);
    lv_obj_send_event(ui_secondButton, LV_EVENT_CLICKED, NULL);
    CHECK(second_clicked == 2);
    return 0;
}
'''
    run_c_fixture(tmp_path, project, fixture)
    (tmp_path / "app").unlink()
    compile_c(tmp_path)
    env = os.environ.copy()
    env.update({"LVSIM_HEADLESS": "1", "LVSIM_FRAMES": "1", "LVSIM_DUMP": str(tmp_path / "frame.raw")})
    result = subprocess.run([str(tmp_path / "app"), "--selftest"], cwd=tmp_path, env=env, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stdout + result.stderr
    assert len((tmp_path / "frame.raw").read_bytes()) == 800 * 480 * 2


@settings(max_examples=25, deadline=None, derandomize=True)
@given(st.text(max_size=80))
def test_fuzz_generated_c_compiles(text):
    root = Path(__file__).parents[1]
    project = Project("fuzz_c")
    project.add_widget(project.pages[0], "label", {"text": text}, "label1")
    with tempfile.TemporaryDirectory() as directory:
        generate_c(project, directory)
        result = subprocess.run([
            "gcc", "-fsyntax-only", "-std=c11", "-Wall", "-Wextra", "-Werror", "-DLV_CPYTHON_BUILD",
            "-DLV_CONF_INCLUDE_SIMPLE", f"-I{root / '.reference/lvgl-bindings'}",
            f"-I{root / '.reference/lvgl-bindings/lvgl'}", "ui.c", "ui_events.c",
        ], cwd=directory, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr


def test_a_file_exported_by_0_4_keeps_its_markers_and_gets_new_handlers(tmp_path):
    project = Project()
    project.add_widget(project.pages[0], "button", name="button1")
    project.ensure_handler("button1", "CLICKED")
    generate_c(project, tmp_path)
    events = tmp_path / "ui_events.c"
    events.write_text(events.read_text().replace("lms:new-handlers", "lvgl-ide:new-handlers"))
    project.add_widget(project.pages[0], "label", name="label1")
    project.ensure_handler("label1", "FOCUSED")
    generate_c(project, tmp_path)
    updated = events.read_text()
    assert updated.index("void label1_focused(lv_event_t * e)") < updated.index("// </lvgl-ide:new-handlers>")
    assert NEW_HANDLERS_BEGIN not in updated and NEW_HANDLERS_END not in updated
