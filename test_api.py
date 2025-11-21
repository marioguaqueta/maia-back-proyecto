#!/usr/bin/env python3
"""
Test script for the HerdNet Animal Detection API

Usage:
    python test_api.py <path_to_zip_file>

Example:
    python test_api.py ./test_images.zip
    python test_api.py ./test_images.zip --rotation 1 --patch-size 1024
"""

import requests
import sys
import json
import os
import argparse
from pathlib import Path


def test_health_endpoint(base_url="http://localhost:5000"):
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✓ Health Check Successful!")
            print(f"  Status: {data.get('status')}")
            print(f"  Model Loaded: {data.get('model_loaded')}")
            print(f"  Device: {data.get('device')}")
            print(f"  Number of Classes: {data.get('num_classes')}")
            print(f"  Classes: {list(data.get('classes', {}).values())}")
            return True
        else:
            print(f"\n✗ Health check failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n✗ Error connecting to server: {str(e)}")
        print("  Make sure the Flask server is running!")
        return False


def test_analyze_endpoint(
    zip_path, 
    base_url="http://localhost:5000",
    patch_size=512,
    overlap=160,
    rotation=0,
    thumbnail_size=256,
    include_thumbnails=True,
    include_plots=False
):
    """Test the image analysis endpoint"""
    print("\n" + "="*60)
    print("Testing Image Analysis Endpoint")
    print("="*60)
    
    # Check if file exists
    if not os.path.exists(zip_path):
        print(f"\n✗ Error: File not found: {zip_path}")
        return False
    
    print(f"\nUploading: {zip_path}")
    print(f"Parameters:")
    print(f"  Patch Size: {patch_size}")
    print(f"  Overlap: {overlap}")
    print(f"  Rotation: {rotation}x90°")
    print(f"  Thumbnail Size: {thumbnail_size}")
    print(f"  Include Thumbnails: {include_thumbnails}")
    print(f"  Include Plots: {include_plots}")
    print("\nSending request... (this may take a while for large files)")
    
    try:
        with open(zip_path, 'rb') as f:
            files = {'file': (os.path.basename(zip_path), f, 'application/zip')}
            data = {
                'patch_size': patch_size,
                'overlap': overlap,
                'rotation': rotation,
                'thumbnail_size': thumbnail_size,
                'include_thumbnails': str(include_thumbnails).lower(),
                'include_plots': str(include_plots).lower()
            }
            
            response = requests.post(
                f"{base_url}/analyze-image",
                files=files,
                data=data,
                timeout=300  # 5 minute timeout
            )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n" + "="*60)
            print("✓ Analysis Successful!")
            print("="*60)
            
            # Print summary
            summary = result.get('summary', {})
            print("\n📊 SUMMARY:")
            print(f"  Total Images: {summary.get('total_images', 0)}")
            print(f"  Images with Detections: {summary.get('images_with_detections', 0)}")
            print(f"  Images without Detections: {summary.get('images_without_detections', 0)}")
            print(f"  Total Detections: {summary.get('total_detections', 0)}")
            
            # Print species counts
            species_counts = summary.get('species_counts', {})
            if species_counts:
                print("\n🦁 SPECIES DETECTED:")
                for species, count in sorted(species_counts.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {species}: {count}")
            
            # Print processing parameters
            params = result.get('processing_params', {})
            print("\n⚙️  PROCESSING PARAMETERS:")
            for key, value in params.items():
                print(f"  {key}: {value}")
            
            # Print detection details
            detections = result.get('detections', [])
            if detections:
                print(f"\n🔍 DETECTIONS (showing first 10 of {len(detections)}):")
                for i, detection in enumerate(detections[:10]):
                    img_name = detection.get('images', 'unknown')
                    species = detection.get('species', 'unknown')
                    score = detection.get('scores', 0)
                    x = detection.get('x', 0)
                    y = detection.get('y', 0)
                    print(f"  {i+1}. {img_name}: {species} at ({x}, {y}) - confidence: {score:.2%}")
            
            # Print thumbnail info
            thumbnails = result.get('thumbnails', [])
            if thumbnails:
                print(f"\n🖼️  THUMBNAILS: {len(thumbnails)} generated")
                print(f"  (Base64 data included in response)")
            
            # Print plot info
            plots = result.get('plots', [])
            if plots:
                print(f"\n📈 PLOTS: {len(plots)} generated")
                print(f"  (Base64 data included in response)")
            
            # Save full response to file
            output_file = 'api_response.json'
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Full response saved to: {output_file}")
            
            # Optionally save thumbnails and plots as separate files
            if thumbnails and len(thumbnails) <= 20:
                save_images_from_response(result)
            
            return True
            
        else:
            print(f"\n✗ Analysis failed with status {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data.get('error', 'Unknown error')}")
                print(f"Message: {error_data.get('message', 'No message provided')}")
            except:
                print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n✗ Request timed out. The file might be too large or processing is taking too long.")
        return False
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def save_images_from_response(response_data):
    """Save thumbnails and plots from API response"""
    import base64
    
    print("\n📁 Saving images locally...")
    
    # Create output directories
    os.makedirs('output_thumbnails', exist_ok=True)
    os.makedirs('output_plots', exist_ok=True)
    
    # Save thumbnails
    thumbnails = response_data.get('thumbnails', [])
    for thumb in thumbnails:
        img_name = thumb.get('image_name', 'unknown')
        det_id = thumb.get('detection_id', 0)
        species = thumb.get('species', 'unknown')
        base64_data = thumb.get('thumbnail_base64', '')
        
        if base64_data:
            filename = f"{Path(img_name).stem}_{det_id}_{species}.jpg"
            filepath = os.path.join('output_thumbnails', filename)
            
            img_data = base64.b64decode(base64_data)
            with open(filepath, 'wb') as f:
                f.write(img_data)
    
    if thumbnails:
        print(f"  ✓ Saved {len(thumbnails)} thumbnails to output_thumbnails/")
    
    # Save plots
    plots = response_data.get('plots', [])
    for plot in plots:
        img_name = plot.get('image_name', 'unknown')
        base64_data = plot.get('plot_base64', '')
        
        if base64_data:
            filename = f"plot_{img_name}"
            filepath = os.path.join('output_plots', filename)
            
            img_data = base64.b64decode(base64_data)
            with open(filepath, 'wb') as f:
                f.write(img_data)
    
    if plots:
        print(f"  ✓ Saved {len(plots)} plots to output_plots/")


def main():
    parser = argparse.ArgumentParser(description='Test HerdNet Animal Detection API')
    parser.add_argument('zip_file', help='Path to ZIP file containing images')
    parser.add_argument('--url', default='http://localhost:5000', help='API base URL')
    parser.add_argument('--patch-size', type=int, default=512, help='Patch size for stitching')
    parser.add_argument('--overlap', type=int, default=160, help='Overlap for stitching')
    parser.add_argument('--rotation', type=int, default=0, help='Number of 90-degree rotations (0-3)')
    parser.add_argument('--thumbnail-size', type=int, default=256, help='Thumbnail size')
    parser.add_argument('--no-thumbnails', action='store_true', help='Exclude thumbnails from response')
    parser.add_argument('--include-plots', action='store_true', help='Include plots in response')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🦁 HerdNet Animal Detection API Test")
    print("="*60)
    
    # Test health endpoint first
    if not test_health_endpoint(args.url):
        print("\n❌ Server not responding. Please start the Flask server first.")
        sys.exit(1)
    
    # Test analysis endpoint
    success = test_analyze_endpoint(
        args.zip_file,
        base_url=args.url,
        patch_size=args.patch_size,
        overlap=args.overlap,
        rotation=args.rotation,
        thumbnail_size=args.thumbnail_size,
        include_thumbnails=not args.no_thumbnails,
        include_plots=args.include_plots
    )
    
    if success:
        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60 + "\n")
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("❌ Tests failed!")
        print("="*60 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
