# 🛠️ Visual Studio Code Installer for Parrot OS

This Python script simplifies the process of installing **Visual Studio Code** on **Parrot OS** or any Debian-based Linux system. It checks for an existing installation, adds Microsoft's repository and GPG key if needed, and installs VS Code via APT. It’s ideal for quick setup or scripting out a new environment.

---

## 📦 Features

- ✅ Detects if VS Code is already installed
- 🧠 Prompts for user confirmation before installation
- 🔐 Adds Microsoft’s secure APT repository and key
- 📥 Installs required dependencies
- 🖥️ Instructs how to open VS Code after setup

---

## 🧑‍💻 Prerequisites

Make sure you have:

- Python 3 installed (`python3 --version`)
- `sudo` privileges on the system
- An internet connection

---

## 🚀 How to Use This Script

### 1. 📥 Download the Script

You can manually save the script as `install_vscode.py`, or use `wget` if hosted online:
```bash
wget https://your-domain.com/install_vscode.py

