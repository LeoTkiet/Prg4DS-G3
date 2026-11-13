"""
- Cung cấp bảng màu (palette), style chuẩn hóa cho Matplotlib/Seaborn trên toàn bộ các notebook.
- Đảm bảo mọi biểu đồ đều có đầy đủ Title, Axis Labels, Units, Legend và chú thích kích thước mẫu.
- Cung cấp các hàm vẽ trực quan hóa tái sử dụng cho EDA và phân tích chuyên sâu.
"""

from pathlib import Path
from typing import Dict, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def set_project_plot_style() -> None:
    """
    Thiết lập cấu hình hiển thị biểu đồ thống nhất cho cả nhóm.
    """
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["axes.titlesize"] = 13
    plt.rcParams["axes.labelsize"] = 11
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.3
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "sans-serif"]


def plot_quarterly_volume(
    tables: Dict[str, pd.DataFrame] | pd.DataFrame,
    title: str = "Phân bố số lượng bản ghi của 4 bảng theo quý (2025 Q1 - 2026 Q1)",
    ax: Optional[plt.Axes] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Vẽ biểu đồ cột thể hiện số lượng bản ghi của 4 bảng qua 5 quý.
    Hỗ trợ cả dict gồm 4 DataFrames hoặc 1 DataFrame tổng hợp sẵn.
    """
    if isinstance(tables, dict):
        quarter_df = pd.DataFrame(
            {name: df["quarter"].value_counts() for name, df in tables.items() if "quarter" in df.columns}
        ).sort_index()
    else:
        quarter_df = tables

    fig = None
    if ax is None:
        fig, ax = plt.subplots(figsize=(11, 6))
    else:
        fig = ax.get_figure()

    colors = ["#2b5c8f", "#d95f02", "#7570b3", "#1b9e77"]
    x = np.arange(len(quarter_df.index))
    width = 0.2
    table_names = list(quarter_df.columns)

    for i, col in enumerate(table_names):
        offset = (i - (len(table_names) - 1) / 2) * width
        rects = ax.bar(
            x + offset,
            quarter_df[col],
            width,
            label=f"{col} (n={quarter_df[col].sum():,})",
            color=colors[i % len(colors)],
            alpha=0.9,
            edgecolor="white",
            linewidth=0.8,
        )
        # Ghi số lượng trên đầu mỗi cột
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                f"{int(height / 1000)}k" if height >= 1000 else f"{int(height)}",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
            )

    max_height = float(quarter_df.max().max()) if not quarter_df.empty else 0.0
    ax.set_ylim(0, max_height * 1.15)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Phân vùng quý (Quarter)", fontsize=11, labelpad=8)
    ax.set_ylabel("Số lượng bản ghi (Dòng)", fontsize=11, labelpad=8)
    ax.set_xticks(x)
    ax.set_xticklabels(quarter_df.index, fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(
        title="Bảng dữ liệu",
        frameon=True,
        fontsize=9,
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
    )
    fig.tight_layout()

    return fig, ax


def plot_missing_overview(
    df: pd.DataFrame,
    title: str = "Tỷ lệ giá trị khuyết (Missing Rate) ở các trường dữ liệu",
    top_n: int = 15,
    ax: Optional[plt.Axes] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Vẽ biểu đồ thanh ngang thể hiện tỷ lệ % missing của top_n cột khuyết nhiều nhất.
    Tự động phân màu cảnh báo: Đỏ (>50%), Vàng cam (20-50%), Xanh lam (<=20%).
    """
    missing_pct = (df.isna().sum() / len(df) * 100).sort_values(ascending=False)
    missing_pct = missing_pct[missing_pct > 0].head(top_n)

    fig = None
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = ax.get_figure()

    if missing_pct.empty:
        ax.text(0.5, 0.5, "Không có giá trị khuyết", ha="center", va="center")
        return fig, ax

    colors = [
        "#d95f02" if v > 50 else ("#e6ab02" if v > 20 else "#2b5c8f")
        for v in missing_pct.values[::-1]
    ]

    bars = ax.barh(
        missing_pct.index[::-1],
        missing_pct.values[::-1],
        color=colors,
        alpha=0.9,
        edgecolor="white",
    )
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Tỷ lệ khuyết (%)", fontsize=11, labelpad=8)
    ax.set_ylabel("Tên trường dữ liệu", fontsize=11, labelpad=8)
    ax.set_xlim(0, max(float(missing_pct.max()), 10.0) * 1.15)
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    for bar in bars:
        w = bar.get_width()
        ax.annotate(
            f"{w:.1f}%",
            xy=(w, bar.get_y() + bar.get_height() / 2),
            xytext=(4, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=9,
            fontweight="bold",
        )

    fig.tight_layout()
    return fig, ax



