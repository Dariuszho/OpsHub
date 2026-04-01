# Technology Stack & Build System

## Current Status
This project has a **working implementation**.

## Technology Stack

### Core Technologies
- **Language**: Python 3.10+
- **Platform**: Cross-platform desktop (Windows, Linux, macOS)
- **Architecture**: Single Python file (`encrypted_notebook.py`)
- **GUI Framework**: PyQt6

### Security & Encryption
- **Encryption**: AES-256-GCM (authenticated encryption via `cryptography` library)
- **Key Derivation**: Argon2id (64MB memory cost, 3 iterations)
- **Data Storage**: Single encrypted binary file (`.enc`)

### Dependencies
- `PyQt6>=6.4.0` - GUI framework
- `cryptography>=41.0.0` - AES-256-GCM and Argon2id

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# Or directly
python encrypted_notebook.py

# Create virtual environment (first time)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

## Cross-Platform Notes
- Uses `pathlib.Path` for all file operations
- Default notebook location: `~/notebook.enc`
- Linux may need: `sudo apt install libxcb-xinerama0 libxcb-cursor0`
