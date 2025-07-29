# app/schema/gmail_schema.py

from pydantic import BaseModel
from typing import Optional, List

class Email(BaseModel):
    id: str
    subject: str
    sender: str
    recipient: str
    body: str
    date: str
    labels: Optional[List[str]] = None
    has_attachments: bool = False

class SendEmailInput(BaseModel):
    to: str
    subject: str
    body: str
    cc: Optional[str] = None
    bcc: Optional[str] = None

class SendEmailOutput(BaseModel):
    success: bool
    message: str
    email_id: Optional[str] = None

class GetEmailsInput(BaseModel):
    query: Optional[str] = None
    max_results: int = 10
    label: Optional[str] = None

class GetEmailsOutput(BaseModel):
    success: bool
    message: str
    emails: Optional[List[Email]] = None

class ReadEmailInput(BaseModel):
    email_id: str

class ReadEmailOutput(BaseModel):
    success: bool
    message: str
    email: Optional[Email] = None

class SearchEmailsInput(BaseModel):
    query: str
    max_results: int = 10

class SearchEmailsOutput(BaseModel):
    success: bool
    message: str
    emails: Optional[List[Email]] = None

class DeleteEmailInput(BaseModel):
    email_id: str

class DeleteEmailOutput(BaseModel):
    success: bool
    message: str

class ReplyToEmailInput(BaseModel):
    email_id: str
    reply_body: str

class ReplyToEmailOutput(BaseModel):
    success: bool
    message: str
    reply_id: Optional[str] = None

class ForwardEmailInput(BaseModel):
    email_id: str
    forward_to: str
    additional_message: Optional[str] = None

class ForwardEmailOutput(BaseModel):
    success: bool
    message: str
    forward_id: Optional[str] = None

class GetLabelsInput(BaseModel):
    pass

class GetLabelsOutput(BaseModel):
    success: bool
    message: str
    labels: Optional[List[str]] = None

class MarkAsReadInput(BaseModel):
    email_id: str

class MarkAsReadOutput(BaseModel):
    success: bool
    message: str

class MarkAsUnreadInput(BaseModel):
    email_id: str

class MarkAsUnreadOutput(BaseModel):
    success: bool
    message: str 