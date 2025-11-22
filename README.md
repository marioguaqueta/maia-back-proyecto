# African Wildlife Detection API

A Flask-based REST API for detecting and analyzing African wildlife in aerial/satellite imagery using **YOLOv11** and **HerdNet** deep learning models, with a modern Streamlit web interface.

## ✨ Features

### Core Detection
- 🦁 **Dual Model Support**: Choose between YOLOv11 (bounding boxes) or HerdNet (point detection)
- 🎯 **YOLOv11 Detection**: Fast, accurate bounding box detection with annotated images
- 📍 **HerdNet Detection**: Precise point-based detection optimized for aerial imagery
- 🗺️ **Large Image Support**: Processes large satellite images (6000x4000+) using intelligent stitching
- 📦 **Batch Processing**: Upload ZIP files with multiple images for batch analysis
- 🖼️ **Single Image Analysis**: Upload individual images (PNG, JPG, GIF, WebP, BMP, TIFF) for quick testing
- ⚡ **Flexible Input**: Choose between ZIP (batch) or single image based on your needs

### Data Management
- 💾 **Database Storage**: SQLite database stores all analysis tasks and complete results
- 🔍 **Task Tracking**: Each analysis gets a unique task_id for easy retrieval
- 📈 **Statistics**: View comprehensive statistics about all analyses

### User Interfaces
- 🌐 **Streamlit Web UI**: Beautiful, easy-to-use web interface
- 🔌 **REST API**: Full-featured REST API for programmatic access
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile

### Deployment
- ☁️ **Cloud-Ready**: Models download automatically from Google Drive
- 🚀 **Easy Setup**: No large files in repository
- 📦 **Streamlit Cloud Compatible**: Ready for cloud deployment

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd back

# Install dependencies
pip install -r requirements.txt

# Install HerdNet
pip install git+https://github.com/Alexandre-Delplanque/HerdNet.git
```

**Note:** Model files (`best.pt` and `herdnet_model.pth`) will be **automatically downloaded from Google Drive** on first run!

### 2. Start the System

**Option A: Using the startup script (Recommended)**

```bash
# On Linux/Mac
./start.sh

