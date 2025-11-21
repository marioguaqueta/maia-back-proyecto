# HerdNet Animal Detection API

A Flask-based REST API for detecting and analyzing African wildlife in aerial/satellite imagery using the HerdNet deep learning model.

## Features

- 🦁 **Multi-species Detection**: Detects 6 species of African wildlife (buffalo, elephant, kob, topi, warthog, waterbuck)
- 🗺️ **Large Image Support**: Processes large satellite images (6000x4000+) using intelligent stitching
- 📦 **Batch Processing**: Upload ZIP files with multiple images for batch analysis
- 🖼️ **Automatic Thumbnails**: Generates thumbnails of each detected animal
- 📊 **Detection Plots**: Creates annotated images showing detection locations
- 🔄 **Image Rotation**: Supports 90-degree rotation for different image orientations
- ⚙️ **Configurable Parameters**: Adjust patch size, overlap, and other inference parameters

## Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install HerdNet
pip install git+https://github.com/Alexandre-Delplanque/HerdNet.git

# Place your model file
# Copy herdnet_model.pth to the project root directory
```

### 2. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Test the API

```bash
# Test with default parameters
python test_api.py test_images.zip

# Test with custom parameters
python test_api.py test_images.zip --rotation 1 --patch-size 1024 --overlap 200
```

## API Endpoints

### Health Check

**GET** `/health`

Check if the API is running and model is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda",
  "num_classes": 7,
  "classes": {
    "0": "no_animal",
    "1": "buffalo",
    "2": "elephant",
    "3": "kob",
    "4": "topi",
    "5": "warthog",
    "6": "waterbuck"
  }
}
```

### Analyze Images

**POST** `/analyze-image`

Upload a ZIP file containing images for animal detection analysis.

**Request Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file` | File | Yes | - | ZIP file containing images |
| `patch_size` | Integer | No | 512 | Size of patches for stitching |
| `overlap` | Integer | No | 160 | Overlap between patches |
| `rotation` | Integer | No | 0 | Number of 90° rotations (0-3) |
| `thumbnail_size` | Integer | No | 256 | Size of generated thumbnails |
| `include_thumbnails` | Boolean | No | true | Include thumbnail data in response |
| `include_plots` | Boolean | No | false | Include plot data in response |

**Example Request (cURL):**

```bash
curl -X POST http://localhost:5000/analyze-image \
  -F "file=@test_images.zip" \
  -F "patch_size=512" \
  -F "overlap=160" \
  -F "rotation=0" \
  -F "thumbnail_size=256" \
  -F "include_thumbnails=true" \
  -F "include_plots=true"
```

**Example Request (Python):**

```python
import requests

with open('test_images.zip', 'rb') as f:
    files = {'file': f}
    data = {
        'patch_size': 512,
        'overlap': 160,
        'rotation': 0,
        'thumbnail_size': 256,
        'include_thumbnails': 'true',
        'include_plots': 'false'
    }
    response = requests.post(
        'http://localhost:5000/analyze-image',
        files=files,
        data=data
    )
    result = response.json()
