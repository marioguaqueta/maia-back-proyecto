import io
import os
import zipfile
import tempfile
import shutil
from pathlib import Path
import numpy as np
import pandas as pd
import warnings
import base64
from datetime import datetime
import time

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flasgger import Swagger, swag_from

# Import database and model loader
from database import (init_database, generate_task_id, save_task, update_task_success,
                     update_task_error, save_detections, get_task_by_id, get_all_tasks, get_database_stats)
from model_loader import ensure_models

# PyTorch and image processing imports
import torch
import torch.nn as nn
from PIL import Image
import PIL
import albumentations as A
from torch.utils.data import DataLoader

# HerdNet imports
from animaloc.models import HerdNet, LossWrapper
from animaloc.eval import HerdNetStitcher, HerdNetEvaluator
from animaloc.eval.metrics import PointsMetrics
from animaloc.datasets import CSVDataset
from animaloc.data.transforms import DownSample, Rotate90
from animaloc.vizual import draw_points, draw_text
from animaloc.utils.useful_funcs import mkdir

# Suppress warnings and increase PIL image size limit
warnings.filterwarnings('ignore')
PIL.Image.MAX_IMAGE_PIXELS = None

app = Flask(__name__)

# Swagger configuration
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "African Wildlife Detection API",
        "description": "REST API for detecting and analyzing African wildlife in aerial/satellite imagery using YOLOv11 and HerdNet deep learning models",
        "version": "2.1.0",
        "contact": {
            "name": "MAIA Project",
            "url": "https://github.com/your-repo"
        }
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "tags": [
        {
            "name": "Health",
            "description": "API health and status endpoints"
        },
        {
            "name": "YOLOv11",
            "description": "YOLOv11 model endpoints for bounding box detection"
        },
        {
            "name": "HerdNet",
            "description": "HerdNet model endpoints for point-based detection"
        },
        {
            "name": "Tasks",
            "description": "Task management and retrieval endpoints"
        },
        {
            "name": "Database",
            "description": "Database statistics and information"
        }
    ]
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'webp', 'bmp'}
ALLOWED_ZIP_EXTENSIONS = {'zip'}

# ========================================
# Initialize Database and Download Models
# ========================================
print("\n" + "="*60)
print("🚀 Starting Wildlife Detection API")
print("="*60)

# Initialize database
init_database()

# Ensure models are available (download from Google Drive if needed)
model_status = ensure_models()

# ========================================
# Load PyTorch Model for Animal Detection
# ========================================
print("\n" + "="*60)
print("Loading HerdNet PyTorch model...")
print("="*60)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load checkpoint
MODEL_PATH = "./herdnet_baseline_model.pth"
print(f"Loading checkpoint from {MODEL_PATH}...")

map_location = torch.device('cpu')
if torch.cuda.is_available():
    map_location = torch.device('cuda')

checkpoint = torch.load(MODEL_PATH, map_location=map_location)

# Extract model configuration from checkpoint
classes_dict = checkpoint.get('classes', {
    1: 'buffalo', 2: 'elephant', 3: 'kob', 
    4: 'topi', 5: 'warthog', 6: 'waterbuck'
})
num_classes = len(classes_dict) + 1  # +1 for background
img_mean = checkpoint.get('mean', [0.485, 0.456, 0.406])
img_std = checkpoint.get('std', [0.229, 0.224, 0.225])

print(f"Model classes: {classes_dict}")
print(f"Number of classes: {num_classes}")
print(f"Normalization - Mean: {img_mean}, Std: {img_std}")

# Build ANIMAL_CLASSES dictionary
ANIMAL_CLASSES = {0: "no_animal"}
ANIMAL_CLASSES.update(classes_dict)

# Spanish translations for animal classes
SPANISH_NAMES = {
    'buffalo': 'Búfalo',
    'elephant': 'Elefante',
    'kob': 'Kob',
    'topi': 'Topi',
    'warthog': 'Jabalí Verrugoso',
    'waterbuck': 'Antílope Acuático',
    'no_animal': 'Sin Animal'
}

def translate_to_spanish(english_name):
    """Translate animal class name to Spanish."""
    return SPANISH_NAMES.get(english_name.lower(), english_name)

def translate_results_to_spanish(results):
    """
    Translate all species names in results dictionary from English to Spanish.
    This is done at the end to avoid interfering with model processing.
    """
    if not results:
        return results
    
    # Translate detections
    if 'detections' in results:
        for det in results['detections']:
            if 'class_name' in det:
                det['class_name'] = translate_to_spanish(det['class_name'])
            if 'species' in det:
                det['species'] = translate_to_spanish(det['species'])
    
    # Translate species_counts
    if 'species_counts' in results:
        translated_counts = {}
        for species, count in results['species_counts'].items():
            translated_counts[translate_to_spanish(species)] = count
        results['species_counts'] = translated_counts
    
    # Translate summary species_counts
    if 'summary' in results and 'species_counts' in results['summary']:
        translated_counts = {}
        for species, count in results['summary']['species_counts'].items():
            translated_counts[translate_to_spanish(species)] = count
        results['summary']['species_counts'] = translated_counts
    
    return results

# Build the model
print("Building HerdNet model...")
model = HerdNet(num_classes=num_classes, pretrained=False)
model = LossWrapper(model, [])
model.load_state_dict(checkpoint['model_state_dict'])
model = model.to(device)
model.eval()

print(f"✓ Model loaded successfully with {num_classes} classes")
print(f"  Classes: {list(ANIMAL_CLASSES.values())}")


# ========================================
# Load YOLOv11 Model for Animal Detection
# ========================================
print("\nLoading YOLOv11 model...")
try:
    from ultralytics import YOLO
    
    YOLO_MODEL_PATH = "./best.pt"
    yolo_model = YOLO(YOLO_MODEL_PATH)
    yolo_model.to(device)
    
    # Get class names from the model
    YOLO_CLASSES = yolo_model.names  # Dictionary of class ID to class name
    
    print(f"✓ YOLOv11 model loaded successfully")
    print(f"  Model classes: {YOLO_CLASSES}")
    print(f"  Number of classes: {len(YOLO_CLASSES)}")
    yolo_loaded = True
except Exception as e:
    print(f"⚠ Warning: Could not load YOLOv11 model: {str(e)}")
    yolo_model = None
    YOLO_CLASSES = {}
    yolo_loaded = False

