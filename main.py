import os
import json
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
from openai import OpenAI
import aiofiles

from schemas import ChatRequest, DocumentUploadResponse
from prompts import SYSTEM_PROMPT, build_rag_prompt
from rag_service import process_and_index_pdf, query_rag_context

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")  # Groq: https://api.groq.com/openai/v1
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

if not API_KEY:
    print("\n[HATA] OPENAI_API_KEY yok! .env dosyasına ekle.\n")
    print("  Groq (ücretsiz): https://console.groq.com/keys")
    print("  OpenAI: https://platform.openai.com/api-keys\n")
else:
    tag = "OpenAI"
    if BASE_URL and "groq" in BASE_URL:
        tag = "Groq"
    elif BASE_URL and "openrouter" in BASE_URL:
        tag = "OpenRouter"
    print(f"\n[BİLGİ] {tag} | model={MODEL_NAME} | key={API_KEY[:8]}...\n")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL) if API_KEY else None

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(title="FewMates Academic Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = Path(__file__).resolve().parent / "index.html"
    if index_path.exists():
        return index_path.read_text(encoding="utf-8")
    return "<h1>FewMates API</h1><p>index.html bulunamadı. /docs adresini dene.</p>"


# --------------------------------------------------------------------------
# 1. RAG: DOCUMENT UPLOAD & INDEXING
# --------------------------------------------------------------------------
@app.post("/upload-pdf", response_model=DocumentUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF documents are supported.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    try:
        chunks_count = process_and_index_pdf(file_path, file.filename)
        return DocumentUploadResponse(
            filename=file.filename,
            chunks_indexed=chunks_count,
            status="Document indexed successfully.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")


# --------------------------------------------------------------------------
# 2. SSE: REAL-TIME STREAMING CHAT
# --------------------------------------------------------------------------
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    if not client:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY tanımlı değil.")

    async def event_generator():
        try:
            prompt_text = request.message

            if request.use_rag:
                context = query_rag_context(request.message)
                prompt_text = build_rag_prompt(request.message, context)

            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_text},
                ],
                stream=True,
            )

            for chunk in stream:
                text = chunk.choices[0].delta.content or ""
                if text:
                    data = json.dumps({"text": text}, ensure_ascii=False)
                    yield f"data: {data}\n\n"
                    await asyncio.sleep(0.01)

            yield "data: [DONE]\n\n"

        except Exception as e:
            error_data = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"data: {error_data}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# --------------------------------------------------------------------------
# 3. Basit JSON chat (frontend /api/chat için)
# --------------------------------------------------------------------------
@app.post("/api/chat")
async def chat_json(request: ChatRequest):
    if not client:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY tanımlı değil.")

    try:
        prompt_text = request.message
        if request.use_rag:
            context = query_rag_context(request.message)
            prompt_text = build_rag_prompt(request.message, context)

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text},
            ],
        )
        answer = completion.choices[0].message.content or ""
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)