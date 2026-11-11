param(
    [switch]$SkipInstaller
)

$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Python = if ($env:PYTHON) { $env:PYTHON } else { "python" }

& $Python -m PyInstaller --noconfirm --clean --distpath "$Root/dist" --workpath "$Root/build/pyinstaller-windows" "$Root/packaging/lvgl-mpy-studio-windows.spec"
if ($LASTEXITCODE -ne 0) { throw "PyInstaller returned $LASTEXITCODE" }

$Version = & $Python -c "from lvgl_mpy_studio import __version__; print(__version__)"
$Archive = "$Root/dist/LVGL_MPY_STUDIO-$Version-win64.zip"
Remove-Item $Archive -Force -ErrorAction SilentlyContinue
Compress-Archive -Path "$Root/dist/LVGL_MPY_STUDIO" -DestinationPath $Archive -CompressionLevel Optimal

if (-not $SkipInstaller) {
    $Command = Get-Command ISCC.exe -ErrorAction SilentlyContinue
    $Compiler = if ($Command) { $Command.Source } else { "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" }
    if (-not (Test-Path $Compiler)) {
        throw "Inno Setup 6 not found. Install it or use -SkipInstaller to build only the ZIP."
    }
    & $Compiler "/DMyAppVersion=$Version" "$Root/packaging/lvgl-mpy-studio.iss"
    if ($LASTEXITCODE -ne 0) { throw "Inno Setup returned $LASTEXITCODE" }
}

Write-Host "Portable package: $Archive"
