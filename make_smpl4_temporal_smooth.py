import argparse
import json
from pathlib import Path

import numpy as np


def smooth_1d_series(values: np.ndarray, window: int) -> np.ndarray:
    if window <= 1 or len(values) <= 1:
        return values.copy()
    if window % 2 == 0:
        window += 1
    pad = window // 2
    padded = np.pad(values, ((pad, pad), (0, 0)), mode="edge")
    kernel = np.ones(window, dtype=np.float32) / float(window)
    out = np.empty_like(values, dtype=np.float32)
    for i in range(values.shape[1]):
        out[:, i] = np.convolve(padded[:, i], kernel, mode="valid")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=r"D:\08A4_kgy\emc_output\cam00_full\sv1p\smpl")
    ap.add_argument("--dst", default=r"D:\08A4_kgy\emc_output\cam00_full\sv1p\smpl4")
    ap.add_argument("--win-rh", type=int, default=9)
    ap.add_argument("--win-th", type=int, default=9)
    ap.add_argument("--win-poses", type=int, default=7)
    args = ap.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)
    dst.mkdir(parents=True, exist_ok=True)

    files = sorted(src.glob("*.json"))
    if not files:
        raise FileNotFoundError(f"No json found in {src}")

    rh = []
    th = []
    poses = []
    shapes = []
    raw_data = []

    for fp in files:
        with fp.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not data:
            raise RuntimeError(f"Empty json: {fp}")
        item = data[0]
        raw_data.append(data)
        rh.append(np.asarray(item["Rh"], dtype=np.float32).reshape(-1))
        th.append(np.asarray(item["Th"], dtype=np.float32).reshape(-1))
        poses.append(np.asarray(item["poses"], dtype=np.float32).reshape(-1))
        shapes.append(np.asarray(item["shapes"], dtype=np.float32).reshape(-1))

    rh_arr = np.stack(rh, axis=0)
    th_arr = np.stack(th, axis=0)
    poses_arr = np.stack(poses, axis=0)
    shapes_arr = np.stack(shapes, axis=0)

    rh_s = smooth_1d_series(rh_arr, args.win_rh)
    th_s = smooth_1d_series(th_arr, args.win_th)
    poses_s = smooth_1d_series(poses_arr, args.win_poses)
    shapes_mean = shapes_arr.mean(axis=0, keepdims=False)

    for idx, fp in enumerate(files):
        data = raw_data[idx]
        data[0]["Rh"] = rh_s[idx].reshape(1, -1).tolist()
        data[0]["Th"] = th_s[idx].reshape(1, -1).tolist()
        data[0]["poses"] = poses_s[idx].reshape(1, -1).tolist()
        data[0]["shapes"] = shapes_mean.reshape(1, -1).tolist()
        with (dst / fp.name).open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"[OK] src={src}")
    print(f"[OK] dst={dst}")
    print(f"[OK] files={len(files)}")
    print(
        f"[OK] windows: Rh={args.win_rh}, Th={args.win_th}, poses={args.win_poses}"
    )


if __name__ == "__main__":
    main()
