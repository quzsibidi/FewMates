import os
import json
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from google import genai
from google.genai import types

from schemas import ChatRequest, ChatResponse
from prompts import build_system_instruction

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY bulunamadı! .env dosyasını kontrol edin.")

client = genai.Client(api_key=API_KEY)

app = FastAPI(title="Okul & Ders Danışmanı API")

def load_school_data(filepath: str = "okul_data.json") -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.dumps(json.load(f), ensure_ascii=False, indent=2)
    except FileNotFoundError:
        return "{'bilgi': 'Genel okul verisi yüklenmedi.'}"

SCHOOL_INFO = load_school_data()

# Web Arayüzü Ana Sayfası
@app.get("/")
async def get_index():
    return FileResponse("index.html")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        user_dict = request.user_data.model_dump()
        
        system_instruction = build_system_instruction(
            school_info=SCHOOL_INFO,
            user_data=user_dict,
            mode_instruction=request.mode_instruction
        )
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction
        )
        
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=request.message,
            config=config
        )
        
        return ChatResponse(
            user_id=request.user_data.user_id,
            response=response.text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API Hatası: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)