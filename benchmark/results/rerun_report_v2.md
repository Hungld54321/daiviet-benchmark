# Rerun report v2 — FISAT 2026 (sau khi sửa rò rỉ dữ liệu)

Không commit, không push. Code sinh/đánh giá = `HEAD` (tag `paper-fisat-v1`); `train_benchmark.py` chỉ khác HEAD ở ký tự `→` → `->`.

## 1. Table 5 (chạy mới)

Overall = trung bình cộng 3 thời kỳ; khớp cột Overall trong `metrics_overall.csv`.

| Model | Thời kỳ | FID50 | CLIP | SSIM | LPIPS | PSNR |
|---|---|---|---|---|---|---|
| M1 | Ly-Tran | 341.03 | 0.2727 | 0.0935 | 0.6461 | 4.20 |
| M1 | Le | 383.46 | 0.2690 | 0.0230 | 0.7636 | 6.07 |
| M1 | Nguyen | 349.48 | 0.2737 | 0.1123 | 0.8348 | 6.27 |
| M1 | Overall | 357.99 | 0.2718 | 0.0763 | 0.7482 | 5.51 |
| M2 | Ly-Tran | 337.20 | 0.2481 | 0.1432 | 0.6492 | 4.01 |
| M2 | Le | 382.73 | 0.2518 | 0.0271 | 0.7636 | 5.47 |
| M2 | Nguyen | 339.40 | 0.2677 | 0.2262 | 0.8116 | 6.20 |
| M2 | Overall | 353.11 | 0.2559 | 0.1322 | 0.7415 | 5.22 |
| M3 | Ly-Tran | 411.21 | 0.2151 | 0.0652 | 0.6190 | 4.92 |
| M3 | Le | 431.83 | 0.2173 | 0.0138 | 0.7393 | 5.66 |
| M3 | Nguyen | 375.40 | 0.2252 | 0.0862 | 0.7985 | 7.79 |
| M3 | Overall | 406.15 | 0.2192 | 0.0551 | 0.7189 | 6.12 |
| M6 | Ly-Tran | 308.96 | 0.2494 | 0.2063 | 0.6314 | 4.30 |
| M6 | Le | 365.59 | 0.2519 | 0.0339 | 0.7776 | 5.54 |
| M6 | Nguyen | 320.82 | 0.2627 | 0.2525 | 0.8102 | 6.09 |
| M6 | Overall | 331.79 | 0.2547 | 0.1642 | 0.7397 | 5.31 |

## 2. So sánh từng ô với số trong bài (Δ = mới − bài)

**FID50**

| Model | Thời kỳ | Bài | Mới | Δ |
|---|---|---|---|---|
| M1 | Ly-Tran | 341.03 | 341.03 | +0.00 |
| M1 | Le | 383.46 | 383.46 | +0.00 |
| M1 | Nguyen | 349.48 | 349.48 | +0.00 |
| M1 | Overall | 357.99 | 357.99 | +0.00 |
| M2 | Ly-Tran | 345.00 | 337.20 | -7.80 |
| M2 | Le | 375.94 | 382.73 | +6.79 |
| M2 | Nguyen | 328.35 | 339.40 | +11.05 |
| M2 | Overall | 349.76 | 353.11 | +3.35 |
| M3 | Ly-Tran | 388.54 | 411.21 | +22.67 |
| M3 | Le | 366.28 | 431.83 | +65.55 |
| M3 | Nguyen | 360.57 | 375.40 | +14.83 |
| M3 | Overall | 371.80 | 406.15 | +34.35 |
| M6 | Ly-Tran | 339.62 | 308.96 | -30.66 |
| M6 | Le | 370.67 | 365.59 | -5.08 |
| M6 | Nguyen | 322.19 | 320.82 | -1.37 |
| M6 | Overall | 344.16 | 331.79 | -12.37 |

**CLIP**

