# ToPoint Notebook

A privacy-focused desktop application for managing text and markdown notes with strong encryption. All notes are stored in a single encrypted file under your control. No cloud, no tracking, no network access.

## Features

- **AES-256-GCM encryption** with Argon2id key derivation
- **Create, edit, and delete** text and markdown notes
- **Import/export** individual `.txt` and `.md` files
- **Markdown preview** with basic formatting support (Ctrl+P)
- **Full-text search** across all notes
- **Dark/light theme** toggle (Ctrl+T)
- **Auto-save** on close and lock
- **Lock/unlock** with password (Ctrl+L)
- **Single encrypted file** storage (`notebook.enc`)
- **Cross-platform** - works on Windows, Linux, and macOS

> **Note:** Standalone executables for Windows (.exe) and Linux (.AppImage) are provided unsigned and without certificates. Code signing and certification is optional and left to the end user or distributor to apply as needed.

## Requirements

- Python 3.10 or higher
- PyQt6
- cryptography

## Setup

### Windows

```powershell
# Clone the repository
git clone <repo-url>
cd ToPointNotebook

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Linux / macOS

```bash
# Clone the repository
git clone <repo-url>
cd ToPointNotebook

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 main.py
```

> **Note (Linux):** You may need to install Qt6 system libraries.
> 
> Ubuntu/Debian:
> ```bash
> sudo apt install libxcb-xinerama0 libxcb-cursor0
> ```
> 
> CentOS/Fedora:
> ```bash
> sudo dnf install libxcb xcb-util-cursor xcb-util-wm xcb-util-image xcb-util-keysyms
> ```

## Usage

### First Launch

1. Run the application
2. Set a password for your new notebook
3. Your encrypted notebook file is saved at `~/notebook.enc`

### Subsequent Launches

1. Run the application
2. Enter your password to unlock
3. Your notes are loaded from `~/notebook.enc`

### Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| Ctrl+N | New note |
| Ctrl+S | Save notebook |
| Ctrl+Shift+S | Save notebook as... |
| Ctrl+O | Open notebook |
| Ctrl+F | Search notes |
| Ctrl+L | Lock application |
| Ctrl+T | Toggle dark/light theme |
| Ctrl+P | Preview markdown |
| Ctrl+Q | Exit |

### Menu Functions

- **File > New Note** - Create a new note with a custom title
- **File > Open Notebook** - Open a different `.enc` notebook file
- **File > Save Notebook** - Save all notes to the encrypted file
- **File > Save Notebook As** - Save to a new file location
- **File > Import File** - Import a `.txt` or `.md` file as a new note
- **File > Export Note** - Export the current note to a file
- **File > Lock** - Lock the application (clears memory)
- **Edit > Find** - Focus the search bar
- **Edit > Delete Note** - Delete the current note
- **View > Toggle Theme** - Switch between light and dark mode
- **View > Preview Markdown** - Preview current note as rendered markdown

## Security

- **Encryption:** AES-256-GCM (authenticated encryption)
- **Key derivation:** Argon2id with 64MB memory cost
- **Storage:** Single encrypted binary file
- **No plaintext:** Notes are never stored unencrypted on disk
- **Auto-save on lock:** Data is persisted before clearing memory
- **Local only:** No network access, no telemetry, no cloud

## Project Structure

```
ToPointNotebook/
├── encrypted_notebook.py         # Main application (single file)
├── main.py                       # Entry point
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .gitignore                    # Git ignore rules
├── .venv/                        # Virtual environment (not committed)
└── .kiro/                        # IDE configuration and specs
    ├── specs/                    # Feature specifications
    └── steering/                 # Project guidance documents
```

## License

Private project. All rights reserved.
