# DaiViet-Pattern Benchmark

Comparative evaluation of four generative models for Vietnamese ornamental pattern (*hoa văn*) synthesis, using a curated dataset of vector motifs extracted from the *Hoa Văn Đại Việt* publication series.

---

## Overview

This benchmark compares four Stable Diffusion variants (M1, M2, M3, M6) on the task of generating Vietnamese ornamental motifs across three historical dynasties: **Lý-Trần**, **Lê**, and **Nguyễn**. The central question is whether period-aware cultural conditioning (M6) measurably improves generation fidelity over standard LoRA fine-tuning (M2) and vanilla SDXL (M1).

The full pipeline runs end-to-end: PDF vector source → motif extraction → benchmark dataset → training → generation → evaluation.

---

## Dataset

The dataset is built exclusively from **200 PDF vector files** published by the *Hoa Văn Đại Việt* project (collaboration between Đại Việt Cổ Phong and Comicola). Each file contains ornamental patterns hand-drawn by professional illustrators from original museum artifacts and historical records — not photographs or web-scraped images.

| Property | Detail |
|---|---|
| **Source** | 200 PDF vector files — *Hoa Văn Đại Việt* (Đại Việt Cổ Phong × Comicola) |
| **Content** | Patterns hand-drawn by professional illustrators from museum artifacts |
| **Extraction method** | Adaptive grid detection (`extract_pdf_motifs.py`) |
| **Total motifs** | 291 individual motifs |
| **Periods** | Lý-Trần: 50 &nbsp;·&nbsp; Lê: 94 &nbsp;·&nbsp; Nguyễn: 147 |
| **Train / Test split** | 232 train / 59 test (stratified by period, `seed=42`) |
| **Test references** | Lý-Trần: 10 &nbsp;·&nbsp; Lê: 19 &nbsp;·&nbsp; Nguyễn: 30 |
| **Metadata** | Excel annotations per file: motif ID, artist, description, historical source |
| **Image format** | PNG, 768 × 768 px (SDXL models) &nbsp;·&nbsp; 512 × 512 px (SD 1.5) |

Each motif is accompanied by structured Excel metadata maintained by the project team, including provenance (dynasty, artifact type, museum reference) and artist attribution.

---

## Models Benchmarked

| ID | Base Model | Fine-tuning | Key Config | Epochs |
|---|---|---|---|---|
| **M1** | SDXL 1.0 | None (control group) | Vanilla inference, no trigger word | — |
| **M2** | SDXL 1.0 | LoRA | rank=16, α=32, lr_unet=1e-4, lr_te=1e-5 | 50 |
| **M3** | SD 1.5 | LoRA | rank=16, α=32, lr_unet=1e-4, lr_te=1e-5 | 50 |
| **M6** | SDXL 1.0 | LoRA + Cultural Loss | rank=16, α=32; latent Gram matrix, λ=0.3, every=16 steps | 30 |

**M6 cultural loss** computes a Gram matrix style loss in latent space between the predicted clean latent (`pred_x0`) and a same-period reference latent sampled per batch. Gradient flows directly through the UNet prediction without VAE decoding, keeping peak VRAM at 11.7 GB on an RTX 4080.

All models generate 50 images per period (150 total) using fixed seeds 0–49, period-specific trigger words, and identical inference settings (30 DDIM steps, CFG=7.5, resolution per model class).

---

## Results

> **Correction (October 2026).** The results below replace an earlier version. In the earlier run, 18 images that belong to the training split were also present in the test image folder, and M2, M3 and M6 were trained on 250 images instead of the intended 232. M2, M3 and M6 were retrained on the 232-image training split and re-evaluated; M1 (no training) reproduces the earlier numbers exactly. Details: `benchmark/results/rerun_report_v2.md`.

### Overall (macro-average across 3 periods)

| Model | FID50 ↓ | CLIP ↑ | SSIM ↑ | LPIPS ↓ | PSNR ↑ | Inf. Time (s) |
|---|---|---|---|---|---|---|
| **M6** | **331.79** | 0.2547 | **0.1642** | 0.7397 | 5.31 | 4.43 |
| M2 | 353.11 | 0.2559 | 0.1322 | 0.7415 | 5.22 | 4.39 |
| M1 | 357.99 | **0.2718** | 0.0763 | 0.7482 | 5.51 | 4.41 |
| M3 | 406.15 | 0.2192 | 0.0551 | **0.7189** | **6.12** | **2.45** |

### Per-period breakdown

