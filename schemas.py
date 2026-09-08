from pydantic import BaseModel
from typing import List

class ScheduleSlot(BaseModel):
    day: str
    busy_slots: List[str]
    subjects_today: List[str]

class UserProfile(BaseModel):
    weak_subjects: List[str]
    daily_study_target_hours: int = 3
    preferred_study_time: str = "evening"

class StudyPlanRequest(BaseModel):
    user_id: str
    weekly_schedule: List[ScheduleSlot]
    user_profile: UserProfile