| Model | Thời kỳ | Bài | Mới | Δ |
|---|---|---|---|---|
| M1 | Ly-Tran | 0.2727 | 0.2727 | +0.0000 |
| M1 | Le | 0.2690 | 0.2690 | +0.0000 |
| M1 | Nguyen | 0.2737 | 0.2737 | +0.0000 |
| M1 | Overall | 0.2718 | 0.2718 | +0.0000 |
| M2 | Ly-Tran | 0.2479 | 0.2481 | +0.0002 |
| M2 | Le | 0.2573 | 0.2518 | -0.0055 |
| M2 | Nguyen | 0.2479 | 0.2677 | +0.0198 |
| M2 | Overall | 0.2510 | 0.2559 | +0.0049 |
| M3 | Ly-Tran | 0.2197 | 0.2151 | -0.0046 |
| M3 | Le | 0.2333 | 0.2173 | -0.0160 |
| M3 | Nguyen | 0.2341 | 0.2252 | -0.0089 |
| M3 | Overall | 0.2290 | 0.2192 | -0.0098 |
| M6 | Ly-Tran | 0.2364 | 0.2494 | +0.0130 |
| M6 | Le | 0.2789 | 0.2519 | -0.0270 |
| M6 | Nguyen | 0.2574 | 0.2627 | +0.0053 |
| M6 | Overall | 0.2576 | 0.2547 | -0.0029 |

**SSIM**

| Model | Thời kỳ | Bài | Mới | Δ |
|---|---|---|---|---|
| M1 | Ly-Tran | 0.0935 | 0.0935 | +0.0000 |
| M1 | Le | 0.0230 | 0.0230 | +0.0000 |
| M1 | Nguyen | 0.1123 | 0.1123 | +0.0000 |
| M1 | Overall | 0.0763 | 0.0763 | +0.0000 |
| M2 | Ly-Tran | 0.1532 | 0.1432 | -0.0100 |
| M2 | Le | 0.0284 | 0.0271 | -0.0013 |
| M2 | Nguyen | 0.2450 | 0.2262 | -0.0188 |
| M2 | Overall | 0.1422 | 0.1322 | -0.0100 |
| M3 | Ly-Tran | 0.0859 | 0.0652 | -0.0207 |
| M3 | Le | 0.0214 | 0.0138 | -0.0076 |
| M3 | Nguyen | 0.0988 | 0.0862 | -0.0126 |
| M3 | Overall | 0.0687 | 0.0551 | -0.0136 |
| M6 | Ly-Tran | 0.1844 | 0.2063 | +0.0219 |
| M6 | Le | 0.0336 | 0.0339 | +0.0003 |
| M6 | Nguyen | 0.2690 | 0.2525 | -0.0165 |
| M6 | Overall | 0.1623 | 0.1642 | +0.0019 |

**LPIPS**

| Model | Thời kỳ | Bài | Mới | Δ |
|---|---|---|---|---|
| M1 | Ly-Tran | 0.6461 | 0.6461 | +0.0000 |
| M1 | Le | 0.7636 | 0.7636 | +0.0000 |
| M1 | Nguyen | 0.8348 | 0.8348 | +0.0000 |
| M1 | Overall | 0.7482 | 0.7482 | +0.0000 |
| M2 | Ly-Tran | 0.6378 | 0.6492 | +0.0114 |
| M2 | Le | 0.7734 | 0.7636 | -0.0098 |
| M2 | Nguyen | 0.8329 | 0.8116 | -0.0213 |
| M2 | Overall | 0.7480 | 0.7415 | -0.0065 |
| M3 | Ly-Tran | 0.6126 | 0.6190 | +0.0064 |
| M3 | Le | 0.7165 | 0.7393 | +0.0228 |
| M3 | Nguyen | 0.7648 | 0.7985 | +0.0337 |
| M3 | Overall | 0.6980 | 0.7189 | +0.0209 |
| M6 | Ly-Tran | 0.6341 | 0.6314 | -0.0027 |
| M6 | Le | 0.7748 | 0.7776 | +0.0028 |
| M6 | Nguyen | 0.8163 | 0.8102 | -0.0061 |
| M6 | Overall | 0.7417 | 0.7397 | -0.0020 |

**PSNR**

| Model | Thời kỳ | Bài | Mới | Δ |
|---|---|---|---|---|
| M1 | Ly-Tran | 4.20 | 4.20 | +0.00 |
| M1 | Le | 6.07 | 6.07 | +0.00 |
| M1 | Nguyen | 6.27 | 6.27 | +0.00 |
| M1 | Overall | 5.51 | 5.51 | +0.00 |
| M2 | Ly-Tran | 3.84 | 4.01 | +0.17 |
| M2 | Le | 5.39 | 5.47 | +0.08 |
| M2 | Nguyen | 6.57 | 6.20 | -0.37 |
| M2 | Overall | 5.27 | 5.22 | -0.05 |
| M3 | Ly-Tran | 5.15 | 4.92 | -0.23 |
| M3 | Le | 6.54 | 5.66 | -0.88 |
| M3 | Nguyen | 7.83 | 7.79 | -0.04 |
| M3 | Overall | 6.51 | 6.12 | -0.39 |
| M6 | Ly-Tran | 4.23 | 4.30 | +0.07 |
| M6 | Le | 5.68 | 5.54 | -0.14 |
| M6 | Nguyen | 6.05 | 6.09 | +0.04 |
| M6 | Overall | 5.32 | 5.31 | -0.01 |

