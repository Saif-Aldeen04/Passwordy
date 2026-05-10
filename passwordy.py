#!/usr/bin/env python3

import os
import sys
import tempfile
import shutil
import hashlib
from getpass import getpass

# Third-party libraries for cross-platform support
try:
    import pyperclip # For universal clipboard support
    from colorama import init, Fore, Style # For universal terminal colors
    from cryptography.fernet import Fernet # For secure encryption
    init(autoreset=True)
except ImportError:
    print("Missing dependencies. Please run: pip install pyperclip colorama cryptography")
    sys.exit(1)

# Dynamically find the temp directory for the current OS
SESSION_FILE = os.path.join(tempfile.gettempdir(), "passwordy_session")

# ---------- Colors ----------
class C:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    RESET = Style.RESET_ALL

# ---------- Banner ----------
def banner():
    print(C.CYAN + r"""
██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ ██╗   ██╗
██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║ ╚████╔╝
██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║  ╚██╔╝
██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝   ██║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝    ╚═╝
""" + C.RESET)

# ---------- Fernet Encryption ----------
def get_cipher():
    folder = os.path.join(os.path.expanduser("~"), ".passwordy")
    if not os.path.exists(folder):
        os.mkdir(folder)
    key_file = os.path.join(folder, ".secret.key")
    
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
    else:
        with open(key_file, "rb") as f:
            key = f.read()
    return Fernet(key)

cipher = get_cipher()

def encrypt(text):
    return cipher.encrypt(text.encode('utf-8')).decode('utf-8')

def decrypt(text):
    return cipher.decrypt(text.encode('utf-8')).decode('utf-8')

# ---------- User File ----------
def get_user_file(username):
    # os.path.expanduser("~") works on Windows, Mac, and Linux
    folder = os.path.join(os.path.expanduser("~"), ".passwordy")
    if not os.path.exists(folder):
        os.mkdir(folder)
    # Use SHA256 hash for a consistent, secure filename
    safe_name = hashlib.sha256(username.encode('utf-8')).hexdigest()
    return os.path.join(folder, f"{safe_name}.txt")

# ---------- Create Account ----------
def create_account():
    username = input("username: ").strip()
    password = getpass("password: ").strip()
    user_file = get_user_file(username)
    enc_user = encrypt(username)
    enc_pass = encrypt(password)
    with open(user_file, "w") as f:
        f.write(enc_user + "\n")
        f.write(enc_pass + "\n")
    with open(SESSION_FILE, "w") as s:
        s.write(username)
    print(C.GREEN + f"\nWelcome {username}" + C.RESET)
    password_menu(user_file)

# ---------- Login ----------
def login():
    username = input("username: ").strip()
    password = getpass("password: ").strip()
    user_file = get_user_file(username)
    if not os.path.exists(user_file):
        print(C.RED + "Account not found." + C.RESET)
        return
    with open(user_file) as f:
        enc_user = f.readline().strip()
        enc_pass = f.readline().strip()
    saved_user = decrypt(enc_user)
    saved_pass = decrypt(enc_pass)
    if username == saved_user and password == saved_pass:
        with open(SESSION_FILE, "w") as s:
            s.write(username)
        print(C.GREEN + f"\nWelcome {username}" + C.RESET)
        password_menu(user_file)
    else:
        print(C.RED + "Wrong username or password" + C.RESET)

# ---------- Create Password ----------
def create_password(user_file):
    print("\nplatform: Facebook, Instagram or any other")
    platform = input("platform: ").strip()
    password = getpass("password: ").strip()
    enc_platform = encrypt(platform)
    enc_password = encrypt(password)
    with open(user_file, "a") as f:
        f.write(f"{enc_platform}:{enc_password}\n")
    print(C.GREEN + "Password saved!" + C.RESET)
    sys.exit()

# ---------- Retrieve Password ----------
def retrieve_password(user_file):
    platform_input = input("Enter platform name: ").strip().lower()
    with open(user_file) as f:
        lines = f.readlines()[2:]
    for line in lines:
        dec_line = decrypt(line.strip())
        if ":" in dec_line:
            platform, password = dec_line.split(":", 1)
            if platform.lower() == platform_input:
                # Use pyperclip instead of xclip for cross-platform support
                pyperclip.copy(password)
                print(C.GREEN + f"Password for {platform} copied to clipboard!" + C.RESET)
                sys.exit()
    print(C.YELLOW + "Platform not found." + C.RESET)
    sys.exit()

# ---------- Edit Password ----------
def edit_password(user_file):
    platform_input = input("Enter platform to edit: ").strip().lower()
    new_password = getpass("Enter new password: ")
    with open(user_file) as f:
        lines = f.readlines()
    header = lines[:2]
    data = lines[2:]
    updated = False
    new_lines = []
    for line in data:
        dec_line = decrypt(line.strip())
        if ":" in dec_line:
            platform, password = dec_line.split(":", 1)
            if platform.lower() == platform_input:
                enc_platform = encrypt(platform)
                enc_pass = encrypt(new_password)
                new_lines.append(f"{enc_platform}:{enc_pass}\n")
                updated = True
            else:
                new_lines.append(line)
    if updated:
        with open(user_file, "w") as f:
            f.writelines(header + new_lines)
        print(C.GREEN + "Password updated!" + C.RESET)
    else:
        print(C.RED + "Platform not found." + C.RESET)
    sys.exit()

# ---------- Password Menu ----------
def password_menu(user_file):
    print("\n1) Create new password")
    print("2) Retrieve password")
    print("3) Edit password")
    choice = input("> ")
    if choice == "1":
        create_password(user_file)
    elif choice == "2":
        retrieve_password(user_file)
    elif choice == "3":
        edit_password(user_file)
    else:
        print(C.RED + "Invalid option" + C.RESET)

# ---------- Logout ----------
def logout():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        print(C.YELLOW + "Logged out" + C.RESET)

# ---------- Main ----------
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "logout":
        logout()
        return
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE) as s:
            username = s.read().strip()
        user_file = get_user_file(username)
        print(C.GREEN + f"Welcome back {username}" + C.RESET)
        password_menu(user_file)
        return
    banner()
    print("1) Login")
    print("2) Create Account")
    choice = input("> ")
    if choice == "1":
        login()
    elif choice == "2":
        create_account()
    else:
        print(C.RED + "Invalid option" + C.RESET)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # This catch-all ensures that on Windows/Linux, 
        # Ctrl + C exits silently and returns to the prompt.
        print("\n" + C.YELLOW + "Operation cancelled by user." + C.RESET)
        try:
            sys.exit(0)
        except SystemExit:
            # Forceful exit to prevent any lingering Windows threads
            os._exit(0)