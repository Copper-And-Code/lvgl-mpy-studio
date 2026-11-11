import ast

from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.gen.board_gen import generate_board
from lvgl_mpy_studio.gen.gen_c import generate_c
from lvgl_mpy_studio.gen.project_gen import generate_app_events, generate_project


def test_generated_files_and_sourcemap(tmp_path):
    project = Project("demo")
    project.add_widget(project.pages[0], "button", name="btn1")
    _name, handler = project.ensure_handler("btn1")
    handler.body = "global contatore\ncontatore += 1\n"
    project.code.module = "contatore = 0\n"
    generate_project(project, tmp_path)
    assert {path.name for path in tmp_path.iterdir()} >= {"ui.py", "app_events.py", "main.py", "display_driver.py", "sourcemap.json"}
    for name in ("ui.py", "app_events.py", "main.py", "display_driver.py"):
        ast.parse((tmp_path / name).read_text())
    assert "global btn1\n" in (tmp_path / "ui.py").read_text()
    assert "ui.btn1.add_event_cb" in (tmp_path / "main.py").read_text()


def test_empty_handler_generates_no_code(tmp_path):
    project = Project()
    project.add_widget(project.pages[0], "button", name="btn1")
    project.ensure_handler("btn1")
    generate_project(project, tmp_path)
    assert "btn1_clicked" not in (tmp_path / "app_events.py").read_text()
    assert "add_event_cb" not in (tmp_path / "main.py").read_text()


def test_empty_handler_called_from_code_is_kept():
    project = Project()
    project.add_widget(project.pages[0], "button", name="btn1")
    project.ensure_handler("btn1")
    project.code.module = "def run():\n    btn1_clicked(None)\n"
    source, _sourcemap = generate_app_events(project)
    assert "def btn1_clicked(e):\n    pass" in source


def compact_project():
    project = Project("demo")
    project.add_widget(project.pages[0], "button", {"radius": 9}, "used")
    project.add_widget(project.pages[0], "button", {"radius": 9}, "unused")
    project.pages.append(project.new_page("settings"))
    return project


def test_only_widgets_referenced_by_code_are_public(tmp_path):
    project = compact_project()
    project.code.module = "def go():\n    ui.used.set_text('x')\n"
    generate_project(project, tmp_path)
    source = (tmp_path / "ui.py").read_text()
    assert "global used\n" in source
    assert "unused" in source and "global used, unused" not in source
    assert "objects" not in source
    assert "globals()" not in source


def test_dynamic_access_keeps_every_widget_public(tmp_path):
    project = compact_project()
    project.code.module = "def go():\n    getattr(ui, 'unused').set_x(1)\n"
    generate_project(project, tmp_path)
    assert "global used, unused" in (tmp_path / "ui.py").read_text()


def test_unused_helpers_are_dropped_and_used_ones_kept(tmp_path):
    project = compact_project()
    generate_project(project, tmp_path / "a")
    source = (tmp_path / "a" / "ui.py").read_text()
    assert "def load_page" not in source
    assert "get_current_page" not in source
    assert "_init()" not in source
    project.code.module = "def go():\n    ui.load_page(ui.PAGE_SETTINGS)\n"
    generate_project(project, tmp_path / "b")
    source = (tmp_path / "b" / "ui.py").read_text()
    assert "def load_page(page_index):" in source
    assert "PAGE_SETTINGS = 1\n" in source
    assert "PAGE_MAIN" not in source
    assert "load_page_anim" not in source


def test_identical_styles_are_shared(tmp_path):
    generate_project(compact_project(), tmp_path)
    source = (tmp_path / "ui.py").read_text()
    assert "lv.style_t()" in source
    assert source.count(".add_style(_styles[") >= 2
    assert "set_style_radius" not in source
    assert "_init_styles()\n" in source


