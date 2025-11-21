# Quick Start Guide - HerdNet Animal Detection API

Get up and running with the HerdNet Animal Detection API in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- `herdnet_model.pth` model file

## Step 1: Install Dependencies (2 minutes)

```bash
# Install Python packages
pip install -r requirements.txt

# Install HerdNet from GitHub
pip install git+https://github.com/Alexandre-Delplanque/HerdNet.git
```

**Alternative (if pip install fails):**

```bash
# Clone and install HerdNet manually
git clone https://github.com/Alexandre-Delplanque/HerdNet.git
cd HerdNet
pip install -e .
cd ..
```

## Step 2: Place Model File (30 seconds)

Copy your `herdnet_model.pth` file to the project root directory:

```bash
# Your directory structure should look like:
back/
├── app.py
├── herdnet_model.pth  ← Model file here
├── requirements.txt
└── ...
```

## Step 3: Start the Server (10 seconds)

```bash
python app.py
```

You should see:

```
Loading HerdNet PyTorch model...
Using device: cuda
Model loaded successfully with 7 classes
Starting Flask server...
```

The server is now running at `http://localhost:5000`

## Step 4: Test the API (1 minute)

### Option A: Use the Test Script

```bash
# Create a test ZIP file with your images
python create_test_zip.py /path/to/your/images test_images.zip

# Run the test
python test_api.py test_images.zip
```

### Option B: Use cURL

```bash
# First, create a ZIP file with some images
zip test_images.zip image1.jpg image2.jpg image3.jpg

# Then test the API
curl -X POST http://localhost:5000/analyze-image \
  -F "file=@test_images.zip"
```

### Option C: Use Python

```python
import requests

with open('test_images.zip', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/analyze-image',
        files={'file': f}
    )
    result = response.json()
    
print(f"Total detections: {result['summary']['total_detections']}")
print(f"Species found: {list(result['summary']['species_counts'].keys())}")
```

## Expected Output

```
✓ Analysis complete!
  Total detections: 47
  Images with animals: 3/5
  Species found: ['buffalo', 'elephant', 'waterbuck']
```

## What's Next?

### Adjust Parameters for Better Results

Try different rotation angles if your images are sideways:

```bash
python test_api.py test_images.zip --rotation 1
```

Try larger patches for better context on large images:

```bash
python test_api.py test_images.zip --patch-size 1024 --overlap 200
```

### Get Thumbnails and Plots

```bash
python test_api.py test_images.zip --include-plots
```

This will save:
- `api_response.json` - Full API response
- `output_thumbnails/` - Individual animal thumbnails
- `output_plots/` - Annotated images with detections

### Integrate into Your Application

**Python:**

```python
import requests
import base64
from PIL import Image
from io import BytesIO

def analyze_wildlife_images(zip_path):
    with open(zip_path, 'rb') as f:
        files = {'file': f}
        data = {
            'patch_size': 512,
            'overlap': 160,
            'include_thumbnails': 'true'
        }
        response = requests.post(
            'http://localhost:5000/analyze-image',
            files=files,
            data=data
        )
    
    result = response.json()
    
    # Get summary
    summary = result['summary']
    print(f"Found {summary['total_detections']} animals!")
    
    # Save first thumbnail
    if result['thumbnails']:
        thumb = result['thumbnails'][0]
        img_data = base64.b64decode(thumb['thumbnail_base64'])
        img = Image.open(BytesIO(img_data))
        img.save('first_detection.jpg')
    
    return result

# Usage
result = analyze_wildlife_images('wildlife.zip')
```

**JavaScript/Node.js:**

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function analyzeWildlifeImages(zipPath) {
    const formData = new FormData();
    formData.append('file', fs.createReadStream(zipPath));
    formData.append('patch_size', '512');
    formData.append('overlap', '160');
    
    const response = await axios.post(
        'http://localhost:5000/analyze-image',
        formData,
        { headers: formData.getHeaders() }
    );
    
    const result = response.data;
    console.log(`Found ${result.summary.total_detections} animals!`);
    
    return result;
}

// Usage
analyzeWildlifeImages('wildlife.zip');
```

## Common Parameters

| Parameter | Default | Description | When to Change |
|-----------|---------|-------------|----------------|
| `patch_size` | 512 | Size of image patches | Large images: try 768-1024 |
| `overlap` | 160 | Patch overlap | More accuracy: try 200-256 |
| `rotation` | 0 | 90° rotations | Sideways images: try 1-3 |
| `thumbnail_size` | 256 | Thumbnail crop size | Larger animals: try 512 |

## Troubleshooting

### Server won't start

```bash
# Check if port 5000 is in use
lsof -i :5000

# Use a different port
# Edit app.py, change the last line to:
app.run(host="0.0.0.0", port=8000, debug=True)
```

### Model not found error

```bash
# Check if model file exists
ls -lh herdnet_model.pth

# If missing, copy it to the project root
cp /path/to/herdnet_model.pth .
```

### Out of memory

```python
# Use smaller patch size
python test_api.py test.zip --patch-size 512

# Or force CPU mode (edit app.py):
device = torch.device("cpu")  # Instead of "cuda"
```

### No detections found

- Try different rotation values (0, 1, 2, 3)
- Ensure images contain the supported species
- Check image quality and resolution
- Increase overlap for better boundary detection

## Next Steps

1. **Read the full documentation:**
   - `README.md` - Complete project overview
   - `API_DOCUMENTATION.md` - Detailed API reference

2. **Optimize for your use case:**
   - Experiment with different parameters
   - Profile your typical image sizes
   - Adjust batch sizes for your hardware

3. **Production deployment:**
   - Use gunicorn instead of Flask development server
   - Add authentication and rate limiting
   - Set up proper logging and monitoring
   - Consider using a task queue for async processing

## Production Deployment (Bonus)

For production use:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 300 app:app
```

Or with Docker:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/Alexandre-Delplanque/HerdNet.git
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "300", "app:app"]
```

## Need Help?

- Check `README.md` for more details
- See `API_DOCUMENTATION.md` for complete API reference
- Review `TROUBLESHOOTING.md` for common issues
- Open an issue on GitHub

---

**That's it! You're ready to detect wildlife in aerial imagery! 🦁🐘🦌**
