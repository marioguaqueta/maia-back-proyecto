# Getting Started - Quick Reference

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Place Your Model
Ensure `herdnet_model.pth` is in the project root.

### 3. Run the Server
```bash
python app.py
```

Server starts at `http://localhost:8000`

## 📦 Create a Test ZIP File

```bash
# Put your images in a folder
mkdir test_images
cp *.jpg test_images/

# Create ZIP
python create_test_zip.py test_images test_batch.zip
```

## 🧪 Test the API

```bash
# Test the endpoint
python test_api.py test_batch.zip
```

## 📊 Expected Output

```
==================================================
Testing API at: http://localhost:8000
==================================================
Testing health endpoint...
Status: 200
Response: {'status': 'ok'}
✓ Health check passed

Analyzing ZIP file: test_batch.zip
Status: 200

======================================================================
BATCH ANALYSIS SUMMARY
======================================================================
ZIP file: test_batch.zip

Total images: 10
Successful analyses: 10
Failed analyses: 0
Images with animals: 7
Images without animals: 3

Model: HerdNet
Device: cpu
Classes: 7

======================================================================
INDIVIDUAL RESULTS
======================================================================

[1/10] image1.jpg
  ✓ ANIMAL DETECTED: buffalo
    Confidence: 95.6%
    Top prediction: buffalo (95.6%)
    Image size: 4000x3000

[2/10] image2.jpg
  ✓ ANIMAL DETECTED: elephant
    Confidence: 92.3%
    Top prediction: elephant (92.3%)
    Image size: 3840x2160

...
```

## 🌐 Using curl

```bash
# Upload and analyze
curl -X POST http://localhost:8000/analyze-image \
  -F "file=@test_batch.zip" \
  | json_pp
```

## 🐍 Using Python

```python
import requests

# Send ZIP file
with open('test_batch.zip', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/analyze-image',
        files={'file': f}
    )

# Get results
result = response.json()
print(f"Processed {result['summary']['total_images']} images")
print(f"Found animals in {result['summary']['images_with_animals']} images")

# Show detections
for img in result['results']:
    if img['success'] and img['analysis']['contains_animal']:
        print(f"  {img['filename']}: {img['analysis']['predicted_class']} "
              f"({img['analysis']['confidence']:.1%})")
```

## 🎯 Detected Species

- Buffalo (African buffalo)
- Elephant (African elephants)
- Kob (Kob antelopes)
- Topi (Topi antelopes)
- Warthog
- Waterbuck
- Other animals

## 📝 Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run server (development)
python app.py

# Run server (production)
gunicorn --bind 0.0.0.0:8000 app:app

# Create test ZIP
python create_test_zip.py <image_folder> <output.zip>

# Test API
python test_api.py <zip_file>

# Check health
curl http://localhost:8000/health
```

## 🐛 Troubleshooting

**"ModuleNotFoundError: No module named 'animaloc'"**
```bash
pip install git+https://github.com/Alexandre-Delplanque/HerdNet.git
```

**"Model file not found"**
- Ensure `herdnet_model.pth` is in the same directory as `app.py`

**"No images found in ZIP"**
- Check ZIP contains image files (.jpg, .png, etc.)
- Try: `unzip -l test.zip` to list contents

## 📚 Full Documentation

- **README.md** - Complete API documentation
- **QUICKSTART.md** - Detailed quick start
- **BATCH_PROCESSING.md** - Batch processing guide
- **MODEL_INFO.md** - About HerdNet model
- **SETUP_INSTRUCTIONS.md** - Installation guide
- **IMPLEMENTATION_SUMMARY.md** - Technical overview

## 🎓 Next Steps

1. Read [BATCH_PROCESSING.md](BATCH_PROCESSING.md) for advanced usage
2. See [MODEL_INFO.md](MODEL_INFO.md) for model details
3. Check [README.md](README.md) for full API reference

---

**Need Help?** Check the documentation files listed above.

