#!/usr/bin/env python3
"""
scripts/optimize_images.py
Tự động quét, resize và chuyển đổi toàn bộ ảnh (PNG, JPG) sang WebP với chuẩn chất lượng cao.
"""

import os
import sys
from PIL import Image

def optimize_and_convert_to_webp(target_dir="static/images", max_width=1600, quality=85):
    if not os.path.exists(target_dir):
        print(f"Thư mục không tồn tại: {target_dir}")
        return

    converted_count = 0
    total_saved_bytes = 0

    for root, _, files in os.walk(target_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in ('.png', '.jpg', '.jpeg'):
                orig_path = os.path.join(root, f)
                webp_name = os.path.splitext(f)[0] + '.webp'
                webp_path = os.path.join(root, webp_name)

                try:
                    orig_size = os.path.getsize(orig_path)
                    with Image.open(orig_path) as img:
                        w, h = img.size
                        if w > max_width:
                            new_w = max_width
                            new_h = int(h * (max_width / w))
                            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

                        img.save(webp_path, 'WEBP', quality=quality, method=6)

                    new_size = os.path.getsize(webp_path)
                    saved = orig_size - new_size
                    total_saved_bytes += max(0, saved)
                    converted_count += 1

                    print(f"✓ Đã chuyển đổi: {orig_path} -> {webp_name} ({orig_size/1024:.1f}KB -> {new_size/1024:.1f}KB)")
                    os.remove(orig_path)
                except Exception as e:
                    print(f"✗ Lỗi khi xử lý {orig_path}: {e}")

    print(f"\n Hoàn tất! Đã chuyển đổi {converted_count} file sang WebP. Tiết kiệm: {total_saved_bytes/1024:.1f} KB")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else "static/images"
    optimize_and_convert_to_webp(target)