| Model | Period | FID50 ↓ | CLIP ↑ | SSIM ↑ | LPIPS ↓ | PSNR ↑ |
|---|---|---|---|---|---|---|
| M6 | Lý-Trần | **308.96** | 0.2494 | **0.2063** | 0.6314 | 4.30 |
| M2 | Lý-Trần | 337.20 | 0.2481 | 0.1432 | 0.6492 | 4.01 |
| M1 | Lý-Trần | 341.03 | **0.2727** | 0.0935 | 0.6461 | 4.20 |
| M3 | Lý-Trần | 411.21 | 0.2151 | 0.0652 | **0.6190** | **4.92** |
| M6 | Lê | **365.59** | 0.2519 | **0.0339** | 0.7776 | 5.54 |
| M2 | Lê | 382.73 | 0.2518 | 0.0271 | 0.7636 | 5.47 |
| M1 | Lê | 383.46 | **0.2690** | 0.0230 | 0.7636 | **6.07** |
| M3 | Lê | 431.83 | 0.2173 | 0.0138 | **0.7393** | 5.66 |
| M6 | Nguyễn | **320.82** | 0.2627 | **0.2525** | 0.8102 | 6.09 |
| M2 | Nguyễn | 339.40 | 0.2677 | 0.2262 | 0.8116 | 6.20 |
| M1 | Nguyễn | 349.48 | **0.2737** | 0.1123 | 0.8348 | 6.27 |
| M3 | Nguyễn | 375.40 | 0.2252 | 0.0862 | **0.7985** | **7.79** |

> **Metric definitions:** FID50 — Fréchet Inception Distance on N=50 generated images (lower = better). CLIP — cosine similarity with CLIP ViT-L/14 embeddings (higher = better). SSIM — Structural Similarity Index (higher = better). LPIPS — Learned Perceptual Image Patch Similarity, VGG (lower = better). PSNR — Peak Signal-to-Noise Ratio in dB (higher = better). SSIM / LPIPS / PSNR use nearest-reference proxy matching (unpaired setting).

---

## Key Findings

- In this run, M6 has the lowest FID50 (331.79) and the highest SSIM (0.1642) overall, and is also best on both metrics in each of the three periods.

- M1 (vanilla SDXL) has the highest CLIP score (0.2718). M3 (SD 1.5) has the best LPIPS (0.7189) and PSNR (6.12 dB), the fastest inference (2.45 s vs. 4.4 s for the SDXL models), and the worst FID50 (406.15), CLIP (0.2192) and SSIM (0.0551).

- M2 and M6 (SDXL, fine-tuned) have lower FID50 than M1 (SDXL, no fine-tuning); M2 vs. M1 is mixed across metrics (FID50 353.11 vs. 357.99, CLIP 0.2559 vs. 0.2718).

> Note: M2 (50 epochs) and M6 (30 epochs) differ in training length, so the
> M2–M6 gap does not isolate the effect of the cultural loss. Each model was
> trained once with a single seed, and FID50 uses 50 generated vs 10–30 real
> images, so differences are indicative rather than a definitive ranking.
> No single model is best on all metrics: M6 has the best overall FID50 and SSIM,
> M1 the best CLIP score, and M3 the best LPIPS and PSNR.

---

## Repository Structure

```
DaiViet-Pattern/
│
├── extract_pdf_motifs.py         # PDF → PNG motif extraction (adaptive grid detection)
├── prepare_benchmark_data.py     # Train/test split, resolution resize, manifest generation
├── crawl_wikimedia.py            # Supplementary image crawler (not part of benchmark dataset)
│
├── dataset_manifest.csv          # Full dataset inventory (all 291 motifs + metadata)
├── benchmark_manifest.csv        # Train/test split manifest (seed=42)
│
├── vector_extracted/
│   ├── ly_tran/extract_manifest.csv   # Extraction log: Lý-Trần (50 motifs, 45 source PDFs)
│   ├── le/extract_manifest.csv        # Extraction log: Lê (94 motifs, 85 source PDFs)
│   └── nguyen/extract_manifest.csv    # Extraction log: Nguyễn (147 motifs, 70 source PDFs)
│
└── benchmark/
    ├── train_benchmark.py        # Training loop — LoRA (M2/M3) and LoRA+cultural loss (M6)
    ├── generate_benchmark.py     # Image generation — 50 seeds × 3 periods × 4 models
    ├── evaluate_benchmark.py     # Evaluation — FID50 / CLIP / SSIM / LPIPS / PSNR
    ├── run_full_benchmark.py     # End-to-end pipeline orchestrator
    ├── README.md                 # Quick-start notes
    │
    ├── checkpoints/
    │   ├── M2/
    │   │   ├── pytorch_lora_weights.safetensors   # [gitignored — large binary]
    │   │   ├── training_log.csv                   # Step-level loss log (5,800 rows)
    │   │   └── training_config.json               # Full hyperparameter record
    │   ├── M3/                                    # Same structure as M2
    │   └── M6/                                    # Same structure + loss_cultural column
    │
    ├── results/
    │   ├── evaluation_report.txt   # Human-readable full evaluation report
    │   ├── metrics_overall.csv     # Overall metrics (machine-readable)
    │   └── metrics_per_period.csv  # Per-period breakdown (machine-readable)
    │
    └── pipeline_logs/
        └── pipeline_v4_status.txt  # Timestamped execution log (TRAIN → GEN → EVAL)
```

