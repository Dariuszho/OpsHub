# Design Document: Encrypted Notebook Application

## Overview

The Encrypted Notebook is a privacy-focused desktop application that provides secure, self-custody management of text and markdown notes. Built as a single Python file using PyQt6/PySide6, the application stores all user data in a single encrypted file, ensuring complete user control over their information without reliance on external services.

### Key Design Principles

- **Privacy First**: All data remains under user control with no network transmission
- **Security by Design**: Industry-standard AES-256 encryption with secure key derivation
- **Simplicity**: Single-file architecture for easy deployment and maintenance
- **Internationalization**: Full Unicode support with bidirectional text handling for RTL languages
- **Cross-Platform**: Native desktop experience on Windows, Linux, and macOS

## Architecture

### High-Level Architecture

The application follows a component-based architecture within a single Python file, with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    NotebookApp (Main GUI)                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Editor    │  │ FileManager │  │    I18nEngine       │  │
│  │             │  │             │  │                     │  │
│  │ - Text Edit │  │ - Import    │  │ - RTL Support       │  │
│  │ - Markdown  │  │ - Export    │  │ - Unicode Handling  │  │
│  │ - Search    │  │ - Encoding  │  │ - Text Direction    │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌─────────────────────────────┐   │
│  │   EncryptionEngine  │  │        DataStore            │   │
│  │                     │  │                             │   │
│  │ - AES-256 Crypto    │  │ - Encrypted File Storage    │   │
│  │ - Key Derivation    │  │ - Backup Management         │   │
│  │ - Memory Security   │  │ - Data Integrity            │   │
│  └─────────────────────┘  └─────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **GUI Framework**: PyQt6/PySide6 for advanced internationalization support
- **Encryption**: `cryptography` library with AES-256-GCM
- **Key Derivation**: Argon2id for password-based key derivation
- **Text Processing**: Python's built-in Unicode support with PyQt6's bidirectional text handling
- **File Handling**: `pathlib` for cross-platform file operations

## Components and Interfaces

### EncryptionEngine

**Purpose**: Handles all cryptographic operations with security-first design.

**Key Responsibilities**:
- AES-256-GCM encryption/decryption for authenticated encryption
- Argon2id key derivation with configurable parameters
- Secure random salt and IV generation
- Memory clearing for sensitive data
- Data integrity verification

**Interface**:
```python
class EncryptionEngine:
    def derive_key(self, password: str, salt: bytes) -> bytes
    def encrypt_data(self, data: bytes, key: bytes) -> EncryptedData
    def decrypt_data(self, encrypted_data: EncryptedData, key: bytes) -> bytes
    def generate_salt(self) -> bytes
    def clear_memory(self, sensitive_data: bytearray) -> None
    def verify_integrity(self, data: bytes, expected_hash: bytes) -> bool
```

**Security Features**:
- Uses `secrets` module for cryptographically secure random generation
- Implements constant-time comparison for authentication
- Clears sensitive data from memory using `memoryview` and explicit zeroing
- Configurable Argon2id parameters (memory cost, time cost, parallelism)

### DataStore

**Purpose**: Manages the single encrypted file containing all notes and metadata.

**Key Responsibilities**:
- Single encrypted file format with versioning
- Note storage with metadata (title, creation date, modification date, tags)
- Automatic backup creation with configurable intervals
- Data corruption detection and recovery
- Atomic write operations to prevent data loss

**Interface**:
```python
class DataStore:
    def load_data(self, file_path: Path, password: str) -> NotebookData
    def save_data(self, data: NotebookData, file_path: Path, password: str) -> None
    def create_backup(self, backup_path: Path) -> None
    def restore_from_backup(self, backup_path: Path, password: str) -> NotebookData
    def verify_integrity(self, file_path: Path) -> bool
    def migrate_data_format(self, old_data: dict) -> NotebookData
```

**File Format**:
```
Encrypted File Structure:
┌─────────────────────────────────────────────────────────┐
│ Header (32 bytes)                                       │
│ - Magic Number (4 bytes): "ENCN"                        │
│ - Version (4 bytes): Format version                     │
│ - Salt (16 bytes): For key derivation                   │
│ - Reserved (8 bytes): Future use                        │
├─────────────────────────────────────────────────────────┤
│ Encrypted Payload                                       │
│ - IV (12 bytes): AES-GCM initialization vector         │
│ - Encrypted Data: JSON-serialized notebook data        │
│ - Authentication Tag (16 bytes): GCM authentication    │
└─────────────────────────────────────────────────────────┘
```

