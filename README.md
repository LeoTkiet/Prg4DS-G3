<<<<<<< Updated upstream
# Phân tích Sự cố Bất lợi Thuốc Thú y (2025) & Dự báo Mức độ Nghiêm trọng năm 2026 (Q1–Q2)
=======
# Phân tích Sự cố Bất lợi Thuốc Thú y (2020–2025) & Dự báo Mức độ Nghiêm trọng năm 2026 (Q1)
>>>>>>> Stashed changes
*(OpenFDA Animal & Veterinary Adverse Events Analysis & Temporal Prediction)*

> **Đồ án cuối kỳ môn học:** CSC17104 – Lập trình cho Khoa học Dữ liệu (Programming for Data Science)  
> **Trường:** Đại học Khoa học Tự nhiên, ĐHQG-HCM (FIT@HCMUS)  
> **Nhóm thực hiện:** Prg4DS-G3

---

## Mục lục
1. [Thành viên nhóm](#1-thành-viên-nhóm)
<<<<<<< Updated upstream
2. [Mô tả bộ dữ liệu & Phạm vi thời gian (2025–2026 Q2)](#2-mô-tả-bộ-dữ-liệu--phạm-vi-thời-gian-20252026-q2)
=======
2. [Mô tả bộ dữ liệu & Phạm vi thời gian (2020–2026 Q1)](#2-mô-tả-bộ-dữ-liệu--phạm-vi-thời-gian-20202026-q1)
>>>>>>> Stashed changes
3. [Cấu trúc thư mục dự án](#3-cấu-trúc-thư-mục-dự-án)
4. [Hệ thống 6 câu hỏi nghiên cứu & Phân công](#4-hệ-thống-6-câu-hỏi-nghiên-cứu--phân-công)
5. [Kế hoạch vận hành chi tiết (Operational Plan)](#5-kế-hoạch-vận-hành-chi-tiết-operational-plan)
6. [Các phát hiện chính (Key Findings)](#6-các-phát-hiện-chính-key-findings)
7. [Hướng dẫn cài đặt và chạy dự án](#7-hướng-dẫn-cài-đặt-và-chạy-dự-án)
8. [Cam kết học thuật & Khai báo sử dụng AI](#8-cam-kết-học-thuật--khai-báo-sử-dụng-ai)

---

## 1. Thành viên nhóm

| Mã TV | Họ và Tên | MSSV | Vai trò chính | Phụ trách câu hỏi | Phản biện chéo (Reviewer) |
|:---:|---|---:|---|---|:---:|
| **M1** | **Đinh Công Khang** | `24120332` | Quản lý cấu trúc Repo, Pipeline tích hợp 4 quý năm 2025, Mô hình Học máy (ML) | **Q1**, **Q6 (ML)** | M3 (Kiệt) |
| **M2** | **Trần Ngô Uyên Nhi** | `24120210` | Chuẩn hóa đơn vị sinh học (tuổi/cân nặng), Phân tích thời gian & đối tượng báo cáo, Chuẩn hóa trực quan hóa | **Q2**, **Q5** | M1 (Khang) |
| **M3** | **Huỳnh Tuấn Kiệt** | `24120356` | Xác minh schema/license, Làm phẳng cấu trúc JSON `drug`/`reaction`/`outcome`, Kiểm định thống kê & độ vững | **Q3**, **Q4** | M2 (Nhi) |

---

<<<<<<< Updated upstream
## 2. Mô tả bộ dữ liệu & Phạm vi thời gian (2025–2026 Q2)
=======
## 2. Mô tả bộ dữ liệu & Phạm vi thời gian (2020–2026 Q1)
>>>>>>> Stashed changes

### 2.1. Thông tin nguồn & Giấy phép
- **Tên bộ dữ liệu:** OpenFDA Animal & Veterinary Adverse Events (`animalandveterinary/event`).
- **Tổ chức thu thập & công bố:** U.S. Food and Drug Administration (FDA) – Center for Veterinary Medicine (CVM).
- **Đường dẫn tải dữ liệu chính thức:** [https://open.fda.gov/data/downloads/](https://open.fda.gov/data/downloads/) (mục **Animal and Veterinary $\rightarrow$ Animal and Veterinary Event**).
- **Giấy phép (License) & Điều khoản:** Creative Commons **CC0 1.0 Universal** (Public Domain Dedication) — xem tại [https://open.fda.gov/license/](https://open.fda.gov/license/) và [https://open.fda.gov/terms/](https://open.fda.gov/terms/).
- **Định dạng gốc:** Các tệp nén `.json.zip` được phân vùng theo từng quý (`YYYYq1`, `YYYYq2`, `YYYYq3`, `YYYYq4`), bên trong có cấu trúc JSON lồng nhau sâu (`meta` và mảng `results[]`).

<<<<<<< Updated upstream
### 2.2. Phạm vi dữ liệu: 4 quý năm 2025 và Kiểm thử 2026 (Q1–Q2)
Phạm vi phân tích dữ liệu: **toàn bộ 4 quý của năm 2025**, dự đoán và kiểm thử trên tập dữ liệu **2026 Q1–Q2**:

1. **Giai đoạn Phân tích & Huấn luyện (2025 Q1 – Q4):**
   - Bao gồm **4 phân vùng quý** (`2025q1` $\rightarrow$ `2025q4`).
   - Sử dụng để trả lời các câu hỏi phân tích chuyên sâu (Q1–Q5) và làm **Tập Huấn luyện + Kiểm định chéo theo thời gian (Training & Temporal Validation Set)** cho bài toán Học máy (Q6).
2. **Giai đoạn Dự báo & Kiểm thử Thực tế (2026 Q1 & Q2):**
   - Bao gồm **2 phân vùng quý** của năm 2026 (`2026q1` và `2026q2`, do hiện tại năm 2026 chưa kết thúc và chưa công bố Q3, Q4).
=======
### 2.2. Chiến lược mở rộng phạm vi dữ liệu: 2020–2025 và Kiểm thử 2026 (Q1)
Thay vì chỉ phân tích một tệp đơn lẻ như trong báo cáo khảo sát sơ bộ (14,826 báo cáo), nhóm mở rộng quy mô lên **chuỗi dữ liệu đa năm từ 2020 đến quý đầu năm 2026**:
1. **Giai đoạn Lịch sử & Huấn luyện (2020 – 2025):**
   - Bao gồm **24 phân vùng quý** (`2020q1` $\rightarrow$ `2025q4`).
   - Sử dụng để khám phá xu hướng dài hạn, trả lời các câu hỏi phân tích chuyên sâu (Q1–Q5), và làm **Tập Huấn luyện + Kiểm định chéo theo thời gian (Training & Temporal Validation Set)** cho bài toán Học máy (Q6).
2. **Giai đoạn Dự báo & Kiểm thử Thực tế (2026 Q1):**
   - Bao gồm **phân vùng quý mới nhất** của năm 2026 (`2026q1`, do hiện tại năm 2026 chưa kết thúc và chưa công bố Q2, Q3, Q4).
>>>>>>> Stashed changes
   - Đóng vai trò là **Tập Kiểm thử Ngoài Thời gian (Out-of-Time Test Set)** hoàn toàn độc lập để:
     - Đối chiếu xem xu hướng phản ứng bất lợi năm 2026 có tiếp nối quy luật của năm 2025 hay xuất hiện biến động mới (data/concept drift).
     - Kiểm tra khách quan độ chính xác của mô hình học máy khi dự đoán cho năm 2026 (đáp ứng chuẩn mực yêu cầu **Time-based Split** tại Mục 3.3 của đề cương đồ án).


### 2.3. Cấu trúc Schema JSON lồng nhau & Thiết kế 4 Bảng Quan hệ Phẳng
Mỗi phần tử trong `results[]` đại diện cho một báo cáo sự kiện (`unique_aer_id_number` / `report_id`). Để tránh bùng nổ tổ hợp (Cartesian explosion) khi một báo cáo chứa nhiều thuốc (`drug[]`), nhiều triệu chứng (`reaction[]`) và nhiều kết cục (`outcome[]`), nhóm thiết kế quy trình **flatten/normalize** thành 4 bảng chuẩn hóa lưu tại `data/processed/`:

| Bảng chuẩn hóa | Khóa chính / Khóa ngoại | Các trường thông tin cốt lõi |
|---|---|---|
| **`reports.parquet`** | `unique_aer_id_number` (PK) | `original_receive_date`, `onset_date`, `year`, `quarter`, `primary_reporter`, `secondary_reporter`, `type_of_information`, `serious_ae`, `treated_for_ae`, `number_of_animals_affected`, cùng thông tin phẳng hóa từ đối tượng `animal` (`species`, `gender`, `reproductive_status`, `age_years`, `weight_kg`, `breed`) |
| **`drugs.parquet`** | `unique_aer_id_number` (FK) | `active_ingredients` (name, dose), `route`, `dosage_form`, `atc_vet_code`, `manufacturer_name`, `used_according_to_label`, `off_label_use`, `lot_number` |
| **`reactions.parquet`** | `unique_aer_id_number` (FK) | `veddra_term_code`, `veddra_term_name`, `veddra_version`, `number_of_animals_affected`, `accuracy` |
| **`outcomes.parquet`** | `unique_aer_id_number` (FK) | `medical_status` (`Recovered/Normal`, `Died`, `Euthanized`, `Ongoing`, `Unknown`), `number_of_animals_affected` |

### 2.4. Khai báo các công trình/notebook công khai liên quan (Declare Existing Work)
- Tài liệu chính thức của FDA: [openFDA Animal & Veterinary API Documentation](https://open.fda.gov/apis/animalandveterinary/event/).
<<<<<<< Updated upstream
- Khác với các bản thống kê mô tả đơn biến thường gặp trên cổng openFDA (chỉ đếm tần suất top thuốc hoặc top loài riêng lẻ), đồ án của nhóm đi sâu vào: (1) chuẩn hóa đa bảng trên chuỗi thời gian 2025–2026 Q2, (2) kiểm soát biến nhiễu (confounders) và định lượng độ bất định (Odds Ratio, Bootstrap CI), và (3) xây dựng pipeline học máy dự báo vượt thời gian (2025 Q1–Q4 $\rightarrow$ 2026 Q1–Q2) không rò rỉ dữ liệu.

---

### 2.5. Thuật ngữ viết tắt (Abbreviations)

| Viết tắt | Ý nghĩa |
|---|---|
| **AE** | Adverse Event (biến cố/phản ứng bất lợi) |
| **VeDDRA** | Veterinary Dictionary for Drug Related Affairs |
| **CVM** | Center for Veterinary Medicine (thuộc FDA) |
| **FDA** | U.S. Food and Drug Administration |
| **OR** | Odds Ratio (tỷ số chênh) |
| **CI** | Confidence Interval (khoảng tin cậy) |
| **PR-AUC** | Precision-Recall Area Under the Curve |
| **ROC-AUC** | Receiver Operating Characteristic Area Under the Curve |
| **ML** | Machine Learning (học máy) |
| **Q1–Q4** | Quý 1 đến Quý 4 trong năm |
=======
- Khác với các bản thống kê mô tả đơn biến thường gặp trên cổng openFDA (chỉ đếm tần suất top thuốc hoặc top loài riêng lẻ), đồ án của nhóm đi sâu vào: (1) chuẩn hóa đa bảng trên chuỗi thời gian 2020–2026 Q1, (2) kiểm soát biến nhiễu (confounders) và định lượng độ bất định (Odds Ratio, Bootstrap CI), và (3) xây dựng pipeline học máy dự báo vượt thời gian (2020–2025 $\rightarrow$ 2026 Q1) không rò rỉ dữ liệu.
>>>>>>> Stashed changes

---

## 3. Cấu trúc thư mục dự án

Cấu trúc kho lưu trữ tuân thủ nghiêm ngặt **Mục 4 (Deliverables and repository structure)** của hướng dẫn đồ án:

```text
Prg4DS-G3/
├── README.md                              # Mô tả đồ án, câu hỏi, kế hoạch vận hành & hướng dẫn chạy
├── environment.yml                        # Cấu hình môi trường Conda (Python, NumPy, Pandas, Scikit-learn...)
├── LLM_USAGE.md                           # Nhật ký khai báo sử dụng công cụ AI/LLM của từng thành viên
├── LICENSE                                # Giấy phép mã nguồn của kho lưu trữ
├── .gitignore                             # Cấu hình bỏ qua các tệp dữ liệu lớn trong data/raw và data/processed
├── data/
<<<<<<< Updated upstream
│   ├── raw/                               # Chứa các file JSON tải từ openFDA (2025 Q1 - 2026 Q2) [Không commit]
=======
│   ├── raw/                               # Chứa các file JSON/ZIP tải từ openFDA (2020 Q1 - 2026 Q1) [Không commit]
>>>>>>> Stashed changes
│   └── processed/                         # Chứa 4 bảng phẳng đã làm sạch (.parquet/.csv) [Không commit]
├── src/                                   # Các module Python tái sử dụng giữa các notebook
│   ├── __init__.py
│   ├── data_loader.py                     # Đọc JSON đa quý, tách meta/results và flatten thành 4 bảng
│   ├── preprocessing.py                   # Chuẩn hóa ngày, quy đổi đơn vị tuổi/cân nặng, log số dòng
│   ├── features.py                        # Tạo biến dẫn xuất (D3) và chia tập dữ liệu theo thời gian (2025 Q1-Q4 vs 2026 Q1-Q2)
│   └── visualization.py                   # Thiết lập style biểu đồ thống nhất cho cả nhóm
├── notebooks/
│   ├── 01_collection_exploration.ipynb    # Mục 3.1 (Data Collection) & Mục 3.2 (Data Exploration)
│   ├── 02_analysis.ipynb                  # Mục 3.3 & 3.4: Phân tích 5 câu hỏi Non-ML (Q1 - Q5)
│   └── 03_ml_question.ipynb               # Mục 3.3, 3.4 & 3.5: Câu hỏi ML (Q6: 2025 Q1-Q4 -> 2026 Q1-Q2) & Tổng kết/Reflection
└── slides.pdf                             # Slide thuyết trình cuối kỳ (sẽ cập nhật khi hoàn tất thực nghiệm)
```

---

## 4. Hệ thống 6 câu hỏi nghiên cứu & Phân công

Nhóm gồm $n = 3$ thành viên $\rightarrow$ xây dựng **$2 \times 3 = 6$ câu hỏi nghiên cứu** (5 câu hỏi phân tích chuyên sâu Non-ML và 1 câu hỏi Học máy ML).

### 4.1. Bảng ma trận câu hỏi Non-ML (Q1–Q5) và Tiêu chí độ sâu (D1–D6)
Theo yêu cầu Mục 3.3, mỗi câu hỏi Non-ML phải thỏa mãn **ít nhất 2 tiêu chí** và cả nhóm phải bao phủ **ít nhất 4/6 tiêu chí** (kế hoạch của nhóm bao phủ trọn vẹn **6/6 tiêu chí D1–D6**):
<<<<<<< Updated upstream
- **D1 (Combining data):** Gộp nhiều bảng chuẩn hóa (`reports`, `drugs`, `reactions`, `outcomes`) hoặc gộp 4 phân vùng quý năm 2025, kiểm tra số dòng và khóa không khớp trước/sau khi gộp.
- **D2 (Reshaping & time):** Pivot/melt, gom nhóm theo quý (`2025Q1`–`2026Q2`), cửa sổ trượt (rolling window), so sánh cùng kỳ (period-over-period) và độ trễ thời gian (lags).
=======
- **D1 (Combining data):** Gộp nhiều bảng chuẩn hóa (`reports`, `drugs`, `reactions`, `outcomes`) hoặc gộp chuỗi phân vùng đa năm, kiểm tra số dòng và khóa không khớp trước/sau khi gộp.
- **D2 (Reshaping & time):** Pivot/melt, gom nhóm theo quý (`2020Q1`–`2026Q1`), cửa sổ trượt (rolling window), so sánh cùng kỳ (period-over-period) và độ trễ thời gian (lags).
>>>>>>> Stashed changes
- **D3 (Derived variables):** Tạo biến mới có cơ sở khoa học (`age_years`, `weight_kg`, `life_stage`, `num_drugs` / polypharmacy, `reporting_delay_days`, `has_off_label_use`).
- **D4 (Controlling for a confounder):** Kiểm tra xem quy luật có còn giữ nguyên khi phân tầng theo biến nhiễu thứ ba (loài, nhóm tuổi, người báo cáo, đa trị liệu).
- **D5 (Quantifying uncertainty):** Khoảng tin cậy 95% (Bootstrap CI), kiểm định giả thuyết thống kê ($\chi^2$, Kruskal-Wallis, Mann-Whitney U) và độ lớn hiệu ứng (Cramér's V, Odds Ratio).
- **D6 (Robustness check):** Kiểm tra độ nhạy của kết luận khi thay đổi ngưỡng lọc ngoại lai (outlier threshold), quy tắc xử lý nhóm `'Unknown'` hoặc khung thời gian.

| Mã câu | Chủ sở hữu | Nội dung câu hỏi nghiên cứu & Động lực thực tiễn | D1 | D2 | D3 | D4 | D5 | D6 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
<<<<<<< Updated upstream
| **Q1** | **M1 — Khang** | **Đặc trưng phản ứng theo loài & Xu hướng theo quý (2025–2026 Q2):** Những phản ứng bất lợi (VeDDRA terms) nào chiếm tỷ trọng cao nhất ở Chó, Mèo và các loài khác trong năm 2025, và xu hướng biến động theo quý (kèm dấu hiệu mùa vụ trong phạm vi 1 năm) của chúng diễn biến ra sao khi bước sang nửa đầu năm 2026 (Q1–Q2)?<br>🎯 *Hỗ trợ bác sĩ thú y và hãng dược dự báo nhu cầu giám sát phản ứng phụ theo mùa.* | ✅ | ✅ | | | ✅ | |
| **Q2** | **M2 — Nhi** | **Mức độ nghiêm trọng (`serious_ae`) theo sinh trắc học & Kiểm soát biến nhiễu:** Tỷ lệ sự cố nghiêm trọng và kết cục tử vong trong năm 2025 thay đổi như thế nào theo giai đoạn tuổi (`life_stage`), cân nặng chuẩn hóa (`weight_kg`) và giới tính của vật nuôi sau khi kiểm soát biến nhiễu là **loài** và **số lượng thuốc dùng kèm (`num_drugs`)**?<br>🎯 *Giúp phân tầng rủi ro lâm sàng trước khi kê đơn cho thú non/thú già hoặc thú nhẹ cân.* | | | ✅ | ✅ | ✅ | ✅ |
| **Q3** | **M3 — Kiệt** | **Tương tác Hoạt chất – Phản ứng giữa Safety Issue và Lack of Efficacy:** Các hoạt chất (`active_ingredients`) và đường dùng (`route`) nào có tỷ suất đồng xuất hiện (Reporting Odds Ratio) đặc trưng nhất với từng phản ứng cụ thể, và pattern này khác biệt ra sao giữa nhóm **Safety Issue** và **Lack Of Expected Effectiveness** trong năm 2025?<br>🎯 *Phân biệt nhóm thuốc có nguy cơ độc tính sinh học với nhóm thuốc đang bị giảm hiệu lực/kháng thuốc (như thuốc giun tim, bọ chét).* | ✅ | ✅ | | ✅ | ✅ | |
| **Q4** | **M3 — Kiệt** | **Tác động của dùng thuốc sai nhãn (`off-label`) & Đa trị liệu:** Việc dùng thuốc off-label kết hợp với đa trị liệu (`polypharmacy`) trong năm 2025 có liên hệ như thế nào với mức độ nghiêm trọng (`serious_ae`) và kết cục y khoa (`outcome`) khi đã kiểm soát biến nhiễu là **loài vật nuôi** và **đối tượng báo cáo (`primary_reporter`)**?<br>🎯 *Cung cấp bằng chứng định lượng cảnh báo rủi ro khi dùng thuốc trái nhãn hướng dẫn.* | ✅ | | ✅ | ✅ | | ✅ |
| **Q5** | **M2 — Nhi** | **Hành vi báo cáo & Độ trễ thời gian (`reporting_delay`) theo Đối tượng báo cáo:** Giữa Bác sĩ thú y (`Veterinarian`), Chủ vật nuôi (`Animal Owner`) và Nhân viên y tế khác, có sự khác biệt có ý nghĩa thống kê nào về **độ trễ gửi báo cáo** (`original_receive_date - onset_date`), loại thông tin và tỷ lệ nghiêm trọng qua 4 quý năm 2025 và 2026 Q1–Q2 hay không?<br>🎯 *Giúp cơ quan quản lý hiệu chỉnh độ trễ báo cáo (reporting lag) khi phân tích dữ liệu mới của năm 2026.* | | ✅ | ✅ | | ✅ | ✅ |

### 4.2. Thiết kế Câu hỏi Học máy Q6 (Owner: M1 — Khang)
- **Câu hỏi Q6:** *Dựa trên các đặc trưng sẵn có ngay tại thời điểm tiếp nhận báo cáo từ dữ liệu lịch sử **2025 (Q1–Q4)** (đặc điểm sinh học của vật nuôi, số lượng thuốc, đường dùng, trạng thái dùng đúng nhãn/off-label, hoạt chất chính, đối tượng báo cáo và thời điểm trong năm), mô hình học máy có thể dự đoán chính xác khả năng một báo cáo trong **nửa đầu năm 2026 (Q1 & Q2)** trở thành **sự cố nghiêm trọng (`serious_ae = True`)** ở mức độ nào? Những đặc trưng nào quan trọng nhất và mô hình thường dự đoán sai ở những phân nhóm nào của năm 2026?*
- **Đáp ứng 6 tiêu chuẩn bắt buộc của Mục 3.3 (Requirements for the ML question):**
  1. **User & Chống rò rỉ dữ liệu (Leakage Prevention):** Phục vụ hệ thống phân loại ưu tiên (triage) hồ sơ của FDA CVM. Loại bỏ triệt để các cột hậu nghiệm gây rò rỉ như `outcome` (Died/Euthanized/Recovered), `treated_for_ae` và `duration`.
  2. **Chia tập dữ liệu theo thời gian (Time-based Split):**
     - **Tập Huấn luyện & Kiểm định (Train/Val):** Dữ liệu 4 quý từ **2025 Q1 đến 2025 Q4**.
     - **Tập Kiểm thử Thực tế (Out-of-Time Test):** Dữ liệu **2026 Q1 và 2026 Q2** (đánh giá đúng 1 lần duy nhất).
  3. **Pipeline & So sánh mô hình:** Đóng gói toàn bộ bước Impute/Scale/Encode trong `scikit-learn Pipeline` + `ColumnTransformer`. So sánh **Trivial Baseline** (`DummyClassifier`) với ít nhất 2 mô hình (**Logistic Regression** và **HistGradientBoosting / Random Forest**).
  4. **Cross-validation & Metric:** Tinh chỉnh siêu tham số bằng `TimeSeriesSplit` trong nội bộ **2025 Q1–Q4** (tối đa 3 fold); đánh giá trên tập Test 2026 bằng **PR-AUC**, **ROC-AUC** và **F1-score / Recall**.
  5. **Phân tích lỗi (Error Analysis):** Mổ xẻ False Positives / False Negatives trên tập 2026 Q1–Q2 theo loài, nhóm tuổi, người báo cáo và kiểm tra hiện tượng lệch phân phối (temporal shift) giữa 2025 và 2026.
=======
| **Q1** | **M1 — Khang** | **Đặc trưng phản ứng theo loài & Xu hướng mùa vụ (2020–2026 Q1):** Những phản ứng bất lợi (VeDDRA terms) nào chiếm tỷ trọng cao nhất ở Chó, Mèo và các loài khác trong giai đoạn 2020–2025, và xu hướng biến động theo quý/mùa vụ của chúng diễn biến ra sao khi bước sang quý đầu năm 2026 (Q1)?<br>🎯 *Hỗ trợ bác sĩ thú y và hãng dược dự báo nhu cầu giám sát phản ứng phụ theo mùa.* | ✅ | ✅ | | | ✅ | |
| **Q2** | **M2 — Nhi** | **Mức độ nghiêm trọng (`serious_ae`) theo sinh trắc học & Kiểm soát biến nhiễu:** Tỷ lệ sự cố nghiêm trọng và kết cục tử vong thay đổi như thế nào theo giai đoạn tuổi (`life_stage`), cân nặng chuẩn hóa (`weight_kg`) và giới tính của vật nuôi sau khi kiểm soát biến nhiễu là **loài** và **số lượng thuốc dùng kèm (`num_drugs`)**?<br>🎯 *Giúp phân tầng rủi ro lâm sàng trước khi kê đơn cho thú non/thú già hoặc thú nhẹ cân.* | | | ✅ | ✅ | ✅ | ✅ |
| **Q3** | **M3 — Kiệt** | **Tương tác Hoạt chất – Phản ứng giữa Safety Issue và Lack of Efficacy:** Các hoạt chất (`active_ingredients`) và đường dùng (`route`) nào có tỷ suất đồng xuất hiện (Reporting Odds Ratio) đặc trưng nhất với từng phản ứng cụ thể, và pattern này khác biệt ra sao giữa nhóm **Safety Issue** và **Lack Of Expected Effectiveness** giai đoạn 2020–2025?<br>🎯 *Phân biệt nhóm thuốc có nguy cơ độc tính sinh học với nhóm thuốc đang bị giảm hiệu lực/kháng thuốc (như thuốc giun tim, bọ chét).* | ✅ | ✅ | | ✅ | ✅ | |
| **Q4** | **M3 — Kiệt** | **Tác động của dùng thuốc sai nhãn (`off-label`) & Đa trị liệu:** Việc dùng thuốc off-label kết hợp với đa trị liệu (`polypharmacy`) có liên hệ như thế nào với mức độ nghiêm trọng (`serious_ae`) và kết cục y khoa (`outcome`) khi đã kiểm soát biến nhiễu là **loài vật nuôi** và **đối tượng báo cáo (`primary_reporter`)**?<br>🎯 *Cung cấp bằng chứng định lượng cảnh báo rủi ro khi dùng thuốc trái nhãn hướng dẫn.* | ✅ | | ✅ | ✅ | | ✅ |
| **Q5** | **M2 — Nhi** | **Hành vi báo cáo & Độ trễ thời gian (`reporting_delay`) theo Đối tượng báo cáo:** Giữa Bác sĩ thú y (`Veterinarian`), Chủ vật nuôi (`Animal Owner`) và Nhân viên y tế khác, có sự khác biệt có ý nghĩa thống kê nào về **độ trễ gửi báo cáo** (`original_receive_date - onset_date`), loại thông tin và tỷ lệ nghiêm trọng qua các năm 2020–2026 Q1 hay không?<br>🎯 *Giúp cơ quan quản lý hiệu chỉnh độ trễ báo cáo (reporting lag) khi phân tích dữ liệu mới của năm 2026.* | | ✅ | ✅ | | ✅ | ✅ |

### 4.2. Thiết kế Câu hỏi Học máy Q6 (Owner: M1 — Khang)
- **Câu hỏi Q6:** *Dựa trên các đặc trưng sẵn có ngay tại thời điểm tiếp nhận báo cáo từ dữ liệu lịch sử **2020–2025** (đặc điểm sinh học của vật nuôi, số lượng thuốc, đường dùng, trạng thái dùng đúng nhãn/off-label, hoạt chất chính, đối tượng báo cáo và thời điểm trong năm), mô hình học máy có thể dự đoán chính xác khả năng một báo cáo trong **quý đầu năm 2026 (Q1)** trở thành **sự cố nghiêm trọng (`serious_ae = True`)** ở mức độ nào? Những đặc trưng nào quan trọng nhất và mô hình thường dự đoán sai ở những phân nhóm nào của năm 2026?*
- **Đáp ứng 6 tiêu chuẩn bắt buộc của Mục 3.3 (Requirements for the ML question):**
  1. **User & Chống rò rỉ dữ liệu (Leakage Prevention):** Phục vụ hệ thống phân loại ưu tiên (triage) hồ sơ của FDA CVM. Loại bỏ triệt để các cột hậu nghiệm gây rò rỉ như `outcome` (Died/Euthanized/Recovered), `treated_for_ae` và `duration`.
  2. **Chia tập dữ liệu theo thời gian (Time-based Split):**
     - **Tập Huấn luyện & Kiểm định (Train/Val):** Dữ liệu 6 năm từ **2020 Q1 đến 2025 Q4**.
     - **Tập Kiểm thử Thực tế (Out-of-Time Test):** Dữ liệu **2026 Q1** (đánh giá đúng 1 lần duy nhất).
  3. **Pipeline & So sánh mô hình:** Đóng gói toàn bộ bước Impute/Scale/Encode trong `scikit-learn Pipeline` + `ColumnTransformer`. So sánh **Trivial Baseline** (`DummyClassifier`) với ít nhất 2 mô hình (**Logistic Regression** và **HistGradientBoosting / Random Forest**).
  4. **Cross-validation & Metric:** Tinh chỉnh siêu tham số bằng `TimeSeriesSplit` chỉ trên tập 2020–2025; đánh giá trên tập Test 2026 bằng **PR-AUC**, **ROC-AUC** và **F1-score / Recall**.
  5. **Phân tích lỗi (Error Analysis):** Mổ xẻ False Positives / False Negatives trên tập 2026 Q1 theo loài, nhóm tuổi, người báo cáo và kiểm tra hiện tượng lệch phân phối (temporal shift) giữa 2020–2025 và 2026.
>>>>>>> Stashed changes
  6. **Giải thích mô hình (Interpretation):** Sử dụng **Permutation Importance** để xác định các yếu tố quyết định mức độ nghiêm trọng.

---

## 5. Kế hoạch vận hành chi tiết (Operational Plan)

Để đảm bảo tiến độ, tính tái lập (reproducibility) và sự phối hợp nhịp nhàng giữa 3 thành viên trên Git/GitHub, nhóm vận hành theo **5 Giai đoạn (Phases)** dưới đây:

```mermaid
flowchart LR
<<<<<<< Updated upstream
    P1["Giai đoạn 1\nThu thập & Flatten JSON\n(2025 Q1 - 2026 Q2)"] --> P2["Giai đoạn 2\nEDA & Tiền xử lý lõi\n(Notebook 01)"]
=======
    P1["Giai đoạn 1\nThu thập & Flatten JSON\n(2020 Q1 - 2026 Q1)"] --> P2["Giai đoạn 2\nEDA & Tiền xử lý lõi\n(Notebook 01)"]
>>>>>>> Stashed changes
    P2 --> P3["Giai đoạn 3\nPhân tích sâu Q1-Q5\n(Notebook 02)"]
    P2 --> P4["Giai đoạn 4\nHuấn luyện 2025 Q1-Q4\n& Test 2026 (Notebook 03)"]
    P3 --> P5["Giai đoạn 5\nTổng hợp, Rà soát chéo\n& Slide thuyết trình"]
    P4 --> P5
```

### Giai đoạn 1: Thu thập Dữ liệu & Xây dựng Pipeline Đọc JSON (Data Ingestion)
<<<<<<< Updated upstream
- **Mục tiêu:** Tải đầy đủ 6 tệp dữ liệu quý từ `2025q1` đến `2026q2` từ [openFDA Downloads](https://open.fda.gov/data/downloads/) vào `data/raw/` và viết hàm làm phẳng trong `src/data_loader.py`.
=======
- **Mục tiêu:** Tải đầy đủ 25 tệp dữ liệu quý từ `2020q1` đến `2026q1` từ [openFDA Downloads](https://open.fda.gov/data/downloads/) vào `data/raw/` và viết hàm làm phẳng trong `src/data_loader.py`.
>>>>>>> Stashed changes
- **Đầu việc cụ thể:**
  - **Kiệt (M3):** Kiểm tra cấu trúc `meta` và `results` của các file qua từng quý (2025 Q1–Q4 và 2026 Q1–Q2; xem schema giữa 2025 và 2026 có thay đổi trường nào không).
  - **Khang (M1):** Viết hàm đọc hàng loạt file `.json` / `.json.zip`, tách thành 4 bảng `reports`, `drugs`, `reactions`, `outcomes` gắn nhãn `year`, `quarter` và kiểm tra trùng lặp `unique_aer_id_number`.
  - **Nhi (M2):** Lập từ điển dữ liệu (Data Dictionary) và kiểm tra tính toàn vẹn của khóa ngoại giữa 4 bảng.

### Giai đoạn 2: Khám phá Dữ liệu (EDA) & Tiền xử lý Chuẩn hóa (`01_collection_exploration.ipynb`)
- **Mục tiêu:** Hoàn thành toàn bộ Mục 3.1 và 3.2 của đề cương và xuất dữ liệu sạch ra `data/processed/`.
- **Đầu việc cụ thể:**
  - **Nhi (M2):** Viết hàm trong `src/preprocessing.py` để quy đổi đơn vị tuổi (`day`, `week`, `month`, `year` $\rightarrow$ `age_years`) và cân nặng (`lb`, `oz`, `g`, `kg` $\rightarrow$ `weight_kg`); khám phá phân phối biến số và ngoại lai.
  - **Kiệt (M3):** Chuẩn hóa các nhãn phân loại (`species`, `gender`, `route`, `type_of_information`), phân tích cơ chế dữ liệu khuyết (Missing Data) và đề xuất phương án xử lý.
<<<<<<< Updated upstream
  - **Khang (M1):** Tổng hợp thống kê quy mô dữ liệu theo từng quý (2025 Q1–Q4 vs. 2026 Q1–Q2), vẽ biểu đồ tổng quan và chốt kế hoạch tiền xử lý.
=======
  - **Khang (M1):** Tổng hợp thống kê quy mô dữ liệu theo từng năm (2020–2025 vs. 2026 Q1), vẽ biểu đồ tổng quan và chốt kế hoạch tiền xử lý.
>>>>>>> Stashed changes

### Giai đoạn 3: Phân tích 5 Câu hỏi Non-ML (`02_analysis.ipynb`)
- **Mục tiêu:** Mỗi thành viên triển khai các câu hỏi mình sở hữu theo đúng cấu trúc Mục 3.4: *(1) Mô tả tiền xử lý bằng Markdown + in số dòng trước/sau mỗi bước lọc/gộp $\rightarrow$ (2) Giải thích phương pháp & tiêu chí D1–D6 $\rightarrow$ (3) Ít nhất 2 biểu đồ chuẩn chỉnh + trả lời bằng số liệu cụ thể & nêu hạn chế*.
- **Phân công thực hiện & Phản biện chéo (Cross-review):**
  - **Q1:** Khang thực hiện $\rightarrow$ Kiệt review.
  - **Q2 & Q5:** Nhi thực hiện $\rightarrow$ Khang review.
  - **Q3 & Q4:** Kiệt thực hiện $\rightarrow$ Nhi review.

### Giai đoạn 4: Xây dựng & Kiểm thử Mô hình Học máy trên năm 2026 (`03_ml_question.ipynb`)
- **Mục tiêu:** Hoàn thành câu hỏi Q6 đáp ứng trọn vẹn 6 yêu cầu ML của đề cương.
- **Đầu việc cụ thể:**
<<<<<<< Updated upstream
  - **Khang (M1):** Xây dựng `src/features.py`, thiết kế `ColumnTransformer` + `Pipeline`, huấn luyện Baseline + Logistic Regression + HistGradientBoosting/RandomForest trên tập **2025 Q1–Q4** với `TimeSeriesSplit`.
  - **Nhi (M2) & Kiệt (M3):** Phối hợp đánh giá mô hình trên tập **Test 2026 (Q1 & Q2)**, thực hiện phân tích lỗi (Error Analysis) theo loài/nhóm tuổi/người báo cáo và chạy **Permutation Importance**.
=======
  - **Khang (M1):** Xây dựng `src/features.py`, thiết kế `ColumnTransformer` + `Pipeline`, huấn luyện Baseline + Logistic Regression + HistGradientBoosting/RandomForest trên tập **2020–2025** với `TimeSeriesSplit`.
  - **Nhi (M2) & Kiệt (M3):** Phối hợp đánh giá mô hình trên tập **Test 2026 (Q1)**, thực hiện phân tích lỗi (Error Analysis) theo loài/nhóm tuổi/người báo cáo và chạy **Permutation Importance**.
>>>>>>> Stashed changes

### Giai đoạn 5: Tổng kết, Đảm bảo Tái lập (Reproducibility) & Chuẩn bị Bảo vệ
- **Mục tiêu:** Hoàn thiện Mục 3.5 (Summary & Individual Reflections), cập nhật `README.md`, `LLM_USAGE.md` và `slides.pdf`.
- **Kiểm tra cuối cùng:** Xóa môi trường tạm, chạy lại toàn bộ 3 notebook theo chế độ **Restart Kernel and Run All** từ đầu đến cuối để đảm bảo không có lỗi đường dẫn hay thứ tự biến.

### Quy ước làm việc với Git & GitHub (Git Workflow)
1. **Nhánh (Branching):** Không commit thẳng lên `main`. Mỗi thành viên tạo nhánh theo cú pháp `feature/<ten>-<cong-viec>` (ví dụ: `feature/kiet-data-loader`, `feature/nhi-eda-numerical`, `feature/khang-q6-ml`).
2. **Thông điệp Commit:** Rõ ràng, có tiền tố công việc (ví dụ: `feat(src): add unit conversion for animal age and weight`, `analysis(q3): compute reporting odds ratio for active ingredients`).
3. **Pull Request & Review:** Mọi PR vào `main` phải được người phản biện chéo kiểm tra (đặc biệt là kiểm tra việc log số dòng `log_row_count_change` và tiêu chuẩn nhãn biểu đồ) trước khi merge.

---

## 6. Các phát hiện chính (Key Findings)

<<<<<<< Updated upstream
> **Trạng thái hiện tại:** Dự án đang ở giai đoạn **Thiết lập kiến trúc & Kế hoạch vận hành**. Dữ liệu đầy đủ giai đoạn **2025 Q1–Q4** và **2026 (Q1–Q2)** sẽ được nạp vào `data/raw/` ở Giai đoạn 1.
=======
> **Trạng thái hiện tại:** Dự án đang ở giai đoạn **Thiết lập kiến trúc & Kế hoạch vận hành**. Dữ liệu đầy đủ giai đoạn **2020–2025** và **2026 (Q1)** sẽ được nạp vào `data/raw/` ở Giai đoạn 1.
>>>>>>> Stashed changes
>
> **Thống kê khảo sát ban đầu (trên 1 phân vùng mẫu 14,826 báo cáo trong báo cáo sơ bộ):**
> - **Cấu trúc lồng nhau:** 14,826 báo cáo chứa tới **27,131 mục thuốc (`drug`)** và **43,448 mục phản ứng (`reaction`)** ($\approx 1.83$ thuốc và $2.93$ phản ứng trên mỗi báo cáo).
> - **Phân bố nhóm thông tin (`type_of_information`):** *Safety Issue* chiếm tỷ trọng lớn nhất (7,309 báo cáo — 49.3%), tiếp theo là *Lack Of Expected Effectiveness* (4,816 báo cáo — 32.5%) và cả hai (1,309 báo cáo — 8.8%).
> - **Mức độ nghiêm trọng (`serious_ae`):** Ghi nhận 5,895 ca nghiêm trọng (`true` — 39.8%), 7,641 ca không nghiêm trọng (`false` — 51.5%) và 1,290 ca khuyết thông tin (`8.7%`).
> - **Phân bố theo loài & người báo cáo:** Chó (*Dog*: 10,515 ca) và Mèo (*Cat*: 2,626 ca) chiếm đa số; người báo cáo chủ yếu gồm Bác sĩ thú y (*Veterinarian*: 4,348), Nhân viên y tế khác (*Other Health Care Professional*: 4,233) và Chủ vật nuôi (*Animal Owner*: 3,532).
> - **Top 5 phản ứng phổ biến nhất trên tập mẫu:** *Vomiting* (1,553), *Lack of efficacy (endoparasite) - heartworm* (1,264), *Lethargy* (1,112), *Lack of efficacy (ectoparasite) - flea* (1,089), và *Diarrhoea* (873).
>
<<<<<<< Updated upstream
> *(Phần này sẽ được cập nhật bằng 3–5 phát hiện định lượng toàn diện trên tập dữ liệu 2025–2026 Q2 sau khi hoàn tất Giai đoạn 3 và Giai đoạn 4).*
=======
> *(Phần này sẽ được cập nhật bằng 3–5 phát hiện định lượng toàn diện trên tập dữ liệu 2020–2026 Q1 sau khi hoàn tất Giai đoạn 3 và Giai đoạn 4).*
>>>>>>> Stashed changes

---

## 7. Hướng dẫn cài đặt và chạy dự án

### 7.1. Yêu cầu hệ thống (Prerequisites)
- Windows 10/11, macOS 12+, hoặc Linux (Ubuntu 20.04+).
- Đã cài **Miniconda** hoặc **Anaconda**. Kiểm tra:
  ```powershell
  conda --version
  ```
- Khuyến nghị: ≥ 4 GB RAM, ≥ 2 GB dung lượng trống và có kết nối Internet để tải gói/dữ liệu.

### 7.2. Tạo và kích hoạt môi trường từ `environment.yml`
Tại thư mục gốc của dự án (`Prg4DS-G3`), chạy:

```powershell
conda env create -f environment.yml
conda activate ds-env
```

<<<<<<< Updated upstream
Kiểm tra môi trường:
```powershell
python --version
python -c "import numpy, pandas, scipy, sklearn, matplotlib, seaborn, pyarrow; print('Môi trường OK')"
```

Nếu môi trường đã tồn tại và cần cập nhật theo `environment.yml`:
```powershell
conda env update -f environment.yml --prune
```

Xóa và tạo lại môi trường khi gặp lỗi:
```powershell
conda deactivate
conda env remove -n ds-env
conda env create -f environment.yml
```

**Lưu ý trên Windows PowerShell:**
```powershell
conda init powershell
# Mở lại terminal. Nếu bị chặn script:
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 7.3. Tải dữ liệu từ openFDA (2025 Q1 – 2026 Q2)
1. Truy cập trang tải dữ liệu chính thức: **[https://open.fda.gov/data/downloads/](https://open.fda.gov/data/downloads/)**.
2. Tìm đến mục **Animal and Veterinary $\rightarrow$ Animal and Veterinary Event**.
3. Tải các tệp `.json.zip` (hoặc giải nén thành `.json`) của:
   - Năm **2025** (đủ 4 quý **Q1–Q4**).
   - Năm **2026** (hiện có **Q1** và **Q2**).
=======
### Bước 2: Tải dữ liệu từ openFDA (2020 Q1 – 2026 Q1)
1. Truy cập trang tải dữ liệu chính thức: **[https://open.fda.gov/data/downloads/](https://open.fda.gov/data/downloads/)**.
2. Tìm đến mục **Animal and Veterinary $\rightarrow$ Animal and Veterinary Event**.
3. Tải các tệp `.json.zip` (hoặc giải nén thành `.json`) của:
   - Các năm **2020, 2021, 2022, 2023, 2024, 2025** (mỗi năm 4 quý Q1–Q4).
   - Năm **2026** (hiện có **Q1**).
>>>>>>> Stashed changes
4. Đặt toàn bộ các tệp đã tải vào thư mục `data/raw/`. *(Lưu ý: `.gitignore` đã được cấu hình để không đẩy các tệp dữ liệu dung lượng lớn này lên GitHub).*

### 7.4. Chạy các Notebook theo đúng thứ tự
Khởi động JupyterLab từ thư mục gốc của dự án:

```powershell
jupyter lab
```

Mở và chạy (**Restart Kernel and Run All**) lần lượt theo thứ tự:
1. [`notebooks/01_collection_exploration.ipynb`](notebooks/01_collection_exploration.ipynb) — Đọc dữ liệu thô từ `data/raw/`, khám phá schema, xử lý làm sạch cơ bản và xuất 4 bảng phẳng vào `data/processed/`.
2. [`notebooks/02_analysis.ipynb`](notebooks/02_analysis.ipynb) — Thực hiện phân tích chuyên sâu, kiểm định thống kê và trực quan hóa cho 5 câu hỏi Non-ML (**Q1 – Q5**).
<<<<<<< Updated upstream
3. [`notebooks/03_ml_question.ipynb`](notebooks/03_ml_question.ipynb) — Huấn luyện mô hình học máy trên giai đoạn **2025 Q1–Q4**, dự đoán và đánh giá độ chính xác trên tập kiểm thử **2026 (Q1–Q2)** (**Q6**), phân tích lỗi, giải thích mô hình và tổng kết đồ án.

### 7.5. Troubleshooting thường gặp
- `conda: command not found` → chưa cài Miniconda/Anaconda hoặc chưa thêm vào PATH.
- `conda activate` không có tác dụng trên PowerShell → chạy `conda init powershell` và mở lại terminal.
- Jupyter không thấy kernel `ds-env` → chạy:
  ```powershell
  python -m ipykernel install --user --name ds-env
  ```
- `ModuleNotFoundError` → kiểm tra đã `conda activate ds-env` chưa, sau đó chạy `conda env update -f environment.yml --prune`.
- Không đọc được dữ liệu → kiểm tra file nằm đúng trong `data/raw/` và đúng 6 quý (2025 Q1–Q4, 2026 Q1–Q2).
=======
3. [`notebooks/03_ml_question.ipynb`](notebooks/03_ml_question.ipynb) — Huấn luyện mô hình học máy trên giai đoạn **2020–2025**, dự đoán và đánh giá độ chính xác trên tập kiểm thử **2026 (Q1)** (**Q6**), phân tích lỗi, giải thích mô hình và tổng kết đồ án.
>>>>>>> Stashed changes

---

## 8. Cam kết học thuật & Khai báo sử dụng AI

- Mọi nguồn dữ liệu, tài liệu tham khảo và đoạn mã tham khảo bên ngoài đều được trích dẫn rõ ràng.
- Mọi phiên sử dụng công cụ AI/LLM của các thành viên trong nhóm đều được ghi chép minh bạch trong tệp [`LLM_USAGE.md`](LLM_USAGE.md) theo đúng quy định tại Mục 6 của đề cương môn học.
- Mã nguồn của kho lưu trữ được phát hành theo giấy phép tại tệp [`LICENSE`](LICENSE); dữ liệu openFDA sử dụng giấy phép CC0 1.0 Universal.
- Để đảm bảo tái lập, các mô hình học máy sử dụng `random_state` cố định và toàn bộ pipeline được đóng gói trong `scikit-learn Pipeline`.
