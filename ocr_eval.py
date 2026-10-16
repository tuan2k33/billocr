import base64
import io
import json
import os
import re
import sys
import time
from difflib import SequenceMatcher
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError
from PIL import Image

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

FIELDS = ["company", "date", "address", "total"]
PROMPT = """Đọc hóa đơn trong ảnh và trả về DUY NHẤT một JSON, không giải thích, không markdown, đúng 4 khóa sau:
- "company": tên công ty/cửa hàng ở dòng đầu hóa đơn, in hoa như trên hóa đơn, không kèm địa chỉ và không kèm mã đăng ký trong ngoặc (ví dụ bỏ "(S19537-X)"). Nếu có hai dòng tên thì lấy dòng đầu.
- "date": chỉ ngày, không có giờ, giữ định dạng in trên hóa đơn (ví dụ "25/12/2018").
- "address": địa chỉ đầy đủ trên một dòng, nối các dòng bằng dấu phẩy.
- "total": tổng tiền cuối cùng khách phải trả (sau thuế, sau làm tròn), chỉ chữ số và dấu chấm, không đơn vị tiền tệ, ví dụ "9.00".
Không thấy trường nào thì để chuỗi rỗng."""

split = sys.argv[1]
n = int(sys.argv[2])
model = sys.argv[3] if len(sys.argv) > 3 else "openrouter/free"
root = Path("data") / split
out_path = Path(f"results_{split}.jsonl")


def encode(path):
    img = Image.open(path).convert("RGB")
    img.thumbnail((1600, 1600))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m.group(0)) if m else {}


def norm(field, v):
    v = re.sub(r"\s+", " ", str(v or "")).strip().upper()
    if field == "total":
        v = re.sub(r"[^0-9.]", "", v)
        try:
            return f"{float(v):.2f}"
        except ValueError:
            return v
    return v


def same(field, a, b):
    a, b = norm(field, a), norm(field, b)
    if field in ("company", "address"):
        return SequenceMatcher(None, a, b).ratio() >= 0.9
    return a == b


def ask(path):
    for attempt in range(4):
        try:
            r = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": PROMPT},
                    {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + encode(path)}},
                ]}],
            )
            return r.model, r.choices[0].message.content
        except RateLimitError:
            time.sleep(10 * (attempt + 1))
    raise RuntimeError("rate limited")


done = {}
if out_path.exists():
    for line in out_path.read_text().splitlines():
        d = json.loads(line)
        done[d["id"]] = d

imgs = sorted((root / "img").glob("*.jpg"))[:n]
with out_path.open("a") as f:
    for p in imgs:
        if p.stem in done:
            continue
        truth = json.loads((root / "entities" / f"{p.stem}.txt").read_text())
        try:
            used, text = ask(p)
            pred = parse(text)
        except Exception as e:
            print(p.stem, "ERROR", str(e)[:100])
            continue
        rec = {"id": p.stem, "model": used, "pred": pred, "truth": truth}
        done[p.stem] = rec
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f.flush()
        ok = [same(k, pred.get(k), truth.get(k)) for k in FIELDS]
        print(p.stem, used, "".join("Y" if x else "n" for x in ok))
        time.sleep(3.5)

recs = [done[p.stem] for p in imgs if p.stem in done]
if recs:
    print(f"\n{len(recs)} ảnh")
    for k in FIELDS:
        c = sum(same(k, r["pred"].get(k), r["truth"].get(k)) for r in recs)
        print(f"{k}: {c}/{len(recs)} = {c/len(recs):.0%}")
