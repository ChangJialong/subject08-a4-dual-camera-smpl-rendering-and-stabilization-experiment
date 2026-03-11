import argparse
import json
from pathlib import Path


TARGET_SHAPES = [
    0.4894700348377228,
    0.908483624458313,
    4.775576114654541,
    0.7642002701759338,
    6.354478359222412,
    -0.998260498046875,
    -2.556788206100464,
    9.176281929016113,
    -3.135380268096924,
    -2.6686112880706787,
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=r"D:\08A4_kgy\emc_output\cam00_full\sv1p\smpl")
    ap.add_argument("--dst", default=r"D:\08A4_kgy\emc_output\cam00_full\sv1p\smpl5")
    args = ap.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)
    dst.mkdir(parents=True, exist_ok=True)

    files = sorted(src.glob("*.json"))
    if not files:
        raise FileNotFoundError(f"No json found in {src}")

    count = 0
    for fp in files:
        with fp.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not data:
            continue
        for item in data:
            item["shapes"] = [TARGET_SHAPES]
        with (dst / fp.name).open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        count += 1

    print(f"[OK] src={src}")
    print(f"[OK] dst={dst}")
    print(f"[OK] files={count}")


if __name__ == "__main__":
    main()
