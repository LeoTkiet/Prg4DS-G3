# Data Dictionary v0 — OpenFDA Animal & Veterinary Adverse Events

> **Phiên bản:** v0 (initial draft)  
> **Nguồn dữ liệu:** [openFDA Animal & Veterinary Adverse Events](https://open.fda.gov/data/downloads/)  
> **API Docs:** [https://open.fda.gov/apis/animalandveterinary/event/](https://open.fda.gov/apis/animalandveterinary/event/)  
> **Giấy phép:** Creative Commons CC0 1.0 Universal  
> **Phạm vi:** 2025 Q1–Q4 + 2026 Q1  
> **Ngày thu thập và khởi tạo:** Thu thập ngày 06/11/2026 (`2026-11-06T16:53:03Z`), khởi tạo tài liệu ngày 07/11/2026 (trên phiên bản dữ liệu openFDA cập nhật ngày `2026-11-02`).

---

## 1. Bảng `reports` — Thông tin cấp báo cáo (Report-level)

Mỗi dòng = 1 báo cáo duy nhất. Khóa chính: `unique_aer_id_number`.

| # | Tên cột | Kiểu dữ liệu | JSON path gốc | Mô tả | Ghi chú |
|---|---------|---------------|----------------|-------|---------|
| 1 | `unique_aer_id_number` | `str` | `unique_aer_id_number` | Mã báo cáo duy nhất (Adverse Event Report ID) | **Primary Key** |
| 2 | `report_id` | `str` | `report_id` | Mã báo cáo nội bộ FDA | Có thể trùng nếu cùng report được cập nhật |
| 3 | `original_receive_date` | `str (YYYYMMDD)` | `original_receive_date` | Ngày FDA nhận báo cáo lần đầu | Cần parse → datetime |
| 4 | `onset_date` | `str (YYYYMMDD)` | `onset_date` | Ngày khởi phát phản ứng bất lợi | Có thể NULL; dùng tính `reporting_delay_days` |
| 5 | `year` | `int` | *(derived)* | Năm trích từ `original_receive_date` | **Biến dẫn xuất** |
| 6 | `quarter` | `str` | *(derived)* | Quý theo format `YYYYqN` | **Biến dẫn xuất** |
| 7 | `primary_reporter` | `str` | `primary_reporter` | Đối tượng báo cáo chính (Veterinarian, Animal Owner, Other Health Professional, ...) | Categorical |
| 8 | `secondary_reporter` | `str` | `secondary_reporter` | Đối tượng báo cáo phụ | Thường NULL |
| 9 | `type_of_information` | `str` | `type_of_information` | Loại thông tin báo cáo: Safety Issue, Lack Of Expected Effectiveness, cả hai, Product Defect/Quality Issue | Categorical |
| 10 | `serious_ae` | `str/bool` | `serious_ae` | Sự cố nghiêm trọng? (true/false) | **Target variable cho Q6 (ML)**; có giá trị khuyết |
| 11 | `treated_for_ae` | `str/bool` | `treated_for_ae` | Có điều trị cho phản ứng bất lợi? (true/false) | **Leakage risk** nếu dùng cho ML |
| 12 | `number_of_animals_affected` | `int/str` | `number_of_animals_affected` | Số cá thể bị ảnh hưởng trong báo cáo | Thường = 1 |
| 13 | `number_of_animals_treated` | `int/str` | `number_of_animals_treated` | Số cá thể được điều trị | |
| 14 | `animal_species` | `str` | `animal.species` | Loài vật nuôi (Dog, Cat, Horse, ...) | Categorical; nhiều loài |
| 15 | `animal_gender` | `str` | `animal.gender` | Giới tính (Male, Female, Neutered Male, Spayed Female, Unknown) | Categorical |
| 16 | `animal_reproductive_status` | `str` | `animal.reproductive_status` | Tình trạng sinh sản (Intact, Neutered, Spayed, Unknown) | |
| 17 | `animal_female_animal_physiological_status` | `str` | `animal.female_animal_physiological_status` | Trạng thái sinh lý con cái (Not Pregnant, Pregnant, Lactating, ...) | Thường NULL nếu Male |
| 18 | `animal_breed_breed_component` | `str` | `animal.breed.breed_component` | Giống (breed) — có thể là chuỗi hoặc list nếu mixed breed | Cần flatten nếu là list |
| 19 | `animal_breed_is_crossbred` | `str/bool` | `animal.breed.is_crossbred` | Có phải giống lai? | |
| 20 | `animal_age_min` | `float` | `animal.age.min` | Tuổi tối thiểu (đơn vị gốc) | Cần quy đổi → `age_years` |
| 21 | `animal_age_max` | `float` | `animal.age.max` | Tuổi tối đa (đơn vị gốc) | |
| 22 | `animal_age_unit` | `str` | `animal.age.unit` | Đơn vị tuổi gốc: Year, Month, Week, Day | Dùng để quy đổi |
| 23 | `animal_age_qualifier` | `str` | `animal.age.qualifier` | Dạng qualifier: Measured, Estimated, Unknown | |
| 24 | `animal_weight_min` | `float` | `animal.weight.min` | Cân nặng tối thiểu (đơn vị gốc) | Cần quy đổi → `weight_kg` |
| 25 | `animal_weight_max` | `float` | `animal.weight.max` | Cân nặng tối đa (đơn vị gốc) | |
| 26 | `animal_weight_unit` | `str` | `animal.weight.unit` | Đơn vị cân nặng gốc: Kilogram, Pound, Gram, Ounce | Dùng để quy đổi |
| 27 | `animal_weight_qualifier` | `str` | `animal.weight.qualifier` | Dạng qualifier: Measured, Estimated, Unknown | |

---

## 2. Bảng `drugs` — Thông tin thuốc / hoạt chất (Drug-level)

Mỗi dòng = 1 mục thuốc trong 1 báo cáo. Quan hệ 1:N với `reports`.

| # | Tên cột | Kiểu dữ liệu | JSON path gốc | Mô tả | Ghi chú |
|---|---------|---------------|----------------|-------|---------|
| 28 | `unique_aer_id_number` | `str` | *(FK)* | Khóa ngoại liên kết về `reports` | **Foreign Key** |
| 29 | `drug_idx` | `int` | *(derived)* | Thứ tự thuốc trong báo cáo (0, 1, 2, ...) | |
| 30 | `active_ingredients_name` | `str` | `drug[].active_ingredients[].name` | Tên hoạt chất (ví dụ: Fluralaner, Ivermectin) | Có thể list → cần explode hoặc join |
| 31 | `active_ingredients_dose` | `str/dict` | `drug[].active_ingredients[].dose` | Liều lượng hoạt chất | Nested; cần parse |
| 32 | `brand_name` | `str` | `drug[].brand_name` | Tên thương hiệu thuốc | |
| 33 | `dosage_form` | `str` | `drug[].dosage_form` | Dạng bào chế (Tablet, Solution, Topical, ...) | Categorical |
| 34 | `administration_route` | `str` | `drug[].route` | Đường dùng (Oral, Topical, Subcutaneous, ...) | Categorical |
| 35 | `manufacturer_name` | `str` | `drug[].manufacturer.name` | Tên nhà sản xuất | |
| 36 | `manufacturer_registration_number` | `str` | `drug[].manufacturer.registration_number` | Mã đăng ký nhà sản xuất | |
| 37 | `used_according_to_label` | `str/bool` | `drug[].used_according_to_label` | Thuốc được dùng đúng nhãn? | true/false |
| 38 | `off_label_use` | `str` | `drug[].off_label_use` | Mô tả cách dùng sai nhãn (nếu có) | Thường NULL khi `used_according_to_label = true` |
| 39 | `lot_number` | `str` | `drug[].lot_number` | Số lô sản phẩm | |
| 40 | `lot_expiration` | `str` | `drug[].lot_expiration` | Ngày hết hạn lô | |
| 41 | `atc_vet_code` | `str` | `drug[].atc_vet_code` | Mã phân loại ATC Vet (hệ thống WHO) | |
| 42 | `previous_ae_to_drug` | `str/bool` | `drug[].previous_ae_to_drug` | Đã có AE trước đó với thuốc này? | |

---

## 3. Bảng `reactions` — Phản ứng bất lợi (Reaction-level)

Mỗi dòng = 1 phản ứng VeDDRA trong 1 báo cáo. Quan hệ 1:N với `reports`.

| # | Tên cột | Kiểu dữ liệu | JSON path gốc | Mô tả | Ghi chú |
|---|---------|---------------|----------------|-------|---------|
| 43 | `unique_aer_id_number` | `str` | *(FK)* | Khóa ngoại liên kết về `reports` | **Foreign Key** |
| 44 | `veddra_term_code` | `str` | `reaction[].veddra_term_code` | Mã thuật ngữ VeDDRA (hệ thống phân loại phản ứng thú y) | |
| 45 | `veddra_term_name` | `str` | `reaction[].veddra_term_name` | Tên phản ứng (Vomiting, Lethargy, Diarrhoea, Death, ...) | **Core analysis variable** |
| 46 | `veddra_version` | `str/int` | `reaction[].veddra_version` | Phiên bản bảng thuật ngữ VeDDRA | |
| 47 | `reaction_number_of_animals_affected` | `int/str` | `reaction[].number_of_animals_affected` | Số cá thể có phản ứng này | |
| 48 | `reaction_accuracy` | `str` | `reaction[].accuracy` | Độ chính xác của phản ứng (Exact, Possible, ...) | |

---

## 4. Bảng `outcomes` — Kết cục y khoa (Outcome-level)

Mỗi dòng = 1 kết cục trong 1 báo cáo. Quan hệ 1:N với `reports`.

| # | Tên cột | Kiểu dữ liệu | JSON path gốc | Mô tả | Ghi chú |
|---|---------|---------------|----------------|-------|---------|
| — | `unique_aer_id_number` | `str` | *(FK)* | Khóa ngoại liên kết về `reports` | **Foreign Key** |
| — | `medical_status` | `str` | `outcome[].medical_status` | Kết cục y khoa: Recovered/Normal, Died, Euthanized, Ongoing, Unknown | Categorical |
| — | `outcome_number_of_animals_affected` | `int/str` | `outcome[].number_of_animals_affected` | Số cá thể có kết cục này | |

---

## 5. Biến dẫn xuất (Derived Variables) — sẽ tạo ở giai đoạn tiền xử lý

| Biến | Công thức / Logic | Mục đích |
|------|-------------------|----------|
| `age_years` | Quy đổi `animal_age_min` theo `animal_age_unit` (Day→/365.25, Week→/52.18, Month→/12) | Chuẩn hóa so sánh tuổi |
| `weight_kg` | Quy đổi `animal_weight_min` theo `animal_weight_unit` (lb→×0.4536, oz→×0.02835, g→/1000) | Chuẩn hóa so sánh cân nặng |
| `life_stage` | Phân nhóm từ `age_years` + `animal_species` (Neonatal, Young, Adult, Senior) | Phân tầng phân tích |
| `reporting_delay_days` | `original_receive_date − onset_date` (ngày) | Phân tích hành vi báo cáo (Q5) |
| `num_drugs` | Đếm số drug[] trong mỗi report | Xác định đa trị liệu (polypharmacy) |
| `has_off_label_use` | `any(drug.used_according_to_label == false)` | Phân tích dùng thuốc sai nhãn (Q4) |

---

## Ghi chú chung

1. **Schema JSON lồng nhau**: Mỗi record gốc trong `results[]` chứa các object/array con (`animal`, `drug[]`, `reaction[]`, `outcome[]`). Bảng `reports` được flatten từ cấp root + `animal.*`. Các bảng `drugs`, `reactions`, `outcomes` được explode từ array tương ứng.
2. **Giá trị khuyết**: Nhiều trường tùy chọn (onset_date, weight, age, secondary_reporter, off_label_use) có tỷ lệ NULL cao — cần phân tích cơ chế khuyết (MCAR/MAR/MNAR) ở giai đoạn EDA.
3. **Đơn vị không đồng nhất**: Tuổi (Day/Week/Month/Year) và cân nặng (Kilogram/Pound/Gram/Ounce) cần quy đổi trước khi phân tích.
4. **Ngưỡng 48 cột**: Data dictionary này liệt kê 48 trường chính (27 cột reports + 15 cột drugs + 6 cột reactions) dùng cho phân tích. Bảng `outcomes` và biến dẫn xuất bổ sung thêm.

