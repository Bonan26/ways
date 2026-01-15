#!/usr/bin/env python3
"""
Alpha Wolves - Extract Wild Symbols
====================================
Remove backgrounds from W1 and W2 images.

W1: Gold wolf - remove yellow/gold gradient background
W2: Matrix wolf - remove dark green background
"""

from PIL import Image
import numpy as np
import os

BASE_PATH = "/Users/ariebonan/Desktop/alpha_wolf/Wolf_parts_final"
OUTPUT_PATH = "/Users/ariebonan/Desktop/alpha_wolf/assets/symbols"


def remove_background_by_color(image: Image.Image, target_colors: list, tolerance: int = 30) -> Image.Image:
    """
    Remove background by making target colors transparent.

    Args:
        image: PIL Image
        target_colors: List of RGB tuples to make transparent
        tolerance: Color matching tolerance (0-255)

    Returns:
        Image with transparent background
    """
    img_array = np.array(image.convert("RGBA"))

    # Create alpha mask (start with all opaque)
    alpha = img_array[:, :, 3].copy()

    for target_rgb in target_colors:
        # Calculate color distance
        r_diff = np.abs(img_array[:, :, 0].astype(int) - target_rgb[0])
        g_diff = np.abs(img_array[:, :, 1].astype(int) - target_rgb[1])
        b_diff = np.abs(img_array[:, :, 2].astype(int) - target_rgb[2])

        # Pixels within tolerance become transparent
        mask = (r_diff < tolerance) & (g_diff < tolerance) & (b_diff < tolerance)
        alpha[mask] = 0

    img_array[:, :, 3] = alpha
    return Image.fromarray(img_array)


def remove_background_flood(image: Image.Image, start_points: list, tolerance: int = 35) -> Image.Image:
    """
    Remove background using flood fill from corner points.
    More aggressive approach for gradient backgrounds.
    """
    img = image.convert("RGBA")
    img_array = np.array(img)
    height, width = img_array.shape[:2]

    # Get background colors from corners
    bg_colors = []
    for x, y in start_points:
        if 0 <= x < width and 0 <= y < height:
            bg_colors.append(img_array[y, x, :3])

    # Create mask based on similarity to corner colors
    alpha = np.ones((height, width), dtype=np.uint8) * 255

    for bg_color in bg_colors:
        r_diff = np.abs(img_array[:, :, 0].astype(int) - int(bg_color[0]))
        g_diff = np.abs(img_array[:, :, 1].astype(int) - int(bg_color[1]))
        b_diff = np.abs(img_array[:, :, 2].astype(int) - int(bg_color[2]))

        total_diff = r_diff + g_diff + b_diff
        mask = total_diff < tolerance * 3
        alpha[mask] = 0

    img_array[:, :, 3] = alpha
    return Image.fromarray(img_array)


def process_w1():
    """Process W1 - Gold wolf with gold/yellow background."""
    print("\n" + "="*50)
    print("Processing W1: Alpha Wild (Gold Wolf)")
    print("="*50)

    input_path = os.path.join(BASE_PATH, "Wolf_1.png")
    output_path = os.path.join(OUTPUT_PATH, "W1.png")

    img = Image.open(input_path)
    print(f"  Input size: {img.size}")

    # Sample the gold background colors from corners
    img_array = np.array(img.convert("RGB"))

    # Get colors from corners (background areas)
    corners = [
        (10, 10),                              # Top-left
        (img.width - 10, 10),                  # Top-right
        (10, img.height - 10),                 # Bottom-left
        (img.width - 10, img.height - 10),    # Bottom-right
        (img.width // 2, 10),                  # Top-center
    ]

    # Gold/yellow background colors to remove
    gold_colors = [
        (213, 180, 99),   # Main gold
        (225, 195, 110),  # Lighter gold
        (200, 165, 85),   # Darker gold
        (235, 210, 130),  # Bright gold
        (190, 155, 75),   # Deep gold
        (220, 188, 105),  # Mid gold
    ]

    # Remove background
    result = remove_background_flood(img, corners, tolerance=40)

    # Save
    result.save(output_path, "PNG")
    print(f"  [SAVED] {output_path}")

    return result


def process_w2():
    """Process W2 - Matrix wolf with dark green background."""
    print("\n" + "="*50)
    print("Processing W2: Beta Wild (Matrix Wolf)")
    print("="*50)

    input_path = os.path.join(BASE_PATH, "off_collection_giveaways_8.png")
    output_path = os.path.join(OUTPUT_PATH, "W2.png")

    img = Image.open(input_path)
    print(f"  Input size: {img.size}")

    # Dark green background colors to remove
    corners = [
        (10, 10),
        (img.width - 10, 10),
        (10, img.height - 10),
        (img.width - 10, img.height - 10),
    ]

    # Remove background
    result = remove_background_flood(img, corners, tolerance=25)

    # Save
    result.save(output_path, "PNG")
    print(f"  [SAVED] {output_path}")

    return result


def main():
    """Process both wild symbols."""
    print("\n" + "="*60)
    print("ALPHA WOLVES - Wild Symbol Extractor")
    print("="*60)

    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # Process W1
    try:
        process_w1()
    except Exception as e:
        print(f"  [ERROR] W1: {e}")

    # Process W2
    try:
        process_w2()
    except Exception as e:
        print(f"  [ERROR] W2: {e}")

    print("\n" + "="*60)
    print("EXTRACTION COMPLETE")
    print("="*60)

    # List all symbols
    print("\nAll symbols in output folder:")
    for f in sorted(os.listdir(OUTPUT_PATH)):
        if f.endswith('.png'):
            filepath = os.path.join(OUTPUT_PATH, f)
            size = os.path.getsize(filepath)
            print(f"  - {f} ({size:,} bytes)")


if __name__ == "__main__":
    main()
