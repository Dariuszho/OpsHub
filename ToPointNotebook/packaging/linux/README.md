# ToPoint Notebook - Linux AppImage Build

## What is AppImage?

A portable Linux application format. One `.AppImage` file runs on all major distro
families without installation. Download, make executable, double-click.

## Build Instructions

### Step 1: Install system dependencies

#### Ubuntu / Debian
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip wget fuse libxcb-xinerama0 libxcb-cursor0
```

#### Fedora / CentOS / RHEL
```bash
sudo dnf install python3 python3-pip wget fuse xcb-util-cursor xcb-util-wm xcb-util-image xcb-util-keysyms
```

#### Arch / Manjaro
```bash
sudo pacman -S python python-pip wget fuse2 xcb-util-cursor xcb-util-wm xcb-util-image xcb-util-keysyms
```

### Step 2: Clone the repository
```bash
git clone <repo-url>
cd ToPointNotebook
```

### Step 3: Create virtual environment and install Python dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install PyQt6 cryptography pyinstaller
```

### Step 4: Build the AppImage
```bash
cd packaging/linux
chmod +x build.sh
./build.sh
```

Build takes 1-3 minutes depending on your machine.

### Step 5: Verify the build
```bash
ls -la ToPointNotebook*.AppImage
```

If successful, you'll see `ToPointNotebook-x86_64.AppImage`.

## Running the AppImage

```bash
chmod +x ToPointNotebook-x86_64.AppImage
./ToPointNotebook-x86_64.AppImage
```

No Python, no pip, no dependencies needed on the target machine.

## Troubleshooting

### Build errors

The build script outputs errors directly to the terminal. To capture a log:
```bash
./build.sh 2>&1 | tee build.log
```
Check `build.log` for details if the build fails.

### Common issues

**"fuse: device not found"**
- Install FUSE: `sudo apt install fuse` (Ubuntu) / `sudo dnf install fuse` (Fedora) / `sudo pacman -S fuse2` (Arch)
- If in a VM or container: `sudo modprobe fuse`

**"No module named PyQt6"**
- Make sure the virtual environment is activated: `source .venv/bin/activate`
- Reinstall: `pip install PyQt6`

**"pyinstaller: command not found"**
- Make sure the virtual environment is activated: `source .venv/bin/activate`
- Reinstall: `pip install pyinstaller`

**AppImage runs but shows no window**
- Install xcb libraries for your distro (see Step 1)
- Try running from terminal to see error output: `./ToPointNotebook-x86_64.AppImage`

**"dlopen: libxcb-cursor.so.0: cannot open"**
- Ubuntu: `sudo apt install libxcb-cursor0`
- Fedora: `sudo dnf install xcb-util-cursor`
- Arch: `sudo pacman -S xcb-util-cursor`

## Desktop Integration

```bash
# Option 1: Copy to local bin
mkdir -p ~/.local/bin
cp ToPointNotebook-x86_64.AppImage ~/.local/bin/ToPointNotebook
chmod +x ~/.local/bin/ToPointNotebook

# Option 2: Use AppImageLauncher for full desktop integration
# https://github.com/TheAssassin/AppImageLauncher
```

## Notes

- Build must be done on Linux (cannot cross-build from Windows or WSL reliably)
- Build on Ubuntu 22.04 for maximum compatibility across all distro families
- The AppImage bundles Python, PyQt6, cryptography, and all dependencies inside
- appimagetool is downloaded automatically on first build
