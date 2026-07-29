import os
from PIL import Image

img_dir = "/home/ngoctin/Projects/my_website/static/images"

for filename in os.listdir(img_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        full_path = os.path.join(img_dir, filename)
        base_name = os.path.splitext(filename)[0]
        webp_path = os.path.join(img_dir, base_name + ".webp")
        
        try:
            with Image.open(full_path) as img:
                img.convert("RGB").save(webp_path, "WEBP", quality=75, optimize=True)
                orig_size = os.path.getsize(full_path)
                webp_size = os.path.getsize(webp_path)
                print(f"Converted {filename}: {orig_size} bytes -> {webp_size} bytes (saved to {base_name}.webp)")
        except Exception as e:
            print(f"Error converting {filename}: {e}")
