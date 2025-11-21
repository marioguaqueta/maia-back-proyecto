#!/usr/bin/env python3
"""
Helper script to create a test ZIP file with sample images
"""
import zipfile
import sys
from pathlib import Path


def create_test_zip(image_dir, output_zip):
    """
    Create a ZIP file from a directory of images
    
    Args:
        image_dir: Path to directory containing images
        output_zip: Output ZIP file path
    """
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'}
    image_dir = Path(image_dir)
    
    if not image_dir.exists():
        print(f"Error: Directory {image_dir} does not exist")
        return False
    
    # Find all image files
    image_files = []
    for ext in image_extensions:
        image_files.extend(image_dir.glob(f'**/*{ext}'))
        image_files.extend(image_dir.glob(f'**/*{ext.upper()}'))
    
    if not image_files:
        print(f"Error: No image files found in {image_dir}")
        return False
    
    print(f"Found {len(image_files)} images")
    print(f"Creating ZIP file: {output_zip}")
    
    # Create ZIP file
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for img_file in image_files:
            # Get relative path
            arcname = img_file.relative_to(image_dir)
            print(f"  Adding: {arcname}")
            zipf.write(img_file, arcname)
    
    print(f"\n✓ Successfully created {output_zip}")
    print(f"  Total files: {len(image_files)}")
    return True


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print(f"  {sys.argv[0]} <image_directory> <output_zip>")
        print("\nExample:")
        print(f"  {sys.argv[0]} ./test_images ./test_images.zip")
        sys.exit(1)
    
    image_dir = sys.argv[1]
    output_zip = sys.argv[2]
    
    if create_test_zip(image_dir, output_zip):
        print("\nYou can now test the API with:")
        print(f"  python test_api.py {output_zip}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

