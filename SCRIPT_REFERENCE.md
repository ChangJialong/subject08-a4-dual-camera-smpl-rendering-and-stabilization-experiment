# 08A4 Experiment Script Reference

> Root: `D:\08A4_kgy`

## A. One-click dual-camera run

### `run_08A4_dualcam_render.ps1`
- Purpose: run EasyMocap for both cam00 and cam01, save logs, clean `EZcap_clean/output/sv1p` temporary folder after completion.
- Inputs:
  - Python env: `easymocap`
  - EMC root: `F:\GitHub\EZcap_clean`
  - Config ymls in `D:\08A4_kgy\configs`
  - Data roots in `D:\08A4_kgy\data\cam00|cam01`
- Outputs:
  - Logs: `cam00_run.log`, `cam01_run.log`, `run_all.log`
  - EMC output under `D:\08A4_kgy\emc_output\...`

## B. SMPL json editing scripts

### `make_smpl2_fix_rh_th.py`
- Copy `smpl -> smpl2`
- Force all frames `Rh` and `Th` to frame `000000.json` values.

### `make_smpl3_fix_th_only.py`
- Copy `smpl -> smpl3`
- Force all frames `Th` to frame `000000.json`, keep original `Rh`.

### `make_smpl4_temporal_smooth.py`
- Copy `smpl -> smpl4`
- Temporal smoothing:
  - `Rh`: moving average window 9
  - `Th`: moving average window 9
  - `poses`: moving average window 7
  - `shapes`: global mean over sequence

### `make_smpl5_fix_shapes.py`
- Copy `smpl -> smpl5`
- Replace all frame `shapes` with one fixed 10D vector.

## C. Re-render scripts from modified SMPL

### `render_from_smpl1.py`
- Render `smpl1` -> `render_smpl1` -> `render_smpl1.mp4`

### `render_from_smpl2.py`
- Render `smpl2` -> `render_smpl2` -> `render_smpl2.mp4`

### `render_from_smpl3.py`
- Render `smpl3` -> `render_smpl3` -> `render_smpl3.mp4`

### `render_from_smpl4_fast.py`
- Generic fast renderer (used for smpl4/smpl5 testing)
- Key options: `--max-frames`, `--scale`, `--crf`, `--preset`, `--jpeg-quality`

## D. Documentation in result folder

### `emc_output\cam00_full\sv1p\README.md`
- Describes `smpl1~smpl5` and corresponding render videos.
