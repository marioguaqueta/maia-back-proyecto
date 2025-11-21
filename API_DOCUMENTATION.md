# HerdNet API - Complete Documentation

## Overview

The HerdNet Animal Detection API provides a RESTful interface for detecting African wildlife in aerial and satellite imagery. The API uses the HerdNet deep learning model and implements the same inference logic as the original `infer.py` script from the HerdNet project.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, no authentication is required. This is suitable for local development and internal use.

---

## Endpoints

### 1. Health Check

Check if the API is running and the model is loaded correctly.

**Endpoint:** `GET /health`

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

**Status Codes:**
- `200 OK`: API is healthy and ready
- `500 Internal Server Error`: API is not properly initialized

---

### 2. Analyze Images

Upload a ZIP file containing images for animal detection and analysis.

**Endpoint:** `POST /analyze-image`

**Content-Type:** `multipart/form-data`

#### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file` | File | ✅ Yes | - | ZIP file containing JPG/JPEG/PNG images |
| `patch_size` | Integer | No | 512 | Size of patches for stitching (pixels) |
| `overlap` | Integer | No | 160 | Overlap between patches (pixels) |
| `rotation` | Integer | No | 0 | Number of 90° rotations to apply (0-3) |
| `thumbnail_size` | Integer | No | 256 | Size of thumbnails around detections (pixels) |
| `include_thumbnails` | Boolean | No | true | Include base64-encoded thumbnails in response |
| `include_plots` | Boolean | No | false | Include base64-encoded annotated plots in response |

#### Parameter Details

##### `patch_size`
- **Range:** 256 - 2048
- **Recommended:** 512 (default), 768, or 1024
- **Notes:** 
  - Larger values require more memory but may improve context
  - Must be divisible by 32
  - For images smaller than this size, no patching is applied

##### `overlap`
- **Range:** 64 - 512
- **Recommended:** 160 (default) or 200
- **Notes:**
  - Higher values improve detection at patch boundaries
  - Increases processing time linearly
  - Should be at least 25% of patch_size

##### `rotation`
- **Values:** 0, 1, 2, or 3
- **0:** No rotation (0°)
- **1:** Rotate 90° clockwise
- **2:** Rotate 180°
- **3:** Rotate 270° clockwise (90° counter-clockwise)
- **Notes:** Useful when images are captured at different orientations

##### `thumbnail_size`
- **Range:** 64 - 512
- **Recommended:** 256 (default)
- **Notes:** Size of the square crop around each detection

##### `include_thumbnails`
- **Values:** "true" or "false" (string)
- **Notes:** 
  - Set to "false" to reduce response size
  - Thumbnails are base64-encoded JPEG images

##### `include_plots`
- **Values:** "true" or "false" (string)
- **Notes:**
  - Set to "true" to get annotated images with detection markers
  - Significantly increases response size
  - Plots are base64-encoded JPEG images

#### Request Examples

##### cURL

```bash
# Basic request
curl -X POST http://localhost:5000/analyze-image \
  -F "file=@wildlife_images.zip"

# With custom parameters
curl -X POST http://localhost:5000/analyze-image \
  -F "file=@wildlife_images.zip" \
  -F "patch_size=1024" \
  -F "overlap=200" \
  -F "rotation=1" \
  -F "thumbnail_size=512" \
  -F "include_thumbnails=true" \
  -F "include_plots=true"

# Minimal response (no images)
curl -X POST http://localhost:5000/analyze-image \
  -F "file=@wildlife_images.zip" \
  -F "include_thumbnails=false" \
  -F "include_plots=false"
```

##### Python (requests library)

```python
import requests

# Basic request
with open('wildlife_images.zip', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:5000/analyze-image',
        files=files
    )
    result = response.json()

# With custom parameters
with open('wildlife_images.zip', 'rb') as f:
    files = {'file': f}
    data = {
        'patch_size': 1024,
        'overlap': 200,
        'rotation': 1,
        'thumbnail_size': 512,
        'include_thumbnails': 'true',
        'include_plots': 'true'
    }
    response = requests.post(
        'http://localhost:5000/analyze-image',
        files=files,
        data=data,
        timeout=300  # 5 minutes
    )
    result = response.json()
```

