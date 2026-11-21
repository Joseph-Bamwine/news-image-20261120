#!/usr/bin/env python3
# News image for 2026-11-20 - revised version 2
"""
News image entry for 2026-11-20.
Generates a PNG summarizing world news for November 20, 2026.
"""
import os
import struct
import zlib
from pathlib import Path


def write_png(path: Path, width: int, height: int, pixels: list) -> None:
    """Write a PNG file using only standard library."""
    # PNG signature
    png = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    png += struct.pack('>I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
    
    # IDAT chunk - compress pixel data
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)  # filter type 0 (none)
        for x in range(width):
            r, g, b = pixels[y * width + x]
            raw_data.extend([r, g, b])
    
    compressed = zlib.compress(raw_data, level=9)
    idat_crc = zlib.crc32(b'IDAT' + compressed) & 0xffffffff
    png += struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', idat_crc)
    
    # IEND chunk
    iend_crc = zlib.crc32(b'IEND') & 0xffffffff
    png += struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
    
    path.write_bytes(png)


def create_news_image() -> list:
    """Create pixel data for a 1024x1024 news summary image."""
    width, height = 1024, 1024
    pixels = [(25, 30, 40)] * (width * height)  # Dark navy background
    
    def set_pixel(x: int, y: int, color: tuple) -> None:
        if 0 <= x < width and 0 <= y < height:
            pixels[y * width + x] = color
    
    def draw_rect(x: int, y: int, w: int, h: int, color: tuple) -> None:
        for dy in range(h):
            for dx in range(w):
                set_pixel(x + dx, y + dy, color)
    
    def draw_text(x: int, y: int, text: str, color: tuple, scale: int = 1) -> None:
        # Simple 5x7 font rendering
        font = {
            'A': [0x1F, 0x11, 0x1F, 0x11, 0x11],
            'B': [0x1E, 0x11, 0x1E, 0x11, 0x1E],
            'C': [0x0E, 0x11, 0x10, 0x11, 0x0E],
            'D': [0x1C, 0x12, 0x12, 0x12, 0x1C],
            'E': [0x1F, 0x10, 0x1E, 0x10, 0x1F],
            'F': [0x1F, 0x10, 0x1E, 0x10, 0x10],
            'G': [0x0E, 0x11, 0x13, 0x11, 0x0F],
            'H': [0x11, 0x11, 0x1F, 0x11, 0x11],
            'I': [0x1F, 0x04, 0x04, 0x04, 0x1F],
            'J': [0x1F, 0x02, 0x02, 0x12, 0x0C],
            'K': [0x11, 0x12, 0x1C, 0x12, 0x11],
            'L': [0x10, 0x10, 0x10, 0x10, 0x1F],
            'M': [0x11, 0x1B, 0x15, 0x11, 0x11],
            'N': [0x11, 0x19, 0x15, 0x13, 0x11],
            'O': [0x0E, 0x11, 0x11, 0x11, 0x0E],
            'P': [0x1E, 0x11, 0x1E, 0x10, 0x10],
            'Q': [0x0E, 0x11, 0x11, 0x15, 0x0E],
            'R': [0x1E, 0x11, 0x1E, 0x12, 0x11],
            'S': [0x0F, 0x10, 0x0E, 0x01, 0x1E],
            'T': [0x1F, 0x04, 0x04, 0x04, 0x04],
            'U': [0x11, 0x11, 0x11, 0x11, 0x0E],
            'V': [0x11, 0x11, 0x11, 0x0A, 0x04],
            'W': [0x11, 0x11, 0x15, 0x15, 0x0A],
            'X': [0x11, 0x0A, 0x04, 0x0A, 0x11],
            'Y': [0x11, 0x0A, 0x04, 0x04, 0x04],
            'Z': [0x1F, 0x01, 0x02, 0x04, 0x1F],
            '0': [0x0E, 0x11, 0x13, 0x15, 0x0E],
            '1': [0x04, 0x0C, 0x04, 0x04, 0x0E],
            '2': [0x0E, 0x11, 0x02, 0x04, 0x1F],
            '3': [0x1E, 0x01, 0x0E, 0x01, 0x1E],
            '4': [0x12, 0x12, 0x1F, 0x02, 0x02],
            '5': [0x1F, 0x10, 0x1E, 0x01, 0x1E],
            '6': [0x0E, 0x10, 0x1E, 0x11, 0x0E],
            '7': [0x1F, 0x01, 0x02, 0x04, 0x04],
            '8': [0x0E, 0x11, 0x0E, 0x11, 0x0E],
            '9': [0x0E, 0x11, 0x0F, 0x01, 0x0E],
            ':': [0x00, 0x04, 0x00, 0x04, 0x00],
            '-': [0x00, 0x00, 0x1F, 0x00, 0x00],
            '.': [0x00, 0x00, 0x00, 0x00, 0x04],
            ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
            '/': [0x01, 0x02, 0x04, 0x08, 0x10],
        }
        
        for i, ch in enumerate(text.upper()):
            if ch not in font:
                continue
            char_x = x + i * 6 * scale
            char_y = y
            pattern = font[ch]
            for row_idx, row in enumerate(pattern):
                for col_idx in range(5):
                    if row & (0x10 >> col_idx):
                        for sy in range(scale):
                            for sx in range(scale):
                                set_pixel(char_x + col_idx * scale + sx, char_y + row_idx * scale + sy, color)
    
    # Draw header bar
    draw_rect(0, 0, width, 120, (15, 20, 30))
    draw_text(60, 20, "WORLD NEWS", (100, 200, 255), 3)
    draw_text(60, 70, "NOVEMBER 20, 2026", (200, 220, 180), 2)
    
    # Draw date divider line
    draw_rect(60, 110, 900, 3, (60, 100, 140))
    
    # News sections - 4 columns x 2 rows
    sections = [
        # Row 1
        {"x": 40, "y": 140, "w": 470, "h": 400, "title": "AMERICAS", "color": (80, 160, 255),
         "items": [
             "US: Fed holds rates at 4.5% amid cooling inflation",
             "Brazil: Amazon deforestation drops 40% YoY",
             "Canada: New Arctic sovereignty pact signed",
             "Mexico: Judicial reform sparks protests",
             "Chile: Lithium nationalization bill passes",
         ]},
        {"x": 534, "y": 140, "w": 470, "h": 400, "title": "EUROPE", "color": (60, 200, 120),
         "items": [
             "EU: AI Act enforcement begins across bloc",
             "UK: King Charles visits Poland for NATO summit",
             "Germany: Coalition agrees green steel subsidies",
             "France: Pension age debate reignites",
             "Ukraine: Grain corridor extended 12 months",
         ]},
        # Row 2
        {"x": 40, "y": 560, "w": 470, "h": 400, "title": "ASIA-PACIFIC", "color": (255, 180, 60),
         "items": [
             "China: Property stimulus revives Tier-1 markets",
             "India: Chandrayaan-4 enters lunar orbit",
             "Japan: BOJ ends negative rates era",
             "SKorea: Chip act funds 3nm domestic fab",
             "Australia: Great Barrier Reef shows recovery",
         ]},
        {"x": 534, "y": 560, "w": 470, "h": 400, "title": "MIDEAST & AFRICA", "color": (220, 100, 100),
         "items": [
             "Gaza: Ceasefire talks resume in Cairo",
             "Saudi: NEOM completes first transit line",
             "Nigeria: Dangote refinery hits full capacity",
             "Kenya: Digital ID rollout reaches 20M",
             "South Africa: Just Energy Transition funded",
         ]},
    ]
    
    for sec in sections:
        x, y, w, h = sec["x"], sec["y"], sec["w"], sec["h"]
        title_color = sec["color"]
        
        # Section background
        draw_rect(x, y, w, h, (35, 42, 55))
        # Title bar
        draw_rect(x, y, w, 50, (25, 30, 40))
        draw_text(x + 15, y + 10, sec["title"], title_color, 2)
        # Divider
        draw_rect(x + 10, y + 50, w - 20, 2, title_color)
        
        # News items
        for i, item in enumerate(sec["items"]):
            item_y = y + 65 + i * 60
            # Bullet
            draw_rect(x + 15, item_y + 15, 10, 10, title_color)
            # Text (truncated for space)
            draw_text(x + 35, item_y + 5, item[:55], (200, 210, 220), 1)
    
    # Bottom bar with key themes
    draw_rect(0, 980, width, 44, (15, 20, 30))
    draw_text(60, 988, "KEY THEMES:", (150, 180, 220), 1)
    themes = ["CLIMATE & ENERGY  |  AI GOVERNANCE  |  GEOPOLITICAL SHIFTS  |  TECH SOVEREIGNTY  |  HEALTH & SCIENCE"]
    draw_text(200, 988, themes[0], (100, 200, 180), 1)
    
    return pixels


def main():
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "entry.png"
    
    pixels = create_news_image()
    write_png(output_path, 1024, 1024, pixels)
    
    # Verify file size
    size = output_path.stat().st_size
    print(f"Generated {output_path} ({size} bytes, {size/1024:.1f} KB)")
    
    if size > 1048576:
        print("WARNING: File exceeds 1 MiB limit!")
    else:
        print("File size OK (<= 1 MiB)")


if __name__ == "__main__":
    main()
