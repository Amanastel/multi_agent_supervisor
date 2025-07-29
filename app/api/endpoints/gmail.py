# app/api/endpoints/gmail.py

from fastapi import APIRouter, HTTPException
from app.schema.gmail_schema import (
    SendEmailInput, SendEmailOutput,
    GetEmailsInput, GetEmailsOutput,
    ReadEmailInput, ReadEmailOutput,
    SearchEmailsInput, SearchEmailsOutput,
    DeleteEmailInput, DeleteEmailOutput,
    ReplyToEmailInput, ReplyToEmailOutput,
    ForwardEmailInput, ForwardEmailOutput,
    GetLabelsInput, GetLabelsOutput,
    MarkAsReadInput, MarkAsReadOutput,
    MarkAsUnreadInput, MarkAsUnreadOutput
)
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

router = APIRouter(prefix="/gmail", tags=["gmail"])

@router.post("/send", response_model=SendEmailOutput)
async def send_email_endpoint(input: SendEmailInput):
    """Send an email"""
    result = send_email(input)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return result

@router.post("/get", response_model=GetEmailsOutput)
async def get_emails_endpoint(input: GetEmailsInput):
    """Get emails from Gmail"""
    result = get_emails(input)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return result

@router.post("/read", response_model=ReadEmailOutput)
async def read_email_endpoint(input: ReadEmailInput):
    """Read a specific email"""
    result = read_email(input)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return result

@router.post("/search", response_model=SearchEmailsOutput)
async def search_emails_endpoint(input: SearchEmailsInput):
    """Search emails"""
    result = search_emails(input)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return result

@router.delete("/delete", response_model=DeleteEmailOutput)
async def delete_email_endpoint(input: DeleteEmailInput):
    """Delete an email"""
    result = delete_email(input)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return result

@router.post("/reply", response_model=ReplyToEmailOutput)
async def reply_to_email_endpoint(input: ReplyToEmailInput):
    """Reply to an email"""
    result = reply_to_email(input)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return result

@router.post("/forward", response_model=ForwardEmailOutput)
async def forward_email_endpoint(input: ForwardEmailInput):
    """Forward an email"""
    result = forward_email(input)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return result

@router.get("/labels", response_model=GetLabelsOutput)
async def get_labels_endpoint():
    """Get all Gmail labels"""
    input_data = GetLabelsInput()
    result = get_labels(input_data)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return result

@router.post("/mark-read", response_model=MarkAsReadOutput)
async def mark_as_read_endpoint(input: MarkAsReadInput):
    """Mark an email as read"""
    result = mark_as_read(input)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return result

@router.post("/mark-unread", response_model=MarkAsUnreadOutput)
async def mark_as_unread_endpoint(input: MarkAsUnreadInput):
    """Mark an email as unread"""
    result = mark_as_unread(input)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return result 