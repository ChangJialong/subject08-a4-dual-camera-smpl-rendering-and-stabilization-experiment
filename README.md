# Subject 08 A4 Dual-Camera SMPL Rendering and Stabilization Experiment

This directory contains the full local experiment for Subject 08, Action A4, dual-camera EasyMocap processing and SMPL stabilization tests.

## 1) Goal

- Run EasyMocap on two cameras (`CamIntelRealSense_00` + `CamIntelRealSense_01`)
- Export SMPL results
- Perform controlled parameter experiments on SMPL json:
  - fix `Rh`
  - fix `Th`
  - fix both `Rh+Th`
  - temporal smoothing
  - fix `shapes`
- Re-render videos for side-by-side comparison

## 2) Main inputs

- Raw RS source: `D:\8\RS\recording_2026_01_19_15_10_44`
- EasyMocap root used by scripts: `F:\GitHub\EZcap_clean`

## 3) Main outputs

- Experiment root: `D:\08A4_kgy`
- EMC results:
  - `D:\08A4_kgy\emc_output\cam00_full\sv1p`
  - `D:\08A4_kgy\emc_output\cam01_full\sv1p`
- Render comparison videos:
  - `render.mp4` (original)
  - `render_smpl1.mp4` ... `render_smpl5.mp4`
  - `render_smpl401.mp4` (high-quality 30s version of smpl4)

## 4) Current script summary

See `SCRIPT_REFERENCE.md`.

## 5) Notes

- This experiment folder includes a large amount of generated artifacts (frames/json/videos/logs).
- For reproducibility, keep scripts + configs + README; generated frames can be re-created when needed.

## 6) Repository packaging note

To keep GitHub repository size manageable, this repo keeps scripts/configs/logs and representative outputs.
Large regenerated artifacts (full frame dumps and full EMC intermediate trees) remain in local workspace D:\08A4_kgy.

