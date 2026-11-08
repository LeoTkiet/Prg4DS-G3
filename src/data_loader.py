"""
Module: data_loader.py
Chức năng dự kiến:
- Đọc các file JSON (hoặc .json.zip) tải về từ openFDA Animal & Veterinary Adverse Events
<<<<<<< Updated upstream
  giai đoạn 2025 (Q1-Q4) đến 2026 (Q1-Q2) trong thư mục `data/raw/`.
=======
  giai đoạn 2020 (Q1-Q4) đến 2026 (Q1) trong thư mục `data/raw/`.
>>>>>>> Stashed changes
- Trích xuất phần `meta` (để kiểm tra ngày cập nhật, tổng số bản ghi từng quý) và phần `results`.
- Chuẩn hóa thành 4 bảng quan hệ phẳng (Relational Tables) liên kết qua `unique_aer_id_number`:
  1. `reports`: Thông tin cấp báo cáo (id, ngày nhận, ngày khởi phát, người báo cáo, serious_ae, treated_for_ae, type_of_information, animal demographics...).
  2. `drugs`: Danh sách thuốc/hoạt chất lồng nhau (explode từ `drug[]`).
  3. `reactions`: Danh sách phản ứng bất lợi theo thuật ngữ VeDDRA (explode từ `reaction[]`).
  4. `outcomes`: Kết cục y khoa của vật nuôi (explode từ `outcome[]`).
"""

from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd


def discover_raw_files(raw_dir: str | Path = "../data/raw") -> List[Path]:
    """
<<<<<<< Updated upstream
    Tìm tất cả các file JSON / ZIP thuộc giai đoạn 2025 Q1 - 2026 Q2 trong `data/raw/`.
=======
    Tìm tất cả các file JSON / ZIP thuộc giai đoạn 2020 Q1 - 2026 Q1 trong `data/raw/`.
>>>>>>> Stashed changes
    (Skeleton - sẽ triển khai khi có dữ liệu).
    """
    raise NotImplementedError("Sẽ triển khai ở Giai đoạn 1 (Data Collection & Ingestion).")


def load_and_flatten_quarter(file_path: str | Path) -> Dict[str, pd.DataFrame]:
    """
    Đọc 1 file JSON của openFDA và tách thành các DataFrame con (`reports`, `drugs`, `reactions`, `outcomes`).
    (Skeleton - sẽ triển khai ở Giai đoạn 1).
    """
    raise NotImplementedError("Sẽ triển khai ở Giai đoạn 1 (Data Collection & Ingestion).")


def build_consolidated_tables(
    raw_dir: str | Path = "../data/raw",
    processed_dir: str | Path = "../data/processed",
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
<<<<<<< Updated upstream
    Hợp nhất toàn bộ dữ liệu từ 2025 Q1-Q4 (Train/Historical) và 2026 Q1-Q2 (Test),
=======
    Hợp nhất toàn bộ dữ liệu từ 2020-2025 (Train/Historical) và 2026 Q1 (Test),
>>>>>>> Stashed changes
    kiểm tra trùng lặp `unique_aer_id_number` và lưu ra `data/processed/`.
    (Skeleton - sẽ triển khai ở Giai đoạn 1 & 2).
    """
    raise NotImplementedError("Sẽ triển khai ở Giai đoạn 1 & 2.")