def analyze_images_with_yolo(image_dir, conf_threshold=0.25, iou_threshold=0.45, img_size=640, include_annotated_images=True):
    """
    Analyze images using YOLOv11 model
    
    Args:
        image_dir: Directory containing images
        conf_threshold: Confidence threshold for detections (default 0.25)
        iou_threshold: IOU threshold for NMS (default 0.45)
        img_size: Image size for inference (default 640)
        include_annotated_images: Whether to generate annotated images with bboxes (default True)
    
    Returns:
        Dictionary with detection results, statistics, and annotated images
    """
    if not yolo_loaded:
        raise Exception("YOLOv11 model is not loaded. Check that best.pt exists.")
    
    # Get all image files
    img_names = [i for i in os.listdir(image_dir) 
                 if i.endswith(('.JPG', '.jpg', '.JPEG', '.jpeg', '.png', '.PNG', '.bmp', '.webp'))]
    
    if not img_names:
        raise Exception("No images found in the uploaded zip file")
    
    print(f"Processing {len(img_names)} images with YOLOv11...")
    
    all_detections = []
    images_with_animals = []
    images_without_animals = []
    species_counts = {}
    annotated_images = []
    
    for img_name in img_names:
        img_path = os.path.join(image_dir, img_name)
        
        try:
            # Run inference
            results = yolo_model.predict(
                source=img_path,
                conf=conf_threshold,
                iou=iou_threshold,
                imgsz=img_size,
                verbose=False
            )
            
            # Process results
            result = results[0]
            boxes = result.boxes
            
            image_detections = []
            image_has_animals = False
            
            # Load original image for annotation
            original_img = Image.open(img_path)
            annotated_img = original_img.copy()
            
            if len(boxes) > 0:
                image_has_animals = True
                images_with_animals.append(img_name)
                
                # Create drawing context for annotations
                from PIL import ImageDraw, ImageFont
                draw = ImageDraw.Draw(annotated_img)
                
                # Try to load a font, fall back to default if not available
                try:
                    # Calculate font size based on image size
                    font_size = max(12, int(min(original_img.width, original_img.height) * 0.02))
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
                except:
                    font = ImageFont.load_default()
                
                for box in boxes:
                    # Get detection details
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                    
                    # Get class name (keep in English during processing)
                    class_name = YOLO_CLASSES.get(class_id, f"class_{class_id}")
                    
                    # Update species counts
                    species_counts[class_name] = species_counts.get(class_name, 0) + 1
                    
                    detection = {
                        'image': img_name,
                        'class_id': class_id,
                        'class_name': class_name,
                        'confidence': confidence,
                        'bbox': {
                            'x1': bbox[0],
                            'y1': bbox[1],
                            'x2': bbox[2],
                            'y2': bbox[3]
                        },
                        'center': {
                            'x': (bbox[0] + bbox[2]) / 2,
                            'y': (bbox[1] + bbox[3]) / 2
                        }
                    }
                    
                    image_detections.append(detection)
                    all_detections.append(detection)
                    
                    # Draw bounding box on the image
                    if include_annotated_images:
                        # Define color based on class (you can customize this)
                        colors = [
                            '#FF0000', '#00FF00', '#0000FF', '#FFFF00', 
                            '#FF00FF', '#00FFFF', '#FFA500', '#800080',
                            '#FFC0CB', '#A52A2A'
                        ]
                        color = colors[class_id % len(colors)]
                        
                        # Draw rectangle
                        line_width = max(2, int(min(original_img.width, original_img.height) * 0.003))
                        draw.rectangle(
                            [(bbox[0], bbox[1]), (bbox[2], bbox[3])],
                            outline=color,
                            width=line_width
                        )
                        
                        # Draw label with background
                        label = f"{class_name} {confidence:.2f}"
                        
                        # Get text bounding box
                        try:
                            bbox_text = draw.textbbox((bbox[0], bbox[1]), label, font=font)
                            text_width = bbox_text[2] - bbox_text[0]
                            text_height = bbox_text[3] - bbox_text[1]
                        except:
                            # Fallback for older PIL versions
                            text_width, text_height = draw.textsize(label, font=font)
                        
                        # Draw background rectangle for text
                        text_bg_bbox = [
                            bbox[0],
                            max(0, bbox[1] - text_height - 4),
                            bbox[0] + text_width + 4,
                            bbox[1]
                        ]
                        draw.rectangle(text_bg_bbox, fill=color)
                        
                        # Draw text
                        draw.text(
                            (bbox[0] + 2, max(0, bbox[1] - text_height - 2)),
                            label,
                            fill='white',
                            font=font
                        )
            
            if not image_has_animals:
                images_without_animals.append(img_name)
            
            # Convert annotated image to base64 if there were detections
            if include_annotated_images and image_has_animals:
                # Resize images if too large (to avoid huge base64 strings)
                max_size = 1920
                original_img_resized = original_img
                annotated_img_resized = annotated_img
                
                if max(annotated_img.width, annotated_img.height) > max_size:
                    ratio = max_size / max(annotated_img.width, annotated_img.height)
                    new_size = (int(annotated_img.width * ratio), int(annotated_img.height * ratio))
                    original_img_resized = original_img.resize(new_size, Image.Resampling.LANCZOS)
                    annotated_img_resized = annotated_img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Convert original image to base64
                buffered_original = io.BytesIO()
                original_img_resized.save(buffered_original, format="JPEG", quality=85)
                original_base64 = base64.b64encode(buffered_original.getvalue()).decode('utf-8')
                
                # Convert annotated image to base64
                buffered_annotated = io.BytesIO()
                annotated_img_resized.save(buffered_annotated, format="JPEG", quality=85)
                annotated_base64 = base64.b64encode(buffered_annotated.getvalue()).decode('utf-8')
                
                annotated_images.append({
                    'image_name': img_name,
                    'detections_count': len(image_detections),
                    'original_image_base64': original_base64,
                    'annotated_image_base64': annotated_base64,
                    'original_size': {
                        'width': original_img.width,
                        'height': original_img.height
                    },
                    'annotated_size': {
                        'width': annotated_img_resized.width,
                        'height': annotated_img_resized.height
                    }
                })
            
            print(f"  ✓ {img_name}: {len(image_detections)} detections")
            
        except Exception as e:
            print(f"  ✗ Error processing {img_name}: {str(e)}")
            images_without_animals.append(img_name)
    
    # Prepare summary
    summary = {
        'total_images': len(img_names),
        'images_with_animals': len(images_with_animals),
        'images_without_animals': len(images_without_animals),
        'total_detections': len(all_detections),
        'species_counts': species_counts,
        'images_with_detections_list': images_with_animals,
        'images_without_detections_list': images_without_animals
    }
    
    results = {
        'summary': summary,
        'detections': all_detections,
        'annotated_images': annotated_images,
        'processing_params': {
            'conf_threshold': conf_threshold,
            'iou_threshold': iou_threshold,
            'img_size': img_size
        }
    }
    
    # Translate results to Spanish before returning
    return translate_results_to_spanish(results)

def allowed_image(filename):
    """Check if the file is an allowed image type"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}


def allowed_zip(filename):
    """Check if the file is a zip file"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_ZIP_EXTENSIONS


