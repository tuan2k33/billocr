# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mục đích

Ứng dụng LLM đọc ảnh hóa đơn (bill OCR) và trả JSON 4 trường `company`, `date`, `address`, `total`, đánh giá trên SROIE 2019. Gọi model qua OpenRouter (SDK `openai`, `base_url=https://openrouter.ai/api/v1`). Chỉ dùng model `:free`; key chỉ cho phép chi tiêu gần $0 nên model trả phí sẽ không chạy.

## Lệnh

Venv ở `.venv` (symlink tới `~/.dev/venvs/openrouter`, tạo bằng `/mnt/c/Dev/env/mkproj`). Cài gói: `uv pip install --python .venv/bin/python <gói>`.

- Gọi thử một prompt: `.venv/bin/python main.py [model] [prompt]`
- Đánh giá: `.venv/bin/python ocr_eval.py <train|test> <số ảnh> [model]`, ví dụ `ocr_eval.py test 20 nvidia/nemotron-3.5-super-vl:free`
- Còn bao nhiêu request free hôm nay: `GET https://openrouter.ai/api/v1/key` (trường `free_model_daily_requests`)

Không có test hay lint.

## Kiến trúc

- `main.py`: ví dụ chat tối thiểu.
- `ocr_eval.py`: mỗi ảnh một request (ảnh resize tối đa 1600px, base64), parse JSON từ câu trả lời, so với `data/<split>/entities/<id>.txt`. Kết quả ghi nối tiếp vào `results_<split>.jsonl`, chạy lại sẽ bỏ qua ảnh đã có (xoá file này khi đổi prompt hoặc model để đo lại). Chấm: `date` và `total` khớp tuyệt đối sau chuẩn hóa, `company` và `address` khớp gần đúng (độ giống ≥ 0.9) vì nhãn SROIE có lỗi chính tả.
- `data/`: SROIE2019 (`train` 626 ảnh, `test` 347 ảnh; mỗi split có `img/`, `entities/`, `box/`) cùng `layoutlm-base-uncased` đã fine-tune, hiện chưa dùng. Đã ignore khỏi git.
- `free-models.md`: danh sách model free (chat, embedding, loại khác) lấy từ OpenRouter; thay đổi theo thời gian.

## Lưu ý

- Key trong `.env` (`OPENROUTER_API_KEY`), đã ignore.
- Giới hạn free: 20 request/phút, 1000/ngày (tài khoản đã nạp ≥ $10), dùng chung mọi model free; request lỗi cũng bị tính. Script sleep 3.5s giữa các request và retry khi 429.
- Không dùng `openrouter/free` để đo độ chính xác: router chọn model ngẫu nhiên, có lần trúng model không đọc được ảnh (ví dụ content-safety). Dùng model cố định có input ảnh: `nvidia/nemotron-3.5-super-vl:free` chạy ổn; `google/gemma-4-31b-it:free` hay bị 429 từ upstream.
