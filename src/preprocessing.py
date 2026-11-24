"""
Module: preprocessing.py
Chức năng:
- Chuẩn hóa kiểu dữ liệu ngày tháng (`original_receive_date`, `onset_date`, `first_exposure_date`, `last_exposure_date` từ định dạng YYYYMMDD).
- Quy đổi đơn vị tuổi (`age_min` + `age_unit`) về `age_years` và cân nặng (`weight_min` + `weight_unit`) về `weight_kg`, kèm lọc ngoại lai theo ngưỡng sinh học từng loài.
- Chuẩn hóa nhãn phân loại không đồng nhất (loài, giới tính, tình trạng sinh sản, đường dùng thuốc, nhãn off-label, kết cục lâm sàng).
- Xử lý giá trị khuyết tường minh & thiếu ẩn (placeholder như `'MSK'`, `'Unknown'`, `'Noinformationsupplied'`), khử trùng lặp bảng `reactions`, và đảm bảo toàn vẹn khóa ngoại (referential integrity).
- Kiểm tra và báo cáo số dòng (row count) trước và sau mỗi bước lọc/gộp theo đúng yêu cầu mục 3.4.
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd


KEY = "unique_aer_id_number"
EXPECTED_QUARTERS = ("2025q1", "2025q2", "2025q3", "2025q4", "2026q1")

# Hệ số quy đổi đơn vị tuổi sang năm (age_years = age_raw / factor)
AGE_UNIT_TO_YEARS: Dict[str, float] = {
    "year": 1.0,
    "years": 1.0,
    "month": 12.0,
    "months": 12.0,
    "week": 52.18,
    "weeks": 52.18,
    "day": 365.25,
    "days": 365.25,
    "hour": 8766.0,
    "hours": 8766.0,
    "minute": 525960.0,
    "minutes": 525960.0,
}

# Hệ số quy đổi đơn vị cân nặng sang kilôgam (weight_kg = weight_raw * factor)
WEIGHT_UNIT_TO_KG: Dict[str, float] = {
    "kilogram": 1.0,
    "kilograms": 1.0,
    "kg": 1.0,
    "pound": 0.45359237,
    "pounds": 0.45359237,
    "lb": 0.45359237,
    "ounce": 0.0283495231,
    "ounces": 0.0283495231,
    "oz": 0.0283495231,
    "gram": 0.001,
    "grams": 0.001,
    "g": 0.001,
}

# Ngưỡng trần sinh học hợp lý theo loài (Plausible Caps — thống nhất với NB01 EDA & NB03)
AGE_PLAUSIBLE_MAX: Dict[str, float] = {
    "Dog": 25.0,
    "Cat": 30.0,
    "Horse": 45.0,
    "Cattle": 30.0,
    "Pig": 25.0,
    "Chicken": 15.0,
    "Goat": 25.0,
    "Sheep": 25.0,
    "Rabbit": 15.0,
    "Ferret": 12.0,
    "Turkey": 15.0,
    "Other": 60.0,
    "Other Mammals": 60.0,
}

WEIGHT_PLAUSIBLE_MAX: Dict[str, float] = {
    "Dog": 100.0,
    "Cat": 20.0,
    "Horse": 1500.0,
    "Cattle": 2000.0,
    "Pig": 500.0,
    "Chicken": 20.0,
    "Goat": 300.0,
    "Sheep": 300.0,
    "Rabbit": 12.0,
    "Ferret": 5.0,
    "Turkey": 30.0,
    "Other": 2000.0,
    "Other Mammals": 2000.0,
}

LIFE_STAGE_CUTOFFS: Dict[str, Tuple[float, float]] = {
    "Dog": (1.0, 7.0),
    "Cat": (1.0, 10.0),
    "Horse": (2.0, 15.0),
    "Cattle": (1.0, 6.0),
    "Pig": (1.0, 5.0),
    "Chicken": (0.5, 2.0),
    "Goat": (1.0, 6.0),
    "Sheep": (1.0, 6.0),
    "Rabbit": (0.5, 5.0),
    "Ferret": (0.5, 5.0),
    "Turkey": (0.5, 2.0),
    "Other": (1.0, 7.0),
    "Other Mammals": (1.0, 7.0),
}

HERD_SPECIES = ("Cattle", "Pig", "Chicken", "Goat", "Sheep", "Turkey")

# Chuỗi thiếu ẩn (implicit placeholders) phát hiện trong EDA Mục 2.4
PLACEHOLDER_RE = re.compile(
    r"^(?:unknown|outcome unknown|unknown medication|msk|not given|not provided|"
    r"requested,?\s*unknown|no\s*information\s*supplied|none|n/a|na|null|<na>|\s*|"
    r".*\(\s*unknown\s*\))$",
    flags=re.IGNORECASE,
)

# Danh sách các cột nhãn boolean cần chuẩn hóa thống nhất về ('true', 'false', missing_label)
REPORT_BOOL_COLS = ("serious_ae", "treated_for_ae", "is_crossbred")
DRUG_BOOL_COLS = (
    "used_according_to_label",
    "previous_exposure_to_drug",
    "previous_ae_to_drug",
    "ae_abated_after_stopping_drug",
    "ae_reappeared_after_resuming_drug",
)

# Cột bị che hoàn toàn ('MSK') hoặc định danh lô nhiễu cần loại khỏi bảng drugs sạch
DRUGS_DROP_COLS = ("brand_name", "manufacturer_name", "lot_number")


def log_row_count_change(
    step_name: str,
    before_count: int,
    after_count: int,
    reason: str = "",
) -> None:
    """
    Hàm tiện ích in báo cáo thay đổi số dòng sau mỗi bước filtering/merging/dropping
    (bắt buộc theo mục 3.4 của đề cương đồ án).
    """
    diff = after_count - before_count
    pct = (diff / before_count * 100) if before_count > 0 else 0.0
    print(
        f"[{step_name}] Rows: {before_count:,} -> {after_count:,} "
        f"(Change: {diff:+,} | {pct:+.2f}%) | Reason: {reason}"
    )


def _strip_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Loại khoảng trắng thừa ở tên cột và các cột chuỗi."""
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]
    for col in out.select_dtypes(include=["object", "string"]).columns:
        out[col] = out[col].map(lambda v: v.strip() if isinstance(v, str) else v)
        out[col] = out[col].replace("", np.nan)
    return out


