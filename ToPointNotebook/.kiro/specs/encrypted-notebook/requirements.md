# Requirements Document

## Introduction

The Encrypted Notebook is a simple, focused application for managing text and markdown files with strong privacy guarantees. The system provides self-custody data management by storing all user content in a single encrypted file, ensuring users maintain complete control over their data without relying on external services.

## Glossary

- **Encrypted_Notebook**: The main application system that manages user notes and files
- **Data_Store**: The single encrypted file that contains all user notes and metadata
- **Note**: A text or markdown document managed by the system
- **Encryption_Engine**: The component responsible for encrypting and decrypting the data store
- **File_Manager**: The component that handles importing and exporting individual files
- **Editor**: The component that provides text and markdown editing capabilities with multi-language support
- **I18n_Engine**: The component responsible for internationalization, text direction handling, and multi-language support

## Requirements

### Requirement 1: Data Storage and Encryption

**User Story:** As a user, I want all my notes stored in a single encrypted file, so that I maintain complete control over my data and can easily backup or transfer my entire notebook.

#### Acceptance Criteria

1. THE Encrypted_Notebook SHALL store all notes and metadata in a single encrypted file
2. WHEN the application starts, THE Encryption_Engine SHALL decrypt the Data_Store using the user's password
3. WHEN the application closes, THE Encryption_Engine SHALL encrypt all data and save it to the Data_Store
4. WHEN a user provides an incorrect password, THE Encryption_Engine SHALL return an authentication error
5. THE Data_Store SHALL use industry-standard encryption algorithms (AES-256 or equivalent)

### Requirement 2: Note Management

**User Story:** As a user, I want to create, edit, and organize text and markdown notes, so that I can maintain my personal knowledge base.

#### Acceptance Criteria

1. THE Encrypted_Notebook SHALL support creating new notes with text or markdown content
2. THE Encrypted_Notebook SHALL support editing existing notes
3. THE Encrypted_Notebook SHALL support deleting notes
4. THE Encrypted_Notebook SHALL display a list of all notes with their titles
5. WHEN a note is created, THE Encrypted_Notebook SHALL assign it a unique identifier
6. THE Encrypted_Notebook SHALL support both plain text and markdown file formats

### Requirement 3: File Import and Export

**User Story:** As a user, I want to import existing text and markdown files into my notebook, so that I can consolidate my existing documents.

#### Acceptance Criteria

1. WHEN a user selects a text or markdown file, THE File_Manager SHALL import it as a new note
2. WHEN a user exports a note, THE File_Manager SHALL save it as a standalone text or markdown file
3. THE File_Manager SHALL preserve the original file format during import and export operations
4. WHEN importing multiple files, THE File_Manager SHALL create separate notes for each file
5. THE File_Manager SHALL handle file encoding correctly for text files

### Requirement 4: User Interface and Editing

**User Story:** As a user, I want a simple interface for writing and editing my notes, so that I can focus on content creation without distractions.

#### Acceptance Criteria

1. THE Editor SHALL provide syntax highlighting for markdown content
2. THE Editor SHALL support basic text editing operations (cut, copy, paste, undo, redo)
3. THE Encrypted_Notebook SHALL display notes in a readable format
4. THE Encrypted_Notebook SHALL provide a search function to find notes by content or title
5. WHEN editing markdown, THE Editor SHALL provide a preview mode
6. THE Editor SHALL auto-save changes to prevent data loss

### Requirement 5: Security and Privacy

**User Story:** As a user, I want my notes to be secure and private, so that sensitive information remains protected even if my device is compromised.

#### Acceptance Criteria

1. THE Encryption_Engine SHALL never store the user's password in plain text
2. THE Encryption_Engine SHALL use a secure key derivation function for password-based encryption
3. WHEN the application is idle, THE Encrypted_Notebook SHALL automatically lock after a configurable timeout
4. THE Encrypted_Notebook SHALL clear sensitive data from memory when locked
5. THE Data_Store SHALL be indistinguishable from random data when encrypted
6. THE Encrypted_Notebook SHALL not transmit any user data over the network

### Requirement 6: Data Integrity and Backup

**User Story:** As a user, I want assurance that my notes won't be corrupted or lost, so that I can rely on the application for important information.

#### Acceptance Criteria

1. THE Encryption_Engine SHALL verify data integrity when decrypting the Data_Store
2. WHEN data corruption is detected, THE Encrypted_Notebook SHALL alert the user and attempt recovery
3. THE Encrypted_Notebook SHALL create automatic backups of the Data_Store at configurable intervals
4. THE Encrypted_Notebook SHALL allow users to manually create backups of their Data_Store
5. WHEN restoring from backup, THE Encrypted_Notebook SHALL verify the backup's integrity before proceeding
6. THE Encrypted_Notebook SHALL maintain a backup history with timestamps

### Requirement 7: Internationalization and Multi-Language Support

**User Story:** As a user who writes in different languages, I want the application to properly support multi-language text including right-to-left languages, so that I can create notes in my native language with proper text rendering and input handling.

#### Acceptance Criteria

1. THE Editor SHALL support Unicode text input and display for all languages
2. THE Editor SHALL properly handle right-to-left (RTL) languages including Hebrew, Arabic, Persian, and Urdu
3. THE Editor SHALL automatically detect text direction and apply appropriate alignment
4. THE Editor SHALL support bidirectional text (mixed LTR and RTL content) within the same note
5. THE Editor SHALL handle complex script rendering for languages with ligatures and contextual forms
6. THE File_Manager SHALL preserve text encoding and direction when importing and exporting files
7. THE Encrypted_Notebook SHALL support language-specific keyboard layouts and input methods
8. THE Editor SHALL maintain proper cursor movement and text selection behavior in RTL text
9. THE search functionality SHALL work correctly with multi-language content including RTL text
10. THE Encrypted_Notebook SHALL store and retrieve multi-language metadata (note titles, tags) correctly

### Requirement 8: Application Lifecycle

**User Story:** As a user, I want the application to start quickly and handle errors gracefully, so that I can access my notes reliably.

#### Acceptance Criteria

1. WHEN the application starts for the first time, THE Encrypted_Notebook SHALL guide the user through initial setup
2. WHEN no Data_Store exists, THE Encrypted_Notebook SHALL create a new encrypted file
3. IF the Data_Store is corrupted, THEN THE Encrypted_Notebook SHALL attempt to restore from the most recent backup
4. THE Encrypted_Notebook SHALL handle application crashes gracefully without data loss
5. WHEN the user changes their password, THE Encryption_Engine SHALL re-encrypt the Data_Store with the new password


## Future Features (Planned)

### Backup and Restore
- Automatic backup of the encrypted notebook file at configurable intervals
- Manual backup creation on demand
- Restore from backup with integrity verification
- Backup history with timestamps

### Auto-Lock Timer
- Configurable idle timeout that automatically locks the application
- Clears sensitive data from memory when locked
- Requires password re-entry to unlock

### Rename Note
- Allow renaming an existing note title without recreating it
- Accessible via right-click context menu and Edit menu

### macOS Packaging
- PyInstaller build for macOS producing a `.app` bundle
- Separate `packaging/macos/` directory with build script
