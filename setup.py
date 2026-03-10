from setuptools import setup

setup(
    name="passwordy",
    version="1.1",
    py_modules=["passwordy"],
    install_requires=[
        "pyperclip", # Clipboard support
        "colorama",  # Color support for Windows CMD/PowerShell
        "cryptography", # Secure encryption
    ],
    entry_points={
        "console_scripts": [
            "passwordy=passwordy:main",
        ],
    },
)