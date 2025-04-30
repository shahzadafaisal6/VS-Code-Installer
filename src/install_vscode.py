#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
import time
from typing import Optional
import platform
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename=f'vscode_installer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Display a beautiful banner."""
    banner = f"""
{Colors.BLUE}{Colors.BOLD}
╔═══════════════════════════════════════════╗
║     Visual Studio Code Installer Tool     ║
║         Created by: HAMNA TEC             ║
║             Contact: +923367866994        ║
╚═══════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)

def is_root() -> bool:
    """Check if the script is running with root privileges."""
    return os.geteuid() == 0

def is_vscode_installed() -> bool:
    """Check if VS Code is already installed."""
    return shutil.which("code") is not None

def print_status(message: str, status: str, color: str):
    """Print a formatted status message."""
    print(f"{color}[{status}]{Colors.ENDC} {message}")

def ask_user(prompt: str) -> bool:
    """Ask for yes/no confirmation with colored prompt."""
    while True:
        try:
            ans = input(f"{Colors.YELLOW}{prompt} (y/n): {Colors.ENDC}").strip().lower()
            if ans in ['y', 'yes']:
                return True
            elif ans in ['n', 'no']:
                return False
            print(f"{Colors.RED}Please enter 'y' or 'n'.{Colors.ENDC}")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(1)

def run_command(command: str, use_sudo: bool = True) -> int:
    """Run a shell command with proper error handling."""
    try:
        if use_sudo and not command.startswith("sudo") and not is_root():
            command = f"sudo {command}"
        
        logging.info(f"Executing command: {command}")
        print(f"{Colors.BLUE}Running: {command}{Colors.ENDC}")
        
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        rc = process.poll()
        if rc != 0:
            _, stderr = process.communicate()
            logging.error(f"Command failed with error: {stderr}")
            print(f"{Colors.RED}Error: {stderr}{Colors.ENDC}")
        return rc
    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        print(f"{Colors.RED}Error: {str(e)}{Colors.ENDC}")
        return 1

def check_system_compatibility() -> bool:
    """Check if the system is compatible for VS Code installation."""
    system = platform.system()
    if system != "Linux":
        print_status(f"This installer only supports Linux (detected: {system})", "ERROR", Colors.RED)
        return False
    
    # Check for required dependencies
    dependencies = ["wget", "gpg", "apt"]
    missing = [dep for dep in dependencies if not shutil.which(dep)]
    
    if missing:
        print_status(f"Missing required dependencies: {', '.join(missing)}", "WARNING", Colors.YELLOW)
        return ask_user("Would you like to install missing dependencies?")
    return True

def install_vscode() -> bool:
    """Install VS Code with progress indication."""
    print(f"\n{Colors.BOLD}Starting VS Code installation...{Colors.ENDC}")
    
    steps = [
        ("Updating package lists", "apt update"),
        ("Installing prerequisites", "apt install -y software-properties-common apt-transport-https wget gpg"),
        ("Downloading Microsoft GPG key", "wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg"),
        ("Installing GPG key", "install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg"),
        ("Adding VS Code repository", """sh -c 'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'"""),
        ("Updating package lists", "apt update"),
        ("Installing VS Code", "apt install -y code")
    ]

    for step_name, command in steps:
        print(f"\n{Colors.BLUE}► {step_name}...{Colors.ENDC}")
        if run_command(command) != 0:
            print_status(f"Failed during: {step_name}", "ERROR", Colors.RED)
            return False
        
    return True

def uninstall_vscode() -> bool:
    """Uninstall VS Code and clean up repositories."""
    print(f"\n{Colors.BOLD}Uninstalling VS Code...{Colors.ENDC}")
    
    steps = [
        ("Removing VS Code package", "apt remove --purge -y code"),
        ("Removing VS Code repository", "rm -f /etc/apt/sources.list.d/vscode.list"),
        ("Removing GPG key", "rm -f /etc/apt/keyrings/packages.microsoft.gpg"),
        ("Cleaning up", "apt autoremove -y")
    ]

    for step_name, command in steps:
        print(f"\n{Colors.BLUE}► {step_name}...{Colors.ENDC}")
        if run_command(command) != 0:
            print_status(f"Failed during: {step_name}", "ERROR", Colors.RED)
            return False
    
    return True

def main():
    try:
        print_banner()
        
        if not check_system_compatibility():
            sys.exit(1)

        is_installed = is_vscode_installed()
        
        if is_installed:
            print_status("Visual Studio Code is already installed on this system.", "INFO", Colors.GREEN)
            if ask_user("Would you like to uninstall VS Code?"):
                if uninstall_vscode():
                    print_status("VS Code has been successfully uninstalled!", "SUCCESS", Colors.GREEN)
                else:
                    print_status("Failed to uninstall VS Code.", "ERROR", Colors.RED)
        else:
            print_status("Visual Studio Code is not installed.", "INFO", Colors.YELLOW)
            if ask_user("Would you like to install VS Code?"):
                if install_vscode():
                    print_status("VS Code has been successfully installed!", "SUCCESS", Colors.GREEN)
                    print(f"\n{Colors.GREEN}📢 You can launch VS Code by:{Colors.ENDC}")
                    print("   1. Typing 'code' in the terminal")
                    print("   2. Finding it in your application menu")
                else:
                    print_status("Failed to install VS Code.", "ERROR", Colors.RED)
            else:
                print_status("Installation cancelled by user.", "INFO", Colors.YELLOW)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"{Colors.RED}An unexpected error occurred. Check the logs for details.{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()

