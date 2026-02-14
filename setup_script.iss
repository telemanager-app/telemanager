[Setup]
AppName=TeleManager
AppVersion=1.0
AppPublisher=Eyuel Engida
DefaultDirName={userappdata}\TeleManager
DefaultGroupName=TeleManager
PrivilegesRequired=lowest
SetupIconFile={src}\appicon.ico
UninstallDisplayIcon={app}\TeleManager.exe
Compression=lzma2
SolidCompression=yes
OutputDir={src}
OutputBaseFilename=TeleManager_Setup
WizardStyle=modern

[Files]
; NOTE FOR DEVS: Place 'Telegram.exe' in a 'bin' folder next to this script before building
Source: "TeleManager.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "bin\Telegram.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "appicon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\profiles"

[Icons]
Name: "{autodesktop}\TeleManager"; Filename: "{app}\TeleManager.exe"; IconFilename: "{app}\appicon.ico"
Name: "{group}\TeleManager"; Filename: "{app}\TeleManager.exe"; IconFilename: "{app}\appicon.ico"

[Run]
Filename: "{app}\TeleManager.exe"; Description: "Launch TeleManager"; Flags: nowait postinstall skipifsilent