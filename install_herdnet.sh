#!/bin/bash
# Installation script for HerdNet Animal Detection API

echo "======================================"
echo "Installing HerdNet API Dependencies"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed. Please install git first."
    exit 1
fi
echo "Git is installed: $(git --version)"
echo ""

# Install PyTorch (you may want to customize this based on your CUDA version)
echo "Installing PyTorch..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
echo ""

# Install other requirements
echo "Installing Flask and other dependencies..."
pip install Flask gunicorn pillow numpy
echo ""

# Install HerdNet from GitHub
echo "Installing HerdNet from GitHub..."
pip install git+https://github.com/Alexandre-Delplanque/HerdNet.git
echo ""

# Install HerdNet dependencies
echo "Installing HerdNet additional dependencies..."
pip install albumentations opencv-python PyYAML hydra-core
echo ""

# Verify installation
echo "======================================"
echo "Verifying installation..."
echo "======================================"
python3 -c "
import torch
import flask
from animaloc.models import HerdNet, load_model
print('✓ PyTorch:', torch.__version__)
print('✓ Flask:', flask.__version__)
print('✓ HerdNet: Successfully imported')
print('✓ CUDA available:', torch.cuda.is_available())
"

echo ""
echo "======================================"
echo "Installation complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Place your herdnet_model.pth file in this directory"
echo "2. Run the application: python app.py"
echo ""