def _normalize_placeholder_to_nan(series: pd.Series) -> pd.Series:
    """Chuyển các chuỗi thiếu ẩn (Unknown, MSK, Noinformationsupplied, *(Unknown)...) thành NaN."""
    def _clean(val):
        if pd.isna(val):
            return np.nan
        s = str(val).strip()
        if not s or PLACEHOLDER_RE.match(s):
            return np.nan
        return s

    return series.map(_clean)


def _normalize_boolean_series(
    series: pd.Series,
    missing_label: str = "Unknown",
) -> pd.Series:
    """
    Chuẩn hóa thống nhất các cột nhãn boolean về ('true', 'false', missing_label).
    Mọi giá trị khuyết (NaN), placeholder hoặc chuỗi danh sách không hợp lệ
    (như "['true', 'false']" ở is_crossbred) đều được gán về `missing_label`.
    """
    norm = series.astype(str).str.strip().str.lower()
    return pd.Series(
        np.where(norm.isin(["true", "false"]), norm, missing_label),
        index=series.index,
        dtype="object",
    )


def _map_species_group(species: pd.Series) -> pd.Series:
    """Ánh xạ loài thành 3 nhóm lớn phục vụ Q1: Dog, Cat, Other."""
    sl = species.fillna("").astype(str).str.strip().str.lower()
    return pd.Series(
        np.where(sl.eq("dog"), "Dog", np.where(sl.eq("cat"), "Cat", "Other")),
        index=species.index,
        dtype="object",
    )


def assign_life_stage(age_years: pd.Series, species: pd.Series) -> pd.Series:
    """Phân tầng giai đoạn sống (Junior / Adult / Senior / Unknown) theo ngưỡng từng loài."""
    stage = pd.Series("Unknown", index=age_years.index, dtype="object")
    for sp, (j_max, a_max) in LIFE_STAGE_CUTOFFS.items():
        mask = species.eq(sp) & age_years.notna()
        stage.loc[mask & age_years.lt(j_max)] = "Junior"
        stage.loc[mask & age_years.ge(j_max) & age_years.le(a_max)] = "Adult"
        stage.loc[mask & age_years.gt(a_max)] = "Senior"
    # Với loài không có trong từ điển ngưỡng nhưng có tuổi hợp lệ, dùng ngưỡng mặc định của Other
    known_sp = set(LIFE_STAGE_CUTOFFS.keys())
    other_mask = ~species.isin(known_sp) & age_years.notna()
    j_def, a_def = LIFE_STAGE_CUTOFFS["Other"]
    stage.loc[other_mask & age_years.lt(j_def)] = "Junior"
    stage.loc[other_mask & age_years.ge(j_def) & age_years.le(a_def)] = "Adult"
    stage.loc[other_mask & age_years.gt(a_def)] = "Senior"
    return stage