### FileManager

**Purpose**: Handles import and export of individual text and markdown files.

**Key Responsibilities**:
- Import text/markdown files with encoding detection
- Export notes to standalone files preserving format
- Batch import operations with progress tracking
- Format preservation and metadata handling
- Unicode normalization and encoding management

**Interface**:
```python
class FileManager:
    def import_file(self, file_path: Path) -> Note
    def import_multiple_files(self, file_paths: List[Path]) -> List[Note]
    def export_note(self, note: Note, file_path: Path) -> None
    def detect_encoding(self, file_path: Path) -> str
    def preserve_format(self, content: str, original_format: str) -> str
    def normalize_unicode(self, text: str) -> str
```

**Encoding Support**:
- UTF-8 (primary)
- UTF-16 with BOM detection
- Latin-1 fallback for legacy files
- Automatic encoding detection using `chardet` library
- Unicode normalization (NFC) for consistent storage

### Editor

**Purpose**: Provides the main text editing interface with full internationalization support.

**Key Responsibilities**:
- Rich text editing with PyQt6's QTextEdit
- Markdown syntax highlighting with RTL awareness
- Bidirectional text support for mixed LTR/RTL content
- Auto-save functionality with configurable intervals
- Search and replace with multi-language support
- Undo/redo operations with proper text direction handling

**Interface**:
```python
class Editor(QTextEdit):
    def setup_rtl_support(self) -> None
    def detect_text_direction(self, text: str) -> Qt.LayoutDirection
    def apply_syntax_highlighting(self, format_type: str) -> None
    def setup_auto_save(self, interval_seconds: int) -> None
    def search_text(self, query: str, options: SearchOptions) -> List[SearchResult]
    def insert_text_with_direction(self, text: str, direction: Qt.LayoutDirection) -> None
```

**RTL Language Support**:
- Automatic text direction detection using Unicode bidirectional algorithm
- Proper cursor movement in RTL text (visual vs. logical order)
- Context-sensitive text alignment (right-align for RTL paragraphs)
- Support for complex scripts (Arabic, Hebrew, Persian, Urdu)
- Font fallback system for missing glyphs
- Input method integration for complex text input

### I18nEngine

**Purpose**: Comprehensive internationalization support with focus on RTL languages.

**Key Responsibilities**:
- Bidirectional text algorithm implementation
- Unicode text shaping and normalization
- Font management with fallback support
- Keyboard layout and input method integration
- Text direction detection and cursor management
- Language-specific text processing

**Interface**:
```python
class I18nEngine:
    def detect_text_direction(self, text: str) -> TextDirection
    def shape_text(self, text: str, language: str) -> ShapedText
    def get_font_for_script(self, script: str) -> QFont
    def setup_input_method(self, language: str) -> None
    def normalize_unicode(self, text: str, form: str = 'NFC') -> str
    def get_cursor_position(self, text: str, visual_pos: int) -> int
```

**Bidirectional Text Handling**:
- Implementation of Unicode Bidirectional Algorithm (UBA)
- Support for embedding levels and directional overrides
- Proper handling of neutral characters in mixed-direction text
- Visual-to-logical and logical-to-visual position mapping
- Context-sensitive punctuation and number handling

### NotebookApp

**Purpose**: Main application controller and GUI coordinator.

**Key Responsibilities**:
- Application lifecycle management (startup, shutdown, session handling)
- Main window layout with RTL-aware design
- Menu system with internationalized shortcuts
- User authentication and password management
- Auto-lock functionality with configurable timeout
- Theme management (light/dark mode)
- Settings persistence and configuration management

**Interface**:
```python
class NotebookApp(QMainWindow):
    def setup_ui(self) -> None
    def authenticate_user(self, password: str) -> bool
    def lock_application(self) -> None
    def unlock_application(self, password: str) -> bool
    def setup_auto_lock(self, timeout_minutes: int) -> None
    def apply_theme(self, theme: Theme) -> None
    def save_settings(self) -> None
    def load_settings(self) -> None
```

