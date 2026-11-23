# Phân tích Sự cố Bất lợi Thuốc Thú y (2025) & Dự báo Mức độ Nghiêm trọng năm 2026 (Q1)
*(OpenFDA Animal & Veterinary Adverse Events Analysis & Temporal Prediction)*

> **Đồ án cuối kỳ môn học:** CSC17104 – Lập trình cho Khoa học Dữ liệu (Programming for Data Science)  
> **Trường:** Đại học Khoa học Tự nhiên, ĐHQG-HCM (FIT@HCMUS)  
> **Nhóm thực hiện:** Global Ban

---

## Mục lục
1. [Thành viên nhóm](#1-thành-viên-nhóm)
2. [Mô tả bộ dữ liệu & Phạm vi thời gian (2025–2026 Q1)](#2-mô-tả-bộ-dữ-liệu--phạm-vi-thời-gian-20252026-q1)
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
| **M2** | **Trần Ngô Uyên Nhi** | `24120210` | Chuẩn hóa đơn vị sinh học (tuổi/cân nặng), Phân tích sinh trắc học & Dịch tễ đàn vật nuôi (Gia súc, Gia cầm), Chuẩn hóa trực quan hóa | **Q2**, **Q5** | M1 (Khang) |
| **M3** | **Huỳnh Tuấn Kiệt** | `24120356` | Xác minh schema/license, Làm phẳng cấu trúc JSON `drug`/`reaction`/`outcome`, Kiểm định thống kê & độ vững | **Q3**, **Q4** | M2 (Nhi) |

---

## 2. Mô tả bộ dữ liệu & Phạm vi thời gian (2025–2026 Q1)

### 2.1. Xác minh Giấy phép (License), Tác giả & Nguồn gốc (Provenance)
- **Tên bộ dữ liệu:** OpenFDA Animal & Veterinary Adverse Events (`animalandveterinary/event`).
- **Tác giả / Tổ chức thu thập & công bố (Author & Publisher):** **U.S. Food and Drug Administration (FDA) – Center for Veterinary Medicine (CVM)**, trực thuộc Bộ Y tế và Dịch vụ Nhân sinh Hoa Kỳ (U.S. Department of Health and Human Services — HHS). Hệ thống gốc là cơ sở dữ liệu giám sát hậu mại **CVM Adverse Drug Experience (ADE)**, được trích xuất và công bố qua nền tảng dữ liệu mở **openFDA**.
- **Nguồn gốc & Đường dẫn truy cập chính thức (Source & Manifest):**
  - Cổng tải dữ liệu hàng loạt (Bulk Downloads): [https://open.fda.gov/data/downloads/](https://open.fda.gov/data/downloads/) (mục **Animal and Veterinary $\rightarrow$ Animal and Veterinary Event**).
  - Manifest JSON chính thức (chứa danh sách phân vùng, ngày xuất `export_date`, số bản ghi và URL tải trực tiếp): [`https://api.fda.gov/download.json`](https://api.fda.gov/download.json) (khóa `results.animalandveterinary.event`).
  - Tài liệu đặc tả API & Schema: [https://open.fda.gov/apis/animalandveterinary/event/](https://open.fda.gov/apis/animalandveterinary/event/).
- **Xác minh Giấy phép (License Verification — CC0 1.0 Universal):**
  - **Giấy phép:** **Creative Commons CC0 1.0 Universal (Public Domain Dedication)** — xác minh trực tiếp tại [https://open.fda.gov/license/](https://open.fda.gov/license/), trong trường `meta.license` của mọi tệp JSON tải về, và văn bản pháp lý tại [https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/).
  - **Quyền sử dụng:** Dữ liệu thuộc phạm vi công cộng (Public Domain), cho phép sao chép, chỉnh sửa, phân phối và khai thác tự do cho mục đích học thuật/nghiên cứu mà không bị ràng buộc bản quyền.
  - **Điều khoản & Miễn trừ trách nhiệm bắt buộc (Terms & Disclaimer):** Tuân thủ [openFDA Terms of Service](https://open.fda.gov/terms/). Theo trường `meta.disclaimer` trong mỗi tệp dữ liệu: *(1) Không sử dụng dữ liệu openFDA làm căn cứ duy nhất để ra quyết định điều trị thú y hay lâm sàng; (2) FDA không tự động xác minh độc lập nguyên nhân – kết quả của từng báo cáo riêng lẻ; (3) Khi trích dẫn cần ghi rõ nguồn từ openFDA / FDA CVM.*
- **Định dạng gốc:** Các tệp nén `.json.zip` phân vùng theo từng quý (`YYYYq1`–`YYYYq4`), bên trong gồm đối tượng `meta` (chứa `disclaimer`, `license`, `last_updated`, `results.total`) và mảng `results[]` có cấu trúc JSON lồng nhau sâu.

### 2.2. Phương pháp thu thập, Quần thể & Phạm vi thời gian (Collection Method, Population & Period)
- **Phương pháp thu thập dữ liệu (Collection Method — Giám sát Cảnh giác dược Thú y):**
  *(Lưu ý: Khác với đề xuất ban đầu ở giai đoạn tiền khả thi dùng dữ liệu viễn thám/khảo sát thực địa, bộ dữ liệu chính thức của nhóm được thu thập qua hệ thống **Giám sát Cảnh giác dược Thú y — Veterinary Pharmacovigilance** của FDA CVM từ hai kênh chính)*:
  1. **Báo cáo bắt buộc từ nhà sản xuất (Mandatory Reporting — 21 CFR 514.80):** Các hãng dược và nhà tài trợ thuốc thú y được cấp phép (NADA/ANADA) có nghĩa vụ gửi báo cáo sự cố bất lợi về FDA CVM, gồm báo cáo cảnh báo 15 ngày và báo cáo định kỳ, trên biểu mẫu **Form FDA 1932**. Biểu mẫu có thể nộp giấy, qua bảng câu hỏi Rational Questionnaire hoặc qua **FDA Electronic Submissions Gateway (ESG)**. Các trường dữ liệu theo **VICH GL42**, chuẩn bản tin điện tử theo **VICH GL35** (*CVM GFI #214*).
  2. **Báo cáo tự nguyện từ thực tế lâm sàng (Voluntary / Spontaneous Reporting):** Bác sĩ thú y (`Veterinarian`), chủ vật nuôi (`Animal Owner`), người chăn nuôi và nhân viên y tế khác báo cho hãng sản xuất (để hãng chuyển tiếp về FDA) hoặc gửi trực tiếp cho FDA CVM bằng biểu mẫu **Form FDA 1932a**.
  3. **Chuẩn hóa thuật ngữ chuyên ngành:** Trước khi phát hành lên openFDA, các triệu chứng và phản ứng lâm sàng được mã hóa theo từ điển chuẩn quốc tế **VeDDRA** (*Veterinary Dictionary for Drug Regulatory Activities*), và thuốc được ánh xạ theo hệ thống phân loại **ATCvet** của Tổ chức Y tế Thế giới (WHO).
- **Quần thể nghiên cứu & Đơn vị quan sát (Population & Unit of Observation):**
  - **Quần thể mục tiêu (Target Population):** Các trường hợp động vật (thú cưng như Chó, Mèo; ngựa; gia súc, gia cầm và các loài vật nuôi khác) sử dụng thuốc thú y, chế phẩm sinh học hoặc thiết bị thú y (chủ yếu tại Hoa Kỳ hoặc do nhà sản xuất đăng ký với FDA báo cáo) gặp biến cố bất lợi (`Safety Issue`), thiếu hụt hiệu quả mong đợi (`Lack Of Expected Effectiveness`) hoặc lỗi chất lượng sản phẩm (`Product Defect`).
  - **Đơn vị quan sát (Unit of Observation):** Mỗi bản ghi trong `results[]` (định danh bởi khóa chính `unique_aer_id_number`) là **một báo cáo sự kiện bất lợi (Adverse Event Report)**. Một báo cáo thường đại diện cho 1 cá thể bệnh (phổ biến ở thú cưng: Chó, Mèo) nhưng cũng có thể đại diện cho một nhóm/đàn vật nuôi được điều trị cùng lúc (`number_of_animals_affected > 1`, thường gặp ở gia súc, gia cầm, thủy sản).
- **Phạm vi thời gian (Temporal Period — 2025 Q1 đến 2026 Q1):**
  Dù cơ sở dữ liệu lịch sử của openFDA lưu trữ từ năm 1987, đồ án tập trung vào **5 phân vùng quý liên tiếp mới nhất (`2025q1` $\rightarrow$ `2026q1`)** để phản ánh đúng thực trạng thuốc thú y hiện hành:
  1. **Giai đoạn Phân tích & Huấn luyện (2025 Q1 – Q4):**
     - Bao gồm **4 phân vùng quý** (`2025q1`, `2025q2`, `2025q3`, `2025q4`).
     - Sử dụng để trả lời 5 câu hỏi phân tích chuyên sâu (Q1–Q5) và làm **Tập Huấn luyện + Kiểm định chéo theo thời gian (Training & Temporal Validation Set)** cho bài toán Học máy (Q6).
  2. **Giai đoạn Dự báo & Kiểm thử Thực tế (2026 Q1):**
     - Bao gồm **phân vùng quý đầu tiên của năm 2026 (`2026q1`)**.
     - Đóng vai trò là **Tập Kiểm thử Ngoài Thời gian (Out-of-Time Test Set)** hoàn toàn độc lập để:
       - Đối chiếu xem xu hướng phản ứng bất lợi đầu năm 2026 có tiếp nối quy luật năm 2025 hay xuất hiện dịch chuyển phân phối (*data/concept drift*).
       - Đánh giá khách quan khả năng tổng quát hóa của mô hình học máy theo chuẩn **Time-based Split** tại Mục 3.3 của đề cương đồ án.

### 2.3. Các hạn chế và thiên lệch đã biết (Limitations & Known Biases)
Do đặc thù của hệ thống báo cáo cảnh giác dược hậu mại, bộ dữ liệu có **7 hạn chế và thiên lệch cốt lõi** cần luôn được lưu ý khi diễn giải kết quả:
1. **Thiếu mẫu số phơi nhiễm (Lack of Denominator / No Exposure Data):** Dữ liệu chỉ chứa các ca **có xảy ra và được báo cáo sự cố**, hoàn toàn không có tổng số cá thể động vật đã dùng thuốc an toàn hoặc doanh số liều thuốc bán ra. Vì vậy, **không thể tính tỷ lệ mắc bệnh tuyệt đối (incidence rate / absolute risk)**; nhóm chỉ kết luận về tỷ trọng trong tập báo cáo hoặc sử dụng **Tỷ số chênh báo cáo (Reporting Odds Ratio — ROR)**.
2. **Không thiết lập quan hệ nhân quả trực tiếp (No Proof of Causality):** Một báo cáo ghi nhận thuốc $A$ và phản ứng $B$ chỉ phản ánh sự kết hợp về mặt thời gian (*temporal association*), không chứng minh thuốc $A$ gây ra phản ứng $B$. Phản ứng có thể bắt nguồn từ bệnh lý nền, tuổi già, tương tác đa thuốc (*polypharmacy*) hoặc sai sót khi dùng thuốc (*off-label*).
3. **Báo cáo thiếu & Thiên lệch mức độ nghiêm trọng (Under-reporting & Severity/Stimulated Reporting Bias):** Chỉ một phần nhỏ các phản ứng phụ ngoài thực tế được gửi về FDA. Các biến cố nặng (`serious_ae = true`, tử vong), thuốc vừa mới cấp phép (*Weber effect*), hoặc thuốc đang có cảnh báo an toàn từ truyền thông/FDA có xác suất được báo cáo cao hơn hẳn các phản ứng nhẹ thoáng qua.
4. **Thiên lệch theo loài và hành vi người báo cáo (Species & Reporter Bias):** Thú cưng trong gia đình (đặc biệt là Chó và Mèo) được chăm sóc cá thể hóa nên chiếm tỷ trọng áp đảo trong cơ sở dữ liệu so với vật nuôi trang trại. Bên cạnh đó, báo cáo từ Bác sĩ thú y (`Veterinarian`), Chủ vật nuôi (`Animal Owner`) và Hãng dược khác biệt rõ rệt về độ đầy đủ lâm sàng, thuật ngữ mô tả và độ trễ gửi báo cáo (`reporting_delay_days`).
5. **Khử trùng lặp phòng ngừa theo `unique_aer_id_number` & Phân biệt với `report_id` (Precautionary Deduplication & Identifier Distinction):** Về mặt lý thuyết, khi một ca bệnh có thêm thông tin bổ sung (follow-up), hồ sơ có thể được cập nhật lại với cùng mã báo cáo `unique_aer_id_number`. Dù kiểm tra thực tế trên các cặp phân vùng quý liền kề (`2025q1` $\leftrightarrow$ `2025q2`, `2025q4` $\leftrightarrow$ `2026q1`) ghi nhận `0` bản ghi trùng `unique_aer_id_number`, `src/data_loader.py` vẫn thực hiện bước **khử trùng lặp phòng ngừa** theo khóa `unique_aer_id_number` (giữ bản ở quý/file muộn nhất). **Lưu ý quan trọng:** Chỉ khử trùng lặp theo `unique_aer_id_number`, tuyệt đối **không** dedupe theo `report_id`, vì `report_id` là mã số hồ sơ đăng ký thuốc NADA/ANADA (ví dụ: `N141302`, `N141272`) — nhiều ca bệnh độc lập của cùng một thuốc sẽ có chung `report_id` (ví dụ `2025q4` $\leftrightarrow$ `2026q1` có 311 mã `report_id` trùng nhau).
6. **Dữ liệu khuyết không ngẫu nhiên & Đơn vị đo lường hỗn hợp (Missingness & Heterogeneous Units):** Nhiều trường thông tin (`onset_date`, `age`, `weight`, `serious_ae`, `off_label_use`) bị khuyết theo cơ chế phụ thuộc vào người báo cáo hoặc loại thông tin (MAR/MNAR). Ngoài ra, tuổi (`Day`, `Week`, `Month`, `Year`) và cân nặng (`Kilogram`, `Pound`, `Gram`, `Ounce`) được lưu ở nhiều đơn vị khác nhau, bắt buộc phải chuẩn hóa trước khi phân tích.
7. **Độ trễ đăng tải & dữ liệu theo thời điểm tải (Posting Delay & Snapshot):** openFDA cập nhật theo quý và báo cáo có thể trễ 3–6 tháng kể từ lúc FDA nhận; hồ sơ cũng có thể được bổ sung sau đó. Vì vậy phân vùng `2026q1` là ảnh chụp tại thời điểm tải (`meta.last_updated` ghi trong `data/raw/MANIFEST.json`), có thể chưa đầy đủ hoặc thay đổi nếu tải lại về sau, ảnh hưởng đến các phân tích cập nhật mới nhất và tập test của Q6.

### 2.4. Cấu trúc Schema JSON lồng nhau & Thiết kế 4 Bảng Quan hệ Phẳng
Mỗi phần tử trong `results[]` đại diện cho một báo cáo sự kiện (định danh duy nhất bởi `unique_aer_id_number`; không nhầm với `report_id` là mã đăng ký thuốc NADA/ANADA). Để tránh bùng nổ tổ hợp (Cartesian explosion) khi một báo cáo chứa nhiều thuốc (`drug[]`), nhiều triệu chứng (`reaction[]`) và nhiều kết cục (`outcome[]`), nhóm thiết kế quy trình **flatten/normalize** (trong `src/data_loader.py`) thành **4 bảng quan hệ phẳng chuẩn hóa** định dạng `.csv` lưu tại `data/processed/`, bao gồm tổng cộng **77 trường dữ liệu gốc/phẳng hóa**:

| Bảng chuẩn hóa | Khóa liên kết | Quy mô thực tế (5 quý) | Các trường thông tin cốt lõi (khớp 100% schema của `src/data_loader.py`) |
|---|:---:|:---:|---|
| **`reports.csv`** | `unique_aer_id_number` (PK) | **94.412** dòng $\times$ **33** cột | `unique_aer_id_number`, `report_id`, `original_receive_date`, `onset_date`, `primary_reporter`, `secondary_reporter`, `type_of_information`, `serious_ae`, `treated_for_ae`, `foreign_or_domestic`, `time_between_exposure_and_onset`, `number_of_animals_affected`, `number_of_animals_treated`, các trường sinh trắc học phẳng hóa từ `animal` (`species`, `gender`, `reproductive_status`, `female_physio_status`, `breed_component`, `is_crossbred`, `age_min`, `age_max`, `age_unit`, `age_qualifier`, `weight_min`, `weight_max`, `weight_unit`, `weight_qualifier`), `duration_value`, `duration_unit`, `health_prior_condition`, `health_prior_assessed_by`, `quarter`, `source_file` |
| **`drugs.csv`** | `unique_aer_id_number` (FK) | **174.123** dòng $\times$ **31** cột | `drug_idx`, `active_ingredients` (nối bằng `';'`), `brand_name`, `dosage_form`, `route`, `atc_vet_code`, `manufacturer_name`, `used_according_to_label`, `off_label_use`, `lot_number`, `lot_expiration`, `dose_numerator`, `dose_numerator_unit`, `dose_denominator`, `dose_denominator_unit`, `frequency_value`, `frequency_unit`, `first_exposure_date`, `last_exposure_date`, `admin_date`, `admin_interval`, `admin_interval_unit`, `previous_exposure_to_drug`, `previous_ae_to_drug`, `ae_abated_after_stopping_drug`, `ae_reappeared_after_restarting_drug`, `quarter`, `source_file`... |
| **`reactions.csv`** | `unique_aer_id_number` (FK) | **270.244** dòng $\times$ **8** cột | `veddra_term_code`, `veddra_term_name`, `veddra_version`, `number_of_animals_affected`, `accuracy`, `reaction_idx`, `quarter`, `source_file` |
| **`outcomes.csv`** | `unique_aer_id_number` (FK) | **85.143** dòng $\times$ **5** cột | `medical_status` (`Recovered/Normal`, `Died`, `Euthanized`, `Ongoing`, `Outcome Unknown`), `number_of_animals_affected`, `outcome_idx`, `quarter`, `source_file` |

> 📖 **Từ điển dữ liệu hoàn chỉnh:** Xem chi tiết định nghĩa lâm sàng, kiểu dữ liệu, cơ chế khuyết thiếu và danh mục 21 biến dẫn xuất chuẩn hóa tại [Data Dictionary v2 (data/data_dictionary.md)](data/data_dictionary.md).

### 2.5. Khai báo các công trình/notebook công khai liên quan & Điểm khác biệt (Declare Existing Work)

Nhóm đã khảo sát các công trình nghiên cứu, kho mã nguồn và công cụ phân tích công khai liên quan đến bộ dữ liệu **openFDA Animal & Veterinary Adverse Events**:

| STT | Công trình / Kho mã nguồn / Tài liệu công khai | Nội dung & Cách tiếp cận chính | Điểm khác biệt cốt lõi trong đồ án của nhóm **Global Ban** |
|:---:|---|---|---|
| 1 | **Cổng khám phá tương tác chính thức của openFDA**<br>([openFDA Animal & Veterinary Interactive Chart](https://open.fda.gov/apis/animalandveterinary/event/explore-the-api-with-an-interactive-chart/)) | Cung cấp giao diện truy vấn API trực tuyến và biểu đồ cột đếm tần suất đơn biến (Top `animal.species`, Top `primary_reporter`, Top `reaction.veddra_term_name` trên toàn bộ lịch sử). | Đi xa hơn thống kê đếm đơn biến: nhóm thực hiện **chuẩn hóa đa bảng**, quy đổi đơn vị sinh trắc học (`age_years`, `weight_kg`), **kiểm soát biến nhiễu (D4)** và **ước lượng khoảng tin cậy / kiểm định giả thuyết (D5)** thay vì chỉ nhìn tần suất thô. |
| 2 | **Kho mã nguồn hạ tầng, Thư viện AI Skills & Công cụ truy vấn trên GitHub**<br>([`FDA/openfda`](https://github.com/FDA/openfda), [`OpenVet-Projects/VetClaw`](https://github.com/OpenVet-Projects/VetClaw), [`api-evangelist/openfda`](https://github.com/api-evangelist/openfda)) | Tập trung vào pipeline nạp dữ liệu backend (`FDA/openfda` — `animalandveterinarydrugevent`), thư viện kỹ năng (skills) AI thú y có tích hợp SDK client cho openFDA (`OpenVet-Projects/VetClaw`), hoặc đặc tả API/wrapper tra cứu qua REST API (`api-evangelist/openfda`). | Xây dựng **pipeline dữ liệu tái lập hoàn chỉnh** (`src/download_data.py`, `src/data_loader.py`) tải trực tiếp các phân vùng quý từ manifest, kiểm tra toàn vẹn SHA-256, khử trùng lặp phòng ngừa theo `unique_aer_id_number` và chống bùng nổ tổ hợp khi kết nối 4 bảng. |
| 3 | **Nghiên cứu Học máy & XAI trên dữ liệu openFDA CVM**<br>*(Sholehrasa et al., 2025 — [`arXiv:2510.01520`](https://arxiv.org/abs/2510.01520): "Predictive Modeling and Explainable AI for Veterinary Safety Profiles, Residue Assessment, and Health Outcomes Using Real-World Data and Physicochemical Properties")* | Khai thác dữ liệu lịch sử 1987–2025Q1 kết hợp các đặc trưng hóa lý của thuốc trích xuất từ PubChem (khối lượng phân tử, XLogP3, số chất nhận liên kết hydro...) và kỹ thuật lấy mẫu SMOTE-ENN để phân loại kết cục hậu nghiệm (*Death vs. Recovery*). | (1) Tập trung vào **giai đoạn đương đại 2025 Q1–Q4 & kiểm thử vượt thời gian sang 2026 Q1** (*Out-of-Time Validation*) thay vì gộp chung dữ liệu từ 1987 vốn có độ lệch thời đại lớn; (2) Giải bài toán **Triage tại thời điểm tiếp nhận hồ sơ** (dự đoán `serious_ae`), **loại bỏ triệt để rò rỉ dữ liệu hậu nghiệm** (`outcome`, `treated_for_ae`, `duration`). |
| 4 | **Các nghiên cứu Cảnh giác dược thú y chuyên biệt**<br>*(Xu et al., 2019 — Topics in Companion Animal Medicine, 37:100366, [`doi:10.1016/j.tcam.2019.100366`](https://doi.org/10.1016/j.tcam.2019.100366); Farrell et al., 2025 — Frontiers in Veterinary Science, 12:1581490, [`doi:10.3389/fvets.2025.1581490`](https://doi.org/10.3389/fvets.2025.1581490))* | Xu et al. (2019) phân tích dữ liệu openFDA CVM trên Chó và Mèo nhưng tập trung vào 2 hoạt chất trị ký sinh trùng đơn lẻ (*selamectin* và *spinosad*); Farrell et al. (2025) phân tích bất cân xứng các biến cố cơ xương khớp của kháng thể đơn dòng *bedinvetmab* so với 6 thuốc đối chứng trị viêm xương khớp ở chó trên cơ sở dữ liệu **EudraVigilance Veterinary (EVV)** của EMA (2004–2024). | Phân tích **toàn cảnh và đối sánh đa chiều** trên toàn bộ báo cáo openFDA CVM (2025 Q1–2026 Q1): đối chiếu cấu trúc đồng xuất hiện hoạt chất – phản ứng (ROR) giữa *Safety Issue* và *Lack Of Expected Effectiveness* (Q3), đánh giá tác động tương tác *Off-label $\times$ Polypharmacy* (Q4), và phân tích các yếu tố liên quan đến tỷ lệ động vật bị ảnh hưởng trong đàn ở báo cáo gia súc, gia cầm (Q5). |

---

### 2.6. Thuật ngữ viết tắt (Abbreviations)

| Viết tắt | Ý nghĩa |
|---|---|
| **AE** | Adverse Event (biến cố/phản ứng bất lợi) |
| **VeDDRA** | Veterinary Dictionary for Drug Regulatory Activities |
| **CVM** | Center for Veterinary Medicine (thuộc FDA) |
| **FDA** | U.S. Food and Drug Administration |
| **OR** | Odds Ratio (tỷ số chênh) |
| **CI** | Confidence Interval (khoảng tin cậy) |
| **PR-AUC** | Precision-Recall Area Under the Curve |
| **ROC-AUC** | Receiver Operating Characteristic Area Under the Curve |
| **ML** | Machine Learning (học máy) |
| **Q1–Q4** | Quý 1 đến Quý 4 trong năm |

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
│   ├── raw/                               # Chứa các file JSON tải từ openFDA (2025 Q1 - 2026 Q1) [Không commit]
│   ├── processed/                         # Chứa 4 bảng phẳng đã làm sạch (.csv, 77 cột) [Không commit]
│   └── data_dictionary.md                 # Từ điển dữ liệu v2 chi tiết 77 cột và 21 biến dẫn xuất
├── src/                                   # Các module Python tái sử dụng giữa các notebook
│   ├── __init__.py
│   ├── download_data.py                   # Tải dữ liệu tự động từ API manifest, kiểm tra mã băm SHA-256
│   ├── data_loader.py                     # Đọc JSON đa quý, tách meta/results và flatten thành 4 bảng CSV
│   ├── preprocessing.py                   # Chuẩn hóa ngày, quy đổi đơn vị tuổi/cân nặng, log số dòng
│   ├── features.py                        # Tạo biến dẫn xuất (D3) và chia tập dữ liệu theo thời gian (2025 Q1-Q4 vs 2026 Q1)
│   └── visualization.py                   # Thiết lập style biểu đồ thống nhất cho cả nhóm
├── notebooks/
│   ├── 01_collection_exploration.ipynb    # Mục 3.1 & 3.2: Thu thập 5 quý (94.412 báo cáo), EDA & Tiền xử lý dữ liệu lõi
│   ├── 02_analysis.ipynb                  # Mục 3.3 & 3.4: Master Hub tổng hợp 5 câu hỏi Non-ML (Q1 - Q5)
│   │   ├── 02a_analysis_khang.ipynb       # Phân tích sâu Q1 (Species adverse reactions & Seasonal trend) [Đang phát triển]
│   │   ├── 02b_analysis_nhi.ipynb         # Phân tích sâu Q2 (Biometrics & Severity) & Q5 (Livestock attack rate)
│   │   └── 02c_analysis_kiet.ipynb        # Phân tích sâu Q3 (ROR Safety vs. Efficacy) & Q4 (Off-label & Polypharmacy)
│   └── 03_ml_question.ipynb               # Mục 3.3, 3.4 & 3.5: Mô hình Học máy Q6 (Triage phân loại serious_ae 2025 -> 2026) & Tổng kết/Reflection
└── slides.pdf                             # Slide thuyết trình cuối kỳ (sẽ cập nhật khi hoàn tất thực nghiệm)
```

---

## 4. Hệ thống 6 câu hỏi nghiên cứu & Phân công

Nhóm gồm $n = 3$ thành viên $\rightarrow$ xây dựng **$2 \times 3 = 6$ câu hỏi nghiên cứu** (5 câu hỏi phân tích chuyên sâu Non-ML và 1 câu hỏi Học máy ML).

### 4.1. Bảng ma trận câu hỏi Non-ML (Q1–Q5) và Tiêu chí độ sâu (D1–D6)
Theo yêu cầu Mục 3.3, mỗi câu hỏi Non-ML phải thỏa mãn **ít nhất 2 tiêu chí** và cả nhóm phải bao phủ **ít nhất 4/6 tiêu chí** (kế hoạch của nhóm bao phủ trọn vẹn **6/6 tiêu chí D1–D6**):
- **D1 (Combining data):** Gộp nhiều bảng chuẩn hóa (`reports`, `drugs`, `reactions`, `outcomes`) hoặc gộp 4 phân vùng quý năm 2025, kiểm tra số dòng và khóa không khớp trước/sau khi gộp.
- **D2 (Reshaping & time):** Pivot/melt, gom nhóm theo quý (`2025Q1`–`2026Q1`), cửa sổ trượt (rolling window), so sánh cùng kỳ (period-over-period) và độ trễ thời gian (lags).
- **D3 (Derived variables):** Tạo biến mới có cơ sở khoa học (`age_years`, `weight_kg`, `life_stage`, `num_drugs` / polypharmacy, `attack_rate`, `has_off_label_use`).
- **D4 (Controlling for a confounder):** Kiểm tra xem quy luật có còn giữ nguyên khi phân tầng theo biến nhiễu thứ ba (loài, nhóm tuổi, người báo cáo, đa trị liệu).
- **D5 (Quantifying uncertainty):** Khoảng tin cậy 95% (Bootstrap CI), kiểm định giả thuyết thống kê ($\chi^2$, Kruskal-Wallis, Mann-Whitney U) và độ lớn hiệu ứng (Cramér's V, Odds Ratio).
- **D6 (Robustness check):** Kiểm tra độ nhạy của kết luận khi thay đổi ngưỡng lọc ngoại lai (outlier threshold), quy tắc xử lý nhóm `'Unknown'` hoặc khung thời gian.

| Mã câu | Chủ sở hữu | Nội dung câu hỏi nghiên cứu & Động lực thực tiễn | D1 | D2 | D3 | D4 | D5 | D6 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Q1** | **M1 — Khang** | **Đặc trưng phản ứng theo loài & Xu hướng theo quý (2025–2026 Q1):** Những phản ứng bất lợi (VeDDRA terms) nào chiếm tỷ trọng cao nhất ở Chó, Mèo và các loài khác trong năm 2025, và xu hướng biến động theo quý (kèm dấu hiệu mùa vụ trong phạm vi 1 năm) của chúng diễn biến ra sao khi bước sang quý đầu năm 2026 (Q1)?<br>🎯 *Hỗ trợ bác sĩ thú y và hãng dược dự báo nhu cầu giám sát phản ứng phụ theo mùa.* | ✅ | ✅ | | | ✅ | |
| **Q2** | **M2 — Nhi** | **Đặc điểm sinh học & Nguy cơ sự cố nghiêm trọng:** Những đặc điểm sinh học nào (giai đoạn sống, trọng lượng cơ thể, giới tính) có liên quan đến các biến cố bất lợi nghiêm trọng, sau khi đã kiểm soát yếu tố loài và số lượng thuốc sử dụng?<br>🎯 *Giúp bác sĩ thú y và hệ thống triage phân tầng nguy cơ lâm sàng, nhận diện nhóm thú nuôi dễ tổn thương (thú già/non, nhẹ cân) để điều chỉnh liều và theo dõi sát.* | | | ✅ | ✅ | ✅ | ✅ |
| **Q3** | **M3 — Kiệt** | **Tương tác Hoạt chất – Phản ứng giữa Safety Issue và Lack of Efficacy:** Các hoạt chất (`active_ingredients`) và đường dùng (`route`) nào có tỷ suất đồng xuất hiện (Reporting Odds Ratio) đặc trưng nhất với từng phản ứng cụ thể, và pattern này khác biệt ra sao giữa nhóm **Safety Issue** và **Lack Of Expected Effectiveness** trong năm 2025?<br>🎯 *Phân biệt nhóm thuốc có nguy cơ độc tính sinh học với nhóm thuốc đang bị giảm hiệu lực/kháng thuốc (như thuốc giun tim, bọ chét).* | ✅ | ✅ | | ✅ | ✅ | |
| **Q4** | **M3 — Kiệt** | **Tác động của dùng thuốc sai nhãn (`off-label`) & Đa trị liệu:** Việc dùng thuốc off-label kết hợp với đa trị liệu (`polypharmacy`) trong năm 2025 có liên hệ như thế nào với mức độ nghiêm trọng (`serious_ae`) và kết quả lâm sàng (`outcome`) khi đã kiểm soát biến nhiễu là **loài vật nuôi** và **đối tượng báo cáo (`primary_reporter`)**?<br>🎯 *Cung cấp bằng chứng định lượng cảnh báo rủi ro khi dùng thuốc trái nhãn hướng dẫn.* | ✅ | | ✅ | ✅ | | ✅ |
| **Q5** | **M2 — Nhi** | **Tỷ lệ động vật bị ảnh hưởng trong đàn (Attack Rate) ở Gia súc, Gia cầm:** Những yếu tố nào có liên quan đến tỷ lệ động vật bị ảnh hưởng trong tổng số động vật được điều trị ở mỗi đàn?<br>🎯 *Giúp cơ quan thú y trang trại và hãng dược ước lượng tỷ lệ lan rộng (attack rate) của phản ứng bất lợi trong toàn đàn khi áp dụng thuốc hàng loạt trên các loài gia súc, gia cầm.* | ✅ | | ✅ | ✅ | ✅ | ✅ |

### 4.2. Thiết kế Câu hỏi Học máy Q6 (Owner: M1 — Khang)
- **Câu hỏi Q6:** *Dựa trên các đặc trưng sẵn có ngay tại thời điểm tiếp nhận báo cáo từ dữ liệu lịch sử **2025 (Q1–Q4)** (đặc điểm sinh học của vật nuôi, số lượng thuốc, đường dùng, trạng thái dùng đúng nhãn/off-label, hoạt chất chính, đối tượng báo cáo và thời điểm trong năm), mô hình học máy có thể dự đoán chính xác khả năng một báo cáo trong **quý đầu năm 2026 (Q1)** trở thành **sự cố nghiêm trọng (`serious_ae = True`)** ở mức độ nào? Những đặc trưng nào quan trọng nhất và mô hình thường dự đoán sai ở những phân nhóm nào của năm 2026?*
- **Đáp ứng 6 tiêu chuẩn bắt buộc của Mục 3.3 (Requirements for the ML question):**
  1. **User & Chống rò rỉ dữ liệu (Leakage Prevention):** Phục vụ hệ thống phân loại ưu tiên (triage) hồ sơ của FDA CVM. Loại bỏ triệt để các cột hậu nghiệm gây rò rỉ như `outcome` (Died/Euthanized/Recovered), `treated_for_ae` và `duration`.
  2. **Chia tập dữ liệu theo thời gian (Time-based Split):**
     - **Tập Huấn luyện & Kiểm định (Train/Val):** Dữ liệu 4 quý từ **2025 Q1 đến 2025 Q4**.
     - **Tập Kiểm thử Thực tế (Out-of-Time Test):** Dữ liệu **2026 Q1** (đánh giá đúng 1 lần duy nhất).
  3. **Pipeline & So sánh mô hình:** Đóng gói toàn bộ bước Impute/Scale/Encode trong `scikit-learn Pipeline` + `ColumnTransformer`. So sánh **Trivial Baseline** (`DummyClassifier`) với ít nhất 2 mô hình (**Logistic Regression** và **HistGradientBoosting / Random Forest**).
  4. **Cross-validation & Metric:** Tinh chỉnh siêu tham số bằng `TimeSeriesSplit` trong nội bộ **2025 Q1–Q4** (tối đa 3 fold); đánh giá trên tập Test 2026 bằng **PR-AUC**, **ROC-AUC** và **F1-score / Recall**.
  5. **Phân tích lỗi (Error Analysis):** Mổ xẻ False Positives / False Negatives trên tập 2026 Q1 theo loài, nhóm tuổi, người báo cáo và kiểm tra hiện tượng lệch phân phối (temporal shift) giữa 2025 và 2026.
  6. **Giải thích mô hình (Interpretation):** Sử dụng **Permutation Importance** để xác định các yếu tố quyết định mức độ nghiêm trọng.

---

## 5. Kế hoạch vận hành chi tiết (Operational Plan)

Để đảm bảo tiến độ, tính tái lập (reproducibility) và sự phối hợp nhịp nhàng giữa 3 thành viên trên Git/GitHub, nhóm vận hành theo **5 Giai đoạn (Phases)** dưới đây:

```mermaid
flowchart LR
    P1["Giai đoạn 1\nThu thập & Flatten JSON\n(2025 Q1 - 2026 Q1)"] --> P2["Giai đoạn 2\nEDA & Tiền xử lý lõi\n(Notebook 01)"]
    P2 --> P3["Giai đoạn 3\nPhân tích sâu Q1-Q5\n(Notebook 02)"]
    P2 --> P4["Giai đoạn 4\nHuấn luyện 2025 Q1-Q4\n& Test 2026 (Notebook 03)"]
    P3 --> P5["Giai đoạn 5\nTổng hợp, Rà soát chéo\n& Slide thuyết trình"]
    P4 --> P5
```

### Giai đoạn 1: Thu thập Dữ liệu & Xây dựng Pipeline Đọc JSON (Data Ingestion) `[ĐÃ HOÀN THÀNH]`
- **Mục tiêu:** Tải đầy đủ 5 tệp dữ liệu quý từ `2025q1` đến `2026q1` từ [openFDA Downloads](https://open.fda.gov/data/downloads/) vào `data/raw/` và viết hàm làm phẳng trong `src/data_loader.py`.
- **Kết quả thực tế:**
  - Hoàn thiện pipeline tải và kiểm tra SHA-256 (`src/download_data.py`), lưu `MANIFEST.json`.
  - Hoàn thiện `src/data_loader.py`: tách và làm phẳng cấu trúc JSON thành 4 bảng quan hệ với 77 cột dữ liệu gốc (`reports.csv`: 94.412 dòng, `drugs.csv`: 174.123 dòng, `reactions.csv`: 270.244 dòng, `outcomes.csv`: 85.143 dòng), khử trùng lặp theo `unique_aer_id_number` (giữ bản ở quý muộn nhất).
  - Hoàn thành từ điển dữ liệu [Data Dictionary v2](data/data_dictionary.md) chi tiết 77 cột và 21 biến dẫn xuất.

### Giai đoạn 2: Khám phá Dữ liệu (EDA) & Tiền xử lý Chuẩn hóa (`01_collection_exploration.ipynb`) `[ĐÃ HOÀN THÀNH]`
- **Mục tiêu:** Hoàn thành toàn bộ Mục 3.1 và 3.2 của đề cương và xuất dữ liệu sạch ra `data/processed/`.
- **Kết quả thực tế:**
  - Quy đổi và chuẩn hóa thành công các đại lượng sinh trắc học sang hệ SI (`age_years`, `weight_kg`), phân loại `life_stage` và lọc bỏ cá thể `Human`.
  - Phân tích sâu cơ chế dữ liệu khuyết (Missing Data Mechanism): nhận diện cơ chế MAR rõ rệt theo đối tượng báo cáo (`primary_reporter`), bóc tách tình trạng khuyết ẩn (`brand_name`, `manufacturer_name` bị FDA gắn nhãn `'MSK'`, và 30.56% `outcomes` mang giá trị `'Outcome Unknown'`).
  - Xây dựng 21 biến dẫn xuất có cơ sở khoa học phục vụ các câu hỏi nghiên cứu Q1–Q6. Notebook chạy hoàn tất từ đầu đến cuối không lỗi và đã lưu toàn bộ biểu đồ EDA.

### Giai đoạn 3: Phân tích 5 Câu hỏi Non-ML (`02_analysis.ipynb`) `[ĐANG TIẾN HÀNH]`
- **Mục tiêu:** Mỗi thành viên triển khai các câu hỏi mình sở hữu theo đúng cấu trúc Mục 3.4: *(1) Mô tả tiền xử lý bằng Markdown + in số dòng trước/sau mỗi bước lọc/gộp $\rightarrow$ (2) Giải thích phương pháp & tiêu chí D1–D6 $\rightarrow$ (3) Ít nhất 2 biểu đồ chuẩn chỉnh + trả lời bằng số liệu cụ thể & nêu hạn chế*.
- **Phân công thực hiện & Phân tách module:**
  - Để tránh xung đột git khi 3 thành viên cùng commit song song vào một notebook lớn, nhóm áp dụng kiến trúc module:
    - `notebooks/02_analysis.ipynb`: Master Hub tích hợp, dẫn nhập và kết luận chung.
    - `notebooks/02a_analysis_khang.ipynb`: Q1 (Khang phụ trách — Đặc trưng phản ứng theo loài & Xu hướng theo quý).
    - `notebooks/02b_analysis_nhi.ipynb`: Q2 (Đặc điểm sinh học & Nguy cơ) và Q5 (Attack Rate ở vật nuôi đàn) (Nhi phụ trách).
    - `notebooks/02c_analysis_kiet.ipynb`: Q3 (ROR Hoạt chất – Phản ứng) và Q4 (Off-label & Polypharmacy) (Kiệt phụ trách).
  - Phản biện chéo: Q1 do Kiệt review; Q2 & Q5 do Khang review; Q3 & Q4 do Nhi review.

### Giai đoạn 4: Xây dựng & Kiểm thử Mô hình Học máy trên năm 2026 (`03_ml_question.ipynb`) `[ĐÃ HOÀN THÀNH THỰC NGHIỆM]`
- **Mục tiêu:** Hoàn thành câu hỏi Q6 đáp ứng trọn vẹn 6 yêu cầu ML của đề cương theo chuẩn Time-based Split.
- **Kết quả thực tế:**
  - Xây dựng Pipeline chống rò rỉ dữ liệu nghiêm ngặt: loại bỏ toàn bộ thông tin hậu nghiệm (`outcome`, `treated_for_ae`, `duration`).
  - Chia tập theo thời gian: Huấn luyện trên 4 quý 2025 (68.340 mẫu non-human sau làm sạch) với `TimeSeriesSplit` 3-fold; Kiểm thử trên Quý 1/2026 (15.376 mẫu non-human).
  - So sánh mô hình: `HistGradientBoostingClassifier` vượt trội hoàn toàn Trivial Baseline và Logistic Regression (PR-AUC 0.7901 vs 0.4044; ROC-AUC 0.8384).
  - Xác lập ngưỡng phân loại tối ưu $0.365$ từ Out-of-Fold 2025, đạt Recall **82.23%** trên tập Test 2026 Q1.
  - Phân tích tầm quan trọng bằng Permutation Importance và rà soát tính ổn định phân phối (Temporal Stability) hàng tuần.

### Giai đoạn 5: Tổng kết, Đảm bảo Tái lập (Reproducibility) & Chuẩn bị Bảo vệ `[ĐANG TIẾN HÀNH]`
- **Mục tiêu:** Hoàn thiện Mục 3.5 (Summary & Individual Reflections), cập nhật `README.md`, `LLM_USAGE.md` và `slides.pdf`.
- **Kiểm tra cuối cùng:** Rà soát chéo giữa các thành viên, xóa môi trường tạm, kiểm tra khả năng chạy lại trơn tru của toàn bộ pipeline từ thu thập đến ML.

### Quy ước làm việc với Git & GitHub (Git Workflow)
1. **Nhánh (Branching):** Không commit thẳng lên `main`. Mỗi thành viên tạo nhánh theo cú pháp `feature/<ten>-<cong-viec>` (ví dụ: `feature/kiet-data-loader`, `feature/nhi-eda-numerical`, `feature/khang-q6-ml`).
2. **Thông điệp Commit:** Rõ ràng, có tiền tố công việc (ví dụ: `feat(src): add unit conversion for animal age and weight`, `analysis(q3): compute reporting odds ratio for active ingredients`).
3. **Pull Request & Review:** Mọi PR vào `main` phải được người phản biện chéo kiểm tra (đặc biệt là kiểm tra việc log số dòng `log_row_count_change` và tiêu chuẩn nhãn biểu đồ) trước khi merge.

---

## 6. Các phát hiện chính (Key Findings)

Dựa trên toàn bộ cơ sở dữ liệu **94.412 báo cáo sự cố bất lợi** (gồm **174.123** lượt dùng thuốc, **270.244** triệu chứng phản ứng và **85.143** kết cục lâm sàng) xuyên suốt **5 phân vùng quý liên tiếp (2025 Q1 – 2026 Q1)**, nhóm ghi nhận các phát hiện định lượng cốt lõi sau:

### 6.1. Khám phá Dữ liệu (EDA) & Dịch tễ học Cảnh giác dược Thú y
1. **Thiên lệch cơ cấu loài và hành vi báo cáo:**
   - Thú cưng gia đình chiếm tỷ trọng áp đảo trong tổng số báo cáo: **Chó** (*Dog*) chiếm khoảng **65%** và **Mèo** (*Cat*) chiếm khoảng **20%**. Trong khi đó, ở nhóm vật nuôi trang trại, **Bò** (*Cattle*) là loài được báo cáo nhiều nhất.
   - Cơ chế khuyết dữ liệu thể hiện rõ tính chất **MAR (Missing at Random)** theo nhóm người báo cáo (`primary_reporter`): Bác sĩ thú y (*Veterinarian*) cung cấp hồ sơ đầy đủ nhất về mặt sinh trắc học và lâm sàng. Ngược lại, Chủ vật nuôi (*Animal Owner*) bị khuyết trường tuổi ở **26.4%** số ca và khuyết đánh giá mức độ nghiêm trọng (`serious_ae`) ở **13.2%** số ca.
2. **Khuyết thiếu ẩn (Hidden Missingness) & Tính bảo mật thông tin:**
   - **100%** giá trị ở các cột thương hiệu (`brand_name`) và nhà sản xuất (`manufacturer_name`) trong bảng `drugs.csv` bị FDA CVM che giấu dưới nhãn `'MSK'` (Masked) để bảo mật thương mại trong cơ sở dữ liệu công khai. Do đó, các phân tích dược lý bắt buộc phải dựa vào tên hoạt chất chuẩn hóa (`active_ingredients`) hoặc mã phân loại `atc_vet_code`.
   - Bảng kết cục lâm sàng (`outcomes.csv`) ghi nhận tới **30.56%** (26.017 dòng) mang giá trị `'Outcome Unknown'`, đòi hỏi phải xử lý cẩn trọng khi phân tích diễn tiến bệnh lý.
3. **Rủi ro đa trị liệu (Polypharmacy):**
   - Đa số các ca bệnh ghi nhận từ 1 đến 2 loại thuốc đồng thời (trung bình 1.84 thuốc/báo cáo). Tuy nhiên, khi số lượng thuốc sử dụng đồng thời tăng lên $\ge 3$ loại, tỷ lệ phát sinh biến cố bất lợi nghiêm trọng (`serious_ae = True`) tăng vọt rõ rệt, nhấn mạnh tầm quan trọng của việc kiểm soát tương tác thuốc trong thú y.

### 6.2. Dự báo Mức độ Nghiêm trọng & Phân tầng Ưu tiên (ML Q6)
1. **Hiệu năng vượt trội trong dự báo ngoài thời gian (Out-of-Time Generalization):**
   - Trên tập kiểm thử độc lập **2026 Q1** (15.376 ca non-human hoàn chỉnh), mô hình `HistGradientBoostingClassifier` đạt chỉ số **PR-AUC = 0.7901** (tăng vọt gần gấp đôi so với Baseline ngẫu nhiên là **0.4044**; vượt trội hơn Logistic Regression là 0.7281 và Random Forest là 0.7654) và **ROC-AUC = 0.8384**.
2. **Ngưỡng Triage lâm sàng và khả năng bắt giữ ca nguy cấp:**
   - Áp dụng ngưỡng cắt xác suất tối ưu **$0.365$** (được xác định độc lập thông qua kiểm định chéo Out-of-Fold trên dữ liệu năm 2025), mô hình đạt độ nhạy (Recall) **82.23%**, độ chuẩn xác (Precision) **65.18%**, và **F1-score = 0.7272** trên Quý 1/2026.
   - Điều này mang ý nghĩa thực tiễn to lớn cho FDA CVM: hệ thống Triage tự động có khả năng phát hiện sớm và gắn cờ ưu tiên xử lý cho **hơn 82% tổng số ca biến cố nghiêm trọng thực tế** ngay tại thời điểm vừa tiếp nhận hồ sơ mà không bị rò rỉ thông tin hậu nghiệm.
3. **Các yếu tố quyết định mức độ nghiêm trọng (Feature Importance):**
   - Kết quả phân tích Permutation Importance trên tập kiểm thử 2026 Q1 chỉ ra 4 nhóm đặc trưng có ảnh hưởng lớn nhất đến mức độ nghiêm trọng:
     1. **Hoạt chất chính (`top_active_ingredients`):** Khi xáo trộn làm sụt giảm **0.1791** PR-AUC (yếu tố mang tính quyết định cao nhất).
     2. **Đường dùng thuốc chính (`route_primary`):** Làm sụt giảm **0.0591** PR-AUC (các đường tiêm tĩnh mạch/tiêm bắp thường gắn liền với bệnh cảnh nặng hơn đường uống/bôi ngoài da).
     3. **Phân loại bản chất biến cố (`type_of_information`):** Làm sụt giảm **0.0461** PR-AUC.
     4. **Dạng bào chế chính (`dosage_form_primary`):** Làm sụt giảm **0.0151** PR-AUC.
4. **Tính ổn định phân phối theo thời gian (Temporal Stability):**
   - Phân tích chuỗi thời gian số lượng ca nghiêm trọng theo tuần trong Quý 1/2026 dao động ổn định trong khoảng **450–570 ca/tuần**, phản ánh nhịp độ tương đồng với Quý 1/2025. Không phát hiện sự cố dịch chuyển phân phối đột ngột (*concept drift*), chứng minh mô hình có độ bền vững cao khi triển khai giám sát thường quy.

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

### 7.3. Tải dữ liệu từ openFDA và tạo 4 bảng CSV (2025 Q1 – 2026 Q1)

**Bước 1: Tải JSON thô** (chạy tại thư mục gốc, đã `conda activate ds-env`):

```powershell
python src/download_data.py
```

Script đọc danh sách file từ `https://api.fda.gov/download.json`, tải các tệp `.json.zip` của 5 quý `2025q1`–`2026q1`, giải nén vào `data/raw/` và ghi nhật ký `data/raw/MANIFEST.json` (ngày cập nhật, số bản ghi, SHA-256). Các tùy chọn:

```powershell
python src/download_data.py --force                       # tải lại dù file đã có
python src/download_data.py --quarters 2025q1 2025q2      # chỉ tải một số quý
```

Nếu có file tải lỗi, script in danh sách file lỗi và thoát với mã 1; chạy lại lệnh để tải bù (file đã tải xong sẽ được bỏ qua).

**Bước 2: Tạo 4 bảng CSV** (`reports.csv`, `drugs.csv`, `reactions.csv`, `outcomes.csv` trong `data/processed/`). Có hai cách, kết quả như nhau:

- Chạy **Cell 2** của `notebooks/01_collection_exploration.ipynb` (đặt `REBUILD = True` nếu muốn tạo lại), hoặc
- Chạy trực tiếp từ terminal:

```powershell
python -c "import logging; logging.basicConfig(level=logging.INFO); from src.data_loader import build_consolidated_tables; build_consolidated_tables()"
```

Hàm này làm phẳng JSON lồng nhau thành 4 bảng, loại `unique_aer_id_number` trùng giữa các file (giữ bản ở quý muộn nhất), và dừng với lỗi nếu thiếu file hoặc thiếu quý. Các cột ngày/số vẫn là chuỗi, việc ép kiểu làm ở bước tiền xử lý.

> `data/raw/` và `data/processed/` không được commit (xem `.gitignore`), nên mỗi thành viên cần chạy 2 bước trên sau khi clone repo.

### 7.4. Chạy các Notebook theo đúng thứ tự
Khởi động JupyterLab từ thư mục gốc của dự án:

```powershell
jupyter lab
```

Mở và chạy (**Restart Kernel and Run All**) lần lượt theo thứ tự:
1. [`notebooks/01_collection_exploration.ipynb`](notebooks/01_collection_exploration.ipynb) — Đọc dữ liệu thô từ `data/raw/`, khám phá schema, xử lý làm sạch cơ bản, chuẩn hóa sinh trắc học và xuất 4 bảng phẳng vào `data/processed/`.
2. [`notebooks/02_analysis.ipynb`](notebooks/02_analysis.ipynb) (Master Hub) hoặc các notebook phân tích chuyên sâu theo từng nhóm câu hỏi:
   - [`notebooks/02a_analysis_khang.ipynb`](notebooks/02a_analysis_khang.ipynb): Phân tích sâu **Q1** (Phản ứng theo loài & Xu hướng theo quý).
   - [`notebooks/02b_analysis_nhi.ipynb`](notebooks/02b_analysis_nhi.ipynb): Phân tích sâu **Q2** (Đặc điểm sinh học) và **Q5** (Tỷ lệ ảnh hưởng ở vật nuôi đàn).
   - [`notebooks/02c_analysis_kiet.ipynb`](notebooks/02c_analysis_kiet.ipynb): Phân tích sâu **Q3** (ROR Hoạt chất – Phản ứng) và **Q4** (Off-label & Polypharmacy).
3. [`notebooks/03_ml_question.ipynb`](notebooks/03_ml_question.ipynb) — Huấn luyện mô hình học máy trên giai đoạn **2025 Q1–Q4**, dự đoán và đánh giá độ chính xác trên tập kiểm thử ngoài thời gian **2026 (Q1)** (**Q6**), phân tích lỗi, giải thích mô hình bằng Permutation Importance và tổng kết đồ án.

### 7.5. Troubleshooting thường gặp
- `conda: command not found` → chưa cài Miniconda/Anaconda hoặc chưa thêm vào PATH.
- `conda activate` không có tác dụng trên PowerShell → chạy `conda init powershell` và mở lại terminal.
- Jupyter không thấy kernel `ds-env` → chạy:
  ```powershell
  python -m ipykernel install --user --name ds-env
  ```
- `ModuleNotFoundError` → kiểm tra đã `conda activate ds-env` chưa, sau đó chạy `conda env update -f environment.yml --prune`.
- Không đọc được dữ liệu → kiểm tra file nằm đúng trong `data/raw/` và đủ 5 quý (2025 Q1–Q4, 2026 Q1) hoặc chạy lại `python src/download_data.py`.

---

## 8. Cam kết học thuật & Khai báo sử dụng AI

- Mọi nguồn dữ liệu, tài liệu tham khảo và đoạn mã tham khảo bên ngoài đều được trích dẫn rõ ràng.
- Mọi phiên sử dụng công cụ AI/LLM của các thành viên trong nhóm đều được ghi chép minh bạch trong tệp [`LLM_USAGE.md`](LLM_USAGE.md) theo đúng quy định tại Mục 6 của đề cương môn học.
- Mã nguồn của kho lưu trữ được phát hành theo giấy phép tại tệp [`LICENSE`](LICENSE); dữ liệu openFDA sử dụng giấy phép CC0 1.0 Universal.
- Để đảm bảo tái lập, các mô hình học máy sử dụng `random_state` cố định và toàn bộ pipeline được đóng gói trong `scikit-learn Pipeline`.
