import base64
import math
from pathlib import Path
from typing import Tuple, List, Dict, Any
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .config import GEMINI_API_KEY, NANO_BANANA_MODEL
from .schemas import CharacterSpec

POSE_ORDER: List[str] = [
    "idle",
    "bounce",
    "step_left",
    "step_right",
    "arms_up",
    "spin",
    "jump",
    "hold",
]


def _hex_to_rgb(hex_str: str, fallback: Tuple[int, int, int] = (249, 213, 229)) -> Tuple[int, int, int]:
    s = (hex_str or "").strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) == 6:
        try:
            return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
        except ValueError:
            pass
    return fallback


def remove_chromakey_green(raw_img: Image.Image) -> Image.Image:
    """Removes #00FF00 chroma-key background and returns a clean RGBA image."""
    rgba = raw_img.convert("RGBA")
    arr = np.array(rgba, dtype=np.int16)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    # Detect pure/near-pure chroma green (#00FF00)
    green_mask = (g > 185) & (r < 95) & (b < 95) & ((g - np.maximum(r, b)) > 100)
    # Soft edge anti-aliasing feathering
    edge_mask = (~green_mask) & (g > 140) & ((g - np.maximum(r, b)) > 65)

    out = arr.copy()
    out[green_mask, 3] = 0
    out[edge_mask, 1] = np.minimum(out[edge_mask, 1], np.maximum(out[edge_mask, 0], out[edge_mask, 2]) + 15)
    out[edge_mask, 3] = (out[edge_mask, 3] * 0.55).astype(np.int16)

    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), mode="RGBA")


