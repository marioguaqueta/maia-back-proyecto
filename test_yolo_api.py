#!/usr/bin/env python3
"""
Test script for YOLOv11 API endpoint

This script tests the /analyze-yolo endpoint which uses YOLOv11 model
for animal detection in images from ZIP files.

Usage:
    python test_yolo_api.py <path_to_zip_file> [conf_threshold] [iou_threshold] [img_size]

Examples:
    python test_yolo_api.py general_dataset/test.zip
    python test_yolo_api.py general_dataset/test.zip 0.3 0.5 640
    python test_yolo_api.py general_dataset/test2.zip 0.25 0.45 1024
"""

import requests
import json
import sys
from pathlib import Path
from datetime import datetime


def test_health_endpoint(base_url="http://localhost:8000"):
    """
    Test the /health endpoint to check if both models are loaded
    
    Args:
        base_url: Base URL of the API
    
    Returns:
        bool: True if healthy, False otherwise
    """
    url = f"{base_url}/health"
    
    print(f"\n{'='*60}")
    print("Testing Health Endpoint")
    print(f"URL: {url}")
    print(f"{'='*60}\n")
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✓ API is healthy!")
            print(f"\nModels Status:")
            
            for model_name, model_info in data.get('models', {}).items():
                status = "✓ Loaded" if model_info.get('loaded') else "✗ Not Loaded"
                print(f"\n  {model_name.upper()}:")
                print(f"    Status: {status}")
                print(f"    Device: {model_info.get('device', 'N/A')}")
                print(f"    Classes: {model_info.get('num_classes', 0)}")
                
                if model_info.get('classes'):
                    print(f"    Available classes: {list(model_info['classes'].values())[:5]}...")
            
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error connecting to API: {str(e)}")
        return False


def test_models_info(base_url="http://localhost:8000"):
    """
    Test the /models/info endpoint
    
    Args:
        base_url: Base URL of the API
    
    Returns:
        bool: True if successful, False otherwise
    """
    url = f"{base_url}/models/info"
    
    print(f"\n{'='*60}")
    print("Testing Models Info Endpoint")
    print(f"URL: {url}")
    print(f"{'='*60}\n")
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Models information retrieved!")
            print("\nAvailable Models:")
            
            for model_name, model_info in data.get('models', {}).items():
                print(f"\n  {model_name.upper()}:")
                print(f"    Loaded: {model_info.get('loaded')}")
                print(f"    Endpoint: {model_info.get('endpoint')}")
                print(f"    Number of classes: {model_info.get('num_classes')}")
                
                if model_info.get('classes'):
                    print(f"    Classes: {model_info.get('classes')}")
            
            return True
        else:
            print(f"✗ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_yolo_endpoint(
    zip_path,
    base_url="http://localhost:8000",
    conf_threshold=0.25,
    iou_threshold=0.45,
    img_size=640,
    save_results=True
):
    """
    Test the /analyze-yolo endpoint with a ZIP file
    
    Args:
        zip_path: Path to ZIP file containing images
        base_url: Base URL of the API
        conf_threshold: Confidence threshold for detections (0.0 - 1.0)
        iou_threshold: IOU threshold for NMS (0.0 - 1.0)
        img_size: Image size for inference (e.g., 640, 1024)
        save_results: Whether to save results to JSON file
    
    Returns:
        bool: True if successful, False otherwise
    """
    url = f"{base_url}/analyze-yolo"
    
    print(f"\n{'='*60}")
    print("Testing YOLOv11 Analysis Endpoint")
    print(f"URL: {url}")
    print(f"ZIP file: {zip_path}")
    print(f"{'='*60}")
    print(f"\nParameters:")
    print(f"  Confidence threshold: {conf_threshold}")
    print(f"  IOU threshold: {iou_threshold}")
    print(f"  Image size: {img_size}")
    print(f"{'='*60}\n")
    
    # Prepare the request
    try:
        with open(zip_path, 'rb') as f:
            files = {'file': f}
            data = {
                'conf_threshold': conf_threshold,
                'iou_threshold': iou_threshold,
                'img_size': img_size
            }
            
            # Send request
            print("Sending request to API...")
            print("(This may take a while depending on the number of images)\n")
            
            response = requests.post(url, files=files, data=data, timeout=600)
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n{'='*60}")
            print("✓ SUCCESS! Analysis Complete")
            print(f"{'='*60}\n")
            
            # Display summary
            summary = result.get('summary', {})
            print("Summary:")
            print(f"  Model: {result.get('model', 'N/A')}")
            print(f"  Total images processed: {summary.get('total_images', 0)}")
            print(f"  Images with animals: {summary.get('images_with_animals', 0)}")
            print(f"  Images without animals: {summary.get('images_without_animals', 0)}")
            print(f"  Total detections: {summary.get('total_detections', 0)}")
            
            # Display species counts
            species_counts = summary.get('species_counts', {})
            if species_counts:
                print(f"\nSpecies Detected:")
                for species, count in sorted(species_counts.items(), key=lambda x: x[1], reverse=True):
                    print(f"  • {species}: {count} detection(s)")
            else:
                print(f"\nNo animals detected in the images.")
            
            # Display sample detections
            detections = result.get('detections', [])
            if detections:
                print(f"\nSample Detections (first 5):")
                for i, det in enumerate(detections[:5]):
                    print(f"\n  Detection {i+1}:")
                    print(f"    Image: {det.get('image')}")
                    print(f"    Class: {det.get('class_name')} (ID: {det.get('class_id')})")
                    print(f"    Confidence: {det.get('confidence', 0):.2%}")
                    print(f"    Center: ({det.get('center', {}).get('x', 0):.0f}, {det.get('center', {}).get('y', 0):.0f})")
            
            # Display processing parameters
            params = result.get('processing_params', {})
            if params:
                print(f"\nProcessing Parameters Used:")
                print(f"  Confidence threshold: {params.get('conf_threshold')}")
                print(f"  IOU threshold: {params.get('iou_threshold')}")
                print(f"  Image size: {params.get('img_size')}")
            
            # Save results to file
            if save_results:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = f'yolo_results_{timestamp}.json'
                
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                
                print(f"\n{'='*60}")
                print(f"✓ Full results saved to: {output_file}")
                print(f"{'='*60}\n")
            
            return True
            
        else:
            print(f"\n{'='*60}")
            print("✗ ANALYSIS FAILED")
            print(f"{'='*60}")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}\n")
            return False
            
    except FileNotFoundError:
        print(f"✗ Error: File not found: {zip_path}\n")
        return False
    except requests.exceptions.Timeout:
        print(f"✗ Error: Request timed out. The server might be processing a large ZIP file.\n")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        return False


