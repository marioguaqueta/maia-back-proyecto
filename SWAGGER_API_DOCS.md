# 📚 Swagger API Documentation

The African Wildlife Detection API now includes comprehensive **Swagger/OpenAPI** documentation for easy API exploration and testing.

## 🌐 Accessing the Documentation

Once your Flask server is running, you can access the interactive Swagger UI at:

```
http://localhost:8000/docs
```

Or if deployed:

```
http://YOUR_EC2_IP:8000/docs
```

## ✨ Features

### Interactive API Explorer
- 📖 **Complete API Reference**: All endpoints documented with parameters and responses
- 🧪 **Try It Out**: Test endpoints directly from your browser
- 📝 **Request/Response Examples**: See what data to send and what you'll receive
- 🏷️ **Organized by Tags**: Endpoints grouped by functionality

### Swagger UI Capabilities

1. **Explore Endpoints**: Browse all available API endpoints
2. **View Schemas**: See request and response data structures
3. **Test Directly**: Execute API calls from the documentation
4. **Download Spec**: Get the OpenAPI specification in JSON format

## 📋 API Endpoints Overview

### 🏥 Health & Status
- `GET /` - API root with welcome message
- `GET /health` - Check API health and model status
- `GET /models/info` - Get information about available models

### 🎯 YOLOv11 Detection
- `POST /analyze-yolo` - Batch analysis (ZIP file with multiple images)
- `POST /analyze-single-image-yolo` - Single image analysis

**Parameters:**
- `file`: Image(s) to analyze
- `conf_threshold`: Confidence threshold (0.0-1.0, default: 0.25)
- `iou_threshold`: IOU threshold for NMS (0.0-1.0, default: 0.45)
- `img_size`: Image size for inference (default: 640)
- `include_annotated_images`: Include images with bounding boxes (default: true)

### 📍 HerdNet Detection
- `POST /analyze-image` - Batch analysis (ZIP file with multiple images)
- `POST /analyze-single-image-herdnet` - Single image analysis

**Parameters:**
- `file`: Image(s) to analyze
- `patch_size`: Patch size for stitching (default: 512)
- `overlap`: Overlap for stitching (default: 160)
- `rotation`: Number of 90° rotations (0-3, default: 0)
- `thumbnail_size`: Size for animal thumbnails (default: 256)
- `include_thumbnails`: Include animal thumbnails (default: true)
- `include_plots`: Include detection plots (default: false)

### 📊 Task Management
- `GET /tasks` - List all analysis tasks with filtering
- `GET /tasks/<task_id>` - Get specific task by ID

**Query Parameters for /tasks:**
- `model_type`: Filter by 'yolo' or 'herdnet'
- `status`: Filter by 'completed', 'processing', or 'failed'
- `limit`: Maximum tasks to return (default: 100)
- `offset`: Pagination offset (default: 0)

### 💾 Database Statistics
- `GET /database/stats` - Get comprehensive database statistics

## 🎓 How to Use Swagger UI

### 1. Open the Documentation

Navigate to http://localhost:8000/docs in your browser.

### 2. Explore an Endpoint

Click on any endpoint to expand its documentation and see:
- Description
- Parameters (query, path, form data, etc.)
- Request body schema
- Response schemas for different status codes
- Examples

### 3. Try an Endpoint

**Example: Test the /health endpoint**

1. Click on `GET /health` to expand
2. Click the **"Try it out"** button
3. Click **"Execute"**
4. View the response below

**Example: Test YOLOv11 Analysis**

1. Click on `POST /analyze-yolo` to expand
2. Click **"Try it out"**
3. Choose a ZIP file using the file selector
4. Adjust parameters (optional):
   - `conf_threshold`: 0.3
   - `iou_threshold`: 0.5
   - `img_size`: 640
5. Click **"Execute"**
6. View the response (this may take a few moments)

### 4. View Response

The Swagger UI will show:
- Response Code (200, 400, 500, etc.)
- Response Body (JSON with results)
- Response Headers
- Curl command (you can copy and use in terminal)

## 📖 OpenAPI Specification

### Download the Spec

The OpenAPI specification (JSON format) is available at:

```
http://localhost:8000/apispec.json
```

You can:
- Import it into Postman
- Use it with API clients
- Generate client SDKs
- Share with frontend developers

### Swagger Version

This API uses **Swagger 2.0** specification (also known as OpenAPI 2.0).

## 🛠️ For Developers

### Adding Documentation to New Endpoints

When adding new endpoints, include Swagger documentation in the docstring:

