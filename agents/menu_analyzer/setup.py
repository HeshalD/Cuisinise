#!/usr/bin/env python3
"""
Setup script for NLP Menu Analyzer
Installs required dependencies and spaCy English model
"""

import subprocess
import sys

# Optional colored output
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    C = {"info": Fore.CYAN, "success": Fore.GREEN, "error": Fore.RED, "warn": Fore.YELLOW}
except ImportError:
    C = {"info": "", "success": "", "error": "", "warn": ""}


def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"{C['info']}📦 {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"{C['success']}✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{C['error']}❌ Error during {description}")
        return False


def check_python_version():
    if sys.version_info < (3, 7):
        print(f"{C['warn']}⚠️ Python 3.7+ is recommended. You are running {sys.version}")
        return False
    return True


def main():
    print(f"{C['info']}🚀 Setting up NLP Menu Analyzer...")
    print("=" * 50)

    check_python_version()

    # Upgrade pip first
    run_command("python -m pip install --upgrade pip", "Upgrading pip")

    # Required packages
    packages = [
        "pandas",
        "numpy",
        "scikit-learn",
        "sentence-transformers",
        "spacy",
        "colorama"
    ]

    print(f"{C['info']}📋 Required packages:")
    for pkg in packages:
        print(f"   • {pkg}")
    print()

    # Install packages
    for package in packages:
        run_command(f"pip install {package}", f"Installing {package}")

    # Install spaCy English model
    run_command("python -m spacy download en_core_web_sm", "Installing spaCy English model")

    print("\n" + "=" * 50)
    print(f"{C['success']}✅ Setup completed!")
    print("\n🎯 Next steps:")
    print("1. Run: python main.py")
    print("2. Choose option 1 for conversational search")
    print("3. Try queries like: 'I want something healthy for breakfast'")
    print("\n🍽️ Enjoy your NLP-powered menu search!")


if __name__ == "__main__":
    main()
