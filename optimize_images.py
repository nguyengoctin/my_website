#!/usr/bin/env python3
import os
import sys
from PIL import Image

def optimize_directory(target_dir, max_width=1400, quality=75):
    """
    Recursively scans target_dir, resizes large images, converts PNG/JPG to WebP 
    with maximum compression, and removes original uncompressed files.
    """
    if not os.path.exists(target_dir):
        print(f"❌ Directory '{target_dir}' does not exist.")
        return

    print(f"🚀 Starting image optimization scan in: {target_dir}")
    print(f"⚙️ Settings: Max Width = {max_width}px | Quality = {quality}% | Format = WebP (method 6)")
    print("-" * 75)

    total_orig_size = 0
    total_webp_size = 0
    converted_count = 0

    for root, _, files in os.walk(target_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.webp']:
                full_path = os.path.join(root, file)
                base_name = os.path.splitext(file)[0]
                webp_path = os.path.join(root, base_name + ".webp")

                orig_size = os.path.getsize(full_path)
                total_orig_size += orig_size

                try:
                    with Image.open(full_path) as img:
                        # Convert RGBA/P to RGB if needed, or handle transparency
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGBA")
                        else:
                            img = img.convert("RGB")

                        # Smart Downscaling if wider than max_width
                        w, h = img.size
                        if w > max_width:
                            new_h = int((max_width / w) * h)
                            img = img.resize((max_width, new_h), Image.Resampling.LANCZOS)

                        # Save with maximal WebP compression (method 6 is highest compression in libwebp)
                        img.save(webp_path, "WEBP", quality=quality, method=6, optimize=True)

                    webp_size = os.path.getsize(webp_path)
                    total_webp_size += webp_size
                    converted_count += 1

                    saved_percent = (1 - webp_size / orig_size) * 100
                    print(f"✅ {file:<30} | {orig_size/1024:>7.1f} KB -> {webp_size/1024:>6.1f} KB | 📉 -{saved_percent:.1f}%")

                    # Remove original uncompressed file if webp was successfully created
                    if os.path.exists(webp_path) and full_path != webp_path:
                        os.remove(full_path)

                except Exception as e:
                    print(f"⚠️ Error processing {file}: {e}")

    print("-" * 75)
    if converted_count > 0:
        total_saved = total_orig_size - total_webp_size
        total_saved_percent = (1 - total_webp_size / total_orig_size) * 100
        print(f"🎉 Optimized {converted_count} images!")
        print(f"📦 Total size before : {total_orig_size / 1024 / 1024:.2f} MB")
        print(f"📦 Total size after  : {total_webp_size / 1024 / 1024:.2f} MB")
        print(f"✨ Space saved       : {total_saved / 1024 / 1024:.2f} MB (-{total_saved_percent:.1f}%)")
    else:
        print("ℹ️ No PNG/JPG images found to process.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "/home/ngoctin/Projects/my_website/static/images"
    optimize_directory(target)
