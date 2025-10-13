# GPU Installation Guide for RecipeSearcher

## The Error Explained

The error `ERROR: Could not find a version that satisfies the requirement faiss-gpu` occurs because:

1. **`faiss-gpu` is not available via pip** - It's only distributed through conda-forge
2. **FAISS GPU requires CUDA** - It needs proper CUDA toolkit installation
3. **Platform-specific builds** - GPU support varies by operating system

## Solution Options

### Option 1: Use Conda (Recommended)

If you have conda installed:

```bash
# Install FAISS GPU via conda
conda install -c conda-forge faiss-gpu

# Install other dependencies via pip
pip install -r requirements.txt
```

### Option 2: Manual Installation

1. **Install CUDA Toolkit** (if not already installed):
   - Download from: https://developer.nvidia.com/cuda-downloads
   - Install CUDA 11.8 or 12.x

2. **Install FAISS GPU manually**:
   ```bash
   # Try conda-forge
   conda install -c conda-forge faiss-gpu
   
   # Or build from source (advanced)
   pip install faiss-gpu --no-binary=faiss-gpu
   ```

### Option 3: Use CPU Version (Fallback)

If GPU installation fails, the code will automatically fall back to CPU:

```bash
pip install faiss-cpu
```

## Quick Setup Commands

### For Conda Users:
```bash
# Create new environment
conda create -n cuisinise-gpu python=3.9
conda activate cuisinise-gpu

# Install FAISS GPU
conda install -c conda-forge faiss-gpu

# Install other dependencies
pip install -r requirements.txt

# Test installation
python test_gpu.py
```

### For Pip-Only Users:
```bash
# Install CPU version (will work but slower)
pip install faiss-cpu

# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other dependencies
pip install -r requirements.txt
```

## Verification

Run the test script to verify GPU setup:

```bash
python test_gpu.py
```

This will show:
- GPU detection status
- Memory usage
- Performance benchmarks

## Performance Impact

- **With GPU**: 5-10x faster similarity search
- **CPU Only**: Still functional but slower for large datasets
- **Mixed**: PyTorch and SpaCy can still use GPU even if FAISS uses CPU

## Troubleshooting

### Common Issues:

1. **"CUDA not available"**: Install CUDA toolkit
2. **"FAISS GPU not found"**: Use conda installation
3. **"Memory errors"**: Reduce batch sizes or use CPU fallback

### Check GPU Status:
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")

import faiss
print(f"FAISS GPUs: {faiss.get_num_gpus()}")
```

The code is designed to work with or without GPU - it will automatically detect and use the best available option!





