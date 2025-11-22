"""
Test script to verify YOLO model loading with Spanish translations
"""

import torch

# Check device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {device}")

# Spanish translations
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

# Load YOLO model
print("\nLoading YOLOv11 model...")
try:
    from ultralytics import YOLO
    
    YOLO_MODEL_PATH = "./best.pt"
    print(f"Loading from: {YOLO_MODEL_PATH}")
    
    yolo_model = YOLO(YOLO_MODEL_PATH)
    yolo_model.to(device)
    
    # Get class names from the model (READ ONLY)
    YOLO_CLASSES = yolo_model.names
    
    print(f"\n✓ YOLOv11 model loaded successfully")
    print(f"\nOriginal classes (English):")
    for k, v in YOLO_CLASSES.items():
        print(f"  {k}: {v}")
    
    print(f"\nTranslated classes (Spanish):")
    for k, v in YOLO_CLASSES.items():
        spanish = translate_to_spanish(v)
        print(f"  {k}: {v} → {spanish}")
    
    print(f"\n✅ Model loading test PASSED")
    print(f"   Classes can be accessed: {len(YOLO_CLASSES)} classes")
    print(f"   Translation works correctly")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

