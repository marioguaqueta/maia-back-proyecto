# Changelog

## [4.0.0] - Complete infer.py Integration - 2024-11-18

### 🎯 Major Overhaul
Complete refactor to integrate official HerdNet `infer.py` inference logic into the Flask API.

### Added
- ✅ **Official HerdNet Pipeline** - Uses `HerdNetEvaluator` and `HerdNetStitcher` (same as infer.py)
- ✅ **LMDS Detection** - Proper Local Maxima Detection System for accurate animal localization
- ✅ **Thumbnail Generation** - Automatic cropped images of each detection with species label and confidence
- ✅ **Plot Generation** - Annotated full images with detection markers
- ✅ **Base64 Encoding** - Images returned as base64 for easy web integration
- ✅ **Rotation Support** - `rotation` parameter for 90° image rotations (0-3)
- ✅ **Configurable Parameters** - All infer.py parameters exposed via API
  - `patch_size` - Size of patches for stitching (default: 512)
  - `overlap` - Overlap between patches (default: 160)
  - `rotation` - Number of 90° rotations (default: 0)
  - `thumbnail_size` - Size of thumbnails (default: 256)
  - `include_thumbnails` - Include thumbnail data (default: true)
  - `include_plots` - Include plot data (default: false)
- ✅ **Comprehensive Documentation**
  - `API_DOCUMENTATION.md` - Complete API reference
  - `INTEGRATION_SUMMARY.md` - Technical integration details
  - Updated `README.md` - Full project documentation
  - Updated `QUICKSTART.md` - Quick start guide
- ✅ **Enhanced Test Script** - test_api.py with full parameter support

### Changed
- 🔄 **Complete app.py Refactor** - Now uses exact infer.py logic
- 🔄 **Model Loading** - Loads checkpoint metadata (classes, mean, std)
- 🔄 **Dataset Preparation** - Uses CSVDataset with proper transforms
- 🔄 **Evaluation** - HerdNetEvaluator with stitcher and LMDS
- 🔄 **Response Format** - Includes summary, detections, thumbnails, and plots
- 🔄 **Dependencies** - Added pandas, kept albumentations, removed scipy

### Technical Details

#### Model Initialization
```python
checkpoint = torch.load(MODEL_PATH, map_location=map_location)
classes_dict = checkpoint['classes']
img_mean = checkpoint['mean']
img_std = checkpoint['std']
model = HerdNet(num_classes=num_classes, pretrained=False)
model = LossWrapper(model, [])
model.load_state_dict(checkpoint['model_state_dict'])
```

#### Dataset & Transforms
```python
end_transforms = [Rotate90(k=rotation), DownSample(down_ratio=2)]
albu_transforms = [A.Normalize(mean=img_mean, std=img_std)]
dataset = CSVDataset(csv_file=df, root_dir=dir, 
                     albu_transforms=albu_transforms,
                     end_transforms=end_transforms)
```

#### Evaluation Pipeline
```python
stitcher = HerdNetStitcher(model, size=(512,512), overlap=160)
evaluator = HerdNetEvaluator(model, dataloader, metrics,
                             lmds_kwargs=dict(kernel_size=(3,3)),
                             stitcher=stitcher)
evaluator.evaluate()
detections = evaluator.detections
```

### Removed
- ❌ Custom image patching logic
- ❌ Manual stitching implementation
- ❌ Custom local maxima detection (now uses official LMDS)
- ❌ scipy dependency (no longer needed)

### Performance
- ⚡ Same processing time as infer.py CLI
- ⚡ Identical detection accuracy
- ⚡ GPU acceleration support
- ⚡ Efficient batch processing

### Migration Guide
See `INTEGRATION_SUMMARY.md` for complete migration instructions from:
- Previous API version
- infer.py CLI script
- Custom implementations

### API Compatibility
- ✅ Backward compatible with ZIP file uploads
- ✅ New optional parameters (default values maintain previous behavior)
- ✅ Enhanced response format (previous fields still included)

---

## [3.0.0] - Batch Processing with ZIP Files

### Added
- ✅ **ZIP file upload support** - Process multiple images in a single request
- ✅ **Batch processing** - Analyze all images in the ZIP file automatically
- ✅ **Summary statistics** - Total images, successful analyses, animals detected
- ✅ **Individual results** - Detailed analysis for each image
- ✅ **Error handling per image** - Failed images don't stop batch processing
- ✅ **Helper script** (`create_test_zip.py`) to create test ZIP files
- ✅ **African wildlife classes** - Configured for buffalo, elephant, kob, topi, warthog, waterbuck

### Changed
- ✅ Endpoint now accepts `file` parameter (ZIP file) instead of `image`
- ✅ Response format includes summary and results array
- ✅ Updated test script to work with ZIP files
- ✅ Updated all documentation for batch processing
- ✅ Animal classes updated for African wildlife species

### Technical Improvements
- Uses `tempfile` for secure temporary file handling
- Automatic cleanup of extracted files
- Recursive search for images in ZIP subdirectories
- Graceful error handling for corrupted images

## [2.1.0] - HerdNet Integration

### Added
- ✅ Official HerdNet package integration from GitHub
- ✅ Proper model loading using `animaloc.models.load_model()`
- ✅ Installation script (`install_herdnet.sh`) for easy setup
- ✅ HerdNet dependencies (albumentations, opencv-python, PyYAML, hydra-core)
- ✅ Documentation about HerdNet architecture and paper citation

### Changed
- ✅ Updated model loading to use official HerdNet architecture
- ✅ Removed custom SimpleCNN class (replaced with proper HerdNet)
- ✅ Updated requirements.txt to install HerdNet from GitHub
- ✅ Enhanced README with HerdNet model information
- ✅ Updated QUICKSTART with HerdNet installation instructions

## [2.0.0] - Code Cleanup

### Removed
- ❌ All AWS S3 integration code
- ❌ boto3 dependency and related imports
- ❌ AWS credentials and environment variable requirements
- ❌ `/upload-file` endpoint
- ❌ S3 bucket configuration
- ❌ File upload functionality to S3
- ❌ UUID and datetime dependencies (no longer needed)
- ❌ werkzeug.utils imports (no longer needed)

### Changed
- ✅ `/analyze-image` endpoint now only analyzes images (no upload)
- ✅ Simplified response format (removed S3 URL, bucket, s3_key fields)
- ✅ Cleaner imports and dependencies
- ✅ Updated requirements.txt to include only necessary packages
- ✅ Updated all documentation (README.md, QUICKSTART.md)
- ✅ Updated test script to match new response format

### Kept
- ✅ PyTorch model loading and inference
- ✅ Animal detection functionality
- ✅ Image validation and preprocessing
- ✅ Multiple animal class support
- ✅ Confidence scores
- ✅ `/health` endpoint
- ✅ Error handling

## [1.0.0] - Initial Version

### Features
- Animal detection using HerdNet PyTorch model
- S3 integration for image storage
- Multiple animal class detection
- Confidence scores for predictions

