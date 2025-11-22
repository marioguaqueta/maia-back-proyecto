"""
Verification script to test that all components are properly set up
"""

import sys
import os

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required = {
        'flask': 'Flask',
        'torch': 'PyTorch',
        'streamlit': 'Streamlit',
        'plotly': 'Plotly',
        'gdown': 'gdown',
        'PIL': 'Pillow',
        'pandas': 'pandas',
        'requests': 'requests'
    }
    
    missing = []
    for module, name in required.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - MISSING")
            missing.append(name)
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed\n")
    return True


def check_files():
    """Check if all required files exist."""
    print("🔍 Checking files...")
    
    required_files = [
        'app.py',
        'database.py',
        'model_loader.py',
        'streamlit_app.py',
        'start.sh',
        'start.bat',
        'requirements.txt',
        'README.md'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    
    print("✅ All required files present\n")
    return True


def check_database():
    """Check if database can be initialized."""
    print("🔍 Checking database...")
    
    try:
        from database import init_database, generate_task_id
        
        # Initialize database
        init_database()
        print("  ✓ Database initialized")
        
        # Test task ID generation
        task_id = generate_task_id()
        print(f"  ✓ Task ID generation works: {task_id[:8]}...")
        
        # Check if database file exists
        if os.path.exists('wildlife_detection.db'):
            print("  ✓ Database file created")
        
        print("✅ Database module working\n")
        return True
    except Exception as e:
        print(f"❌ Database error: {str(e)}\n")
        return False


def check_model_loader():
    """Check if model loader module works."""
    print("🔍 Checking model loader...")
    
    try:
        from model_loader import MODELS, GDRIVE_FOLDER_ID
        
        print(f"  ✓ Google Drive folder ID: {GDRIVE_FOLDER_ID}")
        print(f"  ✓ Models configured: {list(MODELS.keys())}")
        
        print("✅ Model loader module working\n")
        print("⚠️  Models will download on first app run")
        print(f"   Expected files: {', '.join([MODELS[m]['filename'] for m in MODELS])}\n")
        return True
    except Exception as e:
        print(f"❌ Model loader error: {str(e)}\n")
        return False


def main():
    """Run all checks."""
    print("="*60)
    print("🚀 Wildlife Detection System - Setup Verification")
    print("="*60)
    print()
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Files", check_files),
        ("Database", check_database),
        ("Model Loader", check_model_loader)
    ]
    
    results = {}
    for name, check_func in checks:
        results[name] = check_func()
    
    # Summary
    print("="*60)
    print("📊 Summary")
    print("="*60)
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print("="*60)
        print("🎉 All checks passed! You're ready to go!")
        print("="*60)
        print()
        print("To start the system:")
        print("  • Linux/Mac: ./start.sh")
        print("  • Windows:   start.bat")
        print()
        print("Or manually:")
        print("  1. Terminal 1: python app.py")
        print("  2. Terminal 2: streamlit run streamlit_app.py")
        print()
        print("Then access:")
        print("  • Streamlit UI: http://localhost:8501")
        print("  • Flask API:    http://localhost:8000")
        print("="*60)
        sys.exit(0)
    else:
        print("="*60)
        print("❌ Some checks failed. Please fix the issues above.")
        print("="*60)
        sys.exit(1)


if __name__ == "__main__":
    main()

