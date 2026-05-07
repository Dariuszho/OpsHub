#!/bin/bash
# ToPoint Notebook - Linux AppImage Build Script
# Builds a portable .AppImage that runs on Debian, RedHat, and Arch families
# Run from this directory: ./build.sh

set -e

echo "=== ToPoint Notebook - Linux AppImage Build ==="

APP_NAME="ToPointNotebook"
APP_DIR="${APP_NAME}.AppDir"

# Check dependencies
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "Error: PyQt6 not installed. Run: pip install PyQt6"
    exit 1
fi

if ! python3 -c "import cryptography" 2>/dev/null; then
    echo "Error: cryptography not installed. Run: pip install cryptography"
    exit 1
fi

# Check/install PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# Clean previous build
rm -rf dist build "${APP_DIR}" *.spec "${APP_NAME}"*.AppImage

# Copy application file
cp ../../encrypted_notebook.py .

# Build with PyInstaller first (creates self-contained binary)
echo "Building binary with PyInstaller..."
pyinstaller --onefile --name "${APP_NAME}" encrypted_notebook.py

# Create AppDir structure
echo "Creating AppDir structure..."
mkdir -p "${APP_DIR}/usr/bin"
mkdir -p "${APP_DIR}/usr/share/applications"
mkdir -p "${APP_DIR}/usr/share/icons/hicolor/256x256/apps"

# Copy binary
cp "dist/${APP_NAME}" "${APP_DIR}/usr/bin/"

# Create desktop entry
cat > "${APP_DIR}/${APP_NAME}.desktop" << EOF
[Desktop Entry]
Type=Application
Name=ToPoint Notebook
Comment=Encrypted note-taking application
Exec=ToPointNotebook
Icon=topoint-notebook
Categories=Utility;TextEditor;
Terminal=false
EOF

# Copy desktop file to standard location too
cp "${APP_DIR}/${APP_NAME}.desktop" "${APP_DIR}/usr/share/applications/"

# Create a simple SVG icon
cat > "${APP_DIR}/topoint-notebook.svg" << 'SVGEOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect x="8" y="4" width="48" height="56" rx="4" fill="#1e1e2e" stroke="#89b4fa" stroke-width="2"/>
  <rect x="14" y="12" width="36" height="4" rx="2" fill="#89b4fa"/>
  <rect x="14" y="22" width="28" height="3" rx="1.5" fill="#45475a"/>
  <rect x="14" y="30" width="32" height="3" rx="1.5" fill="#45475a"/>
  <rect x="14" y="38" width="24" height="3" rx="1.5" fill="#45475a"/>
  <circle cx="48" cy="48" r="12" fill="#89b4fa"/>
  <rect x="45" y="42" width="6" height="12" rx="1" fill="#1e1e2e"/>
  <rect x="42" y="45" width="12" height="6" rx="1" fill="#1e1e2e"/>
</svg>
SVGEOF

# Copy icon to standard location
cp "${APP_DIR}/topoint-notebook.svg" "${APP_DIR}/usr/share/icons/hicolor/256x256/apps/"

# Create AppRun
cat > "${APP_DIR}/AppRun" << 'RUNEOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
exec "${HERE}/usr/bin/ToPointNotebook" "$@"
RUNEOF
chmod +x "${APP_DIR}/AppRun"

# Download appimagetool if not present
if [ ! -f appimagetool ]; then
    echo "Downloading appimagetool..."
    ARCH=$(uname -m)
    wget -q "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-${ARCH}.AppImage" -O appimagetool
    chmod +x appimagetool
fi

# Build AppImage
echo "Building AppImage..."
ARCH=$(uname -m) ./appimagetool "${APP_DIR}" "${APP_NAME}-${ARCH}.AppImage"

# Cleanup
rm -rf dist build *.spec "${APP_DIR}" encrypted_notebook.py

ARCH=$(uname -m)
APPIMAGE_FILE="${APP_NAME}-${ARCH}.AppImage"
if [ -n "$APPIMAGE_FILE" ]; then
    echo ""
    echo "=== Build successful ==="
    echo "Output: ${APPIMAGE_FILE}"
    echo ""
    echo "To run: chmod +x ${APPIMAGE_FILE} && ./${APPIMAGE_FILE}"
else
    echo ""
    echo "=== Build FAILED ==="
fi
