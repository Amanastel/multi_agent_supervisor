# app/api/endpoints/calendar.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.calendar_agent import get_calendar_agent

router = APIRouter()

class CalendarRequest(BaseModel):
    prompt: str

@router.post("/calendar/schedule")
async def schedule_with_calendar_agent(request: CalendarRequest):
    try:
        agent = get_calendar_agent()
        result = agent.invoke({"input": request.prompt})
        # ✅ Extract only the final plain response string (no HTML)
        if isinstance(result, dict) and "output" in result:
            return {"response": result["output"]}
        else:
            return {"response": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

