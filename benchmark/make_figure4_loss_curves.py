# -*- coding: utf-8 -*-
"""
benchmark/make_figure4_loss_curves.py
Figure 4 -- diffusion-loss curves of the re-run (v2) training logs.

NEW script (the script of the original figure was not available); written from
the parameter list given by the author.
  (a) M2 and M3   (b) M6
  x: Training Step, log scale (step 1 = first optimizer step), y: Diffusion Loss, 0-0.20
  solid line: EMA(span=200), lw=2.0; dots: EMA value at ~17 log-spaced steps
Exports SVG, then PDF (cairosvg if available, else matplotlib's native PDF).

Run from anywhere:  python benchmark/make_figure4_loss_curves.py [--preview out.png]
"""
import argparse
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams.update({
    "font.family": "serif",
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
})

REPO = Path(__file__).resolve().parent.parent
CKPT = REPO / "benchmark" / "checkpoints"
OUT_DIR = REPO / "benchmark" / "results"
STEM = "figure4_loss_curves_rerun_v2"

BLUE, RED = "#2166ac", "#d6604d"
EMA_SPAN = 200
N_MARKERS = 17          # log-spaced marker positions (16-18 after de-duplication)
PANELS = [
    ("(a)", [("M2", BLUE), ("M3", RED)]),
    ("(b)", [("M6", BLUE)]),
]


def load_curve(model: str):
    df = pd.read_csv(CKPT / model / "training_log.csv")
    step = df["step"].to_numpy() + 1                     # log file is 0-indexed
    ema = df["loss_diffusion"].ewm(span=EMA_SPAN, adjust=False).mean().to_numpy()
    return step, ema


def marker_positions(step: np.ndarray) -> np.ndarray:
    target = np.unique(np.round(np.logspace(0, np.log10(step.max()), N_MARKERS)).astype(int))
    idx = np.searchsorted(step, target)
    idx = np.unique(idx[idx < len(step)])
    assert 16 <= len(idx) <= 18, f"{len(idx)} markers"
    return idx


def make_figure() -> plt.Figure:
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.8))
    for ax, (tag, series) in zip(axes, PANELS):
        n_max = 0
        for model, color in series:
            step, ema = load_curve(model)
            n_max = max(n_max, int(step.max()))
            ax.plot(step, ema, color=color, lw=2.0, label=model,
                    marker="o", ms=5.5, markeredgecolor="white", clip_on=False,
                    markevery=[int(i) for i in marker_positions(step)])
        ax.set_xscale("log")
        ax.set_xlim(1, n_max)
        ax.set_ylim(0, 0.20)
        ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
        ax.set_xlabel("Training Step", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.legend(frameon=False, fontsize=8, loc="upper right")
        ax.text(0.5, -0.30, tag, transform=ax.transAxes, ha="center", va="top", fontsize=9)
    fig.subplots_adjust(left=0.105, right=0.985, bottom=0.24, top=0.96, wspace=0.24)
    fig.text(0.025, 0.58, "Diffusion Loss", rotation=90, ha="center", va="center", fontsize=9)
    return fig


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", help="also write a PNG preview to this path")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg_path, pdf_path = OUT_DIR / f"{STEM}.svg", OUT_DIR / f"{STEM}.pdf"
    fig = make_figure()
    fig.savefig(svg_path, format="svg", bbox_inches="tight", facecolor="white")
    print(f"SVG saved: {svg_path}  (<text> elements: "
          f"{len(re.findall(r'<text', svg_path.read_text(encoding='utf-8')))})")

    try:
        import cairosvg
        cairosvg.svg2pdf(url=str(svg_path), write_to=str(pdf_path))
        print(f"PDF saved via cairosvg: {pdf_path}")
    except (ImportError, OSError) as e:
        fig.savefig(pdf_path, format="pdf", bbox_inches="tight", facecolor="white")
        print(f"cairosvg unavailable ({type(e).__name__}); PDF saved via matplotlib native "
              f"backend (pdf.fonttype=42, selectable text): {pdf_path}")
    if args.preview:
        fig.savefig(args.preview, format="png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