## 3. Huấn luyện (chạy mới)

| Model | Epoch | Step/epoch | Tổng step | Thời gian (phút) | VRAM đỉnh (GB) | L_diff TB epoch cuối | L_cult TB epoch cuối |
|---|---|---|---|---|---|---|---|
| M2 | 50 | 116 | 5800 | 87.9 | 10.75 | 0.05072 | — |
| M3 | 50 | 29 | 1450 | 22.0 | 7.81 | 0.05623 | — |
| M6 | 30 | 116 | 3480 | 54.5 | 11.69 | 0.04499 | 0.00145 |

Cách tính (giống `train_benchmark.py`): trung bình số học của loss từng step trong epoch cuối. L_cult chỉ được tính mỗi 16 step (các step còn lại ghi 0 và vẫn nằm trong mẫu số). Trung bình chỉ trên các step có tính L_cult (n=7): 0.02409. Giá trị L_diff/L_cult trong bảng được tính lại từ `training_log.csv` và đối chiếu với dòng in ra cuối epoch của log train: M2: 0.05072/0.05072, M3: 0.05623/0.05623, M6: 0.04499/0.04499 (log/csv).

Lần train cũ (bài, từ `training_log.csv`/`training_config.json` ở HEAD):

| Model | Epoch | Step/epoch | L_diff TB epoch cuối | L_cult TB epoch cuối | Thời gian | VRAM đỉnh |
|---|---|---|---|---|---|---|
| M2 | 50 | 125 | 0.04285 | — | không có bản ghi | không có bản ghi |
| M3 | 50 | 31 | 0.05181 | — | không có bản ghi | không có bản ghi |
| M6 | 30 | 125 | 0.04922 | 0.00232 | không có log (~58 phút theo trí nhớ của người chạy, không kiểm chứng được) | 11.7 (chỉ README, không có log gốc) |

Thời gian và VRAM của các lần train cũ không được lưu trong repo (không có log train ở HEAD); không ước lượng.

## 4. Hình

**4b. Lưới ảnh sinh 3×4** — `benchmark/results/figure3_generated_grid_rerun_v2.{svg,pdf,png}` (+ `_mpl.pdf`). Dùng đúng script `benchmark/make_figure3_v3.py` (import nguyên bản, chỉ đổi tên file xuất để không ghi đè hình cũ) và đúng seed `top_score` trong `benchmark/samples_for_review/selected_samples.csv` (file từ 2026-04-27, không sửa). Seed không được chọn lại theo ảnh mới:

| Thời kỳ | M1 | M2 | M3 | M6 |
|---|---|---|---|---|
| Ly-Tran | 4 | 27 | 49 | 27 |
| Le | 4 | 27 | 49 | 27 |
| Nguyen | 31 | 27 | 49 | 27 |

Nhận xét định tính: ảnh M3 mới là kết cấu mịn kiểu nhiễu/đường nét dày đặc, không rõ họa tiết; M2 và M6 vẫn là họa tiết tông vàng-đen.

