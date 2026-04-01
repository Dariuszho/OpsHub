---
inclusion: manual
---

# Packaging

## Overview

Packaging configs live in `packaging/` with separate subdirectories per platform.
These are independent from the main application code. The build scripts copy
`encrypted_notebook.py` from the project root at build time.

```
packaging/
├── windows/          # PyInstaller -> .exe
│   ├── build.bat     # Build script
│   └── README.md     # Windows build instructions
└── linux/            # PyInstaller + AppImage -> .AppImage
    ├── build.sh      # Build script
    └── README.md     # Linux build instructions
```

## Windows (PyInstaller)

Produces a standalone `.exe` that runs without Python installed.

```cmd
cd packaging\windows
build.bat
```
Output: `packaging/windows/dist/ToPointNotebook.exe`

## Linux (AppImage)

Produces a portable `.AppImage` that runs on all major distro families
(Debian, RedHat, Arch) without any dependencies.

```bash
cd packaging/linux
chmod +x build.sh
./build.sh
```
Output: `packaging/linux/ToPointNotebook-x86_64.AppImage`

## Key Rules

- Build scripts copy `encrypted_notebook.py` from project root - never modify the source
- Each platform directory is self-contained and independently manageable
- Windows build must be done on Windows
- Linux build must be done on Linux
- Build on the oldest target distro for best Linux compatibility
- Test built packages on clean machines without Python installed

## Future Options

- **macOS**: PyInstaller with `--osx-bundle-identifier` for `.app` bundle
- **Windows installer**: Wrap `.exe` with Inno Setup or NSIS
- **Flatpak/Snap**: Alternative Linux packaging if AppImage doesn't cover a use case
