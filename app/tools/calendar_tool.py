# app/tools/calendar_tool.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta


from langchain.tools import StructuredTool
from app.services.calendar_service import (
    schedule_event,
    delete_event,
    get_events,
    reschedule_event,
)
from app.schema.calendar_schema import (
    ScheduleEventInput,
    DeleteEventInput,
    GetEventsInput,
    RescheduleEventInput
)



class ListEventsInput(BaseModel):
    date: str  # YYYY-MM-DD


class CheckAvailabilityInput(BaseModel):
    date: str  # YYYY-MM-DD
    time: str  # HH:MM

class SuggestFreeTimeInput(BaseModel):
    date: str  # YYYY-MM-DD
    duration_minutes: int


def check_availability(date: str, time: str) -> str:
    input_data = GetEventsInput(start_date=date, end_date=date)
    events = get_events(input_data)
    
    if not events.success:
        return f"Error fetching events: {events.message}"
    
    # Basic check — time string match
    for event in events.events if events.events else []:
        if event.time == time:
            return f"❌ Not available — you have '{event.title}' at {time}."

    return f"✅ Available at {time} on {date}."

def schedule_event_wrapper(title: str, date: str, time: str, location: str = None) -> str:
    input_data = ScheduleEventInput(
        title=title,
        date=date,
        time=time,
        location=location
    )
    result = schedule_event(input_data)

    if result.success:
        return f"{result.message}\n📅 Event Link: {result.url}"
    else:
        return result.message


def list_events_by_day(date: str) -> str:
    input_data = GetEventsInput(start_date=date, end_date=date)
    result = get_events(input_data)
    return result.message

def delete_event_wrapper(title: str, date: str, time: str) -> str:
    input_data = DeleteEventInput(
        title=title,
        date=date,
        time=time
    )
    result = delete_event(input_data)
    return result.message


def get_events_wrapper(start_date: str, end_date: str) -> str:
    input_data = GetEventsInput(
        start_date=start_date,
        end_date=end_date
    )
    result = get_events(input_data)
    return result.message

def suggest_free_slots(date: str, duration_minutes: int) -> str:
    input_data = GetEventsInput(start_date=date, end_date=date)
    events_result = get_events(input_data)

    if not events_result.success:
        return f"Error: {events_result.message}"

    # Assume working hours are 09:00 to 18:00
    busy_times = [event.time for event in events_result.events] if events_result.events else []
    free_slots = []

    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    slot_duration = timedelta(minutes=duration_minutes)

    current_time = start_time
    while current_time + slot_duration <= end_time:
        time_str = current_time.strftime("%H:%M")
        if time_str not in busy_times:
            free_slots.append(time_str)
        current_time += timedelta(minutes=30)

    if not free_slots:
        return "😕 No available slots found for the specified duration."

    return "🆓 Available time slots:\n" + "\n".join(free_slots)

def reschedule_event_wrapper(
    title: str,
    original_date: str,
    original_time: str,
    new_date: str,
    new_time: str
) -> str:
    input_data = RescheduleEventInput(
        title=title,
        original_date=original_date,
        original_time=original_time,
        new_date=new_date,
        new_time=new_time
    )
    result = reschedule_event(input_data)

    # ✅ If rescheduling failed because event was not found — fallback to schedule
    if not result.success and "not found" in result.message.lower():
        fallback_input = ScheduleEventInput(
            title=title,
            date=new_date,
            time=new_time
        )
        fallback_result = schedule_event(fallback_input)
        return f"ℹ️ Original event not found. Created new one instead.\n{fallback_result.message}"

    return result.message


# 🎯 Tool: Create calendar event
calendar_tool = StructuredTool.from_function(
    name="schedule_event",
    description="Use this tool to schedule a calendar event given title, date, time, and optional location.",
    func=schedule_event_wrapper,
    args_schema=ScheduleEventInput,
    return_direct=True
)

# 🗑️ Tool: Delete calendar event
calendar_delete_tool = StructuredTool.from_function(
    name="delete_event",
    description="Use this tool to delete a calendar event by title, date, and time.",
    func=delete_event_wrapper,
    args_schema=DeleteEventInput,
    return_direct=True
)

list_day_events_tool = StructuredTool.from_function(
    name="list_day_events",
    description="List all events scheduled for a specific date.",
    func=list_events_by_day,
    args_schema=ListEventsInput,
    return_direct=True
)

# 📥 Tool: Get calendar events
calendar_get_events_tool = StructuredTool.from_function(
    name="get_events",
    description="Use this tool to get events from the calendar for a given date range.",
    func=get_events_wrapper,
    args_schema=GetEventsInput,
    return_direct=True
)

# 🔁 Tool: Reschedule calendar event
reschedule_event_tool = StructuredTool.from_function(
    name="reschedule_event",
    description=(
        "Use this tool to reschedule an existing calendar event. "
        "You must provide the event title, original date/time, and the new date/time."
    ),
    func=reschedule_event_wrapper,
    args_schema=RescheduleEventInput,
    return_direct=True
)


check_availability_tool = StructuredTool.from_function(
    name="check_availability",
    description="Check if a specific date and time is available for new events.",
    func=check_availability,
    args_schema=CheckAvailabilityInput,
    return_direct=True
)

suggest_free_slots_tool = StructuredTool.from_function(
    name="suggest_free_slots",
    description="Suggest available time slots for a given date and meeting duration.",
    func=suggest_free_slots,
    args_schema=SuggestFreeTimeInput,
    return_direct=True
)


