import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

model = sys.argv[1] if len(sys.argv) > 1 else "openrouter/auto"
prompt = sys.argv[2] if len(sys.argv) > 2 else "Xin chào, trả lời ngắn gọn."

resp = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": prompt}],
)
print(resp.model)
print(resp.choices[0].message.content)
