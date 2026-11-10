"""
Module: data_loader.py
Chức năng:
- Đọc các file JSON (hoặc .json.zip) tải về từ openFDA Animal & Veterinary Adverse Events
  giai đoạn 2025 (Q1-Q4) đến 2026 (Q1) trong thư mục `data/raw/`.
- Trích xuất phần `meta` (để kiểm tra ngày cập nhật, tổng số bản ghi từng quý) và phần `results`.
- Chuẩn hóa thành 4 bảng quan hệ phẳng liên kết qua `unique_aer_id_number`:
  1. `reports`: Thông tin cấp báo cáo (id, ngày nhận, ngày khởi phát, người báo cáo, serious_ae, treated_for_ae, type_of_information, animal demographics...).
  2. `drugs`: Danh sách thuốc nhúng trong `drug[]`, kèm cột `active_ingredients` (tên hoạt chất nối bằng ';').
     các cột liều `dose_*` và tần suất `frequency_value`, `frequency_unit` (làm phẳng từ `dose` và `frequency_of_administration`).
  3. `reactions`: Danh sách phản ứng bất lợi theo thuật ngữ VeDDRA (explode từ `reaction[]`).
  4. `outcomes`: Kết cục y khoa của vật nuôi (explode từ `outcome[]`).
Mọi giá trị giữ nguyên dạng chuỗi như file gốc; ép kiểu (ngày, số) làm ở bước tiền xử lý trong notebook.
"""


from pathlib import Path
from typing import Dict, List, Tuple
import json
import logging
import re
import zipfile
 
import pandas as pd
 
log = logging.getLogger(__name__)
 
KEY = "unique_aer_id_number"
 
# Khớp cả hai kiểu tên file:
# animalandveterinary-event-2025q1.json(.zip)
# animalandveterinary-event-2025q1-0001-of-0001.json(.zip)   (một quý có thể có nhiều phần)
_QUARTER_FILE_RE = re.compile(
    r"animalandveterinary-event-(\d{4}q[1-4])(?:-\d{4}-of-\d{4})?\.(json|json\.zip)$",
    re.IGNORECASE,
)
 
# Các trường cấp báo cáo được đưa vào reports (cột animal được làm phẳng riêng)
_NESTED_REPORT_FIELDS = {"reaction", "drug", "outcome", "animal", "receiver",
                         "duration", "health_assessment_prior_to_exposure"}



def discover_raw_files(raw_dir: str | Path = "data/raw") -> List[Path]:
    """
    Tìm tất cả các file JSON / ZIP chứa dữ liệu openFDA AV Events trong `data/raw/`.
    Nếu cùng một quý có cả .json và .json.zip thì ưu tiên .json.
    Trả về danh sách Path sắp xếp theo thời gian (2025q1 → 2026q1).
    """
    raw_path = Path(raw_dir)
    if not raw_path.is_dir():
        log.warning(f"Thư mục raw không tồn tại: {raw_path.resolve()}")
        return []
 
    found: dict[tuple[str, str], Path] = {}  # (quý, tên không đuôi) → Path
    for f in raw_path.iterdir():
        m = _QUARTER_FILE_RE.search(f.name)
        if not m:
            continue
        stem = re.sub(r"\.(json|json\.zip)$", "", f.name, flags=re.IGNORECASE)
        k = (m.group(1).lower(), stem)
        if k in found and m.group(2).lower() == "json.zip":
            continue
        found[k] = f
 
    files = [found[k] for k in sorted(found)]
    log.info(f"Tìm thấy {len(files)} file dữ liệu trong {raw_path.resolve()}")
    return files
 
 
def read_json_file(file_path: str | Path) -> dict:
    """Đọc 1 file JSON hoặc JSON.ZIP, trả về dict gốc (chứa 'meta' và 'results')."""
    file_path = Path(file_path)
    if file_path.name.lower().endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zf:
            json_names = [n for n in zf.namelist() if n.endswith(".json")]
            if not json_names:
                raise ValueError(f"Không tìm thấy file .json trong {file_path.name}")
            with zf.open(json_names[0]) as jf:
                return json.load(jf)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
 
 
