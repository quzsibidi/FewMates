import os
import json
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types

from schemas import ChatRequest, ChatResponse
from prompts import build_system_instruction

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY error! Check your .env file.")

client = genai.Client(api_key=API_KEY)

app = FastAPI(title="AI School & Study Assistant API")

# CORS Middleware Configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session store for managing chat history in memory
SESSION_STORE: dict[str, list[types.Content]] = {}

def load_json_file(filepath: str, fallback_json: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.dumps(json.load(f), ensure_ascii=False, indent=2)
    except FileNotFoundError:
        return fallback_json

SCHOOL_INFO = load_json_file("okul_data.json", '{"info": "School data not loaded."}')
DEFAULT_USER_DATA = load_json_file("user_data.json", '{"info": "User data not loaded."}')

@app.get("/")
async def get_index():
    return FileResponse("index.html")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        user_dict = request.user_data.model_dump()
        session_id = request.session_id or "default_session"
        
        system_instruction = build_system_instruction(
            school_info=SCHOOL_INFO,
            user_data=user_dict,
            mode_instruction=request.mode_instruction
        )
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction
        )
        
        if session_id not in SESSION_STORE:
            SESSION_STORE[session_id] = []
            
        history = SESSION_STORE[session_id]
        
        history.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=request.message)]
            )
        )
        
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=history,
            config=config
        )
        
        history.append(
            types.Content(
                role="model",
                parts=[types.Part.from_text(text=response.text)]
            )
        )
        
        return ChatResponse(
            user_id=request.user_data.user_id,
            session_id=session_id,
            response=response.text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API Error: {str(e)}")

@app.delete("/api/chat/clear/{session_id}")
async def clear_chat_history(session_id: str):
    if session_id in SESSION_STORE:
        del SESSION_STORE[session_id]
        return {"status": "success", "message": f"Session {session_id} cleared."}
    return {"status": "not_found", "message": f"Session {session_id} does not exist."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)