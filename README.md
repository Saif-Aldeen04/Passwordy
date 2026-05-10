# 🔑 Passwordy (Cross-Platform)

**Passwordy** is a lightweight, cross-platform command-line interface (CLI) password manager. It allows you to store, retrieve, and manage credentials directly from your terminal on **Windows, macOS, and Linux** while maintaining local privacy through data encryption.

---

## 🚀 Features

* **Cross-Platform**: Works natively on Windows, macOS, and Linux.
* **Universal Installation**: Simple setup via `pip`, making the tool available globally.
* **Secure Storage**: Encrypts data using a Caesar Cipher (Key=3) before local storage.
* **Clipboard Integration**: Uses `pyperclip` to securely copy passwords to the system clipboard.
* **Session Management**: Implements temporary session handling using system-specific temp directories.

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Saif-Aldeen04/Passwordy.git
cd Passwordy
```

### 2. Install via Pip
Install the tool and its dependencies (pyperclip, colorama) globally:
```bash
pip install .
```

---

## 📖 How to Use

Launch the tool from any terminal window:
```bash
passwordy
```

### Core Commands
- **1) Login / Create Account**: Set up your master vault or access existing records.
- **2) Create New Password**: Securely store credentials for different platforms.
- **3) Retrieve Password**: Search for a platform to copy its password to your clipboard.
- **4) Edit Password**: Update existing credentials within your vault.

**Logout**: Run `passwordy logout` to clear the active session.

---

## 🏗️ Technical Architecture

- **Storage**: Data is stored in the hidden `~/.passwordy/` directory.
- **Security Disclaimer**: This project is for educational purposes. The Caesar Cipher is used for basic data obfuscation and is not recommended for high-security production environments.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Saif Aldeen Wael Alsayed**  
3rd Year Student, Faculty of Computers and Information