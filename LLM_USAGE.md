# Nhật ký Sử dụng Công cụ AI / LLM (`LLM_USAGE.md`)

Tài liệu này ghi nhận toàn bộ các lần sử dụng công cụ AI/LLM đáng kể của các thành viên nhóm **Global Ban** trong quá trình thực hiện đồ án cuối kỳ môn **CSC17104 – Lập trình cho Khoa học Dữ liệu**, tuân thủ quy định tại **Mục 6 (Academic Integrity and Use of LLMs)** của đề cương đồ án.

## Nguyên tắc sử dụng AI của nhóm
1. Chỉ sử dụng các công cụ LLM (ChatGPT, Claude, Gemini, GitHub Copilot...) với vai trò **gia sư hỗ trợ (tutor)**: giải thích khái niệm, tra cứu cú pháp thư viện (`pandas`, `scikit-learn`, `matplotlib`), gỡ lỗi (debug) hoặc gợi ý cấu trúc tổ chức dự án.
2. **Tuyệt đối không** dùng AI để tự động viết thay phần phân tích dữ liệu, diễn giải kết quả thực nghiệm, kết luận hay phần phản ánh cá nhân (individual reflections).
3. Mọi thành viên phải hiểu và giải thích được từng dòng lệnh trong toàn bộ đồ án khi vấn đáp (Q&A).

---

## Nhật ký chi tiết (Usage Log)

### Lần 1 — Khởi tạo cấu trúc thư mục & Kế hoạch vận hành đồ án (2026-11-05)
- **Thành viên:** Huỳnh Tuấn Kiệt
- **Công cụ:** Google Antigravity (Gemini)
- **Đã hỏi gì:** Yêu cầu tái cấu trúc thư mục dự án theo đúng chuẩn Mục 4 của đề cương môn học (`CSC17104`), chuyển đổi từ báo cáo sơ bộ 1 file sang kế hoạch vận hành dữ liệu **OpenFDA Animal & Veterinary Adverse Events** giai đoạn **2025 (Q1–Q4)** (dùng để phân tích và huấn luyện mô hình) và **2026 Q1** (dùng làm tập kiểm thử thực tế Out-of-Time Test), đồng thời chuẩn hóa 6 câu hỏi nghiên cứu đáp ứng tiêu chí độ sâu `D1–D6` và yêu cầu bài toán ML.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Sử dụng cấu trúc thư mục (`data/raw/`, `data/processed/`, `src/`, `notebooks/`), các file khung (`01_collection_exploration.ipynb`, `02_analysis.ipynb`, `03_ml_question.ipynb`) và bản mô tả kế hoạch vận hành trong `README.md`.
  - Nhóm sẽ tự tải dữ liệu thực tế từ cổng openFDA, tự viết mã xử lý JSON lồng nhau, chạy thực nghiệm, kiểm chứng số liệu và cập nhật kết quả phân tích.
### Lần 2 — Soạn thảo script tải dữ liệu, module nạp/làm phẳng JSON và Data Dictionary v0 (2026-11-07)
- **Thành viên:** Trần Ngô Uyên Nhi
- **Công cụ:** Claude (Anthropic)
- **Đã hỏi gì:** Nhờ soạn bản nháp `src/download_data.py` (tải các quý 2025 Q1–Q4 và 2026 Q1 qua manifest openFDA), `src/data_loader.py` (đọc JSON/ZIP, làm phẳng thành 4 bảng `reports`, `drugs`, `reactions`, `outcomes`, loại trùng `unique_aer_id_number` giữa các quý) và `data_dictionary.md` v0.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Tự đọc và chạy từng hàm để hiểu luồng xử lý: vì sao phải đổi tên file theo quý (tên gốc các quý trùng nhau, sẽ ghi đè), vì sao giữ phiên bản ở quý muộn nhất khi trùng id, vì sao giữ nguyên dạng chuỗi và để ép kiểu ở notebook.
  - Kiểm chứng đầu ra bằng số liệu thật: so khớp số bản ghi giữa `meta.total`, `len(results)` và manifest; đối chiếu SHA-256 và `last_updated` trong `MANIFEST.json`; kiểm tra số dòng trước/sau khi loại trùng, khóa ngoại của 3 bảng con.
  - Đối chiếu Data Dictionary với dữ liệu thực tế (kiểm tra tên cột, kiểu dữ liệu, tỷ lệ khuyết) và sửa các chỗ không khớp, ví dụ tên cột trong dictionary khác tên cột do `data_loader.py` sinh ra. Dictionary hiện đánh dấu v0 và sẽ cập nhật sau EDA.
### Lần 3 — Rút gọn phạm vi dữ liệu & chuẩn hóa tài liệu cài đặt (2026-11-07)
- **Thành viên:** Đinh Công Khang (24120332) — đại diện nhóm tổng hợp.
- **Công cụ:** OpenCode (AI coding agent).
- **Đã hỏi gì:** Điều chỉnh toàn bộ kế hoạch đồ án từ phạm vi nhiều năm xuống chỉ còn 4 quý năm 2025 để phân tích/huấn luyện, giữ nguyên 2026 Q1 làm tập kiểm thử ngoài thời gian; đồng thời rà soát `README.md` và `environment.yml` (cài môi trường, hướng dẫn dữ liệu, package trùng lặp).
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Nhóm thống nhất loại bỏ hoàn toàn các năm trước 2025; cập nhật đồng bộ README, docstring trong `src/`, 3 notebook và mục lục.
  - Chỉnh `environment.yml` (bỏ package trùng lặp, đưa `conda-forge` lên trước, thêm `ipykernel`) và mở rộng mục 7 của README thành các bước cài đặt/kiểm tra/troubleshooting.
  - Các thay đổi được nhóm kiểm tra lại bằng `git diff` trước khi commit.

