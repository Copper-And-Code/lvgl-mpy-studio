from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

root = Path(SPECPATH).parent
runtime = root / "runtime/out-win64"

datas = [
    (str(root / "lvgl_mpy_studio/gen/widgets.json"), "lvgl_mpy_studio/gen"),
    (str(root / "lvgl_mpy_studio/gen/completion.json"), "lvgl_mpy_studio/gen"),
    (str(root / "lvgl_mpy_studio/translations"), "lvgl_mpy_studio/translations"),
    (str(root / "lvgl_mpy_studio/boards"), "lvgl_mpy_studio/boards"),
    (str(root / "lvgl_mpy_studio/blocks"), "lvgl_mpy_studio/blocks"),
    (str(root / "lvgl_mpy_studio/icon.ico"), "lvgl_mpy_studio"),
    (str(root / "runtime/display_driver.py"), "runtime"),
    (str(root / "runtime/program"), "runtime/program"),  # programs without pages
    (str(root / "native/lvsim"), "native/lvsim"),
    # Only what is needed to build the C target: no tests, demos, documentation or scripts.
    (str(root / ".reference/lvgl-bindings/lvgl/src"), ".reference/lvgl-bindings/lvgl/src"),
    *[(str(root / ".reference/lvgl-bindings/lvgl" / name), ".reference/lvgl-bindings/lvgl") for name in ("lvgl.h", "lvgl_private.h", "lv_version.h", "LICENCE.txt", "COPYRIGHTS.md")],
    (str(root / ".reference/lvgl-bindings/lv_conf.h"), ".reference/lvgl-bindings"),
    (str(root / "docs/target.md"), "docs"),
    (str(root / "docs/boards.md"), "docs"),
    (str(root / "docs/boards.it.md"), "docs"),
    (str(root / "docs/windows-c.md"), "docs"),
    (str(root / "packaging/NOTICE.txt"), "share/doc/lvgl-mpy-studio"),
    (str(root / "LICENSE"), "share/doc/lvgl-mpy-studio"),
    (str(root / "LICENSE-MIT.txt"), "share/doc/lvgl-mpy-studio"),
    (str(root / "LICENSING.md"), "share/doc/lvgl-mpy-studio"),
    (str(root / "packaging/licenses"), "share/doc/lvgl-mpy-studio/licenses"),
    (str(root / "lvgl_mpy_studio/gen/output/licenses"), "lvgl_mpy_studio/gen/output/licenses"),
    (str(root / "THIRD_PARTY.md"), "share/doc/lvgl-mpy-studio"),
]
for name in ("lvsim-runtime.exe", "lvsim-standalone.exe", "lvsim-onefile.exe", "mpy-cross.exe", "SDL2.dll", "liblvgl.a"):
    datas.append((str(runtime / name), "runtime/out-win64"))
datas.append((str(root / "runtime/out/lvsim-onefile"), "runtime/out"))  # games for Linux built on Windows
datas += [(str(root / "runtime/out-web" / name), "runtime/out-web") for name in ("micropython.mjs", "micropython.wasm")]
datas.append((str(root / "runtime/web"), "runtime/web"))
for name in ("include", "lib"):
    datas.append((str(runtime / "SDL2" / name), f"runtime/out-win64/SDL2/{name}"))

analysis = Analysis(
    [str(root / "packaging/launcher.py")],
    pathex=[str(root)],
    binaries=[],
    datas=datas,
    hiddenimports=collect_submodules("mpremote") + collect_submodules("qtawesome"),
    hookspath=[],
    runtime_hooks=[],
    excludes=["pytest", "hypothesis"],
    noarchive=False,
)
# The PyInstaller hook adds every QtAwesome font: the others have different licences and are not needed.
analysis.datas = [item for item in analysis.datas if "qtawesome/fonts" not in item[0].replace("\\", "/") or "materialdesignicons6" in item[0]]
pyz = PYZ(analysis.pure)
exe = EXE(pyz, analysis.scripts, [], exclude_binaries=True, name="LVGL_MPY_STUDIO", console=False, icon=str(root / "lvgl_mpy_studio/icon.ico"))
collection = COLLECT(exe, analysis.binaries, analysis.datas, name="LVGL_MPY_STUDIO")