def _quarter_of(file_path: Path) -> str:
    m = _QUARTER_FILE_RE.search(file_path.name)
    if not m:
        raise ValueError(f"Tên file không có quý: {file_path.name}")
    return m.group(1).lower()


def _flat(prefix: str, d: dict | None) -> dict:
    """{'a': {'b': 1}} → {'prefix_b': 1}; d rỗng/None → {}."""
    return {f"{prefix}_{k}": v for k, v in (d or {}).items()}


def load_and_flatten_quarter(file_path: str | Path) -> Dict[str, pd.DataFrame]:
    """
    Đọc 1 file JSON của openFDA và tách thành 4 DataFrame:
    `reports`, `drugs`, `reactions`, `outcomes`. Mỗi bảng có thêm cột `quarter`.
    """
    file_path = Path(file_path)
    quarter = _quarter_of(file_path)
    data = read_json_file(file_path)
    results = data.get("results")
    if not isinstance(results, list):
        raise ValueError(f"File {file_path.name} thiếu trường 'results' hợp lệ.")

    reports, drugs, reactions, outcomes = [], [], [], []
    n_list_fields = 0

    for r in results:
        rid = r.get(KEY)
        if not rid:
            log.warning(f"{file_path.name}: Bỏ qua 1 bản ghi thiếu {KEY}")
            continue
 
        # --- reports: các trường cấp báo cáo + animal làm phẳng ---
        row = {k: v for k, v in r.items() if k not in _NESTED_REPORT_FIELDS}
        for k, v in row.items():
            if isinstance(v, list):          # vài báo cáo có ngày dạng list → lấy phần tử đầu
                row[k] = v[0] if v else None
                n_list_fields += 1
        a = r.get("animal") or {}
        breed = a.get("breed") or {}
        bc = breed.get("breed_component")
        bc = bc if isinstance(bc, list) else ([] if bc is None else [bc])
        row.update({
            "species": a.get("species"),
            "gender": a.get("gender"),
            "reproductive_status": a.get("reproductive_status"),
            "female_physio_status": a.get("female_animal_physiological_status"),
            **_flat("age", a.get("age")),
            **_flat("weight", a.get("weight")),
            "is_crossbred": breed.get("is_crossbred"),
            "breed_component": ";".join(map(str, bc)),
            **_flat("duration", r.get("duration")),
            "health_prior_condition": (r.get("health_assessment_prior_to_exposure") or {}).get("condition"),
            "health_prior_assessed_by": (r.get("health_assessment_prior_to_exposure") or {}).get("assessed_by"),
            "quarter": quarter,
            "source_file": file_path.name,
        })
        reports.append(row)
 
        # --- reactions / outcomes ---
        for x in r.get("reaction", []) or []:
            reactions.append({KEY: rid, **x, "quarter": quarter, "source_file": file_path.name})
        for x in r.get("outcome", []) or []:
            outcomes.append({KEY: rid, **x, "quarter": quarter, "source_file": file_path.name})
 
        # --- drugs: mỗi thuốc một dòng, hoạt chất nối bằng ';' ---
        for i, d in enumerate(r.get("drug", []) or []):
            drow = {k: v for k, v in d.items()
                    if k not in ("dose", "manufacturer", "active_ingredients",
                                  "frequency_of_administration")}
            drow.update({
                KEY: rid,
                "drug_idx": i,
                **_flat("dose", d.get("dose")),
                **_flat("frequency", d.get("frequency_of_administration")),
                "manufacturer_name": (d.get("manufacturer") or {}).get("name"),
                "active_ingredients": ";".join(
                    n for ai in (d.get("active_ingredients") or []) if (n := ai.get("name"))),
                "quarter": quarter,
                "source_file": file_path.name,
            })
            drugs.append(drow)
 
    if n_list_fields:
        log.warning(f"{file_path.name}: {n_list_fields} trường cấp báo cáo có dạng list, đã lấy phần tử đầu.")
 
    meta = data.get("meta", {})
    log.info(f"{file_path.name}: {len(results):,} báo cáo (last_updated={meta.get('last_updated')}, "
             f"meta.total={meta.get('results', {}).get('total')})")
 
    return {
        "reports": pd.DataFrame(reports),
        "drugs": pd.DataFrame(drugs),
        "reactions": pd.DataFrame(reactions),
        "outcomes": pd.DataFrame(outcomes),
    }
 

