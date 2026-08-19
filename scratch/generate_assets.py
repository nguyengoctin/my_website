import os
from PIL import Image, ImageDraw, ImageFilter

def create_favicon_svg():
    # 100% Transparent Background SVG Favicon
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="blueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#60a5fa" />
      <stop offset="100%" stop-color="#3b82f6" />
    </linearGradient>
    <linearGradient id="pinkGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f472b6" />
      <stop offset="100%" stop-color="#ec4899" />
    </linearGradient>
  </defs>

  <!-- 100% Transparent Background - Pure Code Bracket Symbols -->
  <g stroke-linecap="round" stroke-linejoin="round">
    <!-- Left Bracket < (Blue #3b82f6 / #60a5fa) -->
    <path d="M 175 135 L 60 256 L 175 377" fill="none" stroke="url(#blueGrad)" stroke-width="58" />
    
    <!-- Slash / (Blue #3b82f6 / #60a5fa) -->
    <path d="M 295 110 L 217 402" fill="none" stroke="url(#blueGrad)" stroke-width="56" />
    
    <!-- Right Bracket > (Pink #ec4899 / #f472b6) -->
    <path d="M 337 135 L 452 256 L 337 377" fill="none" stroke="url(#pinkGrad)" stroke-width="58" />
  </g>
</svg>'''
    return svg_content

def generate_transparent_favicon_images(output_dir):
    # Base high-res canvas (512x512) 100% Transparent
    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    blue_color = (59, 130, 246, 255)   # #3b82f6
    blue_light = (96, 165, 250, 255)   # #60a5fa
    pink_color = (236, 72, 153, 255)   # #ec4899
    pink_light = (244, 114, 182, 255)  # #f472b6

    # Draw Left Bracket < in Blue
    # Points: (175, 135) -> (60, 256) -> (175, 377)
    draw.line([(175, 135), (60, 256)], fill=blue_light, width=56)
    draw.line([(60, 256), (175, 377)], fill=blue_color, width=56)
    for pt in [(175, 135), (60, 256), (175, 377)]:
        draw.ellipse([pt[0] - 28, pt[1] - 28, pt[0] + 28, pt[1] + 28], fill=blue_color)

    # Draw Slash / in Blue
    # Points: (295, 110) -> (217, 402)
    draw.line([(295, 110), (217, 402)], fill=blue_light, width=54)
    for pt in [(295, 110), (217, 402)]:
        draw.ellipse([pt[0] - 27, pt[1] - 27, pt[0] + 27, pt[1] + 27], fill=blue_light)

    # Draw Right Bracket > in Pink
    # Points: (337, 135) -> (452, 256) -> (337, 377)
    draw.line([(337, 135), (452, 256)], fill=pink_light, width=56)
    draw.line([(452, 256), (337, 377)], fill=pink_color, width=56)
    for pt in [(337, 135), (452, 256), (337, 377)]:
        draw.ellipse([pt[0] - 28, pt[1] - 28, pt[0] + 28, pt[1] + 28], fill=pink_color)

    # Save 100% Transparent SVG
    svg_path = os.path.join(output_dir, "favicon.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(create_favicon_svg())

    # Save PNG variations with high-quality Lanczos resampling
    img.save(os.path.join(output_dir, "apple-touch-icon.png"), "PNG")
    
    img_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
    img_192.save(os.path.join(output_dir, "favicon.png"), "PNG")
    
    img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
    img_32.save(os.path.join(output_dir, "favicon-32x32.png"), "PNG")

    img_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
    img_16.save(os.path.join(output_dir, "favicon-16x16.png"), "PNG")

    # Save favicon.ico with transparency
    img.save(os.path.join(output_dir, "favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

if __name__ == "__main__":
    static_dir = "/home/ngoctin/Projects/my_website/static"
    print("Generating 100% Transparent Favicon files...")
    generate_transparent_favicon_images(static_dir)
    print("Transparent Favicon files generated successfully in", static_dir)