##### JavaScript (fetch API)

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('patch_size', '512');
formData.append('overlap', '160');
formData.append('rotation', '0');
formData.append('include_thumbnails', 'true');
formData.append('include_plots', 'false');

fetch('http://localhost:5000/analyze-image', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

#### Response Structure

##### Success Response (200 OK)

```json
{
  "success": true,
  "message": "Images analyzed successfully",
  "summary": {
    "total_images": 10,
    "images_with_detections": 7,
    "images_without_detections": 3,
    "total_detections": 142,
    "species_counts": {
      "buffalo": 45,
      "elephant": 23,
      "kob": 38,
      "waterbuck": 36
    }
  },
  "detections": [
    {
      "images": "IMG_001.JPG",
      "x": 1234.5,
      "y": 5678.9,
      "labels": 1,
      "species": "buffalo",
      "scores": 0.9543
    },
    {
      "images": "IMG_001.JPG",
      "x": 2345.6,
      "y": 6789.0,
      "labels": 2,
      "species": "elephant",
      "scores": 0.8923
    }
  ],
  "thumbnails": [
    {
      "image_name": "IMG_001.JPG",
      "detection_id": 0,
      "species": "buffalo",
      "confidence": 0.9543,
      "position": {
        "x": 1234,
        "y": 5678
      },
      "thumbnail_base64": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBD..."
    }
  ],
  "plots": [
    {
      "image_name": "IMG_001.JPG",
      "plot_base64": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBD..."
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

##### Field Descriptions

**`summary` object:**
- `total_images`: Total number of valid images found in the ZIP file
- `images_with_detections`: Number of images containing at least one detection
- `images_without_detections`: Number of images with no detections
- `total_detections`: Total number of animal detections across all images
- `species_counts`: Dictionary mapping species name to detection count

**`detections` array:** List of all detections, each containing:
- `images`: Filename of the image
- `x`: X-coordinate of detection center (in original image pixels)
- `y`: Y-coordinate of detection center (in original image pixels)
- `labels`: Numeric class label (1-6)
- `species`: Species name (string)
- `scores`: Confidence score (0.0 - 1.0)

**`thumbnails` array:** (if `include_thumbnails=true`) List of thumbnail data:
- `image_name`: Source image filename
- `detection_id`: Sequential ID for this detection in the image
- `species`: Detected species name
- `confidence`: Confidence score (0.0 - 1.0)
- `position`: Object with `x` and `y` coordinates
- `thumbnail_base64`: Base64-encoded JPEG image data

**`plots` array:** (if `include_plots=true`) List of annotated plot data:
- `image_name`: Source image filename
- `plot_base64`: Base64-encoded JPEG image with detection markers

**`processing_params` object:** Echo of the processing parameters used

##### Error Responses

**400 Bad Request** - Invalid input

```json
{
  "error": "No file provided"
}
```

```json
{
  "error": "File must be a ZIP archive"
}
```

**500 Internal Server Error** - Processing failed

```json
{
  "success": false,
  "error": "Analysis failed",
  "message": "No images found in the uploaded zip file"
}
```

```json
{
  "success": false,
  "error": "Analysis failed",
  "message": "Out of memory error: reduce patch_size or use CPU"
}
```

#### Status Codes

- `200 OK`: Analysis completed successfully
- `400 Bad Request`: Invalid request (missing file, wrong file type, etc.)
- `500 Internal Server Error`: Server error during processing

---

## Working with Response Data

### Extracting Thumbnails

Thumbnails are provided as base64-encoded JPEG images. Here's how to decode them:

**Python:**

```python
import base64
from PIL import Image
from io import BytesIO

# Get response
result = response.json()

# Save thumbnails
for thumb in result['thumbnails']:
    img_data = base64.b64decode(thumb['thumbnail_base64'])
    img = Image.open(BytesIO(img_data))
    
    filename = f"{thumb['image_name']}_{thumb['detection_id']}_{thumb['species']}.jpg"
    img.save(filename)
```

**JavaScript:**

```javascript
// Convert base64 to Blob and display in browser
const base64Data = thumbnail.thumbnail_base64;
const blob = base64ToBlob(base64Data, 'image/jpeg');
const url = URL.createObjectURL(blob);

const img = document.createElement('img');
img.src = url;
document.body.appendChild(img);

function base64ToBlob(base64, type = 'image/jpeg') {
  const binary = atob(base64);
  const array = [];
  for (let i = 0; i < binary.length; i++) {
    array.push(binary.charCodeAt(i));
  }
  return new Blob([new Uint8Array(array)], { type });
}
```

### Exporting Detections to CSV

```python
import pandas as pd

# Get response
result = response.json()
detections = result['detections']

# Create DataFrame
df = pd.DataFrame(detections)

# Save to CSV
df.to_csv('detections.csv', index=False)
```

### Creating Detection Summary Report

```python
def create_summary_report(result):
    """Generate a text summary of detection results"""
    summary = result['summary']
    
    report = f"""
Animal Detection Summary
========================

Total Images Processed: {summary['total_images']}
Images with Animals: {summary['images_with_detections']}
Images without Animals: {summary['images_without_detections']}
Total Detections: {summary['total_detections']}

Species Breakdown:
"""
    
    for species, count in sorted(summary['species_counts'].items(), 
                                  key=lambda x: x[1], reverse=True):
        percentage = (count / summary['total_detections']) * 100
        report += f"  {species}: {count} ({percentage:.1f}%)\n"
    
    return report

# Usage
print(create_summary_report(result))
```

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider:
- Adding rate limiting middleware
- Implementing request queuing
- Setting up authentication

## Best Practices

### Request Optimization

1. **Use appropriate parameters:**
   - Start with defaults
   - Adjust based on results
   - Balance accuracy vs. speed

2. **Minimize response size:**
   - Set `include_plots=false` unless needed
   - Set `include_thumbnails=false` for large batches
   - Process images in smaller batches

3. **Handle timeouts:**
   - Set appropriate timeout values (5+ minutes for large batches)
   - Implement retry logic with exponential backoff

### Error Handling

```python
import requests
from requests.exceptions import Timeout, ConnectionError

def analyze_images_with_retry(zip_path, max_retries=3):
    """Analyze images with retry logic"""
    for attempt in range(max_retries):
        try:
            with open(zip_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    'http://localhost:5000/analyze-image',
                    files=files,
                    timeout=300
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 400:
                    # Don't retry on bad request
                    print(f"Error: {response.json()}")
                    return None
                else:
                    # Retry on server error
                    print(f"Attempt {attempt + 1} failed, retrying...")
                    
        except (Timeout, ConnectionError) as e:
            print(f"Network error on attempt {attempt + 1}: {e}")
            
    print("Max retries exceeded")
    return None
```

## Performance Expectations

### Processing Times (Approximate)

| Scenario | Images | Total Pixels | Time (GPU) | Time (CPU) |
|----------|--------|--------------|------------|------------|
| Small batch | 10 | 2000x2000 each | 30-60s | 2-5 min |
| Medium batch | 50 | 2000x2000 each | 3-5 min | 15-30 min |
| Large images | 5 | 6000x4000 each | 2-4 min | 10-20 min |
| Mixed batch | 20 | Various sizes | 2-6 min | 10-30 min |

**Note:** Times vary based on:
- Hardware (GPU model, RAM, CPU)
- Parameter settings (patch_size, overlap)
- Image complexity (density of animals)
- Number of detections (thumbnail generation)

## Troubleshooting

### Common Issues

**1. "No file provided" error**
- Ensure the form field name is exactly "file"
- Check that the file is properly attached to the request

**2. "File must be a ZIP archive" error**
- Verify the file has a `.zip` extension
- Ensure the file is actually a valid ZIP archive

**3. "No images found in the uploaded zip file" error**
- Check that the ZIP contains JPG/JPEG/PNG files
- Ensure images are not in nested subdirectories
- Verify image file extensions are correct

**4. Timeout errors**
- Increase the timeout value
- Reduce the number of images in the batch
- Reduce patch_size or overlap

**5. Out of memory errors**
- Reduce patch_size (e.g., from 1024 to 512)
- Use CPU instead of GPU
- Process fewer images at once
- Reduce thumbnail_size

## Support

For additional help or to report issues:
- Check the main README.md for troubleshooting tips
- Review the HerdNet documentation
- Open an issue in the project repository

