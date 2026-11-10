# Data Dictionary v1 — OpenFDA Animal & Veterinary Adverse Events

> **Phiên bản:** v1 (đồng bộ hoàn toàn với schema CSV đầu ra của `src/data_loader.py`)  
> **Nguồn dữ liệu:** [openFDA Animal & Veterinary Adverse Events](https://open.fda.gov/data/downloads/)  
> **API Docs:** [https://open.fda.gov/apis/animalandveterinary/event/](https://open.fda.gov/apis/animalandveterinary/event/)  
> **Giấy phép:** Creative Commons CC0 1.0 Universal  
> **Phạm vi:** 2025 Q1–Q4 + 2026 Q1  
> **Ngày thu thập và khởi tạo:** Thu thập ngày 06/11/2026 (`2026-11-06T16:53:03Z`), cập nhật tài liệu ngày 10/11/2026 (trên phiên bản dữ liệu openFDA cập nhật ngày `2026-11-02`).

---

## 1. Bảng `reports.csv` — Thông tin cấp báo cáo (Report-level)

Mỗi dòng = 1 báo cáo duy nhất. Khóa chính: `unique_aer_id_number`.

| # | Tên cột (`reports.csv`) | Kiểu dữ liệu | JSON path / Nguồn gốc | Mô tả | Ghi chú |
|---|---------|---------------|----------------|-------|---------|
| 1 | `unique_aer_id_number` | `str` | `unique_aer_id_number` | Mã định danh báo cáo sự kiện bất lợi duy nhất (Adverse Event Report ID) | **Primary Key** (khóa duy nhất để khử trùng lặp) |
| 2 | `report_id` | `str` | `report_id` | Mã số hồ sơ/đơn đăng ký thuốc NADA/ANADA của FDA (vd: `N141302`, `N141272`) | Nhiều báo cáo khác nhau có cùng `report_id` — **tuyệt đối không dùng để dedupe** |
| 3 | `original_receive_date` | `str (YYYYMMDD)` | `original_receive_date` | Ngày FDA nhận báo cáo lần đầu | Cần parse → `datetime` ở bước tiền xử lý |
| 4 | `onset_date` | `str (YYYYMMDD)` | `onset_date` | Ngày khởi phát phản ứng bất lợi | Có thể NULL; dùng tính `reporting_delay_days` |
| 5 | `primary_reporter` | `str` | `primary_reporter` | Đối tượng báo cáo chính (`Veterinarian`, `Animal Owner`, `Other Health Care Professional`, ...) | Categorical |
| 6 | `secondary_reporter` | `str` | `secondary_reporter` | Đối tượng báo cáo phụ | Thường NULL |
| 7 | `type_of_information` | `str` | `type_of_information` | Loại thông tin báo cáo: `Safety Issue`, `Lack Of Expected Effectiveness`, cả hai, `Product Defect` | Categorical |
| 8 | `serious_ae` | `str/bool` | `serious_ae` | Sự cố nghiêm trọng? (`true`/`false`) | **Target variable cho Q6 (ML)**; có giá trị khuyết |
| 9 | `treated_for_ae` | `str/bool` | `treated_for_ae` | Có điều trị cho phản ứng bất lợi? (`true`/`false`) | **Leakage risk** — loại bỏ khi huấn luyện ML |
| 10 | `number_of_animals_affected` | `int/str` | `number_of_animals_affected` | Số cá thể bị ảnh hưởng trong báo cáo | Thường = 1 (thú cưng) hoặc > 1 (gia súc/đàn) |
| 11 | `number_of_animals_treated` | `int/str` | `number_of_animals_treated` | Số cá thể được điều trị | |
| 12 | `species` | `str` | `animal.species` | Loài vật nuôi (`Dog`, `Cat`, `Horse`, `Cattle`, ...) | Categorical |
| 13 | `gender` | `str` | `animal.gender` | Giới tính (`Male`, `Female`, `Unknown`, ...) | Categorical |
| 14 | `reproductive_status` | `str` | `animal.reproductive_status` | Tình trạng sinh sản (`Intact`, `Neutered`, `Unknown`, ...) | Categorical |
| 15 | `female_physio_status` | `str` | `animal.female_animal_physiological_status` | Trạng thái sinh lý con cái (`Not Pregnant`, `Pregnant`, `Lactating`, ...) | Thường NULL nếu Male |
| 16 | `breed_component` | `str` | `animal.breed.breed_component` | Giống vật nuôi (nếu là list nhiều giống sẽ được nối bằng `';'`) | Làm phẳng trong `data_loader.py` |
| 17 | `is_crossbred` | `str/bool` | `animal.breed.is_crossbred` | Có phải giống lai? (`true`/`false`) | |
| 18 | `age_min` | `float/str` | `animal.age.min` | Tuổi tối thiểu (ở đơn vị gốc `age_unit`) | Quy đổi → `age_years` ở bước tiền xử lý |
| 19 | `age_max` | `float/str` | `animal.age.max` | Tuổi tối đa (ở đơn vị gốc `age_unit`) | |
| 20 | `age_unit` | `str` | `animal.age.unit` | Đơn vị tuổi gốc (`Year`, `Month`, `Week`, `Day`, ...) | Dùng để quy đổi về năm |
| 21 | `age_qualifier` | `str` | `animal.age.qualifier` | Dạng qualifier của tuổi (`Measured`, `Estimated`, `Unknown`) | |
| 22 | `weight_min` | `float/str` | `animal.weight.min` | Cân nặng tối thiểu (ở đơn vị gốc `weight_unit`) | Quy đổi → `weight_kg` ở bước tiền xử lý |
| 23 | `weight_max` | `float/str` | `animal.weight.max` | Cân nặng tối đa (ở đơn vị gốc `weight_unit`) | |
| 24 | `weight_unit` | `str` | `animal.weight.unit` | Đơn vị cân nặng gốc (`Kilogram`, `Pound`, `Gram`, `Ounce`, ...) | Dùng để quy đổi về kg |
| 25 | `weight_qualifier` | `str` | `animal.weight.qualifier` | Dạng qualifier của cân nặng (`Measured`, `Estimated`, `Unknown`) | |
| 26 | `duration_value` | `float/str` | `duration.value` | Thời gian kéo dài của phản ứng (giá trị) | **Leakage risk** — loại bỏ khi huấn luyện ML |
| 27 | `duration_unit` | `str` | `duration.unit` | Đơn vị thời gian kéo dài của phản ứng | **Leakage risk** — loại bỏ khi huấn luyện ML |
| 28 | `health_prior_condition` | `str` | `health_assessment_prior_to_exposure.condition` | Tình trạng sức khỏe trước khi dùng thuốc (`Good`, `Fair`, `Poor`, `Unknown`) | |
| 29 | `health_prior_assessed_by` | `str` | `health_assessment_prior_to_exposure.assessed_by` | Người đánh giá sức khỏe trước phơi nhiễm (`Veterinarian`, `Animal Owner`, ...) | |
| 30 | `quarter` | `str` | *(loader metadata)* | Phân vùng quý của file dữ liệu (`2025q1`–`2026q1`) | Gắn tự động bởi `src/data_loader.py` |
| 31 | `source_file` | `str` | *(loader metadata)* | Tên file JSON gốc trong `data/raw/` | Dùng để truy vết nguồn & đồng bộ bảng con khi dedupe |

---

## 2. Bảng `drugs.csv` — Thông tin thuốc / hoạt chất (Drug-level)

Mỗi dòng = 1 mục thuốc trong 1 báo cáo. Quan hệ 1:N với `reports.csv`.

| # | Tên cột (`drugs.csv`) | Kiểu dữ liệu | JSON path / Nguồn gốc | Mô tả | Ghi chú |
|---|---------|---------------|----------------|-------|---------|
| 32 | `unique_aer_id_number` | `str` | *(FK)* | Khóa ngoại liên kết về `reports.csv` | **Foreign Key** |
| 33 | `drug_idx` | `int/str` | *(loader index)* | Thứ tự thuốc trong mảng `drug[]` của báo cáo (`0, 1, 2, ...`) | |
| 34 | `active_ingredients` | `str` | `drug[].active_ingredients[].name` | Tên các hoạt chất trong thuốc nối bằng dấu `';'` | Có thể tách (`str.split(';')`) khi phân tích hoạt chất đơn |
| 35 | `brand_name` | `str` | `drug[].brand_name` | Tên thương hiệu thuốc (nếu được công bố) | Thường bị che (`MSK`) hoặc NULL |
| 36 | `dosage_form` | `str` | `drug[].dosage_form` | Dạng bào chế (`Tablet`, `Solution`, `Chewable`, `Topical`, ...) | Categorical |
| 37 | `route` | `str` | `drug[].route` | Đường dùng thuốc (`Oral`, `Topical`, `Subcutaneous`, ...) | Categorical |
| 38 | `manufacturer_name` | `str` | `drug[].manufacturer.name` | Tên nhà sản xuất thuốc | Làm phẳng từ `manufacturer.name` |
| 39 | `atc_vet_code` | `str` | `drug[].atc_vet_code` | Mã phân loại dược lý thú y ATCvet (WHO) | |
| 40 | `used_according_to_label` | `str/bool` | `drug[].used_according_to_label` | Thuốc có được dùng đúng nhãn hướng dẫn không? (`true`/`false`) | Biến cốt lõi cho Q4 |
| 41 | `off_label_use` | `str` | `drug[].off_label_use` | Chi tiết hành vi dùng sai nhãn (`Overdose`, `Underdose`, `Unapproved species`, ...) | Thường NULL khi `used_according_to_label = true` |
| 42 | `dose_numerator` | `float/str` | `drug[].dose.numerator` | Tử số liều dùng | Làm phẳng qua `_flat("dose", ...)` |
| 43 | `dose_numerator_unit` | `str` | `drug[].dose.numerator_unit` | Đơn vị tử số liều dùng | |
| 44 | `dose_denominator` | `float/str` | `drug[].dose.denominator` | Mẫu số liều dùng | |
| 45 | `dose_denominator_unit` | `str` | `drug[].dose.denominator_unit` | Đơn vị mẫu số liều dùng | |
| 46 | `frequency_value` | `float/str` | `drug[].frequency_of_administration.value` | Giá trị tần suất dùng thuốc | Làm phẳng qua `_flat("frequency", ...)` |
| 47 | `frequency_unit` | `str` | `drug[].frequency_of_administration.unit` | Đơn vị tần suất dùng thuốc | |
| 48 | `lot_number` | `str` | `drug[].lot_number` | Số lô sản phẩm | |
| 49 | `lot_expiration` | `str` | `drug[].lot_expiration` | Ngày hết hạn lô | |
| 50 | `previous_ae_to_drug` | `str/bool` | `drug[].previous_ae_to_drug` | Đã từng gặp AE trước đó với thuốc này? | *(Cùng các cờ phơi nhiễm tùy chọn khác trong `drug[]`)* |
| 51 | `quarter` | `str` | *(loader metadata)* | Phân vùng quý (`2025q1`–`2026q1`) | |
| 52 | `source_file` | `str` | *(loader metadata)* | Tên file JSON gốc | |

---

## 3. Bảng `reactions.csv` — Phản ứng bất lợi (Reaction-level)

Mỗi dòng = 1 phản ứng VeDDRA trong 1 báo cáo. Quan hệ 1:N với `reports.csv`.

| # | Tên cột (`reactions.csv`) | Kiểu dữ liệu | JSON path / Nguồn gốc | Mô tả | Ghi chú |
|---|---------|---------------|----------------|-------|---------|
| 53 | `unique_aer_id_number` | `str` | *(FK)* | Khóa ngoại liên kết về `reports.csv` | **Foreign Key** |
| 54 | `veddra_term_code` | `str` | `reaction[].veddra_term_code` | Mã thuật ngữ VeDDRA | |
| 55 | `veddra_term_name` | `str` | `reaction[].veddra_term_name` | Tên phản ứng lâm sàng (`Vomiting`, `Lethargy`, `Diarrhoea`, ...) | **Core analysis variable** (Q1, Q3) |
| 56 | `veddra_version` | `str/int` | `reaction[].veddra_version` | Phiên bản bộ từ điển VeDDRA | |
| 57 | `number_of_animals_affected` | `int/str` | `reaction[].number_of_animals_affected` | Số cá thể biểu hiện phản ứng này | |
| 58 | `accuracy` | `str` | `reaction[].accuracy` | Độ chính xác của ghi nhận phản ứng (`Actual`, `Suspected`, ...) | |
| 59 | `quarter` | `str` | *(loader metadata)* | Phân vùng quý (`2025q1`–`2026q1`) | |
| 60 | `source_file` | `str` | *(loader metadata)* | Tên file JSON gốc | |

---

## 4. Bảng `outcomes.csv` — Kết cục y khoa (Outcome-level)

Mỗi dòng = 1 kết cục trong 1 báo cáo. Quan hệ 1:N với `reports.csv`.

| # | Tên cột (`outcomes.csv`) | Kiểu dữ liệu | JSON path / Nguồn gốc | Mô tả | Ghi chú |
|---|---------|---------------|----------------|-------|---------|
| 61 | `unique_aer_id_number` | `str` | *(FK)* | Khóa ngoại liên kết về `reports.csv` | **Foreign Key** |
| 62 | `medical_status` | `str` | `outcome[].medical_status` | Kết cục y khoa: `Recovered/Normal`, `Died`, `Euthanized`, `Ongoing`, `Unknown` | **Leakage risk** cho Q6 (ML) |
| 63 | `number_of_animals_affected` | `int/str` | `outcome[].number_of_animals_affected` | Số cá thể có kết cục này | |
| 64 | `quarter` | `str` | *(loader metadata)* | Phân vùng quý (`2025q1`–`2026q1`) | |
| 65 | `source_file` | `str` | *(loader metadata)* | Tên file JSON gốc | |

---

## 5. Biến dẫn xuất (Derived Variables) — Tạo ở giai đoạn Tiền xử lý & Feature Engineering

| Biến dẫn xuất | Nguồn & Công thức quy đổi | Mục đích sử dụng |
|---|---|---|
| `year` | Trích xuất từ `original_receive_date` (hoặc 4 ký tự đầu của `quarter`) | Phân tách giai đoạn 2025 vs. 2026 |
| `age_years` | Quy đổi `age_min` theo `age_unit` (`Day` $\rightarrow /365.25$, `Week` $\rightarrow /52.18$, `Month` $\rightarrow /12$) | Chuẩn hóa so sánh tuổi vật nuôi (Q2, Q6) |
| `weight_kg` | Quy đổi `weight_min` theo `weight_unit` (`Pound` $\rightarrow \times 0.453592$, `Ounce` $\rightarrow \times 0.02835$, `Gram` $\rightarrow /1000$) | Chuẩn hóa so sánh cân nặng (Q2, Q6) |
| `life_stage` | Phân nhóm từ `age_years` theo `species` (`Junior/Young`, `Adult`, `Senior`, `Unknown`) | Phân tầng rủi ro lâm sàng (Q2) |
| `reporting_delay_days` | `original_receive_date - onset_date` (tính theo ngày) | Phân tích độ trễ báo cáo theo đối tượng gửi (Q5) |
| `num_drugs` | Đếm số dòng thuốc (`drug_idx`) trên mỗi `unique_aer_id_number` | Xác định đa trị liệu (`polypharmacy` khi `num_drugs >= 2`) (Q2, Q4, Q6) |
| `has_off_label_use` | `any(used_according_to_label == 'false')` hoặc có `off_label_use` trên báo cáo | Phân tích tác động dùng thuốc sai nhãn (Q4, Q6) |
