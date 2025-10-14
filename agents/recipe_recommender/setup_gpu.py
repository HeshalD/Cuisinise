#!/usr/bin/env python3
"""
GPU Setup Script for RecipeSearcher
This script helps configure the environment for optimal GPU usage.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ {description} failed with exception: {e}")
        return False

def check_gpu_availability():
    """Check if GPU is available"""
    print("=== Checking GPU Availability ===")
    
    # Check NVIDIA GPU
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ NVIDIA GPU detected")
            print("GPU Info:")
            print(result.stdout)
            return True
        else:
            print("✗ No NVIDIA GPU detected")
            return False
    except FileNotFoundError:
        print("✗ nvidia-smi not found. NVIDIA drivers may not be installed.")
        return False

def check_cuda_installation():
    """Check CUDA installation"""
    print("\n=== Checking CUDA Installation ===")
    
    try:
        result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ CUDA compiler found")
            print("CUDA Version:")
            print(result.stdout)
            return True
        else:
            print("✗ CUDA compiler not found")
            return False
    except FileNotFoundError:
        print("✗ nvcc not found. CUDA toolkit may not be installed.")
        return False

def install_gpu_dependencies():
    """Install GPU-optimized dependencies"""
    print("\n=== Installing GPU Dependencies ===")
    
    # Uninstall CPU-only FAISS if present
    run_command("pip uninstall faiss-cpu -y", "Removing CPU-only FAISS")
    
    # Try different methods to install FAISS with GPU support
    print("Attempting to install FAISS with GPU support...")
    
    # Method 1: Try conda-forge (if conda is available)
    if run_command("conda --version", "Checking for conda"):
        print("Trying conda installation for FAISS GPU...")
        if run_command("conda install -c conda-forge faiss-gpu -y", "Installing FAISS GPU via conda"):
            print("✓ FAISS GPU installed via conda")
        else:
            print("Conda installation failed, trying pip alternatives...")
    
    # Method 2: Try pip with conda-forge channel
    if not run_command("pip install faiss-gpu", "Installing FAISS GPU via pip"):
        print("Trying alternative FAISS installation methods...")
        
        # Method 3: Try installing from conda-forge via pip
        if not run_command("pip install --extra-index-url https://pypi.org/simple/ faiss-gpu", "Installing FAISS GPU with extra index"):
            # Method 4: Try building from source (advanced users)
            print("Trying to install FAISS with GPU support from source...")
            if not run_command("pip install faiss-gpu --no-binary=faiss-gpu", "Building FAISS GPU from source"):
                print("Warning: All FAISS GPU installation methods failed.")
                print("Installing CPU version as fallback...")
                run_command("pip install faiss-cpu", "Installing CPU FAISS as fallback")
                print("Note: You can manually install FAISS GPU later using:")
                print("  conda install -c conda-forge faiss-gpu")
    
    # Install PyTorch with CUDA support
    print("\nInstalling PyTorch with CUDA support...")
    if not run_command("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118", 
                         "Installing PyTorch with CUDA support"):
        print("Warning: CUDA PyTorch installation failed. Installing CPU version.")
        run_command("pip install torch torchvision torchaudio", "Installing CPU PyTorch")
    
    # Install other dependencies
    run_command("pip install -r requirements.txt", "Installing other dependencies")

def configure_environment():
    """Configure environment variables for optimal GPU usage"""
    print("\n=== Configuring Environment ===")
    
    env_vars = {
        "CUDA_VISIBLE_DEVICES": "0",  # Use first GPU
        "PYTORCH_CUDA_ALLOC_CONF": "max_split_size_mb:128",
        "SPACY_GPU_MEMORY_FRACTION": "0.8",
        "OMP_NUM_THREADS": "1",  # Avoid CPU-GPU conflicts
    }
    
    print("Recommended environment variables:")
    for key, value in env_vars.items():
        print(f"  export {key}={value}")
    
    # Create a .env file
    env_file = Path(__file__).parent / ".env"
    with open(env_file, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print(f"✓ Environment variables saved to {env_file}")

def test_gpu_setup():
    """Test if GPU setup is working"""
    print("\n=== Testing GPU Setup ===")
    
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✓ CUDA available: {torch.cuda.is_available()}")
            print(f"✓ CUDA version: {torch.version.cuda}")
            print(f"✓ GPU count: {torch.cuda.device_count()}")
            print(f"✓ Current GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("✗ CUDA not available in PyTorch")
            return False
        
        import faiss
        print(f"✓ FAISS version: {faiss.__version__}")
        
        if hasattr(faiss, "get_num_gpus") and faiss.get_num_gpus() > 0:
            print(f"✓ FAISS GPU support: {faiss.get_num_gpus()} GPUs available")
        else:
            print("✗ FAISS GPU support not available")
            return False
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("GPU Setup for RecipeSearcher")
    print("=" * 50)
    
    # Check system requirements
    gpu_available = check_gpu_availability()
    cuda_available = check_cuda_installation()
    
    if not gpu_available:
        print("\n⚠️  No GPU detected. The system will run on CPU.")
        print("For GPU acceleration, please install NVIDIA drivers and CUDA toolkit.")
        return False
    
    if not cuda_available:
        print("\n⚠️  CUDA not found. GPU acceleration may not work optimally.")
        print("Please install CUDA toolkit for best performance.")
    
    # Install dependencies
    install_gpu_dependencies()
    
    # Configure environment
    configure_environment()
    
    # Test setup
    if test_gpu_setup():
        print("\n✓ GPU setup completed successfully!")
        print("\nTo use the optimized GPU version:")
        print("1. Activate your virtual environment")
        print("2. Run: python test_gpu.py")
        return True
    else:
        print("\n✗ GPU setup failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
