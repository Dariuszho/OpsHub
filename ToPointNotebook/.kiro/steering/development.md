# Development Environment & Standards

## Development Environment
- **Primary Development Platform**: Windows OS
- **Testing Strategy**: Manual testing on Linux and macOS by user
- **Development Role**: Senior Python developer with authority to suggest structural improvements

## Senior Developer Authority
As a senior Python developer on this project, I have the responsibility to:
- Apply highest standards and best practices in Python development
- Suggest structural improvements when I identify better approaches
- Question design decisions that may impact code quality, maintainability, or security
- **Always ask the user before making significant structural or design changes**

## Development Standards

### Code Quality Requirements
- **Type Hints**: Use comprehensive type annotations throughout the codebase
- **Docstrings**: Google-style docstrings for all classes and methods
- **Error Handling**: Comprehensive exception handling with specific exception types
- **Logging**: Structured logging for debugging and monitoring
- **Code Coverage**: Aim for >90% test coverage when tests are implemented

### Security Standards
- **Cryptographic Libraries**: Use `cryptography` library instead of `pycrypto` for modern, secure implementations
- **Key Management**: Implement proper key derivation with salt and iteration counts
- **Memory Security**: Use `memoryview` and explicit memory clearing for sensitive data
- **Input Validation**: Validate all user inputs and file operations
- **Secure Defaults**: Fail securely, use secure defaults for all configurations

### Architecture Standards
- **SOLID Principles**: Apply Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion
- **Design Patterns**: Use appropriate patterns (Observer for UI updates, Strategy for encryption algorithms, etc.)
- **Separation of Concerns**: Clear boundaries between GUI, business logic, and data layers
- **Dependency Injection**: Avoid tight coupling between components
- **Internationalization**: Use Qt's internationalization framework for proper RTL and complex script support

### Platform-Specific Considerations

#### Windows (Primary Development)
- Use `pathlib.Path` for all file operations
- Handle Windows-specific file locking and permissions
- Test with Windows Defender and antivirus software
- Consider Windows-specific packaging with PyInstaller
- Test with Windows IME for Asian language input
- Verify proper font rendering with ClearType

#### Linux/macOS (User Testing)
- Ensure proper file permissions handling
- Test with different Python versions available on these platforms
- Verify GUI scaling and appearance on different desktop environments
- Handle case-sensitive file systems appropriately
- Test with various input methods (ibus, fcitx, etc.)
- Verify font fallback behavior across different distributions

## Code Structure Recommendations

### Potential Improvements to Consider
Based on senior developer experience, I may suggest:

1. **Configuration Management**: Add a configuration system for user preferences
2. **Plugin Architecture**: Design for potential future extensions
3. **Async Operations**: Use asyncio for file I/O to prevent GUI freezing
4. **State Management**: Implement proper state management patterns
5. **Testing Framework**: Add unit tests, integration tests, and GUI tests
6. **Packaging**: Professional packaging with proper metadata and dependencies

### When to Ask for Permission
I will ask the user before:
- Changing the single-file architecture to multi-file structure
- Adding external dependencies beyond PyQt6/PySide6 and cryptography
- Modifying the core encryption approach
- Adding complex features not in the original requirements
- Restructuring the component hierarchy significantly

## Development Workflow

### Code Review Standards
- All code must pass type checking with `mypy`
- All code must pass linting with `pylint` or `ruff`
- Security review for all cryptographic operations
- Performance review for file operations and GUI responsiveness

### Testing Strategy
- Unit tests for all business logic components
- Integration tests for encryption/decryption workflows
- GUI tests for critical user interactions
- Cross-platform compatibility tests (user-driven)
- Security tests for encryption and key management

### Documentation Requirements
- Inline comments explaining complex algorithms
- Architecture decision records (ADRs) for major design choices
- User documentation for installation and usage
- Developer documentation for future maintenance

## Quality Gates
Before considering the application complete:
1. All requirements from specifications must be implemented
2. Code must pass all quality checks (typing, linting, security)
3. Manual testing must pass on all three target platforms
4. Security review must be completed for encryption components
5. Performance must be acceptable for typical usage patterns