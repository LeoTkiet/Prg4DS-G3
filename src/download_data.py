"""
- Tải dữ liệu openFDA Animal & Veterinary Adverse Events cho các quý chỉ định
  (2025 Q1-Q4 + 2026 Q1) về thư mục data/raw/.
- Dùng openFDA REST API, phân trang (pagination) theo original_receive_date.
- Ghi metadata: nguồn, ngày tải, SHA-256 checksum vào data/raw/MANIFEST.json.

Chạy từ thư mục gốc của repo:
    python src/download_data.py            # tải 5 quý mặc định
    python src/download_data.py --force    # tải lại dù file đã có

Kết quả:
    data/raw/animalandveterinary-event-<quý>-<phần>.json   (mỗi quý một hoặc nhiều file)
    data/raw/MANIFEST.json                                  (nhật ký tải: ngày cập nhật, số dòng, sha256)
"""
import argparse
import hashlib
import json
import re
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# Danh sách file của openFDA (manifest) và các quý nhóm đã chọn.
MANIFEST_URL = "https://api.fda.gov/download.json"
QUARTERS = ["2025q1", "2025q2", "2025q3", "2025q4", "2026q1"]

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
QUARTER_RE = re.compile(r"/animalandveterinary/event/(\d{4}q\d)/")


def fetch(url: str, timeout: int = 120) -> bytes:
    """Tải một URL và trả về nội dung dạng bytes."""
    req = urllib.request.Request(url, headers={"User-Agent": "prg4ds-student-project"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def select_partitions(manifest: dict, quarters: list[str]) -> list[dict]:
    """Lọc từ manifest các file zip thuộc những quý cần lấy.

    Một quý có thể bị chia thành nhiều phần (0001-of-0002, ...), nên ta lấy theo
    danh sách trong manifest thay vì tự dựng URL.
    """
    event = manifest["results"]["animalandveterinary"]["event"]
    selected = []
    for part in event["partitions"]:
        m = QUARTER_RE.search(part["file"])
        if m and m.group(1) in quarters:
            selected.append({**part, "quarter": m.group(1)})
    missing = set(quarters) - {p["quarter"] for p in selected}
    if missing:
        raise RuntimeError(f"Manifest không có các quý: {sorted(missing)}")
    return sorted(selected, key=lambda p: p["file"])


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_json(zip_path: Path, quarter: str, raw_dir: Path) -> Path:
    """Giải nén file JSON duy nhất trong zip và đổi tên có kèm quý.

    Tên gốc của mọi quý đều là `animalandveterinary-event-0001-of-0001.json`,
    nên nếu không đổi tên thì các quý sẽ ghi đè lên nhau.
    """
    with zipfile.ZipFile(zip_path) as zf:
        inner = zf.namelist()[0]
        stem = Path(inner).stem  # ví dụ: animalandveterinary-event-0001-of-0001
        new_name = stem.replace("animalandveterinary-event-", f"animalandveterinary-event-{quarter}-") + ".json"
        out_path = raw_dir / new_name
        with zf.open(inner) as src, open(out_path, "wb") as dst:
            while chunk := src.read(1 << 20):
                dst.write(chunk)
    return out_path


def describe_file(json_path: Path, quarter: str, partition: dict) -> dict:
    """Đọc phần `meta` và kiểm tra số bản ghi so với manifest."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    meta = data["meta"]
    n_results = len(data["results"])
    entry = {
        "file": json_path.name,
        "quarter": quarter,
        "source_url": partition["file"],
        "last_updated": meta.get("last_updated"),            # ngày openFDA cập nhật file này
        "records_in_meta": meta["results"]["total"],
        "records_in_results": n_results,
        "records_in_manifest": partition.get("records"),
        "sha256": sha256_of(json_path),
    }
    if not (entry["records_in_meta"] == n_results == entry["records_in_manifest"]):
        print(f"  CẢNH BÁO {json_path.name}: số bản ghi không khớp "
              f"(meta={entry['records_in_meta']}, results={n_results}, manifest={entry['records_in_manifest']})")
    return entry


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="tải lại dù file đã tồn tại")
    ap.add_argument("--quarters", nargs="+", default=QUARTERS, help="ví dụ: 2025q1 2025q2")
    args = ap.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(fetch(MANIFEST_URL))
    event_info = manifest["results"]["animalandveterinary"]["event"]
    partitions = select_partitions(manifest, args.quarters)

    entries = []
    for part in partitions:
        quarter = part["quarter"]
        stem = Path(part["file"]).name.removesuffix(".json.zip")
        target = RAW_DIR / (stem.replace("animalandveterinary-event-", f"animalandveterinary-event-{quarter}-") + ".json")
        if target.exists() and not args.force:
            print(f"[bỏ qua] {target.name} đã có")
        else:
            print(f"[tải] {part['file']} (~{part.get('size_mb')} MB zip)")
            zip_path = RAW_DIR / (stem + f"-{quarter}.zip")
            zip_path.write_bytes(fetch(part["file"]))
            target = extract_json(zip_path, quarter, RAW_DIR)
            zip_path.unlink()  # xóa zip sau khi giải nén
        entries.append(describe_file(target, quarter, part))

    log = {
        "manifest_url": MANIFEST_URL,
        "manifest_export_date": event_info.get("export_date"),   # ngày openFDA xuất danh sách file
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "files": entries,
    }
    (RAW_DIR / "MANIFEST.json").write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\nQuý     last_updated  số bản ghi  file")
    for e in entries:
        print(f"{e['quarter']}  {e['last_updated']}   {e['records_in_results']:>9}  {e['file']}")
    print(f"\nĐã ghi {RAW_DIR / 'MANIFEST.json'}")


if __name__ == "__main__":
    main()