from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class UserSchedulePayload(BaseModel):
    user_id: str
    weak_courses: List[str] = Field(default_factory=list)
    busy_hours: Dict[str, List[str]] = Field(default_factory=dict)
    daily_target_hours: int = 2

class ChatMessage(BaseModel):
    role: str  # "user" veya "model"
    content: str

class ChatRequest(BaseModel):
    session_id: Optional[str] = "default_session"
    user_data: UserSchedulePayload
    message: str
    mode_instruction: Optional[str] = "Respond in English. Be direct, clear, and supportive."
    history: Optional[List[ChatMessage]] = Field(default_factory=list)

class ChatResponse(BaseModel):
    user_id: str
    session_id: str
    response: str