```

**Response:**

```json
{
  "success": true,
  "message": "Images analyzed successfully",
  "summary": {
    "total_images": 5,
    "images_with_detections": 3,
    "images_without_detections": 2,
    "total_detections": 47,
    "species_counts": {
      "buffalo": 15,
      "elephant": 12,
      "waterbuck": 20
    }
  },
  "detections": [
    {
      "images": "image1.jpg",
      "x": 1234,
      "y": 5678,
      "labels": 1,
      "species": "buffalo",
      "scores": 0.95
    }
  ],
  "thumbnails": [
    {
      "image_name": "image1.jpg",
      "detection_id": 0,
      "species": "buffalo",
      "confidence": 0.95,
      "position": {"x": 1234, "y": 5678},
      "thumbnail_base64": "base64_encoded_image_data..."
    }
  ],
  "plots": [
    {
      "image_name": "image1.jpg",
      "plot_base64": "base64_encoded_plot_data..."
    }
  ],
  "processing_params": {
    "patch_size": 512,
    "overlap": 160,
    "rotation": 0,
    "thumbnail_size": 256
  }
}
```

## Parameter Guide

### Patch Size

Controls the size of image patches used for inference. Larger patches may capture more context but require more memory.

- **Small images (< 2000px)**: Not used, image processed as whole
- **Medium images (2000-4000px)**: 512-1024 recommended
- **Large images (> 4000px)**: 512-768 recommended

### Overlap

Overlap between patches in pixels. Higher overlap improves detection at patch boundaries but increases processing time.

- **Minimum**: 128px
- **Recommended**: 160-200px
- **High accuracy**: 256px

### Rotation

Number of 90-degree rotations to apply to images before processing. Useful for images captured at different orientations.

- `0`: No rotation (0°)
- `1`: 90° clockwise
- `2`: 180°
- `3`: 270° clockwise (90° counter-clockwise)

### Thumbnail Size

Size of the thumbnail crop around each detection in pixels.

- **Small**: 128px
- **Medium**: 256px (default)
- **Large**: 512px

## Model Information

This API uses the **HerdNet** model, a deep learning architecture specifically designed for detecting and counting animals in aerial imagery.

### Supported Species

1. Buffalo (*Syncerus caffer*)
2. Elephant (*Loxodonta africana*)
3. Kob (*Kobus kob*)
4. Topi (*Damaliscus lunatus*)
5. Warthog (*Phacochoerus africanus*)
6. Waterbuck (*Kobus ellipsiprymnus*)

### Model Citation

If you use this model in your research, please cite:

```
Delplanque, A., Foucher, S., Lejeune, P., Linchant, J., & Théau, J. (2022).
Multispecies detection and identification of African mammals in aerial imagery using convolutional neural networks.
Remote Sensing in Ecology and Conservation, 8(2), 166-179.
```

## Requirements

- Python 3.8+
- PyTorch 2.0+
- CUDA (optional, for GPU acceleration)
- 8GB+ RAM (16GB+ recommended for large images)
- Model file: `herdnet_model.pth`

## Project Structure

```
back/
├── app.py                    # Main Flask application
├── test_api.py              # API testing script
├── requirements.txt         # Python dependencies
├── herdnet_model.pth       # Model weights (not in repo)
├── README.md               # This file
└── docs/
    ├── API_DOCUMENTATION.md
    └── PARAMETER_TUNING.md
```

## Performance Tips

### For Large Images (> 4000px)

- Use patch_size=512 or 768
- Use overlap=160-200
- Enable GPU if available
- Process in batches of 10-20 images

### For Small Images (< 2000px)

- Images are processed whole (no patching)
- Faster processing
- No overlap needed

### Memory Considerations

- Larger patch sizes require more VRAM/RAM
- More overlap increases processing time linearly
- Thumbnails and plots increase response size significantly

## Troubleshooting

### Server won't start

- Check if port 5000 is available
- Ensure all dependencies are installed
- Verify `herdnet_model.pth` is in the project root

### Out of memory errors

- Reduce `patch_size` (e.g., from 1024 to 512)
- Process fewer images at once
- Disable GPU and use CPU

### Low detection accuracy

- Try different rotation values
- Increase overlap (e.g., 200 or 256)
- Ensure images are high quality

### Slow processing

- Enable GPU acceleration
- Reduce overlap
- Increase patch_size (if memory allows)
- Set `include_plots=false` and `include_thumbnails=false`

## License

This project uses the HerdNet model which is licensed under the MIT License.

## Support

For issues related to:
- **API**: Open an issue in this repository
- **HerdNet model**: Visit https://github.com/Alexandre-Delplanque/HerdNet
- **Model training**: Contact alexandre.delplanque@uliege.be

## Acknowledgments

- HerdNet model by Alexandre Delplanque (University of Liège)
- Based on research published in Remote Sensing in Ecology and Conservation
