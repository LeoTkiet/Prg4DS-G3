# Global Ban — Phân tích suy thoái và phục hồi thảm thực vật

> Đồ án cuối kỳ môn **CSC17104 – Programming for Data Science**, Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM.
> Drive đồ án: https://drive.google.com/drive/folders/1wzgOSg2hi_MEvgz5dCnEI01W2bJNMnE6?usp=drive_link

## Mục lục

- [Thành viên](#thành-viên)
- [Mục tiêu và dữ liệu](#mục-tiêu-và-dữ-liệu)
- [Phân công và câu hỏi nghiên cứu](#phân-công-và-câu-hỏi-nghiên-cứu)
- [Phát hiện chính](#phát-hiện-chính)
- [Quy trình làm việc và Git flow](#quy-trình-làm-việc-và-git-flow)
- [Cài đặt và chạy dự án](#cài-đặt-và-chạy-dự-án)
- [Tuyên bố sử dụng AI](#tuyên-bố-sử-dụng-ai)

## Thành viên

| Mã | Thành viên | MSSV |
|---|---|---|
| M1 | Đinh Công Khang | 24120332 |
| M2 | Trần Ngô Uyên Nhi | 24120210 |
| M3 | Huỳnh Tuấn Kiệt | 24120356 |

## Mục tiêu và dữ liệu

Dự án tìm hiểu các yếu tố liên quan đến suy thoái thảm thực vật và hiệu quả phục hồi, sau đó dùng các kỹ thuật phân tích dữ liệu để trả lời các câu hỏi mang tính định hướng giá trị (meaningful questions) góp phần hỗ trợ việc diễn giải và đề xuất hành động cấp thiết để phục hồi thảm thực vật.

- **Bộ dữ liệu:** [Vegetation Degradation and Restoration Dataset](https://www.kaggle.com/datasets/ziya07/vegetation-degradation-and-restoration-dataset), tác giả Kaggle `ziya07`.
- **Quy mô dự kiến:** 6.000 dòng và 48 cột.
- **Nội dung:** quan sát sinh thái, chỉ số viễn thám (ví dụ NDVI, SAVI, MSI, PRI, RVI), đặc điểm vùng/mùa, điều kiện đất-khí hậu, đa dạng sinh học, mức suy thoái và kết quả phục hồi.
- **Giấy phép:** CC0. Xem thông tin giấy phép và điều khoản hiện hành trên [trang bộ dữ liệu Kaggle](https://www.kaggle.com/datasets/ziya07/vegetation-degradation-and-restoration-dataset).
- **Notebook/phân tích công khai liên quan:** 
    + 01_collection_exploration.ipynb
    + 02_analysis.ipynb
    + 03_ml_question.ipynb
 

Dữ liệu tải về được đặt trong `data/raw/`, dữ liệu đã xử lý (nếu có) đặt trong `data/processed/`. Không đưa dữ liệu thô dung lượng lớn hoặc thông tin xác thực Kaggle lên Git.

## Phân công và câu hỏi nghiên cứu

Mỗi thành viên phụ trách hai câu hỏi. Người phản biện được phân công chéo để kiểm tra mã, phương pháp và mức độ căn cứ của kết luận.

| Câu | Chủ sở hữu | Người phản biện | Câu hỏi |
|---|---|---|---|
| Q1 | M1 — Khang | M3 — Kiệt | Phân bố `Degradation_Level` thay đổi thế nào theo `Region_Type` và `Season`? Vùng/mùa nào có mức suy thoái nặng nhất? |
| Q2 | M2 — Nhi | M1 — Khang | Các chỉ số phổ `NDVI`, `SAVI`, `MSI`, `PRI`, `RVI` khác nhau thế nào giữa ba mức suy thoái? |
| Q3 | M3 — Kiệt | M2 — Nhi | Các yếu tố khí hậu, đất và áp lực con người (`Drought`, `Grazing`, `Human_Disturbance`, `Soil`, `Rainfall`) liên quan thế nào đến mức suy thoái? |
| Q4 | M3 — Kiệt | M2 — Nhi | `Restoration_Age_Years` và các chỉ số phục hồi thay đổi thế nào theo `Restoration_Effect_Class`? |
| Q5 | M2 — Nhi | M1 — Khang | Đa dạng sinh học (`Species_Richness`, tỷ lệ loài bản địa/xâm lấn) khác nhau thế nào giữa các mức suy thoái và phục hồi? |
| Q6 | M1 — Khang | M3 — Kiệt | Có thể xếp hạng các `Site_ID` theo mức ưu tiên phục hồi dựa trên suy thoái cao và tiềm năng phục hồi không? |

**Phân rã công việc chính**

- **Khang (M1):** khởi tạo cấu trúc repo và notebook; EDA cấu trúc dữ liệu; phát triển Q1, Q6; tích hợp các nhánh và điều phối rà soát.
- **Nhi (M2):** tải dữ liệu và lập từ điển dữ liệu; EDA biến số; tiện ích dùng chung/feature engineering; phát triển Q2, Q5; chuẩn hóa biểu đồ và định dạng.
- **Kiệt (M3):** xác minh nguồn, giấy phép và cách thu thập; EDA biến phân loại; thiết kế/làm sạch dữ liệu và QA; phát triển Q3, Q4; kiểm tra độ vững và khả năng tái lập.
- **Cả nhóm:** thống nhất câu hỏi; rà soát chéo; kiểm tra dữ liệu sau tiền xử lý; chạy lại toàn bộ notebook; chuẩn bị trình bày, phản ánh cá nhân và tài liệu tham khảo.

## Phát hiện chính

**Chưa có phát hiện thực nghiệm để báo cáo.** Tại thời điểm viết README, ba notebook trong repo chỉ có các tiêu đề khung; chưa có CSV trong `data/`, mã phân tích, biểu đồ hay kết quả đã chạy. Vì vậy nhóm chưa thể đưa ra kết luận có số liệu mà không suy diễn.

Sau khi hoàn tất EDA và sáu câu hỏi, hãy thay phần này bằng 3–5 phát hiện có số liệu, nêu rõ nhóm so sánh/phương pháp, biểu đồ hoặc kiểm định hỗ trợ, ý nghĩa thực tiễn và giới hạn. Đặc biệt làm nổi bật phát hiện bất ngờ nhất.

## Quy trình làm việc và Git flow

1. Chia mỗi đầu việc thành task có owner, reviewer, phụ thuộc và đầu ra; cập nhật trạng thái theo `Not Started → In Progress → In Review → Done`. Nếu bị chặn, ghi rõ lý do.
2. Tạo nhánh theo task, ví dụ `feature/khang-q1` hoặc `feature/nhi-data-cleaning`; không phát triển trực tiếp trên `main`.
3. Commit theo mẫu `<TaskID>: <động từ> <nội dung>`, ví dụ `T21: clean missing values`.
4. Mở Pull Request vào `main`, mô tả thay đổi và cách kiểm tra; nhờ reviewer được phân công xem xét. Chỉ merge sau khi xử lý nhận xét và chạy các kiểm tra liên quan.
5. Tích hợp thường xuyên để giảm xung đột; sau khi merge, chạy lại notebook bị ảnh hưởng. Trước khi nộp, **Restart & Run All** theo đúng thứ tự ở dưới.
6. Một task chỉ hoàn tất khi mã chạy được, đã push/merge, có giải thích bằng văn bản và được reviewer xác nhận. Mỗi thành viên cần hiểu được toàn bộ dự án, không chỉ phần mình viết.

## Cài đặt và chạy dự án

Các lệnh dưới đây giả định đang ở thư mục `global-ban/`.

### 1. Tạo môi trường

Cần cài Miniconda hoặc Anaconda, sau đó chạy:

```powershell
conda env create -f environment.yml
conda activate ds-env
```

### 2. Tải dữ liệu

Tạo thư mục đích trong PowerShell:

```powershell
New-Item -ItemType Directory -Force data/raw, data/processed
```

Tải tệp CSV từ trang [Kaggle dataset](https://www.kaggle.com/datasets/ziya07/vegetation-degradation-and-restoration-dataset), giải nén nếu cần, rồi đặt các CSV vào `data/raw/`.

Hoặc dùng Kaggle CLI (cần quyền truy cập dataset và cấu hình API token Kaggle riêng; không commit token):

```powershell
python -m pip install kaggle
kaggle datasets download -d ziya07/vegetation-degradation-and-restoration-dataset -p data/raw --unzip
```

Trước khi chạy notebook, kiểm tra tên tệp, số dòng/cột và ghi ngày tải/nguồn dữ liệu trong phần mô tả dữ liệu. Nếu notebook sử dụng đường dẫn hoặc tên tệp cụ thể, cập nhật cho khớp tệp đã tải.

### 3. Chạy notebook theo thứ tự

Khởi động Jupyter từ thư mục `global-ban/`:

```powershell
jupyter lab
```

Mở và chạy **Restart Kernel and Run All** theo thứ tự:

1. [`notebooks/01_collection_exploration.ipynb`](notebooks/01_collection_exploration.ipynb) — nguồn dữ liệu, mô tả và khám phá ban đầu.
2. [`notebooks/02_analysis.ipynb`](notebooks/02_analysis.ipynb) — tiền xử lý và phân tích các câu hỏi không học máy.
3. [`notebooks/03_ml_question.ipynb`](notebooks/03_ml_question.ipynb) — bài toán học máy, baseline, mô hình và đánh giá.

**Trạng thái hiện tại:** các notebook mới là skeleton, chưa chứa các bước trên và chưa thể tạo kết quả dự án hoàn chỉnh. Sau khi triển khai, đảm bảo đường dẫn dữ liệu tương đối tính từ repo, cập nhật thứ tự/chuyển dữ liệu giữa notebook nếu có, rồi chạy lại từ đầu trong môi trường mới.

## Tuyên bố sử dụng AI

Nhóm được phép dùng công cụ AI như một công cụ hỗ trợ học tập, nhưng mỗi thành viên phải khai báo các phiên làm việc trong [`LLM_USAGE.md`](LLM_USAGE.md). Mỗi khai báo cần nêu **công cụ**, **đã hỏi gì**, và **đã sử dụng hoặc chỉnh sửa câu trả lời ra sao**. Thành viên phải tự kiểm chứng nội dung, trích dẫn nguồn khi cần và có khả năng giải thích phần việc của mình; không dùng AI để thay nhóm viết phần phân tích, kết luận hoặc reflection. Không đưa dữ liệu nhạy cảm, thông tin xác thực hay nội dung không được phép chia sẻ vào công cụ AI.
