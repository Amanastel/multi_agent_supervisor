# app/tools/gmail_tool.py

from pydantic import BaseModel
from typing import Optional
from langchain.tools import StructuredTool
from app.services.gmail_service import (
    send_email,
    get_emails,
    read_email,
    search_emails,
    delete_email,
    reply_to_email,
    forward_email,
    get_labels,
    mark_as_read,
    mark_as_unread
)
from app.schema.gmail_schema import (
    SendEmailInput,
    GetEmailsInput,
    ReadEmailInput,
    SearchEmailsInput,
    DeleteEmailInput,
    ReplyToEmailInput,
    ForwardEmailInput,
    GetLabelsInput,
    MarkAsReadInput,
    MarkAsUnreadInput
)

# Input models for tools
class SendEmailToolInput(BaseModel):
    to: str
    subject: str
    body: str
    cc: Optional[str] = None
    bcc: Optional[str] = None

class GetEmailsToolInput(BaseModel):
    query: Optional[str] = None
    max_results: int = 10
    label: Optional[str] = None

class ReadEmailToolInput(BaseModel):
    email_id: str

class SearchEmailsToolInput(BaseModel):
    query: str
    max_results: int = 10

class DeleteEmailToolInput(BaseModel):
    email_id: str

class ReplyToEmailToolInput(BaseModel):
    email_id: str
    reply_body: str

class ForwardEmailToolInput(BaseModel):
    email_id: str
    forward_to: str
    additional_message: Optional[str] = None

class MarkAsReadToolInput(BaseModel):
    email_id: str

class MarkAsUnreadToolInput(BaseModel):
    email_id: str

# Tool wrapper functions
def send_email_wrapper(to: str, subject: str, body: str, cc: Optional[str] = None, bcc: Optional[str] = None) -> str:
    """Send an email"""
    input_data = SendEmailInput(
        to=to,
        subject=subject,
        body=body,
        cc=cc,
        bcc=bcc
    )
    result = send_email(input_data)
    return result.message

def get_emails_wrapper(query: Optional[str] = None, max_results: int = 10, label: Optional[str] = None) -> str:
    """Get emails from Gmail"""
    input_data = GetEmailsInput(
        query=query,
        max_results=max_results,
        label=label
    )
    result = get_emails(input_data)
    return result.message

def read_email_wrapper(email_id: str) -> str:
    """Read a specific email by ID"""
    input_data = ReadEmailInput(email_id=email_id)
    result = read_email(input_data)
    return result.message

def search_emails_wrapper(query: str, max_results: int = 10) -> str:
    """Search emails using Gmail search syntax"""
    input_data = SearchEmailsInput(
        query=query,
        max_results=max_results
    )
    result = search_emails(input_data)
    return result.message

def delete_email_wrapper(email_id: str) -> str:
    """Delete an email by ID"""
    input_data = DeleteEmailInput(email_id=email_id)
    result = delete_email(input_data)
    return result.message

def reply_to_email_wrapper(email_id: str, reply_body: str) -> str:
    """Reply to an email"""
    input_data = ReplyToEmailInput(
        email_id=email_id,
        reply_body=reply_body
    )
    result = reply_to_email(input_data)
    return result.message

def forward_email_wrapper(email_id: str, forward_to: str, additional_message: Optional[str] = None) -> str:
    """Forward an email"""
    input_data = ForwardEmailInput(
        email_id=email_id,
        forward_to=forward_to,
        additional_message=additional_message
    )
    result = forward_email(input_data)
    return result.message

def get_labels_wrapper() -> str:
    """Get all Gmail labels"""
    input_data = GetLabelsInput()
    result = get_labels(input_data)
    return result.message

def mark_as_read_wrapper(email_id: str) -> str:
    """Mark an email as read"""
    input_data = MarkAsReadInput(email_id=email_id)
    result = mark_as_read(input_data)
    return result.message

def mark_as_unread_wrapper(email_id: str) -> str:
    """Mark an email as unread"""
    input_data = MarkAsUnreadInput(email_id=email_id)
    result = mark_as_unread(input_data)
    return result.message

# LangChain Tools
send_email_tool = StructuredTool.from_function(
    name="send_email",
    description="Send an email using Gmail. Provide recipient email, subject, and body. Optionally include CC and BCC.",
    func=send_email_wrapper,
    args_schema=SendEmailToolInput,
    return_direct=True
)

get_emails_tool = StructuredTool.from_function(
    name="get_emails",
    description="Get emails from Gmail. You can specify a query, max results, and label to filter emails.",
    func=get_emails_wrapper,
    args_schema=GetEmailsToolInput,
    return_direct=True
)

read_email_tool = StructuredTool.from_function(
    name="read_email",
    description="Read a specific email by its ID. Use this after getting email IDs from get_emails or search_emails.",
    func=read_email_wrapper,
    args_schema=ReadEmailToolInput,
    return_direct=True
)

search_emails_tool = StructuredTool.from_function(
    name="search_emails",
    description="Search emails using Gmail search syntax. Examples: 'from:john@example.com', 'subject:meeting', 'is:unread'.",
    func=search_emails_wrapper,
    args_schema=SearchEmailsToolInput,
    return_direct=True
)

delete_email_tool = StructuredTool.from_function(
    name="delete_email",
    description="Delete an email by its ID. Use this after getting email IDs from get_emails or search_emails.",
    func=delete_email_wrapper,
    args_schema=DeleteEmailToolInput,
    return_direct=True
)

reply_to_email_tool = StructuredTool.from_function(
    name="reply_to_email",
    description="Reply to an email by its ID. Provide the email ID and your reply message.",
    func=reply_to_email_wrapper,
    args_schema=ReplyToEmailToolInput,
    return_direct=True
)

forward_email_tool = StructuredTool.from_function(
    name="forward_email",
    description="Forward an email to another recipient. Provide the email ID, recipient email, and optional additional message.",
    func=forward_email_wrapper,
    args_schema=ForwardEmailToolInput,
    return_direct=True
)

get_labels_tool = StructuredTool.from_function(
    name="get_labels",
    description="Get all available Gmail labels. Useful for filtering emails by label.",
    func=get_labels_wrapper,
    args_schema=GetLabelsInput,
    return_direct=True
)

mark_as_read_tool = StructuredTool.from_function(
    name="mark_as_read",
    description="Mark an email as read by its ID.",
    func=mark_as_read_wrapper,
    args_schema=MarkAsReadToolInput,
    return_direct=True
)

mark_as_unread_tool = StructuredTool.from_function(
    name="mark_as_unread",
    description="Mark an email as unread by its ID.",
    func=mark_as_unread_wrapper,
    args_schema=MarkAsUnreadToolInput,
    return_direct=True
) 