def analyze_images_with_evaluator(image_dir, patch_size=512, overlap=160, rotation=0, thumbnail_size=256):
    """
    Analyze images using HerdNetEvaluator (same as infer.py)
    
    Args:
        image_dir: Directory containing images
        patch_size: Patch size for stitching (default 512)
        overlap: Overlap for stitching (default 160)
        rotation: Number of 90-degree rotations (default 0)
        thumbnail_size: Size for thumbnails (default 256)
    
    Returns:
        Dictionary with detection results, thumbnails, and plots
    """
    # Create results directory
    results_dir = os.path.join(image_dir, 'results')
    mkdir(results_dir)
    plots_dir = os.path.join(results_dir, 'plots')
    mkdir(plots_dir)
    thumbs_dir = os.path.join(results_dir, 'thumbnails')
    mkdir(thumbs_dir)
    
    # Prepare dataset
    img_names = [i for i in os.listdir(image_dir) 
                 if i.endswith(('.JPG', '.jpg', '.JPEG', '.jpeg', '.png', '.PNG'))]
    
    if not img_names:
        raise Exception("No images found in the uploaded zip file")
    
    n = len(img_names)
    df = pd.DataFrame(data={
        'images': img_names, 
        'x': [0]*n, 
        'y': [0]*n, 
        'labels': [1]*n
    })
    
    # Setup transforms
    end_transforms = []
    if rotation != 0:
        end_transforms.append(Rotate90(k=rotation))
    end_transforms.append(DownSample(down_ratio=2, anno_type='point'))
    
    albu_transforms = [A.Normalize(mean=img_mean, std=img_std)]
    
    dataset = CSVDataset(
        csv_file=df,
        root_dir=image_dir,
        albu_transforms=albu_transforms,
        end_transforms=end_transforms
    )
    
    dataloader = DataLoader(
        dataset, 
        batch_size=1, 
        shuffle=False,
        sampler=torch.utils.data.SequentialSampler(dataset)
    )
    
    # Build the stitcher
    stitcher = HerdNetStitcher(
        model=model,
        size=(patch_size, patch_size),
        overlap=overlap,
        down_ratio=2,
        up=True,
        reduction='mean',
        device_name=device
    )
    
    # Build the evaluator
    metrics = PointsMetrics(5, num_classes=num_classes)
    evaluator = HerdNetEvaluator(
        model=model,
        dataloader=dataloader,
        metrics=metrics,
        lmds_kwargs=dict(kernel_size=(3, 3), adapt_ts=0.2, neg_ts=0.1),
        device_name=device,
        print_freq=1,
        stitcher=stitcher,
        work_dir=results_dir,
        header='[INFERENCE]'
    )
    
    # Run inference
    print(f"Starting inference on {n} images...")
    evaluator.evaluate(wandb_flag=False, viz=False, log_meters=False)
    
    # Get detections
    detections = evaluator.detections
    detections.dropna(inplace=True)
    # Map species names (keep in English during processing)
    detections['species'] = detections['labels'].map(classes_dict)
    
    # Save detections CSV
    csv_path = os.path.join(results_dir, 'detections.csv')
    detections.to_csv(csv_path, index=False)
    
    # Generate plots and thumbnails
    print('Generating plots and thumbnails...')
    img_names_with_detections = np.unique(detections['images'].values).tolist()
    
    thumbnails_data = []
    plots_data = []
    
    for img_name in img_names_with_detections:
        img_path = os.path.join(image_dir, img_name)
        img = Image.open(img_path)
        
        # Apply rotation if specified
        if rotation != 0:
            rot_degrees = rotation * 90
            img = img.rotate(rot_degrees, expand=True)
        
        img_copy = img.copy()
        
        # Get detection points for this image
        img_detections = detections[detections['images'] == img_name]
        pts = list(img_detections[['y', 'x']].to_records(index=False))
        pts = [(y, x) for y, x in pts]
        
        # Draw points on image
        output_plot = draw_points(img, pts, color='red', size=10)
        plot_path = os.path.join(plots_dir, img_name)
        output_plot.save(plot_path, quality=95)
        
        # Convert original image to base64
        buffered_original = io.BytesIO()
        img_copy.save(buffered_original, format="JPEG", quality=85)
        original_base64 = base64.b64encode(buffered_original.getvalue()).decode('utf-8')
        
        # Convert plot to base64
        buffered_plot = io.BytesIO()
        output_plot.save(buffered_plot, format="JPEG", quality=95)
        plot_base64 = base64.b64encode(buffered_plot.getvalue()).decode('utf-8')
        
        plots_data.append({
            'image_name': img_name,
            'original_image_base64': original_base64,
            'plot_base64': plot_base64,
            'detections_count': len(pts)
        })
        
        # Create thumbnails for each detection
        sp_score = list(img_detections[['species', 'scores']].to_records(index=False))
        for i, ((y, x), (sp, score)) in enumerate(zip(pts, sp_score)):
            off = thumbnail_size // 2
            coords = (x - off, y - off, x + off, y + off)
            
            # Ensure coordinates are within image bounds
            coords = (
                max(0, coords[0]),
                max(0, coords[1]),
                min(img_copy.width, coords[2]),
                min(img_copy.height, coords[3])
            )
            
            thumbnail = img_copy.crop(coords)
            score_pct = round(score * 100, 0)
            thumbnail = draw_text(
                thumbnail, 
                f"{sp} | {score_pct}%", 
                position=(10, 5), 
                font_size=int(0.08 * thumbnail_size)
            )
            
            thumb_name = img_name[:-4] + f'_{i}.JPG'
            thumb_path = os.path.join(thumbs_dir, thumb_name)
            thumbnail.save(thumb_path)
            
            # Convert thumbnail to base64
            buffered = io.BytesIO()
            thumbnail.save(buffered, format="JPEG")
            thumb_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            thumbnails_data.append({
                'image_name': img_name,
                'detection_id': i,
                'species': sp,
                'confidence': float(score),
                'position': {'x': int(x), 'y': int(y)},
                'thumbnail_base64': thumb_base64
            })
    
    # Prepare summary statistics
    total_detections = len(detections)
    images_with_detections = len(img_names_with_detections)
    images_without_detections = n - images_with_detections
    
    # Detection counts by species
    species_counts = detections['species'].value_counts().to_dict()
    
    # Convert detections DataFrame to list of dicts
    detections_list = detections.to_dict('records')
    
    return {
        'total_images': n,
        'images_with_detections': images_with_detections,
        'images_without_detections': images_without_detections,
        'total_detections': total_detections,
        'species_counts': species_counts,
        'detections': detections_list,
        'thumbnails': thumbnails_data,
        'plots': plots_data,
        'processing_params': {
            'patch_size': patch_size,
            'overlap': overlap,
            'rotation': rotation,
            'thumbnail_size': thumbnail_size
        }
    }


