import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from tqdm import tqdm

from myeasymocap.io.model import SMPLLoader
from easymocap.visualize.pyrender_wrapper import plot_meshes

sv1p = Path(r"D:\08A4_kgy\emc_output\cam00_full\sv1p")
smpl_dir = sv1p / "smpl2"
img_dir = Path(r"D:\08A4_kgy\data\cam00\images\08A4_00")
render_dir = sv1p / "render_smpl2"
video_out = sv1p / "render_smpl2.mp4"
ffmpeg = Path(r"F:\software\Anaconda\envs\easymocap\Library\bin\ffmpeg.exe")

render_dir.mkdir(parents=True, exist_ok=True)

smpl_files = sorted(smpl_dir.glob("*.json"))
img_files = sorted(img_dir.glob("*.jpg"))
if not smpl_files:
    raise FileNotFoundError(f"No json in {smpl_dir}")
if not img_files:
    raise FileNotFoundError(f"No images in {img_dir}")

n = min(len(smpl_files), len(img_files))

first = cv2.imread(str(img_files[0]))
if first is None:
    raise RuntimeError(f"Cannot read image: {img_files[0]}")
h, w = first.shape[:2]
focal = 1.2 * min(h, w)
K = np.array([[focal, 0.0, w / 2.0], [0.0, focal, h / 2.0], [0.0, 0.0, 1.0]], dtype=np.float32)
R = np.eye(3, dtype=np.float32)
T = np.zeros((3, 1), dtype=np.float32)

loader = SMPLLoader(
    model_path='models/pare/data/body_models/smpl/SMPL_NEUTRAL.pkl',
    regressor_path='models/J_regressor_body25.npy'
)
body_model = loader()['body_model']
faces = body_model.faces

for i in tqdm(range(n), desc='render_smpl2'):
    with smpl_files[i].open('r', encoding='utf-8') as f:
        ann = json.load(f)
    if not ann:
        continue
    item = ann[0]
    params = {
        'Rh': np.array(item['Rh'], dtype=np.float32),
        'Th': np.array(item['Th'], dtype=np.float32),
        'poses': np.array(item['poses'], dtype=np.float32),
        'shapes': np.array(item['shapes'], dtype=np.float32),
    }

    img = cv2.imread(str(img_files[i]))
    if img is None:
        continue

    vertices = body_model.vertices(params, return_tensor=False)[0]
    meshes = {
        0: {
            'vertices': vertices,
            'faces': faces,
            'id': 0,
            'name': 'human_0'
        }
    }
    out = plot_meshes(img, meshes, K, R, T, mode='image')
    cv2.imwrite(str(render_dir / f"{i:06d}.jpg"), out)

cmd = [
    str(ffmpeg), '-y', '-hide_banner', '-loglevel', 'error',
    '-r', '30', '-i', str(render_dir / '%06d.jpg'),
    '-vf', 'scale=2*ceil(iw/2):2*ceil(ih/2)',
    '-pix_fmt', 'yuv420p', '-vcodec', 'libx264', '-r', '30',
    str(video_out)
]
subprocess.run(cmd, check=True)
print(f"[OK] rendered frames: {n}")
print(f"[OK] video: {video_out}")