**4a. Loss curves** — `benchmark/results/figure4_loss_curves_rerun_v2.{svg,pdf}`, vẽ bằng **script MỚI** `benchmark/make_figure4_loss_curves.py`. Script của hình cũ không còn (không tìm thấy trong repo, lịch sử git, worktree, thư mục người dùng hay transcript), nên script này được viết lại từ danh sách thông số do tác giả cung cấp; kiểu dáng có thể khác hình cũ ở các chi tiết không được nêu.
- Theo thông số: figsize 6.5×2.8, 2 panel ((a) M2+M3, (b) M6); trục x Training Step thang log, trục y Diffusion Loss tuyến tính 0–0.20, nhãn y chung đặt bằng `fig.text`; đường liền EMA `span=200` (`adjust=False`), lw 2.0; chấm tròn ms 5.5, viền trắng, 17 điểm chia đều thang log (tại mỗi model, trên giá trị EMA); màu M2 và M6 `#2166ac`, M3 `#d6604d`; font serif, `svg.fonttype='none'`, `pdf.fonttype=42`; chỉ diffusion loss. Dữ liệu: `training_log.csv` của lần train mới.
- Quyết định của tôi cho chi tiết không được nêu: step trong log đánh số từ 0 nên trục x dùng `step + 1` (bắt đầu từ 1); xlim panel (a) là 1–5800, panel (b) là 1–3480; nhãn "(a)"/"(b)" đặt dưới trục x; có chú giải (M2, M3 / M6); không lưới; gai đồ thị mặc định.
- **PDF không đi qua cairosvg:** `cairosvg` không chạy được trên máy này (thiếu thư viện hệ thống `libcairo`). PDF được xuất bằng backend PDF gốc của matplotlib với `pdf.fonttype=42` (chữ là TrueType, chọn được). SVG có chữ thật (26 phần tử `<text>`). Nếu cần đúng đường cairosvg thì phải cài libcairo, tôi chưa làm.

## 5. 18 file thừa trong `test/images` (không di chuyển)

Các file này nằm trong thư mục test nhưng thuộc `split == "train"` trong manifest (và cũng nằm trong thư mục train). `evaluate_benchmark.py` lấy ảnh test theo manifest nên không dùng chúng.

768 và 512 cùng danh sách: True. Danh sách (18 file):

- `HVDV_-_NGN_-_010b_crop_01.png`
- `HVDV_-_NGN_-_AO_-_023_crop_02.png`
- `HVDV_-_NGN_-_AO_-_037_crop_01.png`
- `HVDV_-_NGN_-_AO_-_040_crop_01.png`
- `HVDV_-_NGN_-_AO_-_097_crop_02.png`
- `HVDV_-_NGN_-_AO_-_098_crop_01.png`
- `HVDV_-_NGN_-_AO_-_098_crop_08.png`
- `HVDV_-_NGN_-_AO_-_099_crop_01.png`
- `HVDV_-_NGN_-_DO_-_006_crop_01.png`
- `HVDV_-_NGN_-_DO_-_008_crop_01.png`
- `HVDV_-_NGN_-_DO_-_011_crop_01.png`
- `HVDV_-_NGN_-_KT_-_005_crop_01.png`
- `HVDV_-_NGN_-_KT_-_008_crop_01.png`
- `HVDV_-_NGN_-_KT_-_017_crop_01.png`
- `HVDV_-_NGN_-_KT_-_018_crop_01.png`
- `HVDV_-_NGN_-_KT_-_018_crop_02.png`
- `HVDV_-_NGN_-_KT_-_019_crop_03.png`
- `HVDV_-_NGN_-_PT_-_003_crop_01.png`

## 6. Quy trình, đối chiếu và lưu ý

**Tái lập M1 (Bước 4).** Sinh lại M1 bằng `generate_benchmark.py` HEAD và đánh giá bằng `evaluate_benchmark.py` HEAD: 20/20 ô (4 dòng × 5 metric) khớp bài đến hết số chữ số thập phân. Lần đánh giá cuối (4 model) cho M1 giống hệt (mục 2, Δ = 0 mọi ô). Kết quả Bước 4 riêng được giữ ở `benchmark/_results_M1_step4/`.

**Nguyên nhân lần chạy trước sai.** `generate_benchmark.py` có thay đổi prompt chưa commit (đổi "pattern" → "motif", thêm negative prompt, `safety_checker=None`). Patch lưu ở `benchmark/_patches/generate_prompts_uncommitted.patch`; file đã khôi phục về HEAD. `evaluate_benchmark.py` không bị sửa lần nào trong lần chạy này (không cần patch `local_files_only`: biến môi trường offline là đủ).