**GUI Layout**:
```
┌─────────────────────────────────────────────────────────────┐
│ Menu Bar (File, Edit, View, Tools, Help)                   │
├─────────────────────────────────────────────────────────────┤
│ Toolbar (New, Open, Save, Search, Lock)                    │
├─────────────────┬───────────────────────────────────────────┤
│ Note List       │ Editor Pane                               │
│                 │                                           │
│ ┌─────────────┐ │ ┌───────────────────────────────────────┐ │
│ │ Note 1      │ │ │ # Markdown Content                    │ │
│ │ Note 2      │ │ │                                       │ │
│ │ Note 3      │ │ │ This is **bold** text in English.    │ │
│ │ ...         │ │ │                                       │ │
│ └─────────────┘ │ │ هذا نص **عريض** باللغة العربية.        │ │
│                 │ │                                       │ │
│ Search: [____]  │ │ Mixed LTR and RTL text handling.      │ │
│                 │ └───────────────────────────────────────┘ │
├─────────────────┴───────────────────────────────────────────┤
│ Status Bar (Note count, word count, encryption status)     │
└─────────────────────────────────────────────────────────────┘
```

## Data Models

### Core Data Structures

**Note Model**:
```python
@dataclass
class Note:
    id: str                    # UUID4 identifier
    title: str                 # Note title (supports Unicode)
    content: str               # Note content (supports RTL/LTR)
    format: NoteFormat         # TEXT or MARKDOWN
    created_at: datetime       # Creation timestamp
    modified_at: datetime      # Last modification timestamp
    tags: List[str]           # User-defined tags
    language: Optional[str]    # Detected/specified language code
    text_direction: TextDirection  # LTR, RTL, or AUTO
    metadata: Dict[str, Any]   # Extensible metadata
```

**NotebookData Model**:
```python
@dataclass
class NotebookData:
    version: str               # Data format version
    notes: Dict[str, Note]     # Notes indexed by ID
    settings: UserSettings     # User preferences
    created_at: datetime       # Notebook creation time
    last_backup: Optional[datetime]  # Last backup timestamp
    integrity_hash: str        # Data integrity verification
```

**UserSettings Model**:
```python
@dataclass
class UserSettings:
    auto_save_interval: int    # Auto-save interval in seconds
    auto_lock_timeout: int     # Auto-lock timeout in minutes
    backup_interval: int       # Backup interval in hours
    theme: Theme              # UI theme (LIGHT, DARK, AUTO)
    default_language: str     # Default language code
    font_family: str          # Preferred font family
    font_size: int           # Font size in points
    rtl_support: bool        # Enable RTL language support
    spell_check: bool        # Enable spell checking
```

### Encryption Data Structures

**EncryptedData Model**:
```python
@dataclass
class EncryptedData:
    iv: bytes                 # Initialization vector (12 bytes)
    ciphertext: bytes         # Encrypted data
    tag: bytes               # Authentication tag (16 bytes)
    salt: bytes              # Key derivation salt (16 bytes)
    
    def to_bytes(self) -> bytes:
        """Serialize to binary format for storage."""
        
    @classmethod
    def from_bytes(cls, data: bytes) -> 'EncryptedData':
        """Deserialize from binary format."""
```