def parse_fda_dates(
    df: pd.DataFrame,
    date_cols: Iterable[str] = ("original_receive_date", "onset_date"),
    max_delay_days: int = 3650,
) -> pd.DataFrame:
    """
    Chuyển đổi các cột ngày dạng chuỗi 'YYYYMMDD' sang `datetime64[ns]` (lưu ở `<col>_dt`),
    đồng thời trích xuất `receive_year`, `receive_month`, `year_quarter`, `receive_week_in_q`
    (1..14 cho các quý 92 ngày) và `reporting_delay_days` (lọc ngoại lai ngoài [0, max_delay_days]).

    Lưu ý: Các chuỗi ngày không đầy đủ (chỉ có năm `YYYY` hoặc `YYYYMM`) được chuyển thành `NaT`
    bằng `errors='coerce'` để tránh suy đoán ngày sai khi tính `reporting_delay_days`.
    """
    out = df.copy()
    for col in date_cols:
        if col in out.columns:
            out[f"{col}_dt"] = pd.to_datetime(out[col], format="%Y%m%d", errors="coerce")

    if "original_receive_date_dt" in out.columns:
        rdt = out["original_receive_date_dt"]
        out["receive_year"] = rdt.dt.year.astype("Int64")
        out["receive_month"] = rdt.dt.month.astype("Int64")
        out["year_quarter"] = pd.Series(
            np.where(
                rdt.notna(),
                rdt.dt.year.astype("Int64").astype(str) + "Q" + rdt.dt.quarter.astype("Int64").astype(str),
                None,
            ),
            index=out.index,
            dtype="object",
        )
        if "quarter" in out.columns:
            q_norm = out["quarter"].astype(str).str.strip().str.lower()
            quarter_starts = {
                q: f"{q[:4]}-{int(q[-1]) * 3 - 2:02d}-01"
                for q in EXPECTED_QUARTERS
            }
            q_start = pd.to_datetime(q_norm.map(quarter_starts), errors="coerce")
            out["receive_week_in_q"] = ((rdt - q_start).dt.days // 7 + 1).astype("Int64")

    if {"original_receive_date_dt", "onset_date_dt"}.issubset(out.columns):
        raw_delay = (out["original_receive_date_dt"] - out["onset_date_dt"]).dt.days
        valid_mask = (raw_delay >= 0) & (raw_delay <= max_delay_days)
        out["reporting_delay_days_raw"] = raw_delay
        out["reporting_delay_days"] = raw_delay.where(valid_mask)

    return out


def standardize_animal_age_and_weight(df: pd.DataFrame) -> pd.DataFrame:
    """
    Quy đổi `age_min` + `age_unit` về năm (`age_years`), `weight_min` + `weight_unit`
    về kilôgam (`weight_kg`), áp dụng ngưỡng sinh học theo loài (`AGE_PLAUSIBLE_MAX`,
    `WEIGHT_PLAUSIBLE_MAX`) và gán nhãn `life_stage`.
    """
    out = df.copy()
    species = out["species"].fillna("Other") if "species" in out.columns else pd.Series("Other", index=out.index)

    if {"age_min", "age_unit"}.issubset(out.columns):
        age_raw = pd.to_numeric(out["age_min"], errors="coerce")
        age_factor = out["age_unit"].astype(str).str.strip().str.lower().map(AGE_UNIT_TO_YEARS)
        age_y = age_raw / age_factor
        age_cap = species.map(AGE_PLAUSIBLE_MAX).fillna(60.0)
        out["age_years_raw"] = age_y
        out["age_years"] = age_y.where((age_y > 0) & (age_y <= age_cap))
        out["life_stage"] = assign_life_stage(out["age_years"], species)

    if {"weight_min", "weight_unit"}.issubset(out.columns):
        weight_raw = pd.to_numeric(out["weight_min"], errors="coerce")
        weight_factor = out["weight_unit"].astype(str).str.strip().str.lower().map(WEIGHT_UNIT_TO_KG)
        weight_k = weight_raw * weight_factor
        weight_cap = species.map(WEIGHT_PLAUSIBLE_MAX).fillna(2000.0)
        out["weight_kg_raw"] = weight_k
        out["weight_kg"] = weight_k.where((weight_k > 0) & (weight_k <= weight_cap))

    return out


def attach_drug_summary(
    reports_df: pd.DataFrame,
    drugs_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Gắn các đặc trưng tổng hợp thuốc cấp báo cáo (`num_drugs`, `has_off_label_use`,
    `route_primary`, `dosage_form_primary`, `top_active_ingredients`) vào `reports_df`
    mà không chạy lại toàn bộ bước làm sạch `reports`.
    """
    df = reports_df.copy()
    if drugs_df is None or len(drugs_df) == 0:
        return df

    d_sub = drugs_df[drugs_df[KEY].isin(df[KEY])].copy()
    drug_counts = d_sub.groupby(KEY).size()
    df["num_drugs"] = df[KEY].map(drug_counts).fillna(0).astype("Int64")

    # Cờ off-label cấp báo cáo: có bất kỳ thuốc nào used_according_to_label == 'false' hoặc có off_label_use
    has_off = pd.Series(False, index=d_sub.index)
    if "used_according_to_label" in d_sub.columns:
        has_off |= d_sub["used_according_to_label"].astype(str).str.strip().str.lower().eq("false")
    if "off_label_use" in d_sub.columns:
        has_off |= _normalize_placeholder_to_nan(d_sub["off_label_use"]).notna()
    off_keys = set(d_sub.loc[has_off, KEY].unique())
    df["has_off_label_use"] = df[KEY].isin(off_keys).astype("Int64")

    # Đặc trưng thuốc chính đầu tiên (route_primary, dosage_form_primary, top_active_ingredients)
    for src_col, dst_col in (
        ("route", "route_primary"),
        ("dosage_form", "dosage_form_primary"),
        (
            "active_ingredients_clean" if "active_ingredients_clean" in d_sub.columns else "active_ingredients",
            "top_active_ingredients",
        ),
    ):
        if src_col in d_sub.columns:
            valid_d = d_sub[[KEY, src_col]].copy()
            valid_d[src_col] = _normalize_placeholder_to_nan(valid_d[src_col])
            first_map = valid_d.dropna(subset=[src_col]).drop_duplicates(KEY).set_index(KEY)[src_col]
            df[dst_col] = df[KEY].map(first_map).fillna("Unknown")

    return df


def clean_reports(
    reports_df: pd.DataFrame,
    drugs_df: pd.DataFrame | None = None,
    verbose: bool = True,
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Làm sạch bảng `reports`:
    1. Chuẩn hóa chuỗi, lọc đúng 5 quý (`2025q1`–`2026q1`), lọc bỏ báo cáo trên người (`Human`).
    2. Parse ngày tháng (`parse_fda_dates`) và lọc ngoại lai `reporting_delay_days` ngoài [0, 3650].
    3. Chuẩn hóa sinh trắc học (`age_years`, `weight_kg`, `life_stage`, `gender_clean`, `species_group`).
    4. Ép kiểu số lượng động vật (`Int64`), nhãn `serious` (0/1), `attack_rate` cho đàn gia súc.
    5. Nếu truyền `drugs_df`, bổ sung biến tổng hợp cấp báo cáo (`num_drugs`, `has_off_label_use`, `route_primary`, `dosage_form_primary`, `top_active_ingredients`).
    """
    stats: Dict[str, int] = {}
    df = _strip_string_columns(reports_df)
    stats["reports_rows_raw"] = len(df)

    # 1. Chuẩn hóa quarter & lọc phạm vi 5 quý nghiên cứu
    if "quarter" in df.columns:
        df["quarter"] = df["quarter"].astype(str).str.strip().str.lower()
        before = len(df)
        df = df[df["quarter"].isin(EXPECTED_QUARTERS)].copy()
        if verbose and len(df) != before:
            log_row_count_change("PREP_reports_quarters", before, len(df), "Giữ phạm vi 5 quý 2025q1–2026q1")

    # 2. Lọc bỏ cá thể người (Human)
    before = len(df)
    human_mask = df["species"].fillna("").astype(str).str.strip().str.lower().eq("human")
    stats["reports_human_dropped"] = int(human_mask.sum())
    df = df.loc[~human_mask].copy()
    if verbose:
        log_row_count_change(
            "PREP_reports_drop_human",
            before,
            len(df),
            "Loại bỏ báo cáo trên người (species == 'Human') để giữ đúng quần thể thú y",
        )

    # 3. Parse ngày tháng & tính độ trễ báo cáo
    df = parse_fda_dates(df, date_cols=("original_receive_date", "onset_date"))
    if "reporting_delay_days_raw" in df.columns:
        raw_d = df["reporting_delay_days_raw"]
        stats["delay_negative_nullified"] = int((raw_d < 0).sum())
        stats["delay_gt_10y_nullified"] = int((raw_d > 3650).sum())
        df = df.drop(columns=["reporting_delay_days_raw"])

    # 4. Quy đổi tuổi, cân nặng & phân tầng life_stage
    df = standardize_animal_age_and_weight(df)
    if "age_years_raw" in df.columns:
        stats["age_outliers_nullified"] = int(df["age_years_raw"].notna().sum() - df["age_years"].notna().sum())
        df = df.drop(columns=["age_years_raw"])
    if "weight_kg_raw" in df.columns:
        stats["weight_outliers_nullified"] = int(df["weight_kg_raw"].notna().sum() - df["weight_kg"].notna().sum())
        df = df.drop(columns=["weight_kg_raw"])

    # 5. Chuẩn hóa biến phân loại, boolean & số nguyên
    df["species"] = df["species"].fillna("Unknown")
    df["species_group"] = _map_species_group(df["species"])
    df["gender_clean"] = df["gender"].where(df["gender"].isin(["Male", "Female"]), "Unknown/Mixed")

    for col in (
        "primary_reporter",
        "reproductive_status",
        "type_of_information",
        "health_prior_condition",
        "female_physio_status",
    ):
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")
    if "female_physio_status" in df.columns:
        df["female_physio_status"] = df["female_physio_status"].str.replace(
            r"(?i)^not applicable$", "Not applicable", regex=True
        )

    for col in REPORT_BOOL_COLS:
        if col in df.columns:
            df[col] = _normalize_boolean_series(df[col], missing_label="Unknown")

    for col in ("number_of_animals_affected", "number_of_animals_treated"):
        if col in df.columns:
            num = pd.to_numeric(df[col], errors="coerce")
            # Chỉ giữ số lượng >= 0
            df[col] = num.where(num >= 0).round().astype("Int64")

    # Nhãn mục tiêu nhị phân serious (0/1/NA)
    if "serious_ae" in df.columns:
        df["serious"] = (
            df["serious_ae"]
            .map({"true": 1, "false": 0})
            .astype("Int64")
        )

    # Biến tỷ lệ ảnh hưởng đàn (Q5) và cờ kiểm định độ vững attack_rate > 1
    if {"number_of_animals_affected", "number_of_animals_treated"}.issubset(df.columns):
        treated = df["number_of_animals_treated"].astype("Float64")
        affected = df["number_of_animals_affected"].astype("Float64")
        is_herd = df["species"].isin(HERD_SPECIES) & (treated > 0)
        df["attack_rate"] = np.where(is_herd, (affected / treated).astype(float), np.nan)
        df["attack_rate_gt_1"] = (df["attack_rate"] > 1.0).fillna(False)
        stats["herd_attack_rate_gt_1"] = int(df["attack_rate_gt_1"].sum())

    # 6. Tổng hợp đặc trưng cấp báo cáo từ bảng drugs (nếu có)
    if drugs_df is not None and len(drugs_df) > 0:
        df = attach_drug_summary(df, drugs_df)

    stats["reports_rows_clean"] = len(df)
    return df.reset_index(drop=True), stats


def clean_drugs(
    drugs_df: pd.DataFrame,
    valid_report_ids: pd.Index | set,
    verbose: bool = True,
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Làm sạch bảng `drugs`:
    1. Đồng bộ khóa ngoại với `reports_clean` (loại các thuốc thuộc ca `Human`).
    2. Loại bỏ cột bị FDA che 100% ('MSK': `brand_name`, `manufacturer_name`) và `lot_number` nhiễu.
    3. Parse ngày phơi nhiễm (`first_exposure_date`, `last_exposure_date`).
    4. Chuẩn hóa đường dùng (`route`), `administered_by`, `dosage_form`, `atc_vet_code`, `used_according_to_label`,
       và tạo `active_ingredients_clean` (chuẩn hóa chuỗi thiếu ẩn thành NaN).
    5. Ép kiểu số học (`drug_idx`, `dose_numerator`, `dose_denominator`, `frequency_value`).
    """
    stats: Dict[str, int] = {}
    df = _strip_string_columns(drugs_df)
    stats["drugs_rows_raw"] = len(df)

    # 1. Cascade lọc theo valid_report_ids
    before = len(df)
    df = df[df[KEY].isin(valid_report_ids)].copy()
    if verbose:
        log_row_count_change(
            "PREP_drugs_cascade_non_human",
            before,
            len(df),
            "Đồng bộ khóa ngoại với bảng reports sau khi loại ca Human",
        )

    # 2. Loại các cột 100% bị che ('MSK') và lot_number
    drop_cols = [c for c in DRUGS_DROP_COLS if c in df.columns]
    stats["drugs_cols_dropped"] = len(drop_cols)
    if drop_cols:
        df = df.drop(columns=drop_cols)

    # 3. Parse ngày phơi nhiễm thuốc
    df = parse_fda_dates(df, date_cols=("first_exposure_date", "last_exposure_date"))

    # 4. Chuẩn hóa danh mục, boolean & thiếu ẩn
    for col in ("route", "administered_by", "dosage_form", "atc_vet_code"):
        if col in df.columns:
            cleaned = _normalize_placeholder_to_nan(df[col])
            df[col] = cleaned.fillna("Unknown")

    for col in DRUG_BOOL_COLS:
        if col in df.columns:
            missing_lbl = "Missing/Unknown" if col == "used_according_to_label" else "Unknown"
            df[col] = _normalize_boolean_series(df[col], missing_label=missing_lbl)

    if "active_ingredients" in df.columns:
        ai_clean = _normalize_placeholder_to_nan(df["active_ingredients"])
        stats["drugs_active_ing_missing_effective"] = int(ai_clean.isna().sum())
        df["active_ingredients_clean"] = ai_clean

    # 5. Ép kiểu số
    if "drug_idx" in df.columns:
        df["drug_idx"] = pd.to_numeric(df["drug_idx"], errors="coerce").astype("Int64")
    for col in ("dose_numerator", "dose_denominator", "frequency_value"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    stats["drugs_rows_clean"] = len(df)
    return df.reset_index(drop=True), stats


def clean_reactions(
    reactions_df: pd.DataFrame,
    valid_report_ids: pd.Index | set,
    verbose: bool = True,
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Làm sạch bảng `reactions`:
    1. Đồng bộ khóa ngoại với `reports_clean`.
    2. Loại bỏ các dòng trùng lặp hoàn toàn (579 dòng trên dữ liệu thô ở EDA Mục 2.1.4; sau cascade còn 570 dòng bị loại ở bước này).
    3. Khử trùng lặp theo cặp `(unique_aer_id_number, veddra_term_code)`, giữ bản ghi đầy đủ thông tin nhất.
    4. Chuẩn hóa `accuracy` (`NaN -> 'Unknown'`) và ép kiểu `number_of_animals_affected` (`Int64`).
    """
    stats: Dict[str, int] = {}
    df = _strip_string_columns(reactions_df)
    stats["reactions_rows_raw"] = len(df)

    # 1. Cascade lọc theo valid_report_ids
    before = len(df)
    df = df[df[KEY].isin(valid_report_ids)].copy()
    if verbose:
        log_row_count_change(
            "PREP_reactions_cascade_non_human",
            before,
            len(df),
            "Đồng bộ khóa ngoại với bảng reports sau khi loại ca Human",
        )

    # 2. Loại dòng trùng lặp hoàn toàn
    before = len(df)
    df = df.drop_duplicates().copy()
    stats["reactions_exact_dups_dropped"] = before - len(df)
    if verbose:
        log_row_count_change(
            "PREP_reactions_drop_exact_dups",
            before,
            len(df),
            "Loại bỏ dòng trùng lặp hoàn toàn (tránh thổi phồng tần suất Q1 và ROR Q3)",
        )

    # 3. Khử trùng theo cặp (unique_aer_id_number, veddra_term_code), ưu tiên dòng đầy đủ nhất
    if {KEY, "veddra_term_code"}.issubset(df.columns):
        before = len(df)
        df["_non_null_score"] = df.notna().sum(axis=1)
        df = (
            df.sort_values("_non_null_score", ascending=False, kind="stable")
            .drop_duplicates(subset=[KEY, "veddra_term_code"], keep="first")
            .drop(columns=["_non_null_score"])
            .copy()
        )
        stats["reactions_key_dups_dropped"] = before - len(df)
        if verbose:
            log_row_count_change(
                "PREP_reactions_dedup_report_term",
                before,
                len(df),
                "Khử trùng lặp cặp (unique_aer_id_number, veddra_term_code), giữ bản ghi đầy đủ nhất",
            )

    # 4. Chuẩn hóa nhãn & ép kiểu
    if "accuracy" in df.columns:
        df["accuracy"] = _normalize_placeholder_to_nan(df["accuracy"]).fillna("Unknown")
    if "number_of_animals_affected" in df.columns:
        num = pd.to_numeric(df["number_of_animals_affected"], errors="coerce")
        df["number_of_animals_affected"] = num.where(num >= 0).round().astype("Int64")

    stats["reactions_rows_clean"] = len(df)
    return df.reset_index(drop=True), stats


def clean_outcomes(
    outcomes_df: pd.DataFrame,
    valid_report_ids: pd.Index | set,
    verbose: bool = True,
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Làm sạch bảng `outcomes`:
    1. Đồng bộ khóa ngoại với `reports_clean`.
    2. Chuẩn hóa `medical_status` (giữ rõ `'Outcome Unknown'`, thêm cờ `is_outcome_known`).
    3. Ép kiểu `number_of_animals_affected` sang `Int64`.
    """
    stats: Dict[str, int] = {}
    df = _strip_string_columns(outcomes_df)
    stats["outcomes_rows_raw"] = len(df)

    # 1. Cascade lọc theo valid_report_ids
    before = len(df)
    df = df[df[KEY].isin(valid_report_ids)].copy()
    if verbose:
        log_row_count_change(
            "PREP_outcomes_cascade_non_human",
            before,
            len(df),
            "Đồng bộ khóa ngoại với bảng reports sau khi loại ca Human",
        )

    # 2. Chuẩn hóa medical_status & gắn cờ biết kết cục
    if "medical_status" in df.columns:
        df["medical_status"] = df["medical_status"].fillna("Outcome Unknown")
        unknown_mask = df["medical_status"].str.lower().isin({"outcome unknown", "unknown", ""})
        df.loc[unknown_mask, "medical_status"] = "Outcome Unknown"
        df["is_outcome_known"] = ~unknown_mask
        stats["outcomes_unknown_count"] = int(unknown_mask.sum())

    # 3. Ép kiểu số nguyên
    if "number_of_animals_affected" in df.columns:
        num = pd.to_numeric(df["number_of_animals_affected"], errors="coerce")
        df["number_of_animals_affected"] = num.where(num >= 0).round().astype("Int64")

    stats["outcomes_rows_clean"] = len(df)
    return df.reset_index(drop=True), stats


def run_core_preprocessing(
    tables: Dict[str, pd.DataFrame],
    verbose: bool = True,
) -> Tuple[Dict[str, pd.DataFrame], Dict[str, int]]:
    """
    Chạy trọn bộ pipeline tiền xử lý lõi (Task T14) cho cả 4 bảng:
    `reports`, `drugs`, `reactions`, `outcomes`.
    Trả về `(clean_tables, audit_stats)`.
    """
    audit: Dict[str, int] = {}

    # Bước 1: Làm sạch reports một lần duy nhất (lọc Human, parse ngày, chuẩn hóa sinh trắc học)
    reports_base, s_rep = clean_reports(tables["reports"], drugs_df=None, verbose=verbose)
    valid_ids = set(reports_base[KEY].unique())

    # Bước 2: Làm sạch 3 bảng con đồng bộ theo valid_ids
    drugs_clean, s_drg = clean_drugs(tables["drugs"], valid_ids, verbose=verbose)
    reactions_clean, s_rea = clean_reactions(tables["reactions"], valid_ids, verbose=verbose)
    outcomes_clean, s_out = clean_outcomes(tables["outcomes"], valid_ids, verbose=verbose)

    # Bước 3: Gắn các biến tổng hợp cấp báo cáo từ drugs_clean trực tiếp vào reports_base
    reports_clean = attach_drug_summary(reports_base, drugs_clean)

    for d in (s_rep, s_drg, s_rea, s_out):
        audit.update(d)

    # Kiểm định toàn vẹn sau tiền xử lý
    assert reports_clean[KEY].is_unique, "Khóa chính unique_aer_id_number ở reports_clean bị trùng!"
    for name, child in (
        ("drugs", drugs_clean),
        ("reactions", reactions_clean),
        ("outcomes", outcomes_clean),
    ):
        orphans = int((~child[KEY].isin(reports_clean[KEY])).sum())
        assert orphans == 0, f"{name}_clean còn {orphans} dòng không có báo cáo cha!"

    clean_tables = {
        "reports": reports_clean,
        "drugs": drugs_clean,
        "reactions": reactions_clean,
        "outcomes": outcomes_clean,
    }
    return clean_tables, audit


def save_clean_tables(
    clean_tables: Dict[str, pd.DataFrame],
    output_dir: str | Path = "data/processed/clean",
) -> List[Path]:
    """
    Lưu 4 bảng đã tiền xử lý sạch ra thư mục `output_dir` (mặc định `data/processed/clean/`)
    bằng ghi nguyên tử (atomic write) để giữ nguyên 4 bảng phẳng thô ở `data/processed/`
    phục vụ khả năng tái lập EDA ở NB01 và tương thích ngược với NB02/NB03.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    saved: List[Path] = []
    for name in ("reports", "drugs", "reactions", "outcomes"):
        df = clean_tables[name]
        csv_path = out_path / f"{name}.csv"
        tmp_path = csv_path.with_suffix(".csv.tmp")
        try:
            df.to_csv(tmp_path, index=False)
            tmp_path.replace(csv_path)
        except BaseException:
            if tmp_path.exists():
                tmp_path.unlink()
            raise
        saved.append(csv_path)
    return saved


# Kiểu dữ liệu cố định khi đọc lại 4 bảng sạch nhằm tránh Pandas ép nhầm mã/ngày chuỗi sang float/int
_CLEAN_DTYPES: Dict[str, Dict[str, str]] = {
    "reports": {
        KEY: "string",
        "report_id": "string",
        "original_receive_date": "string",
        "onset_date": "string",
        "quarter": "string",
        "source_file": "string",
        "year_quarter": "string",
        "serious_ae": "string",
        "treated_for_ae": "string",
        "is_crossbred": "string",
        "receive_year": "Int64",
        "receive_month": "Int64",
        "receive_week_in_q": "Int64",
        "number_of_animals_affected": "Int64",
        "number_of_animals_treated": "Int64",
        "serious": "Int64",
        "num_drugs": "Int64",
        "has_off_label_use": "Int64",
    },
    "drugs": {
        KEY: "string",
        "first_exposure_date": "string",
        "last_exposure_date": "string",
        "lot_expiration": "string",
        "manufacturing_date": "string",
        "product_ndc": "string",
        "atc_vet_code": "string",
        "quarter": "string",
        "source_file": "string",
        "used_according_to_label": "string",
        "previous_exposure_to_drug": "string",
        "previous_ae_to_drug": "string",
        "ae_abated_after_stopping_drug": "string",
        "ae_reappeared_after_resuming_drug": "string",
        "drug_idx": "Int64",
    },
    "reactions": {
        KEY: "string",
        "veddra_term_code": "string",
        "veddra_version": "string",
        "quarter": "string",
        "source_file": "string",
        "number_of_animals_affected": "Int64",
    },
    "outcomes": {
        KEY: "string",
        "quarter": "string",
        "source_file": "string",
        "number_of_animals_affected": "Int64",
    },
}


def load_clean_tables(
    clean_dir: str | Path = "data/processed/clean",
) -> Dict[str, pd.DataFrame]:
    """
    Đọc lại 4 bảng đã tiền xử lý sạch từ `data/processed/clean/` với kiểu dữ liệu được khóa rõ ràng:
    - Cột ngày chuẩn hóa (`*_dt`) đọc dạng `datetime64[ns]`.
    - Cột khóa/mã định danh/ngày thô (`unique_aer_id_number`, `report_id`, `original_receive_date`,
      `onset_date`, `veddra_term_code`, `product_ndc`, ...) giữ nguyên kiểu chuỗi (`string`).
    - Cột số nguyên có thể khuyết (`serious`, `num_drugs`, `number_of_animals_*`, ...) giữ kiểu `Int64`.
    """
    p = Path(clean_dir)
    reports = pd.read_csv(
        p / "reports.csv",
        dtype=_CLEAN_DTYPES["reports"],
        parse_dates=["original_receive_date_dt", "onset_date_dt"],
        low_memory=False,
    )
    drugs = pd.read_csv(
        p / "drugs.csv",
        dtype=_CLEAN_DTYPES["drugs"],
        parse_dates=["first_exposure_date_dt", "last_exposure_date_dt"],
        low_memory=False,
    )
    reactions = pd.read_csv(
        p / "reactions.csv",
        dtype=_CLEAN_DTYPES["reactions"],
        low_memory=False,
    )
    outcomes = pd.read_csv(
        p / "outcomes.csv",
        dtype=_CLEAN_DTYPES["outcomes"],
        low_memory=False,
    )
    return {
        "reports": reports,
        "drugs": drugs,
        "reactions": reactions,
        "outcomes": outcomes,
    }
