# 🛠️ VS Code Installer

A comprehensive Visual Studio Code installer and uninstaller for Linux systems (especially Parrot OS and Debian-based distributions) with a beautiful command-line interface.

## 📦 Features
- 🚀 Automated VS Code installation and uninstallation
- ✅ Detects if VS Code is already installed
- 🔍 System compatibility checks
- 🔐 Adds Microsoft's secure APT repository and key
- 📥 Installs required dependencies
- 🎨 Beautiful colored interface
- 📝 Detailed logging
- 🔒 Proper error handling
- 🧹 Clean uninstallation with proper cleanup

## Developer Information
- Developer: Faisal
- Company: HAMNA TEC
- Contact: 
  - +923367866994
  - +923013116258
- Repository: https://github.com/shahzadafaisal6/VS-Code-Installer

## 🧑‍💻 Prerequisites
- Python 3.6 or higher
- Linux-based operating system (optimized for Parrot OS and Debian-based systems)
- Root/sudo privileges
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shahzadafaisal6/VS-Code-Installer.git
cd VS-Code-Installer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the installer with:
```bash
python src/install_vscode.py
```

The script will:
1. Check system compatibility
2. Detect if VS Code is already installed
3. Provide options to install or uninstall
4. Handle the process automatically with proper error handling
5. Guide you on how to open VS Code after installation

## Logging

Logs are automatically generated in the current directory with timestamp for debugging purposes.

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Feel free to submit issues and pull requests.