**Môi trường.** `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, `PYTHONUTF8=1`. Python 3.11.9, torch 2.5.1+cu121, diffusers 0.37.1, transformers 5.4.0, peft 0.18.1, clean-fid 0.1.35, lpips 0.1.4, RTX 4080. Phiên bản thư viện của lần chạy trong bài không được ghi lại. Tag `paper-fisat-v1` → `1eb1e6a`.

**Cấu hình train (chung).** 232 ảnh, rank 16, alpha 32, lr UNet 1e-4, lr text encoder 1e-5, warmup 100, seed 42. M2: SDXL 768, 50 epoch, batch 2. M3: SD 1.5 512, 50 epoch, batch 8. M6: SDXL 768, 30 epoch, batch 2, λ_cult 0.3, `--cultural_every 16`.

**Bằng chứng lần train cũ dùng 250 ảnh.** `training_log.csv` ở HEAD có 125 step/epoch (M2, M6, batch 2) và 31 step/epoch (M3, batch 8), tức 250 ảnh/epoch (232 + 18). Lần train mới có 116 và 29 step/epoch (232 ảnh).

**Backup, không xóa/ghi đè.** `benchmark/checkpoints/{M2,M3,M6}_pre_retrain/`, `M3_crashed_ep10/`, `M6_50ep_unused/` (M6 50 epoch, không dùng), `benchmark/_generated_wrong_prompts/`, `benchmark/_results_wrong_prompts/`, `benchmark/generated_pre_retrain/`, `*_v1_leaked/`, `results/train_M6_50ep_unused_log.txt`. `benchmark_manifest.csv` không sửa. Không commit, không push, không động tới Zenodo.

**Lưu ý đọc kết quả.**
- FID50 dùng N = 50 ảnh/thời kỳ và mỗi model train một lần (seed 42), nên chênh lệch vài điểm FID chưa chắc có ý nghĩa.
- So với bài: M1 không đổi; M2 lẫn lộn (Overall FID +3.35, CLIP +0.0049, SSIM −0.0100, LPIPS −0.0065); M3 kém hơn rõ (Overall FID +34.35, CLIP −0.0098, SSIM −0.0136); M6 tốt hơn ở FID (Overall −12.37) với SSIM +0.0019.
- Các nhận định trong README/bài dựa trên số cũ cần xem lại. Ví dụ "M6 vs M2": số cũ giảm FID50 5.6 điểm và SSIM +14.1%; số mới giảm 21.32 điểm và SSIM +24.2% (0.1642 so với 0.1322).

## 7. Cultural loss của M6 (lần chạy mới, 30 epoch)

Dữ liệu: `benchmark/checkpoints/M6/training_log.csv`; `loss_cultural` chỉ được tính ở các step có `step % 16 == 0` (cột `step` bắt đầu từ 0, đúng điều kiện `global_step % cultural_every == 0` trong `train_benchmark.py`). Có 218 step như vậy trên tổng 3480; cả 218 đều có giá trị > 0 và không có step nào khác có giá trị > 0.

**Theo từng step, chỉ trên 218 step có tính cultural loss:**

| | min | max | trung vị | phân vị 5 | phân vị 95 | trung bình |
|---|---|---|---|---|---|---|
| Lần mới (v2) | 0.00085 | 0.12907 | 0.02063 | 0.00511 | 0.10412 | 0.03202 |
| Bài cũ (HEAD, 235 step) | 0.00104 | 0.15322 | 0.02191 | 0.00391 | 0.09251 | 0.03284 |

**Trung bình theo epoch, có tính cả step ghi 0 (đúng như số in cuối mỗi epoch trong log train):**

| | min | max | trung vị | phân vị 5 | phân vị 95 |
|---|---|---|---|---|---|
| Lần mới (v2, 30 epoch) | 0.00084 | 0.00431 | 0.00193 | 0.00112 | 0.00296 |
| Bài cũ (HEAD, 30 epoch) | 0.00075 | 0.00335 | 0.00192 | 0.00092 | 0.00322 |

**Về câu cũ "fluctuates between 0.001 and 0.005":** khoảng đó **không** đúng với giá trị theo step (92% step của lần cũ và 96% step của lần mới nằm trên 0.005, đỉnh trên 0.12). Nó khớp với trung bình theo epoch có tính step ghi 0 (lần mới: 0.0008–0.0043, hơn 90% epoch nằm trong 0.001–0.005), tức là đại lượng đã bị chia loãng khoảng 16 lần do 15/16 step ghi 0. Nếu sửa câu, nên nói rõ đại lượng được mô tả: ví dụ "the per-step cultural loss (computed every 16 steps) has a median of 0.021 (5th-95th percentile 0.005-0.104)", hoặc "the epoch-averaged value, which includes the zero-valued steps, stays between 0.0008 and 0.0043".

CSV: `benchmark/results/rerun_v2_m6_cultural_loss_stats.csv` (cả hai cách tính, cả hai lần chạy).