def print_usage():
    """Print usage information"""
    print("\n" + "="*60)
    print("YOLOv11 API Test Script")
    print("="*60)
    print("\nUsage:")
    print("  python test_yolo_api.py <path_to_zip_file> [conf_threshold] [iou_threshold] [img_size]")
    print("\nArguments:")
    print("  path_to_zip_file : Path to ZIP file containing images (required)")
    print("  conf_threshold   : Confidence threshold 0.0-1.0 (optional, default: 0.25)")
    print("  iou_threshold    : IOU threshold 0.0-1.0 (optional, default: 0.45)")
    print("  img_size         : Image size for inference (optional, default: 640)")
    print("\nExamples:")
    print("  python test_yolo_api.py general_dataset/test.zip")
    print("  python test_yolo_api.py general_dataset/test.zip 0.3")
    print("  python test_yolo_api.py general_dataset/test.zip 0.3 0.5")
    print("  python test_yolo_api.py general_dataset/test.zip 0.3 0.5 1024")
    print("\nCommon image sizes:")
    print("  • 640  : Standard (fast, good for most cases)")
    print("  • 1024 : High resolution (slower, better for small objects)")
    print("  • 1280 : Very high resolution (slowest, best accuracy)")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    # Check arguments
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    zip_path = sys.argv[1]
    
    # Validate ZIP file exists
    if not Path(zip_path).exists():
        print(f"\n✗ Error: File not found: {zip_path}\n")
        print_usage()
        sys.exit(1)
    
    # Parse optional parameters with validation
    conf_threshold = 0.25
    iou_threshold = 0.45
    img_size = 640
    
    try:
        if len(sys.argv) > 2:
            conf_threshold = float(sys.argv[2])
            if not 0.0 <= conf_threshold <= 1.0:
                print(f"✗ Error: conf_threshold must be between 0.0 and 1.0")
                sys.exit(1)
        
        if len(sys.argv) > 3:
            iou_threshold = float(sys.argv[3])
            if not 0.0 <= iou_threshold <= 1.0:
                print(f"✗ Error: iou_threshold must be between 0.0 and 1.0")
                sys.exit(1)
        
        if len(sys.argv) > 4:
            img_size = int(sys.argv[4])
            if img_size < 32 or img_size > 2048:
                print(f"✗ Error: img_size must be between 32 and 2048")
                sys.exit(1)
    
    except ValueError as e:
        print(f"\n✗ Error: Invalid parameter value: {str(e)}\n")
        print_usage()
        sys.exit(1)
    
    # Run tests
    print("\n" + "="*60)
    print("Starting YOLOv11 API Tests")
    print("="*60)
    
    # Test 1: Health check
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print("\n✗ Cannot proceed: API health check failed")
        print("Make sure the Flask server is running on http://localhost:8000\n")
        sys.exit(1)
    
    # Test 2: Models info
    test_models_info()
    
    # Test 3: YOLOv11 analysis
    success = test_yolo_endpoint(
        zip_path,
        conf_threshold=conf_threshold,
        iou_threshold=iou_threshold,
        img_size=img_size,
        save_results=True
    )
                # Display annotated images info

    
    # Final result
    print("\n" + "="*60)
    if success:
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ TESTS FAILED")
    print("="*60 + "\n")
    
    sys.exit(0 if success else 1)