import json
from pathlib import Path

src = Path(r"D:\08A4_kgy\emc_output\cam00_full\sv1p\smpl")
dst = Path(r"D:\08A4_kgy\emc_output\cam00_full\sv1p\smpl3")
dst.mkdir(parents=True, exist_ok=True)

with (src / "000000.json").open("r", encoding="utf-8") as f:
    base = json.load(f)
base_th = base[0]["Th"]

count = 0
for fp in sorted(src.glob("*.json")):
    with fp.open("r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        # 保留原始 Rh，不改 Rh
        item["Th"] = base_th
    with (dst / fp.name).open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    count += 1

print("base_th =", base_th)
print("written =", count)