**KeyDerivationParams Model**:
```python
@dataclass
class KeyDerivationParams:
    algorithm: str = "argon2id"    # Key derivation algorithm
    memory_cost: int = 65536       # Memory cost in KB
    time_cost: int = 3             # Time cost (iterations)
    parallelism: int = 1           # Parallelism factor
    salt_length: int = 16          # Salt length in bytes
    key_length: int = 32           # Derived key length in bytes
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Single encrypted file storage
*For any* set of notes and metadata, when stored by the Encrypted_Notebook, all data should be contained within a single encrypted file.
**Validates: Requirements 1.1**

### Property 2: Successful decryption with correct password
*For any* encrypted data store and correct password, the Encryption_Engine should successfully decrypt and provide access to all stored data.
**Validates: Requirements 1.2**

### Property 3: Data persistence on application close
*For any* changes made during a session, when the application closes, all changes should be encrypted and persisted to the Data_Store.
**Validates: Requirements 1.3**

### Property 4: Authentication failure with incorrect password
*For any* encrypted data store and incorrect password, the Encryption_Engine should return an authentication error and deny access.
**Validates: Requirements 1.4**

### Property 5: Note creation and storage
*For any* valid note content (text or markdown), creating a new note should result in the note being stored and retrievable from the system.
**Validates: Requirements 2.1**

### Property 6: Note modification persistence
*For any* existing note and valid modifications, editing the note should result in the changes being persisted and retrievable.
**Validates: Requirements 2.2**

### Property 7: Note deletion removes access
*For any* existing note, when deleted, the note should no longer be accessible or appear in the note list.
**Validates: Requirements 2.3**

### Property 8: Note list completeness
*For any* set of created notes, the displayed note list should contain all notes with their correct titles.
**Validates: Requirements 2.4**

### Property 9: Unique note identifiers
*For any* number of notes created, each note should have a unique identifier that distinguishes it from all other notes.
**Validates: Requirements 2.5**

### Property 10: Format support preservation
*For any* note created in either plain text or markdown format, the system should preserve and correctly handle the specified format.
**Validates: Requirements 2.6**

### Property 11: File import creates notes
*For any* valid text or markdown file, importing the file should create a new note with the file's content.
**Validates: Requirements 3.1**

### Property 12: Note export preserves content
*For any* note, exporting it to a file should create a standalone file with identical content.
**Validates: Requirements 3.2**

### Property 13: Import-export format preservation
*For any* text or markdown file, importing then immediately exporting should preserve the original file format and content.
**Validates: Requirements 3.3**

### Property 14: Batch import creates separate notes
*For any* set of multiple files, importing them should create a separate note for each file.
**Validates: Requirements 3.4**

### Property 15: Encoding preservation during file operations
*For any* text file with specific encoding, importing and exporting should preserve the text content correctly regardless of encoding.
**Validates: Requirements 3.5**

### Property 16: Markdown syntax highlighting
*For any* markdown content in the editor, syntax elements should be visually highlighted according to markdown formatting rules.
**Validates: Requirements 4.1**

### Property 17: Text editing operations functionality
*For any* text content, all basic editing operations (cut, copy, paste, undo, redo) should work correctly and preserve text integrity.
**Validates: Requirements 4.2**

### Property 18: Search functionality accuracy
*For any* search query and existing notes, the search should return all notes that contain the query in their title or content.
**Validates: Requirements 4.4**

### Property 19: Auto-save prevents data loss
*For any* changes made in the editor, the auto-save mechanism should persist changes within the configured interval.
**Validates: Requirements 4.6**

### Property 20: Password security in storage
*For any* user password, the system should never store the password in plain text in memory or persistent storage.
**Validates: Requirements 5.1**

### Property 21: Auto-lock timeout functionality
*For any* configured timeout period, when the application is idle for that duration, it should automatically lock and require re-authentication.
**Validates: Requirements 5.3**

### Property 22: Memory clearing on lock
*For any* sensitive data in memory, when the application locks, all sensitive data should be cleared from memory.
**Validates: Requirements 5.4**

### Property 23: Encrypted data randomness
*For any* encrypted data store, the encrypted content should be statistically indistinguishable from random data.
**Validates: Requirements 5.5**

### Property 24: Network isolation
*For any* application operation, no user data should be transmitted over any network connection.
**Validates: Requirements 5.6**

### Property 25: Data integrity verification
*For any* encrypted data store, when decrypting, the system should verify data integrity and detect any corruption.
**Validates: Requirements 6.1**

### Property 26: Corruption detection and recovery
*For any* detected data corruption, the system should alert the user and attempt recovery from available backups.
**Validates: Requirements 6.2**

### Property 27: Automatic backup creation
*For any* configured backup interval, the system should automatically create backups of the Data_Store at the specified intervals.
**Validates: Requirements 6.3**

### Property 28: Manual backup functionality
*For any* user request, the system should allow manual creation of backups and verify their successful creation.
**Validates: Requirements 6.4**

### Property 29: Backup integrity verification
*For any* backup restoration attempt, the system should verify the backup's integrity before proceeding with restoration.
**Validates: Requirements 6.5**

### Property 30: Backup history maintenance
*For any* created backup, the system should maintain a record with accurate timestamps in the backup history.
**Validates: Requirements 6.6**

### Property 31: Unicode text support
*For any* Unicode text in any language, the editor should correctly input, display, and store the text without corruption.
**Validates: Requirements 7.1**

### Property 32: RTL language handling
*For any* right-to-left language text (Hebrew, Arabic, Persian, Urdu), the editor should properly render and handle input with correct directionality.
**Validates: Requirements 7.2**

### Property 33: Automatic text direction detection
*For any* text input, the editor should automatically detect the text direction and apply appropriate alignment.
**Validates: Requirements 7.3**

### Property 34: Bidirectional text support
*For any* note containing mixed LTR and RTL content, the editor should correctly render and handle both directions within the same document.
**Validates: Requirements 7.4**

### Property 35: Complex script rendering
*For any* text in languages with ligatures and contextual forms, the editor should render the text with proper character shaping and connections.
**Validates: Requirements 7.5**

### Property 36: Text direction preservation in file operations
*For any* file with specific text direction and encoding, importing then exporting should preserve both the encoding and text direction.
**Validates: Requirements 7.6**

### Property 37: Input method support
*For any* language-specific keyboard layout or input method, the system should correctly handle text input and character composition.
**Validates: Requirements 7.7**

### Property 38: RTL cursor and selection behavior
*For any* RTL text, cursor movement and text selection should follow the visual and logical order appropriate for the text direction.
**Validates: Requirements 7.8**

### Property 39: Multi-language search functionality
*For any* search query in any language (including RTL), the search should correctly find and return matching content regardless of text direction.
**Validates: Requirements 7.9**

### Property 40: Multi-language metadata round-trip
*For any* note metadata (titles, tags) in any language, storing and retrieving should preserve the content and language characteristics.
**Validates: Requirements 7.10**

### Property 41: New data store creation
*For any* system startup with no existing Data_Store, the system should create a new encrypted file and initialize it properly.
**Validates: Requirements 8.2**

### Property 42: Automatic backup recovery
*For any* corrupted Data_Store with available backups, the system should automatically attempt restoration from the most recent valid backup.
**Validates: Requirements 8.3**

### Property 43: Crash recovery without data loss
*For any* application crash or unexpected termination, previously saved data should remain intact and accessible upon restart.
**Validates: Requirements 8.4**

### Property 44: Password change re-encryption
*For any* password change operation, the system should re-encrypt the entire Data_Store with the new password while preserving all data.
**Validates: Requirements 8.5**

## Error Handling

### Encryption and Security Errors

**Authentication Failures**:
- Invalid password attempts should be logged with rate limiting to prevent brute force attacks
- After multiple failed attempts, implement exponential backoff delays
- Clear error messages without revealing information about the data structure

**Data Corruption Handling**:
- Implement multiple layers of integrity checking (file-level, data-level, note-level)
- Graceful degradation when partial corruption is detected
- Automatic backup restoration with user confirmation
- Detailed error reporting for forensic analysis

**Memory Security**:
- Secure memory allocation for sensitive data using `mlock()` where available
- Explicit memory clearing using `memset()` or equivalent
- Protection against memory dumps and swap file exposure
- Garbage collection considerations for Python objects containing sensitive data

### File System Errors

**File Access Issues**:
- Handle permission errors with clear user guidance
- Detect and handle file locking conflicts
- Graceful handling of disk space limitations
- Cross-platform path handling and character encoding issues

**Import/Export Errors**:
- Encoding detection failures with fallback strategies
- Large file handling with progress indication and cancellation
- Network drive and cloud storage synchronization conflicts
- File format validation and sanitization

### Internationalization Errors

**Text Rendering Issues**:
- Missing font fallback strategies for unsupported scripts
- Complex script shaping failures with graceful degradation
- Bidirectional text algorithm edge cases
- Input method integration failures

**Encoding Problems**:
- Unicode normalization conflicts
- Byte order mark (BOM) handling
- Legacy encoding conversion errors
- Character set detection ambiguities

### Application Lifecycle Errors

**Startup Failures**:
- Configuration file corruption recovery
- Missing dependency detection and user guidance
- Platform-specific initialization failures
- First-run setup error handling

**Runtime Errors**:
- Auto-save failure recovery with user notification
- Search index corruption and rebuilding
- Theme and UI state restoration failures
- Plugin or extension loading errors (future extensibility)

## Testing Strategy

### Dual Testing Approach

The testing strategy employs both unit testing and property-based testing to ensure comprehensive coverage:

**Unit Testing Focus**:
- Specific examples demonstrating correct behavior
- Edge cases and boundary conditions
- Error conditions and exception handling
- Integration points between components
- Platform-specific functionality verification

**Property-Based Testing Focus**:
- Universal properties that hold for all inputs
- Comprehensive input coverage through randomization
- Cryptographic property verification
- Text processing correctness across languages
- Data integrity and round-trip properties

### Property-Based Testing Configuration

**Testing Framework**: `hypothesis` for Python property-based testing
**Minimum Iterations**: 100 iterations per property test
**Test Tagging**: Each property test must reference its design document property using the format:
`# Feature: encrypted-notebook, Property {number}: {property_text}`

