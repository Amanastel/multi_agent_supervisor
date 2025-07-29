# app/services/calendar_service.py

import httpx
from datetime import datetime
from dateutil import parser
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import Optional
from app.schema.calendar_schema import (
    ScheduleEventInput, ScheduleEventOutput,
    DeleteEventInput, DeleteEventOutput,
    GetEventsInput, GetEventsOutput,
    Event, RescheduleEventInput,
)
from app.config import GOOGLE_CALENDAR_TOKEN




def get_calendar_service():
    credentials = Credentials(token=GOOGLE_CALENDAR_TOKEN)
    return build("calendar", "v3", credentials=credentials)


def get_events(input: GetEventsInput) -> GetEventsOutput:
    calendar_id = "primary"
    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

    headers = {
        "Authorization": f"Bearer {GOOGLE_CALENDAR_TOKEN}",
        "Content-Type": "application/json"
    }

    params = {
        "timeMin": f"{input.start_date}T00:00:00Z",
        "timeMax": f"{input.end_date}T23:59:59Z",
        "singleEvents": True,
        "orderBy": "startTime"
    }

    try:
        response = httpx.get(url, headers=headers, params=params)
        response.raise_for_status()
        events_raw = response.json().get("items", [])

        if not events_raw:
            return GetEventsOutput(success=True, message="📭 No events found in the given date range.")

        structured_events = []
        message_lines = ["📅 Upcoming events:"]

        for event in events_raw:
            title = event.get("summary", "No Title")
            start = event.get("start", {}).get("dateTime")
            location = event.get("location", "Virtual")

            if not start:
                continue

            dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
            structured_event = Event(
                title=title,
                date=dt.strftime("%Y-%m-%d"),
                time=dt.strftime("%H:%M"),
                location=location
            )
            structured_events.append(structured_event)
            message_lines.append(f"- {title} at {structured_event.time} on {structured_event.date}")

        return GetEventsOutput(
            success=True,
            message="\n".join(message_lines),
            events=structured_events
        )

    except Exception as e:
        return GetEventsOutput(success=False, message=f"❌ Error fetching events: {str(e)}")


def schedule_event(input: ScheduleEventInput) -> ScheduleEventOutput:
    calendar_id = "primary"
    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

    headers = {
        "Authorization": f"Bearer {GOOGLE_CALENDAR_TOKEN}",
        "Content-Type": "application/json"
    }

    event_payload = {
        "summary": input.title,
        "start": {
            "dateTime": f"{input.date}T{input.time}:00",
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": f"{input.date}T{input.time}:00",
            "timeZone": "Asia/Kolkata"
        },
        "location": input.location or "Virtual"
    }

    try:
        response = httpx.post(url, headers=headers, json=event_payload)
        response.raise_for_status()
        event_data = response.json()

        return ScheduleEventOutput(
            success=True,
            message="✅ Event successfully scheduled.",
            url=event_data.get("htmlLink")
        )

    except httpx.HTTPStatusError as e:
        return ScheduleEventOutput(success=False, message=f"❌ Google Calendar error: {e.response.text}")
    except Exception as ex:
        return ScheduleEventOutput(success=False, message=f"❌ Unexpected error: {str(ex)}")


def delete_event(input: DeleteEventInput) -> DeleteEventOutput:
    calendar_id = "primary"
    list_url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

    headers = {
        "Authorization": f"Bearer {GOOGLE_CALENDAR_TOKEN}",
        "Content-Type": "application/json"
    }

    time_min = f"{input.date}T00:00:00Z"
    time_max = f"{input.date}T23:59:59Z"

    try:
        list_response = httpx.get(list_url, headers=headers, params={
            "timeMin": time_min,
            "timeMax": time_max,
            "singleEvents": True,
            "orderBy": "startTime"
        })
        list_response.raise_for_status()
        events = list_response.json().get("items", [])

        for event in events:
            event_title = event.get("summary", "")
            start = event.get("start", {}).get("dateTime", "")

            if input.title.lower() in event_title.lower() and input.time in start:
                event_id = event["id"]
                delete_url = f"{list_url}/{event_id}"
                delete_response = httpx.delete(delete_url, headers=headers)
                delete_response.raise_for_status()

                return DeleteEventOutput(
                    success=True,
                    message=f"🗑️ Event '{input.title}' at {input.time} on {input.date} deleted successfully."
                )

        return DeleteEventOutput(success=False, message="❌ No matching event found.")
    except httpx.HTTPStatusError as e:
        return DeleteEventOutput(success=False, message=f"❌ Google Calendar error: {e.response.text}")
    except Exception as ex:
        return DeleteEventOutput(success=False, message=f"❌ Unexpected error: {str(ex)}")


def reschedule_event(input: RescheduleEventInput) -> ScheduleEventOutput:
    try:
        service = get_calendar_service()

        events_result = service.events().list(
            calendarId='primary',
            timeMin=f"{input.original_date}T00:00:00Z",
            timeMax=f"{input.original_date}T23:59:59Z",
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get("items", [])
        matched_event = None

        for event in events:
            title = event.get("summary", "")
            start_time_str = event.get("start", {}).get("dateTime", "")

            if not start_time_str:
                continue

            try:
                start_dt = parser.isoparse(start_time_str)
                start_date = start_dt.strftime("%Y-%m-%d")
                start_time_formatted = start_dt.strftime("%H:%M")
            except Exception:
                continue

            if (
                input.title.lower() in title.lower()
                and input.original_date == start_date
                and input.original_time == start_time_formatted
            ):
                matched_event = event
                break

        if not matched_event:
            return ScheduleEventOutput(success=False, message="❌ Event not found to reschedule.")

        event_id = matched_event.get("id")

        updated_event = {
            'summary': input.title,
            'start': {
                'dateTime': f"{input.new_date}T{input.new_time}:00",
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': f"{input.new_date}T{input.new_time}:00",
                'timeZone': 'Asia/Kolkata',
            },
        }

        service.events().update(calendarId='primary', eventId=event_id, body=updated_event).execute()

        return ScheduleEventOutput(success=True, message="🔁 Event rescheduled successfully.")

    except Exception as e:
        return ScheduleEventOutput(success=False, message=f"❌ Error: {str(e)}")
