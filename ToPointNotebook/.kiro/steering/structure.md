# Project Structure & Organization

## Repository Structure

```
ToPointNotebook/
├── encrypted_notebook.py         # Main application (single file)
├── main.py                       # Entry point wrapper
├── requirements.txt              # Python dependencies (PyQt6, cryptography)
├── README.md                     # Documentation and setup instructions
├── .gitignore                    # Git ignore rules
├── .venv/                        # Virtual environment (not committed)
├── packaging/                    # Platform-specific build configs
│   ├── windows/                  # PyInstaller -> .exe
│   └── linux/                    # AppImage build
└── .kiro/                        # IDE configuration
    ├── specs/encrypted-notebook/ # Feature specification
    │   ├── requirements.md
    │   ├── design.md
    │   ├── tasks.md
    │   └── .config.kiro
    └── steering/                 # Project guidance
        ├── product.md
        ├── tech.md
        ├── structure.md
        ├── development.md
        └── packaging.md
```

## Application Architecture

### Single-File Design
All application code lives in `encrypted_notebook.py`:

```python
# Module-level functions
derive_key()          # Argon2id key derivation
encrypt_bytes()       # AES-256-GCM encryption
decrypt_bytes()       # AES-256-GCM decryption
notes_to_json()       # Serialize notes to JSON
json_to_notes()       # Deserialize JSON to notes
save_to_file()        # Encrypt and write to disk
load_from_file()      # Read and decrypt from disk

# Theme constants
LIGHT_THEME           # Apple-inspired light stylesheet
DARK_THEME            # Catppuccin Mocha dark stylesheet

# Classes
class NoteFormat      # Enum: TEXT, MARKDOWN
class Note            # Dataclass: id, title, content, fmt, timestamps
class PasswordDialog  # QDialog for password entry
class EncryptedNotebook(QMainWindow)  # Main application window
```

### Data Flow
1. User enters password -> Argon2id derives AES-256 key
2. Notes stored as JSON -> encrypted with AES-256-GCM -> written to `.enc` file
3. On load: read `.enc` -> decrypt -> parse JSON -> populate UI
4. Every create/edit/delete persists immediately to disk

## Naming Conventions
- **Classes**: PascalCase (e.g., `EncryptedNotebook`, `PasswordDialog`)
- **Functions**: snake_case (e.g., `derive_key`, `save_to_file`)
- **Private methods**: _prefixed snake_case (e.g., `_on_new_note`, `_persist`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `SALT_SIZE`, `LIGHT_THEME`)
