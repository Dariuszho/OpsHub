@echo off
REM ToPoint Notebook - Windows Build Script
REM Builds a standalone .exe using PyInstaller
REM Run from this directory: build.bat

echo === ToPoint Notebook - Windows Build ===

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Clean previous build
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist ToPointNotebook.spec del ToPointNotebook.spec

REM Copy application file
copy /Y ..\..\encrypted_notebook.py . >nul

REM Build
echo Building executable...
pyinstaller --onefile --windowed --name "ToPointNotebook" encrypted_notebook.py

REM Cleanup temp files
del encrypted_notebook.py
if exist build rmdir /s /q build
if exist ToPointNotebook.spec del ToPointNotebook.spec

if exist dist\ToPointNotebook.exe (
    echo.
    echo === Build successful ===
    echo Output: dist\ToPointNotebook.exe
) else (
    echo.
    echo === Build FAILED ===
)
