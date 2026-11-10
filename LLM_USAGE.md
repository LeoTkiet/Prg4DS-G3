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

---

## Mẫu ghi nhận cho các phiên tiếp theo

```markdown
### Lần <STT> — <Chủ đề công việc> (YYYY-MM-DD)
- **Thành viên:** <Họ tên & MSSV>
- **Công cụ:** <Tên công cụ / Model>
- **Đã hỏi gì:** <Tóm tắt câu hỏi hoặc lỗi cần tra cứu>
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:** <Cách nhóm kiểm chứng, sửa đổi và áp dụng vào code/notebook>
```