# On Windows
start.bat
```

**Option B: Manual start (two terminals)**

Terminal 1 - Backend:
```bash
python app.py
```

Terminal 2 - Frontend:
```bash
streamlit run streamlit_app.py
```

### 3. Access the Application

- **🌐 Web Interface:** http://localhost:8501 (Streamlit UI)
- **🔌 API Endpoint:** http://localhost:8000 (Flask API)

## 🎯 Which Model Should I Use?

### Use YOLOv11 if you want:
- ✅ Fast processing (1-2 seconds per image)
- ✅ Bounding boxes around animals
- ✅ Standard image sizes
- ✅ Real-time detection capabilities
- ✅ Simple, straightforward output

### Use HerdNet if you want:
- ✅ Very large satellite images (6000x4000+)
- ✅ Precise center-point locations
- ✅ Individual animal thumbnails
- ✅ Scientific-grade accuracy
- ✅ Optimized aerial imagery processing

**💡 Tip:** Try both models and compare results!

## 🌐 Using the Streamlit Interface

The Streamlit web interface provides a beautiful, card-based UI for easy system access:

### 📁 New Analysis Page
1. Upload a ZIP file with wildlife images
2. Select YOLOv11 or HerdNet model
3. Configure parameters (confidence, patch size, etc.)
4. Click "Run Analysis"
5. **View results in modern card layout:**
   - 🖼️ **Image Cards**: Each image in its own styled card
   - 🎯 **Detection Badges**: Color-coded counts and dimensions
   - 📊 **Collapsible Tables**: Expandable detection details per image
   - 🔍 **Interactive Viewer**: Full-size view with zoom & pan
   - ⬇️ **Quick Download**: Direct download from each card
6. Save the task_id to retrieve results later

### 📊 View Results Page
- Browse all past analyses
- Filter by model type and status
- View full JSON results in card format
- See processing statistics

### 📈 Statistics Page
- View aggregate statistics
- Species distribution charts
- Analysis trends over time
- Model usage comparison

### ℹ️ About Page
- Model information and comparisons
- Supported species
- Citation information

### 🎨 Card-Based UI Features
- **2-Column Grid Layout**: Gallery-style image browsing
- **Hover Effects**: Smooth animations and shadows
- **Responsive Design**: Adapts to screen size
- **Collapsible Details**: Keep UI clean, expand when needed
- **Integrated Actions**: View and download directly from cards

For more details, see [`CARD_UI_DESIGN.md`](CARD_UI_DESIGN.md)

## 🔌 API Endpoints

### Health Check

**GET** `/health`

Check if the API is running and models are loaded.

```json
{
  "status": "healthy",
  "models": {
    "herdnet": {"loaded": true, "num_classes": 7},
    "yolov11": {"loaded": true, "num_classes": 6}
  }
}
```

### Analyze with YOLO

**POST** `/analyze-yolo`

Upload a ZIP file for YOLOv11 analysis.

**Parameters:**
- `file`: ZIP file with images (required)
- `conf_threshold`: Confidence threshold (default: 0.25)
- `iou_threshold`: IOU threshold for NMS (default: 0.45)
- `img_size`: Image size for inference (default: 640)
- `include_annotated_images`: Include annotated images (default: true)

**Response:**
```json
{
  "success": true,
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "model": "YOLOv11",
  "summary": {
    "total_images": 5,
    "total_detections": 47,
    "species_counts": {"buffalo": 15, "elephant": 12}
  },
  "detections": [...],
  "annotated_images": [...],
  "processing_time_seconds": 12.5
}
```

### Analyze with HerdNet

**POST** `/analyze-image`

Upload a ZIP file for HerdNet analysis.

**Parameters:**
- `file`: ZIP file with images (required)
- `patch_size`: Patch size for stitching (default: 512)
- `overlap`: Overlap for stitching (default: 160)
- `rotation`: Number of 90-degree rotations (default: 0)
- `thumbnail_size`: Size for thumbnails (default: 256)
- `include_thumbnails`: Include thumbnails (default: true)
- `include_plots`: Include detection plots (default: false)

**Response:**
```json
{
  "success": true,
  "task_id": "456e7890-e89b-12d3-a456-426614174111",
  "model": "HerdNet",
  "summary": {
    "total_images": 5,
    "total_detections": 82,
    "species_counts": {"buffalo": 25, "elephant": 18}
  },
  "detections": [...],
  "thumbnails": [...],
  "processing_time_seconds": 45.8
}
```

### Analyze Single Image with YOLO

**POST** `/analyze-single-image-yolo`

Upload a single image for YOLOv11 analysis.

**Parameters:**
- `file`: Single image file (PNG, JPG, JPEG, GIF, WebP, BMP, TIFF) (required)
- `conf_threshold`: Confidence threshold (default: 0.25)
- `iou_threshold`: IOU threshold for NMS (default: 0.45)
- `img_size`: Image size for inference (default: 640)
- `include_annotated_images`: Include annotated images (default: true)

**Response:** Same format as batch analysis, but with `total_images: 1`

### Analyze Single Image with HerdNet

**POST** `/analyze-single-image-herdnet`

Upload a single image for HerdNet analysis (optimized for large aerial/satellite images).

**Parameters:**
- `file`: Single image file (PNG, JPG, JPEG, GIF, WebP, BMP, TIFF) (required)
- `patch_size`: Patch size for stitching (default: 512)
- `overlap`: Overlap for stitching (default: 160)
- `rotation`: Number of 90-degree rotations (default: 0)
- `thumbnail_size`: Size for thumbnails (default: 256)
- `include_thumbnails`: Include thumbnails (default: true)
- `include_plots`: Include detection plots (default: false)

**Response:** Same format as batch analysis, but with `total_images: 1`

**💡 Tip:** Use single image endpoints for quick testing or when you need real-time analysis without creating ZIP files!

### Get Tasks

**GET** `/tasks`

List all analysis tasks with optional filtering.

**Query Parameters:**
- `model_type`: Filter by 'yolo' or 'herdnet'
- `status`: Filter by 'completed', 'processing', or 'failed'
- `limit`: Maximum tasks to return (default: 100)
- `offset`: Pagination offset (default: 0)

### Get Task by ID

**GET** `/tasks/<task_id>`

Retrieve a specific task and its complete results.

**Response includes:**
- Task metadata (status, timestamps, parameters)
- Complete JSON response with all detections
- All base64-encoded images (if included in original request)

### Database Statistics

**GET** `/database/stats`

Get comprehensive database statistics.

```json
{
  "success": true,
  "statistics": {
    "total_tasks": 150,
    "tasks_by_model": {"yolo": 85, "herdnet": 65},
    "total_detections": 8547,
    "species_distribution": {"buffalo": 2341, "elephant": 1876}
  }
}
```

## 💾 Database Features

### What Gets Stored

Every analysis automatically stores:

**For YOLO:**
- ✅ All detection data (coordinates, confidence, species)
- ✅ Complete bounding box information
- ✅ **All annotated images as base64** (if requested)
- ✅ Summary statistics and processing parameters

**For HerdNet:**
- ✅ All detection data (center points, confidence, species)
- ✅ **All animal thumbnails as base64** (if requested)
- ✅ **All detection plots as base64** (if requested)
- ✅ Summary statistics and processing parameters

### Workflow Example

```python
import requests

# 1. Run analysis
response = requests.post('http://localhost:8000/analyze-yolo', 
    files={'file': open('images.zip', 'rb')})
task_id = response.json()['task_id']

