#!/usr/bin/env python3.12
"""
Alpha Wolves - Asset Generator using Imagen 4
"""

import os
from google import genai
from google.genai import types
from PIL import Image
import numpy as np

# Load API key
API_KEY = "AIzaSyDojt2u3_tHYtQx0TqfQOCsvyQTxJ6ruEI"

# Initialize client
client = genai.Client(api_key=API_KEY)


def remove_background(image_path: str, tolerance: int = 25):
    """Remove background by detecting corner colors and making them transparent"""
    img = Image.open(image_path).convert("RGBA")
    data = np.array(img)
    height, width = data.shape[:2]

    # Sample background color from corners
    corners = [
        (10, 10),
        (width - 10, 10),
        (10, height - 10),
        (width - 10, height - 10),
    ]

    # Get average background color from corners
    bg_colors = [data[y, x, :3] for x, y in corners]
    bg_color = np.mean(bg_colors, axis=0).astype(int)
    print(f"  Detected background color: RGB{tuple(bg_color)}")

    # Calculate distance from background color
    r_diff = np.abs(data[:, :, 0].astype(int) - bg_color[0])
    g_diff = np.abs(data[:, :, 1].astype(int) - bg_color[1])
    b_diff = np.abs(data[:, :, 2].astype(int) - bg_color[2])

    # Total color distance
    total_diff = r_diff + g_diff + b_diff
    mask = total_diff < tolerance * 3

    print(f"  Removing {mask.sum():,} pixels ({mask.sum()/mask.size*100:.1f}%)")

    # Make matching pixels transparent
    data[mask] = [0, 0, 0, 0]

    # Save result
    result = Image.fromarray(data)
    result.save(image_path, "PNG")
    print(f"  Background removed: {image_path}")

# Style prompt base - Alpha Wolves NFT Style
STYLE_PROMPT = """
Style: Modern NFT cartoon art, clean and stylish.

Visual style:
- Bold black outlines, consistent thickness
- Vibrant flat colors with subtle cel-shading
- High contrast, punchy palette
- Detailed but clean - NOT minimalist, NOT grotesque
- Premium collectible look

Background: Solid pure magenta (#FF00FF). MUST be uniform solid color with NO gradients, NO shading, NO texture.
"""

def generate_symbol(symbol_name: str, description: str, output_path: str):
    """Generate a symbol asset using Gemini Image Generation"""

    full_prompt = f"""
Generate an image with these specifications:

{STYLE_PROMPT}

Subject: {description}

The image should be a slot machine symbol, perfectly centered, with the subject taking up most of the frame.
Square format, high detail, clean edges for easy extraction.
The green background must be solid and uniform.
"""

    print(f"Generating {symbol_name}...")
    print(f"Prompt: {description}")

    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=full_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                output_mime_type="image/png",
            )
        )

        # Save the image
        if response.generated_images:
            image_data = response.generated_images[0].image.image_bytes
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"Saved to: {output_path}")
            return True

        print("No image in response")
        return False

    except Exception as e:
        print(f"Error: {e}")
        return False


# All symbols to generate
SYMBOLS = {
    # Premium - Wolf characters (NFT style - HEAD + SHOULDERS bust portrait, no frame)
    "boss_wolf": "Wolf head and shoulders portrait, 3/4 profile view, dark fur, wearing pinstripe suit collar visible, gold chain with dollar pendant, dark sunglasses, long snout with sharp fangs in confident smirk, tan muzzle, mob boss energy, NO frame NO border",
    "hustler": "Wolf head and shoulders portrait, 3/4 profile view, dark fur, wearing hoodie with hood down, snapback cap backwards, gold chain with diamond pendant, fangs showing in grin, tan muzzle, intense eyes, hip-hop attitude, NO frame NO border",
    "tech_bro": "Wolf head and shoulders portrait, 3/4 profile view, grey fur, round glasses with green reflection, AirPods in ear, smug expression with fangs, tan muzzle, bitcoin pendant on chain, tech bro energy, NO frame NO border",
    "diamond_hands": "Wolf head and shoulders portrait, 3/4 profile view, black fur with sparkles, multiple gold chains with diamonds, diamond grillz on fangs, intense greedy eyes, bling aesthetic, NO frame NO border",

    # Low - Wolf items (detailed, stylized with character)
    "bone": "Detailed cartoon bone with bite marks and cracks, slightly worn and battle-scarred, bold black outlines, off-white color with subtle shading, wolf tooth marks visible, not too clean - has character",
    "meat": "Juicy T-bone steak with detailed marbling, rich red meat with white fat, slight char marks, bold outlines, appetizing and detailed, premium cut look, not cartoonishly simple",
    "claw": "Single wolf paw from front view, four fingers with sharp curved black claws, grey fur, powerful and menacing, detailed anatomy, slot symbol style, ONE paw only",
    "fang": "Large wolf fang tooth, ivory colored with detailed root, slight blood stains at base, sharp and menacing, crack details, powerful predator trophy, detailed not simple",

    # Special
    "alpha_wolf": "NFT-style alpha wolf in 3/4 profile, pure black fur with golden glow effects, glowing golden eyes with intensity, crown with digital glitch effect, long snout with massive fangs in dominant snarl, gold chain, leader of the pack energy, most detailed and impressive",
    "howling_wild": "NFT-style wolf howling at moon, 3/4 profile head tilted up, black fur with neon purple/blue glow aura, eyes closed in howl, visible fangs, sound wave effects around, mystical wild energy, detailed fur texture",
    "moon_scatter": "Large detailed blood moon with wolf silhouette howling inside, purple and crimson tones, mystical scatter symbol, cracks and craters on moon surface, eerie glow effect, detailed not simple",
    "territory": "Tattered flag with wolf paw print emblem, graffiti spray paint style, urban street art aesthetic, bold colors (red/black/gold), battle-worn edges, conquest symbol, detailed texture",
}


