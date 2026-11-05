"""
Module: visualization.py
Chức năng dự kiến:
- Cung cấp bảng màu (palette), style chuẩn hóa cho Matplotlib/Seaborn trên toàn bộ các notebook.
- Đảm bảo mọi biểu đồ đều có đầy đủ Title, Axis Labels, Units, Legend và chú thích kích thước mẫu (n=...).
"""

import matplotlib.pyplot as plt


def set_project_plot_style() -> None:
    """
    Thiết lập cấu hình hiển thị biểu đồ thống nhất cho cả nhóm.
    """
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["axes.titlesize"] = 13
    plt.rcParams["axes.labelsize"] = 11
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.3

