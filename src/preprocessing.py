"""
Module: preprocessing.py
Chức năng dự kiến:
- Chuẩn hóa kiểu dữ liệu ngày tháng (`original_receive_date`, `onset_date` từ định dạng YYYYMMDD).
- Quy đổi đơn vị tuổi (`animal.age`) về `age_in_years` và cân nặng (`animal.weight`) về `weight_in_kg`.
- Chuẩn hóa nhãn phân loại không đồng nhất (loài, giới tính, tình trạng sinh sản, đường dùng thuốc).
- Xử lý giá trị khuyết (Missing/Unknown) và lọc ngoại lai (Outliers) theo quy tắc minh bạch.
- Kiểm tra và báo cáo số dòng (row count) trước và sau mỗi bước lọc/gộp theo đúng yêu cầu mục 3.4.
"""

import pandas as pd


def parse_fda_dates(df: pd.DataFrame, date_cols: list[str]) -> pd.DataFrame:
    """
    Chuyển đổi các cột ngày dạng chuỗi 'YYYYMMDD' sang `datetime64[ns]`,
    đồng thời trích xuất `year`, `quarter`, `year_quarter` và `reporting_delay_days`.
    (Skeleton - sẽ triển khai ở Giai đoạn 2).
    """
    raise NotImplementedError("Sẽ triển khai ở Giai đoạn 2 (Preprocessing).")


def standardize_animal_age_and_weight(df: pd.DataFrame) -> pd.DataFrame:
    """
    Quy đổi `animal.age.min`/`max` + `unit` về năm (`age_years`)
    và `animal.weight.min`/`max` + `unit` về kilôgam (`weight_kg`).
    (Skeleton - sẽ triển khai ở Giai đoạn 2).
    """
    raise NotImplementedError("Sẽ triển khai ở Giai đoạn 2 (Preprocessing).")


def log_row_count_change(step_name: str, before_count: int, after_count: int, reason: str = "") -> None:
    """
    Hàm tiện ích in báo cáo thay đổi số dòng sau mỗi bước filtering/merging/dropping
    (bắt buộc theo mục 3.4 của đề cương đồ án).
    """
    diff = after_count - before_count
    pct = (diff / before_count * 100) if before_count > 0 else 0.0
    print(f"[{step_name}] Rows: {before_count:,} -> {after_count:,} (Change: {diff:+,} | {pct:+.2f}%) | Reason: {reason}")

