# -*- coding: utf-8 -*-
"""
benchmark/make_review_grid.py
Create comparison grids for TS. Hai review.

Steps:
  1. Score all 50 images per model×period, select top 3
  2. Create 3 per-period grids (4 models × 3 seeds)
  3. Create 1 overview grid (4 models × 3 periods, top-1 each)
  4. Copy 36 selected images to individual/ subfolder
"""

import csv
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ── Paths ────────────────────────────────────────────────────────────────────
REPO        = Path(__file__).resolve().parent.parent
GEN_DIR     = REPO / "benchmark" / "generated"
OUT_DIR     = REPO / "benchmark" / "samples_for_review"
IND_DIR     = OUT_DIR / "individual"

MODELS      = ["M1", "M2", "M3", "M6"]
PERIODS     = ["Ly-Tran", "Le", "Nguyen"]
N_SEEDS     = 50
TOP_N       = 3          # images to select per model×period

# Grid appearance
THUMB_SIZE  = 400        # px per cell (square)
LABEL_H     = 60         # header row height (model labels)
ROW_LABEL_W = 80         # left column width (seed / period labels)
PAD         = 6          # padding between cells
BG_COLOR    = (245, 245, 242)
LABEL_COLOR = (30, 30, 30)
HEADER_BG   = (220, 215, 205)
FONT_LARGE  = 22
FONT_SMALL  = 16