### Lần 4 — Xác minh giấy phép CC0, tác giả, phương pháp thu thập, hạn chế dữ liệu và công trình công khai liên quan (2026-11-09)
- **Thành viên:** Huỳnh Tuấn Kiệt (24120356)
- **Công cụ:** Google Antigravity
- **Đã hỏi gì:** Xác minh giấy phép CC0 1.0 Universal, tác giả/tổ chức phát hành (FDA CVM), nguồn gốc (openFDA manifest & API), phương pháp thu thập thực tế của dữ liệu Cảnh giác dược Thú y (thay cho mô tả remote sensing + field survey của đề xuất cũ), quần thể (population), phạm vi thời gian (2025 Q1–Q4 & 2026 Q1), các hạn chế/thiên lệch (limitations/biases), liệt kê các công trình/notebook/repo công khai liên quan kèm điểm khác biệt của đồ án nhóm, và đồng bộ bảng schema CSV giữa `README.md`, `data/data_dictionary.md` với `src/data_loader.py`.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Đối chiếu trực tiếp với trang giấy phép (`open.fda.gov/license`), điều khoản sử dụng (`open.fda.gov/terms`) và quy trình báo cáo của FDA CVM: báo cáo bắt buộc 21 CFR 514.80 (Form FDA 1932) qua cổng **FDA Electronic Submissions Gateway (ESG / ESG NextGen)** với chuẩn **HL7 ICSR** theo **VICH GL35** (*CVM GFI #214*), và báo cáo tự nguyện qua biểu mẫu PDF **Form FDA 1932a** hoặc **Rational Questionnaire** trên **Safety Reporting Portal (SRP)**.
  - Cập nhật chi tiết Mục 2 (`2.1`–`2.6`) trong `README.md`, Mục 1 (`1.1`–`1.6`) trong `notebooks/01_collection_exploration.ipynb` và `data/data_dictionary.md`: làm rõ chỉ khử trùng lặp phòng ngừa theo `unique_aer_id_number` (không dedupe theo `report_id` vì đó là mã đơn đăng ký thuốc NADA/ANADA), đồng bộ đầy đủ tên cột thực tế của 4 bảng `.csv` (bao gồm `source_file`, `quarter`, `species`, `age_min`, `active_ingredients`, `dose_*`, `frequency_*`...), và đối sánh chính xác với 4 nhóm công trình công khai (`openFDA Interactive Chart`, `FDA/openfda` & `VetClaw`, bài báo `arXiv:2510.01520` dùng đặc trưng hóa lý PubChem, cùng nghiên cứu của Xu et al., 2019 và Farrell et al., 2025 trên EudraVigilance Veterinary — EVV).

### Lần 5 — Triển khai Mục 2.1 EDA Tổng quan & Kiểm tra Toàn vẹn Schema trong Notebook 01 (Task T08) (2026-11-13)
- **Thành viên:** Trần Ngô Uyên Nhi (`24120210`)
- **Công cụ:** Google Antigravity (Gemini)
- **Đã hỏi gì:** Hướng dẫn xây dựng các hàm kiểm tra và trực quan hóa tổng quan 4 bảng (`reports`, `drugs`, `reactions`, `outcomes`) theo yêu cầu Mục 3.2 của đề cương: thống kê kích thước (shape) và bộ nhớ, kiểm tra tính duy nhất của khóa chính `unique_aer_id_number`, phân biệt với `report_id`, kiểm tra khóa ngoại/khóa mồ côi (orphan keys), trùng lặp, bảng kế hoạch chuyển đổi kiểu dữ liệu và danh sách loại trừ cột hậu nghiệm chống rò rỉ dữ liệu (Data Leakage) cho bài toán ML.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Áp dụng các đoạn mã kiểm tra toàn vẹn dữ liệu vào Mục 2.1 của `notebooks/01_collection_exploration.ipynb`: xác nhận 0 khóa mồ côi (`orphan_rows = 0`), kiểm tra độ bao phủ 89.66% của bảng `outcomes`.
  - Viết module trực quan hóa dùng chung `src/visualization.py` (`plot_quarterly_volume`, `plot_missing_overview`) và tự chạy lại trên toàn bộ 94,412 dòng để ghi nhận số liệu thực tế vào các markdown note.
  - Tự rà soát và bổ sung biện giải chuyên môn về lý do loại trừ các cột hậu nghiệm (`outcomes`, `treated_for_ae`, `duration`) để bảo vệ tính toàn vẹn của mô hình ML Q6.

### Lần 6 — Tinh chỉnh Hệ thống Câu hỏi Q2 & Q5, Tái cấu trúc Module và Hoàn thiện EDA Đào sâu T10 (2026-11-15)
- **Thành viên:** Trần Ngô Uyên Nhi (`24120210`)
- **Công cụ:** Google Antigravity (Gemini & Claude)
- **Đã hỏi gì:**
  - Nhận xét và phản biện hệ thống 6 câu hỏi nghiên cứu: Đánh giá câu hỏi sinh học Q2 và đề xuất thay thế câu hỏi Q5 cũ (về độ trễ báo cáo) bằng câu hỏi dịch tễ đàn gia súc/gia cầm mới (*"Những yếu tố nào có liên quan đến tỷ lệ động vật bị ảnh hưởng trong tổng số động vật được điều trị ở mỗi đàn?"*).
  - Đồng bộ phát biểu tiếng Việt chính thức của Q2 và Q5 trên toàn bộ tài liệu dự án (`README.md`, `data/data_dictionary.md`, `notebooks/02_analysis.ipynb`).
  - Hỗ trợ xây dựng các cell phân tích cho Task T10 trong `notebooks/01_collection_exploration.ipynb`: quy đổi tuổi/cân nặng sinh học, trích xuất 964 báo cáo đàn hợp lệ để tính `attack_rate = affected / treated`, phân tích phân phối ngoại lai, kiểm tra cơ chế MAR.
  - Tham vấn giải pháp tái cấu trúc kiến trúc Notebook 01 thành các phân đoạn module riêng biệt theo thành viên (`2.2` Nhi, `2.3` Kiệt, `2.4` Khang) nhằm tránh xung đột Git (merge conflict) khi làm việc nhóm và tinh giản các phân tích thống kê suy diễn để dành cho Notebook 02.
  - Khắc phục cảnh báo `FutureWarning` trong Seaborn v0.13+ khi dùng `palette` không kèm `hue`.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Nhóm thảo luận và thống nhất thay thế câu Q5 sang phân tích dịch tễ đàn gia súc/gia cầm vì đây là hướng đi đột phá, khai thác được các trường `number_of_animals_treated` và `number_of_animals_affected` thay vì chỉ tập trung vào chó/mèo.
  - Kiểm tra trực tiếp trên dữ liệu: xác nhận 964 báo cáo đàn hợp lệ có `treated > 0`, phát hiện 13 ca ngoại lai `attack_rate > 1` (do sai lệch ghi nhận) để làm cơ sở cho bước kiểm tra độ vững D6.
  - Áp dụng cấu trúc module hóa vào Notebook 01: tinh giản bớt phần kiểm định Wilson CI và Kruskal-Wallis (đưa sang `02_analysis.ipynb`), giữ lại trực quan phân phối và tương quan ban đầu.
  - Sửa lỗi cú pháp Seaborn bằng cách gán `hue="species"` và `legend=False` ở các ô vẽ biểu đồ.
  - Tự kiểm tra lại toàn bộ file notebook bằng lệnh kiểm tra cú pháp và git diff trước khi commit.

---

### Lần 7 — Phản biện Q1/Q6 và xây dựng EDA chuyên sâu Task T08 (NB02, NB03) (2026-11-16)
- **Thành viên:** Đinh Công Khang (24120332) — với hỗ trợ từ AI coding agent.
- **Công cụ:** OpenCode (model: opencode/big-pickle).
- **Đã hỏi gì:** Nhận xét/phản biện hệ thống 6 câu hỏi nghiên cứu trong `README.md` (trọng tâm Q1, Q6); xây dựng các cell phân tích EDA chuyên sâu cho Task T08 trong `notebooks/02_analysis.ipynb` (Q1) và `notebooks/03_ml_question.ipynb` (Q6); sửa `FutureWarning` groupby/pivot Categorical, định dạng bảng bằng `display()`, và xử lý hiển thị `veddra_term_name` quá dài.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Đã rà soát nội dung phản biện (phạm vi, thiên lệch dữ liệu tự nguyện, giới hạn suy luận mùa vụ/nhân quả, leakage & drift cho Q6) và điều chỉnh cho phù hợp với rubric/đề tài trước khi áp dụng.
  - Các cell notebook do AI gợi ý/sinh (load & join `reports`↔`reactions`/`drugs`, `log_row_count_change`, tỷ trọng theo loài×quý, bootstrap CI, χ²/Cramér’s V, EDA nhãn `serious_ae`, tín hiệu sinh học/bối cảnh, so sánh train 2025Q1–Q4 vs test 2026Q1) cần được **chạy lại trên dữ liệu thực tế**, kiểm chứng số liệu/biểu đồ, đơn vị quan sát và giả định thống kê; tuyệt đối không dùng `outcome`/`treated_for_ae`/`duration` làm đặc trưng dự báo Q6.
  - Các chỉnh sửa trình bày (`display/style`, `observed=True`, rút gọn nhãn VeDDRA khi hiển thị nhưng giữ giá trị gốc cho phân tích) đã được áp dụng vào notebook và cần được kiểm tra trực quan/khả năng tái lập (Restart Kernel & Run All) trước khi commit.

### Lần 8 — Khắc phục lỗi phản biện tiền xử lý Q1/Q6, tối ưu hóa pipeline ML NB03 và đồng bộ toàn diện Data Dictionary v2 & README (2026-11-23)
- **Thành viên:** Đinh Công Khang (`24120332`)
- **Công cụ:** Google Antigravity (Gemini 2.5 Pro)
- **Đã hỏi gì:**
  - Hỗ trợ gỡ lỗi và giải quyết các phản biện của reviewer (LeoTkiet) trên nhánh `feat/khang-preprocessing` về phần tiền xử lý cho 2 câu hỏi Q1 và Q6:
    - Trong `notebooks/01_collection_exploration.ipynb`: Khắc phục cảnh báo `SettingWithCopyWarning` tại Cell 27 bằng `.copy()` và bổ sung nhãn trục Y; chuẩn hóa logic nhận diện thiếu ẩn tại Cell 41 bằng regex `_PLACEHOLDER_PAT`; thay thế phương thức `.join()` bằng `pd.merge()` tại Cell 48 để loại bỏ cảnh báo `Pandas4Warning`.
    - Trong `notebooks/03_ml_question.ipynb`: Bổ sung import `clone` từ `sklearn.base`; bổ sung bộ lọc cá thể người (`species != 'Human'`), ngưỡng giới hạn sinh học hợp lý (`age_years <= 35`, `weight_kg <= 1200`), ép kiểu số và gắn nhãn `has_off_label_use`; giải quyết dứt điểm lỗi cạn kiệt bộ nhớ (OOM) và lỗi ma trận thưa không tương thích với `HistGradientBoostingClassifier` bằng cấu hình `OneHotEncoder(sparse_output=False, max_categories=50)`; xử lý lỗi không tương thích giữa `cross_val_predict` và `TimeSeriesSplit` bằng cách lập trình vòng lặp thủ công tạo Out-of-Fold (OOF) predictions trên tập huấn luyện 2025; cập nhật các số liệu định lượng thực nghiệm chính xác vào markdown kết quả.
  - Tự đánh giá và hoàn thiện tiêu chuẩn tiền xử lý theo rubric đồ án cho hai câu hỏi Q1 (tiêu chí D1, D2, D5) và Q6 (đầy đủ 6 tiêu chuẩn ML: Leakage prevention, Time-based split, Pipeline & Models comparison, Cross-validation OOF, Error Analysis, Permutation Importance).
  - Cập nhật và đồng bộ hóa tài liệu dự án:
    - Nâng cấp [data/data_dictionary.md](data/data_dictionary.md) lên phiên bản **v2**: Thống kê đầy đủ 77 cột dữ liệu gốc qua 5 quý (94.412 báo cáo, 174.123 thuốc, 270.244 phản ứng, 85.143 kết cục), bổ sung các cột còn thiếu (`foreign_or_domestic`, `time_between_exposure_and_onset`, 10 cột đặc trưng thuốc trong `drugs.csv`), ghi nhận tỷ lệ khuyết thiếu ẩn ở `outcomes.csv` (30.56% 'Outcome Unknown'), lập bảng 21 biến dẫn xuất chuẩn hóa và danh sách loại trừ biến hậu nghiệm chống rò rỉ dữ liệu ML.
    - Cập nhật [README.md](README.md): Cập nhật Mục 2.4 (quy mô 77 cột, 4 bảng CSV và link dictionary v2), Mục 3 (kiến trúc module phân tách các sub-notebooks `02a`, `02b`, `02c`), Mục 5 (đánh dấu hoàn thành Giai đoạn 1, 2 và thực nghiệm Giai đoạn 4), Mục 6 (thay thế số liệu sơ bộ mẫu 14.826 dòng bằng các phát hiện định lượng thực tế toàn diện từ 94.412 báo cáo EDA và kết quả mô hình ML Q6: PR-AUC 0.7901, ROC-AUC 0.8384, Recall 82.23% tại ngưỡng OOF 0.365), Mục 7.4 (hướng dẫn thực thi tuần tự các notebook).
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Tự thực thi chạy lại toàn bộ notebook 01, notebook 02 và notebook 03 ("Restart Kernel and Run All"), xác nhận 100% cell hoàn tất không lỗi và lưu trữ đầy đủ output/biểu đồ.
  - Rà soát cẩn trọng pipeline tiền xử lý và tham số mô hình (`OneHotEncoder`, `HistGradientBoostingClassifier`, `TimeSeriesSplit`) để đảm bảo không rò rỉ dữ liệu (Data Leakage) và cố định seed `random_state=42` đảm bảo tính tái lập (Reproducibility).
  - Toàn bộ số liệu và thông tin cập nhật trong `data_dictionary.md` và `README.md` được đối chiếu chéo với schema thực tế từ `src/data_loader.py` và bảng kết quả chạy thực nghiệm trước khi ghi nhận.

### Lần 9 — Sửa và kiểm chứng pipeline ML Q6 trong NB03 bằng Build mode (2026-11-26)
- **Thành viên:** Đinh Công Khang (`24120332`)
- **Công cụ:** ChatGPT Codex (Build mode)
- **Đã hỏi gì:** Áp dụng trực tiếp năm bản sửa từ phiên phản biện phần học máy Q6 trong `notebooks/03_ml_question.ipynb` và kiểm chứng kết quả trên dữ liệu hiện có.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Codex trực tiếp sửa mã kiểm định cuốn chiếu theo quý trong năm 2025, tách tập chấm điểm toàn bộ báo cáo Q1/2026 khỏi nhóm có nhãn dùng để tính chỉ số và sửa cờ `has_off_label_use` để nhận trường hợp `used_according_to_label = false`.
  - Codex trực tiếp sửa phần phân tích và các dòng in kết luận trong notebook. Các sửa đổi gồm dùng tỷ lệ dương trên tập test làm đường cơ sở AP, tính recall và chênh lệch tỷ lệ nhãn từ dữ liệu, thay câu kết luận cố định về xu hướng bằng đối chiếu dự báo cơ sở cùng kỳ theo tuần/tháng và báo cáo số gắn cờ triage riêng.
  - Codex đối chiếu số lượng và sai số dự báo với CSV, chạy lại các cell huấn luyện và đánh giá bằng Python, rồi kiểm tra riêng hai dòng in AP và recall đã cập nhật. Lần chạy xác nhận 17.182 báo cáo được chấm điểm, trong đó 15.376 có nhãn dùng để đánh giá. Output cũ được xóa khỏi notebook.

---

### Lần 10 — Hỗ trợ kỹ thuật thống kê, thuật toán tối ưu và khung phân tích cho Câu hỏi Q2 (2026-11-27)
- **Thành viên:** Trần Ngô Uyên Nhi (`24120210`)
- **Công cụ:** Google Antigravity (Gemini)
- **Đã hỏi gì:**
  - Các phương pháp thống kê suy diễn nhằm đáp ứng tiêu chí độ sâu `D3–D6` theo rubric:
    - Thuật toán IRLS (Iteratively Reweighted Least Squares) giải bài toán Hồi quy Logistic Đa biến trực tiếp bằng `numpy`/`scipy`, kèm tính toán ma trận hiệp phương sai tiệm cận Fisher Information để xuất sai số chuẩn Wald, 95% CI và p-value và một số thuật toán liên quan.
    - Công thức và code mẫu tính kiểm định Cochran-Mantel-Haenszel (CMH pooled Odds Ratio) cùng phương sai Robins-Breslow-Greenland để kiểm soát biến gây nhiễu `polypharmacy_group` theo phân tầng loài.
    - Vẽ biểu đồ Forest Plot trực quan hóa aOR và 4 kịch bản kiểm tra độ vững D6 (Robustness/Sensitivity checks) bằng `matplotlib`.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - **Sử dụng có chọn lọc & đối chiếu thuật toán:** Thành viên kiểm tra lại từng công thức toán học của IRLS và CMH do AI gợi ý, đối chiếu với lý thuyết thống kê để hiểu rõ cơ chế ước lượng trước khi đưa vào notebook; tự kiểm tra và chạy thử nghiệm các bước tiền xử lý với `log_row_count_change()` để kiểm soát số lượng dòng dữ liệu thực tế (58.634 ca Chó và 12.973 ca Mèo).
  - **Tự thực hiện phân tích và viết biện giải độc lập:** đọc và phân tích bảng số liệu thực nghiệm (các giá trị aOR, p-value, tỷ lệ biến cố), từ đó tự biên soạn và chỉnh sửa toàn bộ phần diễn giải kết quả, ý nghĩa lâm sàng thú y, bàn luận về phát hiện bất ngờ và các hạn chế dữ liệu trong notebook [02_q2_analysis.ipynb](notebooks/02_q2_analysis.ipynb) theo văn phong và nhận định chuyên môn cá nhân.

---

### Lần 11 — Hoàn thiện phân tích Câu hỏi Q5 và đồng bộ phát hiện (2026-11-27)
- **Thành viên:** Trần Ngô Uyên Nhi (`24120210`)
- **Công cụ:** GitHub Copilot (Copilot SDK in VS Code)
- **Đã hỏi gì:** Rà lỗi và chạy lại `notebooks/02_q5_analysis.ipynb`, thay phần ghi nhận placeholder bằng kết quả thực tế, bổ sung phát hiện Q5 vào notebook tổng hợp `02_analysis.ipynb`, cập nhật biến dẫn xuất mới vào `data/data_dictionary.md`.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Chạy notebook bằng `nbconvert --execute` trên dữ liệu sạch thực tế và sửa tương thích Matplotlib (`tick_labels` thay cho `labels`) để hoàn tất biểu đồ.
  - Xác nhận dữ liệu phân tích gồm 964 báo cáo đàn hợp lệ, trong đó có 801 báo cáo Cattle và 1 ca ngoại lai `attack_rate > 1` (`1.2857`).
  - Ghi nhận các kết quả thực nghiệm và phân tích dựa trên đó.

---

### Lần 12 — Triển khai và hoàn thiện phản biện phân tích chuyên sâu Câu hỏi Q3 (Tỷ suất đồng xuất hiện ROR Hoạt chất × Triệu chứng: Safety Issue vs. LOEE — Task T17) (2026-11-27)
- **Thành viên:** Huỳnh Tuấn Kiệt (`24120356`)
- **Công cụ:** Google Antigravity
- **Đã hỏi gì:**
  - Tham vấn thiết kế pipeline phân tích bất cân xứng cảnh giác dược cho Câu hỏi Q3 trong `notebooks/02_q3_analysis.ipynb` đáp ứng 4 tiêu chí độ sâu **D1, D2, D4, D5**: chuẩn hóa danh pháp hoạt chất đơn lẻ từ các chế phẩm phối hợp (`;`, `,`, `/`), hợp nhất các bí danh viết tắt của thuốc nhỏ tai (`Gentamicin`, `Mometasone Furoate`, `Clotrimazole`, `Posaconazole`) và gộp mã thương mại vắc-xin Lyme USDA (`Recombitek Lyme - 2126.R0` cùng `Recombinant E. Coli BL21/ECL19`) về kháng nguyên chuẩn `Borrelia Burgdorferi Ospa (Recombinant E. Coli)`, khử trùng lặp cấp báo cáo `(unique_aer_id_number, ingredient)` và `(unique_aer_id_number, veddra_term_name)` để chống bùng nổ tổ hợp (Cartesian explosion).
  - Cải tiến hàm `compute_disproportionality_table()` theo góp ý phản biện: loại bỏ cách lọc cứng theo tần suất thô (`top_exp_n`, `top_rea_n`), chuyển sang kiểm định bảng liên hợp $2 \times 2$ trên toàn bộ không gian giả thuyết $(E, R)$ thỏa ngưỡng cỡ mẫu tối thiểu ($n_{\text{exp}} \ge 50, n_{\text{rea}} \ge 50, a \ge 20$), áp dụng hiệu chỉnh đa kiểm định Benjamini–Hochberg FDR ($q_{\text{FDR}} < 0.05$) trên toàn bộ $M$ cặp kiểm định rồi mới trích Top 15 theo ROR; đồng thời tách riêng phân tích đường dùng (`route`, sau khi `.dropna(subset=["route"])` từ `drg_q3_valid`) thành hai bảng độc lập cho **Safety Issue** và **LOEE**.
  - Hỗ trợ kiểm tra công thức ước lượng **Cochran–Mantel–Haenszel ($\text{ROR}_{\text{MH}}$)** và phương sai Robins–Breslow–Greenland phân tầng theo loài (`Dog` vs. `Cat`) khi có tầng rỗng ($a_k = 0$), đồng thời tinh chỉnh bố cục trục logarit và hộp chú giải (Legend) trên `Hình 3.1`, `Hình 3.2`, `Hình 3.3`.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Tự chạy thực nghiệm trên tập dữ liệu sạch lõi T14 (`67,831` báo cáo lâm sàng năm 2025, `67,365` báo cáo khớp hoạt chất [`99.31%`] và `64,095` báo cáo khớp đường dùng [`94.49%`]), in rõ quy mô không gian kiểm định $M$ và số cặp đạt đồng thời $q_{\text{FDR}} < 0.05$ & $\text{CI}_{\text{low}} > 1.0$ ngay trước mỗi bảng Top 15 (`Safety Issue`: $M = 3,372 \rightarrow 1,996$ cặp đạt chuẩn; `LOEE`: $M = 203 \rightarrow 142$ cặp đạt chuẩn; `Route × Safety`: $M = 1,291 \rightarrow 592$ cặp; `Route × LOEE`: $M = 64 \rightarrow 31$ cặp).
  - Hiệu chỉnh hàm `compute_mantel_haenszel_species()` để tính tổng trọng số $R_k = a_k d_k / N_k$ và $S_k = b_k c_k / N_k$ trực tiếp trên số đếm nguyên gốc (không cộng $+0.5$ vào tầng có $a_k = 0$), giúp `Velagliflozin × Ketosis` ($a_{\text{Cat}} = 530, a_{\text{Dog}} = 0$) khớp chính xác $\text{ROR}_{\text{MH}} = \text{ROR}_{\text{Cat}} = 14.64$ (loại bỏ $-78.1\%$ độ phóng đại giả tạo do gộp mẫu số của Chó) và phát hiện nhiễu loài đảo chiều ở `Selamectin × LOEE - flea` ($\text{ROR}_{\text{MH}} = 1.77 < 2.0$).
  - Chuẩn hóa thuật ngữ diễn giải xuyên suốt phần thảo luận và kết luận: sử dụng chính xác thuật ngữ **tín hiệu báo cáo mất cân đối mạnh (*strong disproportionality signal*)** thay vì quy kết quan hệ nhân quả trực tiếp, phân biệt rõ nhóm kém hiệu quả thuốc (`LOEE`) với biến cố bất lợi lâm sàng thực sự (`Safety Issue`), và đồng bộ toàn bộ số liệu giữa `02_q3_analysis.ipynb` với Master Hub `02_analysis.ipynb`.

---

### Lần 13 — Triển khai phân tích chuyên sâu Câu hỏi Q4 (Dùng thuốc sai nhãn Off-label, Đa trị liệu & Kết cục y khoa — Task T18) (2026-11-27)
- **Thành viên:** Huỳnh Tuấn Kiệt (`24120356`)
- **Công cụ:** Google Antigravity
- **Đã hỏi gì:**
  - Tham vấn xây dựng pipeline phân tích Câu hỏi Q4 trong `notebooks/02_q4_analysis.ipynb` đáp ứng 4 tiêu chí độ sâu **D1, D3, D4, D6**: tổng hợp trạng thái nhãn thuốc (`label_status`: `On-label Only`, `Off-label`, `Missing/Unknown`) và 7 nhóm hành vi sai nhãn cụ thể (`off_label_use`) từ bảng `drugs` cùng thứ bậc kết cục xấu nhất (`worst_outcome_rank`) từ bảng `outcomes` về cấp báo cáo 1:1.
  - Hỗ trợ kiểm tra công thức phân tầng **Cochran–Mantel–Haenszel ($\text{aOR}_{\text{MH}}$)** qua $3 \times 3 = 9$ tầng (`species_group` $\times$ `reporter_group`), thuật toán **IRLS (Newton–Raphson)** cho Hồi quy Logistic Đa biến có số hạng tương tác ($\text{Off-label} \times \text{Polypharmacy}$), phương pháp tính phương sai tổ hợp tuyến tính $\mathbf{c}^T \mathbf{\Sigma} \mathbf{c}$ cho $\text{aOR}_{\text{joint}}$, thiết kế 9 kịch bản kiểm định độ vững **D6**, và căn chỉnh bố cục nhãn trên `Hình 4.1`, `Hình 4.2`, `Hình 4.3`.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Tự thực thi và kiểm chứng số dòng qua 9 bước `log_row_count_change()` trên `76,630` báo cáo năm 2025 (`50,588` ca Complete-case biết `serious_ae`, `36,709` ca Complete-case biết kết cục lâm sàng) và tập kiểm chứng độc lập `2026 Q1`.
  - Chuyển phép tính $p$-value Wald sang `2.0 * scipy.stats.norm.sf(abs(z))` để tránh hiện tượng tràn số dưới (underflow về `0.00e+00`) khi $|z|$ lớn, đồng thời bổ sung bảng phân rã 7 hành vi sai nhãn cụ thể (`Species Off-Label` có tỷ lệ tử vong/an tử cao nhất `25.09%`, gấp `3.28` lần chuẩn On-label `7.65%`; `Indication Off-Label` có tỷ lệ nghiêm trọng cao nhất `61.58%`) và phân tích cơ chế khuyết MNAR/MAR ở nhóm `Animal Owner` khuyết nhãn (tử vong `27.23%`).
  - Tinh chỉnh tọa độ nhãn theo đỉnh thanh sai số `m_val + e_val + 0.8` ở `Hình 4.1`, tách hướng `xytext` các điểm sát nhau ở `Hình 4.2a` và mở rộng `ylim` ở `Hình 4.2b` & `Hình 4.3a` để hộp chú giải (Legend) không che khuất dữ liệu; cập nhật đồng bộ tóm tắt phát hiện Q4 vào Master Hub `02_analysis.ipynb`.

---

### Lần 14 — Rà soát chuyên sâu và hiệu chỉnh Q1 theo phản biện PR #22 (2026-11-26 → 2026-11-28)
- **Thành viên:** Đinh Công Khang (`24120332`)
- **Công cụ:** OpenCode (AI coding agent; model `opencode/big-pickle`)
- **Đã hỏi gì:**
  - Nhờ đóng vai reviewer Data Science cấp cao, chỉ báo cáo vấn đề thật trong `notebooks/02_q1_analysis.ipynb` theo định dạng: mức độ nghiêm trọng, dòng code, đầu vào/tình huống gây ra, và diff tối thiểu.
  - Sau đó yêu cầu áp dụng các phát hiện đó; đồng thời khôi phục 2 cell code đầu về đúng template gốc với đường dẫn `data/processed/clean`, thêm dòng lựa chọn phương pháp trong Mục 2 và ghi nhận lần sử dụng AI vào `LLM_USAGE.md`.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Không áp dụng ngay nhận xét: chạy lại notebook và kiểm chứng từng phát hiện trên dữ liệu thực (9.719 báo cáo `With no Adverse Events`, 58 bản ghi `Other` không rõ loài, mẫu số robustness của `Other` 9.809 → 1.796, v.v.) trước khi quyết định sửa.
  - Áp dụng diff có biên tập: gộp bộ lọc vào cell tiền xử lý kèm log số dòng; thêm `n_all`/`n_no_defect` vào bảng robustness; đổi lệnh `display()` để liệt kê đủ Top 10; giữ nguyên chữ ký 12 cell, metadata và 2 cell code đầu của template.
  - Phát hiện vấn đề phát sinh sau khi lọc (ô kỳ vọng χ² của `Other` chỉ 2,3) nên điều chỉnh còn 6 term cho riêng nhóm này, chạy lại toàn bộ 5 cell code và viết lại markdown kết quả theo số liệu output thực tế (`Lack of efficacy - NOS` 596/1.814 = 32,86%; χ² p = 0,133).
  - Đối chiếu với `git show HEAD:notebooks/02_q1_analysis.ipynb` để xác nhận cấu trúc/metadata không đổi; chỉ ghi nhận vào nhật ký những nội dung đã kiểm chứng bằng thực thi và số liệu thực tế.
  - Xử lý phản biện vòng 2 của PR #22: khôi phục 5 notebook ngoài phạm vi Q1 về `git merge-base HEAD origin/main` (tránh xung đột với PR #24/#25/#20/#21 đã merge), giữ PR chỉ còn `02_q1_analysis.ipynb` và `LLM_USAGE.md`.
  - Sửa `shorten_term()` để ưu tiên giữ hậu tố phân biệt (`- heartworm`, `- hookworm`, `- flea`) trên legend; mở rộng `xlim` của biểu đồ 1/3 và đặt lại tọa độ nhãn `2026 Q1` theo `ylim` thực tế, đồng thời thêm nhãn trục X cho biểu đồ 2. Chạy lại toàn bộ notebook để cập nhật 3 ảnh PNG.
  - Chú thích rõ `Binomial(n, p_hat)/n` tương đương bootstrap nhị phân có hoàn lại; đối chiếu lại CI Mèo `12,11%` giữa output và markdown.
  - (Đã chuẩn hóa lại số thứ tự toàn bộ nhật ký liên tục 1–16 theo trình tự thời gian sau khi tất cả PR #20–#25 được merge vào `main`.)

---

### Lần 15 — Hoàn thiện NB03 theo phản biện PR #23 của LeoTkiet (2026-11-28)
- **Thành viên:** Đinh Công Khang (`24120332`)
- **Công cụ:** OpenCode (model: opencode/big-pickle).
- **Đã hỏi gì:** Áp dụng trọn vẹn ba nhóm nhận xét trong comment phản biện PR #23 (Mục 2–3) cho `notebooks/03_ml_question.ipynb`: làm liền mạch chuỗi kiểm toán số dòng (10.096 hồ sơ khuyết nhãn và 17.182 hồ sơ được chấm điểm), bổ sung tải lượng triage trên toàn bộ hồ sơ và phục hồi/chuẩn hóa trực quan hóa cùng kết luận định lượng.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - AI rà soát comment review và đối chiếu trực tiếp từng cell của NB03 trước khi đề xuất sửa; nhóm kiểm chứng lại bằng cách chạy lại toàn bộ notebook (Restart & Run All) và đọc output thực tế.
  - Cell 4 bổ sung `ML_label_filter` (93.812 → 83.716, ghi rõ 8.290 ca 2025 + 1.806 ca 2026 Q1), `ML_score_2026Q1` (15.376 → 17.182) và bảng tổng hợp theo quý với `n_reports`, `n_labeled`, `n_missing_label`, `n_scored`; các con số được tính từ dữ liệu thay vì ghi cứng.
  - Cell 9 ép kiểu số đếm về `int`, đổi `error` thành `error_serious_2026_minus_2025`, đổi `serious` thành `n_serious_labeled`, thêm `n_flagged_all_scored` từ `all_scores_2026`, đồng thời khôi phục biểu đồ đường so sánh tuần 2025 Q1 vs 2026 Q1 (có tiêu đề, nhãn trục, đơn vị và chú thích mẫu).
  - Cell 8 và Cell 11 chuẩn hóa nhãn trục tiếng Việt, đưa `n = 15.376` vào tiêu đề, vẽ đường cơ sở AP = 0,4257 trên PR curve và bổ sung nhãn trục Y cho biểu đồ Permutation Importance; kết luận mục 4 in trực tiếp MAE tuần/tháng, chênh lệch tháng 1–3 và tuần 12–13 từ `baseline_errors`.
  - Toàn bộ cell chạy không có lỗi; số liệu định lượng trong output được sinh lại từ dữ liệu và đồng bộ với kết luận trong notebook (có chênh nhẹ so với lần chạy trước do khác phiên bản scikit-learn trong môi trường tái lập).

---

### Lần 16 — Rà soát tổng thể `README.md`, chuẩn hóa thứ tự `LLM_USAGE.md`, cập nhật `environment.yml` & tạo slide thuyết trình (2026-11-29)
- **Thành viên:** Huỳnh Tuấn Kiệt (`24120356`)
- **Công cụ:** Google Antigravity
- **Đã hỏi gì:**
  - Hỗ trợ dựng bản nháp slide thuyết trình tổng hợp dữ liệu và phân tích Q1–Q6 (xuất bản Canva, PDF và PPTX để nhóm chỉnh sửa).
  - Rà soát đối chiếu `README.md` theo yêu cầu đề cương môn học và kết quả thực nghiệm cuối cùng trên nhánh `main` (sau khi merge PR #20–#25).
  - Chuẩn hóa lại thứ tự đánh số trong `LLM_USAGE.md` (khắc phục trùng lặp `Lần 9`, `Lần 10` phát sinh khi merge song song các PR) và rà soát thư viện còn thiếu trong `environment.yml`.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Bổ sung tóm tắt đầy đủ **Key Findings của Q1–Q5** vào Mục `6.2` và đồng bộ số liệu cuối cùng của **Q6 (PR #23)** (`AP 0.7908`, `ROC-AUC 0.8385`, ngưỡng `0.396`, `Recall 78.99%`, `MAE 89.5 ca/tuần`) vào `README.md`, đối chiếu trực tiếp với output thực tế trong `02_analysis.ipynb` và `03_ml_question.ipynb`.
  - Sắp xếp theo trình tự thời gian và đánh số liên tục `Lần 1` đến `Lần 16` trong `LLM_USAGE.md`, bảo toàn nguyên văn nội dung khai báo của từng thành viên.
  - Quét tự động toàn bộ `import` trong `src/` và `notebooks/`, bổ sung `jinja2` (cho `pandas.DataFrame.style`), `nbconvert` và ràng buộc phiên bản tối thiểu (`pandas>=2.0`, `matplotlib>=3.9` cho `tick_labels`, `seaborn>=0.13`, `scikit-learn>=1.4`) vào `environment.yml`.

---

## Mẫu ghi nhận cho các phiên tiếp theo

```markdown
### Lần <STT> — <Chủ đề công việc> (YYYY-MM-DD)
- **Thành viên:** <Họ tên & MSSV>
- **Công cụ:** <Tên công cụ / Model>
- **Đã hỏi gì:** <Tóm tắt câu hỏi hoặc lỗi cần tra cứu>
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:** <Cách nhóm kiểm chứng, sửa đổi và áp dụng vào code/notebook>
```

