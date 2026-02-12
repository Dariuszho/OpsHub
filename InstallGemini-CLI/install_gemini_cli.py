import os
import sys
import platform
import subprocess
import urllib.request
import json
import shutil
import tarfile

def print_step(message):
    print(f"\n[+] {message}")

def print_error(message):
    print(f"\n[!] {message}")

def get_latest_node_version(system_os):
    print_step("Checking for the latest Node.js version...")
    try:
        url = "https://nodejs.org/dist/index.json"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            # Find the latest LTS version or just the latest version
            # Usually the first entry is the latest.
            # We want a version that has files for our OS.
            for strict in [True, False]: # Try finding LTS first, then any
                for entry in data:
                    if strict and not entry.get('lts'):
                        continue
                    version = entry['version']
                    files = entry['files']
                    
                    # Check compatibility
                    if system_os == "Windows" and "win-x64-msi" in files: 
                         return version
                    elif system_os == "Darwin" and "osx-x64-pkg" in files: # MacOS
                         return version
                    elif system_os == "Linux" and "linux-x64" in files:
                         return version
            
            return data[0]['version'] # Fallback
    except Exception as e:
        print_error(f"Failed to fetch Node.js versions: {e}")
        return "v20.11.0" # Fallback to a known recent version

def download_file(url, dest_path):
    print_step(f"Downloading {url}...")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print_step("Download complete.")
        return True
    except Exception as e:
        print_error(f"Download failed: {e}")
        return False

def install_node_windows(version):
    installer_name = f"node-{version}-x64.msi"
    url = f"https://nodejs.org/dist/{version}/{installer_name}"
    dest = os.path.join(os.getcwd(), installer_name)
    
    if download_file(url, dest):
        print_step("Installing Node.js... (A UAC prompt may appear)")
        # Use /qb to show basic UI so user can see progress and handle UAC prompt
        cmd = ["msiexec", "/i", dest, "/qb"] 
        try:
            print("Please approve the installation in the popup window...")
            subprocess.check_call(cmd, shell=True) 
            print_step("Node.js installation completed.")
        except subprocess.CalledProcessError as e:
            print_error(f"Installation failed: {e}")

def install_node_mac(version):
    installer_name = f"node-{version}.pkg"
    url = f"https://nodejs.org/dist/{version}/{installer_name}"
    dest = os.path.join(os.getcwd(), installer_name)
    
    if download_file(url, dest):
        print_step("Installing Node.js... (Requires sudo password)")
        cmd = ["sudo", "installer", "-pkg", dest, "-target", "/"]
        try:
            subprocess.check_call(cmd)
            print_step("Node.js installation completed.")
        except subprocess.CalledProcessError as e:
            print_error(f"Installation failed: {e}")

def install_node_linux(version):
    # For linux we typically download tar.xz
    filename = f"node-{version}-linux-x64.tar.xz"
    url = f"https://nodejs.org/dist/{version}/{filename}"
    dest = os.path.join(os.getcwd(), filename)
    
    if download_file(url, dest):
        print_step("Extracting Node.js...")
        try:
            with tarfile.open(dest) as tar:
                tar.extractall(path=".")
            
            extracted_folder = f"node-{version}-linux-x64"
            print_step(f"Node.js extracted to {extracted_folder}")
            
            # Simplified approach: valid for many distros
            print_step("Installing to /usr/local/ (Requires sudo password)...")
            cmd = f"sudo cp -R {extracted_folder}/* /usr/local/"
            subprocess.check_call(cmd, shell=True)
            print_step("Node.js installation completed.")
        except Exception as e:
            print_error(f"Installation failed: {e}")

def check_node_installed():
    try:
        subprocess.check_call(["node", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call(["npm", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (OSError, subprocess.CalledProcessError):
        return False

def find_npm_path():
    # Helper to find npm executable if not in PATH
    system = platform.system()
    if system == "Windows":
        possible_paths = [
            r"C:\Program Files\nodejs\npm.cmd",
            r"C:\Program Files (x86)\nodejs\npm.cmd",
            os.path.expandvars(r"%APPDATA%\npm\npm.cmd")
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return "npm" # Hope it's in PATH
    return "npm"

def install_gemini_cli():
    print_step("Installing @google/gemini-cli...")
    
    npm_cmd = find_npm_path()
    cmd = [npm_cmd, "install", "-g", "@google/gemini-cli"]
    
    if platform.system() != "Windows" and os.geteuid() != 0:
         print_step("Note: You might be prompted for password for global installation.")
         # If npm_cmd is absolute path, sudo might choke if not configured, but usually fine
         cmd.insert(0, "sudo")

    try:
        subprocess.check_call(cmd, shell=(platform.system() == "Windows"))
        print_step("Gemini CLI installed successfully!")
    except subprocess.CalledProcessError:
        print_error("Failed to install Gemini CLI. Ensure you have permissions.")
    except FileNotFoundError:
        print_error(f"Could not find npm command: {npm_cmd}. Please restart your terminal and try again.")

def main():
    print("-------------------------------------------------")
    print("      Gemini CLI Auto-Installer Script")
    print("-------------------------------------------------")
    
    detected_os = platform.system()
    print(f"Detected OS: {detected_os}")
    
    print("\nSelect target OS for installation:")
    print("1. Windows")
    print("2. MacOS")
    print("3. Linux")
    print("4. Use Detected OS")
    
    choice = input("Enter choice (1-4): ").strip()
    
    target_os = detected_os
    if choice == '1':
        target_os = "Windows"
    elif choice == '2':
        target_os = "Darwin"
    elif choice == '3':
        target_os = "Linux"
    
    if target_os not in ["Windows", "Darwin", "Linux"]:
        print_error("Unsupported OS selected.")
        return

    # Check for Node.js
    if check_node_installed():
        print_step("Node.js is already installed.")
    else:
        print_step("Node.js not found. Proceeding to download and install...")
        version = get_latest_node_version(target_os)
        print(f"Latest version identified: {version}")
        
        if target_os == "Windows":
            install_node_windows(version)
        elif target_os == "Darwin":
            install_node_mac(version)
        elif target_os == "Linux":
            install_node_linux(version)
            
        print_step("Verifying Node.js installation...")
        # On Windows, the path variable update might not be visible in this process.
        # We might need to warn the user.
        if platform.system() == "Windows":
             print("NOTE: On Windows, you may need to restart your terminal or this script to pick up the new 'node' command.")
             # We can try to proceed anyway, but likely 'npm' won't be found.
             # We will try to find where it was installed? Default: C:\Program Files\nodejs\
             # Temporarily add to path for this script
             default_node_path = r"C:\Program Files\nodejs"
             if os.path.exists(default_node_path):
                 os.environ["PATH"] += os.pathsep + default_node_path

    # Install Gemini CLI
    install_gemini_cli()
    
    print("\n-------------------------------------------------")
    print("      Installation Process Finished")
    print("-------------------------------------------------")

if __name__ == "__main__":
    main()
