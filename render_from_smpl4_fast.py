import argparse
import json
import shutil
import subprocess
from pathlib import Path

import cv2
import numpy as np
from tqdm import tqdm

from myeasymocap.io.model import SMPLLoader
from easymocap.visualize.pyrender_wrapper import plot_meshes


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sv1p", default=r"D:\08A4_kgy\emc_output\cam00_full\sv1p")
    ap.add_argument("--smpl-dir-name", default="smpl4")
    ap.add_argument("--img-dir", default=r"D:\08A4_kgy\data\cam00\images\08A4_00")
    ap.add_argument("--render-dir-name", default="render_smpl4")
    ap.add_argument("--video-name", default="render_smpl4.mp4")
    ap.add_argument("--ffmpeg", default=r"F:\software\Anaconda\envs\easymocap\Library\bin\ffmpeg.exe")
    ap.add_argument("--max-frames", type=int, default=600)
    ap.add_argument("--scale", type=float, default=0.5)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crf", type=int, default=30)
    ap.add_argument("--preset", default="veryfast")
    ap.add_argument("--jpeg-quality", type=int, default=80)
    args = ap.parse_args()

    sv1p = Path(args.sv1p)
    smpl_dir = sv1p / args.smpl_dir_name
    img_dir = Path(args.img_dir)
    render_dir = sv1p / args.render_dir_name
    video_out = sv1p / args.video_name
    ffmpeg = Path(args.ffmpeg)

    if not smpl_dir.exists():
        raise FileNotFoundError(f"No dir: {smpl_dir}")
    if not img_dir.exists():
        raise FileNotFoundError(f"No dir: {img_dir}")
    if not ffmpeg.exists():
        raise FileNotFoundError(f"No ffmpeg: {ffmpeg}")

    if render_dir.exists():
        shutil.rmtree(render_dir)
    render_dir.mkdir(parents=True, exist_ok=True)

    smpl_files = sorted(smpl_dir.glob("*.json"))
    img_files = sorted(img_dir.glob("*.jpg"))
    if not smpl_files:
        raise FileNotFoundError(f"No json in {smpl_dir}")
    if not img_files:
        raise FileNotFoundError(f"No images in {img_dir}")

    n = min(len(smpl_files), len(img_files), args.max_frames)
    if n <= 0:
        raise RuntimeError("No frames to render")

    first = cv2.imread(str(img_files[0]))
    if first is None:
        raise RuntimeError(f"Cannot read image: {img_files[0]}")
    h0, w0 = first.shape[:2]
    scale = float(args.scale)
    if scale <= 0:
        raise ValueError("--scale must be > 0")
    w = int(round(w0 * scale))
    h = int(round(h0 * scale))
    w = max(2, w - (w % 2))
    h = max(2, h - (h % 2))
    focal = 1.2 * min(h, w)
    K = np.array([[focal, 0.0, w / 2.0], [0.0, focal, h / 2.0], [0.0, 0.0, 1.0]], dtype=np.float32)
    R = np.eye(3, dtype=np.float32)
    T = np.zeros((3, 1), dtype=np.float32)

    loader = SMPLLoader(
        model_path="models/pare/data/body_models/smpl/SMPL_NEUTRAL.pkl",
        regressor_path="models/J_regressor_body25.npy",
    )
    body_model = loader()["body_model"]
    faces = body_model.faces

    for i in tqdm(range(n), desc="render_smpl4_fast"):
        with smpl_files[i].open("r", encoding="utf-8") as f:
            ann = json.load(f)
        if not ann:
            continue
        item = ann[0]
        params = {
            "Rh": np.asarray(item["Rh"], dtype=np.float32),
            "Th": np.asarray(item["Th"], dtype=np.float32),
            "poses": np.asarray(item["poses"], dtype=np.float32),
            "shapes": np.asarray(item["shapes"], dtype=np.float32),
        }
        img = cv2.imread(str(img_files[i]))
        if img is None:
            continue
        if (img.shape[1], img.shape[0]) != (w, h):
            img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)

        vertices = body_model.vertices(params, return_tensor=False)[0]
        meshes = {0: {"vertices": vertices, "faces": faces, "id": 0, "name": "human_0"}}
        out = plot_meshes(img, meshes, K, R, T, mode="image")
        jpeg_quality = int(args.jpeg_quality)
        jpeg_quality = max(1, min(100, jpeg_quality))
        cv2.imwrite(str(render_dir / f"{i:06d}.jpg"), out, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])

    cmd = [
        str(ffmpeg),
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-stats",
        "-r",
        str(args.fps),
        "-i",
        str(render_dir / "%06d.jpg"),
        "-vf",
        "scale=2*ceil(iw/2):2*ceil(ih/2)",
        "-pix_fmt",
        "yuv420p",
        "-vcodec",
        "libx264",
        "-preset",
        str(args.preset),
        "-crf",
        str(args.crf),
        "-r",
        str(args.fps),
        str(video_out),
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] rendered frames: {n}")
    print(f"[OK] render dir: {render_dir}")
    print(f"[OK] video: {video_out}")


if __name__ == "__main__":
    main()
