# app/api/endpoints/unified.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.agents.unified_agent import run_unified_agent

router = APIRouter(prefix="/unified", tags=["unified"])

class UnifiedRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = None

class UnifiedResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None

@router.post("/chat", response_model=UnifiedResponse)
async def unified_chat_endpoint(request: UnifiedRequest):
    """
    Unified chat endpoint that handles both calendar and Gmail operations.
    
    This endpoint provides a single conversational interface for:
    - Calendar operations (schedule, reschedule, delete events, etc.)
    - Gmail operations (send, read, search, reply to emails, etc.)
    - Combined workflows (e.g., "Check my calendar and send a summary to the team")
    
    Examples:
    - "Schedule a meeting with John tomorrow at 2 PM"
    - "Send an email to john@example.com about the meeting"
    - "What emails do I have from alice@company.com?"
    - "Check my calendar for tomorrow and send a summary to the team"
    - "Reschedule my 3 PM meeting to 4 PM"
    """
    try:
        # Run the unified agent
        response = run_unified_agent(request.prompt)
        
        return UnifiedResponse(
            response=response,
            success=True
        )
        
    except Exception as e:
        return UnifiedResponse(
            response="I encountered an error while processing your request.",
            success=False,
            error=str(e)
        )

@router.get("/health")
async def health_check():
    """Health check endpoint for the unified agent"""
    return {
        "status": "healthy",
        "service": "unified-agent",
        "capabilities": [
            "calendar-management",
            "email-management",
            "combined-workflows"
        ]
    }

@router.get("/capabilities")
async def get_capabilities():
    """Get information about available capabilities"""
    return {
        "calendar_operations": {
            "schedule_event": "Schedule calendar events with title, date, time, and location",
            "delete_event": "Delete calendar events by title, date, and time",
            "get_events": "Get events for a date range",
            "reschedule_event": "Reschedule existing events",
            "check_availability": "Check availability for specific times",
            "list_day_events": "List events for a specific day",
            "suggest_free_slots": "Suggest free time slots for meetings"
        },
        "gmail_operations": {
            "send_email": "Send emails with subject, body, CC, and BCC",
            "get_emails": "Get recent emails with filtering",
            "read_email": "Read specific emails by ID",
            "search_emails": "Search emails using Gmail search syntax",
            "reply_to_email": "Reply to emails with automatic threading",
            "forward_email": "Forward emails to other recipients",
            "delete_email": "Delete emails by ID",
            "mark_as_read": "Mark emails as read",
            "mark_as_unread": "Mark emails as unread",
            "get_labels": "Get all Gmail labels"
        },
        "combined_workflows": {
            "calendar_to_email": "Check calendar and send email summaries",
            "email_to_calendar": "Create calendar events from email content",
            "scheduling_workflow": "Schedule meetings and send invitations",
            "follow_up_workflow": "Send follow-up emails after meetings"
        },
        "search_syntax": {
            "gmail_search": "from:john@example.com, subject:meeting, is:unread, has:attachment",
            "date_formats": "YYYY-MM-DD for dates, HH:MM for times",
            "examples": [
                "Schedule a meeting with John tomorrow at 2 PM",
                "Send an email to john@example.com about the meeting",
                "What emails do I have from alice@company.com?",
                "Check my calendar for tomorrow and send a summary to the team"
            ]
        }
    } 