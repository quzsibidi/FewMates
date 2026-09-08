from pydantic import BaseModel
from typing import List, Dict, Optional

class UserSchedulePayload(BaseModel):
    user_id: str
    zayif_dersler: List[str]
    dolu_saatler: Dict[str, List[str]]  # Örn: {"Pazartesi": ["08:30-15:30"]}
    gunluk_hedef_saat: int = 3

class ChatRequest(BaseModel):
    user_data: UserSchedulePayload
    message: str
    mode_instruction: Optional[str] = None

class ChatResponse(BaseModel):
    user_id: str
    response: str