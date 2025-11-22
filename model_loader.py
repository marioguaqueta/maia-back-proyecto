"""
Model Loader - Downloads models from Google Drive if not present locally
"""

import os
import gdown

# Google Drive folder ID
GDRIVE_FOLDER_ID = "11uMn45darEtFHz1CLe94hxVtRRA99ERd"

# Model configurations
MODELS = {
    'yolo': {
        'filename': 'best.pt',
        'description': 'YOLOv11 model'
    },
    'herdnet': {
        'filename': 'herdnet_model.pth',
        'description': 'HerdNet model'
    }
}


def download_model(model_name):
    """Download a model from Google Drive if it doesn't exist."""
    if model_name not in MODELS:
        return False
    
    config = MODELS[model_name]
    filename = config['filename']
    
    # Check if already exists
    if os.path.exists(filename):
        size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"✓ {config['description']} already exists: {filename} ({size_mb:.1f} MB)")
        return True
    
    print(f"\n📥 Downloading {config['description']} from Google Drive...")
    print(f"   File: {filename}")
    
    try:
        # Download folder and extract file
        folder_url = f"https://drive.google.com/drive/folders/{GDRIVE_FOLDER_ID}"
        gdown.download_folder(url=folder_url, output=".", quiet=False, use_cookies=False)
        
        if os.path.exists(filename):
            size_mb = os.path.getsize(filename) / (1024 * 1024)
            print(f"✅ Downloaded {filename} ({size_mb:.1f} MB)")
            return True
        else:
            print(f"❌ Failed to download {filename}")
            return False
    except Exception as e:
        print(f"❌ Error downloading {filename}: {str(e)}")
        return False


def ensure_models():
    """Ensure all models are available."""
    print("\n" + "="*60)
    print("🔍 Checking model files...")
    print("="*60)
    
    status = {}
    for model_name in ['yolo', 'herdnet']:
        status[model_name] = download_model(model_name)
    
    print("\n" + "="*60)
    print(f"YOLOv11:  {'✓' if status['yolo'] else '✗'}")
    print(f"HerdNet:  {'✓' if status['herdnet'] else '✗'}")
    print("="*60 + "\n")
    
    return status


if __name__ == "__main__":
    ensure_models()