def generate_one(symbol_name: str):
    """Generate a single symbol by name"""
    symbol_name = symbol_name.lower()

    if symbol_name not in SYMBOLS:
        print(f"Unknown symbol: {symbol_name}")
        print(f"Available: {', '.join(SYMBOLS.keys())}")
        return False

    base_path = "web-sdk/static/assets/sprites/symbols_static"
    output_path = f"{base_path}/{symbol_name}.png"

    success = generate_symbol(
        symbol_name=symbol_name.upper(),
        description=SYMBOLS[symbol_name],
        output_path=output_path
    )

    if success:
        remove_background(output_path)
        print(f"✓ {symbol_name} complete\n")
        return True
    return False


def generate_premium_wolves():
    """Generate all 4 premium wolves on one image, then split"""

    prompt = """
Create a 2x2 grid of 4 wolf character portraits, NFT cartoon style.
Each wolf is a head and shoulders bust portrait, 3/4 profile view, bold black outlines, vibrant colors.

Top-left: BOSS WOLF - Dark fur, pinstripe suit collar, gold chain with dollar pendant, dark sunglasses, fangs in confident smirk, tan muzzle, mob boss energy

Top-right: HUSTLER - Dark fur, hoodie, snapback cap backwards, gold chain with diamond pendant, fangs showing in grin, tan muzzle, intense eyes, hip-hop attitude

Bottom-left: TECH BRO - Grey fur, round glasses with green reflection, AirPods, smug expression with fangs, tan muzzle, bitcoin pendant on chain

Bottom-right: DIAMOND HANDS - Black fur with sparkles, multiple gold chains with diamonds, diamond grillz on fangs, intense greedy eyes, bling aesthetic

All 4 wolves must have the SAME art style, same level of detail, same proportions.
Each quadrant clearly separated.
Background: Solid pure magenta (#FF00FF) for ALL 4 quadrants. NO gradients.
"""

    print("Generating 4 premium wolves in one image...")

    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                output_mime_type="image/png",
            )
        )

        if response.generated_images:
            # Save full image
            image_data = response.generated_images[0].image.image_bytes
            full_path = "web-sdk/static/assets/sprites/symbols_static/premium_wolves_full.png"
            with open(full_path, "wb") as f:
                f.write(image_data)
            print(f"Saved full image: {full_path}")

            # Split into 4
            split_premium_wolves(full_path)
            return True

        print("No image in response")
        return False

    except Exception as e:
        print(f"Error: {e}")
        return False


def split_premium_wolves(full_path: str):
    """Split a 2x2 grid into 4 separate images"""
    img = Image.open(full_path)
    width, height = img.size

    half_w = width // 2
    half_h = height // 2

    # Crop coordinates: (left, top, right, bottom)
    wolves = {
        "boss_wolf": (0, 0, half_w, half_h),           # Top-left
        "hustler": (half_w, 0, width, half_h),         # Top-right
        "tech_bro": (0, half_h, half_w, height),       # Bottom-left
        "diamond_hands": (half_w, half_h, width, height),  # Bottom-right
    }

    base_path = "web-sdk/static/assets/sprites/symbols_static"

    for name, coords in wolves.items():
        cropped = img.crop(coords)
        output_path = f"{base_path}/{name}.png"
        cropped.save(output_path, "PNG")
        print(f"  Cropped {name}")
        remove_background(output_path)
        print(f"  ✓ {name} complete")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python generate_asset.py <symbol_name>")
        print("       python generate_asset.py premium  (generates all 4 premium wolves)")
        print(f"\nAvailable symbols:")
        print("  Premium: boss_wolf, hustler, tech_bro, diamond_hands")
        print("  Low:     bone, meat, claw, fang")
        print("  Special: alpha_wolf, howling_wild, moon_scatter, territory")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "premium":
        generate_premium_wolves()
    else:
        generate_one(arg)