@app.route("/", methods=["GET"])
def index():
    """
    API Root / Welcome
    Welcome page with API information and documentation link
    ---
    tags:
      - Health
    responses:
      200:
        description: API information
        schema:
          type: object
          properties:
            message:
              type: string
            version:
              type: string
            documentation:
              type: string
            endpoints:
              type: object
    """
    return jsonify({
        'message': 'African Wildlife Detection API',
        'version': '2.1.0',
        'documentation': '/docs',
        'endpoints': {
            'health': '/health',
            'models_info': '/models/info',
            'yolo_batch': '/analyze-yolo',
            'yolo_single': '/analyze-single-image-yolo',
            'herdnet_batch': '/analyze-image',
            'herdnet_single': '/analyze-single-image-herdnet',
            'tasks_list': '/tasks',
            'task_by_id': '/tasks/<task_id>',
            'database_stats': '/database/stats'
        }
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """
    Health Check Endpoint
    Check if the API is running and models are loaded
    ---
    tags:
      - Health
    responses:
      200:
        description: API is healthy and models are loaded
        schema:
          type: object
          properties:
            status:
              type: string
              example: healthy
            models:
              type: object
              properties:
                herdnet:
                  type: object
                  properties:
                    loaded:
                      type: boolean
                    device:
                      type: string
                    num_classes:
                      type: integer
                    classes:
                      type: object
                yolov11:
                  type: object
                  properties:
                    loaded:
                      type: boolean
                    device:
                      type: string
                    num_classes:
                      type: integer
                    classes:
                      type: object
    """
    return jsonify({
        'status': 'healthy',
        'models': {
            'herdnet': {
                'loaded': True,
                'device': str(device),
                'num_classes': num_classes,
                'classes': ANIMAL_CLASSES
            },
            'yolov11': {
                'loaded': yolo_loaded,
                'device': str(device),
                'num_classes': len(YOLO_CLASSES) if yolo_loaded else 0,
                'classes': YOLO_CLASSES if yolo_loaded else {}
            }
        }
    }), 200

@app.route("/analyze-yolo", methods=["POST"])
def analyze_yolo_endpoint():
    """
    Analyze Images with YOLOv11 (Batch Processing)
    Upload a ZIP file containing multiple images for YOLOv11 bounding box detection
    ---
    tags:
      - YOLOv11
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: ZIP file containing wildlife images
      - name: conf_threshold
        in: formData
        type: number
        required: false
        default: 0.25
        description: Confidence threshold for detections (0.0-1.0)
      - name: iou_threshold
        in: formData
        type: number
        required: false
        default: 0.45
        description: IOU threshold for NMS (0.0-1.0)
      - name: img_size
        in: formData
        type: integer
        required: false
        default: 640
        description: Image size for inference (416, 640, 1280, etc.)
      - name: include_annotated_images
        in: formData
        type: string
        required: false
        default: "true"
        description: Include annotated images with bounding boxes
    responses:
      200:
        description: Analysis completed successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
            task_id:
              type: string
            model:
              type: string
            summary:
              type: object
              properties:
                total_images:
                  type: integer
                images_with_animals:
                  type: integer
                total_detections:
                  type: integer
                species_counts:
                  type: object
            detections:
              type: array
              items:
                type: object
            annotated_images:
              type: array
              items:
                type: object
            processing_time_seconds:
              type: number
      400:
        description: Bad request (no file provided or invalid file type)
      500:
        description: Analysis failed
    """
    task_id = None
    start_time = time.time()
    
    try:
        if not yolo_loaded:
            return jsonify({
                'success': False,
                'error': 'YOLOv11 model not loaded',
                'message': 'The YOLOv11 model (best.pt) could not be loaded. Please check the model file.'
            }), 500
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file is a zip
        if not allowed_zip(file.filename):
            return jsonify({'error': 'File must be a ZIP archive'}), 400
        
        # Get optional parameters
        conf_threshold = float(request.form.get('conf_threshold', 0.25))
        iou_threshold = float(request.form.get('iou_threshold', 0.45))
        img_size = int(request.form.get('img_size', 640))
        include_annotated_images = request.form.get('include_annotated_images', 'true').lower() == 'true'
        
        # Generate task ID
        task_id = generate_task_id()
        
        print(f"\n{'='*60}")
        print(f"Task ID: {task_id}")
        print(f"Processing ZIP file with YOLOv11: {file.filename}")
        print(f"Parameters: conf={conf_threshold}, iou={iou_threshold}, img_size={img_size}")
        print(f"Include annotated images: {include_annotated_images}")
        print(f"{'='*60}\n")
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save and extract ZIP file
            zip_path = os.path.join(temp_dir, 'upload.zip')
            file.save(zip_path)
            
            # Extract images
            images_dir = os.path.join(temp_dir, 'images')
            os.makedirs(images_dir, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Extract only image files
                for member in zip_ref.namelist():
                    if allowed_image(member) and not member.startswith('__MACOSX'):
                        # Extract to flat directory (ignore subdirectories)
                        filename = os.path.basename(member)
                        if filename:  # Skip directories
                            source = zip_ref.open(member)
                            target_path = os.path.join(images_dir, filename)
                            with open(target_path, 'wb') as target:
                                shutil.copyfileobj(source, target)
            
            # Run analysis
            results = analyze_images_with_yolo(
                images_dir,
                conf_threshold=conf_threshold,
                iou_threshold=iou_threshold,
                img_size=img_size,
                include_annotated_images=include_annotated_images
            )
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Count images
            num_images = len([f for f in os.listdir(images_dir) if allowed_image(f)])
            
            # Save task to database
            save_task(task_id, 'yolo', file.filename, num_images, {
                'conf_threshold': conf_threshold,
                'iou_threshold': iou_threshold,
                'img_size': img_size
            })
            
            response = {
                'success': True,
                'task_id': task_id,
                'message': 'Images analyzed successfully with YOLOv11',
                'model': 'YOLOv11',
                'classes': YOLO_CLASSES,
                'summary': results['summary'],
                'detections': results['detections'],
                'processing_params': results['processing_params'],
                'processing_time_seconds': round(processing_time, 2)
            }
            
            # Add annotated images if requested
            if include_annotated_images:
                response['annotated_images'] = results['annotated_images']
                response['annotated_images_count'] = len(results['annotated_images'])
            
            # Update task success and save detections
            update_task_success(
                task_id, processing_time,
                results['summary']['total_detections'],
                results['summary']['images_with_animals'],
                results['summary']['species_counts'],
                response
            )
            
            if results['detections']:
                save_detections(task_id, results['detections'], 'yolo')
            
            print(f"\n{'='*60}")
            print(f"✓ YOLOv11 Analysis complete!")
            print(f"  Task ID: {task_id}")
            print(f"  Processing time: {processing_time:.2f}s")
            print(f"  Total detections: {results['summary']['total_detections']}")
            print(f"  Images with animals: {results['summary']['images_with_animals']}/{results['summary']['total_images']}")
            print(f"  Annotated images generated: {len(results.get('annotated_images', []))}")
            print(f"  Species found: {list(results['summary']['species_counts'].keys())}")
            print(f"{'='*60}\n")
            
            # Translate response to Spanish before returning
            response = translate_results_to_spanish(response)
            
            return jsonify(response), 200
            
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Update task with error if created
        if task_id:
            update_task_error(task_id, str(e))
        
        return jsonify({
            'success': False,
            'task_id': task_id,
            'error': 'Analysis failed',
            'message': str(e)
        }), 500

@app.route("/models/info", methods=["GET"])
def models_info():
    """
    Get Models Information
    Retrieve information about all available detection models
    ---
    tags:
      - Health
    responses:
      200:
        description: Models information retrieved successfully
        schema:
          type: object
          properties:
            models:
              type: object
              properties:
                herdnet:
                  type: object
                  properties:
                    loaded:
                      type: boolean
                    endpoint:
                      type: string
                    classes:
                      type: object
                    num_classes:
                      type: integer
                yolov11:
                  type: object
                  properties:
                    loaded:
                      type: boolean
                    endpoint:
                      type: string
                    classes:
                      type: object
                    num_classes:
                      type: integer
    """
    return jsonify({
        'models': {
            'herdnet': {
                'loaded': True,
                'endpoint': '/analyze-image',
                'classes': ANIMAL_CLASSES,
                'num_classes': num_classes
            },
            'yolov11': {
                'loaded': yolo_loaded,
                'endpoint': '/analyze-yolo',
                'classes': YOLO_CLASSES if yolo_loaded else {},
                'num_classes': len(YOLO_CLASSES) if yolo_loaded else 0
            }
        }
    }), 200

@app.route("/analyze-image", methods=["POST"])
def analyze_image_endpoint():
    """
    Analyze Images with HerdNet (Batch Processing)
    Upload a ZIP file containing multiple images for HerdNet point-based detection
    ---
    tags:
      - HerdNet
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: ZIP file containing wildlife images
      - name: patch_size
        in: formData
        type: integer
        required: false
        default: 512
        description: Patch size for image stitching (384, 512, 768, 1024, 2048)
      - name: overlap
        in: formData
        type: integer
        required: false
        default: 160
        description: Overlap for stitching in pixels (0-300)
      - name: rotation
        in: formData
        type: integer
        required: false
        default: 0
        description: Number of 90-degree rotations (0, 1, 2, 3)
      - name: thumbnail_size
        in: formData
        type: integer
        required: false
        default: 256
        description: Size for animal thumbnails in pixels
      - name: include_thumbnails
        in: formData
        type: string
        required: false
        default: "true"
        description: Include thumbnail images of detected animals
      - name: include_plots
        in: formData
        type: string
        required: false
        default: "false"
        description: Include detection plots with marked points
    responses:
      200:
        description: Analysis completed successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
            task_id:
              type: string
            model:
              type: string
            summary:
              type: object
              properties:
                total_images:
                  type: integer
                images_with_detections:
                  type: integer
                total_detections:
                  type: integer
                species_counts:
                  type: object
            detections:
              type: array
              items:
                type: object
            thumbnails:
              type: array
              items:
                type: object
            plots:
              type: array
              items:
                type: object
            processing_time_seconds:
              type: number
      400:
        description: Bad request
      500:
        description: Analysis failed
    """
    task_id = None
    start_time = time.time()
    
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file is a zip
        if not allowed_zip(file.filename):
            return jsonify({'error': 'File must be a ZIP archive'}), 400
        
        # Get optional parameters
        patch_size = int(request.form.get('patch_size', 512))
        overlap = int(request.form.get('overlap', 160))
        rotation = int(request.form.get('rotation', 0))
        thumbnail_size = int(request.form.get('thumbnail_size', 256))
        include_thumbnails = request.form.get('include_thumbnails', 'true').lower() == 'true'
        include_plots = request.form.get('include_plots', 'false').lower() == 'true'
        
        # Generate task ID
        task_id = generate_task_id()
        
        print(f"\n{'='*60}")
        print(f"Task ID: {task_id}")
        print(f"Processing ZIP file: {file.filename}")
        print(f"Parameters: patch_size={patch_size}, overlap={overlap}, rotation={rotation}, thumbnail_size={thumbnail_size}")
        print(f"{'='*60}\n")
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save and extract ZIP file
            zip_path = os.path.join(temp_dir, 'upload.zip')
            file.save(zip_path)
            
            # Extract images
            images_dir = os.path.join(temp_dir, 'images')
            os.makedirs(images_dir, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Extract only image files
                for member in zip_ref.namelist():
                    if allowed_image(member) and not member.startswith('__MACOSX'):
                        # Extract to flat directory (ignore subdirectories)
                        filename = os.path.basename(member)
                        if filename:  # Skip directories
                            source = zip_ref.open(member)
                            target_path = os.path.join(images_dir, filename)
                            with open(target_path, 'wb') as target:
                                shutil.copyfileobj(source, target)
            
            # Run analysis
            results = analyze_images_with_evaluator(
                images_dir,
                patch_size=patch_size,
                overlap=overlap,
                rotation=rotation,
                thumbnail_size=thumbnail_size
            )
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Count images
            num_images = len([f for f in os.listdir(images_dir) if allowed_image(f)])
            
            # Save task to database
            save_task(task_id, 'herdnet', file.filename, num_images, {
                'patch_size': patch_size,
                'overlap': overlap,
                'rotation': rotation,
                'thumbnail_size': thumbnail_size
            })
            
            # Filter response based on parameters
            response = {
                'success': True,
                'task_id': task_id,
                'message': 'Images analyzed successfully with HerdNet',
                'model': 'HerdNet',
                'summary': {
                    'total_images': results['total_images'],
                    'images_with_detections': results['images_with_detections'],
                    'images_without_detections': results['images_without_detections'],
                    'total_detections': results['total_detections'],
                    'species_counts': results['species_counts']
                },
                'detections': results['detections'],
                'processing_params': results['processing_params'],
                'processing_time_seconds': round(processing_time, 2)
            }
            
            if include_thumbnails:
                response['thumbnails'] = results['thumbnails']
            
            if include_plots:
                response['plots'] = results['plots']
            
            # Update task success and save detections
            update_task_success(
                task_id, processing_time,
                results['total_detections'],
                results['images_with_detections'],
                results['species_counts'],
                response
            )
            
            if results['detections']:
                save_detections(task_id, results['detections'], 'herdnet')
            
            print(f"\n{'='*60}")
            print(f"✓ HerdNet Analysis complete!")
            print(f"  Task ID: {task_id}")
            print(f"  Processing time: {processing_time:.2f}s")
            print(f"  Total detections: {results['total_detections']}")
            print(f"  Images with animals: {results['images_with_detections']}/{results['total_images']}")
            print(f"  Species found: {list(results['species_counts'].keys())}")
            print(f"{'='*60}\n")
            
            # Translate response to Spanish before returning
            response = translate_results_to_spanish(response)
            
            return jsonify(response), 200
            
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Update task with error if created
        if task_id:
            update_task_error(task_id, str(e))
        
        return jsonify({
            'success': False,
            'task_id': task_id,
            'error': 'Analysis failed',
            'message': str(e)
        }), 500


@app.route("/analyze-single-image-yolo", methods=["POST"])
def analyze_single_image_yolo_endpoint():
    """
    Analyze Single Image with YOLOv11
    Upload a single image for YOLOv11 bounding box detection
    ---
    tags:
      - YOLOv11
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Single wildlife image (PNG, JPG, JPEG, GIF, WebP, BMP, TIFF)
      - name: conf_threshold
        in: formData
        type: number
        required: false
        default: 0.25
      - name: iou_threshold
        in: formData
        type: number
        required: false
        default: 0.45
      - name: img_size
        in: formData
        type: integer
        required: false
        default: 640
      - name: include_annotated_images
        in: formData
        type: string
        required: false
        default: "true"
    responses:
      200:
        description: Analysis completed successfully
      400:
        description: Bad request
      500:
        description: Analysis failed
    """
    task_id = None
    start_time = time.time()
    
    try:
        # Check if YOLO model is loaded
        if yolo_model is None:
            return jsonify({'error': 'YOLOv11 model not available'}), 503
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file is an image
        if not allowed_image(file.filename):
            return jsonify({'error': 'File must be an image (png, jpg, jpeg, gif, webp, bmp)'}), 400
        
        # Get optional parameters
        conf_threshold = float(request.form.get('conf_threshold', 0.25))
        iou_threshold = float(request.form.get('iou_threshold', 0.45))
        img_size = int(request.form.get('img_size', 640))
        include_annotated = request.form.get('include_annotated_images', 'true').lower() == 'true'
        
        # Generate task ID
        task_id = generate_task_id()
        
        print(f"\n{'='*60}")
        print(f"YOLO SINGLE IMAGE ANALYSIS")
        print(f"Task ID: {task_id}")
        print(f"Filename: {file.filename}")
        print(f"Confidence: {conf_threshold}, IOU: {iou_threshold}, Size: {img_size}")
        print(f"{'='*60}\n")
        
        # Save task to database (status: processing)
        save_task(
            task_id=task_id,
            model_type='yolo',
            filename=file.filename,
            num_images=1,
            processing_params={
                'conf_threshold': conf_threshold,
                'iou_threshold': iou_threshold,
                'img_size': img_size,
                'include_annotated_images': include_annotated
            }
        )
        
        # Create temp directory for processing
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Save uploaded image
            image_filename = secure_filename(file.filename)
            image_path = os.path.join(temp_dir, image_filename)
            file.save(image_path)
            
            # Process the image
            print(f"Processing image: {image_filename}")
            
            # Run YOLO inference
            results = yolo_model.predict(
                source=image_path,
                conf=conf_threshold,
                iou=iou_threshold,
                imgsz=img_size,
                save=False,
                verbose=False
            )
            
            # Process results
            result = results[0]
            boxes = result.boxes
            
            # Extract detections
            detections = []
            species_counts = {}
            
            for box in boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                xyxy = box.xyxy[0].tolist()
                
                # Get class name (keep in English during processing)
                class_name = result.names[cls_id]
                
                # Count species
                species_counts[class_name] = species_counts.get(class_name, 0) + 1
                
                # Calculate center and dimensions
                x1, y1, x2, y2 = xyxy
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                width = x2 - x1
                height = y2 - y1
                
                detection = {
                    'image': image_filename,
                    'class_id': cls_id,
                    'class_name': class_name,
                    'confidence': conf,
                    'bbox': {
                        'x1': x1,
                        'y1': y1,
                        'x2': x2,
                        'y2': y2
                    },
                    'center': {
                        'x': center_x,
                        'y': center_y
                    },
                    'dimensions': {
                        'width': width,
                        'height': height
                    }
                }
                
                detections.append(detection)
            
            # Prepare response
            response_data = {
                'success': True,
                'task_id': task_id,
                'model': 'YOLOv11',
                'summary': {
                    'total_images': 1,
                    'total_detections': len(detections),
                    'images_with_detections': 1 if len(detections) > 0 else 0,
                    'images_without_detections': 0 if len(detections) > 0 else 1,
                    'species_counts': species_counts
                },
                'detections': detections,
                'processing_params': {
                    'conf_threshold': conf_threshold,
                    'iou_threshold': iou_threshold,
                    'img_size': img_size,
                    'include_annotated_images': include_annotated
                }
            }
            
            # Generate annotated image if requested
            if include_annotated:
                annotated_images = []
                
                # Get annotated image
                annotated_img = result.plot()
                
                # Convert to PIL Image
                annotated_pil = Image.fromarray(annotated_img[..., ::-1])  # BGR to RGB
                
                # Get original dimensions
                orig_img = Image.open(image_path)
                orig_width, orig_height = orig_img.size
                
                # Convert to base64
                buffered = io.BytesIO()
                annotated_pil.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                annotated_images.append({
                    'image_name': image_filename,
                    'detections_count': len(detections),
                    'annotated_image_base64': img_base64,
                    'original_size': {
                        'width': orig_width,
                        'height': orig_height
                    }
                })
                
                response_data['annotated_images'] = annotated_images
            
            # Calculate processing time
            processing_time = time.time() - start_time
            response_data['processing_time_seconds'] = round(processing_time, 2)
            
            # Update task in database with success
            update_task_success(
                task_id=task_id,
                processing_time=processing_time,
                total_detections=len(detections),
                images_with_detections=1 if len(detections) > 0 else 0,
                species_counts=species_counts,
                result_data=response_data
            )
            
            # Save detections to database
            save_detections(task_id, detections, 'yolo')
            
            print(f"\n✅ Single image analysis complete! Task ID: {task_id}")
            print(f"   - Detections: {len(detections)}")
            print(f"   - Processing time: {processing_time:.2f}s\n")
            
            # Translate response to Spanish before returning
            response_data = translate_results_to_spanish(response_data)
            
            return jsonify(response_data), 200
            
        finally:
            # Clean up temp directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        
    except Exception as e:
        print(f"❌ Error in single image YOLO analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Update task with error if task_id exists
        if task_id:
            update_task_error(task_id, str(e))
        
        return jsonify({
            'success': False,
            'task_id': task_id,
            'error': 'Analysis failed',
            'message': str(e)
        }), 500


@app.route("/analyze-single-image-herdnet", methods=["POST"])
def analyze_single_image_herdnet_endpoint():
    """
    Analyze Single Image with HerdNet
    Upload a single image for HerdNet point-based detection (optimized for large aerial/satellite images)
    ---
    tags:
      - HerdNet
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Single wildlife image (PNG, JPG, JPEG, GIF, WebP, BMP, TIFF)
      - name: patch_size
        in: formData
        type: integer
        required: false
        default: 512
      - name: overlap
        in: formData
        type: integer
        required: false
        default: 160
      - name: rotation
        in: formData
        type: integer
        required: false
        default: 0
      - name: thumbnail_size
        in: formData
        type: integer
        required: false
        default: 256
      - name: include_thumbnails
        in: formData
        type: string
        required: false
        default: "true"
      - name: include_plots
        in: formData
        type: string
        required: false
        default: "false"
    responses:
      200:
        description: Analysis completed successfully
      400:
        description: Bad request
      500:
        description: Analysis failed
    """
    task_id = None
    start_time = time.time()
    
    try:
        # Check if HerdNet model is loaded
        if model is None:
            return jsonify({'error': 'HerdNet model not available'}), 503
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file is an image
        if not allowed_image(file.filename):
            return jsonify({'error': 'File must be an image (png, jpg, jpeg, gif, webp, bmp)'}), 400
        
        # Get optional parameters
        patch_size = int(request.form.get('patch_size', 512))
        overlap = int(request.form.get('overlap', 160))
        rotation = int(request.form.get('rotation', 0))
        thumbnail_size = int(request.form.get('thumbnail_size', 256))
        include_thumbnails = request.form.get('include_thumbnails', 'true').lower() == 'true'
        include_plots = request.form.get('include_plots', 'false').lower() == 'true'
        
        # Generate task ID
        task_id = generate_task_id()
        
        print(f"\n{'='*60}")
        print(f"HERDNET SINGLE IMAGE ANALYSIS")
        print(f"Task ID: {task_id}")
        print(f"Filename: {file.filename}")
        print(f"Patch: {patch_size}, Overlap: {overlap}, Rotation: {rotation}")
        print(f"{'='*60}\n")
        
        # Save task to database (status: processing)
        save_task(
            task_id=task_id,
            model_type='herdnet',
            filename=file.filename,
            num_images=1,
            processing_params={
                'patch_size': patch_size,
                'overlap': overlap,
                'rotation': rotation,
                'thumbnail_size': thumbnail_size,
                'include_thumbnails': include_thumbnails,
                'include_plots': include_plots
            }
        )
        
        # Create temp directory for processing
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Save uploaded image
            image_filename = secure_filename(file.filename)
            image_path = os.path.join(temp_dir, image_filename)
            file.save(image_path)
            
            # Process the image with HerdNet using the same approach as batch processing
            print(f"Processing image with HerdNet: {image_filename}")
            
            # Create a results directory
            results_dir = os.path.join(temp_dir, 'results')
            mkdir(results_dir)
            
            # Create a DataFrame with just this one image (same as batch processing)
            df = pd.DataFrame(data={
                'images': [image_filename], 
                'x': [0], 
                'y': [0], 
                'labels': [1]
            })
            
            # Setup transforms (same as batch processing)
            end_transforms = []
            if rotation != 0:
                end_transforms.append(Rotate90(k=rotation))
            end_transforms.append(DownSample(down_ratio=2, anno_type='point'))
            
            albu_transforms = [A.Normalize(mean=img_mean, std=img_std)]
            
            # Create dataset
            dataset = CSVDataset(
                csv_file=df,
                root_dir=temp_dir,
                albu_transforms=albu_transforms,
                end_transforms=end_transforms
            )
            
            # Create dataloader
            dataloader = DataLoader(
                dataset, 
                batch_size=1, 
                shuffle=False,
                sampler=torch.utils.data.SequentialSampler(dataset)
            )
            
            # Build the stitcher
            stitcher = HerdNetStitcher(
                model=model,
                size=(patch_size, patch_size),
                overlap=overlap,
                down_ratio=2,
                up=True,
                reduction='mean',
                device_name=device
            )
            
            # Build the evaluator
            metrics = PointsMetrics(5, num_classes=num_classes)
            evaluator = HerdNetEvaluator(
                model=model,
                dataloader=dataloader,
                metrics=metrics,
                lmds_kwargs=dict(kernel_size=(3, 3), adapt_ts=0.2, neg_ts=0.1),
                device_name=device,
                print_freq=1,
                stitcher=stitcher,
                work_dir=results_dir,
                header='[SINGLE IMAGE INFERENCE]'
            )
            
            # Run inference
            print(f"Running inference on single image...")
            evaluator.evaluate(wandb_flag=False, viz=False, log_meters=False)
            
            # Get detections from evaluator
            detections_df = evaluator.detections
            detections_df.dropna(inplace=True)
            detections_df['species'] = detections_df['labels'].map(classes_dict)
            
            # Process detections
            detections = []
            species_counts = {}
            
            for _, row in detections_df.iterrows():
                species = row['species']
                
                # Count species
                species_counts[species] = species_counts.get(species, 0) + 1
                
                detection = {
                    'images': row['images'],
                    'species': species,
                    'scores': float(row['scores']),
                    'x': float(row['x']),
                    'y': float(row['y'])
                }
                
                detections.append(detection)
            
            # Prepare response
            response_data = {
                'success': True,
                'task_id': task_id,
                'model': 'HerdNet',
                'summary': {
                    'total_images': 1,
                    'total_detections': len(detections),
                    'images_with_animals': 1 if len(detections) > 0 else 0,
                    'species_counts': species_counts
                },
                'detections': detections,
                'processing_params': {
                    'patch_size': patch_size,
                    'overlap': overlap,
                    'rotation': rotation,
                    'thumbnail_size': thumbnail_size,
                    'include_thumbnails': include_thumbnails,
                    'include_plots': include_plots
                }
            }
            
            # Load original image for thumbnails and plots
            if (include_thumbnails or include_plots) and len(detections) > 0:
                image = Image.open(image_path)
                
                # Apply rotation if specified (same as during inference)
                if rotation > 0:
                    rot_degrees = rotation * 90
                    image = image.rotate(rot_degrees, expand=True)
                
                image_np = np.array(image)
                
                # Extract point and class lists from detections
                point_list = [(int(det['y']), int(det['x'])) for det in detections]
                class_list = [detections_df.iloc[i]['labels'] for i in range(len(detections))]
            
            # Generate thumbnails if requested
            if include_thumbnails and len(detections) > 0:
                thumbnails = []
                half_size = thumbnail_size // 2
                
                for det in detections[:50]:  # Limit to first 50
                    x, y = int(det['x']), int(det['y'])
                    
                    # Extract thumbnail
                    x1 = max(0, x - half_size)
                    y1 = max(0, y - half_size)
                    x2 = min(image_np.shape[1], x + half_size)
                    y2 = min(image_np.shape[0], y + half_size)
                    
                    thumbnail = image_np[y1:y2, x1:x2]
                    thumbnail_pil = Image.fromarray(thumbnail)
                    
                    # Convert to base64
                    buffered = io.BytesIO()
                    thumbnail_pil.save(buffered, format="PNG")
                    thumb_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    
                    thumbnails.append({
                        'species': det['species'],
                        'scores': det['scores'],
                        'x': det['x'],
                        'y': det['y'],
                        'thumbnail_base64': thumb_base64
                    })
                
                response_data['thumbnails'] = thumbnails
            
            # Generate plot if requested
            if include_plots and len(detections) > 0:
                plots = []
                
                # Create plot with Spanish labels
                class_labels_spanish = [translate_to_spanish(ANIMAL_CLASSES.get(i, f"class_{i}")) 
                                       for i in range(len(ANIMAL_CLASSES))]
                plot_img = draw_points(
                    image=image_np.copy(),
                    points=point_list,
                    classes=class_list,
                    class_labels=class_labels_spanish,
                    radius=10
                )
                
                # Convert to PIL and base64
                plot_pil = Image.fromarray(plot_img)
                buffered = io.BytesIO()
                plot_pil.save(buffered, format="PNG")
                plot_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                plots.append({
                    'image_name': image_filename,
                    'detections_count': len(detections),
                    'plot_base64': plot_base64
                })
                
                response_data['plots'] = plots
            
            # Calculate processing time
            processing_time = time.time() - start_time
            response_data['processing_time_seconds'] = round(processing_time, 2)
            
            # Update task in database with success
            update_task_success(
                task_id=task_id,
                processing_time=processing_time,
                total_detections=len(detections),
                images_with_detections=1 if len(detections) > 0 else 0,
                species_counts=species_counts,
                result_data=response_data
            )
            
            # Save detections to database
            save_detections(task_id, detections, 'herdnet')
            
            print(f"\n✅ Single image HerdNet analysis complete! Task ID: {task_id}")
            print(f"   - Detections: {len(detections)}")
            print(f"   - Processing time: {processing_time:.2f}s\n")
            
            # Translate response to Spanish before returning
            response_data = translate_results_to_spanish(response_data)
            
            return jsonify(response_data), 200
            
        finally:
            # Clean up temp directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        
    except Exception as e:
        print(f"❌ Error in single image HerdNet analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Update task with error if task_id exists
        if task_id:
            update_task_error(task_id, str(e))
        
        return jsonify({
            'success': False,
            'task_id': task_id,
            'error': 'Analysis failed',
            'message': str(e)
        }), 500


@app.route("/tasks", methods=["GET"])
def get_tasks_endpoint():
    """
    Get All Tasks
    Retrieve a list of all analysis tasks with optional filtering
    ---
    tags:
      - Tasks
    parameters:
      - name: model_type
        in: query
        type: string
        required: false
        description: Filter by model type (yolo or herdnet)
      - name: status
        in: query
        type: string
        required: false
        description: Filter by status (completed, processing, or failed)
      - name: limit
        in: query
        type: integer
        required: false
        default: 100
        description: Maximum number of tasks to return
      - name: offset
        in: query
        type: integer
        required: false
        default: 0
        description: Pagination offset
    responses:
      200:
        description: Tasks retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
            tasks:
              type: array
              items:
                type: object
                properties:
                  task_id:
                    type: string
                  model_type:
                    type: string
                  status:
                    type: string
                  filename:
                    type: string
                  num_images:
                    type: integer
                  total_detections:
                    type: integer
                  created_at:
                    type: string
      500:
        description: Server error
    """
    try:
        model_type = request.args.get('model_type')
        status = request.args.get('status')
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        
        tasks = get_all_tasks(model_type, status, limit, offset)
        
        return jsonify({
            'success': True,
            'count': len(tasks),
            'tasks': tasks
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route("/tasks/<task_id>", methods=["GET"])
def get_task_endpoint(task_id):
    """
    Get Task by ID
    Retrieve a specific task and its complete results by task ID
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        type: string
        required: true
        description: Unique task identifier (UUID)
    responses:
      200:
        description: Task retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
            task:
              type: object
              properties:
                task_id:
                  type: string
                model_type:
                  type: string
                status:
                  type: string
                filename:
                  type: string
                num_images:
                  type: integer
                total_detections:
                  type: integer
                created_at:
                  type: string
                completed_at:
                  type: string
                processing_time_seconds:
                  type: number
                result_data:
                  type: object
                  description: Complete JSON response from the analysis
      404:
        description: Task not found
      500:
        description: Server error
    """
    try:
        task = get_task_by_id(task_id)
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        return jsonify({'success': True, 'task': task}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route("/database/stats", methods=["GET"])
def get_stats_endpoint():
    """
    Get Database Statistics
    Retrieve comprehensive statistics about all analyses in the database
    ---
    tags:
      - Database
    responses:
      200:
        description: Statistics retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
            statistics:
              type: object
              properties:
                total_tasks:
                  type: integer
                  description: Total number of analysis tasks
                tasks_by_model:
                  type: object
                  description: Task counts grouped by model type
                tasks_by_status:
                  type: object
                  description: Task counts grouped by status
                total_detections:
                  type: integer
                  description: Total number of animal detections
                species_distribution:
                  type: object
                  description: Detection counts grouped by species
      500:
        description: Server error
    """
    try:
        stats = get_database_stats()
        return jsonify({'success': True, 'statistics': stats}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Starting Flask server...")
    print("="*60)
    print(f"\n📊 Model Status:")
    print(f"  HerdNet:  ✓ Loaded ({num_classes} classes)")
    print(f"  YOLOv11:  {'✓ Loaded' if yolo_loaded else '✗ Not loaded'}")
    print(f"\n💻 Device: {device}")
    print(f"🦁 Species: {list(classes_dict.values())}")
    print("\n" + "="*60)
    print("  Server: http://0.0.0.0:8000")
    print("  Health: http://localhost:8000/health")
    print("="*60 + "\n")
    app.run(host="0.0.0.0", port=8000, debug=True)
