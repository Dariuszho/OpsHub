# Gemini CLI Auto-Installer

This project provides a Python script to automate the installation of **Node.js** and the **Gemini CLI** (`@google/gemini-cli`) on Windows, macOS, and Linux.

## How the Script Works

The script (`install_gemini_cli.py`) performs the following steps:

1.  **OS Detection**: It automatically detects your operating system (Windows, macOS, or Linux). You can also manually select the target OS if needed.
2.  **Node.js Check & Installation**:
    *   It checks if `node` and `npm` are already installed.
    *   If not found, it fetches the latest version information from the official [Node.js distribution](https://nodejs.org/dist/index.json).
    *   It downloads the appropriate installer:
        *   **Windows**: `.msi` installer (Installing via `msiexec`).
        *   **macOS**: `.pkg` installer (Installing via `installer`).
        *   **Linux**: `.tar.xz` binary archive (Extracted and copied to `/usr/local`).
3.  **Gemini CLI Installation**:
    *   Once Node.js is available, it uses `npm` (Node Package Manager) to install the Gemini CLI globally:
        ```bash
        npm install -g @google/gemini-cli
        ```

## Requirements & Python Libraries

This script is designed to run with a standard Python 3 installation. It **does not require** any external third-party libraries to be installed beforehand.

### Standard Libraries Used
The script utilizes the following built-in Python modules:
*   `os`, `sys`, `platform`: For system detection and file path handling.
*   `subprocess`: To execute system commands (like `msiexec`, `npm`).
*   `urllib.request`: To make HTTP requests to download Node.js.
*   `json`: To parse the Node.js version data.
*   `tarfile`, `shutil`: For handling file extraction on Linux.

### Managing External Libraries (Context)
While this specific script relies only on the standard library, many Python automation scripts require external packages like `requests` (for easier HTTP calls) or `tqdm` (for progress bars).

If you needed to install such libraries, you would typically use `pip` (Python Package Installer).

**How to download and install libraries with pip:**

1.  **Check if pip is installed**:
    ```bash
    pip --version
    ```
2.  **Install a library** (e.g., `requests`):
    ```bash
    pip install requests
    ```
3.  **Install requirements from a file** (common practice):
    If a project has a `requirements.txt` file, you can install all dependencies at once:
    ```bash
    pip install -r requirements.txt
    ```

## Usage Instructions

1.  **Run the script**:
    ```bash
    python install_gemini_cli.py
    ```
2.  **Follow the prompts**:
    *   The script will ask you to confirm your OS or choose one manually.
    *   It will attempt to download and install Node.js if missing. 
    *   **Note**: You may be prompted for your administrator password (sudo) during the installation phase, as installing global tools requires elevated permissions.
3.  **Verification**:
    After the script finishes, you can verify the installation by running:
    ```bash
    gemini --version
    ```
    (Or `gemini-cli --version` depending on the installed binary name).

## Troubleshooting

*   **Permissions**: On Linux and macOS, if the installation fails, ensure you have `sudo` rights.
*   **Path Issues**: On Windows, if `node` is installed but not recognized immediately, you might need to restart your terminal or command prompt for the `PATH` environment variable updates to take effect.
