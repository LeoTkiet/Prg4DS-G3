"""
Module: features.py
Chức năng dự kiến:
- Tạo các biến dẫn xuất (Derived Variables - tiêu chí D3) phục vụ phân tích Q1-Q5.
- Xây dựng ma trận đặc trưng (Feature Matrix X) và biến mục tiêu (Target y) cho bài toán ML (Q6),
  đảm bảo loại bỏ hoàn toàn các biến gây rò rỉ dữ liệu (Data Leakage) như `outcome`, `treated_for_ae`.
- Chia tập dữ liệu theo thời gian (Time-based Split):
  + Tập Huấn luyện & Kiểm định (Train/Val): 2025 Q1 -> 2025 Q4.
  + Tập Kiểm thử thực tế (Out-of-Time Test): 2026 Q1 & Q2.
"""

from typing import Tuple
import pandas as pd


def create_derived_features(
    reports_df: pd.DataFrame,
    drugs_df: pd.DataFrame,
    reactions_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Tổng hợp các biến dẫn xuất cấp báo cáo:
    - `num_drugs` (số lượng thuốc dùng đồng thời / polypharmacy)
    - `num_reactions` (số lượng phản ứng ghi nhận)
    - `has_off_label_use` (có bất kỳ thuốc nào dùng sai nhãn hay không)
    - `reporting_delay_days` (độ trễ từ lúc khởi phát `onset_date` đến `original_receive_date`)
    - `life_stage` (nhóm tuổi chuẩn hóa theo loài)
    (Skeleton - sẽ triển khai ở Giai đoạn 3 & 4).
    """
    raise NotImplementedError("Sẽ triển khai ở Giai đoạn 3 & 4.")


def temporal_train_test_split(
    df: pd.DataFrame,
    date_col: str = "original_receive_date",
    train_start_year: int = 2025,
    train_end_year: int = 2025,
    test_year: int = 2026,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Chia dữ liệu theo mốc thời gian:
    - Train/Validation: 2025 Q1 - Q4
    - Test (Out-of-Time): 2026 (Q1 & Q2)
    (Skeleton - sẽ triển khai ở Giai đoạn 4 cho Q6).
    """
    raise NotImplementedError("Sẽ triển khai ở Giai đoạn 4 (Machine Learning).")