# 2. Retrieve complete results later (even after server restart)
task_response = requests.get(f'http://localhost:8000/tasks/{task_id}')
task = task_response.json()['task']

# Access the complete original JSON response
original_response = task['result_data']
base64_images = original_response.get('annotated_images', [])

# 3. Get only detections
detections = requests.get(f'http://localhost:8000/tasks/{task_id}/detections')

# 4. View statistics
stats = requests.get('http://localhost:8000/database/stats')
```

## ☁️ Google Drive Model Loading

Models are automatically downloaded from Google Drive on first run. This makes deployment to cloud platforms like Streamlit Cloud easy without committing large model files to the repository.

**Features:**
- ✅ Automatic download on first run
- ✅ Cached locally for subsequent runs
- ✅ No manual download required
- ✅ Perfect for Streamlit Cloud deployment

**Model Files:**
- `best.pt` (YOLOv11) - ~300 MB
- `herdnet_model.pth` (HerdNet) - ~250 MB

## 📊 Model Information

### YOLOv11
- **Type:** Bounding box object detection
- **Speed:** Fast (~1-2s per image)
- **Best for:** Standard images, real-time detection
- **Output:** Bounding boxes with confidence scores

### HerdNet
- **Type:** Point-based detection
- **Speed:** Moderate (depends on image size)
- **Best for:** Large aerial/satellite images
- **Output:** Center points, thumbnails, plots

### Supported Species
1. Buffalo (*Syncerus caffer*)
2. Elephant (*Loxodonta africana*)
3. Kob (*Kobus kob*)
4. Topi (*Damaliscus lunatus*)
5. Warthog (*Phacochoerus africanus*)
6. Waterbuck (*Kobus ellipsiprymnus*)

## 🛠️ Project Structure

```
back/
├── app.py                    # Main Flask API
├── streamlit_app.py          # Streamlit web interface
├── database.py               # SQLite database module
├── model_loader.py           # Google Drive model downloader
├── test_api.py              # API testing script
├── test_yolo_api.py         # YOLO testing script
├── start.sh                 # Unix startup script
├── start.bat                # Windows startup script
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── best.pt                 # YOLOv11 model (auto-downloaded)
├── herdnet_model.pth      # HerdNet model (auto-downloaded)
└── wildlife_detection.db  # SQLite database (auto-created)
```

## 🚀 Deployment

### Local Deployment
Use the startup scripts for easy local deployment:
```bash
./start.sh  # Linux/Mac
start.bat   # Windows
```

### Cloud Deployment

The system has two components that need separate deployment:

1. **Flask Backend** → Railway, Heroku, or Render
2. **Streamlit Frontend** → Streamlit Cloud (free!)

**📖 See [STREAMLIT_DEPLOYMENT_GUIDE.md](STREAMLIT_DEPLOYMENT_GUIDE.md) for detailed step-by-step instructions!**

Quick summary:
- Use `requirements-backend.txt` for Flask backend
- Use `requirements-streamlit.txt` for Streamlit frontend  
- Configure `API_BASE_URL` in Streamlit secrets to point to your backend
- Models auto-download from Google Drive on first run

### Docker
Docker deployment is supported. See `Dockerfile` for configuration.

## 📝 Requirements

- Python 3.8+
- PyTorch 2.0+
- CUDA (optional, for GPU acceleration)
- 8GB+ RAM (16GB+ recommended)

## 🐛 Troubleshooting

### Models not downloading
- Check internet connection
- Verify Google Drive folder is accessible
- Check disk space (need ~600MB free)

### Out of memory
- Reduce `patch_size` (HerdNet) or `img_size` (YOLO)
- Process fewer images at once
- Disable thumbnails/plots

### Slow processing
- Enable GPU acceleration
- Reduce overlap (HerdNet)
- Set `include_annotated_images=false` (YOLO)

## 📚 Citations

**HerdNet:**
```
Delplanque, A., Foucher, S., Lejeune, P., Linchant, J., & Théau, J. (2022).
Multispecies detection and identification of African mammals in aerial imagery 
using convolutional neural networks. Remote Sensing in Ecology and Conservation, 8(2), 166-179.
```

**YOLOv11:**
```
Ultralytics YOLOv11 (2024)
https://github.com/ultralytics/ultralytics
```

## 📄 License

This project uses:
- **HerdNet model**: MIT License
- **YOLOv11**: AGPL-3.0 License (Ultralytics)

## 🤝 Support

For issues related to:
- **API/Streamlit**: Open an issue in this repository
- **YOLOv11**: Visit https://github.com/ultralytics/ultralytics
- **HerdNet**: Visit https://github.com/Alexandre-Delplanque/HerdNet

## 🙏 Acknowledgments

- **YOLOv11** by Ultralytics
- **HerdNet** by Alexandre Delplanque (University of Liège)
- Research published in Remote Sensing in Ecology and Conservation
