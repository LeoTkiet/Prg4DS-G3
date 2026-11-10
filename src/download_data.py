"""
- Dùng bulk download của openFDA (danh sách file lấy từ https://api.fda.gov/download.json),
  tải các file .json.zip theo quý rồi giải nén.
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
import shutil
import time
import urllib.error
import http.client
import sys

# Danh sách file của openFDA (manifest) và các quý nhóm đã chọn.
MANIFEST_URL = "https://api.fda.gov/download.json"
QUARTERS = ["2025q1", "2025q2", "2025q3", "2025q4", "2026q1"]

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
QUARTER_RE = re.compile(r"/animalandveterinary/event/(\d{4}q\d)/")


def fetch_json(url: str, timeout: int = 120, retries: int = 3) -> dict:
    """Tải JSON nhỏ (như manifest) trực tiếp vào RAM có cơ chế retry."""
    req = urllib.request.Request(url, headers={"User-Agent": "prg4ds-student-project"})
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (OSError, http.client.HTTPException, json.JSONDecodeError) as e:
            print(f"  [Cảnh báo] Lỗi tải {url} (lần {attempt}/{retries}): {e}")
            if attempt == retries:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff: chờ 2s, 4s...


def download_file(url: str, dest_path: Path, timeout: int = 120, retries: int = 3) -> None:
    """Stream trực tiếp từ network xuống file tạm trên đĩa để tránh tràn RAM (OOM)."""
    req = urllib.request.Request(url, headers={"User-Agent": "prg4ds-student-project"})
    tmp_path = dest_path.with_suffix(dest_path.suffix + ".tmp")
    
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp, open(tmp_path, "wb") as dst:
                shutil.copyfileobj(resp, dst, length=1 << 20)  # Stream từng chunk 1MB
            tmp_path.replace(dest_path)  # Hoàn tất 100% mới đổi tên thành file chính thức
            return
        except (OSError, http.client.HTTPException) as e:
            print(f"  [Cảnh báo] Lỗi tải file {dest_path.name} (lần {attempt}/{retries}): {e}")
            if tmp_path.exists():
                tmp_path.unlink()  # Xóa file tạm bị lỗi
            if attempt == retries:
                raise
            time.sleep(2 ** attempt)


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
    """Giải nén file JSON duy nhất trong zip qua file tạm rồi đổi tên chính thức."""
    with zipfile.ZipFile(zip_path) as zf:
        inner = zf.namelist()[0]
        stem = Path(inner).stem
        new_name = stem.replace("animalandveterinary-event-", f"animalandveterinary-event-{quarter}-") + ".json"
        out_path = raw_dir / new_name
        tmp_path = out_path.with_suffix(".json.tmp")
        try:
            with zf.open(inner) as src, open(tmp_path, "wb") as dst:
                shutil.copyfileobj(src, dst, length=1 << 20)
            tmp_path.replace(out_path)  # Atomic rename
        except BaseException:
            if tmp_path.exists():
                tmp_path.unlink()  # Dọn file rác nếu user bấm Ctrl+C hoặc lỗi đĩa
            raise
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
    manifest = fetch_json(MANIFEST_URL)
    event_info = manifest["results"]["animalandveterinary"]["event"]
    partitions = select_partitions(manifest, args.quarters)

    entries = []
    failed = []
    removed = []
    for part in partitions:
        quarter = part["quarter"]
        stem = Path(part["file"]).name.removesuffix(".json.zip")
        target = RAW_DIR / (stem.replace("animalandveterinary-event-", f"animalandveterinary-event-{quarter}-") + ".json")
        zip_path = RAW_DIR / (stem + f"-{quarter}.zip")

        try:
            if target.exists() and not args.force:
                print(f"[bỏ qua] {target.name} đã có")
            else:
                print(f"[tải] {part['file']} (~{part.get('size_mb')} MB zip)")
                download_file(part["file"], zip_path)
                target = extract_json(zip_path, quarter, RAW_DIR)
                zip_path.unlink(missing_ok=True)

            entries.append(describe_file(target, quarter, part))

        except (OSError, http.client.HTTPException, zipfile.BadZipFile, json.JSONDecodeError, KeyError) as e:
            print(f"  [LỖI] Không thể xử lý {part['file']} (quý {quarter}): {e}")
            failed.append(part["file"])
            # Nếu file target có sẵn nhưng bị hỏng JSON (phát hiện ở describe_file), xóa đi để lần sau tải lại
            if isinstance(e, (json.JSONDecodeError, KeyError)) and target.exists():
                target.unlink(missing_ok=True)      # file hỏng thật thì xoá để lần sau tải lại
                removed.append(target.name)
            if zip_path.exists():
                zip_path.unlink(missing_ok=True)
            continue

    manifest_path = RAW_DIR / "MANIFEST.json"
    old_files = {}
    if manifest_path.exists():
        try:
            old_files = {e["file"]: e for e in
                         json.loads(manifest_path.read_text(encoding="utf-8")).get("files", [])}
        except (json.JSONDecodeError, KeyError, TypeError):
            old_files = {}
    old_files.update({e["file"]: e for e in entries})
    for n in removed:
        old_files.pop(n, None)

    log = {
        "manifest_url": MANIFEST_URL,
        "manifest_export_date": event_info.get("export_date"),
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "files": sorted(old_files.values(), key=lambda e: e["file"]),
    }
    manifest_path.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\nQuý     last_updated  số bản ghi  file")
    for e in entries:
        print(f"{e['quarter']}  {e['last_updated']}   {e['records_in_results']:>9}  {e['file']}")
    print(f"\nĐã ghi {manifest_path}")
    if failed:
        print(f"\n[THẤT BẠI] {len(failed)} file lỗi: {failed}")
        sys.exit(1)


if __name__ == "__main__":
    main()