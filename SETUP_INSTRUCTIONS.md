# Complete Setup Instructions

## Step-by-Step Setup Guide for HerdNet Animal Detection API

### Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher
- pip (Python package manager)
- Git (for installing packages from GitHub)
- (Optional) CUDA-capable GPU for faster inference

### Step 1: Clone or Download This Repository

```bash
cd /path/to/your/projects
git clone <your-repo-url>
cd back
```

### Step 2: Install HerdNet and Dependencies

You have three options:

#### Option A: Quick Install (Recommended)

```bash
pip install -r requirements.txt
```

This command will:
- Install Flask and web dependencies
- Install PyTorch and torchvision
- Install HerdNet from GitHub: https://github.com/Alexandre-Delplanque/HerdNet
- Install all required dependencies (albumentations, opencv-python, etc.)

#### Option B: Using Installation Script

```bash
chmod +x install_herdnet.sh
./install_herdnet.sh
```

The script will:
- Check Python and Git versions
- Install PyTorch
- Install Flask
- Install HerdNet from GitHub
- Verify installation

#### Option C: Manual Step-by-Step

```bash
# 1. Install PyTorch (CPU version)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Or for CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 2. Install Flask and basic dependencies
pip install Flask==3.0.0 gunicorn==21.2.0 pillow==12.0.0 numpy==2.3.5

# 3. Install HerdNet from GitHub
pip install git+https://github.com/Alexandre-Delplanque/HerdNet.git

# 4. Install HerdNet dependencies
pip install albumentations>=1.0.0 opencv-python>=4.5.0 PyYAML>=5.4.0 hydra-core>=1.1.0
```

### Step 3: Verify Installation

```bash
python3 -c "
import torch
import flask
from animaloc.models import HerdNet, load_model
print('✓ PyTorch:', torch.__version__)
print('✓ Flask:', flask.__version__)
print('✓ HerdNet: Successfully imported')
print('✓ CUDA available:', torch.cuda.is_available())
"
```

Expected output:
```
✓ PyTorch: 2.x.x
✓ Flask: 3.0.0
✓ HerdNet: Successfully imported
✓ CUDA available: True/False
```

### Step 4: Prepare Your HerdNet Model

Place your trained `herdnet_model.pth` file in the project root directory:

```bash
back/
├── app.py
├── herdnet_model.pth  ← Your trained model here
├── ...
```

#### Model File Format

Your model file should be a PyTorch `.pth` file created using the official HerdNet training process. It should contain:

```python
{
    'model': <state_dict>,
    'num_classes': <int>,
    'down_ratio': <int>,
    # Optional metadata:
    'classes': {0: 'no_animal', 1: 'cattle', ...},
    'mean': [0.485, 0.456, 0.406],
    'std': [0.229, 0.224, 0.225]
}
```

### Step 5: Configure Animal Classes (Optional)

If your model uses different classes, edit `app.py`:

```python
ANIMAL_CLASSES = {
    0: "no_animal",
    1: "your_species_1",
    2: "your_species_2",
    # ... add your classes
}
```

### Step 6: Run the Application

#### Development Mode

```bash
python app.py
```

The server will start on http://localhost:8000

#### Production Mode

```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

Or with more workers:

```bash
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 app:app
```

### Step 7: Test the API

#### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok"}
```

#### Test Image Analysis

```bash
curl -X POST http://localhost:8000/analyze-image \
  -F "image=@/path/to/test/image.jpg"
```

Or use the provided test script:

```bash
python test_api.py /path/to/test/image.jpg
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'animaloc'"

**Solution:** HerdNet was not installed correctly.

```bash
pip install git+https://github.com/Alexandre-Delplanque/HerdNet.git
```

### Issue: "RuntimeError: Model file not found"

**Solution:** Ensure `herdnet_model.pth` is in the correct directory:

```bash
ls -la herdnet_model.pth
```

### Issue: "CUDA out of memory"

**Solution:** The model is trying to use GPU but running out of memory.

Either:
1. Use CPU mode (automatically handled if CUDA unavailable)
2. Reduce image size before sending
3. Use a GPU with more memory

### Issue: "Import errors for albumentations or opencv"

**Solution:** Install missing dependencies:

```bash
pip install albumentations opencv-python PyYAML hydra-core
```

### Issue: Git SSL certificate errors

**Solution:** Update git or disable SSL verification temporarily:

```bash
git config --global http.sslVerify false
pip install git+https://github.com/Alexandre-Delplanque/HerdNet.git
git config --global http.sslVerify true
```

## Next Steps

1. **Read the documentation**: See [README.md](README.md) for API usage
2. **Model information**: See [MODEL_INFO.md](MODEL_INFO.md) for HerdNet details
3. **Quick testing**: See [QUICKSTART.md](QUICKSTART.md) for quick commands
4. **Train your own model**: Visit https://github.com/Alexandre-Delplanque/HerdNet

## Support

For issues related to:
- **This API wrapper**: Open an issue in this repository
- **HerdNet model**: Visit https://github.com/Alexandre-Delplanque/HerdNet/issues
- **Model training**: Refer to the HerdNet documentation

## Additional Resources

- **HerdNet GitHub**: https://github.com/Alexandre-Delplanque/HerdNet
- **HerdNet Paper**: https://doi.org/10.1016/j.isprsjprs.2023.01.025
- **Colab Demo**: Available in the HerdNet repository
- **PyTorch Documentation**: https://pytorch.org/docs/
- **Flask Documentation**: https://flask.palletsprojects.com/