**Example Property Test Structure**:
```python
from hypothesis import given, strategies as st
import pytest

@given(st.text(min_size=1, max_size=1000))
def test_note_creation_and_retrieval(content):
    """Feature: encrypted-notebook, Property 5: Note creation and storage"""
    # Test that any valid content can be stored and retrieved
    note = create_note(content)
    retrieved_note = get_note(note.id)
    assert retrieved_note.content == content
    assert retrieved_note.id == note.id
```

### Unit Testing Strategy

**Cryptographic Testing**:
- Test vectors for AES-256-GCM encryption/decryption
- Key derivation function parameter validation
- Salt and IV uniqueness verification
- Authentication tag validation
- Memory clearing verification

**File Operations Testing**:
- Import/export with various file encodings (UTF-8, UTF-16, Latin-1)
- Large file handling and memory efficiency
- Concurrent file access scenarios
- Cross-platform path handling

**Internationalization Testing**:
- RTL language rendering with specific test cases (Arabic, Hebrew, Persian)
- Bidirectional text with mixed content
- Complex script ligature handling (Arabic, Devanagari)
- Input method integration testing
- Font fallback verification

**GUI Testing**:
- Automated UI testing using PyQt6's testing framework
- Keyboard shortcut functionality across different layouts
- Theme switching and persistence
- Window state management and restoration
- Accessibility compliance testing

