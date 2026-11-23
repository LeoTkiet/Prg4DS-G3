# Data Dictionary v2 — OpenFDA Animal & Veterinary Adverse Events

> **Phiên bản:** v2 (Đồng bộ hóa 100% với schema CSV thực tế của `src/data_loader.py` và các biến dẫn xuất trong Notebooks 01, 02, 03)  
> **Nguồn dữ liệu:** [openFDA Animal & Veterinary Adverse Events](https://open.fda.gov/data/downloads/)  
> **Cơ quan quản lý & công bố:** U.S. Food and Drug Administration (FDA) – Center for Veterinary Medicine (CVM)  
> **API Docs:** [https://open.fda.gov/apis/animalandveterinary/event/](https://open.fda.gov/apis/animalandveterinary/event/)  
> **Giấy phép:** Creative Commons CC0 1.0 Universal (Public Domain Dedication)  
> **Phạm vi thời gian:** 5 phân vùng quý liên tiếp (`2025q1`, `2025q2`, `2025q3`, `2025q4`, `2026q1`)  
> **Quy mô toàn bộ cơ sở dữ liệu:**
> - `reports.csv`: **94.412** dòng (mỗi dòng là 1 báo cáo duy nhất — Unit of Observation) $\times$ **33** cột
> - `drugs.csv`: **174.123** dòng (mỗi dòng là 1 thuốc trong báo cáo) $\times$ **31** cột
> - `reactions.csv`: **270.244** dòng (mỗi dòng là 1 thuật ngữ VeDDRA) $\times$ **8** cột
> - `outcomes.csv`: **85.143** dòng (mỗi dòng là 1 kết cục lâm sàng) $\times$ **5** cột  
> **Tổng cộng trường dữ liệu gốc/phẳng hóa:** **77** cột

---

## 1. Bảng `reports.csv` — Thông tin cấp báo cáo (Report-level)

Mỗi dòng đại diện cho một báo cáo sự cố bất lợi duy nhất.  
**Khóa chính (Primary Key):** `unique_aer_id_number` (được bảo đảm tính duy nhất và dùng để khử trùng lặp).

| STT | Tên cột (`reports.csv`) | Kiểu dữ liệu | JSON Path / Nguồn gốc | Ý nghĩa & Mô tả lâm sàng / hành chính | Ghi chú & Giá trị mẫu |
|:---:|---|:---:|---|---|---|
| 1 | `unique_aer_id_number` | `str` | `unique_aer_id_number` | Mã định danh duy nhất của báo cáo sự cố bất lợi (Adverse Event Report ID) | **Primary Key** (vd: `USA-USFDACVM-2025-US-0001`) |
| 2 | `report_id` | `str` | `report_id` | Mã số hồ sơ đăng ký thuốc NADA/ANADA của FDA | Nhiều ca bệnh chung 1 thuốc sẽ trùng mã (vd: `N141521`) — **Không dùng để dedupe** |
| 3 | `original_receive_date` | `str` | `original_receive_date` | Ngày FDA tiếp nhận hồ sơ lần đầu (định dạng `YYYYMMDD`) | Ép kiểu `datetime` ở bước tiền xử lý; dùng tính `reporting_delay_days` |
| 4 | `onset_date` | `str` | `onset_date` | Ngày phát bệnh / khởi phát triệu chứng bất lợi (`YYYYMMDD`) | Có thể NULL nếu người báo cáo không nhớ rõ ngày |
| 5 | `primary_reporter` | `str` | `primary_reporter` | Người báo cáo chính (`Veterinarian`, `Animal Owner`, `Other Health Care Professional`, ...) | Phân loại nguồn gốc hồ sơ (ảnh hưởng đến cơ chế thiếu dữ liệu MAR) |
| 6 | `secondary_reporter` | `str` | `secondary_reporter` | Người báo cáo phụ | Thường NULL hoặc cùng đối tượng |
| 7 | `type_of_information` | `str` | `type_of_information` | Phân loại biến cố: `Safety Issue`, `Lack Of Expected Effectiveness`, cả hai, hoặc `Product Defect` | Phân biệt độc tính an toàn sinh học vs giảm hiệu lực thuốc (Q3, Q6) |
| 8 | `serious_ae` | `str/bool` | `serious_ae` | Biến cố có thuộc mức độ nghiêm trọng không? (`true`/`false`) | **Target variable của bài toán Học máy (Q6)** |
| 9 | `treated_for_ae` | `str/bool` | `treated_for_ae` | Vật nuôi có phải can thiệp điều trị y tế cho biến cố bất lợi không? | **Leakage risk** — bắt buộc loại khỏi tập đặc trưng ML Q6 |
| 10 | `number_of_animals_affected` | `int/str` | `number_of_animals_affected` | Số lượng cá thể bị ảnh hưởng trong đợt điều trị | $= 1$ ở thú cưng; $\ge 1$ ở báo cáo đàn gia súc/gia cầm |
| 11 | `number_of_animals_treated` | `int/str` | `number_of_animals_treated` | Tổng số lượng cá thể được dùng thuốc trong đàn | Dùng làm mẫu số tính `attack_rate` ở câu hỏi Q5 |
| 12 | `species` | `str` | `animal.species` | Loài vật nuôi (`Dog`, `Cat`, `Horse`, `Cattle`, `Pig`, ...) | Lọc bỏ `Human` ở tiền xử lý; phân tầng loài cho Q1, Q2, Q4 |
| 13 | `gender` | `str` | `animal.gender` | Giới tính vật nuôi (`Male`, `Female`, `Unknown`, `Mixed`) | Biến sinh trắc học khảo sát ở Q2 |
| 14 | `reproductive_status` | `str` | `animal.reproductive_status` | Tình trạng triệt sản / sinh sản (`Neutered`, `Intact`, `Unknown`) | Biến sinh trắc học khảo sát ở Q2, Q6 |
| 15 | `female_physio_status` | `str` | `animal.female_animal_physiological_status` | Trạng thái sinh lý con cái (`Pregnant`, `Lactating`, `Not Pregnant`) | Thường NULL ở con đực (`Male`) |
| 16 | `breed_component` | `str` | `animal.breed.breed_component` | Tên giống vật nuôi (nếu nhiều giống sẽ nối bằng `';'`) | Làm phẳng từ mảng lồng nhau của openFDA |
| 17 | `is_crossbred` | `str/bool` | `animal.breed.is_crossbred` | Vật nuôi có phải giống lai hay không (`true`/`false`) | |
| 18 | `age_min` | `float/str` | `animal.age.min` | Giá trị tuổi tối thiểu ghi nhận trong hồ sơ | Đơn vị theo cột `age_unit` |
| 19 | `age_max` | `float/str` | `animal.age.max` | Giá trị tuổi tối đa ghi nhận trong hồ sơ (nếu ghi khoảng) | Thường NULL nếu tuổi là giá trị đơn |
| 20 | `age_unit` | `str` | `animal.age.unit` | Đơn vị tính tuổi gốc (`Year`, `Month`, `Week`, `Day`, `Hour`, `Minute`) | Bắt buộc quy đổi chuẩn hóa về năm (`age_years`) |
| 21 | `age_qualifier` | `str` | `animal.age.qualifier` | Tính chất xác thực của tuổi (`Measured`, `Estimated`, `Unknown`) | |
| 22 | `weight_min` | `float/str` | `animal.weight.min` | Giá trị thể trọng tối thiểu ghi nhận trong hồ sơ | Đơn vị theo cột `weight_unit` |
| 23 | `weight_max` | `float/str` | `animal.weight.max` | Giá trị thể trọng tối đa ghi nhận trong hồ sơ | Thường NULL nếu cân nặng là giá trị đơn |
| 24 | `weight_unit` | `str` | `animal.weight.unit` | Đơn vị thể trọng gốc (`Kilogram`, `Pound`, `Gram`, `Ounce`) | Bắt buộc quy đổi chuẩn hóa về kilôgam (`weight_kg`) |
| 25 | `weight_qualifier` | `str` | `animal.weight.qualifier` | Tính chất xác thực của cân nặng (`Measured`, `Estimated`, `Unknown`) | |
| 26 | `duration_value` | `float/str` | `duration.value` | Khoảng thời gian kéo dài của triệu chứng bất lợi | **Leakage risk** — thông tin hậu nghiệm, loại khỏi ML |
| 27 | `duration_unit` | `str` | `duration.unit` | Đơn vị thời gian kéo dài (`Day`, `Hour`, `Week`, ...) | **Leakage risk** — loại khỏi ML |
| 28 | `health_prior_condition` | `str` | `health_assessment_prior_to_exposure.condition` | Tình trạng sức khỏe trước khi dùng thuốc (`Good`, `Fair`, `Poor`, `Unknown`) | |
| 29 | `health_prior_assessed_by` | `str` | `health_assessment_prior_to_exposure.assessed_by` | Người đánh giá tình trạng sức khỏe ban đầu | |
| 30 | `foreign_or_domestic` | `str` | `foreign_or_domestic` | Báo cáo nội địa Hoa Kỳ hay từ nước ngoài gửi về FDA (`Domestic`, `Foreign`) | Đa phần là `Domestic` |
| 31 | `time_between_exposure_and_onset` | `str` | `time_between_exposure_and_onset` | Thời gian từ thời điểm dùng thuốc đến lúc phát bệnh | Dạng chuỗi văn bản mô tả nếu có ghi nhận |
| 32 | `quarter` | `str` | *(loader metadata)* | Phân vùng quý thu thập (`2025q1` đến `2026q1`) | Gắn tự động bởi `src/data_loader.py` |
| 33 | `source_file` | `str` | *(loader metadata)* | Tên tệp tin JSON gốc trong `data/raw/` | Dùng truy vết nguồn gốc và chống trùng lặp đa quý |

---

## 2. Bảng `drugs.csv` — Thông tin thuốc / phơi nhiễm dược lý (Drug-level)

Mỗi dòng tương ứng với 1 mục thuốc trong mảng `drug[]` của báo cáo.  
**Quan hệ:** Nhiều-Một ($N:1$) với bảng `reports.csv` qua khóa ngoại `unique_aer_id_number`.

| STT | Tên cột (`drugs.csv`) | Kiểu dữ liệu | JSON Path / Nguồn gốc | Ý nghĩa & Mô tả lâm sàng / dược lý | Ghi chú & Giá trị mẫu |
|:---:|---|:---:|---|---|---|
| 1 | `unique_aer_id_number` | `str` | *(FK)* | Khóa ngoại liên kết về `reports.csv` | **Foreign Key** |
| 2 | `drug_idx` | `int/str` | *(loader index)* | Thứ tự xuất hiện của thuốc trong báo cáo (`0, 1, 2, ...`) | Dùng tính số lượng thuốc dùng đồng thời (`num_drugs`) |
| 3 | `active_ingredients` | `str` | `drug[].active_ingredients[].name` | Tên các hoạt chất có trong thuốc, nối bằng dấu `';'` | Biến cốt lõi phân tích ROR (Q3) và đặc trưng ML (Q6) |
| 4 | `brand_name` | `str` | `drug[].brand_name` | Tên thương hiệu thương mại của thuốc | **100% bị FDA che nhãn `'MSK'`** vì bảo mật thương mại |
| 5 | `manufacturer_name` | `str` | `drug[].manufacturer.name` | Tên công ty/hãng dược phẩm sản xuất thuốc | **100% bị FDA che nhãn `'MSK'`** |
| 6 | `dosage_form` | `str` | `drug[].dosage_form` | Dạng bào chế thuốc (`Tablet`, `Solution`, `Chewable`, `Topical`, ...) | Phân loại phương thức điều trị |
| 7 | `route` | `str` | `drug[].route` | Đường dùng thuốc (`Oral`, `Topical`, `Subcutaneous`, `Intramuscular`, ...) | Biến phân tầng rủi ro cốt lõi (Q3, Q5, Q6) |
| 8 | `atc_vet_code` | `str` | `drug[].atc_vet_code` | Mã phân loại giải phẫu - điều trị - hóa học thú y (ATCvet của WHO) | Vd: `QP54AB52` (thuốc trị ký sinh trùng) |
| 9 | `used_according_to_label` | `str/bool` | `drug[].used_according_to_label` | Thuốc có được sử dụng đúng theo nhãn hướng dẫn (`true`/`false`) | Biến trung tâm phân tích sai nhãn (Q4, Q6) |
| 10 | `off_label_use` | `str` | `drug[].off_label_use` | Chi tiết hành vi dùng sai nhãn (`Overdose`, `Unapproved species`, ...) | Thường NULL khi `used_according_to_label = true` |
| 11 | `administered_by` | `str` | `drug[].administered_by` | Người trực tiếp cho vật nuôi dùng thuốc (`Animal Owner`, `Veterinarian`, ...) | |
| 12 | `first_exposure_date` | `str` | `drug[].first_exposure_date` | Ngày bắt đầu cho dùng thuốc (`YYYYMMDD`) | |
| 13 | `last_exposure_date` | `str` | `drug[].last_exposure_date` | Ngày kết thúc đợt dùng thuốc (`YYYYMMDD`) | |
| 14 | `dose_numerator` | `float/str` | `drug[].dose.numerator` | Giá trị tử số của liều dùng | |
| 15 | `dose_numerator_unit` | `str` | `drug[].dose.numerator_unit` | Đơn vị tử số liều (`Milligram`, `Milliliter`, ...) | |
| 16 | `dose_denominator` | `float/str` | `drug[].dose.denominator` | Giá trị mẫu số của liều dùng | |
| 17 | `dose_denominator_unit` | `str` | `drug[].dose.denominator_unit` | Đơn vị mẫu số liều (`Animal`, `Kilogram`, `Day`, ...) | |
| 18 | `frequency_value` | `float/str` | `drug[].frequency_of_administration.value` | Giá trị tần suất dùng thuốc | |
| 19 | `frequency_unit` | `str` | `drug[].frequency_of_administration.unit` | Đơn vị tần suất dùng (`Day`, `Week`, `Month`, `Once`, ...) | |
| 20 | `lot_number` | `str` | `drug[].lot_number` | Số lô sản xuất của thuốc | Chứa nhiều placeholder (`Unknown`, `not given`) |
| 21 | `lot_expiration` | `str` | `drug[].lot_expiration` | Ngày hết hạn của lô thuốc (`YYYYMMDD`) | |
| 22 | `previous_exposure_to_drug` | `str/bool` | `drug[].previous_exposure_to_drug` | Vật nuôi từng dùng thuốc này trong quá khứ hay chưa (`true`/`false`) | |
| 23 | `previous_ae_to_drug` | `str/bool` | `drug[].previous_ae_to_drug` | Đã từng bị phản ứng phụ với thuốc này trước đây chưa (`true`/`false`) | |
| 24 | `ae_abated_after_stopping_drug` | `str/bool` | `drug[].ae_abated_after_stopping_drug` | Triệu chứng có thuyên giảm sau khi ngưng dùng thuốc hay không? | Phản ánh tiêu chuẩn đánh giá nhân quả lâm sàng |
| 25 | `ae_reappeared_after_resuming_drug` | `str/bool` | `drug[].ae_reappeared_after_resuming_drug` | Triệu chứng có tái xuất hiện khi cho dùng lại thuốc hay không? | Tiêu chuẩn thử thách lại (Rechallenge) |
| 26 | `number_of_defective_items` | `int/str` | `drug[].number_of_defective_items` | Số lượng sản phẩm bị lỗi chất lượng (nếu là ca Product Defect) | |
| 27 | `product_ndc` | `str` | `drug[].product_ndc` | Mã sản phẩm thuốc quốc gia (National Drug Code) | |
| 28 | `manufacturing_date` | `str` | `drug[].manufacturing_date` | Ngày sản xuất của lô thuốc (`YYYYMMDD`) | |
| 29 | `number_of_items_returned` | `int/str` | `drug[].number_of_items_returned` | Số sản phẩm được thu hồi/trả lại cho nhà sản xuất | |
| 30 | `quarter` | `str` | *(loader metadata)* | Phân vùng quý thu thập (`2025q1` đến `2026q1`) | Gắn tự động bởi `src/data_loader.py` |
| 31 | `source_file` | `str` | *(loader metadata)* | Tên tệp tin JSON gốc trong `data/raw/` | |

---

## 3. Bảng `reactions.csv` — Triệu chứng & Phản ứng bất lợi (Reaction-level)

Mỗi dòng tương ứng với 1 thuật ngữ triệu chứng chuẩn hóa quốc tế VeDDRA được ghi nhận trong báo cáo.  
**Quan hệ:** Nhiều-Một ($N:1$) với bảng `reports.csv` qua khóa ngoại `unique_aer_id_number`.

| STT | Tên cột (`reactions.csv`) | Kiểu dữ liệu | JSON Path / Nguồn gốc | Ý nghĩa & Mô tả lâm sàng | Ghi chú & Giá trị mẫu |
|:---:|---|:---:|---|---|---|
| 1 | `unique_aer_id_number` | `str` | *(FK)* | Khóa ngoại liên kết về `reports.csv` | **Foreign Key** |
| 2 | `veddra_version` | `str/int` | `reaction[].veddra_version` | Phiên bản từ điển VeDDRA tại thời điểm mã hóa | Vd: `18` |
| 3 | `veddra_term_code` | `str` | `reaction[].veddra_term_code` | Mã số định danh thuật ngữ VeDDRA (Numeric Code) | Đạt **100% không khuyết** |
| 4 | `veddra_term_name` | `str` | `reaction[].veddra_term_name` | Tên triệu chứng lâm sàng chuẩn hóa (`Vomiting`, `Lethargy`, `Diarrhoea`, ...) | **Core variable cho Q1 & Q3**; đạt 100% không khuyết |
| 5 | `number_of_animals_affected` | `int/str` | `reaction[].number_of_animals_affected` | Số lượng cá thể trong báo cáo biểu hiện triệu chứng cụ thể này | Thường $= 1$ ở thú cưng |
| 6 | `accuracy` | `str` | `reaction[].accuracy` | Mức độ tin cậy của chẩn đoán phản ứng (`Actual`, `Suspected`, ...) | Khuyết 6.33% |
| 7 | `quarter` | `str` | *(loader metadata)* | Phân vùng quý thu thập (`2025q1` đến `2026q1`) | Dùng phân tích chuỗi thời gian Q1 |
| 8 | `source_file` | `str` | *(loader metadata)* | Tên tệp tin JSON gốc trong `data/raw/` | |

---

## 4. Bảng `outcomes.csv` — Kết quả y khoa lâm sàng (Clinical Outcome-level)

Mỗi dòng tương ứng với một kết cục y khoa được ghi nhận cho động vật sau khi xảy ra sự cố bất lợi.  
**Quan hệ:** Nhiều-Một ($N:1$) với bảng `reports.csv` qua khóa ngoại `unique_aer_id_number`.

| STT | Tên cột (`outcomes.csv`) | Kiểu dữ liệu | JSON Path / Nguồn gốc | Ý nghĩa & Mô tả lâm sàng | Ghi chú & Phân tích chuyên sâu |
|:---:|---|:---:|---|---|---|
| 1 | `unique_aer_id_number` | `str` | *(FK)* | Khóa ngoại liên kết về `reports.csv` | **Foreign Key** |
| 2 | `medical_status` | `str` | `outcome[].medical_status` | Kết cục lâm sàng: `Recovered/Normal`, `Died`, `Euthanized`, `Ongoing`, `Unknown` | **Phát hiện EDA quan trọng:** 30.56% bản ghi mang giá trị `'Outcome Unknown'` (thiếu ẩn); **Leakage risk** cho Q6 |
| 3 | `number_of_animals_affected` | `int/str` | `outcome[].number_of_animals_affected` | Số lượng cá thể gặp kết cục lâm sàng tương ứng | Đạt 100% đầy đủ |
| 4 | `quarter` | `str` | *(loader metadata)* | Phân vùng quý thu thập (`2025q1` đến `2026q1`) | |
| 5 | `source_file` | `str` | *(loader metadata)* | Tên tệp tin JSON gốc trong `data/raw/` | |

---

## 5. Danh mục Biến dẫn xuất chuẩn hóa (Derived Variables Dictionary)

Các biến mới được tạo ra trong quá trình Tiền xử lý (Mục 3.2, 3.4) và Kỹ nghệ đặc trưng (Feature Engineering cho Học máy Q6) trong các notebook `01`, `02a`, `02b`, `02c`, `03`:

| Biến dẫn xuất | Kiểu dữ liệu | Bảng gốc & Công thức quy đổi | Ý nghĩa lâm sàng & Mục đích sử dụng | Câu hỏi áp dụng |
|---|:---:|---|---|:---:|
| `year` | `int/str` | `original_receive_date.str[:4]` hoặc 4 ký tự đầu của `quarter` | Phân đoạn dữ liệu lịch sử năm 2025 vs. năm 2026 | Q1, Q6 |
| `age_years` | `float` | `age_min / factor` (Year: 1, Month: 12, Week: 52.18, Day: 365.25), áp dụng `AGE_PLAUSIBLE_MAX` | Chuẩn hóa toàn bộ tuổi vật nuôi về năm; cắt bỏ ngoại lai phi sinh học | Q2, Q6 |
| `weight_kg` | `float` | `weight_min * factor` (Kg: 1, Lb: 0.453592, Oz: 0.02835, Gram: 0.001), áp dụng `WEIGHT_PLAUSIBLE_MAX` | Chuẩn hóa toàn bộ thể trọng về kilôgam; cắt bỏ ngoại lai do lỗi nhập | Q2, Q6 |
| `life_stage` | `category` | Phân ngưỡng từ `age_years` theo loài: `Junior` (non), `Adult` (trưởng thành), `Senior` (già), `Unknown` | Phân tầng sinh lý để đánh giá nhóm dễ tổn thương | Q2 |
| `gender_clean` | `category` | Gộp nhãn `gender` về 3 nhóm: `Male`, `Female`, `Unknown/Mixed` | Làm sạch nhãn không nhất quán | Q2 |
| `num_drugs` | `int` | Đếm số dòng trong `drugs.csv` tương ứng với mỗi `unique_aer_id_number` | Đo lường mức độ đa trị liệu (**Polypharmacy** khi `num_drugs >= 2`) | Q2, Q4, Q6 |
| `has_off_label_use` | `int (0/1)` | Cờ nhị phân: $= 1$ nếu báo cáo có bất kỳ thuốc nào dùng sai nhãn (`off_label_use` notna hoặc `used_according_to_label == 'false'`) | Đánh giá nguy cơ dùng thuốc sai nhãn ở cấp báo cáo | Q4, Q6 |
| `used_according_to_label` | `category` | Nhãn trạng thái dùng đúng nhãn chủ đạo của báo cáo (`true`, `false`, `Unknown`) | Đặc trưng đầu vào cho mô hình phân loại | Q4, Q6 |
| `reporting_delay_days` | `float` | `(original_receive_date_dt - onset_date_dt).dt.days`, lọc trong khoảng $[0, 3650]$ ngày | Đo lường độ trễ gửi báo cáo về FDA; chỉ báo hành vi giám sát | Q1, Q6 |
| `receive_month` | `int` | `original_receive_date_dt.dt.month` ($1 \rightarrow 12$) | Khảo sát xu hướng mùa vụ trong năm và biến đầu vào cho ML | Q1, Q6 |
| `receive_week_in_q` | `int` | `((receive_dt - quarter_start).dt.days // 7 + 1)` ($1 \rightarrow 13$) | Khảo sát tổng lượng báo cáo theo tuần trong quý để đối chiếu YoY | Q1, Q6 |
| `species_group` | `category` | Ánh xạ `species` thành 3 nhóm lớn: `Dog` (Chó), `Cat` (Mèo), và `Other` (Các loài khác) | Phân tầng báo cáo để xác định Top thuật ngữ VeDDRA đặc trưng | Q1 |
| `attack_rate` (hoặc `affected_ratio`) | `float` | `number_of_animals_affected / number_of_animals_treated` ở báo cáo đàn gia súc | Tỷ lệ động vật bị ảnh hưởng trong đàn được điều trị | Q5 |
| `route_primary` | `category` | Đường dùng thuốc đầu tiên / chính trong báo cáo (`Oral`, `Topical`, `Subcutaneous`, ...) | Đặc trưng dược lý quan trọng thứ 2 trong mô hình triage | Q3, Q5, Q6 |
| `dosage_form_primary` | `category` | Dạng bào chế đầu tiên / chính của thuốc trong báo cáo | Đặc trưng phương thức đưa thuốc | Q6 |
| `top_active_ingredients` | `category` | Chuỗi hoạt chất chính của thuốc trong báo cáo; mã hóa OHE giới hạn Top 50 | Đặc trưng quan trọng nhất trong mô hình phân loại rủi ro Q6 | Q3, Q6 |
| `n_routes` | `int` | Số lượng đường dùng thuốc khác nhau xuất hiện trong cùng 1 báo cáo | Chỉ báo độ phức tạp của phác đồ điều trị | Q6 |
| `n_dosage_forms` | `int` | Số lượng dạng bào chế thuốc khác nhau trong báo cáo | Chỉ báo đa dạng phác đồ | Q6 |
| `n_atc_vet_codes` | `int` | Số lượng nhóm dược lý ATCvet khác nhau được phối hợp | Chỉ báo phối hợp nhóm thuốc điều trị | Q6 |
| `n_active_ingredients` | `int` | Số lượng hoạt chất đơn lẻ được sử dụng đồng thời | Đo lường mức độ phơi nhiễm hóa dược | Q6 |
| `serious` | `int (0/1)` | Ánh xạ nhị phân từ `serious_ae`: `True`/`1` $\rightarrow 1$; `False`/`0` $\rightarrow 0$ | Biến mục tiêu phân loại nhị phân chính thức cho bài toán ML | Q6 |

---

## 6. Danh mục Biến Loại bỏ Chống Rò rỉ Dữ liệu (Data Leakage Exclusion List)

Tuân thủ nghiêm ngặt **Yêu cầu 1 của Bài toán Học máy (Mục 3.3 Đề cương đồ án)**, các cột dưới đây **bắt buộc bị loại bỏ hoàn toàn** khỏi tập đặc trưng ($X$) của mô hình dự đoán lúc tiếp nhận hồ sơ, vì chúng đại diện cho thông tin hậu nghiệm (xảy ra sau khi sự cố bộc lộ mức độ nghiêm trọng) hoặc là khóa định danh:

1. **`serious_ae` / `serious`:** Nhãn mục tiêu ($y$) cần dự đoán, không được nằm trong ma trận đặc trưng ($X$).
2. **`outcome` / `medical_status` (bảng `outcomes.csv`):** Kết quả y khoa lâm sàng (`Died`, `Euthanized`, `Recovered`, `Ongoing`). Đây là kết quả cuối cùng sau quá trình điều trị và là thành phần trực tiếp định nghĩa tính chất nghiêm trọng của ca bệnh $\rightarrow$ Rò rỉ thông tin tương lai nghiêm trọng.
3. **`treated_for_ae` (bảng `reports.csv`):** Ghi nhận liệu động vật có phải điều trị y tế cho phản ứng phụ hay không; hành động này diễn ra sau khi phản ứng bất lợi đã biểu hiện.
4. **`duration_value` & `duration_unit` (bảng `reports.csv`):** Khoảng thời gian kéo dài của triệu chứng; chỉ có thể biết chính xác sau khi triệu chứng đã chấm dứt hoặc con vật đã hồi phục/tử vong.
5. **Mã định danh hồ sơ (`unique_aer_id_number`, `report_id`, `lot_number`):** Các chuỗi định danh hành chính mang tính ngẫu nhiên, không chứa tín hiệu sinh học hoặc gây học vẹt (overfitting).
