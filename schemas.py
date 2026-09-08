from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class UserSchedulePayload(BaseModel):
    user_id: str
    weak_courses: List[str]
    busy_hours: Dict[str, List[str]]
    daily_target_hours: float

class ChatRequest(BaseModel):
    session_id: Optional[str] = "default_session"
    user_data: UserSchedulePayload
    message: str
    mode_instruction: Optional[str] = None
    language: Optional[str] = "tr"

class ChatResponse(BaseModel):
    user_id: str
    session_id: str
    response: str