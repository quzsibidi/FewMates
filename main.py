import os
import json
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from google import genai
from google.genai import types
import aiofiles

from schemas import ChatRequest, DocumentUploadResponse
from prompts import SYSTEM_PROMPT, build_rag_prompt
from rag_service import process_and_index_pdf, query_rag_context

# Initialize Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

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

# --------------------------------------------------------------------------
# 1. RAG: DOCUMENT UPLOAD & INDEXING
# --------------------------------------------------------------------------
@app.post("/upload-pdf", response_model=DocumentUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF documents are supported.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
        
    try:
        chunks_count = process_and_index_pdf(file_path, file.filename)
        return DocumentUploadResponse(
            filename=file.filename,
            chunks_indexed=chunks_count,
            status="Document indexed successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

# --------------------------------------------------------------------------
# 2. SSE: REAL-TIME STREAMING CHAT
# --------------------------------------------------------------------------
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def event_generator():
        try:
            prompt_text = request.message
            
            # Fetch Context from Vector Store if RAG Enabled
            if request.use_rag:
                context = query_rag_context(request.message)
                prompt_text = build_rag_prompt(request.message, context)
            
            # Stream Response via Google GenAI SDK
            response = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=prompt_text,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                )
            )
            
            for chunk in response:
                if chunk.text:
                    data = json.dumps({"text": chunk.text}, ensure_ascii=False)
                    yield f"data: {data}\n\n"
                    await asyncio.sleep(0.01)
                    
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            error_data = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"data: {error_data}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)