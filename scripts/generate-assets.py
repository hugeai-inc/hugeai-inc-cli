#!/usr/bin/env python3
"""Generate the README banner PNG and animated terminal demo GIF."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

SYNE = "/usr/share/fonts/truetype/sand-box/google/Syne/Syne-VariableFont_wght.ttf"
INTER = "/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf"
PLEX = "/usr/share/fonts/truetype/sand-box/google/IBM Plex Mono/IBMPlexMono-Regular.ttf"
PLEX_MED = "/usr/share/fonts/truetype/sand-box/google/IBM Plex Mono/IBMPlexMono-Medium.ttf"
PLEX_BOLD = "/usr/share/fonts/truetype/sand-box/google/IBM Plex Mono/IBMPlexMono-Bold.ttf"
SPACE = "/usr/share/fonts/truetype/sand-box/google/Space Grotesk/SpaceGrotesk-VariableFont_wght.ttf"


def font(path: str, size: int, weight: int | None = None, opsz: float | None = None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size)
    if weight is None:
        return f
    try:
        axes = f.get_variation_axes()
        values = []
        for ax in axes:
            name = ax["name"].decode() if isinstance(ax["name"], bytes) else str(ax["name"])
            low, high, default = ax["minimum"], ax["maximum"], ax["default"]
            if "Weight" in name:
                values.append(max(low, min(high, float(weight))))
            elif "Optical" in name:
                v = float(opsz if opsz is not None else min(high, max(low, size)))
                values.append(v)
            else:
                values.append(float(default))
        f.set_variation_by_axes(values)
    except Exception:
        pass
    return f


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def bg_gradient(w: int, h: int) -> Image.Image:
    img = Image.new("RGB", (w, h), "#07080C")
    px = img.load()
    for y in range(h):
        ty = y / (h - 1)
        for x in range(w):
            tx = x / (w - 1)
            # Deep ink, slightly lighter toward the upper-right.
            r = lerp(7, 18, 0.25 * tx + 0.15 * (1 - ty))
            g = lerp(8, 22, 0.20 * tx + 0.18 * (1 - ty))
            b = lerp(12, 32, 0.28 * tx + 0.22 * (1 - ty))
            # Soft gold bloom in the lower-left, teal bloom upper-right.
            gold = math.exp(-((tx - 0.12) ** 2) / 0.18 - ((ty - 0.78) ** 2) / 0.22)
            teal = math.exp(-((tx - 0.88) ** 2) / 0.16 - ((ty - 0.22) ** 2) / 0.20)
            r = min(255, int(r + 42 * gold + 8 * teal))
            g = min(255, int(g + 28 * gold + 36 * teal))
            b = min(255, int(b + 10 * gold + 44 * teal))
            px[x, y] = (r, g, b)
    return img


def draw_banner() -> Image.Image:
    # Render at 2x and downscale for crisp type.
    W, H = 2560, 720
    img = bg_gradient(W, H)
    # Hairline frame
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Left gold accent bar
    d.rectangle([0, 0, 12, H], fill=(201, 164, 108, 255))

    # Thin inner rule
    d.rectangle([72, 96, 76, H - 96], fill=(201, 164, 108, 80))

    # Three director dots (2-of-3 majority visual): two lit, one dim.
    cy = 360
    xs = [198, 198, 198]
    ys = [cy - 86, cy, cy + 86]
    colors = [(201, 164, 108, 255), (201, 164, 108, 255), (201, 164, 108, 70)]
    for i, (x, y, c) in enumerate(zip(xs, ys, colors)):
        r = 14
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)
        if i < 2:
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(7, 8, 12, 255))
    # Connecting line
    d.line([(198, cy - 86 + 16), (198, cy + 86 - 16)], fill=(201, 164, 108, 70), width=3)

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)

    kicker = font(INTER, 28, weight=560, opsz=18)
    title = font(SYNE, 196, weight=800)
    subtitle = font(INTER, 36, weight=400, opsz=18)
    meta = font(INTER, 26, weight=450, opsz=14)

    gold = (212, 180, 122, 255)
    white = (245, 243, 238, 255)
    mute = (168, 174, 186, 255)

    d.text((320, 118), "HUGE  AI  INC", font=kicker, fill=gold)
    # Track the kicker slightly by drawing it with spacing manually if needed.
    d.text((312, 168), "CLI", font=title, fill=white)
    d.text(
        (320, 430),
        "Board resolutions  ·  meetings  ·  director identity keys",
        font=subtitle,
        fill=mute,
    )
    d.text(
        (320, 512),
        "Ed25519 signatures   ·   2-of-3 majority   ·   brew  ·  apt  ·  go install",
        font=meta,
        fill=(201, 164, 108, 200),
    )

    # Right-side monogram / wordmark block
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    p = ImageDraw.Draw(panel)
    # Thin rounded card
    x0, y0, x1, y1 = 1860, 170, 2448, 550
    p.rounded_rectangle([x0, y0, x1, y1], radius=28, outline=(201, 164, 108, 90), width=3)
    mono = font(SYNE, 72, weight=800)
    small = font(INTER, 22, weight=500, opsz=14)
    p.text((x0 + 48, y0 + 56), "2 of 3", font=mono, fill=white)
    p.text((x0 + 48, y0 + 160), "SIGNED  ATTESTATIONS", font=small, fill=gold)
    p.text((x0 + 48, y0 + 210), "Steven Zeiler", font=small, fill=mute)
    p.text((x0 + 48, y0 + 252), "Derrick Horton", font=small, fill=mute)
    p.text((x0 + 48, y0 + 294), "Huge Hugh, CEO", font=small, fill=mute)
    img = Image.alpha_composite(img, panel)

    rgb = img.convert("RGB")
    out = rgb.resize((1280, 360), Image.Resampling.LANCZOS)
    return out


# ---------- terminal demo GIF ----------

TERM_W, TERM_H = 960, 540
PAD_X = 28
PAD_TOP = 52
LINE_H = 22
COLS = {
    "bg": (12, 14, 20),
    "titlebar": (22, 24, 32),
    "border": (42, 46, 58),
    "text": (230, 232, 236),
    "dim": (120, 126, 140),
    "green": (110, 214, 160),
    "gold": (220, 186, 120),
    "red": (232, 96, 96),
    "amber": (232, 176, 80),
    "ok": (96, 201, 140),
    "cyan": (120, 196, 214),
    "prompt": (110, 214, 160),
}


def term_base() -> Image.Image:
    img = Image.new("RGB", (TERM_W, TERM_H), TERM_COLS := COLS["bg"])
    d = ImageDraw.Draw(img)
    # Window border
    d.rounded_rectangle([0, 0, TERM_W - 1, TERM_H - 1], radius=16, outline=COLS["border"], width=2)
    d.rectangle([1, 1, TERM_W - 2, 40], fill=COLS["titlebar"])
    # traffic lights
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        x = 22 + i * 20
        d.ellipse([x, 14, x + 12, 26], fill=color)
    title_f = font(INTER, 14, weight=500, opsz=14)
    title = "hugeai-inc-cli  —  zsh"
    bbox = d.textbbox((0, 0), title, font=title_f)
    tw = bbox[2] - bbox[0]
    d.text(((TERM_W - tw) / 2, 12), title, font=title_f, fill=COLS["dim"])
    return img


def text_width(draw: ImageDraw.ImageDraw, text: str, fnt) -> int:
    b = draw.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0]


def render_terminal(lines: list[tuple[str, str]], cursor: bool = False, cursor_col: int | None = None) -> Image.Image:
    """lines: list of (role, text) where role is prompt|cmd|out|dim|gold|cyan|ok|red|blank."""
    img = term_base()
    d = ImageDraw.Draw(img)
    regular = ImageFont.truetype(PLEX, 16)
    medium = ImageFont.truetype(PLEX_MED, 16)
    x = PAD_X
    y = PAD_TOP
    for role, text in lines:
        if role == "blank":
            y += LINE_H
            continue
        if role == "prompt_line":
            # text is the command after the prompt
            d.text((x, y), "$ ", font=medium, fill=COLS["prompt"])
            pw = text_width(d, "$ ", medium)
            d.text((x + pw, y), text, font=regular, fill=COLS["text"])
            if cursor and cursor_col is not None:
                # cursor after typed portion
                typed = text[:cursor_col]
                cw = text_width(d, typed, regular)
                d.rectangle([x + pw + cw + 1, y + 2, x + pw + cw + 9, y + 16], fill=COLS["gold"])
        elif role == "prompt_partial":
            d.text((x, y), "$ ", font=medium, fill=COLS["prompt"])
            pw = text_width(d, "$ ", medium)
            d.text((x + pw, y), text, font=regular, fill=COLS["text"])
            cw = text_width(d, text, regular)
            if cursor:
                d.rectangle([x + pw + cw + 1, y + 2, x + pw + cw + 9, y + 16], fill=COLS["gold"])
        else:
            color = {
                "out": COLS["text"],
                "dim": COLS["dim"],
                "gold": COLS["gold"],
                "cyan": COLS["cyan"],
                "ok": COLS["ok"],
                "red": COLS["red"],
                "amber": COLS["amber"],
            }.get(role, COLS["text"])
            d.text((x, y), text, font=regular, fill=color)
        y += LINE_H
    return img


SCENES: list[dict] = [
    {
        "cmd": "hugeai-inc-cli resolution draft --title \"Appoint Huge Hugh as CEO\"",
        "output": [
            ("gold", "not yet implemented"),
            ("blank", ""),
            ("dim", "# Outline  —  resolution draft"),
            ("dim", "#   Create a new board resolution as a draft:"),
            ("dim", "#   sequential number, type (general | ceo_removal | key_recovery),"),
            ("dim", "#   canonical markdown body, threshold default 2 of 3."),
            ("cyan", "  title       Appoint Huge Hugh as CEO"),
            ("cyan", "  type        general"),
            ("cyan", "  status      draft"),
            ("cyan", "  threshold   2 of 3"),
        ],
    },
    {
        "cmd": "hugeai-inc-cli resolution sign --id HR-2026-001 --vote approve",
        "output": [
            ("gold", "not yet implemented"),
            ("blank", ""),
            ("dim", "# Outline  —  resolution sign"),
            ("dim", "#   Sign a canonical payload with the director's Ed25519 key and"),
            ("dim", "#   submit the vote through the verification endpoint."),
            ("cyan", "  resolution  HR-2026-001"),
            ("cyan", "  vote        approve"),
            ("dim", "#   votes: approve | reject | abstain | recused"),
        ],
    },
    {
        "cmd": "hugeai-inc-cli resolution tally --id HR-2026-001",
        "output": [
            ("gold", "not yet implemented"),
            ("blank", ""),
            ("dim", "# Outline  —  resolution tally"),
            ("dim", "#   Count verified attestations against the 2-of-3 majority rule."),
            ("cyan", "  approve     0 / 3"),
            ("cyan", "  reject      0 / 3"),
            ("cyan", "  threshold   2 of 3"),
            ("amber", "  status      open_for_signature"),
        ],
    },
    {
        "cmd": "hugeai-inc-cli resolution verify --id HR-2026-001",
        "output": [
            ("gold", "not yet implemented"),
            ("blank", ""),
            ("dim", "# Outline  —  resolution verify"),
            ("dim", "#   Check each attestation against the signer's active public key"),
            ("dim", "#   and the locked SHA-256 content hash of the canonical text."),
            ("cyan", "  content_hash   (pending)"),
            ("cyan", "  signatures     0 verified"),
        ],
    },
    {
        "cmd": "hugeai-inc-cli keys status",
        "output": [
            ("gold", "not yet implemented"),
            ("blank", ""),
            ("dim", "# Outline  —  keys status"),
            ("dim", "#   Per-director Ed25519 identity keys. Private keys never leave"),
            ("dim", "#   the director's device. Emergency revoke is a 2-of-3 recovery."),
            ("cyan", "  Steven Zeiler      no active key"),
            ("cyan", "  Derrick Horton     no active key"),
            ("cyan", "  Huge Hugh          no active key"),
        ],
    },
]


def build_gif_frames() -> list[tuple[Image.Image, int]]:
    frames: list[tuple[Image.Image, int]] = []
    # duration in ms
    type_ms = 28
    hold_cursor = 420
    hold_output = 1600
    end_hold = 900

    for scene in SCENES:
        cmd = scene["cmd"]
        # empty prompt + blinking cursor
        frames.append((render_terminal([("prompt_partial", "")], cursor=True), 280))
        # type the command
        typed = ""
        for i, ch in enumerate(cmd):
            typed += ch
            # slightly faster on spaces after a while
            dur = type_ms if ch != " " else 18
            if i % 2 == 1:
                # skip every other char visually by combining durations? keep all for smoothness but cheap
                pass
            frames.append((render_terminal([("prompt_partial", typed)], cursor=True), dur))
        frames.append((render_terminal([("prompt_partial", cmd)], cursor=True), hold_cursor))
        # show output
        lines = [("prompt_line", cmd), ("blank", "")] + scene["output"]
        frames.append((render_terminal(lines, cursor=False), hold_output))
        # brief blank before next
        frames.append((render_terminal([("prompt_partial", "")], cursor=True), 200))

    # final hold on last output
    last = SCENES[-1]
    lines = [("prompt_line", last["cmd"]), ("blank", "")] + last["output"] + [("blank", ""), ("prompt_partial", "")]
    frames.append((render_terminal(lines, cursor=True), end_hold))
    return frames


def quantize(img: Image.Image, palette_img: Image.Image) -> Image.Image:
    return img.convert("RGB").quantize(palette=palette_img, dither=Image.Dither.NONE)


def save_gif(path: Path, frames: list[tuple[Image.Image, int]]) -> None:
    # Build a shared 48-color palette from a composite of a few frames.
    sample = Image.new("RGB", (TERM_W, TERM_H * 3))
    picks = [frames[0][0], frames[len(frames) // 2][0], frames[-1][0]]
    for i, im in enumerate(picks):
        sample.paste(im, (0, i * TERM_H))
    palette = sample.quantize(colors=48, method=Image.Quantize.MEDIANCUT)

    qframes = [quantize(im, palette).convert("P") for im, _ in frames]
    durations = [d for _, d in frames]
    qframes[0].save(
        path,
        save_all=True,
        append_images=qframes[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    banner = draw_banner()
    banner_path = ASSETS / "banner.png"
    banner.save(banner_path, "PNG", optimize=True)
    print(f"wrote {banner_path} {banner.size} {banner_path.stat().st_size} bytes")

    frames = build_gif_frames()
    # Drop some in-between typing frames to shrink the GIF if needed.
    # Keep first, last, and every 2nd typing frame when duration is short.
    compacted: list[tuple[Image.Image, int]] = []
    acc = 0
    for im, dur in frames:
        if dur <= 30:
            acc += dur
            if acc < 50 and compacted:
                # merge into previous duration conceptually — keep a frame every ~50ms
                continue
            compacted.append((im, acc if acc else dur))
            acc = 0
        else:
            if acc and compacted:
                pass
            compacted.append((im, dur))
            acc = 0
    gif_path = ASSETS / "demo.gif"
    save_gif(gif_path, compacted)
    print(f"wrote {gif_path} frames={len(compacted)} {gif_path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
