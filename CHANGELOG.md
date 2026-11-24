# Changelog

## paper-fisat-camera-ready — 2026-11

### Fixed
- Removed a train/test leak: 18 images belonging to the training split were also present in the `test/images` folders (listed in `benchmark/results/rerun_report_v2.md`, section 5). The earlier M2/M3/M6 runs were therefore trained on 250 images instead of 232.
- M2, M3 and M6 were retrained on the 232-image training split (same hyperparameters and seed 42) and re-evaluated. M1 is not trained; regenerating and re-evaluating it reproduced the earlier numbers in all 20 cells.
- `generate_benchmark.py` restored to the prompt version used for all reported results; the 'single motif' prompt variant (commit b4518ea) was not used for the paper.

### Changed
- `README.md` and `benchmark/results/{metrics_overall,metrics_per_period}.csv`, `evaluation_report.txt`: updated to the re-run results; Key Findings reworded as run-specific observations with a caveat on training length, single seed and FID50 sample size.
- `benchmark/checkpoints/{M2,M3,M6}/training_log.csv`: replaced with logs of the re-run.
- `.gitignore`: backup checkpoints, old generated images and weight file types (`*.bin`, `*.ckpt`, `*.pth`) are not tracked.

### Added
- `benchmark/results/rerun_report_v2.md` and `rerun_v2_*.csv`: re-run report and comparison with the earlier numbers (kept here for history).
- Figure scripts (`benchmark/make_figure*.py`) and re-run figures, training/generation logs, `run_training.ps1`.

### Previous numbers (superseded, history only)
Overall FID50 / SSIM: M2 349.76 / 0.1422, M3 371.80 / 0.0687, M6 344.16 / 0.1623.
