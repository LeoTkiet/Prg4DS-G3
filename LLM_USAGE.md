# Nhật ký Sử dụng Công cụ AI / LLM (`LLM_USAGE.md`)

Tài liệu này ghi nhận toàn bộ các lần sử dụng công cụ AI/LLM đáng kể của các thành viên nhóm **Prg4DS-G3** trong quá trình thực hiện đồ án cuối kỳ môn **CSC17104 – Lập trình cho Khoa học Dữ liệu**, tuân thủ quy định tại **Mục 6 (Academic Integrity and Use of LLMs)** của đề cương đồ án.

## Nguyên tắc sử dụng AI của nhóm
1. Chỉ sử dụng các công cụ LLM (ChatGPT, Claude, Gemini, GitHub Copilot...) với vai trò **gia sư hỗ trợ (tutor)**: giải thích khái niệm, tra cứu cú pháp thư viện (`pandas`, `scikit-learn`, `matplotlib`), gỡ lỗi (debug) hoặc gợi ý cấu trúc tổ chức dự án.
2. **Tuyệt đối không** dùng AI để tự động viết thay phần phân tích dữ liệu, diễn giải kết quả thực nghiệm, kết luận hay phần phản ánh cá nhân (individual reflections).
3. Mọi thành viên phải hiểu và giải thích được từng dòng lệnh trong toàn bộ đồ án khi vấn đáp (Q&A).

---

## Nhật ký chi tiết (Usage Log)

### Lần 1 — Khởi tạo cấu trúc thư mục & Kế hoạch vận hành đồ án (2026-11-05)
- **Thành viên:** Huỳnh Tuấn Kiệt
- **Công cụ:** Google Antigravity (Gemini)
- **Đã hỏi gì:** Yêu cầu tái cấu trúc thư mục dự án theo đúng chuẩn Mục 4 của đề cương môn học (`CSC17104`), chuyển đổi từ báo cáo sơ bộ 1 file sang kế hoạch vận hành dữ liệu **OpenFDA Animal & Veterinary Adverse Events** giai đoạn **2020–2025** (dùng để phân tích lịch sử và huấn luyện mô hình) và **2026 Q1** (dùng làm tập kiểm thử thực tế Out-of-Time Test), đồng thời chuẩn hóa 6 câu hỏi nghiên cứu đáp ứng tiêu chí độ sâu `D1–D6` và yêu cầu bài toán ML.
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Sử dụng cấu trúc thư mục (`data/raw/`, `data/processed/`, `src/`, `notebooks/`), các file khung (`01_collection_exploration.ipynb`, `02_analysis.ipynb`, `03_ml_question.ipynb`) và bản mô tả kế hoạch vận hành trong `README.md`.
  - Nhóm sẽ tự tải dữ liệu thực tế từ cổng openFDA, tự viết mã xử lý JSON lồng nhau, chạy thực nghiệm, kiểm chứng số liệu và cập nhật kết quả phân tích.

### Lần 2 — Rút gọn phạm vi dữ liệu & chuẩn hóa tài liệu cài đặt (2026-11-07)
- **Thành viên:** Đinh Công Khang (24120332) — đại diện nhóm tổng hợp.
- **Công cụ:** OpenCode (AI coding agent).
- **Đã hỏi gì:** Điều chỉnh toàn bộ kế hoạch đồ án từ phạm vi nhiều năm xuống chỉ còn 4 quý năm 2025 để phân tích/huấn luyện, giữ nguyên 2026 Q1–Q2 làm tập kiểm thử ngoài thời gian; đồng thời rà soát `README.md` và `environment.yml` (cài môi trường, hướng dẫn dữ liệu, package trùng lặp).
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:**
  - Nhóm thống nhất loại bỏ hoàn toàn các năm trước 2025; cập nhật đồng bộ README, docstring trong `src/`, 3 notebook và mục lục.
  - Chỉnh `environment.yml` (bỏ package trùng lặp, đưa `conda-forge` lên trước, thêm `ipykernel`) và mở rộng mục 7 của README thành các bước cài đặt/kiểm tra/troubleshooting.
  - Các thay đổi được nhóm kiểm tra lại bằng `git diff` trước khi commit.

---

## Mẫu ghi nhận cho các phiên tiếp theo

```markdown
### Lần <STT> — <Chủ đề công việc> (YYYY-MM-DD)
- **Thành viên:** <Họ tên & MSSV>
- **Công cụ:** <Tên công cụ / Model>
- **Đã hỏi gì:** <Tóm tắt câu hỏi hoặc lỗi cần tra cứu>
- **Đã sử dụng hoặc chỉnh sửa câu trả lời thế nào:** <Cách nhóm kiểm chứng, sửa đổi và áp dụng vào code/notebook>
```

