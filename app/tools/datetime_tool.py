# app/tools/datetime_tool.py

from langchain.tools import StructuredTool, tool
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import dateparser


class ExtractDatetimeInput(BaseModel):
    text: str


class ExtractDatetimeOutput(BaseModel):
    success: bool
    message: str
    date: Optional[str] = None  # YYYY-MM-DD
    time: Optional[str] = None  # HH:MM (24-hour format)

# FIXED: Accept raw string instead of BaseModel
def extract_datetime_from_text(text: str) -> ExtractDatetimeOutput:
    parsed = dateparser.parse(text)

    if not parsed:
        return ExtractDatetimeOutput(
            success=False,
            message="Could not parse date or time from the text."
        )

    return ExtractDatetimeOutput(
        success=True,
        message="Datetime parsed successfully.",
        date=parsed.strftime("%Y-%m-%d"),
        time=parsed.strftime("%H:%M") if parsed.hour or parsed.minute else None
    )


@tool
def get_current_datetime() -> str:
    """Returns the current date and time."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

datetime_extraction_tool = StructuredTool.from_function(
    name="extract_datetime",
    description="Use this tool to extract date and time from natural language input. For example: 'tomorrow at 3pm', 'next Friday', etc.",
    func=extract_datetime_from_text,
    args_schema=ExtractDatetimeInput,
    return_direct=False
)
