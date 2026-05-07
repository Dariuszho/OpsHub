# ToPoint Notebook - Windows Package

## Prerequisites

- Python 3.10+
- PyQt6 and cryptography installed
- PyInstaller (`pip install pyinstaller`)

## Build

```cmd
cd packaging\windows
build.bat
```

## Output

`dist/ToPointNotebook.exe` - standalone executable, no Python needed on target machine.

## Distribution

Copy `ToPointNotebook.exe` to any Windows machine and run it. No installation required.