def test_unique_styles_stay_local(tmp_path):
    project = Project("demo")
    project.add_widget(project.pages[0], "button", {"radius": 9}, "only")
    generate_project(project, tmp_path)
    source = (tmp_path / "ui.py").read_text()
    assert "lv.style_t()" not in source
    assert "set_style_radius" in source


def component_project():
    project = Project("demo")
    project.add_widget(project.pages[0], "buzzer", name="buzzer1")
    project.add_widget(project.pages[0], "timer", {"period": 250}, "timer1")
    project.add_widget(project.pages[0], "label", name="lab")
    _name, handler = project.ensure_handler("timer1")
    handler.body = "ui.buzzer1.beep(440, 30)\n"
    return project


def test_components_create_no_lvgl_objects(tmp_path):
    generate_project(component_project(), tmp_path)
    ui = (tmp_path / "ui.py").read_text()
    main = (tmp_path / "main.py").read_text()
    assert "import lms_buzzer as buzzer1\n" in ui
    assert "lv.buzzer" not in ui and "lv.timer" not in ui
    assert "ui.timer1 = lv.timer_create(app_events.timer1_tick, 250, None)" in main
    assert (tmp_path / "lms_buzzer.py").exists()
    assert "EVENT.TICK" not in main


def test_project_without_components_has_no_support_code(tmp_path):
    project = Project("demo")
    project.add_widget(project.pages[0], "label", name="lab")
    generate_project(project, tmp_path)
    assert not (tmp_path / "lms_buzzer.py").exists()
    assert "lms_buzzer" not in (tmp_path / "ui.py").read_text()


def test_unused_timer_is_not_generated_and_disabled_timer_is_paused(tmp_path):
    project = Project("demo")
    project.add_widget(project.pages[0], "timer", name="spento")
    generate_project(project, tmp_path / "a")
    assert "timer_create" not in (tmp_path / "a" / "main.py").read_text()
    project.widgets[0].props["enabled"] = False
    _name, handler = project.ensure_handler("spento")
    handler.body = "print(1)\n"
    generate_project(project, tmp_path / "b")
    assert "ui.spento.pause()" in (tmp_path / "b" / "main.py").read_text()


def test_board_gets_buzzer_from_profile(tmp_path):
    project = component_project()
    profiles = {profile["id"]: profile for profile in builtin_profiles()}
    project.set_display_size(240, 240)
    project.board = profiles["waveshare_rp2350_touch_lcd_4_240"]
    result = generate_board(project, project.board, tmp_path / "rp")
    assert "PIN = 1" in (tmp_path / "rp" / "lms_buzzer.py").read_text()
    assert "ui.timer1 = lv.timer_create" in (tmp_path / "rp" / "app_main.py").read_text()
    assert not any("buzzer" in warning for warning in result["warnings"])
    project.set_display_size(1024, 600)
    project.board = profiles["stm32h7_core_v1_3_1024x600"]
    result = generate_board(project, project.board, tmp_path / "stm")
    assert "PIN" not in (tmp_path / "stm" / "lms_buzzer.py").read_text()
    assert any("buzzer" in warning for warning in result["warnings"])


def test_c_target_ignores_components_with_warning(tmp_path):
    result = generate_c(component_project(), tmp_path)
    assert any("buzzer1" in warning for warning in result["warnings"])
    assert "timer1" not in (tmp_path / "ui.c").read_text()
    assert "timer1_tick" not in (tmp_path / "ui_events.c").read_text()


def test_old_project_profile_still_gets_the_board_buzzer(tmp_path):
    project = component_project()
    profile = next(item for item in builtin_profiles() if item["id"] == "esp32_4848s040_480")
    profile.pop("buzzer")
    project.set_display_size(480, 480)
    project.board = profile
    result = generate_board(project, project.board, tmp_path)
    assert "import audio" in (tmp_path / "lms_buzzer.py").read_text()
    assert not any("buzzer" in warning for warning in result["warnings"])
