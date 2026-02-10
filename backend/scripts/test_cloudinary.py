"""
scripts/test_cloudinary.py

Test script to verify Cloudinary connection.
Uploads a dummy image and prints the URL.

Run with:
    docker compose exec backend python scripts/test_cloudinary.py
"""

import os
import sys
import django

# Add the parent directory to the Python path so we can import Django settings
sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

import cloudinary
import cloudinary.uploader


def test_upload():
    print("Testing Cloudinary connection...")
    print(f"Cloud name: {cloudinary.config().cloud_name}")

    # Create a tiny test image in memory
    from PIL import Image
    import io

    img = Image.new("RGB", (100, 100), color="blue")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Upload to Cloudinary
    try:
        result = cloudinary.uploader.upload(
            buffer,
            folder="housing_test",  # Optional: organize in folders
            public_id="test_image",
        )

        print("✅ Upload successful!")
        print(f"Image URL: {result['secure_url']}")
        print(f"Public ID: {result['public_id']}")
        return True
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False


if __name__ == "__main__":
    success = test_upload()
    sys.exit(0 if success else 1)