> **Not tracked in this repository:** `*.safetensors` model weights, raw PDF source files (`vector_source/`), extracted PNG images (`vector_extracted/*.png`), and generated benchmark images (`benchmark/generated/`). All can be regenerated from the steps below.

---

## How to Reproduce

### Prerequisites

```bash
# Python 3.10+, CUDA 11.8+
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install diffusers==0.27.2 transformers peft safetensors accelerate
pip install cleanfid open-clip-torch scikit-image lpips
pip install tqdm pandas openpyxl pdf2image pillow
```

**Hardware:** NVIDIA RTX 4080 16 GB (or equivalent ≥ 12 GB VRAM). M3 (SD 1.5) runs on ≥ 8 GB VRAM.

### Step 1 — Place PDF source files

```
vector_source/45_hoavanlytran/     ← Lý-Trần PDFs (45 files)
vector_source/85_hoavanle/         ← Lê PDFs (85 files)
vector_source/70_hoa_van_nguyen/   ← Nguyễn PDFs (70 files)
vector_source/excel_metadata/      ← Excel annotation files (3 workbooks)
```

Source files are provided separately by the *Hoa Văn Đại Việt* project team.

### Step 2 — Extract motifs from PDFs

```bash
python extract_pdf_motifs.py \
  --input_dir vector_source/45_hoavanlytran \
  --excel "vector_source/excel_metadata/45 Hoa Văn Lý Trần_v04.xlsx" \
  --period Ly-Tran --output_dir vector_extracted/ly_tran

python extract_pdf_motifs.py \
  --input_dir vector_source/85_hoavanle \
  --excel "vector_source/excel_metadata/85 Hoa Văn Thời Lê.xlsx" \
  --period Le --output_dir vector_extracted/le

python extract_pdf_motifs.py \
  --input_dir vector_source/70_hoa_van_nguyen \
  --excel "vector_source/excel_metadata/70 Hoa Văn Thời Nguyễn_ver_03.xlsx" \
  --period Nguyen --output_dir vector_extracted/nguyen
```

### Step 3 — Prepare benchmark dataset

```bash
python prepare_benchmark_data.py
# → benchmark_data/768/D_all/{train,test}/   (SDXL resolution)
# → benchmark_data/512/D_all/{train,test}/   (SD 1.5 resolution)
# → dataset_manifest.csv, benchmark_manifest.csv
```

### Step 4 — Run full benchmark pipeline

```bash
# End-to-end: train M2/M3/M6 → generate all → evaluate all
python benchmark/run_full_benchmark.py

# Or step by step:
python benchmark/train_benchmark.py    --model M2
python benchmark/train_benchmark.py    --model M3
python benchmark/train_benchmark.py    --model M6
python benchmark/generate_benchmark.py --model all
python benchmark/evaluate_benchmark.py --model all
```

Results are written to `benchmark/results/`.

---

## Limitations

- **FID50 is indicative only.** Standard FID uses N=50,000 samples; N=50 per period produces higher-variance estimates. Results should be interpreted directionally rather than as precise distributional scores.

- **SSIM / LPIPS / PSNR are unpaired proxies.** Generated images are matched to held-out test references by period, not by semantic content. These metrics reflect structural plausibility relative to real motifs rather than pixel-level reconstruction.

- **Cultural loss operates in latent space.** M6's Gram matrix loss is computed on predicted clean latents rather than on decoded pixel-space features (VGG perceptual loss), due to the VRAM cost of backpropagating through the SDXL VAE decoder at 768 px. The latent Gram matrix captures a different (lower-level) notion of style similarity than pixel-space VGG features.

- **Small dataset.** 291 motifs across 3 periods is a constrained training set for generative modelling. LoRA fine-tuning mitigates overfitting by preserving the pretrained SDXL prior, but generated diversity may be limited compared to larger domain datasets.

---

## Branch Information

This is the `benchmark` branch. The `main` branch contains separate work.