EXPECTED_QUARTERS = ("2025q1", "2025q2", "2025q3", "2025q4", "2026q1")

def build_consolidated_tables(
    raw_dir: str | Path = "data/raw",
    processed_dir: str | Path = "data/processed",
    expected_quarters: tuple[str, ...] = EXPECTED_QUARTERS,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Hợp nhất dữ liệu 2025 Q1-Q4 (Train/Historical) và 2026 Q1 (Test), kiểm tra trùng lặp
    `unique_aer_id_number` và lưu 4 file CSV ra `data/processed/`.
 
    Nếu một báo cáo xuất hiện ở nhiều quý, giữ phiên bản ở quý muộn nhất và loại các dòng
    con (drugs/reactions/outcomes) của các phiên bản cũ.
    Trả về (reports, drugs, reactions, outcomes).
    """
    files = discover_raw_files(raw_dir)
    if not files:
        raise FileNotFoundError(f"Không có file dữ liệu trong {Path(raw_dir).resolve()}. "
                                "Chạy `python src/download_data.py` trước.")
 
    parts: dict[str, list[pd.DataFrame]] = {"reports": [], "drugs": [], "reactions": [], "outcomes": []}
    failed = []
    for f in files:
        try:
            quarter_dfs = load_and_flatten_quarter(f)
            for name, df in quarter_dfs.items():
                parts[name].append(df)
        except (zipfile.BadZipFile, json.JSONDecodeError, ValueError, KeyError, OSError) as e:
            log.error(f"Lỗi khi đọc/giải mã file {f.name}: {e}.")
            failed.append(f.name)
            continue

    if failed:
        raise RuntimeError(f"Không đọc được {len(failed)} file: {failed}")
    if not parts["reports"]:
        raise RuntimeError("Không đọc được dữ liệu hợp lệ từ bất kỳ file nào trong data/raw.")

    loaded = {q for df in parts["reports"] if "quarter" in df.columns for q in df["quarter"].unique()}
    missing = set(expected_quarters) - loaded
    if missing:
        raise RuntimeError(f"Thiếu dữ liệu các quý: {sorted(missing)}")

    tables = {name: pd.concat(dfs, ignore_index=True) for name, dfs in parts.items()}

    reports = tables["reports"]
    n_before = len(reports)
    reports = (reports.sort_values(["quarter", "source_file"], kind="stable")
                      .drop_duplicates(subset=KEY, keep="last")
                      .reset_index(drop=True))
    log.info(f"reports: {n_before:,} → {len(reports):,} dòng sau khi loại {n_before - len(reports):,} "
             f"{KEY} trùng giữa các file")

    keep = reports[[KEY, "source_file"]]
    out = {"reports": reports}
    for name in ("drugs", "reactions", "outcomes"):
        before = len(tables[name])
        if before > 0 and KEY in tables[name].columns:
            out[name] = tables[name].merge(keep, on=[KEY, "source_file"], how="inner")
        else:
            out[name] = tables[name]
        log.info(f"{name}: {before:,} → {len(out[name]):,} dòng")

    processed = Path(processed_dir)
    processed.mkdir(parents=True, exist_ok=True)
    for name, df in out.items():
        csv_path = processed / f"{name}.csv"
        tmp_path = csv_path.with_suffix(".csv.tmp")
        try:
            df.to_csv(tmp_path, index=False)
            tmp_path.replace(csv_path)
        except BaseException:
            if tmp_path.exists():
                tmp_path.unlink()
            raise
    log.info(f"Đã lưu 4 bảng vào {processed.resolve()}")
 
    return out["reports"], out["drugs"], out["reactions"], out["outcomes"]


def load_processed(processed_dir: str | Path = "data/processed") -> Dict[str, pd.DataFrame]:
    """Đọc lại 4 bảng CSV, giữ nguyên chuỗi (dtype=str); ép kiểu ở notebook."""
    p = Path(processed_dir)
    return {n: pd.read_csv(p / f"{n}.csv", dtype=str, keep_default_na=True)
            for n in ("reports", "drugs", "reactions", "outcomes")}