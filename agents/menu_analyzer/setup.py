#!/usr/bin/env python3
"""
Setup script for NLP Menu Analyzer
This script installs all required dependencies
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up NLP Menu Analyzer...")
    print("=" * 50)
    
    # List of required packages
    packages = [
        "pandas",
        "numpy", 
        "scikit-learn",
        "sentence-transformers",
        "spacy",
        "warnings"
    ]
    
    print("📋 Required packages:")
    for pkg in packages:
        print(f"   • {pkg}")
    print()
    
    # Install packages
    for package in packages:
        if package == "warnings":
            continue  # warnings is built-in
        
        success = run_command(f"pip install {package}", f"Installing {package}")
        if not success:
            print(f"⚠️ Warning: Failed to install {package}")
    
    # Install spaCy English model
    print("\n🧠 Installing spaCy English model...")
    spacy_success = run_command(
        "python -m spacy download en_core_web_sm", 
        "Installing spaCy English model"
    )
    
    if not spacy_success:
        print("⚠️ SpaCy model installation failed. NLP features may be limited.")
    
    print("\n" + "=" * 50)
    print("✅ Setup completed!")
    print("\n🎯 Next steps:")
    print("1. Run: python main.py")
    print("2. Choose option 1 for conversational search")
    print("3. Try queries like: 'I want something healthy for breakfast'")
    print("\n🍽️ Enjoy your NLP-powered menu search!")

if __name__ == "__main__":
    main()