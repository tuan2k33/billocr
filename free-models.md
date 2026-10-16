# Model free trên OpenRouter (lấy từ /api/v1/models)

| Model | Context | Input |
|---|---|---|
| cohere/north-mini-code:free | 256000 | text |
| dots-studio/dots-3-note-preview:free | 512000 | text,image |
| google/gemma-4-26b-a4b-it:free | 262144 | image,text,video |
| google/gemma-4-31b-it:free | 262144 | image,text,video |
| liquid/lfm-2.5-2.6b:free | 65536 | text |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | 256000 | text,audio,image,video |
| nvidia/nemotron-3-super-120b-a12b:free | 262144 | text |
| nvidia/nemotron-3-ultra-550b-a55b:free | 1000000 | text |
| nvidia/nemotron-3.5-content-safety:free | 128000 | text,image |
| nvidia/nemotron-3.5-lightning:free | 1000000 | text |
| nvidia/nemotron-3.5-super-vl:free | 1000000 | text,image,video |
| poolside/laguna-s-2.1:free | 262144 | text |
| poolside/laguna-xs-2.1:free | 262144 | text |
| thinkingmachines/inkling-small:free | 1048576 | text,image,audio |
| thinkingmachines/inkling:free | 1048576 | text,image,audio |

## Router free
- `openrouter/free`: tự chọn ngẫu nhiên một model free phù hợp với request (ảnh, tool calling, structured output...), context 200K.

## Embedding free (endpoint `/api/v1/embeddings`)
- `liquid/lfm-2.5-embedding-350m:free`
- `nvidia/nemotron-3-embed-1b:free`
- `nvidia/llama-nemotron-embed-vl-1b-v2:free`

## Loại khác (có trên trang web, không có trong /models; chưa kiểm tra cách gọi)
- `nvidia/llama-nemotron-rerank-vl-1b-v2:free`: rerank
- `inception/mercury-decide:free`: ra quyết định có xác suất, schema `/v1/systemone`
- `respan/span-01-lite:free`: chấm điểm hành vi hội thoại
- `fish-audio/s2.1-pro-free`: tổng hợp giọng nói (TTS)