# ── Helpers ──────────────────────────────────────────────────────────────────
def _try_font(size: int):
    for name in ["arial.ttf", "Arial.ttf", "DejaVuSans.ttf",
                 "LiberationSans-Regular.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    return ImageFont.load_default()


def score_image(img_path: Path) -> dict:
    """Compute quality score for a single image."""
    img = Image.open(img_path).convert("L")           # grayscale
    arr = np.array(img, dtype=np.float32)

    # 1. Entropy — rich content = high entropy
    hist, _ = np.histogram(arr.ravel(), bins=256, range=(0, 256))
    hist = hist / (hist.sum() + 1e-9)
    entropy = float(-np.sum(hist * np.log2(hist + 1e-9)))

    # 2. Edge density — clear lines = more edges
    from scipy.ndimage import sobel
    sx = sobel(arr, axis=0)
    sy = sobel(arr, axis=1)
    edge_density = float(np.sqrt(sx**2 + sy**2).mean())

    # 3. Penalise near-blank (std < 10) or near-black (mean < 20)
    std  = float(arr.std())
    mean = float(arr.mean())
    blank_penalty = 1.0 if (std > 10 and mean > 20) else 0.0

    score = (entropy / 8.0) * 0.5 + (edge_density / 40.0) * 0.4 + blank_penalty * 0.1
    return {"entropy": entropy, "edge_density": edge_density,
            "std": std, "mean": mean, "score": score}


# ── Step 1: Select top-3 images per model×period ─────────────────────────────
def select_samples() -> dict:
    """
    Returns: {(model, period): [{"seed": int, ...metrics, "path": Path}, ...]}
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    selected = {}
    csv_rows = []

    for model in MODELS:
        for period in PERIODS:
            period_dir = GEN_DIR / model / period
            candidates = []
            for seed in range(N_SEEDS):
                img_path = period_dir / f"{period}_seed_{seed:02d}.png"
                if not img_path.exists():
                    continue
                try:
                    m = score_image(img_path)
                    candidates.append({"seed": seed, "path": img_path, **m})
                except Exception as e:
                    print(f"  [WARN] {model}/{period}/seed{seed}: {e}")

            if not candidates:
                print(f"  [WARN] No images found for {model}/{period}")
                selected[(model, period)] = []
                continue

            # Sort by composite score descending
            candidates.sort(key=lambda x: x["score"], reverse=True)

            # Diversity filter: reject if too similar to already-chosen
            # (compare mean pixel value as rough proxy)
            chosen = []
            for c in candidates:
                if len(chosen) >= TOP_N:
                    break
                arr = np.array(Image.open(c["path"]).convert("L"), dtype=np.float32)
                too_close = any(
                    abs(arr.mean() - np.array(Image.open(p["path"]).convert("L"),
                                              dtype=np.float32).mean()) < 5
                    for p in chosen
                )
                if not too_close:
                    chosen.append(c)

            # Fill up to TOP_N if diversity filter left gaps
            if len(chosen) < TOP_N:
                for c in candidates:
                    if len(chosen) >= TOP_N:
                        break
                    if c not in chosen:
                        chosen.append(c)

            selected[(model, period)] = chosen[:TOP_N]

            for rank, c in enumerate(chosen[:TOP_N]):
                reason = "top_score" if rank == 0 else "diverse"
                csv_rows.append({
                    "model": model, "period": period, "seed": c["seed"],
                    "entropy": round(c["entropy"], 4),
                    "edge_density": round(c["edge_density"], 4),
                    "score": round(c["score"], 4),
                    "reason": reason,
                })

    # Write CSV
    csv_path = OUT_DIR / "selected_samples.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["model","period","seed",
                                               "entropy","edge_density","score","reason"])
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"  Selected samples → {csv_path}")
    return selected


# ── Grid drawing helpers ──────────────────────────────────────────────────────
def _draw_cell(draw, img, canvas, x, y, w, h, font, label=None):
    """Paste thumbnail into canvas cell, draw optional label."""
    thumb = img.resize((w, h), Image.LANCZOS)
    canvas.paste(thumb, (x, y))
    if label:
        draw.rectangle([x, y, x + w, y + 20], fill=(0, 0, 0, 160))
        draw.text((x + 4, y + 2), label, fill=(255, 255, 255), font=font)


def make_period_grid(period: str, selected: dict, out_path: Path):
    """
    4 cols (models) × 3 rows (top-3 seeds) for one period.
    """
    font_lg = _try_font(FONT_LARGE)
    font_sm = _try_font(FONT_SMALL)

    n_rows = TOP_N
    n_cols = len(MODELS)

    W = ROW_LABEL_W + n_cols * (THUMB_SIZE + PAD) + PAD
    H = LABEL_H     + n_rows * (THUMB_SIZE + PAD) + PAD

    canvas = Image.new("RGB", (W, H), BG_COLOR)
    draw   = ImageDraw.Draw(canvas)

    # Header row — model labels
    draw.rectangle([0, 0, W, LABEL_H], fill=HEADER_BG)
    draw.text((4, LABEL_H // 2 - 8), period, fill=LABEL_COLOR, font=font_lg)
    for ci, model in enumerate(MODELS):
        x = ROW_LABEL_W + PAD + ci * (THUMB_SIZE + PAD)
        draw.text((x + THUMB_SIZE // 2 - 20, LABEL_H // 2 - 10),
                  model, fill=LABEL_COLOR, font=font_lg)

    # Content rows
    for ri in range(n_rows):
        y = LABEL_H + PAD + ri * (THUMB_SIZE + PAD)
        # Row label (rank)
        rank_label = f"#{ri+1}"
        draw.text((4, y + THUMB_SIZE // 2 - 8), rank_label,
                  fill=LABEL_COLOR, font=font_sm)

        for ci, model in enumerate(MODELS):
            x = ROW_LABEL_W + PAD + ci * (THUMB_SIZE + PAD)
            choices = selected.get((model, period), [])
            if ri >= len(choices):
                draw.rectangle([x, y, x + THUMB_SIZE, y + THUMB_SIZE],
                               fill=(200, 200, 200))
                draw.text((x + 10, y + THUMB_SIZE // 2), "N/A",
                          fill=(100, 100, 100), font=font_sm)
                continue

            seed = choices[ri]["seed"]
            img_path = GEN_DIR / model / period / f"{period}_seed_{seed:02d}.png"
            img = Image.open(img_path).convert("RGB")
            thumb = img.resize((THUMB_SIZE, THUMB_SIZE), Image.LANCZOS)
            canvas.paste(thumb, (x, y))

            # Seed label overlay
            draw.rectangle([x, y, x + 70, y + 22], fill=(0, 0, 0))
            draw.text((x + 3, y + 3), f"seed {seed:02d}",
                      fill=(255, 255, 255), font=font_sm)

    canvas.save(out_path, quality=92)
    print(f"  Period grid → {out_path.name}  ({W}×{H}px)")


def make_overview_grid(selected: dict, out_path: Path):
    """
    4 cols (models) × 3 rows (periods). Each cell = top-1 image.
    """
    font_lg = _try_font(FONT_LARGE)
    font_sm = _try_font(FONT_SMALL)

    n_rows = len(PERIODS)
    n_cols = len(MODELS)

    W = ROW_LABEL_W + n_cols * (THUMB_SIZE + PAD) + PAD
    H = LABEL_H     + n_rows * (THUMB_SIZE + PAD) + PAD

    canvas = Image.new("RGB", (W, H), BG_COLOR)
    draw   = ImageDraw.Draw(canvas)

    # Header
    draw.rectangle([0, 0, W, LABEL_H], fill=HEADER_BG)
    draw.text((4, LABEL_H // 2 - 8), "Overview", fill=LABEL_COLOR, font=font_lg)
    for ci, model in enumerate(MODELS):
        x = ROW_LABEL_W + PAD + ci * (THUMB_SIZE + PAD)
        draw.text((x + THUMB_SIZE // 2 - 20, LABEL_H // 2 - 10),
                  model, fill=LABEL_COLOR, font=font_lg)

    # Rows
    for ri, period in enumerate(PERIODS):
        y = LABEL_H + PAD + ri * (THUMB_SIZE + PAD)
        # Period label
        period_short = {"Ly-Tran": "Lý-Trần", "Le": "Lê", "Nguyen": "Nguyễn"}[period]
        draw.text((2, y + THUMB_SIZE // 2 - 8), period_short,
                  fill=LABEL_COLOR, font=font_sm)

        for ci, model in enumerate(MODELS):
            x = ROW_LABEL_W + PAD + ci * (THUMB_SIZE + PAD)
            choices = selected.get((model, period), [])
            if not choices:
                draw.rectangle([x, y, x + THUMB_SIZE, y + THUMB_SIZE],
                               fill=(200, 200, 200))
                continue

            seed = choices[0]["seed"]
            img_path = GEN_DIR / model / period / f"{period}_seed_{seed:02d}.png"
            img = Image.open(img_path).convert("RGB")
            thumb = img.resize((THUMB_SIZE, THUMB_SIZE), Image.LANCZOS)
            canvas.paste(thumb, (x, y))

            draw.rectangle([x, y, x + 70, y + 22], fill=(0, 0, 0))
            draw.text((x + 3, y + 3), f"seed {seed:02d}",
                      fill=(255, 255, 255), font=font_sm)

    canvas.save(out_path, quality=92)
    print(f"  Overview grid → {out_path.name}  ({W}×{H}px)")


# ── Step 4: Copy individual images ───────────────────────────────────────────
def copy_individual(selected: dict):
    total = 0
    for (model, period), choices in selected.items():
        dest_dir = IND_DIR / model
        dest_dir.mkdir(parents=True, exist_ok=True)
        for c in choices[:TOP_N]:
            seed = c["seed"]
            src  = GEN_DIR / model / period / f"{period}_seed_{seed:02d}.png"
            dst  = dest_dir / f"{period}_seed_{seed:02d}.png"
            shutil.copy2(src, dst)
            total += 1
    print(f"  Copied {total} individual images → {IND_DIR}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("\n=== Step 1: Scoring and selecting top images ===")
    selected = select_samples()

    # Print selection summary
    for (model, period), choices in sorted(selected.items()):
        seeds = [c["seed"] for c in choices]
        scores = [round(c["score"], 3) for c in choices]
        print(f"  {model}/{period}: seeds={seeds}  scores={scores}")

    print("\n=== Step 2: Creating per-period grids ===")
    for period in PERIODS:
        out = OUT_DIR / f"comparison_{period}.png"
        make_period_grid(period, selected, out)

    print("\n=== Step 3: Creating overview grid ===")
    make_overview_grid(selected, OUT_DIR / "overview_grid.png")

    print("\n=== Step 4: Copying individual images ===")
    copy_individual(selected)

    print("\nDone. Output in:", OUT_DIR)


if __name__ == "__main__":
    main()
