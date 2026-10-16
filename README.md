# billocr

Ứng dụng LLM đọc ảnh hóa đơn và trích xuất `company`, `date`, `address`, `total` thành JSON, gọi model free qua OpenRouter, đánh giá trên SROIE 2019.

Cài đặt: tạo `.env` với `OPENROUTER_API_KEY=...`, cài `openai python-dotenv pillow kagglehub`, tải dữ liệu bằng `kagglehub.dataset_download("urbikn/sroie-datasetv2")` rồi đặt vào `data/`. Chạy: `python ocr_eval.py test 20 nvidia/nemotron-3.5-super-vl:free`.

Kết quả 20 ảnh test: company 90%, date 100%, address 95%, total 100%.
