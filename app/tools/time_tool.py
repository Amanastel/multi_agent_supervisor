# app/tools/time_tool.py
from datetime import datetime
from langchain.tools import StructuredTool
from pydantic import BaseModel
from typing import Optional
import dateparser
from dateparser.search import search_dates

# Schema for datetime extraction
class ExtractDatetimeInput(BaseModel):
    text: str

class ExtractDatetimeOutput(BaseModel):
    success: bool
    message: str
    date: Optional[str] = None  # YYYY-MM-DD
    time: Optional[str] = None  # HH:MM

# Function to extract datetime from natural language
def extract_datetime_from_text(text: str) -> ExtractDatetimeOutput:
    # First attempt direct parsing
    parsed = dateparser.parse(text, settings={"PREFER_DATES_FROM": "future"})

    if parsed:
        return ExtractDatetimeOutput(
            success=True,
            message="✅ Datetime parsed successfully.",
            date=parsed.strftime("%Y-%m-%d"),
            time=parsed.strftime("%H:%M") if parsed.hour or parsed.minute else None
        )

    # If direct parsing fails, try search_dates
    results = search_dates(text, settings={"PREFER_DATES_FROM": "future"})
    if results:
        _, parsed = results[0]
        return ExtractDatetimeOutput(
            success=True,
            message="✅ Datetime parsed using fallback search.",
            date=parsed.strftime("%Y-%m-%d"),
            time=parsed.strftime("%H:%M") if parsed.hour or parsed.minute else None
        )

    # Final fallback
    return ExtractDatetimeOutput(
        success=False,
        message="❌ Could not parse date or time from the text.",
        date=None,
        time=None
    )

# Tool for extracting datetime
extract_datetime = StructuredTool.from_function(
    func=extract_datetime_from_text,
    name="extract_datetime",
    description="Use this tool to extract date and time from natural language like 'next Monday at 5pm'.",
    args_schema=ExtractDatetimeInput,
    return_direct=False
)

# Tool for getting current datetime
get_current_datetime_tool = StructuredTool.from_function(
    func=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    name="get_current_datetime",
    description="Returns the current date and time in 'YYYY-MM-DD HH:MM:SS' format."
)