def _draw_character_pose(
    draw: ImageDraw.ImageDraw,
    frame_idx: int,
    pose: str,
    frame_size: int,
    char: CharacterSpec,
) -> None:
    x0 = frame_idx * frame_size
    cx = x0 + frame_size // 2
    cy = frame_size // 2 + 18

    pal = char.palette if char.palette and len(char.palette) >= 3 else ["#F9D5E5", "#9B5DE5", "#FEE440", "#00BBF9"]
    c_primary = _hex_to_rgb(pal[0], (249, 213, 229))
    c_secondary = _hex_to_rgb(pal[1], (155, 93, 229))
    c_accent = _hex_to_rgb(pal[2], (254, 228, 64))
    c_glow = _hex_to_rgb(pal[3] if len(pal) > 3 else pal[0], (0, 245, 212))
    c_outline = (24, 16, 40)

    is_cyber = "cyber" in char.archetype.lower() or "neon" in char.name.lower() or "kairo" in char.name.lower()

    # Pose kinematic parameters
    dy = 0
    dx = 0
    squash_x = 1.0
    squash_y = 1.0
    arm_l_angle = -35
    arm_r_angle = 35
    leg_l_dx, leg_l_dy = -16, 56
    leg_r_dx, leg_r_dy = 16, 56
    wing_spread = 1.0
    spin_ribbon = False

    if pose == "idle":
        dy = 0
        arm_l_angle, arm_r_angle = -30, 30
    elif pose == "bounce":
        dy = 12
        squash_x, squash_y = 1.12, 0.88
        arm_l_angle, arm_r_angle = -55, 55
        leg_l_dx, leg_r_dx = -22, 22
    elif pose == "step_left":
        dx = -16
        dy = -4
        arm_l_angle, arm_r_angle = -75, 20
        leg_l_dx, leg_l_dy = -34, 48
        leg_r_dx, leg_r_dy = 12, 58
    elif pose == "step_right":
        dx = 16
        dy = -4
        arm_l_angle, arm_r_angle = -20, 75
        leg_l_dx, leg_l_dy = -12, 58
        leg_r_dx, leg_r_dy = 34, 48
    elif pose == "arms_up":
        dy = -8
        arm_l_angle, arm_r_angle = -135, 135
        wing_spread = 1.28
    elif pose == "spin":
        dy = -12
        squash_x = 0.82
        arm_l_angle, arm_r_angle = -95, 110
        leg_l_dx, leg_l_dy = -6, 52
        leg_r_dx, leg_r_dy = 18, 38
        wing_spread = 1.15
        spin_ribbon = True
    elif pose == "jump":
        dy = -30
        squash_x, squash_y = 0.92, 1.12
        arm_l_angle, arm_r_angle = -145, 145
        leg_l_dx, leg_l_dy = -26, 40
        leg_r_dx, leg_r_dy = 28, 36
        wing_spread = 1.40
    elif pose == "hold":
        dy = 4
        arm_l_angle, arm_r_angle = -60, 120
        leg_l_dx, leg_l_dy = -10, 56
        leg_r_dx, leg_r_dy = 22, 50
        wing_spread = 1.18

    px = cx + dx
    py = cy + dy

    # 1. Back Halo / Wings / Cyber Thruster Pack
    if is_cyber:
        # Holographic hexagonal thruster wings
        w_span = int(52 * wing_spread)
        for side in (-1, 1):
            pts = [
                (px, py - 10),
                (px + side * w_span, py - 42),
                (px + side * (w_span + 14), py - 12),
                (px + side * (w_span - 8), py + 18),
            ]
            draw.polygon(pts, fill=c_secondary, outline=c_glow)
            inner_pts = [
                (px + side * 10, py - 8),
                (px + side * (w_span - 8), py - 30),
                (px + side * w_span, py - 10),
            ]
            draw.polygon(inner_pts, fill=c_glow)
    else:
        # Translucent butterfly / prism fairy wings
        w_span = int(56 * wing_spread)
        for side in (-1, 1):
            upper_wing = [
                (px, py - 12),
                (px + side * (w_span // 2), py - 54),
                (px + side * w_span, py - 28),
                (px + side * (w_span - 10), py + 4),
            ]
            lower_wing = [
                (px, py - 2),
                (px + side * (w_span - 8), py + 6),
                (px + side * (w_span - 16), py + 34),
                (px + side * 14, py + 22),
            ]
            draw.polygon(upper_wing, fill=c_glow, outline=c_outline)
            draw.polygon(lower_wing, fill=c_primary, outline=c_outline)

    # 2. Legs & Boots
    draw.line(
        [(px - 10, py + 18), (px + leg_l_dx, py + leg_l_dy)],
        fill=c_outline,
        width=9,
    )
    draw.line(
        [(px - 10, py + 18), (px + leg_l_dx, py + leg_l_dy)],
        fill=c_primary,
        width=5,
    )
    draw.line(
        [(px + 10, py + 18), (px + leg_r_dx, py + leg_r_dy)],
        fill=c_outline,
        width=9,
    )
    draw.line(
        [(px + 10, py + 18), (px + leg_r_dx, py + leg_r_dy)],
        fill=c_primary,
        width=5,
    )
    # Shoes / Thruster boots
    for lx, ly in ((px + leg_l_dx, py + leg_l_dy), (px + leg_r_dx, py + leg_r_dy)):
        draw.ellipse([lx - 9, ly - 6, lx + 9, ly + 7], fill=c_accent, outline=c_outline)

    # 3. Torso / Dress / Cyber Armor
    bw = int(26 * squash_x)
    bh = int(32 * squash_y)
    if is_cyber:
        torso_pts = [
            (px - bw, py - 18),
            (px + bw, py - 18),
            (px + int(bw * 0.75), py + 22),
            (px - int(bw * 0.75), py + 22),
        ]
        draw.polygon(torso_pts, fill=c_secondary, outline=c_outline)
        # Core reactor emblem
        draw.polygon(
            [(px, py - 10), (px + 10, py + 2), (px, py + 14), (px - 10, py + 2)],
            fill=c_accent,
            outline=c_outline,
        )
    else:
        # Ballet bodice + flared tutu skirt
        skirt_pts = [
            (px - 16, py - 14),
            (px + 16, py - 14),
            (px + bw + 14, py + 24),
            (px - bw - 14, py + 24),
        ]
        draw.polygon(skirt_pts, fill=c_secondary, outline=c_outline)
        tutu_pts = [
            (px - bw - 18, py + 14),
            (px, py + 4),
            (px + bw + 18, py + 14),
            (px + bw + 8, py + 26),
            (px, py + 20),
            (px - bw - 8, py + 26),
        ]
        draw.polygon(tutu_pts, fill=c_primary, outline=c_outline)
        draw.ellipse([px - 7, py - 8, px + 7, py + 6], fill=c_accent, outline=c_outline)

    # 4. Arms & Wand / Energy Blade
    for side, ang in ((-1, arm_l_angle), (1, arm_r_angle)):
        rad = math.radians(ang)
        sx = px + side * 18
        sy = py - 12
        ex = int(sx + math.sin(rad) * 34)
        ey = int(sy + math.cos(rad) * 34)
        draw.line([(sx, sy), (ex, ey)], fill=c_outline, width=8)
        draw.line([(sx, sy), (ex, ey)], fill=c_primary, width=4)
        draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=c_accent, outline=c_outline)

        # Right hand holds signature wand or plasma baton
        if side == 1:
            wx = int(ex + math.sin(rad - 0.3) * 26)
            wy = int(ey + math.cos(rad - 0.3) * 26)
            draw.line([(ex, ey), (wx, wy)], fill=c_accent, width=4)
            draw.ellipse([wx - 8, wy - 8, wx + 8, wy + 8], fill=c_glow, outline=c_outline)
            draw.ellipse([wx - 4, wy - 4, wx + 4, wy + 4], fill=(255, 255, 255))

    # 5. Head, Face, Visor / Crown
    hrx = int(24 * squash_x)
    hry = int(23 * squash_y)
    hy = py - 38
    draw.ellipse(
        [px - hrx, hy - hry, px + hrx, hy + hry],
        fill=(255, 238, 230) if not is_cyber else (225, 235, 248),
        outline=c_outline,
        width=3,
    )

    if is_cyber:
        # Glowing cyberpunk visor + headset fins
        draw.rounded_rectangle(
            [px - 18, hy - 6, px + 18, hy + 6],
            radius=4,
            fill=c_glow,
            outline=c_outline,
            width=2,
        )
        draw.polygon(
            [(px - 18, hy - 14), (px, hy - 34), (px + 18, hy - 14)],
            fill=c_secondary,
            outline=c_outline,
        )
    else:
        # Expressive eyes + crystalline tiara crown
        draw.ellipse([px - 11, hy - 4, px - 5, hy + 3], fill=c_outline)
        draw.ellipse([px + 5, hy - 4, px + 11, hy + 3], fill=c_outline)
        draw.ellipse([px - 14, hy + 3, px - 7, hy + 8], fill=(255, 160, 190))
        draw.ellipse([px + 7, hy + 3, px + 14, hy + 8], fill=(255, 160, 190))
        crown_pts = [
            (px - 16, hy - hry + 4),
            (px - 12, hy - hry - 14),
            (px - 4, hy - hry - 4),
            (px, hy - hry - 20),
            (px + 4, hy - hry - 4),
            (px + 12, hy - hry - 14),
            (px + 16, hy - hry + 4),
        ]
        draw.polygon(crown_pts, fill=c_accent, outline=c_outline)

    # 6. Spin / Jump kinetic ribbons
    if spin_ribbon or pose == "jump":
        draw.arc(
            [px - 52, py - 50, px + 52, py + 45],
            start=20,
            end=310,
            fill=c_accent,
            width=4,
        )


def generate_character_sheet(
    char: CharacterSpec,
    out_dir: Path,
    use_nano_banana: bool = True,
) -> Dict[str, Any]:
    """
    Generates an 8-pose sprite sheet on #00FF00 chroma-key (`sprites_chromakey_raw.png`),
    applies chroma-key removal to produce RGBA (`sprites.png`), and optionally calls
    `gemini-nano-banana-2.1` to generate a companion AI character portrait.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    frame_size = 256
    sheet_w = frame_size * len(POSE_ORDER)
    sheet_h = frame_size

    # 1. Create raw #00FF00 chroma-key sheet
    raw_sheet = Image.new("RGB", (sheet_w, sheet_h), (0, 255, 0))
    draw = ImageDraw.Draw(raw_sheet)

    for idx, pose in enumerate(POSE_ORDER):
        _draw_character_pose(draw, idx, pose, frame_size, char)

    raw_path = out_dir / "sprites_chromakey_raw.png"
    raw_sheet.save(str(raw_path), format="PNG")

    # 2. Apply #00FF00 chroma-key removal -> RGBA sprites.png
    rgba_sheet = remove_chromakey_green(raw_sheet)
    sprites_path = out_dir / "sprites.png"
    rgba_sheet.save(str(sprites_path), format="PNG")

    # 3. Call gemini-nano-banana-2.1 for AI character concept art if available
    nano_banana_used = False
    portrait_path = out_dir / "nano_banana_concept.png"
    if use_nano_banana and GEMINI_API_KEY:
        try:
            from google import genai

            client = genai.Client(api_key=GEMINI_API_KEY)
            prompt = (
                f"Create a stylized 2D animation character turnaround icon of {char.name}: "
                f"{char.concept}. Style: {char.style}. Color palette: {', '.join(char.palette)}. "
                f"Isolated on a flat solid #00FF00 green screen background, clean vector outlines, no text."
            )
            interaction = client.interactions.create(
                model=NANO_BANANA_MODEL,
                input=prompt,
                timeout=35.0,
            )
            if interaction.output_image and interaction.output_image.data:
                img_bytes = base64.b64decode(interaction.output_image.data)
                portrait_path.write_bytes(img_bytes)
                nano_banana_used = True
        except Exception as e:
            print(f"[Character] Nano Banana 2.1 note (using procedural chroma-key sheet): {e}")

    return {
        "sprites_path": str(sprites_path),
        "raw_chromakey_path": str(raw_path),
        "poses": POSE_ORDER,
        "frame_size": frame_size,
        "sheet_width": sheet_w,
        "sheet_height": sheet_h,
        "chromakey_color": "#00FF00",
        "nano_banana_used": nano_banana_used,
    }
