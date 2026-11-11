from pathlib import Path
import tomllib

from lvgl_mpy_studio.core.boards import builtin_profiles
from lvgl_mpy_studio.core.model import Project
from lvgl_mpy_studio.gen.board_gen import generate_board
from lvgl_mpy_studio.gen.project_gen import generate_project

ROOT = Path(__file__).parents[1]
NOTICE = "SPDX-License-Identifier: MIT"


def test_ide_license_is_the_full_gpl_text():
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "GNU GENERAL PUBLIC LICENSE" in text and "Version 3, 29 June 2007" in text
    assert "END OF TERMS AND CONDITIONS" in text


def test_project_metadata_declares_both_licenses():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert project["license"] == "GPL-3.0-or-later AND MIT"
    assert all((ROOT / name).exists() for name in project["license-files"])


def test_every_embedded_source_declares_mit():
    embedded = [*(ROOT / "native/lvsim").glob("*.[ch]"), *(ROOT / "lvgl_mpy_studio/gen/output").glob("*.py"), ROOT / "runtime/display_driver.py"]
    assert len(embedded) >= 12
    assert not [path for path in embedded if NOTICE not in path.read_text(encoding="utf-8")]


def buzzer_project():
    project = Project("licenza")
    project.set_display_size(240, 240)
    project.add_widget(project.pages[0], "buzzer", name="buzzer1")
    return project


def test_files_copied_into_a_project_keep_the_notice(tmp_path):
    generate_project(buzzer_project(), tmp_path)
    assert NOTICE in (tmp_path / "display_driver.py").read_text(encoding="utf-8")
    assert NOTICE in (tmp_path / "lms_buzzer.py").read_text(encoding="utf-8")


def test_board_buzzer_keeps_the_notice(tmp_path):
    project = buzzer_project()
    project.board = builtin_profiles()[0]
    generate_board(project, project.board, tmp_path)
    assert NOTICE in (tmp_path / "lms_buzzer.py").read_text(encoding="utf-8")


def test_third_party_license_texts_are_shipped():
    embedded = {path.name: path.read_text(encoding="utf-8") for path in (ROOT / "lvgl_mpy_studio/gen/output/licenses").iterdir()}
    assert set(embedded) == {"LVGL.txt", "MicroPython.txt", "SDL2.txt", "lvgl-bindings.txt", "lvgl-micropython.txt"}
    assert all(len(text) > 500 for text in embedded.values())
    packaged = {path.name for path in (ROOT / "packaging/licenses").iterdir()}
    assert packaged == {"LGPL-2.1.txt", "LGPL-3.0.txt", "MaterialDesignIcons.txt", "Python-PSF.txt", "QtAwesome.txt", "QtPy.txt", "pyserial.txt"}


def test_packages_include_the_license_folders():
    for name in ("lvgl-mpy-studio.spec", "lvgl-mpy-studio-windows.spec"):
        spec = (ROOT / "packaging" / name).read_text(encoding="utf-8")
        assert "packaging/licenses" in spec and "lvgl_mpy_studio/gen/output/licenses" in spec and "LICENSE" in spec


def test_packages_carry_only_the_licensed_icon_font():
    for name in ("lvgl-mpy-studio.spec", "lvgl-mpy-studio-windows.spec"):
        spec = (ROOT / "packaging" / name).read_text(encoding="utf-8")
        assert '"materialdesignicons6" in item[0]' in spec and "analysis.datas = " in spec
    portable = (ROOT / "packaging/build_windows_portable.sh").read_text(encoding="utf-8")
    assert "qtawesome==1.4.2" in portable and "! -name 'materialdesignicons6*' -delete" in portable
    assert "Pictogrammers Free License" in (ROOT / "packaging/licenses/MaterialDesignIcons.txt").read_text(encoding="utf-8")


def test_packages_keep_the_lvgl_license_but_not_its_tests():
    for name in ("lvgl-mpy-studio.spec", "lvgl-mpy-studio-windows.spec"):
        spec = (ROOT / "packaging" / name).read_text(encoding="utf-8")
        assert '"LICENCE.txt"' in spec and '"COPYRIGHTS.md"' in spec
        assert 'lvgl-bindings/lvgl"), ".reference' not in spec
