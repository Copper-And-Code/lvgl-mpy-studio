import ast
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_windows_packaging_configuration():
    spec = ROOT / "packaging/lvgl-mpy-studio-windows.spec"
    ast.parse(spec.read_text(encoding="utf-8"), filename=str(spec))
    source = spec.read_text(encoding="utf-8")
    for name in ("lvsim-runtime.exe", "lvsim-standalone.exe", "mpy-cross.exe", "SDL2.dll", "liblvgl.a"):
        assert name in source
    assert 'name="LVGL_MPY_STUDIO", console=False' in source
    assert "COLLECT(" in source
    assert "THIRD_PARTY.md" in source


def test_windows_installer_is_per_user():
    source = (ROOT / "packaging/lvgl-mpy-studio.iss").read_text(encoding="utf-8")
    assert "PrivilegesRequired=lowest" in source
    assert "DefaultDirName={localappdata}" in source
    assert 'OutputBaseFilename=LVGL_MPY_STUDIO-{#MyAppVersion}-Setup-win64' in source
    assert 'Source: "..\\dist\\LVGL_MPY_STUDIO\\*"' in source


def test_windows_build_produces_zip_and_installer():
    source = (ROOT / "packaging/build_windows.ps1").read_text(encoding="utf-8")
    assert "Compress-Archive" in source
    assert "ISCC.exe" in source
    assert "lvgl-mpy-studio-windows.spec" in source


def test_windows_portable_bundles_msvc_runtime():
    source = (ROOT / "packaging/build_windows_portable.sh").read_text(encoding="utf-8")
    assert "vc_redist.x64.exe" in source
    assert "cabextract" in source
    assert "msvcp140.dll_amd64" in source
    assert '"$VC_RUNTIME"/*.dll_amd64' in source
    assert '"$OUT/python/$name"' in source