```python
@app.route("/your-endpoint", methods=["POST"])
def your_endpoint():
    """
    Your Endpoint Title
    Brief description of what this endpoint does
    ---
    tags:
      - YourCategory
    parameters:
      - name: param_name
        in: formData  # or query, path, header
        type: string  # or integer, number, boolean, file
        required: true
        description: Parameter description
    responses:
      200:
        description: Success response description
        schema:
          type: object
          properties:
            field_name:
              type: string
      400:
        description: Error response description
    """
    # Your code here
```

### Tags Available

- **Health**: Health check and status endpoints
- **YOLOv11**: YOLOv11 model endpoints
- **HerdNet**: HerdNet model endpoints
- **Tasks**: Task management endpoints
- **Database**: Database statistics endpoints

## 🧪 Testing with Curl

Swagger UI provides curl commands for each request. Example:

```bash
# Health check
curl -X GET "http://localhost:8000/health" -H "accept: application/json"

# Analyze with YOLO
curl -X POST "http://localhost:8000/analyze-yolo" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@images.zip" \
  -F "conf_threshold=0.25" \
  -F "iou_threshold=0.45"

# Get all tasks
curl -X GET "http://localhost:8000/tasks?model_type=yolo&limit=10" \
  -H "accept: application/json"

# Get specific task
curl -X GET "http://localhost:8000/tasks/YOUR_TASK_ID" \
  -H "accept: application/json"
```

## 📱 Integration Examples

### Python (requests)

```python
import requests

# Health check
response = requests.get('http://localhost:8000/health')
print(response.json())

# Analyze images with YOLO
files = {'file': open('images.zip', 'rb')}
data = {
    'conf_threshold': 0.25,
    'iou_threshold': 0.45,
    'img_size': 640
}
response = requests.post('http://localhost:8000/analyze-yolo', 
                        files=files, 
                        data=data)
result = response.json()
print(f"Task ID: {result['task_id']}")
print(f"Detections: {result['summary']['total_detections']}")
```

### JavaScript (fetch)

```javascript
// Health check
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Analyze images
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('conf_threshold', '0.25');

fetch('http://localhost:8000/analyze-yolo', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(result => {
    console.log('Task ID:', result.task_id);
    console.log('Detections:', result.summary.total_detections);
  });
```

### Postman

1. Import the OpenAPI spec from `http://localhost:8000/apispec.json`
2. All endpoints will be automatically added to your collection
3. Test each endpoint directly in Postman

## 🔧 Configuration

The Swagger configuration is defined in `app.py`:

```python
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "African Wildlife Detection API",
        "description": "...",
        "version": "2.1.0"
    },
    ...
}
```

### Customize

You can modify:
- Title and description
- Version number
- Contact information
- Base path
- Schemes (http/https)
- Tags and descriptions

## 📝 Best Practices

1. **Always check /health first** - Ensure API and models are loaded
2. **Use appropriate model** - YOLO for speed, HerdNet for large images
3. **Save task_id** - Store it to retrieve results later
4. **Handle errors gracefully** - Check response status codes
5. **Test with small files first** - Verify parameters before batch processing

## 🚀 Production Deployment

When deployed to production (EC2):

1. **Access Swagger UI**:
   ```
   http://YOUR_EC2_IP:8000/docs
   ```

2. **Update base URL** in requests:
   ```python
   API_BASE_URL = "http://YOUR_EC2_IP:8000"
   ```

3. **Consider HTTPS** for production:
   - Set up nginx reverse proxy
   - Add SSL certificate
   - Update swagger config schemes to ["https"]

## 🔒 Security Notes

- Swagger UI is enabled by default for development
- For production, consider:
  - Adding authentication
  - Limiting access to /docs endpoint
  - Using API keys
  - Rate limiting

## 📚 Additional Resources

- **Flasgger Documentation**: https://github.com/flasgger/flasgger
- **Swagger Specification**: https://swagger.io/specification/v2/
- **OpenAPI Guide**: https://swagger.io/docs/specification/about/

## 🆘 Troubleshooting

### Swagger UI not loading
- Check that `flasgger` is installed: `pip install flasgger`
- Verify Flask server is running
- Try accessing `/apispec.json` directly

### Endpoints not showing
- Check docstring format in endpoint function
- Ensure proper indentation in YAML
- Restart Flask server after changes

### File upload not working in Swagger UI
- This is a known Swagger UI limitation for large files
- Use curl or Postman for large file uploads
- Swagger UI works best for small test files

---

**Last Updated**: November 2024  
**Version**: 2.1.0  
**Swagger UI URL**: `/docs`  
**OpenAPI Spec URL**: `/apispec.json`

