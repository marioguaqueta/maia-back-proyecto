# Batch Image Processing Guide

This guide explains how to use the batch processing feature to analyze multiple images at once using ZIP files.

## Overview

The API accepts ZIP files containing multiple images and processes them in a single request. This is ideal for:
- Analyzing aerial survey photos
- Processing batches of wildlife camera trap images
- Bulk animal detection and counting
- Efficient multi-image workflows

## Creating a ZIP File

### Method 1: Using the Helper Script

```bash
python create_test_zip.py /path/to/image/folder output.zip
```

Example:
```bash
python create_test_zip.py ./wildlife_photos ./wildlife_batch.zip
```

### Method 2: Command Line

**On macOS/Linux:**
```bash
# Create ZIP from a folder
zip -r images.zip /path/to/images/

# Create ZIP from specific files
zip images.zip image1.jpg image2.jpg image3.png
```

**On Windows:**
```powershell
# PowerShell
Compress-Archive -Path C:\images\* -DestinationPath images.zip
```

### Method 3: Python Script

```python
import zipfile
from pathlib import Path

def create_zip(image_folder, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for img_file in Path(image_folder).rglob('*.jpg'):
            zipf.write(img_file, img_file.name)

create_zip('./my_images', 'batch.zip')
```

## ZIP File Structure

Your ZIP file can have any structure:

```
images.zip
├── image1.jpg
├── image2.png
├── subfolder/
│   ├── image3.jpg
│   └── image4.png
└── another_folder/
    └── image5.jpg
```

All images will be found recursively regardless of folder structure.

## Sending the Request

### Using curl

```bash
curl -X POST http://localhost:8000/analyze-image \
  -F "file=@images.zip" \
  -o results.json
```

### Using Python

```python
import requests
import json

# Send ZIP file
with open('images.zip', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/analyze-image',
        files={'file': f}
    )

# Parse results
result = response.json()

# Print summary
print(f"Processed {result['summary']['total_images']} images")
print(f"Found animals in {result['summary']['images_with_animals']} images")

# Process individual results
for img_result in result['results']:
    if img_result['success']:
        analysis = img_result['analysis']
        if analysis['contains_animal']:
            print(f"{img_result['filename']}: {analysis['predicted_class']} "
                  f"({analysis['confidence']:.1%})")
```

### Using the Test Script

```bash
python test_api.py images.zip
```

## Response Format

```json
{
  "success": true,
  "zip_filename": "wildlife_photos.zip",
  "summary": {
    "total_images": 15,
    "successful_analyses": 14,
    "failed_analyses": 1,
    "images_with_animals": 10,
    "images_without_animals": 4
  },
  "model": {
    "name": "HerdNet",
    "device": "cpu",
    "num_classes": 7
  },
  "results": [
    {
      "filename": "buffalo_herd.jpg",
      "success": true,
      "analysis": {
        "contains_animal": true,
        "predicted_class": "buffalo",
        "confidence": 0.956,
        "detailed_predictions": [
          {"class": "buffalo", "confidence": 0.956, "class_id": 1},
          {"class": "waterbuck", "confidence": 0.023, "class_id": 6},
          {"class": "no_animal", "confidence": 0.015, "class_id": 0}
        ],
        "image_size": {"width": 4000, "height": 3000}
      }
    },
    {
      "filename": "corrupted_image.jpg",
      "success": false,
      "error": "cannot identify image file"
    }
  ]
}
```

## Processing Results

### Example: Count Animals by Species

```python
from collections import Counter

result = response.json()
species_count = Counter()

for img_result in result['results']:
    if img_result['success']:
        analysis = img_result['analysis']
        if analysis['contains_animal']:
            species_count[analysis['predicted_class']] += 1

print("Animals detected:")
for species, count in species_count.most_common():
    print(f"  {species}: {count}")
```

### Example: Export Results to CSV

```python
import csv

with open('results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Filename', 'Has Animal', 'Species', 'Confidence', 'Width', 'Height'])
    
    for img_result in result['results']:
        if img_result['success']:
            analysis = img_result['analysis']
            writer.writerow([
                img_result['filename'],
                analysis['contains_animal'],
                analysis['predicted_class'],
                f"{analysis['confidence']:.4f}",
                analysis['image_size']['width'],
                analysis['image_size']['height']
            ])
```

### Example: Filter High-Confidence Detections

```python
high_confidence = []

for img_result in result['results']:
    if img_result['success']:
        analysis = img_result['analysis']
        if analysis['contains_animal'] and analysis['confidence'] > 0.9:
            high_confidence.append({
                'filename': img_result['filename'],
                'species': analysis['predicted_class'],
                'confidence': analysis['confidence']
            })

print(f"Found {len(high_confidence)} high-confidence detections")
```

## Performance Considerations

### Processing Time
- **Per image**: ~0.5-2 seconds (depends on image size and hardware)
- **Batch of 50 images**: ~30-100 seconds
- **GPU acceleration**: 3-5x faster than CPU

### Optimal Batch Sizes
- **CPU**: 10-50 images per batch
- **GPU**: 50-200 images per batch
- **Memory considerations**: Larger images require more memory

### Tips for Large Batches
1. **Split very large batches**: Process 100-200 images at a time
2. **Use GPU if available**: Much faster processing
3. **Compress images**: Reduce ZIP file size for faster upload
4. **Monitor server resources**: Watch memory and CPU usage

## Error Handling

Individual image failures don't stop batch processing:

```python
# Check for failed analyses
failed = [r for r in result['results'] if not r['success']]

if failed:
    print(f"Failed to process {len(failed)} images:")
    for fail in failed:
        print(f"  {fail['filename']}: {fail['error']}")
```

## Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WEBP (.webp)
- BMP (.bmp)

Non-image files in the ZIP are automatically skipped.

## Limitations

- Maximum ZIP file size: Limited by server configuration (default ~100MB)
- Maximum images per batch: No hard limit, but consider performance
- Image size: Very large images (>10MB) may be slower to process
- Timeout: Long-running batches may timeout (adjust server timeout if needed)

## Best Practices

1. **Organize your images**: Use folders in the ZIP for better organization
2. **Name files meaningfully**: Helps identify results later
3. **Remove non-images**: Clean ZIPs process faster
4. **Test with small batches first**: Verify everything works before large batches
5. **Save results**: Store the JSON response for later analysis
6. **Monitor progress**: Server logs show per-image progress

## Example Workflow

```bash
# 1. Organize your images
mkdir wildlife_survey
cp *.jpg wildlife_survey/

# 2. Create ZIP file
python create_test_zip.py wildlife_survey survey.zip

# 3. Process with API
python test_api.py survey.zip > results.txt

# 4. Or use Python for programmatic access
python << EOF
import requests, json

with open('survey.zip', 'rb') as f:
    r = requests.post('http://localhost:8000/analyze-image', files={'file': f})

with open('results.json', 'w') as f:
    json.dump(r.json(), f, indent=2)

print("✓ Results saved to results.json")
EOF
```

## Troubleshooting

**ZIP file not accepted:**
- Ensure file has `.zip` extension
- Check ZIP file is not corrupted: `unzip -t file.zip`

**No images found:**
- Verify ZIP contains image files
- Check file extensions are supported
- Try extracting ZIP manually to verify contents

**Slow processing:**
- Reduce image size/resolution before zipping
- Use GPU if available
- Process smaller batches
- Check server resources (CPU/memory)

**Timeout errors:**
- Reduce batch size
- Increase server timeout setting
- Use faster hardware

For more information, see the main [README.md](README.md).

