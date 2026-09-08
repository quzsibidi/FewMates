import os
import json
import aiofiles
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

from schemas import ChatRequest, ChatResponse
from prompts import build_system_instruction
from database import init_db, save_message, get_session_history, delete_session, add_exam, get_exams

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY error! Check your .env file.")

client = genai.Client(api_key=API_KEY)

app = FastAPI(title="AI School & Study Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

async def load_json_file_async(filepath: str, fallback_json: str) -> str:
    try:
        async with aiofiles.open(filepath, mode="r", encoding="utf-8") as f:
            content = await f.read()
            return json.dumps(json.loads(content), ensure_ascii=False, indent=2)
    except FileNotFoundError:
        return fallback_json

@app.get("/")
async def get_index():
    return FileResponse("index.html")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        school_info = await load_json_file_async("okul_data.json", '{"info": "School data not loaded."}')
        user_dict = request.user_data.model_dump()
        session_id = request.session_id or "default_session"
        
        system_instruction = build_system_instruction(
            school_info=school_info,
            user_data=user_dict,
            mode_instruction=request.mode_instruction
        )
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction
        )
        
        save_message(session_id, "user", request.message)
        history = get_session_history(session_id)
        
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=history,
            config=config
        )
        
        save_message(session_id, "model", response.text)
        
        return ChatResponse(
            user_id=request.user_data.user_id,
            session_id=session_id,
            response=response.text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API Error: {str(e)}")

@app.delete("/api/chat/clear/{session_id}")
async def clear_chat_history(session_id: str):
    success = delete_session(session_id)
    if success:
        return {"status": "success", "message": f"Session {session_id} cleared from database."}
    return {"status": "not_found", "message": f"Session {session_id} does not exist."}

class ExamRequest(BaseModel):
    session_id: str
    title: str
    course: str
    date: str

@app.post("/api/exams")
async def create_exam(exam: ExamRequest):
    add_exam(exam.session_id, exam.title, exam.course, exam.date)
    return {"status": "success", "message": f"Exam '{exam.title}' added."}

@app.get("/api/exams/{session_id}")
async def list_exams(session_id: str):
    exams = get_exams(session_id)
    return {"session_id": session_id, "exams": [{"title": r[0], "course": r[1], "date": r[2]} for r in exams]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)