### Integration Testing

**End-to-End Workflows**:
- Complete application lifecycle (startup, use, shutdown)
- Password change and data re-encryption
- Backup creation and restoration
- Import multiple files and export workflow
- Auto-lock and unlock scenarios

**Cross-Platform Testing**:
- Windows primary development environment testing
- Linux distribution testing (Ubuntu, Fedora, Arch)
- macOS testing with different versions
- Font rendering consistency across platforms
- File system permission handling

### Security Testing

**Cryptographic Validation**:
- Encryption algorithm compliance verification
- Key derivation parameter security analysis
- Random number generation quality testing
- Side-channel attack resistance evaluation
- Memory dump analysis for sensitive data leakage

**Penetration Testing**:
- File format fuzzing for corruption resistance
- Password brute force protection testing
- Memory exhaustion and resource limit testing
- Timing attack resistance verification
- Data recovery attempt simulation

### Performance Testing

**Scalability Testing**:
- Large notebook performance (1000+ notes)
- Search performance with extensive content
- Startup time with large encrypted files
- Memory usage optimization verification
- Auto-save performance impact measurement

**Responsiveness Testing**:
- GUI responsiveness during encryption operations
- Real-time text rendering performance
- File import/export progress indication
- Background operation handling
- Thread safety verification

### Test Data Management

**Synthetic Test Data**:
- Generated notes in multiple languages and scripts
- Various file formats and encodings for import testing
- Corrupted data scenarios for error handling testing
- Large datasets for performance testing
- Edge case content (empty notes, very long notes, special characters)

**Real-World Test Data**:
- Sample documents in RTL languages
- Mixed-direction text examples
- Complex script samples with ligatures
- Various markdown formatting examples
- Legacy file format samples for compatibility testing

This comprehensive testing strategy ensures that all requirements are thoroughly validated while maintaining the security and reliability standards expected for a privacy-focused application.