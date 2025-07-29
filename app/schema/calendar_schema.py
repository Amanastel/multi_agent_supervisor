# app/schema/calendar_schema.py

from pydantic import BaseModel, Field
from typing import Optional, List, Union

class Event(BaseModel):
    title: str
    date: str  # Format: "YYYY-MM-DD"
    time: str  # Format: "HH:MM"
    location: Optional[str] = None


class ScheduleEventInput(BaseModel):
    title: str
    date: str  # Format: "YYYY-MM-DD"
    time: str  # Format: "HH:MM"
    location: Optional[str] = None

class ScheduleEventOutput(BaseModel):
    success: bool
    message: str
    url: str | None = None

class DeleteEventInput(BaseModel):
    title: str
    date: str  # format: YYYY-MM-DD
    time: str  # format: HH:MM

class DeleteEventOutput(BaseModel):
    success: bool
    message: str


class GetEventsInput(BaseModel):
    start_date: str  # Format: "YYYY-MM-DD"
    end_date: str    # Format: "YYYY-MM-DD"

class GetEventsOutput(BaseModel):
    success: bool
    message: str
    events: Optional[List[Event]] = None  # ✅ Fix here



class RescheduleEventInput(BaseModel):
    title: str
    original_date: str  # e.g. "2025-07-25"
    original_time: str  # e.g. "14:30"
    new_date: str       # e.g. "2025-07-26"
    new_time: str       # e.g. "16:00"


class RescheduleEventOutput(BaseModel):
    success: bool
    message: str

class UpdateCalendarEventInput(BaseModel):
    current_title: str
    current_date: str
    current_time: Optional[str] = None
    new_title: Optional[str] = None
    new_date: Optional[str] = None
    new_time: Optional[str] = None
    new_description: Optional[str] = None
    new_location: Optional[str] = None
