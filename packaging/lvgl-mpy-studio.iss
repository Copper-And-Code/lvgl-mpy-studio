#ifndef MyAppVersion
#define MyAppVersion "0.6.0"
#endif

[Setup]
LicenseFile=..\LICENSE
AppId={{7D653C2E-4AF5-4D5B-9C49-8C2AC98A3E10}
AppName=LVGL MPY Studio
AppVersion={#MyAppVersion}
AppPublisher=Nunzio Raciti
DefaultDirName={localappdata}\Programs\LVGL MPY Studio
DefaultGroupName=LVGL MPY Studio
PrivilegesRequired=lowest
OutputDir=..\dist
OutputBaseFilename=LVGL_MPY_STUDIO-{#MyAppVersion}-Setup-win64
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
SetupIconFile=..\lvgl_mpy_studio\icon.ico
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\LVGL_MPY_STUDIO.exe

[Files]
Source: "..\dist\LVGL_MPY_STUDIO\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\LVGL MPY Studio"; Filename: "{app}\LVGL_MPY_STUDIO.exe"
Name: "{group}\Disinstalla LVGL MPY Studio"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\LVGL_MPY_STUDIO.exe"; Description: "Avvia LVGL MPY Studio"; Flags: nowait postinstall skipifsilent
